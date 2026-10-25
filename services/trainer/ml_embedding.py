import re

from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin

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


# ---------------------------------------------------------------------------
# Filtre de chunks "mentions légales / politesse générique" (FR/EN/DE).
#
# Pourquoi au niveau CHUNK et pas dans text_cleaning.strip_boilerplate() :
# strip_boilerplate() retire des LIGNES ENTIÈRES qui COMMENCENT par un motif
# connu — ça marche quand chaque mention légale est sur sa propre ligne,
# mais beaucoup d'emails (ex. FIS, PASS Consulting) mettent tout le pied de
# page dans UN SEUL paragraphe sans retour à la ligne ("Kind Regards, FIS
# Talent Acquisition FIS is committed to protecting..."), donc aucune ligne
# ne commence par le motif et rien n'est retiré.
#
# Une fois le texte découpé en chunks (phrase/fenêtre), chaque mention
# légale redevient une unité isolée qu'on peut reconnaître n'importe où
# dans le chunk (pas seulement en début de ligne) et retirer AVANT
# l'embedding — sinon elle pèse dans la moyenne au même titre qu'un chunk
# qui porte le vrai signal de décision, ce qui dilue le vecteur final vers
# un pôle "neutre" et fait chuter la confiance (voir le cas réel FIS :
# 13 chunks dont 2 seulement portent le signal, confidence tombée à 0.585).
LEGAL_BOILERPLATE_CHUNK_PATTERNS = [
    # Confidentialité / destinataire (EN)
    r"\bnot the intended recipient\b",
    r"\bproprietary and/or confidential\b",
    r"\bthis (?:e-?mail|message) (?:is|contains|may contain) confidential\b",
    r"\bif you (?:have )?received this (?:e-?mail|message) in error\b",
    r"\bsubject to archiving and review\b",
    r"\bdelete the message and all copies\b",
    r"\bdo not disclose, distribute or use\b",
    r"\bnotify the sender immediately\b",
    r"\bany message addressed to our domain\b",
    r"\ball rights reserved\b",
    r"\bunsubscribe\b",
    # Confidentialité (FR)
    r"\bce message (?:électronique )?(?:est|contient) confidentiel\b",
    r"\bsi vous n''?êtes pas le destinataire\b",
    r"\bveuillez (?:le )?détruire\b.*\bmessage\b",
    r"\btous droits réservés\b",
    r"\bse désabonner\b",
    r"\bse désinscrire\b",
    # Vertraulichkeit (DE) — vu en production (PASS Consulting)
    r"\bvertrauliche\b.*\binformationen\b",
    r"\bausschließlich für den bezeichneten adressaten\b",
    r"\bnicht der richtige adressat\b",
    r"\bverwendung des inhalts fehlgeleiteter\b",
]
# IGNORECASE au niveau du compile (pas d'(?i) par motif) : combiner
# plusieurs motifs avec (?i) individuels via "|" lève "global flags not at
# the start of the expression" sur Python 3.11+.
_LEGAL_BOILERPLATE_RE = re.compile("|".join(LEGAL_BOILERPLATE_CHUNK_PATTERNS), re.IGNORECASE)


