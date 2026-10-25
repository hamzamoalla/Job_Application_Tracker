#!/usr/bin/env python3
"""
encrypt_training_data.py
-------------------------
Chiffre un fichier texte (ex: export de `training_examples`) avec une clé
(mot de passe) saisie en entrée au moment de l'exécution — la clé n'est
JAMAIS écrite dans le script ni dans un fichier.

Le fichier chiffré produit est celui que tu pousses sur GitHub. Le fichier
en clair, lui, ne doit jamais être commité.

Algorithme : PBKDF2-HMAC-SHA256 (480 000 itérations, sel aléatoire 16
octets) pour dériver une clé à partir du mot de passe, puis chiffrement
symétrique Fernet (AES-128-CBC + HMAC-SHA256, authentifié) de la librairie
`cryptography`.

Format du fichier de sortie : [16 octets de sel][token Fernet].
Le sel n'est pas secret (il sert juste à dériver la clé de façon unique à
chaque chiffrement) ; sans le mot de passe, le fichier reste illisible.

Installation :
    pip install cryptography

Usage :
    python encrypt_training_data.py training_data.txt training_data.enc
"""

import base64
import getpass
import os
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ITERATIONS = 480_000
SALT_SIZE = 16


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python encrypt_training_data.py <fichier_entree.txt> <fichier_sortie.enc>")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    if not os.path.isfile(input_path):
        print(f"Erreur : fichier introuvable : {input_path}")
        sys.exit(1)

    password = getpass.getpass("Clé de chiffrement (mot de passe) : ")
    password_confirm = getpass.getpass("Confirme la clé : ")
    if password != password_confirm:
        print("Erreur : les deux clés saisies ne correspondent pas.")
        sys.exit(1)
    if len(password) < 8:
        print("Attention : clé très courte, préfère une phrase de passe plus longue.")

    with open(input_path, "rb") as f:
        plaintext = f.read()

    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    token = Fernet(key).encrypt(plaintext)

    with open(output_path, "wb") as f:
        f.write(salt)
        f.write(token)

    print(f"OK : {input_path} -> {output_path} ({len(plaintext)} octets en clair -> {len(salt) + len(token)} octets chiffrés)")
    print("Le fichier .enc peut être poussé sur GitHub. Ne commite jamais le fichier en clair.")


if __name__ == "__main__":
    main()
