"""
Transformer scikit-learn partagé par train.py (entraînement) et worker.py
(désérialisation du modèle via joblib).

Pourquoi ce fichier doit exister des DEUX côtés :
joblib/pickle ne sauvegarde pas le code d'une classe personnalisée, juste
une référence ("ml_embedding.SentenceEmbedder") + son état. Pour recharger
le modèle, le worker doit pouvoir importer ce même module — donc ce
fichier doit être copié dans l'image Docker du trainer ET du
classifier-worker, exactement comme text_cleaning.py.

Principe : remplacer TF-IDF (comptage de mots exacts) par des embeddings
de phrases pré-entraînés (modèle "paraphrase-multilingual-MiniLM-L12-v2").
Deux emails qui disent la même chose avec des mots différents se
retrouvent proches dans l'espace vectoriel, parce que le modèle a appris
le sens sur des milliards de phrases avant même de voir vos emails. Avec
seulement ~30 exemples par label, c'est ce qui généralise le mieux.
"""

import re

from sklearn.base import BaseEstimator, TransformerMixin

DEFAULT_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class SentenceEmbedder(BaseEstimator, TransformerMixin):
    """
    Encode une liste de textes en vecteurs sémantiques (384 dimensions
    pour ce modèle). Compatible Pipeline scikit-learn : peut remplacer
    TfidfVectorizer directement, joblib.dump/load fonctionnent pareil.

    Le modèle sentence-transformers (~470 Mo) est chargé une seule fois
    par processus et partagé entre toutes les instances, pour ne pas le
    recharger à chaque fit/transform/prédiction.
    """

    _model = None
    _model_name = None

    def __init__(self, model_name=DEFAULT_MODEL_NAME, batch_size=32):
        self.model_name = model_name
        self.batch_size = batch_size

    def _get_model(self):
        if SentenceEmbedder._model is None or SentenceEmbedder._model_name != self.model_name:
            # Import différé : sentence-transformers (et torch) sont des
            # dépendances lourdes, on ne veut les charger que si ce
            # transformer est réellement utilisé.
            from sentence_transformers import SentenceTransformer

            SentenceEmbedder._model = SentenceTransformer(self.model_name)
            SentenceEmbedder._model_name = self.model_name
        return SentenceEmbedder._model

    def fit(self, X, y=None):
        # Rien à apprendre ici : le modèle d'embedding est déjà
        # pré-entraîné. On garde fit() pour rester compatible Pipeline.
        return self

    def transform(self, X):
        model = self._get_model()
        texts = list(X)
        return model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
        )

    def fit_transform(self, X, y=None, **kwargs):
        return self.transform(X)


# ---------------------------------------------------------------------------
# ChunkPoolingEmbedder : alternative à SentenceEmbedder pour les emails trop
# longs pour tenir dans MAX_BODY_CHARS (600 car.) sans perdre le signal clé
# (voir discussion : ~70% des emails réels dépassent 600 car. nettoyés, et
# le signal décisif (REJECTION/IN_REVIEW/INTERVIEW) peut tomber n'importe où,
# y compris au milieu — la troncature "tête" simple, ou même "tête+queue",
# peut le perdre).
#
# Principe : au lieu d'un seul vecteur pour (jusqu'à) 600 caractères, on
# découpe le texte COMPLET (non tronqué) en plusieurs chunks qui se
# chevauchent légèrement, on embedde chaque chunk séparément, puis on fait
# la MOYENNE des vecteurs obtenus. Chaque partie du texte, y compris le
# milieu d'un email long, contribue au vecteur final — aucune zone n'est
# structurellement ignorée.
#
# Trois stratégies de découpage :
#   - "sentence" : une phrase (ou groupe ponctué par . ! ?) = un chunk.
#     Ne coupe jamais une idée en deux ; s'aligne avec la façon dont le
#     modèle de sentence-embedding a été pré-entraîné (sur des phrases
#     complètes, pas des fenêtres de caractères arbitraires).
#   - "window"   : fenêtres glissantes de N caractères avec chevauchement,
#     indépendant de la ponctuation (robuste si le texte a peu/mal de
#     ponctuation).
#   - "word"     : fenêtres glissantes de N mots avec chevauchement —
#     compromis entre les deux précédents.
# ---------------------------------------------------------------------------

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str, min_words: int = 4) -> list[str]:
    """Découpe sur . ! ? et ignore les fragments trop courts (ex. 'Merci.',
    'Cordialement,') qui n'apportent pas de signal utile seuls."""
    if not text or not text.strip():
        return []
    raw = _SENTENCE_SPLIT_RE.split(text.strip())
    sentences = [s.strip() for s in raw if s.strip()]
    kept = [s for s in sentences if len(s.split()) >= min_words]
    # Si tout a été filtré (texte très court), on garde au moins les
    # fragments bruts plutôt que de perdre le texte entièrement.
    return kept or sentences


