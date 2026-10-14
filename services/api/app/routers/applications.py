from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import conn

router = APIRouter(tags=["applications"])


@router.get("/applications")
def applications():
    """Liste des candidatures avec la date du dernier email."""
    with conn() as c:
        rows = c.execute(
            """
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
            """
        ).fetchall()

    return [
        {
            "id": r[0],
            "company": r[1],
            "position": r[2],
            "application_date": r[3],
            "status": r[4],
            "confidence": r[5],
            "thread_id": r[6],
            "updated_at": r[7],
            "source": r[8],
            "last_email_date": r[9],
        }
        for r in rows
    ]


@router.get("/applications/{application_id}")
def application(application_id: int):
    """Candidature + emails rattachés (plus récent en premier)."""
    with conn() as c:
        row = c.execute(
            """
            SELECT id, company, position, application_date, status,
                   confidence, thread_id, sent_email_id, last_email_id, source
            FROM applications
            WHERE id = %s
            """,
            (application_id,),
        ).fetchone()

        if not row:
            raise HTTPException(404, "Application not found")

        app_id = row[0]
        thread_id = row[6]
        sent_email_id = row[7]
        last_email_id = row[8]

        emails = c.execute(
            """
            SELECT
                e.id, e.gmail_id, e.direction, e.sender, e.recipient,
                e.subject, e.body, e.sent_at, e.classification, e.confidence,
                ae.role
            FROM application_emails ae
            JOIN emails e ON e.id = ae.email_id
            WHERE ae.application_id = %s
            ORDER BY e.sent_at DESC NULLS LAST, e.id DESC
            """,
            (app_id,),
        ).fetchall()

        if not emails:
            emails = c.execute(
                """
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
                """,
                (
                    sent_email_id,
                    last_email_id,
                    thread_id,
                    thread_id,
                    thread_id,
                ),
            ).fetchall()

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