def drop_legal_boilerplate_chunks(chunks: list[str]) -> list[str]:
    """Retire les chunks qui ne sont que mention légale / politesse
    générique. Ne vide jamais complètement la liste : si TOUS les chunks
    matchent (texte entièrement légal, rare), on les garde plutôt que de
    se retrouver avec un embedding vide."""
    filtered = [c for c in chunks if not _LEGAL_BOILERPLATE_RE.search(c)]
    return filtered or chunks


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
        pooling="mean",
        topk=3,
        em_components=2,
    ):
        self.model_name = model_name
        self.strategy = strategy
        self.batch_size = batch_size
        self.window_size = window_size
        self.overlap = overlap
        self.min_words = min_words
        # "mean"      : moyenne de tous les chunks (comportement d'origine).
        # "max"       : max élément par élément sur tous les chunks — garde
        #               la valeur la plus forte par dimension, quel que
        #               soit le chunk d'où elle vient.
        # "mean_topk" : calcule le centre de gravité (moyenne) de tous les
        #               chunks d'un texte, ne garde que les `topk` chunks
        #               les plus ÉLOIGNÉS de ce centre (= les moins
        #               "génériques"/les plus atypiques), puis fait leur
        #               moyenne. Intuition : dans un email, la politesse et
        #               les mentions légales se ressemblent toutes et
        #               tirent vers le centre ; la phrase de décision est
        #               justement celle qui détonne — ce pooling l'isole
        #               sans dépendre de mots-clés écrits à la main et sans
        #               aucun paramètre appris (pas de risque de
        #               surapprentissage, contrairement à une attention
        #               apprise — voir la discussion sur la taille de
        #               données nécessaire pour cette dernière).
        # "em_local"  : même intuition que mean_topk, mais via un mélange de
        #               gaussiennes (EM, sklearn.mixture.GaussianMixture)
        #               refitté SUR LES SEULS CHUNKS DE CE TEXTE à chaque
        #               appel. Version "molle" (pondération continue par
        #               probabilité postérieure) plutôt que "dure" (garder
        #               exactement topk chunks). Aucun état entraîné stocké,
        #               comme mean_topk — mais peu de chunks par email (2-4
        #               chunks parfois) donne peu de matière à l'EM pour
        #               converger proprement.
        # "em_global" : même mélange de gaussiennes, mais appris UNE SEULE
        #               FOIS (vrai fit()) sur TOUS les chunks de TOUS les
        #               textes d'entraînement — bien plus de données pour
        #               l'EM (centaines de chunks même avec ~150-200
        #               emails) que l'attention apprise (qui, elle, a besoin
        #               de labels et n'a que ~20-55 exemples/classe). La
        #               composante dont le poids a priori (gmm.weights_) est
        #               le plus grand est supposée "générique" (le ton
        #               générique/la politesse revient plus souvent, d'un
        #               email à l'autre, que la phrase de décision précise),
        #               et chaque chunk est pondéré par sa probabilité
        #               postérieure de NE PAS appartenir à cette composante.
        self.pooling = pooling
        self.topk = topk
        self.em_components = em_components

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
        chunks = drop_legal_boilerplate_chunks(chunks) if chunks else chunks
        return chunks or [text.strip() if text else ""]

    def fit(self, X, y=None):
        if self.pooling == "em_global":
            import numpy as np
            from sklearn.mixture import GaussianMixture

            texts = list(X)
            per_text_chunks = [self._split(t) for t in texts]
            flat_chunks = [c for chunks in per_text_chunks for c in chunks]

            if len(flat_chunks) < self.em_components:
                # Pas assez de chunks dans ce fold/jeu pour fitter l'EM —
                # fallback silencieux vers une moyenne simple au transform
                # (voir _pool_em_global). Peut arriver sur un petit fold de
                # cross-validation avec peu d'exemples.
                self.em_global_gmm_ = None
                self.em_global_generic_idx_ = None
                return self

            model = self._get_model()
            flat_vectors = model.encode(
                flat_chunks, batch_size=self.batch_size, show_progress_bar=False, convert_to_numpy=True
            )
            gmm = GaussianMixture(
                n_components=self.em_components,
                covariance_type="diag",
                reg_covar=1e-3,
                random_state=42,
                n_init=3,
            )
            gmm.fit(flat_vectors)
            self.em_global_gmm_ = gmm
            # Composante "générique" = celle que l'EM trouve la plus
            # fréquente (poids a priori le plus grand) — la politesse et le
            # ton générique se répètent plus, d'un email à l'autre, qu'une
            # phrase de décision précise.
            self.em_global_generic_idx_ = int(np.argmax(gmm.weights_))
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
            pooled[i] = self._pool(flat_vectors[start:end])
        return pooled

    def _pool(self, chunk_vectors) -> "np.ndarray":
        import numpy as np

        if chunk_vectors.shape[0] == 1:
            # Un seul chunk : toutes les stratégies de pooling sont
            # équivalentes, pas la peine de calculer des distances.
            return chunk_vectors[0]

        if self.pooling == "mean":
            return chunk_vectors.mean(axis=0)

        if self.pooling == "max":
            return chunk_vectors.max(axis=0)

        if self.pooling == "mean_topk":
            centroid = chunk_vectors.mean(axis=0)
            # Distance cosinus au centroïde (1 - similarité cosinus) : plus
            # c'est grand, plus le chunk s'écarte du "ton général" de
            # l'email.
            norms = np.linalg.norm(chunk_vectors, axis=1) * np.linalg.norm(centroid) + 1e-9
            cos_sim = (chunk_vectors @ centroid) / norms
            distances = 1.0 - cos_sim
            k = max(1, min(self.topk, chunk_vectors.shape[0]))
            top_idx = np.argsort(-distances)[:k]
            return chunk_vectors[top_idx].mean(axis=0)

        if self.pooling == "em_local":
            return self._pool_em_local(chunk_vectors)

        if self.pooling == "em_global":
            return self._pool_em_global(chunk_vectors)

        raise ValueError(f"Stratégie de pooling inconnue: {self.pooling!r}")

    def _pool_em_local(self, chunk_vectors) -> "np.ndarray":
        """EM (mélange de gaussiennes) refitté sur les SEULS chunks de ce
        texte — pas d'état entraîné stocké, comme mean_topk, mais version
        "molle" (pondération par probabilité postérieure) au lieu de "dure"
        (garder exactement topk chunks)."""
        import numpy as np
        from sklearn.mixture import GaussianMixture

        n = chunk_vectors.shape[0]
        k = min(self.em_components, n)
        if k < 2:
            return chunk_vectors.mean(axis=0)
        try:
            gmm = GaussianMixture(
                n_components=k, covariance_type="diag", reg_covar=1e-3, random_state=42, n_init=1
            )
            gmm.fit(chunk_vectors)
            posteriors = gmm.predict_proba(chunk_vectors)
            generic_idx = int(np.argmax(gmm.weights_))
            specific_weight = 1.0 - posteriors[:, generic_idx]
            total = specific_weight.sum()
            if total < 1e-6:
                # Tous les chunks assignés à la composante "générique" —
                # repli sur la moyenne simple plutôt qu'une division par un
                # total quasi nul.
                return chunk_vectors.mean(axis=0)
            specific_weight = specific_weight / total
            return (chunk_vectors * specific_weight[:, None]).sum(axis=0)
        except Exception:
            # EM peut échouer à converger sur très peu de points (2-3
            # chunks) — repli silencieux sur la moyenne plutôt que planter
            # tout l'entraînement pour un seul email.
            return chunk_vectors.mean(axis=0)

    def _pool_em_global(self, chunk_vectors) -> "np.ndarray":
        """EM appris une seule fois en fit() sur tout le jeu d'entraînement
        (voir ChunkPoolingEmbedder.fit) — pondère chaque chunk par sa
        probabilité postérieure de ne PAS appartenir à la composante
        "générique" apprise globalement."""
        gmm = getattr(self, "em_global_gmm_", None)
        if gmm is None:
            # fit() pas appelé, ou pas assez de chunks pour fitter l'EM —
            # repli sur la moyenne simple.
            return chunk_vectors.mean(axis=0)
        posteriors = gmm.predict_proba(chunk_vectors)
        generic_idx = self.em_global_generic_idx_
        specific_weight = 1.0 - posteriors[:, generic_idx]
        total = specific_weight.sum()
        if total < 1e-6:
            return chunk_vectors.mean(axis=0)
        specific_weight = specific_weight / total
        return (chunk_vectors * specific_weight[:, None]).sum(axis=0)

    def fit_transform(self, X, y=None, **kwargs):
        # IMPORTANT : appelle bien fit() avant transform() (plus un simple
        # raccourci vers transform()) — indispensable pour "em_global" dont
        # le fit() fait le vrai travail (apprendre le GMM global). Pour les
        # autres poolings, fit() est un no-op, donc ça ne change rien.
        return self.fit(X, y).transform(X)


