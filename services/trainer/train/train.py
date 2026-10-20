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
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from ml_embedding import ChunkPoolingEmbedder, SentenceEmbedder, DEFAULT_MODEL_NAME, split_sentences
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


def build_application_model() -> Pipeline:
    # Inchangé : sur APPLICATION (emails ENVOYÉS, courts), le comparatif de
    # stratégies n'a montré aucun gain du chunking (toutes les stratégies
    # ≈ 0.952 CV F1) — ces textes tiennent déjà sous MAX_BODY_CHARS=600 la
    # plupart du temps, donc un seul chunk = comportement quasi identique.
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


def build_reply_model() -> Pipeline:
    # Promu depuis le comparatif stratégies × classifieurs (voir
    # compare_candidates ci-dessous) : sur REPLY, chunk_word_60 +
    # linear_svm_calibrated a mesuré 0.957 CV F1 contre 0.912 pour
    # l'ancien truncate_600 + logreg — un gain cohérent avec logreg ET
    # linear_svm (pas une seule combinaison chanceuse), sur les emails
    # REÇUS qui sont souvent longs (jusqu'à 70% dépassent 600 caractères
    # nettoyés).
    #
    # IMPORTANT : ce modèle doit être entraîné/servi avec le texte COMPLET
    # (prepare_ml_text_full), PAS le texte tronqué (prepare_ml_text) — voir
    # train() ci-dessous et worker/classification.classify_received().
    embed = ChunkPoolingEmbedder(
        model_name=EMBEDDING_MODEL_NAME,
        strategy="sentence",
        # window_size / overlap inutiles pour strategy="sentence"
    )
    clf = CalibratedClassifierCV(
        LinearSVC(C=1.0, class_weight="balanced", max_iter=5000),
        cv=3,
    )
    return Pipeline([("embed", embed), ("clf", clf)])


# Modèle (stratégie + classifieur) effectivement entraîné et publié, par
# tâche. APPLICATION reste sur l'ancien pipeline ; REPLY utilise désormais
# chunk_word_60 + linear_svm_calibrated (voir build_reply_model ci-dessus).
BUILD_MODEL_FNS = {
    "APPLICATION": build_application_model,
    "REPLY": build_reply_model,
}

# Quel texte (tronqué à 600 car. ou complet) chaque tâche doit utiliser
# pour fit/predict/cross_val_score du modèle PUBLIÉ — doit être cohérent
# avec le texte utilisé par le worker en prédiction (RÈGLE D'OR).
MODEL_TEXT_SOURCE = {
    "APPLICATION": "truncated",
    "REPLY": "full",
}


# ---------------------------------------------------------------------------
# Comparaison de classifieurs ET de stratégies de découpage de texte
# (informatif seulement).
#
# Ne remplace PAS build_model() ni la logique de publish/quality_gate : ça
# tourne en plus, sur les mêmes folds de CV, et les scores sont juste loggés
# dans MLflow (cv_f1_candidate_<stratégie>__<classifieur>) + affichés en
# console. Le but est de décider sur des chiffres mesurés sur les vraies
# données plutôt que de deviner.
#
# Deux axes indépendants testés en grille (stratégie × classifieur) :
#
#   STRATEGIES (comment on prépare le texte avant embedding) :
#     - truncate_600    : comportement actuellement PUBLIÉ (build_model()) —
#                          un seul vecteur sur les 600 premiers caractères
#                          nettoyés (prepare_ml_text).
#     - chunk_sentence   : texte COMPLET (non tronqué, prepare_ml_text_full)
#                          découpé phrase par phrase, un vecteur par phrase,
#                          moyenne des vecteurs. Ne coupe jamais une idée.
#     - chunk_window_300 : texte complet découpé en fenêtres de 300
#                          caractères avec chevauchement (robuste si peu de
#                          ponctuation).
#     - chunk_word_60    : texte complet découpé en fenêtres de 60 mots avec
#                          chevauchement (compromis phrase/caractères).
#
#   CLASSIFIERS (ce qu'on fait des vecteurs obtenus) :
#     - logreg_gridsearch_C, linear_svm_calibrated, knn5_cosine (inchangés).
#
# Les embeddings sont calculés UNE SEULE FOIS par stratégie (pas par
# combinaison stratégie×classifieur×fold) : l'embedding ne dépend pas des
# labels, donc le précalculer hors CV est correct (zéro fuite) et bien plus
# rapide que de réencoder à chaque fold/pipeline.
#
# Pour promouvoir un candidat en production : copier sa config
# (stratégie d'embedding + classifieur) dans build_model() ci-dessus une
# fois que ses scores CV sont systématiquement meilleurs sur plusieurs runs
# (pas un seul run — la variance est grande avec ~150-200 exemples).
# ---------------------------------------------------------------------------

