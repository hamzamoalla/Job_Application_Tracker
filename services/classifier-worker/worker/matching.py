"""Application matching, linking, status updates and consolidation."""

from __future__ import annotations

import logging
import os
from difflib import SequenceMatcher

import psycopg
from psycopg.rows import dict_row

from text_cleaning import normalize
from worker.extraction import email_address

logger = logging.getLogger(__name__)

STALE_IN_REVIEW_DAYS = int(os.getenv("STALE_IN_REVIEW_DAYS", "30"))

ROLE_BY_LABEL = {
    "JOB_APPLICATION": "SENT",
    "IN_REVIEW": "CONFIRMATION",
    "INTERVIEW": "INTERVIEW",
    "REJECTION": "REJECTION",
    "OTHER": "OTHER",
}

STATUS_BY_LABEL = {
    "IN_REVIEW": "IN_REVIEW",
    "REJECTION": "REJECTED",
    "INTERVIEW": "INTERVIEW",
}


def company_similarity(left, right) -> float:
    a, b = normalize(left or ""), normalize(right or "")
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:
        return 0.90
    return SequenceMatcher(None, a, b).ratio()


def position_similarity(left, right) -> float:
    a, b = normalize(left or ""), normalize(right or "")
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:
        return 0.90
    wa, wb = set(a.split()), set(b.split())
    union = wa | wb
    if not union:
        return 0.0
    return len(wa & wb) / len(union)


def link_email(conn, application_id, email_id, role, addresses=None):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO application_emails (application_id, email_id, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (application_id, email_id) DO UPDATE SET role = EXCLUDED.role
            """,
            (application_id, email_id, role),
        )

        if addresses:
            clean = [a for a in (email_address(x) for x in addresses) if a]
            if clean:
                cur.execute(
                    """
                    UPDATE applications
                    SET related_addresses = (
                            SELECT ARRAY(
                                SELECT DISTINCT unnest(
                                    COALESCE(related_addresses, '{}') || %s::text[]
                                )
                            )
                        ),
                        last_email_id = %s,
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (clean, email_id, application_id),
                )
            else:
                cur.execute(
                    """
                    UPDATE applications
                    SET last_email_id = %s, updated_at = NOW()
                    WHERE id = %s
                    """,
                    (email_id, application_id),
                )
        else:
            cur.execute(
                """
                UPDATE applications
                SET last_email_id = %s, updated_at = NOW()
                WHERE id = %s
                """,
                (email_id, application_id),
            )


def insert_processing_event(conn, email_id, event_type, details):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO processing_events (email_id, event_type, details)
            VALUES (%s, %s, %s)
            """,
            (email_id, event_type, psycopg.types.json.Jsonb(details)),
        )


def find_applications_by_company(conn, company, open_only=True):
    if not company:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT id, thread_id, company, position, status, source,
                   sent_email_id, last_email_id, related_addresses
            FROM applications
            WHERE company IS NOT NULL
            ORDER BY updated_at DESC NULLS LAST, id DESC
            """
        )
        rows = cur.fetchall()

    matches = []
    for app in rows:
        if company_similarity(company, app["company"]) < 0.82:
            continue
        if open_only and app["status"] in ("REJECTED",):
            continue
        matches.append(app)
    return matches


def find_matching_application(conn, company, position, address=None):
    candidates = find_applications_by_company(conn, company, open_only=True)
    if not candidates:
        return None

    addr = email_address(address) if address else None

    if addr:
        for app in candidates:
            related = [email_address(x) for x in (app.get("related_addresses") or [])]
            if addr in related:
                return app

    if position:
        scored = []
        for app in candidates:
            if not app["position"]:
                scored.append((app, 0.75))
                continue
            p = position_similarity(position, app["position"])
            if p >= 0.40:
                scored.append((app, 0.60 + 0.40 * p))

        scored.sort(key=lambda x: x[1], reverse=True)
        if scored and scored[0][1] >= 0.70:
            if len(scored) > 1 and scored[0][1] - scored[1][1] < 0.08:
                logger.warning(
                    "Matching ambigu entreprise+poste : %s / %s", company, position
                )
                return None
            return scored[0][0]

    if len(candidates) == 1:
        return candidates[0]
    return None


