from __future__ import annotations

from fastapi import APIRouter

from app.db import conn

router = APIRouter(tags=["stats"])


@router.get("/stats")
def stats():
    with conn() as c:
        applications = c.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        emails = c.execute("SELECT COUNT(*) FROM emails").fetchone()[0]
        pending = c.execute(
            "SELECT COUNT(*) FROM emails WHERE processed=FALSE"
        ).fetchone()[0]
        needs_review = c.execute(
            """
            SELECT COUNT(*) FROM emails
            WHERE processed = TRUE AND confidence IS NOT NULL AND confidence < 0.70
            """
        ).fetchone()[0]
        statuses = c.execute(
            "SELECT status, COUNT(*) FROM applications GROUP BY status"
        ).fetchall()

    return {
        "emails": emails,
        "applications": applications,
        "unprocessed_emails": pending,
        "needs_review_emails": needs_review,
        "statuses": dict(statuses),
    }


@router.get("/health")
def health():
    with conn() as c:
        c.execute("SELECT 1")
    return {"status": "ok"}
