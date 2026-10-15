"""
Classifier worker – polls unprocessed emails, classifies them and
updates applications.

Models are loaded via joblib from MODEL_DIR (/app/models).
Joblib files are hot-reloaded when their mtime changes (no restart needed).
"""

from __future__ import annotations

import logging
import os
import time

import psycopg
from psycopg.rows import dict_row

from text_cleaning import clean_for_extraction

import worker.classification as classification
import worker.extraction as extraction
from worker.matching import (
    ROLE_BY_LABEL,
    STATUS_BY_LABEL,
    apply_rejection,
    consolidate_duplicate_applications,
    create_application,
    expire_stale_applications,
    find_matching_application,
    insert_processing_event,
    link_email,
    update_application_status,
)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "15"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.80"))
ENABLE_GLINER = os.getenv("ENABLE_GLINER_FALLBACK", "true").lower() in ("1", "true", "yes")


# Tracks mtime of joblib files to hot-reload without container restart
_model_mtimes: dict[str, float] = {}


def _file_mtime(path: str) -> float | None:
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def load_sklearn_models(force: bool = False) -> bool:
    """
    Load application/reply joblib models.
    If force=False, only reload when file mtime changed.
    Returns True if at least one model was (re)loaded.
    """
    import joblib

    model_dir = os.getenv("MODEL_DIR", "/app/models")
    paths = {
        "application": os.path.join(model_dir, "application_model.joblib"),
        "reply": os.path.join(model_dir, "reply_model.joblib"),
    }
    reloaded = False

    for key, path in paths.items():
        mtime = _file_mtime(path)
        prev = _model_mtimes.get(key)
        if not force and mtime is not None and prev is not None and mtime == prev:
            continue

        if mtime is None:
            if key == "application":
                classification.application_model = None
            else:
                classification.reply_model = None
            _model_mtimes.pop(key, None)
            if force:
                logger.warning("Modèle introuvable : %s", path)
            continue

        try:
            model = joblib.load(path)
            if key == "application":
                classification.application_model = model
            else:
                classification.reply_model = model
            _model_mtimes[key] = mtime
            reloaded = True
            logger.info("Modèle chargé : %s (%s)", key + "_model", path)
        except Exception:
            logger.exception("Échec chargement %s", path)

    return reloaded


def load_models() -> None:
    """Initial load: sklearn models + optional GLiNER."""
    load_sklearn_models(force=True)

    if ENABLE_GLINER:
        try:
            from gliner import GLiNER

            name = os.getenv("GLINER_MODEL_NAME", "urchade/gliner_multi-v2.1")
            logger.info("Chargement GLiNER (%s)…", name)
            extraction.gliner_model = GLiNER.from_pretrained(name)
            logger.info("GLiNER chargé.")
        except Exception:
            logger.exception("Échec chargement GLiNER – fallback regex/domaine uniquement.")
            extraction.gliner_model = None
    else:
        logger.info("GLiNER désactivé (ENABLE_GLINER_FALLBACK=false).")
        extraction.gliner_model = None


def maybe_reload_models() -> None:
    """Called each poll loop – hot-reload joblib if trainer published new files."""
    if load_sklearn_models(force=False):
        logger.info("Nouveaux modèles détectés et rechargés (hot-reload).")


def human_confirmed_label(email: dict) -> tuple[str, float] | None:
    """
    Label API sets confidence=1.0 and processed=FALSE for human review.
    On reprocess, trust that label — do NOT re-run the ML model.
    """
    conf = email.get("confidence")
    label = email.get("classification")
    if conf is None or not label:
        return None
    try:
        if float(conf) >= 0.999:
            return str(label), 1.0
    except (TypeError, ValueError):
        return None
    return None