def consolidate_duplicate_applications(conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT a1.id AS stale_id, a1.company AS company,
                   a2.id AS main_id, a2.status AS main_status,
                   a2.position AS main_position
            FROM applications a1
            JOIN applications a2
              ON LOWER(a1.company) = LOWER(a2.company) AND a1.id != a2.id
            WHERE a1.status = 'IN_REVIEW'
              AND a2.status IN ('REJECTED', 'INTERVIEW')
            """
        )
        duplicates = cur.fetchall()

    for dup in duplicates:
        stale_id = dup["stale_id"]
        main_id = dup["main_id"]
        logger.info(
            "Nettoyage auto DB : fusion #%s (IN_REVIEW) → #%s (%s – %s)",
            stale_id,
            main_id,
            dup["company"],
            dup["main_status"],
        )
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO application_emails (application_id, email_id, role)
                SELECT %s, email_id, role
                FROM application_emails
                WHERE application_id = %s
                ON CONFLICT (application_id, email_id) DO NOTHING
                """,
                (main_id, stale_id),
            )
            cur.execute(
                "DELETE FROM application_emails WHERE application_id = %s", (stale_id,)
            )
            if dup["main_position"] is None:
                cur.execute(
                    """
                    UPDATE applications
                    SET position = (SELECT position FROM applications WHERE id = %s)
                    WHERE id = %s AND position IS NULL
                    """,
                    (stale_id, main_id),
                )
            cur.execute("DELETE FROM applications WHERE id = %s", (stale_id,))