def _split_text_to_chunks(
    text: str,
    strategy: str = "sentence",
    window_size: int | None = None,
    overlap: int | None = None,
    min_words: int = 4,
) -> list[str]:
    """Même logique de découpage que ChunkPoolingEmbedder._split, mais en
    fonction autonome (pas de dépendance à une instance) — utilisée par
    ChunkAttentionClassifier ci-dessous, qui a besoin des chunks BRUTS
    (pas encore moyennés) puisque l'attention est apprise, pas calculée
    après coup."""
    if strategy == "sentence":
        chunks = split_sentences(text, min_words=min_words)
    elif strategy == "window":
        chunks = split_window_chars(text, window_chars=window_size or 300, overlap_chars=overlap or 100)
    elif strategy == "word":
        chunks = split_window_words(text, window_words=window_size or 60, overlap_words=overlap or 20)
    else:
        raise ValueError(f"Stratégie de découpage inconnue: {strategy!r}")
    chunks = drop_legal_boilerplate_chunks(chunks) if chunks else chunks
    return chunks or [text.strip() if text else ""]


# ---------------------------------------------------------------------------
# ChunkAttentionClassifier : pooling par ATTENTION APPRISE, demandé
# explicitement malgré la mise en garde suivante (taille de données) —
# implémenté en pur NumPy (pas de dépendance à torch, qui n'est pas
# installé dans cet environnement de dev ; sentence-transformers l'amène
# en revanche en dépendance transitive dans l'image Docker réelle du
# trainer, donc ce choix n'est pas motivé par une indisponibilité en
# production — juste plus simple à tester ici et sans dépendance
# supplémentaire à gérer).
#
# ATTENTION (mise en garde déjà discutée, toujours valable) : contrairement
# à "mean"/"max"/"mean_topk" qui n'ont AUCUN paramètre appris, ce pooling
# introduit un vecteur d'attention + une couche de classification appris
# CONJOINTEMENT sur le jeu d'entraînement. Avec ~20-55 exemples par label
# (classes REPLY actuelles), le risque de surapprentissage est réel — c'est
# pour ça que ce candidat est évalué dans compare_candidates() à côté des
# autres (jamais promu automatiquement dans build_reply_model()) et que la
# régularisation L2 est volontairement forte par défaut (reg_lambda=0.05).
# Comparer son score CV à mean_topk sur PLUSIEURS runs avant d'envisager de
# le publier.
#
# Ne peut pas se brancher dans un Pipeline (embed, clf) classique comme les
# autres stratégies : l'attention doit être entraînée EN MÊME TEMPS que le
# classifieur (elle n'a de sens qu'optimisée pour la tâche), donc c'est un
# estimateur unique, auto-suffisant, qui fait tout de fit(X, y) à predict(X).
# ---------------------------------------------------------------------------


