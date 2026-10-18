from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.config import ALLOWED_LABELS
from app.db import conn
from app.schemas import BatchIdsIn, EmailIn, LabelIn
from app.text_cleaning import clean_for_storage, prepare_ml_text

router = APIRouter(tags=["emails"])


@router.post("/emails")
def insert_email(
    email: EmailIn,
    force_reprocess: bool = Query(
        False,
        description="Si true, force processed=FALSE même si le mail existe déjà (re-import manuel).",
    ),
):
    """
    Insert un email.

    - Nouveau gmail_id → insert, processed=FALSE (le worker le traitera).
    - Déjà présent, contenu identique → **aucune modification** (évite la boucle
      du poll continu qui re-traitait les mêmes mails chaque minute).
    - Déjà présent, subject/body changés → update + processed=FALSE.
    - force_reprocess=true → update + processed=FALSE systématique.
    """
    subject, body = clean_for_storage(email.subject, email.body)

    with conn() as c:
        existing = c.execute(
            """
            SELECT id, subject, body, processed
            FROM emails WHERE gmail_id = %s
            """,
            (email.gmail_id,),
        ).fetchone()

        if existing is None:
            row = c.execute(
                """
                INSERT INTO emails
                (gmail_id, thread_id, direction, sender, recipient, subject, body, sent_at, processed)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s, FALSE)
                RETURNING id, gmail_id
                """,
                (
                    email.gmail_id,
                    email.thread_id,
                    email.direction,
                    email.sender,
                    email.recipient,
                    subject,
                    body,
                    email.sent_at,
                ),
            ).fetchone()
            return {
                "id": row[0],
                "gmail_id": row[1],
                "status": "created",
                "reprocessed": False,
            }

        eid, old_subject, old_body, old_processed = existing
        content_changed = (old_subject or "") != (subject or "") or (old_body or "") != (body or "")

        if not force_reprocess and not content_changed:
            # Poll continu : mail déjà connu et inchangé → ne touche à rien
            return {
                "id": eid,
                "gmail_id": email.gmail_id,
                "status": "exists",
                "reprocessed": False,
            }

        # Contenu changé ou re-import forcé
        c.execute(
            """
            UPDATE emails SET
                thread_id = %s,
                direction = %s,
                sender = %s,
                recipient = %s,
                subject = %s,
                body = %s,
                sent_at = %s,
                processed = FALSE
            WHERE id = %s
            """,
            (
                email.thread_id,
                email.direction,
                email.sender,
                email.recipient,
                subject,
                body,
                email.sent_at,
                eid,
            ),
        )
        return {
            "id": eid,
            "gmail_id": email.gmail_id,
            "status": "reprocessed",
            "reprocessed": True,
            "reason": "forced" if force_reprocess else "content_changed",
        }


@router.get("/emails")
def list_emails(
    max_confidence: float | None = Query(
        None,
        description="Ne renvoyer que les emails dont confidence <= cette valeur.",
    ),
    classification: str | None = Query(
        None,
        description="Filtrer sur une classification précise (ex: IN_REVIEW).",
    ),
    direction: str | None = Query(None, description="SENT ou RECEIVED"),
    include_dismissed: bool = Query(
        False,
        description="Si false (défaut), exclut les emails ignorés (review_dismissed).",
    ),
    limit: int = Query(50, ge=1, le=500),
):
    clauses = ["processed = TRUE"]
    params: list = []

    if max_confidence is not None:
        clauses.append("confidence <= %s")
        params.append(max_confidence)
        # File de review: ne pas réafficher les mails ignorés
        if not include_dismissed:
            clauses.append("COALESCE(review_dismissed, FALSE) = FALSE")

    if classification is not None:
        clauses.append("classification = %s")
        params.append(classification)

    if direction is not None:
        clauses.append("direction = %s")
        params.append(direction)

    where_sql = " AND ".join(clauses)
    params.append(limit)

    with conn() as c:
        rows = c.execute(
            f"""
            SELECT id, gmail_id, thread_id, direction, sender, recipient,
                   subject, classification, confidence, sent_at
            FROM emails
            WHERE {where_sql}
            ORDER BY confidence ASC NULLS FIRST, sent_at DESC NULLS LAST
            LIMIT %s
            """,
            params,
        ).fetchall()

    return [
        {
            "id": r[0],
            "gmail_id": r[1],
            "thread_id": r[2],
            "direction": r[3],
            "sender": r[4],
            "recipient": r[5],
            "subject": r[6],
            "classification": r[7],
            "confidence": r[8],
            "sent_at": r[9],
        }
        for r in rows
    ]


@router.get("/emails/{email_id}")
def get_email(email_id: int):
    with conn() as c:
        row = c.execute(
            """
            SELECT id, gmail_id, thread_id, direction, sender, recipient,
                   subject, body, sent_at, classification, confidence
            FROM emails WHERE id = %s
            """,
            (email_id,),
        ).fetchone()

    if not row:
        raise HTTPException(404, "Email not found")

    return {
        "id": row[0],
        "gmail_id": row[1],
        "thread_id": row[2],
        "direction": row[3],
        "sender": row[4],
        "recipient": row[5],
        "subject": row[6],
        "body": row[7],
        "sent_at": row[8],
        "classification": row[9],
        "confidence": row[10],
    }