def create_application(
    conn,
    email,
    company,
    position,
    status,
    confidence,
    source,
    role,
    company_src,
    position_src,
):
    thread_id = email.get("thread_id") or f"external:{email['gmail_id']}"
    if source == "WEBSITE_ASSUMED":
        thread_id = f"external:{email['gmail_id']}"

    addresses = [
        email.get("recipient" if email.get("direction") == "SENT" else "sender")
    ]

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            INSERT INTO applications (
                thread_id, company, position, application_date,
                status, confidence, sent_email_id, last_email_id,
                source, related_addresses
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s,
                CASE WHEN %s = 'SENT' THEN %s ELSE NULL END,
                %s, %s, %s
            )
            ON CONFLICT (thread_id) DO UPDATE SET
                company = COALESCE(applications.company, EXCLUDED.company),
                position = COALESCE(applications.position, EXCLUDED.position),
                status = CASE
                    WHEN applications.status IN ('INTERVIEW', 'REJECTED')
                         AND EXCLUDED.status = 'IN_REVIEW'
                    THEN applications.status
                    ELSE EXCLUDED.status
                END,
                last_email_id = EXCLUDED.last_email_id,
                confidence = EXCLUDED.confidence,
                related_addresses = (
                    SELECT ARRAY(
                        SELECT DISTINCT unnest(
                            COALESCE(applications.related_addresses, '{}')
                            || COALESCE(EXCLUDED.related_addresses, '{}')
                        )
                    )
                ),
                updated_at = NOW()
            RETURNING id
            """,
            (
                thread_id,
                company,
                position,
                email.get("sent_at"),
                status,
                confidence,
                role,
                email["id"],
                email["id"],
                source,
                [email_address(a) for a in addresses if a],
            ),
        )
        row = cur.fetchone()
        app_id = row["id"]

    link_email(conn, app_id, email["id"], role, addresses=addresses)
    logger.info(
        "Candidature #%s créée/MAJ : %s / %s → %s (Company=%s, Position=%s)",
        app_id,
        company,
        position or "?",
        status,
        company_src,
        position_src,
    )
    return app_id


def update_application_status(
    conn,
    app,
    email,
    status,
    confidence,
    role,
    company,
    position,
    company_src,
    position_src,
):
    new_status = status
    if app["status"] in ("INTERVIEW", "REJECTED") and status == "IN_REVIEW":
        new_status = app["status"]

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE applications
            SET status = %s,
                company = COALESCE(company, %s),
                position = COALESCE(position, %s),
                confidence = %s,
                last_email_id = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (new_status, company, position, confidence, email["id"], app["id"]),
        )

    addresses = [email.get("sender") or email.get("recipient")]
    link_email(conn, app["id"], email["id"], role, addresses=addresses)

    insert_processing_event(
        conn,
        email["id"],
        "APPLICATION_STATUS_UPDATED",
        {
            "application_id": app["id"],
            "old_status": app["status"],
            "new_status": new_status,
            "company": company,
            "position": position,
            "company_source": company_src,
            "position_source": position_src,
            "confidence": confidence,
        },
    )


def apply_rejection(conn, email, company, position, confidence, company_src, position_src):
    sender = email_address(email.get("sender"))
    existing = find_matching_application(conn, company, position, address=sender)

    if existing:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE applications
                SET status = 'REJECTED',
                    position = COALESCE(position, %s),
                    confidence = %s,
                    last_email_id = %s,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (position, confidence, email["id"], existing["id"]),
            )
        link_email(conn, existing["id"], email["id"], "REJECTION", addresses=[sender])
        logger.info(
            "Candidature #%s → REJECTED (fusion mail de refus) %s / %s",
            existing["id"],
            company,
            position or existing["position"] or "?",
        )
        insert_processing_event(
            conn,
            email["id"],
            "APPLICATION_STATUS_UPDATED",
            {
                "scope": "matched_fusion",
                "application_id": existing["id"],
                "company": company,
                "position": position,
                "company_source": company_src,
                "position_source": position_src,
                "confidence": confidence,
            },
        )
        return [existing["id"]]

    candidates = find_applications_by_company(conn, company, open_only=True)

    if not candidates:
        return [
            create_application(
                conn,
                email,
                company,
                position,
                "REJECTED",
                confidence,
                "WEBSITE_ASSUMED",
                "REJECTION",
                company_src,
                position_src,
            )
        ]

    targeted = []
    for app in candidates:
        related = [email_address(x) for x in (app.get("related_addresses") or [])]
        if sender and sender in related:
            targeted.append(app)

    if targeted:
        to_reject = targeted
        scope = "targeted"
    elif position:
        to_reject = [
            app
            for app in candidates
            if app["position"] and position_similarity(position, app["position"]) >= 0.40
        ]
        if not to_reject:
            to_reject = candidates
            scope = "company_global_fallback"
        else:
            scope = "position"
    else:
        to_reject = candidates
        scope = "company_global"

    rejected_ids = []
    for app in to_reject:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE applications
                SET status = 'REJECTED',
                    position = COALESCE(position, %s),
                    confidence = %s,
                    last_email_id = %s,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (position, confidence, email["id"], app["id"]),
            )
        link_email(conn, app["id"], email["id"], "REJECTION", addresses=[sender])
        rejected_ids.append(app["id"])

    insert_processing_event(
        conn,
        email["id"],
        "APPLICATION_STATUS_UPDATED",
        {
            "scope": scope,
            "rejected_ids": rejected_ids,
            "company": company,
            "position": position,
            "company_source": company_src,
            "position_source": position_src,
            "confidence": confidence,
        },
    )
    return rejected_ids


def expire_stale_applications(conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            UPDATE applications
            SET status = 'REJECTED', updated_at = NOW()
            WHERE status = 'IN_REVIEW'
              AND updated_at < NOW() - make_interval(days => %s)
            RETURNING id, company, position
            """,
            (STALE_IN_REVIEW_DAYS,),
        )
        rows = cur.fetchall()

    for row in rows:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO processing_events (email_id, event_type, details)
                VALUES (NULL, 'APPLICATION_STALE_REJECTED', %s)
                """,
                (
                    psycopg.types.json.Jsonb(
                        {
                            "application_id": row["id"],
                            "company": row["company"],
                            "position": row["position"],
                            "stale_days": STALE_IN_REVIEW_DAYS,
                        }
                    ),
                ),
            )
