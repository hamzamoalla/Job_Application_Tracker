"""
Adapter between your existing Gmail reader (steps 1-2) and this application.

Your existing reader should call:
    import_email(email)

Expected dictionary:
{
    "id": Gmail message id,
    "thread_id": Gmail thread id,
    "from": "...",
    "to": "...",
    "subject": "...",
    "body": "...",
    "date": "...",
    "direction": "SENT" or "RECEIVED"
}

Run this script only as an example; integrate import_email()
into your existing Gmail polling code.
"""
import os
from datetime import datetime
import psycopg

DB = os.getenv(
    "DATABASE_URL",
    "postgresql://jobtracker:jobtracker@localhost:5432/jobtracker"
)


def import_email(email):
    with psycopg.connect(DB) as c:
        c.execute("""
            INSERT INTO emails
            (gmail_id, thread_id, direction, sender, recipient,
             subject, body, sent_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (gmail_id) DO NOTHING
        """, (
            email["id"],
            email["thread_id"],
            email["direction"],
            email.get("from"),
            email.get("to"),
            email.get("subject"),
            email.get("body"),
            parse_date(email.get("date"))
        ))


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        # If your Gmail reader returns RFC-2822 dates, parse them
        # before calling import_email().
        return None
