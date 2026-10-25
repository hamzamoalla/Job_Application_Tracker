"""
Train application & reply classifiers.

MLOps:
  - Log params / metrics / artifacts to MLflow
  - Register models in the Model Registry
  - Publish joblib to MODEL_DIR only if quality gate passes
    (CV F1 >= MIN_F1 and not worse than previous published model by more than MARGIN)

Workflow interactif (après démarrage du conteneur) :
  1) Choisir la tâche : APPLICATION, REPLY, ou les deux
  2) Pour chaque tâche : évaluer TOUS les candidats (CV)
  3) Afficher le classement numéroté (F1 décroissant)
  4) Saisir le NUMÉRO du candidat à publier
  5) Fit final + quality gate + publish joblib

Mode non-interactif (CI / sans TTY) :
  - TASKS=APPLICATION,REPLY
  - PUBLISH_APPLICATION_CANDIDATE=<clé>  (optionnel ; sinon meilleur score)
  - PUBLISH_REPLY_CANDIDATE=<clé>        (optionnel ; sinon meilleur score)
  - ou SKIP_PUBLISH=1 pour comparaison seule
"""

from __future__ import annotations

import json
import logging
import os
import sys
from collections import Counter
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import psycopg
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from ml_embedding import (
    ChunkAttentionClassifier,
    ChunkPoolingEmbedder,
    SentenceEmbedder,
    DEFAULT_MODEL_NAME,
    split_sentences,
)
from text_cleaning import prepare_ml_text, prepare_ml_text_full

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

MIN_F1_TO_PUBLISH = float(os.getenv("MIN_F1_TO_PUBLISH", "0.80"))
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

MODEL_TEXT_SOURCE = {
    "APPLICATION": "truncated",
    "REPLY": "full",
}


# ---------------------------------------------------------------------------
# Classifieurs partagés
# ---------------------------------------------------------------------------

def _logreg_clf():
    return GridSearchCV(
        LogisticRegression(max_iter=2000, class_weight="balanced", solver="lbfgs"),
        param_grid={"C": [0.1, 0.3, 1.0, 3.0, 10.0]},
        cv=3,
        scoring="f1_macro",
    )


def _linear_svm_clf():
    base = LinearSVC(C=1.0, class_weight="balanced", max_iter=5000)
    return CalibratedClassifierCV(base, cv=3)


def _knn_clf():
    return KNeighborsClassifier(n_neighbors=5, weights="distance", metric="cosine")


CLASSIFIERS = {
    "logreg_gridsearch_C": _logreg_clf,
    "linear_svm_calibrated": _linear_svm_clf,
    "knn5_cosine": _knn_clf,
}


# ---------------------------------------------------------------------------
# APPLICATION — stratégies × classifieurs
# ---------------------------------------------------------------------------

def _build_strategy_embedder(strategy: str):
    if strategy == "truncate_600":
        return SentenceEmbedder(model_name=EMBEDDING_MODEL_NAME)
    if strategy == "chunk_sentence":
        return ChunkPoolingEmbedder(model_name=EMBEDDING_MODEL_NAME, strategy="sentence")
    if strategy == "chunk_window_300":
        return ChunkPoolingEmbedder(
            model_name=EMBEDDING_MODEL_NAME, strategy="window", window_size=300, overlap=100
        )
    if strategy == "chunk_word_60":
        return ChunkPoolingEmbedder(
            model_name=EMBEDDING_MODEL_NAME, strategy="word", window_size=60, overlap=20
        )
    if strategy == "chunk_sentence_max":
        return ChunkPoolingEmbedder(
            model_name=EMBEDDING_MODEL_NAME, strategy="sentence", pooling="max"
        )
    if strategy == "chunk_sentence_topk3":
        return ChunkPoolingEmbedder(
            model_name=EMBEDDING_MODEL_NAME,
            strategy="sentence",
            pooling="mean_topk",
            topk=3,
        )
    raise ValueError(f"Stratégie inconnue: {strategy!r}")


