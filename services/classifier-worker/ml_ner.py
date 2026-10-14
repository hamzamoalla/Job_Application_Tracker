"""
Extraction d'entités (nom d'entreprise / intitulé de poste) via NER
zero-shot GLiNER, utilisée en repli dans worker.py lorsque les regex
(COMPANY_PATTERNS / POSITION_PATTERNS) ne trouvent rien.

Pourquoi GLiNER plutôt qu'un NER classique (spaCy) :
spaCy sait repérer des entités génériques (ORG, PERSON, GPE...) mais ne
connaît pas nativement le concept "poste recherché". GLiNER est un
modèle de NER "zero-shot" : on lui donne les labels voulus ("company
name", "job position") au moment de l'inférence, sans avoir à le
réentraîner ni à labelliser des centaines d'exemples pour chaque nouveau
label.

Modèle utilisé par défaut : urchade/gliner_multi-v2.1 (multilingue
FR/EN, ~350 Mo), comparable en poids à sentence-transformers déjà utilisé
par ml_embedding.py. Entièrement local après le premier téléchargement :
aucun appel réseau à l'inférence.

Ce fichier suit le même principe que ml_embedding.py : le modèle est
chargé une seule fois par process (cache au niveau classe) et partagé
entre tous les appels, pour ne pas payer le coût de chargement à chaque
email traité.
"""

import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = os.getenv("GLINER_MODEL_NAME", "urchade/gliner_multi-v2.1")
DEFAULT_THRESHOLD = float(os.getenv("GLINER_THRESHOLD", "0.4"))

# Nombre de caractères de texte envoyés au modèle. GLiNER, comme tout
# modèle à base de transformer, a un coût d'inférence croissant avec la
# longueur du texte ; un email est déjà nettoyé/tronqué en amont par
# text_cleaning.py, mais ce module peut aussi être appelé directement
# sur subject+body bruts, d'où cette sécurité supplémentaire.
MAX_CHARS = 2000

_model = None
_model_name = None


def _get_model(model_name: str = DEFAULT_MODEL_NAME):
    global _model, _model_name
    if _model is None or _model_name != model_name:
        # Import différé : gliner (et torch) sont des dépendances
        # lourdes, on ne veut les charger que si ce module sert
        # vraiment (c.-à-d. qu'au moins une regex a échoué).
        from gliner import GLiNER

        logger.info("Chargement du modèle GLiNER '%s'...", model_name)
        _model = GLiNER.from_pretrained(model_name)
        _model_name = model_name
        logger.info("Modèle GLiNER chargé.")
    return _model


def extract_entities(text: str, labels, threshold: float = DEFAULT_THRESHOLD):
    """
    Retourne la liste des entités détectées pour les labels demandés,
    triée par score décroissant. Chaque entité est un dict
    {"text": ..., "label": ..., "start": ..., "end": ..., "score": ...}.
    Ne lève jamais d'exception : une erreur d'inférence renvoie [].
    """
    if not text or not text.strip():
        return []

    model = _get_model()
    try:
        entities = model.predict_entities(
            text[:MAX_CHARS], labels, threshold=threshold
        )
    except Exception:
        logger.exception("Erreur d'inférence GLiNER")
        return []

    return sorted(entities, key=lambda e: e["score"], reverse=True)


def best_entity(text: str, label: str, threshold: float = DEFAULT_THRESHOLD):
    """Renvoie le texte de la meilleure entité pour UN label, ou None."""
    entities = extract_entities(text, [label], threshold=threshold)
    return entities[0]["text"].strip() if entities else None


def extract_company_gliner(subject: str, body: str, threshold: float = DEFAULT_THRESHOLD):
    text = f"{subject or ''}\n{body or ''}"
    return best_entity(text, "company name", threshold=threshold)


def extract_position_gliner(subject: str, body: str, threshold: float = DEFAULT_THRESHOLD):
    text = f"{subject or ''}\n{body or ''}"
    return best_entity(text, "job position", threshold=threshold)
