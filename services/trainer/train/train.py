"""Train application & reply classifiers → joblib files in MODEL_DIR."""

from __future__ import annotations

import logging
import os
from collections import Counter
from pathlib import Path

import joblib
import psycopg
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
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

OUTPUT_NAMES = {
    "APPLICATION": "application_model.joblib",
    "REPLY": "reply_model.joblib",
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


def train(task: str, output_name: str) -> None:
    texts, labels = load_examples(task)
    counts = Counter(labels)
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
        logger.info(
            "%s CV F1-macro: %.3f ± %.3f  folds=%s",
            task,
            scores.mean(),
            scores.std(),
            [round(float(s), 3) for s in scores],
        )
    else:
        logger.warning("%s: label with only one example – CV skipped.", task)

    model = build_model()
    model.fit(texts, labels)

    preds = model.predict(texts)
    print(classification_report(labels, preds, zero_division=0))

    path = MODEL_DIR / output_name
    joblib.dump(model, path)
    logger.info("Saved %s → %s", task, path)


def main() -> None:
    logger.info("MODEL_DIR=%s  embedding=%s", MODEL_DIR, EMBEDDING_MODEL_NAME)
    for task, name in OUTPUT_NAMES.items():
        try:
            train(task, name)
        except RuntimeError as exc:
            logger.error("Skipping %s: %s", task, exc)


if __name__ == "__main__":
    main()