STRATEGIES_USE_FULL_TEXT = {
    "chunk_sentence",
    "chunk_window_300",
    "chunk_word_60",
    "chunk_sentence_max",
    "chunk_sentence_topk3",
}

STRATEGIES = [
    "truncate_600",
    "chunk_sentence",
    "chunk_window_300",
    "chunk_word_60",
    "chunk_sentence_max",
    "chunk_sentence_topk3",
]

ATTENTION_CANDIDATES = {
    "chunk_sentence_attention_joint": lambda: ChunkAttentionClassifier(
        model_name=EMBEDDING_MODEL_NAME, strategy="sentence"
    ),
}


def evaluate_application_candidates(
    texts_truncated: list[str], texts_full: list[str], labels: list[str], cv: StratifiedKFold
) -> dict[str, dict]:
    """Mesure F1 CV de chaque stratégie × classifieur (+ attention)."""
    results: dict[str, dict] = {}
    for strategy in STRATEGIES:
        texts_for = texts_full if strategy in STRATEGIES_USE_FULL_TEXT else texts_truncated
        try:
            embedder = _build_strategy_embedder(strategy)
            embeddings = embedder.fit_transform(texts_for)
        except Exception as exc:
            logger.warning("  stratégie %-18s embedding échoué: %s", strategy, exc)
            continue
        for clf_name, build_clf in CLASSIFIERS.items():
            key = f"{strategy}__{clf_name}"
            try:
                scores = cross_val_score(
                    build_clf(), embeddings, labels, cv=cv, scoring="f1_macro", error_score="raise"
                )
                results[key] = {
                    "f1_mean": float(scores.mean()),
                    "f1_std": float(scores.std()),
                }
                logger.info(
                    "  %-40s CV F1-macro: %.3f ± %.3f", key, scores.mean(), scores.std()
                )
            except Exception as exc:
                logger.warning("  %-40s échoué: %s", key, exc)

    for name, build_att in ATTENTION_CANDIDATES.items():
        try:
            scores = cross_val_score(
                build_att(), texts_full, labels, cv=cv, scoring="f1_macro", error_score="raise"
            )
            results[name] = {
                "f1_mean": float(scores.mean()),
                "f1_std": float(scores.std()),
            }
            logger.info(
                "  %-40s CV F1-macro: %.3f ± %.3f  [EXPÉRIMENTAL]",
                name,
                scores.mean(),
                scores.std(),
            )
        except Exception as exc:
            logger.warning("  %-40s échoué: %s", name, exc)
    return results


def build_application_candidate(key: str):
    if key in ATTENTION_CANDIDATES:
        return ATTENTION_CANDIDATES[key]()
    for strategy in STRATEGIES:
        prefix = f"{strategy}__"
        if key.startswith(prefix):
            clf_name = key[len(prefix) :]
            if clf_name in CLASSIFIERS:
                return Pipeline(
                    [
                        ("embed", _build_strategy_embedder(strategy)),
                        ("clf", CLASSIFIERS[clf_name]()),
                    ]
                )
    raise ValueError(f"Candidat APPLICATION inconnu: {key!r}")


def application_text_for_key(key: str, texts_truncated, texts_full):
    """Quel corpus (tronqué / full) utiliser pour le fit final d'un candidat APP."""
    if key in ATTENTION_CANDIDATES:
        return texts_full
    for strategy in STRATEGIES_USE_FULL_TEXT:
        if key.startswith(strategy + "__"):
            return texts_full
    return texts_truncated


# ---------------------------------------------------------------------------
# REPLY — pooling × classifieur (découpage figé "sentence")
# ---------------------------------------------------------------------------

REPLY_POOLING_METHODS = ["mean", "max", "mean_topk", "em_local"]
REPLY_STATEFUL_POOLING_METHODS = ["em_global"]
REPLY_ATTENTION_KEY = "sentence_attention_joint"


