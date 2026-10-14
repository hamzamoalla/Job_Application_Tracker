"""
Nettoyage de texte partagé entre le worker (prédiction) et l'API
(insertion dans training_examples).

RÈGLE D'OR : le texte utilisé pour ENTRAÎNER doit avoir subi exactement
le même nettoyage que le texte utilisé pour PRÉDIRE.
"""

import re
import unicodedata

# Longueur max du corps nettoyé pour le ML.
# Au-delà on n'ajoute que du bruit.
MAX_BODY_CHARS = 600

# Pour l'extraction (GLiNER + regex) on garde un peu plus de contexte.
MAX_EXTRACTION_CHARS = 2000


CUT_PATTERNS = [
    r"(?im)^on .{1,180}wrote:\s*$",
    r"(?im)^le .{1,180}a écrit\s*:\s*$",
    r"(?im)^from:\s.*$",
    r"(?im)^de\s*:\s.*$",
    r"(?im)^-{2,}\s*original message\s*-{2,}\s*$",
    r"(?im)^_{5,}\s*$",
]

BOILERPLATE_LINE_PATTERNS = [
    r"(?i)^unsubscribe.*$",
    r"(?i)^se désinscrire.*$",
    r"(?i)^se désabonner.*$",
    r"(?i).*tous droits réservés.*$",
    r"(?i).*all rights reserved.*$",
    r"(?i)^this email was sent to.*$",
    r"(?i)^cet e-mail a été envoyé à.*$",
    r"(?i)^suivez-nous sur.*$",
    r"(?i)^follow us on.*$",
    r"(?i)^privacy policy.*$",
    r"(?i)^politique de confidentialité.*$",
    r"(?i)^you are receiving this email because.*$",
    r"(?i)^vous recevez cet e-mail car.*$",
    r"(?i)^confidentialité\s*[:\-].*$",
    r"(?i)^this message (?:is|contains) confidential.*$",
    r"(?i)^ce message (?:est|contient) confidentiel.*$",
]


def normalize(value: str) -> str:
    """Normalise une chaîne pour les comparaisons (accents, casse, ponctuation)."""
    value = (value or "").lower()
    value = value.replace("\u00a0", " ")  # espace insécable
    value = re.sub(r"[^a-z0-9+#. ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def remove_invisible_chars(text: str) -> str:
    """
    Supprime les zero-width spaces, non-joiners, soft hyphens,
    combining grapheme joiners, et autres caractères de formatage invisibles.
    Très courant dans les preheaders des emails marketing / recrutement.
    """
    if not text:
        return ""

    # Caractères de contrôle + zero-width + format
    invisible = re.compile(
        r"[\u0000-\u0008\u000B\u000C\u000E-\u001F"
        r"\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u206f"
        r"\ufeff\u00ad\u034f\u061c\u180e\u2000-\u200a]"
    )
    text = invisible.sub("", text)

    # Compacte les espaces laissés par la suppression
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_reply(body: str) -> str:
    """
    Retire les anciennes réponses citées, sans couper le corps
    si le pattern apparaît trop tôt.
    """
    if not body:
        return ""

    cleaned = body
    for pattern in CUT_PATTERNS:
        match = re.search(pattern, cleaned)
        if match and match.start() > 80:
            cleaned = cleaned[: match.start()]

    cleaned = "\n".join(
        line for line in cleaned.splitlines()
        if not line.lstrip().startswith(">")
    )
    return cleaned.strip()


def strip_boilerplate(text: str) -> str:
    """Retire les lignes de pied de page / mentions légales récurrentes."""
    if not text:
        return ""

    lines = []
    for line in text.splitlines():
        if any(re.match(pattern, line.strip()) for pattern in BOILERPLATE_LINE_PATTERNS):
            continue
        lines.append(line)

    result = "\n".join(lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def truncate(text: str, max_chars: int = MAX_BODY_CHARS) -> str:
    if not text or len(text) <= max_chars:
        return text or ""
    return text[:max_chars].rstrip() + " […]"


def prepare_ml_text(subject: str | None, body: str | None) -> str:
    """
    Pipeline de nettoyage unique pour le ML (entraînement + prédiction).
    Étapes : invisible chars → citations → boilerplate → truncate.
    """
    body = remove_invisible_chars(body or "")
    cleaned_body = clean_reply(body)
    cleaned_body = strip_boilerplate(cleaned_body)
    cleaned_body = truncate(cleaned_body, MAX_BODY_CHARS)

    subject = (subject or "").strip()
    return f"Subject: {subject}\nBody: {cleaned_body}".strip()


def clean_for_storage(subject: str | None, body: str | None) -> tuple[str, str]:
    """
    Nettoyage à appliquer dès l'insertion en base.
    Plus agressif que le ML (on veut un body propre en BDD).
    """
    subject = (subject or "").strip()
    body = remove_invisible_chars(body or "")
    body = clean_reply(body)
    body = strip_boilerplate(body)
    # On garde un peu plus de texte en base que pour le ML
    body = truncate(body, max_chars=3000)
    return subject, body


def clean_for_extraction(subject: str | None, body: str | None) -> tuple[str, str]:
    """
    Nettoyage avant extraction entreprise / poste (GLiNER + regex).
    On garde plus de contexte que pour le ML.
    """
    subject = (subject or "").strip()
    body = remove_invisible_chars(body or "")
    body = clean_reply(body)
    body = strip_boilerplate(body)
    body = truncate(body, max_chars=MAX_EXTRACTION_CHARS)
    return subject, body