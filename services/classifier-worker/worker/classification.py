"""ML + heuristic classification helpers."""

from __future__ import annotations

import logging
from typing import Any

from text_cleaning import prepare_ml_text, prepare_ml_text_full
from worker.heuristics import heuristic_classification

# Optionnel : réutiliser le même découpage que le modèle publié (chunk_sentence)
from ml_embedding import split_sentences

logger = logging.getLogger(__name__)

# Seuil en dessous duquel on logge les chunks pour le debug / review
LOW_CONFIDENCE_CHUNK_LOG = 0.70

application_model: Any = None
reply_model: Any = None


def model_predict(
    model: Any, text: str, model_name: str = "unknown"
) -> tuple[str, float]:
    if model is None:
        logger.warning("Modèle '%s' non chargé → fallback OTHER", model_name)
        return "OTHER", 0.0
    try:
        probabilities = model.predict_proba([text])[0]
        index = probabilities.argmax()
        label = str(model.classes_[index])
        confidence = float(probabilities[index])
        logger.info("ML [%s] → label=%s  confidence=%.3f", model_name, label, confidence)
        return label, confidence
    except Exception:
        logger.exception("Erreur prédiction ML (%s)", model_name)
        return "OTHER", 0.0


def _log_chunks_if_low_confidence(
    text: str, label: str, confidence: float, subject: str = ""
) -> None:
    """
    Si confidence < 0.7, affiche tous les chunks (même découpage que
    ChunkPoolingEmbedder strategy='sentence') pour comprendre pourquoi
    le modèle hésite.
    """
    if confidence >= LOW_CONFIDENCE_CHUNK_LOG:
        return

    chunks = split_sentences(text) or [text.strip() or "(vide)"]
    logger.info(
        "LOW_CONF (%.3f) label=%s subject=%r — %d chunk(s):",
        confidence,
        label,
        (subject or "")[:80],
        len(chunks),
    )
    for i, chunk in enumerate(chunks, start=1):
        # Tronquer un peu en log pour ne pas noyer les logs
        preview = chunk if len(chunk) <= 300 else chunk[:300] + " […]"
        logger.info("  chunk[%d/%d] (%d car.): %s", i, len(chunks), len(chunk), preview)


def classify_sent(email: dict) -> tuple[str, float]:
    text = prepare_ml_text(email.get("subject"), email.get("body"))
    label, confidence = model_predict(application_model, text, model_name="application_model")
    # APPLICATION = SentenceEmbedder (1 seul "chunk" = texte tronqué)
    if confidence < LOW_CONFIDENCE_CHUNK_LOG:
        logger.info(
            "LOW_CONF APPLICATION (%.3f) label=%s subject=%r — texte (truncate): %s",
            confidence,
            label,
            (email.get("subject") or "")[:80],
            text[:400] + (" […]" if len(text) > 400 else ""),
        )
    return label, confidence


def classify_received(email: dict) -> tuple[str, float]:
    subject = email.get("subject") or ""
    body = email.get("body") or ""

    rule_result = heuristic_classification(subject, body)

    # REPLY = chunk_sentence + linear_svm_calibrated → texte COMPLET
    text = prepare_ml_text_full(subject, body)
    label, confidence = model_predict(reply_model, text, model_name="reply_model")

    allowed = {"INTERVIEW", "IN_REVIEW", "REJECTION", "OTHER"}
    if label not in allowed:
        label, confidence = "OTHER", confidence

    # Debug : afficher tous les chunks si confiance basse
    _log_chunks_if_low_confidence(text, label, confidence, subject=subject)

    if rule_result is None:
        return label, confidence

    rule_label, rule_confidence = rule_result
    if rule_confidence >= 0.90:
        logger.info("Heuristique prioritaire → %s (%.2f)", rule_label, rule_confidence)
        return rule_label, rule_confidence
    if label == rule_label:
        return label, min(0.95, max(confidence, rule_confidence) + 0.10)
    if confidence < rule_confidence:
        return rule_label, rule_confidence
    return label, confidence