def _build_reply_pooling_embedder(pooling: str) -> ChunkPoolingEmbedder:
    kwargs: dict = {}
    if pooling == "mean_topk":
        kwargs["topk"] = 3
    if pooling in ("em_local", "em_global"):
        kwargs["em_components"] = 2
    return ChunkPoolingEmbedder(
        model_name=EMBEDDING_MODEL_NAME, strategy="sentence", pooling=pooling, **kwargs
    )


def evaluate_reply_candidates(
    texts_full: list[str], labels: list[str], cv: StratifiedKFold
) -> dict[str, dict]:
    results: dict[str, dict] = {}

    for pooling in REPLY_POOLING_METHODS:
        try:
            embedder = _build_reply_pooling_embedder(pooling)
            embeddings = embedder.fit_transform(texts_full)
        except Exception as exc:
            logger.warning("  pooling %-10s embedding échoué: %s", pooling, exc)
            continue
        for clf_name, build_clf in CLASSIFIERS.items():
            key = f"sentence_{pooling}__{clf_name}"
            try:
                scores = cross_val_score(
                    build_clf(),
                    embeddings,
                    labels,
                    cv=cv,
                    scoring="f1_macro",
                    error_score="raise",
                )
                results[key] = {
                    "f1_mean": float(scores.mean()),
                    "f1_std": float(scores.std()),
                }
                logger.info(
                    "  %-40s CV F1-macro: %.3f ± %.3f", key, scores.mean(), scores.std()
                )
            except Exception as exc:
                logger.warning("  %-40s échoué: %s", key, exc)

    for pooling in REPLY_STATEFUL_POOLING_METHODS:
        for clf_name, build_clf in CLASSIFIERS.items():
            key = f"sentence_{pooling}__{clf_name}"
            try:
                pipeline = Pipeline(
                    [
                        ("embed", _build_reply_pooling_embedder(pooling)),
                        ("clf", build_clf()),
                    ]
                )
                scores = cross_val_score(
                    pipeline,
                    texts_full,
                    labels,
                    cv=cv,
                    scoring="f1_macro",
                    error_score="raise",
                )
                results[key] = {
                    "f1_mean": float(scores.mean()),
                    "f1_std": float(scores.std()),
                }
                logger.info(
                    "  %-40s CV F1-macro: %.3f ± %.3f", key, scores.mean(), scores.std()
                )
            except Exception as exc:
                logger.warning("  %-40s échoué: %s", key, exc)

    try:
        scores = cross_val_score(
            ChunkAttentionClassifier(
                model_name=EMBEDDING_MODEL_NAME, strategy="sentence"
            ),
            texts_full,
            labels,
            cv=cv,
            scoring="f1_macro",
            error_score="raise",
        )
        results[REPLY_ATTENTION_KEY] = {
            "f1_mean": float(scores.mean()),
            "f1_std": float(scores.std()),
        }
        logger.info(
            "  %-40s CV F1-macro: %.3f ± %.3f  [EXPÉRIMENTAL]",
            REPLY_ATTENTION_KEY,
            scores.mean(),
            scores.std(),
        )
    except Exception as exc:
        logger.warning("  %-40s échoué: %s", REPLY_ATTENTION_KEY, exc)

    return results


def build_reply_candidate(key: str):
    if key == REPLY_ATTENTION_KEY:
        return ChunkAttentionClassifier(
            model_name=EMBEDDING_MODEL_NAME, strategy="sentence"
        )
    for pooling in REPLY_POOLING_METHODS + REPLY_STATEFUL_POOLING_METHODS:
        prefix = f"sentence_{pooling}__"
        if key.startswith(prefix):
            clf_name = key[len(prefix) :]
            if clf_name in CLASSIFIERS:
                return Pipeline(
                    [
                        ("embed", _build_reply_pooling_embedder(pooling)),
                        ("clf", CLASSIFIERS[clf_name]()),
                    ]
                )
    raise ValueError(f"Candidat REPLY inconnu: {key!r}")


# ---------------------------------------------------------------------------
# Affichage / sélection interactive
# ---------------------------------------------------------------------------

def rank_candidates(results: dict[str, dict]) -> list[tuple[str, dict]]:
    return sorted(results.items(), key=lambda kv: -kv[1]["f1_mean"])