def split_window_chars(text: str, window_chars: int = 300, overlap_chars: int = 100) -> list[str]:
    """Fenêtres glissantes de caractères, avec chevauchement pour limiter
    le risque de couper une phrase clé pile à la frontière entre 2 chunks."""
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= window_chars:
        return [text]
    step = max(1, window_chars - overlap_chars)
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start : start + window_chars].strip()
        if chunk:
            chunks.append(chunk)
        if start + window_chars >= len(text):
            break
        start += step
    return chunks


def split_window_words(text: str, window_words: int = 60, overlap_words: int = 20) -> list[str]:
    """Fenêtres glissantes de mots, avec chevauchement."""
    words = (text or "").split()
    if not words:
        return []
    if len(words) <= window_words:
        return [" ".join(words)]
    step = max(1, window_words - overlap_words)
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start : start + window_words]).strip()
        if chunk:
            chunks.append(chunk)
        if start + window_words >= len(words):
            break
        start += step
    return chunks


SPLITTERS = {
    "sentence": split_sentences,
    "window": split_window_chars,
    "word": split_window_words,
}


class ChunkPoolingEmbedder(BaseEstimator, TransformerMixin):
    """
    Comme SentenceEmbedder, mais découpe chaque texte en plusieurs chunks
    (voir SPLITTERS) avant embedding, puis fait la moyenne des vecteurs de
    chunks pour obtenir un seul vecteur par texte (même dimension que
    SentenceEmbedder, donc interchangeable dans un Pipeline).

    IMPORTANT : à utiliser avec le texte COMPLET (non tronqué à
    MAX_BODY_CHARS) — voir text_cleaning.prepare_ml_text_full — sinon ça
    revient juste à faire du pooling sur un texte déjà amputé.
    """

    _model = None
    _model_name = None

    def __init__(
        self,
        model_name=DEFAULT_MODEL_NAME,
        strategy="sentence",
        batch_size=32,
        window_size=None,
        overlap=None,
        min_words=4,
    ):
        self.model_name = model_name
        self.strategy = strategy
        self.batch_size = batch_size
        self.window_size = window_size
        self.overlap = overlap
        self.min_words = min_words

    def _get_model(self):
        if ChunkPoolingEmbedder._model is None or ChunkPoolingEmbedder._model_name != self.model_name:
            from sentence_transformers import SentenceTransformer

            ChunkPoolingEmbedder._model = SentenceTransformer(self.model_name)
            ChunkPoolingEmbedder._model_name = self.model_name
        return ChunkPoolingEmbedder._model

    def _split(self, text: str) -> list[str]:
        if self.strategy == "sentence":
            chunks = split_sentences(text, min_words=self.min_words)
        elif self.strategy == "window":
            chunks = split_window_chars(
                text,
                window_chars=self.window_size or 300,
                overlap_chars=self.overlap or 100,
            )
        elif self.strategy == "word":
            chunks = split_window_words(
                text,
                window_words=self.window_size or 60,
                overlap_words=self.overlap or 20,
            )
        else:
            raise ValueError(f"Stratégie de découpage inconnue: {self.strategy!r}")
        return chunks or [text.strip() if text else ""]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        import numpy as np

        texts = list(X)
        per_text_chunks = [self._split(t) for t in texts]

        # On embedde TOUS les chunks de TOUS les textes en un seul appel
        # batché (plus efficace que d'appeler model.encode() texte par
        # texte), puis on regroupe par texte d'origine pour la moyenne.
        flat_chunks: list[str] = []
        boundaries: list[tuple[int, int]] = []  # (start, end) index dans flat_chunks par texte
        for chunks in per_text_chunks:
            start = len(flat_chunks)
            flat_chunks.extend(chunks)
            boundaries.append((start, len(flat_chunks)))

        model = self._get_model()
        flat_vectors = model.encode(
            flat_chunks,
            batch_size=self.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
        )

        pooled = np.empty((len(texts), flat_vectors.shape[1]), dtype=flat_vectors.dtype)
        for i, (start, end) in enumerate(boundaries):
            pooled[i] = flat_vectors[start:end].mean(axis=0)
        return pooled

    def fit_transform(self, X, y=None, **kwargs):
        return self.transform(X)