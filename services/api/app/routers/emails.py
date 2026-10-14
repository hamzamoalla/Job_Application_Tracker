from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.config import ALLOWED_LABELS
from app.db import conn
from app.schemas import EmailIn, LabelIn
from app.text_cleaning import clean_for_storage, prepare_ml_text

router = APIRouter(tags=["emails"])


@router.post("/emails")
def insert_email(email: EmailIn):
    subject, body = clean_for_storage(email.subject, email.body)

    with conn() as c:
        row = c.execute(
            """
            INSERT INTO emails
            (gmail_id, thread_id, direction, sender, recipient, subject, body, sent_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (gmail_id) DO UPDATE SET
                thread_id=EXCLUDED.thread_id,
                direction=EXCLUDED.direction,
                sender=EXCLUDED.sender,
                recipient=EXCLUDED.recipient,
                subject=EXCLUDED.subject,
                body=EXCLUDED.body,
                sent_at=EXCLUDED.sent_at
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
    return {"id": row[0], "gmail_id": row[1]}


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
    limit: int = Query(50, ge=1, le=500),
):
    clauses = ["processed = TRUE"]
    params: list = []

    if max_confidence is not None:
        clauses.append("confidence <= %s")
        params.append(max_confidence)

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
    if payload.label not in ALLOWED_LABELS:
        raise HTTPException(400, f"Unknown label. Use one of {sorted(ALLOWED_LABELS)}")

    with conn() as c:
        row = c.execute(
            """
            SELECT id, direction, body, subject FROM emails WHERE id=%s
            """,
            (email_id,),
        ).fetchone()

        if not row:
            raise HTTPException(404, "Email not found")

        task = (
            "APPLICATION"
            if payload.label in {"JOB_APPLICATION", "OTHER"}
            else "REPLY"
        )

        c.execute(
            """
            UPDATE emails SET classification=%s, confidence=1.0
            WHERE id=%s
            """,
            (payload.label, email_id),
        )

        training_text = prepare_ml_text(row[3], row[2])

        c.execute(
            """
            INSERT INTO training_examples(task, text, label)
            VALUES (%s,%s,%s)
            """,
            (task, training_text, payload.label),
        )

        c.execute(
            """
            UPDATE emails SET processed = FALSE WHERE id = %s
            """,
            (email_id,),
        )

    return {"status": "saved_for_training"}