def print_ranked_candidates(task: str, ranked: list[tuple[str, dict]]) -> None:
    print()
    print("=" * 90)
    print(f"  CANDIDATS {task} — classement par F1 CV (décroissant)")
    print("=" * 90)
    print(f"  {'#':>3}  {'clé':45s}  {'F1 moyen':>10s}  {'± std':>8s}")
    print("-" * 90)
    for i, (key, score) in enumerate(ranked, start=1):
        tag = "  [EXPÉRIMENTAL]" if "attention" in key else ""
        print(
            f"  {i:3d}  {key:45s}  {score['f1_mean']:10.3f}  {score['f1_std']:8.3f}{tag}"
        )
    print("=" * 90)
    print("  Saisissez le NUMÉRO du candidat à publier (ou 0 pour ne rien publier).")
    print()


def write_candidates_report(
    path: Path, task: str, ranked: list[tuple[str, dict]]
) -> None:
    lines = [
        "=" * 90,
        f"COMPARATIF CANDIDATS {task}",
        "=" * 90,
        "",
        f"{'#':>3}  {'clé':45s}  {'F1 moyen':>10s}  {'± std':>8s}",
        "-" * 90,
    ]
    for i, (key, score) in enumerate(ranked, start=1):
        tag = "  [EXPÉRIMENTAL]" if "attention" in key else ""
        lines.append(
            f"{i:3d}  {key:45s}  {score['f1_mean']:10.3f}  {score['f1_std']:8.3f}{tag}"
        )
    lines.append("")
    lines.append(
        "Écart < 0.01–0.02 entre deux têtes de liste n'est pas forcément significatif "
        "avec un petit jeu de données."
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_interactive() -> bool:
    if os.getenv("TRAIN_NONINTERACTIVE", "").strip() in ("1", "true", "yes"):
        return False
    return sys.stdin.isatty()


def prompt_tasks() -> list[str]:
    """Choisir APPLICATION / REPLY / les deux — avant tout entraînement."""
    env_tasks = os.getenv("TASKS", "").strip().upper()
    if env_tasks:
        mapping = {
            "APPLICATION": ["APPLICATION"],
            "APP": ["APPLICATION"],
            "REPLY": ["REPLY"],
            "BOTH": ["APPLICATION", "REPLY"],
            "ALL": ["APPLICATION", "REPLY"],
            "APPLICATION,REPLY": ["APPLICATION", "REPLY"],
            "REPLY,APPLICATION": ["APPLICATION", "REPLY"],
        }
        if env_tasks in mapping:
            return mapping[env_tasks]
        parts = [p.strip() for p in env_tasks.split(",") if p.strip()]
        out = []
        for p in parts:
            if p in ("APPLICATION", "APP"):
                out.append("APPLICATION")
            elif p == "REPLY":
                out.append("REPLY")
        if out:
            return out

    if not is_interactive():
        logger.info("Non-interactif : TASKS non défini → APPLICATION + REPLY")
        return ["APPLICATION", "REPLY"]

    print()
    print("=" * 60)
    print("  Quelle tâche entraîner ?")
    print("=" * 60)
    print("  1  APPLICATION  (emails envoyés / candidatures)")
    print("  2  REPLY        (réponses reçues)")
    print("  3  Les deux")
    print()
    while True:
        raw = input("  Votre choix [1/2/3] : ").strip()
        if raw == "1":
            return ["APPLICATION"]
        if raw == "2":
            return ["REPLY"]
        if raw == "3":
            return ["APPLICATION", "REPLY"]
        print("  → Entrez 1, 2 ou 3.")


def prompt_candidate_number(
    task: str,
    ranked: list[tuple[str, dict]],
    env_key: str,
) -> str | None:
    """
    Retourne la clé du candidat choisi, ou None (= ne rien publier).
    - Interactif : saisie d'un numéro
    - Non-interactif : env PUBLISH_*_CANDIDATE, sinon meilleur score
    """
    if not ranked:
        return None

    env_val = os.getenv(env_key, "").strip()
    if env_val:
        if env_val in ("0", "none", "NONE", "skip"):
            return None
        # numéro ou clé
        if env_val.isdigit():
            n = int(env_val)
            if 1 <= n <= len(ranked):
                return ranked[n - 1][0]
            raise ValueError(f"{env_key}={env_val} hors plage 1..{len(ranked)}")
        keys = {k for k, _ in ranked}
        if env_val not in keys:
            raise ValueError(
                f"{env_key}={env_val!r} inconnu. Clés: {', '.join(sorted(keys))}"
            )
        return env_val

    if os.getenv("SKIP_PUBLISH", "").strip() in ("1", "true", "yes"):
        logger.info("%s — SKIP_PUBLISH=1 : comparaison seule, pas de publication", task)
        return None

    if not is_interactive():
        best = ranked[0][0]
        logger.info(
            "%s — non-interactif, pas de %s → publication du #1 : %s (F1=%.3f)",
            task,
            env_key,
            best,
            ranked[0][1]["f1_mean"],
        )
        return best

    print_ranked_candidates(task, ranked)
    while True:
        raw = input(f"  Numéro pour {task} [1-{len(ranked)}, 0=rien] : ").strip()
        if not raw:
            continue
        if not raw.isdigit():
            print("  → Entrez un entier.")
            continue
        n = int(raw)
        if n == 0:
            return None
        if 1 <= n <= len(ranked):
            key = ranked[n - 1][0]
            print(f"  → Sélectionné : #{n}  {key}  (F1={ranked[n - 1][1]['f1_mean']:.3f})")
            return key
        print(f"  → Hors plage (1..{len(ranked)} ou 0).")


# ---------------------------------------------------------------------------
# Données / gate / publish
# ---------------------------------------------------------------------------

def log_chunking_diagnostics(task: str, texts_full: list[str]) -> None:
    if not texts_full:
        return
    chunk_counts = [len(split_sentences(t)) or 1 for t in texts_full]
    avg_chunks = sum(chunk_counts) / len(chunk_counts)
    pct_single = 100 * sum(1 for c in chunk_counts if c <= 1) / len(chunk_counts)
    logger.info(
        "%s — diagnostic données: chunks/phrase moyens=%.1f (%.0f%% à 1 seule phrase)",
        task,
        avg_chunks,
        pct_single,
    )
    mlflow.log_metric("train_data_avg_sentence_chunks", avg_chunks)
    mlflow.log_metric("train_data_pct_single_chunk", pct_single)


def load_examples(task: str) -> tuple[list[str], list[str], list[str]]:
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            """
            SELECT subject, text, label
            FROM training_examples
            WHERE task = %s
            ORDER BY id
            """,
            (task,),
        ).fetchall()

    rows = [
        (subject or "", text.strip(), label)
        for subject, text, label in rows
        if text and text.strip() and label
    ]
    if len(rows) < 10:
        raise RuntimeError(
            f"Not enough {task} examples: {len(rows)} found; at least 10 required."
        )

    texts_truncated = [prepare_ml_text(subject, text) for subject, text, _ in rows]
    texts_full = [prepare_ml_text_full(subject, text) for subject, text, _ in rows]
    labels = [r[2] for r in rows]
    counts = Counter(labels)
    if len(counts) < 2:
        raise RuntimeError(
            f"{task} requires at least two distinct labels; found {dict(counts)}"
        )
    logger.info("Task=%s  examples=%d  distribution=%s", task, len(rows), dict(counts))
    return texts_truncated, texts_full, labels


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


