"""
Train application & reply classifiers.

MLOps:
  - Log params / metrics / artifacts to MLflow
  - Register models in the Model Registry
  - Publish joblib to MODEL_DIR only if quality gate passes
    (CV F1 >= MIN_F1 and not worse than previous published model by more than MARGIN)
"""

from __future__ import annotations

import json
import logging
import os
from collections import Counter
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import psycopg
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

from ml_embedding import SentenceEmbedder, DEFAULT_MODEL_NAME

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
MODEL_DIR = Path(os.getenv("MODEL_DIR", "/app/models"))
MODEL_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", DEFAULT_MODEL_NAME)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MLFLOW_EXPERIMENT = os.getenv("MLFLOW_EXPERIMENT_NAME", "jobtracker-classification")

# Quality gate: only publish joblib if CV F1 is good enough
MIN_F1_TO_PUBLISH = float(os.getenv("MIN_F1_TO_PUBLISH", "0.80"))
# Reject if new F1 is worse than previous published by more than this margin
MAX_F1_REGRESSION = float(os.getenv("MAX_F1_REGRESSION", "0.03"))

OUTPUT_NAMES = {
    "APPLICATION": "application_model.joblib",
    "REPLY": "reply_model.joblib",
}
REGISTERED_NAMES = {
    "APPLICATION": "jobtracker-application-model",
    "REPLY": "jobtracker-reply-model",
}
META_NAMES = {
    "APPLICATION": "application_model.meta.json",
    "REPLY": "reply_model.meta.json",
}


def build_model() -> Pipeline:
    return Pipeline(
        [
            ("embed", SentenceEmbedder(model_name=EMBEDDING_MODEL_NAME)),
            (
                "clf",
                LogisticRegression(
                    C=1.0,
                    max_iter=2000,
                    class_weight="balanced",
                    solver="lbfgs",
                ),
            ),
        ]
    )


def load_examples(task: str) -> tuple[list[str], list[str]]:
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            """
            SELECT text, label
            FROM training_examples
            WHERE task = %s
            ORDER BY id
            """,
            (task,),
        ).fetchall()

    rows = [
        (text.strip(), label)
        for text, label in rows
        if text and text.strip() and label
    ]

    if len(rows) < 10:
        raise RuntimeError(
            f"Not enough {task} examples: {len(rows)} found; at least 10 required."
        )

    texts = [r[0] for r in rows]
    labels = [r[1] for r in rows]
    counts = Counter(labels)

    if len(counts) < 2:
        raise RuntimeError(
            f"{task} requires at least two distinct labels; found {dict(counts)}"
        )

    logger.info("Task=%s  examples=%d  distribution=%s", task, len(rows), dict(counts))
    return texts, labels


def read_previous_f1(task: str) -> float | None:
    meta_path = MODEL_DIR / META_NAMES[task]
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        return float(data["cv_f1_macro_mean"])
    except Exception:
        logger.warning("Could not read previous meta %s", meta_path)
        return None


def quality_gate(task: str, cv_f1: float | None) -> tuple[bool, str]:
    """
    Return (publish?, reason).
    - Must have a CV score
    - CV F1 >= MIN_F1_TO_PUBLISH
    - If a previous published score exists, new must not regress by more than MAX_F1_REGRESSION
    """
    if cv_f1 is None:
        return False, "no CV F1 (insufficient data per class)"

    if cv_f1 < MIN_F1_TO_PUBLISH:
        return (
            False,
            f"CV F1 {cv_f1:.3f} < MIN_F1_TO_PUBLISH {MIN_F1_TO_PUBLISH:.3f}",
        )

    prev = read_previous_f1(task)
    if prev is not None and cv_f1 < prev - MAX_F1_REGRESSION:
        return (
            False,
            f"CV F1 {cv_f1:.3f} regresses vs previous {prev:.3f} "
            f"(max allowed drop {MAX_F1_REGRESSION:.3f})",
        )

    if prev is None:
        return True, f"CV F1 {cv_f1:.3f} OK (first publish)"
    return True, f"CV F1 {cv_f1:.3f} OK (previous {prev:.3f})"