def _logreg_clf():
    # Même modèle que build_model(), mais C choisi par grid search interne
    # (3-fold) au lieu d'être fixé en dur à 1.0.
    return GridSearchCV(
        LogisticRegression(max_iter=2000, class_weight="balanced", solver="lbfgs"),
        param_grid={"C": [0.1, 0.3, 1.0, 3.0, 10.0]},
        cv=3,
        scoring="f1_macro",
    )


def _linear_svm_clf():
    # SVM à frontière linéaire : même profil de risque que la régression
    # logistique (peu de surapprentissage), parfois un peu meilleur sur ce
    # type de tâche. Calibré pour conserver un score de confiance exploitable
    # par le worker (MIN_CONFIDENCE / REVIEW_CONFIDENCE_THRESHOLD).
    base = LinearSVC(C=1.0, class_weight="balanced", max_iter=5000)
    return CalibratedClassifierCV(base, cv=3)


def _knn_clf():
    # Classification par proximité dans l'espace des embeddings : aucun
    # paramètre appris, donc aucun risque de surapprentissage même avec très
    # peu d'exemples par classe. Interprétable (on peut remonter aux
    # exemples les plus proches pour expliquer une prédiction).
    return KNeighborsClassifier(n_neighbors=5, weights="distance", metric="cosine")


CLASSIFIERS = {
    "logreg_gridsearch_C": _logreg_clf,
    "linear_svm_calibrated": _linear_svm_clf,
    "knn5_cosine": _knn_clf,
}


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
    raise ValueError(f"Stratégie inconnue: {strategy!r}")


# Stratégies qui ont besoin du texte NON tronqué (prepare_ml_text_full) —
# toutes sauf la troncature publiée actuellement.
STRATEGIES_USE_FULL_TEXT = {"chunk_sentence", "chunk_window_300", "chunk_word_60"}

STRATEGIES = ["truncate_600", "chunk_sentence", "chunk_window_300", "chunk_word_60"]


def compare_candidates(
    texts_truncated: list[str], texts_full: list[str], labels: list[str], cv: StratifiedKFold
) -> dict[str, float]:
    results: dict[str, float] = {}
    for strategy in STRATEGIES:
        texts_for_strategy = texts_full if strategy in STRATEGIES_USE_FULL_TEXT else texts_truncated
        try:
            embedder = _build_strategy_embedder(strategy)
            embeddings = embedder.fit_transform(texts_for_strategy)
        except Exception as exc:
            logger.warning("  stratégie %-18s a échoué à l'embedding: %s", strategy, exc)
            continue

        for clf_name, build_clf in CLASSIFIERS.items():
            key = f"{strategy}__{clf_name}"
            try:
                scores = cross_val_score(
                    build_clf(), embeddings, labels, cv=cv, scoring="f1_macro", error_score="raise"
                )
                results[key] = float(scores.mean())
                logger.info("  %-40s CV F1-macro: %.3f ± %.3f", key, scores.mean(), scores.std())
            except Exception as exc:
                logger.warning("  %-40s a échoué: %s", key, exc)
    return results