def publish_joblib(
    task: str, model, output_name: str, cv_f1: float, run_id: str, candidate_key: str
) -> None:
    path = MODEL_DIR / output_name
    joblib.dump(model, path)
    meta = {
        "task": task,
        "cv_f1_macro_mean": cv_f1,
        "mlflow_run_id": run_id,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "model_text_source": MODEL_TEXT_SOURCE[task],
        "candidate_key": candidate_key,
    }
    meta_path = MODEL_DIR / META_NAMES[task]
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    logger.info(
        "PUBLISHED joblib %s → %s (cv_f1=%.3f, candidate=%s)",
        task,
        path,
        cv_f1,
        candidate_key,
    )


# ---------------------------------------------------------------------------
# Train APPLICATION
# ---------------------------------------------------------------------------

def train_application(output_name: str) -> None:
    task = "APPLICATION"
    texts, texts_full, labels = load_examples(task)
    counts = Counter(labels)
    registered_name = REGISTERED_NAMES[task]

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)

    with mlflow.start_run(run_name="train-application") as run:
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

        smallest = min(counts.values())
        if smallest < 2:
            logger.warning("%s: label with only one example – CV skipped.", task)
            mlflow.set_tag("stage", "cv_skipped")
            return

        n_splits = min(5, smallest)
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        mlflow.log_param("cv_folds", n_splits)

        logger.info("%s — évaluation de TOUS les candidats…", task)
        results = evaluate_application_candidates(texts, texts_full, labels, cv)
        for key, score in results.items():
            mlflow.log_metric(f"cv_f1_candidate_{key}", score["f1_mean"])

        if not results:
            logger.error("%s — aucun candidat évalué.", task)
            mlflow.set_tag("stage", "no_candidate_evaluated")
            return

        ranked = rank_candidates(results)
        report_path = MODEL_DIR / "application_candidates_report.txt"
        write_candidates_report(report_path, task, ranked)
        mlflow.log_artifact(str(report_path), artifact_path="reports")
        logger.info("%s — rapport: %s", task, report_path)

        selected_key = prompt_candidate_number(
            task, ranked, "PUBLISH_APPLICATION_CANDIDATE"
        )
        if not selected_key:
            logger.info(
                "%s — aucun candidat sélectionné. Modèle précédent conservé.", task
            )
            mlflow.set_tag("stage", "comparison_only")
            return

        cv_f1 = results[selected_key]["f1_mean"]
        mlflow.log_param("selected_candidate", selected_key)
        mlflow.log_metric("cv_f1_macro_mean", cv_f1)
        mlflow.log_metric("cv_f1_macro_std", results[selected_key]["f1_std"])

        model_texts = application_text_for_key(selected_key, texts, texts_full)
        # Cohérence worker : si on publie un candidat full-text, documenter
        text_src = "full" if model_texts is texts_full else "truncated"
        MODEL_TEXT_SOURCE[task] = text_src
        mlflow.log_param("model_text_source", text_src)

        model = build_application_candidate(selected_key)
        model.fit(model_texts, labels)

        preds = model.predict(model_texts)
        train_f1 = f1_score(labels, preds, average="macro", zero_division=0)
        mlflow.log_metric("train_f1_macro", float(train_f1))
        report = classification_report(labels, preds, zero_division=0)
        print(report)
        mlflow.log_text(report, "classification_report.txt")

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn_model",
            registered_model_name=registered_name,
        )

        publish, reason = quality_gate(task, cv_f1)
        mlflow.log_param("publish_to_worker", publish)
        mlflow.log_param("publish_reason", reason)
        logger.info("Quality gate [%s]: publish=%s – %s", task, publish, reason)

        if publish:
            publish_joblib(
                task, model, output_name, cv_f1, run_id, selected_key
            )
            mlflow.log_artifact(str(MODEL_DIR / output_name), artifact_path="joblib")
            mlflow.set_tag("stage", "published")
        else:
            logger.warning(
                "NOT publishing %s (candidat %s) – %s", task, selected_key, reason
            )
            mlflow.set_tag("stage", "rejected_by_gate")


