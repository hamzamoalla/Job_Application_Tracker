"""
Petit outil interactif pour labelliser rapidement les emails ambigus
(confiance basse) sans avoir à taper des commandes curl à la main.

Usage :
    python label_cli.py
    python label_cli.py --max-confidence 0.7 --direction RECEIVED
    python label_cli.py --api http://localhost:8000

Pour chaque email, affiche le sujet, l'expéditeur et le corps, puis
demande le vrai label au clavier (une touche) :

    1 = IN_REVIEW
    2 = REJECTION
    3 = INTERVIEW
    4 = OTHER
    5 = JOB_APPLICATION   (seulement utile pour les emails SENT)
    s = passer cet email (skip, ne rien enregistrer)
    q = quitter

Ce que fait le script en coulisses, pour chaque label donné :
    POST {api}/emails/{id}/label  { "label": "<LABEL>" }
(c'est l'endpoint déjà présent dans app.py)

Il appelle ensuite /emails?max_confidence=... pour passer à la suite.
Rien n'est stocké en local ; tout part directement vers votre API.
"""

import argparse
import sys
import textwrap

import requests

LABELS = {
    "1": "IN_REVIEW",
    "2": "REJECTION",
    "3": "INTERVIEW",
    "4": "OTHER",
    "5": "JOB_APPLICATION",
}


def fetch_candidates(api, max_confidence, direction, limit):
    params = {"max_confidence": max_confidence, "limit": limit}
    if direction:
        params["direction"] = direction

    response = requests.get(f"{api}/emails", params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def fetch_body(api, email_id):
    response = requests.get(f"{api}/emails/{email_id}", timeout=20)
    response.raise_for_status()
    return response.json()


def send_label(api, email_id, label):
    response = requests.post(
        f"{api}/emails/{email_id}/label",
        json={"label": label},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def print_menu():
    print("\n" + "-" * 60)
    for key, label in LABELS.items():
        print(f"  [{key}] {label}")
    print("  [s] passer   [q] quitter")
    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="Labellisation rapide des emails ambigus")
    parser.add_argument("--api", default="http://localhost:8000", help="URL de l'API")
    parser.add_argument("--max-confidence", type=float, default=0.55)
    parser.add_argument("--direction", default="RECEIVED", help="RECEIVED, SENT, ou vide pour les deux")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    direction = args.direction or None

    candidates = fetch_candidates(args.api, args.max_confidence, direction, args.limit)

    if not candidates:
        print("Aucun email ambigu trouvé avec ces filtres. Rien à labelliser.")
        return

    print(f"{len(candidates)} email(s) à relire (confiance <= {args.max_confidence}).")

    labelled = 0
    skipped = 0

    for item in candidates:
        full = fetch_body(args.api, item["id"])

        print("\n" + "=" * 60)
        print(f"Email #{full['id']}  |  classification actuelle : "
              f"{full['classification']} (confiance {full['confidence']:.2f})")
        print(f"De      : {full['sender']}")
        print(f"Sujet   : {full['subject']}")
        print("Corps   :")
        body = (full.get("body") or "").strip()
        print(textwrap.indent(textwrap.shorten(body, width=600, placeholder=" […]"), "  "))

        print_menu()

        choice = input("Quel est le vrai label ? ").strip().lower()

        if choice == "q":
            break

        if choice == "s" or choice not in LABELS:
            skipped += 1
            continue

        label = LABELS[choice]
        try:
            send_label(args.api, full["id"], label)
            print(f"-> enregistré comme {label}.")
            labelled += 1
        except requests.RequestException as error:
            print(f"ERREUR lors de l'enregistrement : {error}", file=sys.stderr)

    print("\n" + "=" * 60)
    print(f"Terminé. Labellisés : {labelled}  |  Passés : {skipped}")
    print("Pensez à relancer l'entraînement :")
    print("  docker compose run trainer")
    print("=" * 60)


if __name__ == "__main__":
    main()