def publish_joblib(task: str, model, output_name: str, cv_f1: float, run_id: str) -> None:
    path = MODEL_DIR / output_name
    joblib.dump(model, path)
    meta = {
        "task": task,
        "cv_f1_macro_mean": cv_f1,
        "mlflow_run_id": run_id,
        "embedding_model": EMBEDDING_MODEL_NAME,
    }
    meta_path = MODEL_DIR / META_NAMES[task]
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    logger.info("PUBLISHED joblib %s → %s (cv_f1=%.3f)", task, path, cv_f1)


def train(task: str, output_name: str) -> None:
    texts, labels = load_examples(task)
    counts = Counter(labels)
    registered_name = REGISTERED_NAMES[task]

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)

    with mlflow.start_run(run_name=f"train-{task.lower()}") as run:
        run_id = run.info.run_id
        logger.info("MLflow run_id=%s task=%s", run_id, task)

        mlflow.log_param("task", task)
        mlflow.log_param("embedding_model", EMBEDDING_MODEL_NAME)
        mlflow.log_param("n_examples", len(texts))
        mlflow.log_param("n_labels", len(counts))
        mlflow.log_param("min_f1_to_publish", MIN_F1_TO_PUBLISH)
        mlflow.log_param("max_f1_regression", MAX_F1_REGRESSION)
        for label, count in counts.items():
            mlflow.log_param(f"count_{label}", count)

        cv_f1: float | None = None
        smallest = min(counts.values())
        if smallest >= 2:
            n_splits = min(5, smallest)
            cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            scores = cross_val_score(
                build_model(),
                texts,
                labels,
                cv=cv,
                scoring="f1_macro",
                error_score="raise",
            )
            cv_f1 = float(scores.mean())
            logger.info(
                "%s CV F1-macro: %.3f ± %.3f  folds=%s",
                task,
                scores.mean(),
                scores.std(),
                [round(float(s), 3) for s in scores],
            )
            mlflow.log_metric("cv_f1_macro_mean", cv_f1)
            mlflow.log_metric("cv_f1_macro_std", float(scores.std()))
            mlflow.log_param("cv_folds", n_splits)
        else:
            logger.warning("%s: label with only one example – CV skipped.", task)

        model = build_model()
        model.fit(texts, labels)

        preds = model.predict(texts)
        train_f1 = f1_score(labels, preds, average="macro", zero_division=0)
        mlflow.log_metric("train_f1_macro", float(train_f1))

        report = classification_report(labels, preds, zero_division=0)
        print(report)
        mlflow.log_text(report, "classification_report.txt")

        # Always register in MLflow (history), even if not published to worker
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn_model",
            registered_model_name=registered_name,
        )

        publish, reason = quality_gate(task, cv_f1)
        mlflow.log_param("publish_to_worker", publish)
        mlflow.log_param("publish_reason", reason)
        logger.info("Quality gate [%s]: publish=%s – %s", task, publish, reason)

        if publish and cv_f1 is not None:
            publish_joblib(task, model, output_name, cv_f1, run_id)
            mlflow.log_artifact(str(MODEL_DIR / output_name), artifact_path="joblib")
            # Optional: tag this run
            mlflow.set_tag("stage", "published")
        else:
            logger.warning(
                "NOT publishing %s to MODEL_DIR – worker keeps previous model. (%s)",
                task,
                reason,
            )
            mlflow.set_tag("stage", "rejected_by_gate")


def main() -> None:
    logger.info("MODEL_DIR=%s  embedding=%s", MODEL_DIR, EMBEDDING_MODEL_NAME)
    logger.info(
        "MLflow URI=%s  experiment=%s",
        MLFLOW_TRACKING_URI,
        MLFLOW_EXPERIMENT,
    )
    logger.info(
        "Gate: MIN_F1_TO_PUBLISH=%.3f  MAX_F1_REGRESSION=%.3f",
        MIN_F1_TO_PUBLISH,
        MAX_F1_REGRESSION,
    )

    for task, name in OUTPUT_NAMES.items():
        try:
            train(task, name)
        except RuntimeError as exc:
            logger.error("Skipping %s: %s", task, exc)


if __name__ == "__main__":
    main()