@router.post("/emails/{email_id}/label")
def label_email(email_id: int, payload: LabelIn):
    """Human label: conf=1.0, processed=FALSE, optional training row + history."""
    if payload.label not in ALLOWED_LABELS:
        raise HTTPException(400, f"Unknown label. Use one of {sorted(ALLOWED_LABELS)}")

    with conn() as c:
        row = c.execute(
            """
            SELECT id, direction, body, subject, classification, confidence
            FROM emails WHERE id=%s
            """,
            (email_id,),
        ).fetchone()

        if not row:
            raise HTTPException(404, "Email not found")

        old_cls, old_conf = row[4], row[5]
        task = (
            "APPLICATION"
            if payload.label in {"JOB_APPLICATION", "OTHER"}
            else "REPLY"
        )

        c.execute(
            """
            UPDATE emails
            SET classification = %s,
                confidence = 1.0,
                processed = FALSE,
                review_dismissed = FALSE
            WHERE id = %s
            """,
            (payload.label, email_id),
        )

        added_to_training = False
        if payload.add_to_training:
            if payload.edited_text and payload.edited_text.strip():
                training_text = payload.edited_text.strip()
            else:
                training_text = prepare_ml_text(row[3], row[2])
            c.execute(
                """
                INSERT INTO training_examples(task, text, label)
                VALUES (%s,%s,%s)
                """,
                (task, training_text, payload.label),
            )
            added_to_training = True

        c.execute(
            """
            INSERT INTO review_history(
                email_id, action,
                old_classification, new_classification,
                old_confidence, new_confidence,
                add_to_training, details
            )
            VALUES (%s, 'LABEL', %s, %s, %s, 1.0, %s, %s::jsonb)
            """,
            (
                email_id,
                old_cls,
                payload.label,
                old_conf,
                added_to_training,
                '{"source":"dashboard"}',
            ),
        )

    return {
        "status": "saved_for_training" if added_to_training else "classification_updated",
        "label": payload.label,
        "confidence": 1.0,
        "processed": False,
        "add_to_training": added_to_training,
    }


@router.post("/emails/{email_id}/dismiss")
def dismiss_email(email_id: int):
    """
    Ignore for review queue: does NOT change classification or confidence.
    Email will not reappear in À relabelliser.
    """
    with conn() as c:
        row = c.execute(
            """
            SELECT id, classification, confidence, review_dismissed
            FROM emails WHERE id = %s
            """,
            (email_id,),
        ).fetchone()
        if not row:
            raise HTTPException(404, "Email not found")

        c.execute(
            """
            UPDATE emails SET review_dismissed = TRUE WHERE id = %s
            """,
            (email_id,),
        )
        c.execute(
            """
            INSERT INTO review_history(
                email_id, action,
                old_classification, new_classification,
                old_confidence, new_confidence,
                add_to_training, details
            )
            VALUES (%s, 'DISMISS', %s, %s, %s, %s, FALSE, %s::jsonb)
            """,
            (
                email_id,
                row[1],
                row[1],
                row[2],
                row[2],
                '{"source":"dashboard"}',
            ),
        )
    return {"status": "dismissed", "email_id": email_id}


@router.post("/emails/{email_id}/undismiss")
def undismiss_email(email_id: int):
    """Re-open an ignored email so it appears again in the review queue."""
    with conn() as c:
        row = c.execute(
            """
            SELECT id, classification, confidence
            FROM emails WHERE id = %s
            """,
            (email_id,),
        ).fetchone()
        if not row:
            raise HTTPException(404, "Email not found")

        c.execute(
            "UPDATE emails SET review_dismissed = FALSE WHERE id = %s",
            (email_id,),
        )
        c.execute(
            """
            INSERT INTO review_history(
                email_id, action,
                old_classification, new_classification,
                old_confidence, new_confidence,
                add_to_training, details
            )
            VALUES (%s, 'UNDISMISS', %s, %s, %s, %s, FALSE, %s::jsonb)
            """,
            (email_id, row[1], row[1], row[2], row[2], '{"source":"dashboard"}'),
        )
    return {"status": "undismissed", "email_id": email_id}


@router.post("/emails/batch-dismiss")
def batch_dismiss(payload: BatchIdsIn):

    results = []
    with conn() as c:
        for email_id in payload.ids:
            row = c.execute(
                """
                SELECT id, classification, confidence FROM emails WHERE id = %s
                """,
                (email_id,),
            ).fetchone()
            if not row:
                continue
            c.execute(
                "UPDATE emails SET review_dismissed = TRUE WHERE id = %s",
                (email_id,),
            )
            c.execute(
                """
                INSERT INTO review_history(
                    email_id, action,
                    old_classification, new_classification,
                    old_confidence, new_confidence,
                    add_to_training, details
                )
                VALUES (%s, 'DISMISS', %s, %s, %s, %s, FALSE, %s::jsonb)
                """,
                (
                    email_id,
                    row[1],
                    row[1],
                    row[2],
                    row[2],
                    '{"source":"dashboard","batch":true}',
                ),
            )
            results.append(email_id)
    return {"status": "dismissed", "ids": results, "count": len(results)}


@router.get("/review-history")
def review_history(limit: int = Query(100, ge=1, le=500)):
    with conn() as c:
        rows = c.execute(
            """
            SELECT h.id, h.email_id, h.action,
                   h.old_classification, h.new_classification,
                   h.old_confidence, h.new_confidence,
                   h.add_to_training, h.details, h.created_at,
                   e.subject, e.sender, e.recipient, e.direction
            FROM review_history h
            JOIN emails e ON e.id = h.email_id
            ORDER BY h.created_at DESC
            LIMIT %s
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "id": r[0],
            "email_id": r[1],
            "action": r[2],
            "old_classification": r[3],
            "new_classification": r[4],
            "old_confidence": r[5],
            "new_confidence": r[6],
            "add_to_training": r[7],
            "details": r[8],
            "created_at": r[9],
            "subject": r[10],
            "sender": r[11],
            "recipient": r[12],
            "direction": r[13],
        }
        for r in rows
    ]