class ChunkAttentionClassifier(BaseEstimator, ClassifierMixin):
    """
    Pour chaque texte : découpe en chunks (comme ChunkPoolingEmbedder),
    embedding de chaque chunk, puis au lieu d'une moyenne/max fixe :
      scores_j = chunk_j · w_att          (un score par chunk)
      attn     = softmax(scores)          (poids d'attention, somme=1)
      doc_vec  = somme_j attn_j * chunk_j (vecteur du document, pondéré)
      logits   = doc_vec @ W_clf + b_clf
      probs    = softmax(logits)

    w_att, W_clf, b_clf sont appris par descente de gradient (Adam, pur
    NumPy, rétropropagation calculée à la main) en minimisant la
    cross-entropie + régularisation L2, sur tout le jeu d'entraînement à
    chaque epoch (full-batch — le jeu est petit, pas besoin de mini-batchs).
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
        reg_lambda=0.05,
        lr=0.05,
        epochs=150,
        random_state=42,
    ):
        self.model_name = model_name
        self.strategy = strategy
        self.batch_size = batch_size
        self.window_size = window_size
        self.overlap = overlap
        self.min_words = min_words
        self.reg_lambda = reg_lambda
        self.lr = lr
        self.epochs = epochs
        self.random_state = random_state

    def _get_model(self):
        if ChunkAttentionClassifier._model is None or ChunkAttentionClassifier._model_name != self.model_name:
            from sentence_transformers import SentenceTransformer

            ChunkAttentionClassifier._model = SentenceTransformer(self.model_name)
            ChunkAttentionClassifier._model_name = self.model_name
        return ChunkAttentionClassifier._model

    def _split(self, text: str) -> list[str]:
        return _split_text_to_chunks(
            text,
            strategy=self.strategy,
            window_size=self.window_size,
            overlap=self.overlap,
            min_words=self.min_words,
        )

    def _embed_raw(self, X) -> list:
        """Retourne, pour chaque texte, la matrice BRUTE (n_chunks, dim) de
        ses chunks — pas encore combinée en un seul vecteur, contrairement à
        ChunkPoolingEmbedder.transform()."""
        texts = list(X)
        per_text_chunks = [self._split(t) for t in texts]

        flat_chunks: list[str] = []
        boundaries: list[tuple[int, int]] = []
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
        return [flat_vectors[start:end] for start, end in boundaries]

    @staticmethod
    def _softmax(z):
        import numpy as np

        z = z - np.max(z)
        e = np.exp(z)
        return e / (e.sum() + 1e-12)

    def fit(self, X, y):
        import numpy as np

        chunk_mats = self._embed_raw(X)
        y = list(y)
        self.classes_ = np.array(sorted(set(y)))
        class_to_idx = {c: i for i, c in enumerate(self.classes_)}
        y_idx = [class_to_idx[label] for label in y]
        n_classes = len(self.classes_)
        dim = chunk_mats[0].shape[1]

        rng = np.random.RandomState(self.random_state)
        w_att = rng.normal(scale=0.01, size=dim)
        W_clf = rng.normal(scale=0.01, size=(dim, n_classes))
        b_clf = np.zeros(n_classes)

        # Adam (implémenté à la main — pas de torch dans cet environnement).
        m_w, v_w = np.zeros_like(w_att), np.zeros_like(w_att)
        m_W, v_W = np.zeros_like(W_clf), np.zeros_like(W_clf)
        m_b, v_b = np.zeros_like(b_clf), np.zeros_like(b_clf)
        beta1, beta2, eps = 0.9, 0.999, 1e-8
        t = 0
        n = len(chunk_mats)

        for _epoch in range(self.epochs):
            grad_w_att = np.zeros_like(w_att)
            grad_W_clf = np.zeros_like(W_clf)
            grad_b_clf = np.zeros_like(b_clf)

            for C, label_idx in zip(chunk_mats, y_idx):
                scores = C @ w_att
                attn = self._softmax(scores)
                doc_vec = attn @ C
                logits = doc_vec @ W_clf + b_clf
                probs = self._softmax(logits)

                d_logits = probs.copy()
                d_logits[label_idx] -= 1.0

                grad_W_clf += np.outer(doc_vec, d_logits)
                grad_b_clf += d_logits

                d_doc_vec = W_clf @ d_logits
                d_attn = C @ d_doc_vec
                # Rétropropagation à travers le softmax de l'attention :
                # dL/dscores_j = attn_j * (d_attn_j - somme_k attn_k * d_attn_k)
                d_scores = attn * (d_attn - np.sum(attn * d_attn))
                grad_w_att += C.T @ d_scores

            # Régularisation L2 (forte par défaut, voir mise en garde
            # ci-dessus sur la taille du jeu de données).
            grad_w_att = grad_w_att / n + self.reg_lambda * w_att
            grad_W_clf = grad_W_clf / n + self.reg_lambda * W_clf
            grad_b_clf = grad_b_clf / n

            t += 1
            for grad, param, m, v in (
                (grad_w_att, w_att, m_w, v_w),
                (grad_W_clf, W_clf, m_W, v_W),
                (grad_b_clf, b_clf, m_b, v_b),
            ):
                m *= beta1
                m += (1 - beta1) * grad
                v *= beta2
                v += (1 - beta2) * (grad**2)
                m_hat = m / (1 - beta1**t)
                v_hat = v / (1 - beta2**t)
                param -= self.lr * m_hat / (np.sqrt(v_hat) + eps)

        self.w_att_ = w_att
        self.W_clf_ = W_clf
        self.b_clf_ = b_clf
        return self

    def predict_proba(self, X):
        import numpy as np

        chunk_mats = self._embed_raw(X)
        probs = np.empty((len(chunk_mats), len(self.classes_)))
        for i, C in enumerate(chunk_mats):
            scores = C @ self.w_att_
            attn = self._softmax(scores)
            doc_vec = attn @ C
            logits = doc_vec @ self.W_clf_ + self.b_clf_
            probs[i] = self._softmax(logits)
        return probs

    def predict(self, X):
        import numpy as np

        probs = self.predict_proba(X)
        return self.classes_[np.argmax(probs, axis=1)]

    def chunk_attention_debug(self, text: str):
        """Utilitaire de debug (pas utilisé par le pipeline) : pour UN
        texte, retourne la liste (chunk, poids d'attention appris), triée
        du plus au moins pesant. Permet de vérifier, sur un cas réel comme
        l'email FIS, si l'attention a bien appris à privilégier les chunks
        de signal plutôt que la politesse/les mentions légales."""
        chunks = self._split(text)
        model = self._get_model()
        vectors = model.encode(chunks, batch_size=self.batch_size, show_progress_bar=False, convert_to_numpy=True)
        scores = vectors @ self.w_att_
        attn = self._softmax(scores)
        pairs = list(zip(chunks, attn.tolist()))
        return sorted(pairs, key=lambda p: -p[1])