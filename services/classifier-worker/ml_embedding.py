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
