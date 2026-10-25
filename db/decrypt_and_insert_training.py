#!/usr/bin/env python3
"""
decrypt_and_insert_training.py
-------------------------------
Déchiffre le fichier .enc (produit par encrypt_training_data.py) avec une
clé saisie en entrée au moment de l'exécution, puis insère les exemples
directement dans la table `training_examples`. Pensé pour être lancé au
redéploiement (ex: dans le conteneur `trainer`, ou en script de setup).

La clé n'est JAMAIS écrite dans le script, ni passée en argument de ligne
de commande (ce qui finirait dans l'historique shell / les logs) : elle est
toujours demandée de façon interactive (saisie masquée).

Installation :
    pip install cryptography psycopg[binary]
    # (si tu préfères psycopg2 : pip install cryptography psycopg2-binary
    #  — le script bascule automatiquement dessus si psycopg n'est pas là)

Format de fichier attendu (texte, un exemple par ligne, 6 champs séparés
par des tabulations, tel qu'exporté par `psql` avec \t activé) :

    id<TAB>"task"<TAB>"text"<TAB>"label"<TAB>"created_at"<TAB>"subject"

`id` et `created_at` sont ignorés à l'insertion (la table génère ses
propres `id`/`created_at` par défaut) — seuls `task`, `text`, `label` et
`subject` sont utilisés. Les doublons exacts (même task/label/subject/text)
sont silencieusement ignorés grâce à la contrainte UNIQUE existante.

Variables d'environnement :
    DATABASE_URL   obligatoire, ex:
                   postgresql://jobtracker:jobtracker@localhost:5432/jobtracker

Usage :
    python decrypt_and_insert_training.py training_data.enc
"""

import base64
import csv
import getpass
import io
import os
import sys

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

try:
    import psycopg
    PSYCOPG_V3 = True
except ImportError:
    import psycopg2 as psycopg  # type: ignore
    PSYCOPG_V3 = False

KDF_ITERATIONS = 480_000
SALT_SIZE = 16
VALID_TASKS = {"APPLICATION", "REPLY"}


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def decrypt_file(path: str, password: str) -> bytes:
    with open(path, "rb") as f:
        raw = f.read()
    salt, token = raw[:SALT_SIZE], raw[SALT_SIZE:]
    key = derive_key(password, salt)
    try:
        return Fernet(key).decrypt(token)
    except InvalidToken:
        print("Erreur : déchiffrement impossible — clé incorrecte ou fichier corrompu/altéré.")
        sys.exit(1)


def parse_lines(text: str):
    """Parse le format TSV id\\ttask\\ttext\\tlabel\\tcreated_at\\tsubject.

    Un champ 'text' peut contenir des retours à la ligne littéraux tant
    qu'il reste entre guillemets (comme dans l'export original) : le module
    csv standard gère nativement ce cas (RFC4180), donc on ne réinvente pas
    de parseur ligne par ligne.
    """
    reader = csv.reader(io.StringIO(text), delimiter="\t", quotechar='"')
    parsed = []
    for rec in reader:
        if len(rec) < 4 or not rec[0].strip().isdigit():
            continue
        task = rec[1].strip()
        text_field = rec[2]
        label = rec[3].strip()
        subject = rec[5].strip() if len(rec) > 5 else None
        if task not in VALID_TASKS or not label:
            continue
        parsed.append({"task": task, "text": text_field, "label": label, "subject": subject})
    return parsed


def insert_examples(examples, database_url: str):
    inserted, skipped = 0, 0
    conn = psycopg.connect(database_url)
    try:
        with conn:
            with conn.cursor() as cur:
                for ex in examples:
                    cur.execute(
                        """
                        INSERT INTO training_examples (task, text, label, subject)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (task, label, subject, text) DO NOTHING
                        """,
                        (ex["task"], ex["text"], ex["label"], ex["subject"]),
                    )
                    if cur.rowcount == 1:
                        inserted += 1
                    else:
                        skipped += 1
    finally:
        conn.close()
    return inserted, skipped


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python decrypt_and_insert_training.py <fichier.enc>")
        sys.exit(1)

    enc_path = sys.argv[1]
    if not os.path.isfile(enc_path):
        print(f"Erreur : fichier introuvable : {enc_path}")
        sys.exit(1)

    database_url = "postgresql://jobtracker:jobtracker@localhost:5432/jobtracker"
    if not database_url:
        print("Erreur : variable d'environnement DATABASE_URL manquante.")
        sys.exit(1)

    password = getpass.getpass("Clé de déchiffrement (mot de passe) : ")

    plaintext = decrypt_file(enc_path, password)
    examples = parse_lines(plaintext.decode("utf-8"))

    if not examples:
        print("Aucun exemple valide trouvé après déchiffrement — vérifie le format du fichier source.")
        sys.exit(1)

    print(f"{len(examples)} exemple(s) déchiffré(s), insertion dans training_examples...")
    inserted, skipped = insert_examples(examples, database_url)
    print(f"OK : {inserted} inséré(s), {skipped} ignoré(s) (doublons déjà présents).")


if __name__ == "__main__":
    main()
