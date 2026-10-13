import os
from pathlib import Path
from collections import Counter

import psycopg
import joblib

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report

from ml_embedding import SentenceEmbedder, DEFAULT_MODEL_NAME


DB = os.environ["DATABASE_URL"]
MODEL_DIR = Path("/app/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", DEFAULT_MODEL_NAME)


def build_model():
    """
    Pipeline à base d'embeddings sémantiques plutôt que de TF-IDF :

      texte -> SentenceEmbedder (modèle pré-entraîné multilingue,
               384 dimensions) -> LogisticRegression

    Pourquoi ce changement par rapport à TF-IDF + Naive Bayes/Logistic
    Regression : TF-IDF compte des mots/n-grams exacts, donc deux
    formulations différentes d'un même refus ("on ne va pas donner
    suite" vs "nous avons décidé de ne pas poursuivre") ne partagent
    quasiment aucun token et le modèle ne peut pas faire le lien. Les
    embeddings de phrases encodent le SENS : ces deux phrases se
    retrouvent proches dans l'espace vectoriel parce que le modèle a été
    pré-entraîné sur des milliards de phrases avant même de voir vos
    emails. Avec seulement ~30 exemples par label, c'est ce transfert de
    connaissance qui généralise le mieux sur des formulations jamais
    vues.

    Logistic Regression suffit en sortie : les embeddings sont déjà des
    features denses et informatives (contrairement à TF-IDF sparse), pas
    besoin d'un classifieur plus complexe.
    """
    return Pipeline([
        ("embed", SentenceEmbedder(model_name=EMBEDDING_MODEL_NAME)),
        (
            "clf",
            LogisticRegression(
                C=1.0,
                max_iter=2000,
                class_weight="balanced",
                solver="lbfgs",
                multi_class="auto",
            ),
        ),
    ])


def train(task: str, output_name: str):
    with psycopg.connect(DB) as connection:
        rows = connection.execute(
            """
            SELECT text, label
            FROM training_examples
            WHERE task = %s
            ORDER BY id
            """,
            (task,),
        ).fetchall()

    # Nettoyage des exemples vides
    rows = [
        (text.strip(), label)
        for text, label in rows
        if text and text.strip() and label
    ]

    if len(rows) < 10:
        raise RuntimeError(
            f"Not enough {task} examples: {len(rows)} found; "
            "at least 10 are required."
        )

    texts = [row[0] for row in rows]
    labels = [row[1] for row in rows]
    counts = Counter(labels)

    if len(counts) < 2:
        raise RuntimeError(
            f"{task} requires at least two labels; found {dict(counts)}"
        )

    print(f"\n{'='*60}")
    print(f"Training task: {task}")
    print(f"Examples: {len(rows)}")
    print(f"Label distribution: {dict(counts)}")
    print(f"Embedding model: {EMBEDDING_MODEL_NAME}")
    print(f"{'='*60}")

    smallest_class = min(counts.values())

    if smallest_class >= 2:
        n_splits = min(5, smallest_class)

        cv = StratifiedKFold(
            n_splits=n_splits,
            shuffle=True,
            random_state=42,
        )
        evaluation_model = build_model()

        # L'encodage des embeddings est la partie la plus lente de ce
        # script (modèle de ~470 Mo, CPU). La cross-validation ré-encode
        # les mêmes textes à chaque fold ; c'est volontairement laissé
        # ainsi pour rester simple, le volume d'exemples reste faible.
        scores = cross_val_score(
            evaluation_model,
            texts,
            labels,
            cv=cv,
            scoring="f1_macro",
            error_score="raise",
        )

        print(
            f"{task} cross-validation F1 macro: "
            f"{scores.mean():.3f} +/- {scores.std():.3f}"
        )
        print(f"Scores by fold: {[round(float(s), 3) for s in scores]}")
    else:
        print(
            f"WARNING: {task} has a label with only one example. "
            "Cross-validation is not possible reliably."
        )

    # Entraînement final sur toutes les données
    final_model = build_model()
    final_model.fit(texts, labels)

    # Affichage d'un petit rapport sur les données d'entraînement
    predictions = final_model.predict(texts)
    print("\nClassification report (on training data):")
    print(classification_report(labels, predictions, zero_division=0))

    output_path = MODEL_DIR / output_name
    joblib.dump(final_model, output_path)

    print(f"Saved {task} model to {output_path}\n")


if __name__ == "__main__":
    train("APPLICATION", "application_model.joblib")
    train("REPLY", "reply_model.joblib")