def log_chunking_diagnostics(task: str, texts_full: list[str]) -> None:
    """
    Diagnostic sur les DONNÉES (pas sur le modèle) : combien de chunks
    (phrases) les exemples d'ENTRAÎNEMENT actuels produisent-ils en moyenne ?

    Pourquoi c'est important : le pooling par chunks n'apporte un vrai
    bénéfice que si le modèle voit, à l'entraînement, des textes structurés
    comme ceux qu'il verra en production (plusieurs phrases/paragraphes).
    Si les exemples d'entraînement sont des résumés courts à une phrase
    (moyenne proche de 1 chunk) alors que les emails réels à classifier en
    ont 5-10 (constaté sur les exemples réels fournis : médiane ~700-1100
    caractères nettoyés, jusqu'à 9 phrases), le modèle n'a jamais vu, à
    l'entraînement, à quoi ressemble un "vecteur moyenné sur plusieurs
    phrases" — c'est un écart de distribution train/serve, même si le code
    de nettoyage est identique des deux côtés.
    """
    if not texts_full:
        return
    chunk_counts = [len(split_sentences(t)) or 1 for t in texts_full]
    avg_chunks = sum(chunk_counts) / len(chunk_counts)
    pct_single_chunk = 100 * sum(1 for c in chunk_counts if c <= 1) / len(chunk_counts)
    logger.info(
        "%s — diagnostic données: nb moyen de chunks (phrase) sur les exemples "
        "d'ENTRAÎNEMENT actuels = %.1f (%.0f%% n'ont qu'1 seule phrase). "
        "Rappel: un email réel long peut en avoir 8-10. Si cette moyenne est "
        "proche de 1, le jeu d'entraînement est structurellement trop "
        "court/résumé pour bien exercer le pooling multi-chunks — il "
        "faudrait l'enrichir avec des corps d'emails réels COMPLETS (comme "
        "db/add_real_examples.sql), pas des résumés manuels d'une phrase.",
        task,
        avg_chunks,
        pct_single_chunk,
    )
    mlflow.log_metric(f"train_data_avg_sentence_chunks", avg_chunks)
    mlflow.log_metric(f"train_data_pct_single_chunk", pct_single_chunk)


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

    # Rebuild the exact same "Subject: ...\nBody: ..." shape the
    # classifier-worker feeds the model at prediction time (see
    # worker/classification.py), instead of training on the raw stored
    # text. Training and inference must see identical formatting —
    # see text_cleaning.py's "RÈGLE D'OR".
    texts_truncated = [prepare_ml_text(subject, text) for subject, text, _ in rows]
    # Version non tronquée, pour les stratégies de découpage par chunks
    # (compare_candidates) — voir text_cleaning.prepare_ml_text_full.
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
        # Traçabilité : quel texte (tronqué/complet) ce modèle attend en
        # entrée — doit rester cohérent avec MODEL_TEXT_SOURCE[task] et
        # avec ce que le worker lui envoie en prédiction.
        "model_text_source": MODEL_TEXT_SOURCE[task],
    }
    meta_path = MODEL_DIR / META_NAMES[task]
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    logger.info("PUBLISHED joblib %s → %s (cv_f1=%.3f)", task, path, cv_f1)


def train(task: str, output_name: str) -> None:
    texts, texts_full, labels = load_examples(task)
    counts = Counter(labels)
    registered_name = REGISTERED_NAMES[task]

    build_model = BUILD_MODEL_FNS[task]
    # Le modèle PUBLIÉ pour cette tâche doit être fit/predict avec le même
    # texte (tronqué ou complet) que ce que le worker lui enverra en
    # prédiction — voir MODEL_TEXT_SOURCE et
    # worker/classification.classify_sent/classify_received.
    model_texts = texts_full if MODEL_TEXT_SOURCE[task] == "full" else texts

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
                model_texts,
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

            # Diagnostic données (voir log_chunking_diagnostics) : indique
            # si le jeu d'entraînement actuel est structurellement adapté
            # au pooling multi-chunks ou non.
            log_chunking_diagnostics(task, texts_full)

            # Informatif seulement : compare stratégies de texte ×
            # classifieurs sur les mêmes folds, sans toucher au modèle
            # publié. Voir le commentaire au-dessus de STRATEGIES/CLASSIFIERS.
            logger.info(
                "%s — comparaison stratégies × classifieurs (mêmes folds CV):", task
            )
            candidate_scores = compare_candidates(texts, texts_full, labels, cv)
            for name, score in candidate_scores.items():
                mlflow.log_metric(f"cv_f1_candidate_{name}", score)

            published_strategy = (
                "chunk_sentence + linear_svm_calibrated"
                if task == "REPLY"
                else "truncate_600 + logreg C=1.0"
            )
            best_key = max(candidate_scores, key=candidate_scores.get) if candidate_scores else None
            logger.info(
                "%s — résumé: build_model() publié (%s) = %.3f",
                task,
                published_strategy,
                cv_f1,
            )
            for name, score in sorted(candidate_scores.items(), key=lambda kv: -kv[1]):
                marker = "  <-- meilleur candidat" if name == best_key else ""
                logger.info("    %-40s %.3f%s", name, score, marker)
            if best_key and candidate_scores[best_key] > cv_f1 + 0.01:
                logger.info(
                    "%s — NOTE: le candidat '%s' (%.3f) dépasse le modèle publié (%.3f) "
                    "sur ce run. Vérifier sur plusieurs runs avant de promouvoir — "
                    "ne change PAS automatiquement build_model().",
                    task,
                    best_key,
                    candidate_scores[best_key],
                    cv_f1,
                )
        else:
            logger.warning("%s: label with only one example – CV skipped.", task)

        model = build_model()
        model.fit(model_texts, labels)

        preds = model.predict(model_texts)
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