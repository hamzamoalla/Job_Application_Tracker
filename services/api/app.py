import os
from datetime import datetime
import psycopg
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from text_cleaning import prepare_ml_text, clean_for_storage

DB = os.environ["DATABASE_URL"]
app = FastAPI(title="Job Application Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def conn():
    return psycopg.connect(DB)


class EmailIn(BaseModel):
    gmail_id: str
    thread_id: str
    direction: str
    sender: str | None = None
    recipient: str | None = None
    subject: str | None = None
    body: str | None = None
    sent_at: datetime | None = None


class LabelIn(BaseModel):
    label: str


@app.get("/health")
def health():
    with conn() as c:
        c.execute("SELECT 1")
    return {"status": "ok"}


@app.post("/emails")
def insert_email(email: EmailIn):
    subject, body = clean_for_storage(email.subject, email.body)

    with conn() as c:
        row = c.execute("""
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
        """, (
            email.gmail_id, email.thread_id, email.direction,
            email.sender, email.recipient, subject, body, email.sent_at
        )).fetchone()
    return {"id": row[0], "gmail_id": row[1]}


@app.get("/emails")
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
        rows = c.execute(f"""
            SELECT id, gmail_id, thread_id, direction, sender, recipient,
                   subject, classification, confidence, sent_at
            FROM emails
            WHERE {where_sql}
            ORDER BY confidence ASC NULLS FIRST, sent_at DESC NULLS LAST
            LIMIT %s
        """, params).fetchall()

    return [
        {
            "id": r[0], "gmail_id": r[1], "thread_id": r[2], "direction": r[3],
            "sender": r[4], "recipient": r[5], "subject": r[6],
            "classification": r[7], "confidence": r[8], "sent_at": r[9],
        }
        for r in rows
    ]


@app.get("/emails/{email_id}")
def get_email(email_id: int):
    with conn() as c:
        row = c.execute("""
            SELECT id, gmail_id, thread_id, direction, sender, recipient,
                   subject, body, sent_at, classification, confidence
            FROM emails WHERE id = %s
        """, (email_id,)).fetchone()

    if not row:
        raise HTTPException(404, "Email not found")

    return {
        "id": row[0], "gmail_id": row[1], "thread_id": row[2], "direction": row[3],
        "sender": row[4], "recipient": row[5], "subject": row[6], "body": row[7],
        "sent_at": row[8], "classification": row[9], "confidence": row[10],
    }


@app.get("/applications")
def applications():
    """
    Retourne la liste des candidatures avec la date exacte du DERNIER email reçu/envoyé.
    """
    with conn() as c:
        rows = c.execute("""
            SELECT
                a.id, a.company, a.position, a.application_date, a.status,
                a.confidence, a.thread_id, a.updated_at, a.source,
                COALESCE(
                    (
                        SELECT MAX(e.sent_at)
                        FROM application_emails ae
                        JOIN emails e ON e.id = ae.email_id
                        WHERE ae.application_id = a.id
                    ),
                    (
                        SELECT MAX(e.sent_at)
                        FROM emails e
                        WHERE e.id = a.last_email_id
                           OR e.id = a.sent_email_id
                           OR (a.thread_id IS NOT NULL AND e.thread_id = a.thread_id)
                    ),
                    a.updated_at,
                    a.application_date
                ) AS last_email_date
            FROM applications a
            ORDER BY last_email_date DESC NULLS LAST
        """).fetchall()

    return [
        {
            "id": r[0], "company": r[1], "position": r[2],
            "application_date": r[3], "status": r[4],
            "confidence": r[5], "thread_id": r[6],
            "updated_at": r[7], "source": r[8],
            "last_email_date": r[9],
        }
        for r in rows
    ]


@app.get("/applications/{application_id}")
def application(application_id: int):
    """
    Retourne une candidature + ses emails rattachés,
    ordonnés du PLUS RÉCENT (en haut) au PLUS ANCIEN (en bas).
    """
    with conn() as c:
        row = c.execute("""
            SELECT id, company, position, application_date, status,
                   confidence, thread_id, sent_email_id, last_email_id, source
            FROM applications
            WHERE id = %s
        """, (application_id,)).fetchone()

        if not row:
            raise HTTPException(404, "Application not found")

        app_id = row[0]
        thread_id = row[6]
        sent_email_id = row[7]
        last_email_id = row[8]

        # 1) Emails rattachés (triés par sent_at DESC pour avoir le plus récent en premier)
        emails = c.execute("""
            SELECT
                e.id, e.gmail_id, e.direction, e.sender, e.recipient,
                e.subject, e.body, e.sent_at, e.classification, e.confidence,
                ae.role
            FROM application_emails ae
            JOIN emails e ON e.id = ae.email_id
            WHERE ae.application_id = %s
            ORDER BY e.sent_at DESC NULLS LAST, e.id DESC
        """, (app_id,)).fetchall()

        # 2) Fallback pour les anciennes candidatures (triés aussi par sent_at DESC)
        if not emails:
            emails = c.execute("""
                SELECT
                    e.id, e.gmail_id, e.direction, e.sender, e.recipient,
                    e.subject, e.body, e.sent_at, e.classification, e.confidence,
                    NULL AS role
                FROM emails e
                WHERE
                    e.id = %s
                    OR e.id = %s
                    OR e.thread_id = %s
                    OR (
                        %s LIKE 'external:%%'
                        AND e.gmail_id = REPLACE(%s, 'external:', '')
                    )
                ORDER BY e.sent_at DESC NULLS LAST, e.id DESC
            """, (
                sent_email_id,
                last_email_id,
                thread_id,
                thread_id,
                thread_id,
            )).fetchall()

    return {
        "id": row[0],
        "company": row[1],
        "position": row[2],
        "application_date": row[3],
        "status": row[4],
        "confidence": row[5],
        "thread_id": row[6],
        "source": row[9],
        "emails": [
            {
                "id": e[0],
                "gmail_id": e[1],
                "direction": e[2],
                "sender": e[3],
                "recipient": e[4],
                "subject": e[5],
                "body": e[6],
                "sent_at": e[7],
                "classification": e[8],
                "confidence": e[9],
                "role": e[10],
            }
            for e in emails
        ],
    }


@app.post("/emails/{email_id}/label")
def label_email(email_id: int, payload: LabelIn):
    allowed = {"JOB_APPLICATION", "OTHER", "REJECTION", "INTERVIEW", "IN_REVIEW"}
    if payload.label not in allowed:
        raise HTTPException(400, f"Unknown label. Use one of {sorted(allowed)}")

    with conn() as c:
        row = c.execute("""
            SELECT id, direction, body, subject FROM emails WHERE id=%s
        """, (email_id,)).fetchone()

        if not row:
            raise HTTPException(404, "Email not found")

        task = "APPLICATION" if payload.label in {"JOB_APPLICATION", "OTHER"} else "REPLY"

        c.execute("""
            UPDATE emails SET classification=%s, confidence=1.0
            WHERE id=%s
        """, (payload.label, email_id))

        training_text = prepare_ml_text(row[3], row[2])

        c.execute("""
            INSERT INTO training_examples(task, text, label)
            VALUES (%s,%s,%s)
        """, (task, training_text, payload.label))

        c.execute("""
            UPDATE emails SET processed = FALSE WHERE id = %s
        """, (email_id,))

    return {"status": "saved_for_training"}


@app.get("/stats")
def stats():
    with conn() as c:
        applications = c.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        emails = c.execute("SELECT COUNT(*) FROM emails").fetchone()[0]
        pending = c.execute("""
            SELECT COUNT(*) FROM emails WHERE processed=FALSE
        """).fetchone()[0]
        needs_review = c.execute("""
            SELECT COUNT(*) FROM emails
            WHERE processed = TRUE AND confidence IS NOT NULL AND confidence < 0.70
        """).fetchone()[0]
        statuses = c.execute("""
            SELECT status, COUNT(*) FROM applications GROUP BY status
        """).fetchall()

    return {
        "emails": emails,
        "applications": applications,
        "unprocessed_emails": pending,
        "needs_review_emails": needs_review,
        "statuses": dict(statuses),
    }