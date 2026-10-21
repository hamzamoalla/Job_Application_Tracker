#!/usr/bin/env python3
"""
Diagnostic du pipeline de nettoyage + chunking (hors DB / hors modèle).

Pour chaque email :
  1. Texte BRUT (subject + body)
  2. Après chaque étape de nettoyage
  3. Texte final (prepare_ml_text / prepare_ml_text_full)
  4. Chunks (strategy sentence — même découpage que le modèle publié)

Usage :
  # Fichier TSV : subject \\t body \\t [label] \\t [confidence]
  python diagnose_cleaning.py --input mails.tsv --out report.md

  # JSON lignes : {"subject":"...","body":"...","label":"..."}
  python diagnose_cleaning.py --input mails.jsonl --out report.md

  # Exemples intégrés (démo)
  python diagnose_cleaning.py --demo --out report_demo.md

  # Limiter le nombre d'emails
  python diagnose_cleaning.py --input mails.tsv --out report.md --limit 20
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Pipeline de nettoyage (copie alignée sur text_cleaning.py enrichi)
# ---------------------------------------------------------------------------

MAX_BODY_CHARS = 600

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
    r"(?i)^this email was intended for.*$",
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
    r"(?i)^kind regards,?$",
    r"(?i)^best regards,?$",
    r"(?i)^best regards\s*[,|].*$",
    r"(?i)^kind regards\s*[,|].*$",
    r"(?i)^cordialement,?$",
    r"(?i)^bien cordialement,?$",
    r"(?i)^sincerely,?$",
    r"(?i)^sincerely yours,?$",
    r"(?i).*proprietary and/or confidential.*",
    r"(?i).*not the intended recipient.*",
    r"(?i).*online privacy notice.*",
    r"(?i).*this message is.*confidential.*",
    r"(?i).*if you are not the intended recipient.*",
    r"(?i).*delete the message and all copies.*",
    r"(?i).*subject to archiving and review.*",
]

SIGNATURE_CUT_RE = re.compile(
    r"(?im)^(?:"
    r"kind\s+regards|best\s+regards|best\s+wishes|"
    r"cordialement|bien\s+cordialement|sincerely(?:\s+yours)?|"
    r"mit\s+freundlichen\s+gr[uü]ßen|viele\s+gr[uü]ße|beste\s+gr[uü]ße|"
    r"warm\s+regards|thanks(?:\s+again)?|thank\s+you"
    r")\s*,?\s*$"
)

URL_RE = re.compile(r"(?i)\b(?:https?://|www\.)\S+")
MAILTO_RE = re.compile(r"(?i)\bmailto:\S+")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def remove_invisible_chars(text: str) -> str:
    if not text:
        return ""
    invisible = re.compile(
        r"[\u0000-\u0008\u000B\u000C\u000E-\u001F"
        r"\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u206f"
        r"\ufeff\u00ad\u034f\u061c\u180e\u2000-\u200a]"
    )
    text = invisible.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_reply(body: str) -> str:
    if not body:
        return ""
    cleaned = body
    for pattern in CUT_PATTERNS:
        match = re.search(pattern, cleaned)
        if match and match.start() > 80:
            cleaned = cleaned[: match.start()]
    cleaned = "\n".join(
        line for line in cleaned.splitlines() if not line.lstrip().startswith(">")
    )
    return cleaned.strip()


def strip_boilerplate(text: str) -> str:
    if not text:
        return ""
    lines = []
    for line in text.splitlines():
        if any(re.match(p, line.strip()) for p in BOILERPLATE_LINE_PATTERNS):
            continue
        lines.append(line)
    result = "\n".join(lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def strip_trailing_signature_block(text: str) -> str:
    """
    Coupe le corps APRÈS la dernière signature (Cordialement / Kind regards / …)
    s'il reste du texte ensuite (footer, legal, admin).

    On ne coupe pas si :
    - aucune signature
    - mail trop court (< 4 lignes)
    - la signature est tout le mail (rien de substantiel avant)
    """
    if not text or not text.strip():
        return text or ""

    lines = text.splitlines()
    if len(lines) < 4:
        return text.strip()

    sig_indices = [
        i for i, line in enumerate(lines) if SIGNATURE_CUT_RE.match(line.strip())
    ]
    if not sig_indices:
        return text.strip()

    last_sig = sig_indices[-1]

    # Rien après la signature → rien à couper
    if last_sig >= len(lines) - 1:
        return text.strip()

    # Rien de substantiel AVANT la signature → mail = signature seule, on garde
    before = "\n".join(lines[:last_sig]).strip()
    if len(before.split()) < 8:
        return text.strip()

    # Corps utile + footer après signature → on garde jusqu'à la signature incluse
    kept = lines[: last_sig + 1]
    result = "\n".join(kept)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def strip_urls(text: str) -> str:
    if not text:
        return ""
    text = URL_RE.sub("", text)
    text = MAILTO_RE.sub("", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\[\s*\]", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate(text: str, max_chars: int = MAX_BODY_CHARS) -> str:
    if not text or len(text) <= max_chars:
        return text or ""
    return text[:max_chars].rstrip() + " […]"


def split_sentences(text: str, min_words: int = 4) -> list[str]:
    if not text or not text.strip():
        return []
    raw = _SENTENCE_SPLIT_RE.split(text.strip())
    sentences = [s.strip() for s in raw if s.strip()]
    kept = [s for s in sentences if len(s.split()) >= min_words]
    return kept or sentences


def pipeline_steps(subject: str, body: str) -> dict:
    """Retourne chaque étape du nettoyage pour inspection.

    Ordre important : signature_cut AVANT boilerplate.
    Sinon strip_boilerplate enlève la ligne « Kind Regards » et
    strip_trailing_signature_block n'a plus d'ancre pour couper le legal.
    """
    steps: dict[str, str] = {}
    steps["0_raw_body"] = body or ""
    t = remove_invisible_chars(body or "")
    steps["1_after_invisible"] = t
    t = clean_reply(t)
    steps["2_after_clean_reply"] = t
    t = strip_trailing_signature_block(t)
    steps["3_after_signature_cut"] = t
    t = strip_boilerplate(t)
    steps["4_after_boilerplate"] = t
    t = strip_urls(t)
    steps["5_after_strip_urls"] = t
    steps["6_prepare_ml_text_full"] = f"Subject: {(subject or '').strip()}\nBody: {t}".strip()
    truncated = truncate(t, MAX_BODY_CHARS)
    steps["7_prepare_ml_text_truncated"] = (
        f"Subject: {(subject or '').strip()}\nBody: {truncated}".strip()
    )
    return steps


def flag_anomalies(steps: dict, chunks: list[str]) -> list[str]:
    """Heuristiques de mauvais comportement à signaler dans le rapport."""
    flags = []
    full = steps.get("6_prepare_ml_text_full", "")
    raw = steps.get("0_raw_body", "")
    after_sig = steps.get("3_after_signature_cut", "")
    after_bp = steps.get("4_after_boilerplate", "")

    if not full.strip() or full.strip() == f"Subject: \nBody:" or full.endswith("Body:"):
        flags.append("⚠️  Texte final quasi vide après nettoyage")

    if len(raw) > 200 and len(after_sig) < 40:
        flags.append("⚠️  Signature cut a trop agressivement vidé le corps")

    legal_markers = [
        "proprietary and/or confidential",
        "not the intended recipient",
        "online privacy notice",
        "subject to archiving",
    ]
    full_l = full.lower()
    for m in legal_markers:
        if m in full_l:
            flags.append(f"⚠️  Marqueur légal encore présent après clean: « {m} »")

    if len(chunks) >= 10:
        flags.append(f"ℹ️  Beaucoup de chunks ({len(chunks)}) — risque de dilution mean-pool")

    short = sum(1 for c in chunks if len(c.split()) < 6)
    if chunks and short / len(chunks) > 0.4:
        flags.append(
            f"ℹ️  {short}/{len(chunks)} chunks très courts (<6 mots) — peu de signal seul"
        )

    if after_bp == after_sig and "kind regards" in after_bp.lower():
        # signature pas coupée alors qu'elle est là
        if SIGNATURE_CUT_RE.search(after_bp):
            # si dans 1ere moitié on ne coupe pas — ok
            pass

    return flags


def md_escape_fence(text: str) -> str:
    """Évite de casser les fences markdown si le body contient ```."""
    return text.replace("```", "``\u200b`")


def render_email_report(
    idx: int,
    subject: str,
    body: str,
    label: str | None = None,
    confidence: float | None = None,
) -> str:
    steps = pipeline_steps(subject, body)
    full = steps["6_prepare_ml_text_full"]
    chunks = split_sentences(full)
    flags = flag_anomalies(steps, chunks)

    meta = []
    if label is not None:
        meta.append(f"**label prédit/attendu:** `{label}`")
    if confidence is not None:
        meta.append(f"**confidence:** `{confidence:.3f}`")
    meta_line = " · ".join(meta) if meta else ""

    parts = [
        f"## Email #{idx}",
        f"**Subject:** {subject or '(vide)'}",
        meta_line,
        "",
        f"- Longueur brut: **{len(body or '')}** car.",
        f"- Longueur full (après clean): **{len(full)}** car.",
        f"- Longueur truncated (600): **{len(steps['7_prepare_ml_text_truncated'])}** car.",
        f"- Nombre de chunks (sentence): **{len(chunks)}**",
        "",
    ]
    if flags:
        parts.append("### Alertes")
        parts.extend(f"- {f}" for f in flags)
        parts.append("")

    # Étapes
    step_titles = [
        ("0_raw_body", "0 — Body BRUT"),
        ("1_after_invisible", "1 — Après remove_invisible_chars"),
        ("2_after_clean_reply", "2 — Après clean_reply (citations)"),
        ("3_after_signature_cut", "3 — Après strip_trailing_signature_block"),
        ("4_after_boilerplate", "4 — Après strip_boilerplate"),
        ("5_after_strip_urls", "5 — Après strip_urls"),
        ("6_prepare_ml_text_full", "6 — FINAL full (Subject + Body) → chunking"),
        ("7_prepare_ml_text_truncated", "7 — FINAL truncated 600 (APPLICATION)"),
    ]
    parts.append("### Étapes de nettoyage")
    for key, title in step_titles:
        text = steps.get(key, "")
        parts.append(f"#### {title}")
        parts.append(f"*({len(text)} caractères)*")
        parts.append("```")
        parts.append(md_escape_fence(text if text else "(vide)"))
        parts.append("```")
        parts.append("")

    parts.append("### Chunks (split_sentences, min_words=4)")
    if not chunks:
        parts.append("*(aucun chunk)*")
    else:
        for i, ch in enumerate(chunks, 1):
            nw = len(ch.split())
            parts.append(f"**chunk[{i}/{len(chunks)}]** — {len(ch)} car., {nw} mots")
            parts.append("```")
            parts.append(md_escape_fence(ch))
            parts.append("```")
            parts.append("")

    parts.append("---")
    parts.append("")
    return "\n".join(parts)