# ---------------------------------------------------------------------------
# Train REPLY
# ---------------------------------------------------------------------------

def train_reply(output_name: str) -> None:
    task = "REPLY"
    texts, texts_full, labels = load_examples(task)
    counts = Counter(labels)
    registered_name = REGISTERED_NAMES[task]
    model_texts = texts_full

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)

    with mlflow.start_run(run_name="train-reply") as run:
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

        smallest = min(counts.values())
        if smallest < 2:
            logger.warning("%s: label with only one example – CV skipped.", task)
            mlflow.set_tag("stage", "cv_skipped")
            return

        n_splits = min(5, smallest)
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        mlflow.log_param("cv_folds", n_splits)

        log_chunking_diagnostics(task, texts_full)

        logger.info(
            "%s — évaluation de TOUS les candidats (pooling × classifieur)…", task
        )
        results = evaluate_reply_candidates(texts_full, labels, cv)
        for key, score in results.items():
            mlflow.log_metric(f"cv_f1_candidate_{key}", score["f1_mean"])

        if not results:
            logger.error("%s — aucun candidat évalué.", task)
            mlflow.set_tag("stage", "no_candidate_evaluated")
            return

        ranked = rank_candidates(results)
        report_path = MODEL_DIR / "reply_candidates_report.txt"
        write_candidates_report(report_path, task, ranked)
        mlflow.log_artifact(str(report_path), artifact_path="reports")
        logger.info("%s — rapport: %s", task, report_path)

        selected_key = prompt_candidate_number(
            task, ranked, "PUBLISH_REPLY_CANDIDATE"
        )
        if not selected_key:
            logger.info(
                "%s — aucun candidat sélectionné. Modèle précédent conservé.", task
            )
            mlflow.set_tag("stage", "comparison_only")
            return

        cv_f1 = results[selected_key]["f1_mean"]
        mlflow.log_param("selected_candidate", selected_key)
        mlflow.log_metric("cv_f1_macro_mean", cv_f1)
        mlflow.log_metric("cv_f1_macro_std", results[selected_key]["f1_std"])

        model = build_reply_candidate(selected_key)
        model.fit(model_texts, labels)

        preds = model.predict(model_texts)
        train_f1 = f1_score(labels, preds, average="macro", zero_division=0)
        mlflow.log_metric("train_f1_macro", float(train_f1))
        report = classification_report(labels, preds, zero_division=0)
        print(report)
        mlflow.log_text(report, "classification_report.txt")

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn_model",
            registered_model_name=registered_name,
        )

        publish, reason = quality_gate(task, cv_f1)
        mlflow.log_param("publish_to_worker", publish)
        mlflow.log_param("publish_reason", reason)
        logger.info("Quality gate [%s]: publish=%s – %s", task, publish, reason)

        if publish:
            publish_joblib(
                task, model, output_name, cv_f1, run_id, selected_key
            )
            mlflow.log_artifact(str(MODEL_DIR / output_name), artifact_path="joblib")
            mlflow.set_tag("stage", "published")
        else:
            logger.warning(
                "NOT publishing %s (candidat %s) – %s", task, selected_key, reason
            )
            mlflow.set_tag("stage", "rejected_by_gate")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("MODEL_DIR=%s  embedding=%s", MODEL_DIR, EMBEDDING_MODEL_NAME)
    logger.info(
        "MLflow URI=%s  experiment=%s", MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT
    )
    logger.info(
        "Gate: MIN_F1_TO_PUBLISH=%.3f  MAX_F1_REGRESSION=%.3f",
        MIN_F1_TO_PUBLISH,
        MAX_F1_REGRESSION,
    )
    logger.info(
        "Mode: %s",
        "interactif (TTY)" if is_interactive() else "non-interactif (env / CI)",
    )

    # 1) Choix de la tâche AVANT tout entraînement
    tasks = prompt_tasks()
    logger.info("Tâches sélectionnées: %s", tasks)

    if "APPLICATION" in tasks:
        try:
            train_application(OUTPUT_NAMES["APPLICATION"])
        except RuntimeError as exc:
            logger.error("Skipping APPLICATION: %s", exc)

    if "REPLY" in tasks:
        try:
            train_reply(OUTPUT_NAMES["REPLY"])
        except RuntimeError as exc:
            logger.error("Skipping REPLY: %s", exc)


if __name__ == "__main__":
    main()