def process_sent_email(conn, email: dict) -> None:
    confirmed = human_confirmed_label(email)
    if confirmed:
        label, confidence = confirmed
        logger.info(
            "Email SENT id=%s: label humain conservé %s (conf=1.0)",
            email["id"],
            label,
        )
    else:
        label, confidence = classification.classify_sent(email)

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE emails
            SET classification = %s, confidence = %s, processed = TRUE
            WHERE id = %s
            """,
            (label, confidence, email["id"]),
        )

    if label != "JOB_APPLICATION" or confidence < MIN_CONFIDENCE:
        insert_processing_event(
            conn,
            email["id"],
            "SENT_EMAIL_CLASSIFIED",
            {
                "classification": label,
                "confidence": confidence,
                "application_created": False,
            },
        )
        return

    subject, body = clean_for_extraction(email.get("subject"), email.get("body"))
    company, position, company_src, position_src = extraction.extract_company_and_position(
        email.get("recipient"), subject, body
    )

    if not company:
        insert_processing_event(
            conn,
            email["id"],
            "NEEDS_MANUAL_REVIEW",
            {
                "classification": label,
                "confidence": confidence,
                "reason": "Entreprise impossible à déterminer sur email envoyé.",
            },
        )
        return

    existing = find_matching_application(
        conn, company, position, address=email.get("recipient")
    )

    if existing:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE applications
                SET company = COALESCE(company, %s),
                    position = COALESCE(position, %s),
                    sent_email_id = COALESCE(sent_email_id, %s),
                    source = CASE
                        WHEN source IN ('WEBSITE_ASSUMED', 'UNKNOWN') THEN 'EMAIL'
                        ELSE source
                    END,
                    status = CASE
                        WHEN status IN ('INTERVIEW', 'REJECTED') THEN status
                        ELSE 'IN_REVIEW'
                    END,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (company, position, email["id"], existing["id"]),
            )
        link_email(
            conn, existing["id"], email["id"], "SENT", addresses=[email.get("recipient")]
        )
        insert_processing_event(
            conn,
            email["id"],
            "APPLICATION_FROM_SENT_EMAIL",
            {
                "application_id": existing["id"],
                "company": company,
                "position": position,
                "company_source": company_src,
                "position_source": position_src,
                "confidence": confidence,
            },
        )
    else:
        create_application(
            conn,
            email,
            company,
            position,
            "IN_REVIEW",
            confidence,
            "EMAIL",
            "SENT",
            company_src,
            position_src,
        )
        insert_processing_event(
            conn,
            email["id"],
            "APPLICATION_FROM_SENT_EMAIL",
            {
                "company": company,
                "position": position,
                "company_source": company_src,
                "position_source": position_src,
                "confidence": confidence,
                "status": "IN_REVIEW",
            },
        )


def process_received_email(conn, email: dict) -> None:
    confirmed = human_confirmed_label(email)
    if confirmed:
        label, confidence = confirmed
        logger.info(
            "Email RECEIVED id=%s: label humain conservé %s (conf=1.0)",
            email["id"],
            label,
        )
    else:
        label, confidence = classification.classify_received(email)

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE emails
            SET classification = %s, confidence = %s, processed = TRUE
            WHERE id = %s
            """,
            (label, confidence, email["id"]),
        )

    target_status = STATUS_BY_LABEL.get(label)
    role = ROLE_BY_LABEL.get(label, "OTHER")

    if not target_status:
        insert_processing_event(
            conn,
            email["id"],
            "RECEIVED_EMAIL_CLASSIFIED",
            {
                "classification": label,
                "confidence": confidence,
                "application_updated": False,
                "reason": "Email non lié à une étape de candidature.",
            },
        )
        return

    min_for_action = (
        0.70 if label in ("REJECTION", "INTERVIEW", "IN_REVIEW") else MIN_CONFIDENCE
    )
    if confidence < min_for_action:
        insert_processing_event(
            conn,
            email["id"],
            "NEEDS_MANUAL_REVIEW",
            {
                "classification": label,
                "confidence": confidence,
                "reason": "Confiance insuffisante (< 0.70).",
            },
        )
        return

    subject, body = clean_for_extraction(email.get("subject"), email.get("body"))
    company, position, company_src, position_src = extraction.extract_company_and_position(
        email.get("sender"), subject, body
    )

    if not company:
        insert_processing_event(
            conn,
            email["id"],
            "NEEDS_MANUAL_REVIEW",
            {
                "classification": label,
                "confidence": confidence,
                "reason": "Entreprise impossible à identifier sur email reçu.",
                "sender": email.get("sender"),
                "subject": email.get("subject"),
            },
        )
        return

    if label == "REJECTION":
        apply_rejection(
            conn, email, company, position, confidence, company_src, position_src
        )
        return

    existing = find_matching_application(
        conn, company, position, address=email.get("sender")
    )

    if existing:
        update_application_status(
            conn,
            existing,
            email,
            target_status,
            confidence,
            role,
            company,
            position,
            company_src,
            position_src,
        )
    else:
        create_application(
            conn,
            email,
            company,
            position,
            target_status,
            confidence,
            "WEBSITE_ASSUMED",
            role,
            company_src,
            position_src,
        )
        insert_processing_event(
            conn,
            email["id"],
            "APPLICATION_CREATED_FROM_RECEIVED_EMAIL",
            {
                "company": company,
                "position": position,
                "company_source": company_src,
                "position_source": position_src,
                "status": target_status,
                "source": "WEBSITE_ASSUMED",
                "confidence": confidence,
            },
        )


def process_email(conn, email: dict) -> None:
    if email["direction"] == "SENT":
        process_sent_email(conn, email)
    elif email["direction"] == "RECEIVED":
        process_received_email(conn, email)
    else:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE emails
                SET classification = 'OTHER', confidence = 0.0, processed = TRUE
                WHERE id = %s
                """,
                (email["id"],),
            )


def main() -> None:
    load_models()

    while True:
        try:
            maybe_reload_models()
            with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
                with conn.transaction():
                    expire_stale_applications(conn)
                    consolidate_duplicate_applications(conn)

                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, gmail_id, thread_id, direction,
                               sender, recipient, subject, body, sent_at,
                               classification, confidence
                        FROM emails
                        WHERE processed = FALSE
                        ORDER BY id ASC
                        LIMIT %s
                        FOR UPDATE SKIP LOCKED
                        """,
                        (BATCH_SIZE,),
                    )
                    emails = cur.fetchall()

                if not emails:
                    time.sleep(POLL_INTERVAL)
                    continue

                for email in emails:
                    try:
                        with conn.transaction():
                            process_email(conn, email)
                    except Exception:
                        logger.exception("Erreur email id=%s", email["id"])
        except Exception:
            logger.exception("Erreur boucle worker")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