def load_csv(path: Path) -> list[dict]:
    """CSV avec header (subject,body,classification,confidence) — gère multi-lignes quotés."""
    import csv

    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for obj in reader:
            conf = obj.get("confidence")
            try:
                conf_f = float(conf) if conf not in (None, "") else None
            except (TypeError, ValueError):
                conf_f = None
            rows.append(
                {
                    "subject": (obj.get("subject") or "").strip(),
                    "body": obj.get("body") or obj.get("text") or "",
                    "label": obj.get("classification") or obj.get("label"),
                    "confidence": conf_f,
                }
            )
    return rows


def load_tsv(path: Path) -> list[dict]:
    """TSV simple (1 ligne = 1 mail). Préférer CSV si bodies multi-lignes."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        subject = parts[0] if len(parts) > 0 else ""
        body = parts[1] if len(parts) > 1 else ""
        label = parts[2] if len(parts) > 2 else None
        conf = None
        if len(parts) > 3:
            try:
                conf = float(parts[3])
            except ValueError:
                conf = None
        rows.append(
            {"subject": subject, "body": body, "label": label, "confidence": conf}
        )
    return rows


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        rows.append(
            {
                "subject": obj.get("subject") or "",
                "body": obj.get("body") or obj.get("text") or "",
                "label": obj.get("label") or obj.get("classification"),
                "confidence": obj.get("confidence"),
            }
        )
    return rows


def demo_emails() -> list[dict]:
    """Quelques cas représentatifs pour valider le pipeline sans fichier d'entrée."""
    return [
        {
            "subject": "FIS Application Update - Hamza Moalla - JR0308866 Product Technical Support Analyst",
            "body": """Dear Hamza,
Thank you for your time and interest in FIS. Unfortunately, given the timing of your application, your resume wasn't reviewed prior to the hiring decision being made. We're sorry that we missed you!
While you are not being considered further for this position, you may qualify for a number of our other posted positions. We invite you to join our
Talent Network
to receive job alerts with new job opportunities that match your interests.
We hope you'll keep us in mind, and we encourage you to apply again! In the meantime, please consider following us on the below social media sites to stay up to date on our company, new job postings, and more.
We sincerely appreciate the time you invested in the application process and wish you every success in future endeavors.
Kind Regards,
FIS Talent Acquisition
FIS is committed to protecting the privacy and security of all personal information that we process in order to provide services to our clients. For specific information on how FIS protects personal information online, please
see the Online Privacy Notice.
The information contained in this message is proprietary and/or confidential. If you are not the intended recipient, please: (i) delete the message and all copies; (ii) do not disclose, distribute or use the message
in any manner; and (iii) notify the sender immediately. In addition, please be aware that any message addressed to our domain is subject to archiving and review by persons other than the intended recipient. Thank you.""",
            "label": "REJECTION",
            "confidence": 0.585,
        },
        {
            "subject": "Your Job Application at much. Consulting",
            "body": """Dear Hamza Moalla,
Thank you very much for your interest in much. Consulting!
We successfully received your application and will review it in the next 3 working days.
We kindly ask for your patience and we will get back to you as soon as possible.
In the meanwhile, we would like to invite you to find out more about our team at: https://muchconsulting.com/career.
Best regards,
Your much. P&C Team
Mail: apply@muchconsulting.de
Phone: +49 89 277817740""",
            "label": "IN_REVIEW",
            "confidence": 0.54,
        },
        {
            "subject": "Hello",
            "body": "Just for test",
            "label": "OTHER",
            "confidence": 0.67,
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnostic nettoyage + chunks → fichier")
    parser.add_argument("--input", "-i", type=Path, help="Fichier .tsv ou .jsonl")
    parser.add_argument(
        "--out", "-o", type=Path, default=Path("cleaning_diagnostic_report.md")
    )
    parser.add_argument("--demo", action="store_true", help="Utiliser les emails de démo")
    parser.add_argument("--limit", type=int, default=None, help="Max emails à traiter")
    args = parser.parse_args()

    if args.demo:
        emails = demo_emails()
    elif args.input:
        suf = args.input.suffix.lower()
        if suf == ".jsonl":
            emails = load_jsonl(args.input)
        elif suf == ".csv":
            emails = load_csv(args.input)
        else:
            # .tsv ou extension inconnue : tenter CSV si header présent, sinon TSV
            head = args.input.read_text(encoding="utf-8-sig")[:200]
            if "subject" in head.lower() and ("," in head or "\t" in head):
                try:
                    emails = load_csv(args.input)
                except Exception:
                    emails = load_tsv(args.input)
            else:
                emails = load_tsv(args.input)
    else:
        print("Fournir --input fichier.csv|.tsv|.jsonl ou --demo", file=sys.stderr)
        sys.exit(1)

    if args.limit is not None:
        emails = emails[: args.limit]

    header = [
        "# Rapport diagnostic — nettoyage & chunking",
        "",
        f"- Emails analysés: **{len(emails)}**",
        f"- MAX_BODY_CHARS: `{MAX_BODY_CHARS}`",
        "- Chunking: `split_sentences` (min_words=4)",
        "",
        "Pour chaque mail: brut → étapes de clean → final full/truncated → chunks.",
        "Les ⚠️ signalent un comportement suspect (texte vidé, legal restant, trop de chunks).",
        "",
        "---",
        "",
    ]
    body_parts = [render_email_report(
        i + 1,
        e["subject"],
        e["body"],
        e.get("label"),
        e.get("confidence"),
    ) for i, e in enumerate(emails)]

    report = "\n".join(header) + "\n".join(body_parts)
    args.out.write_text(report, encoding="utf-8")
    print(f"Rapport écrit → {args.out.resolve()} ({len(emails)} emails)")


if __name__ == "__main__":
    main()