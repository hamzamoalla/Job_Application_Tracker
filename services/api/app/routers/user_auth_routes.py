from __future__ import annotations

import logging
import os
import threading
from datetime import datetime, timezone

import requests
from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.db import conn
from app.user_auth import (
    hash_password,
    new_session_token,
    session_expiry,
    verify_password,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["user-auth"])

MAIL_IMPORTER_URL = os.getenv("MAIL_IMPORTER_URL", "http://mail-importer:8000").rstrip("/")


class LoginIn(BaseModel):
    email: str
    password: str = Field(..., min_length=6)


class ImportTriggerIn(BaseModel):
    max_sent: int = Field(50, ge=0, le=500)
    max_received: int = Field(50, ge=0, le=500)
    # Dashboard re-import: force reclassification of already-stored emails
    force_reprocess: bool = True


class ImportPreviewIn(BaseModel):
    direction: str = Field("RECEIVED", pattern="^(RECEIVED|SENT)$")
    mode: str = Field(..., pattern="^(range|datetime)$")
    start: int | None = Field(None, ge=1, le=500)
    end: int | None = Field(None, ge=1, le=500)
    day: str | None = None
    day_to: str | None = None
    hour: int | None = Field(None, ge=0, le=23)
    minute: int | None = Field(None, ge=0, le=59)


class ImportMessageIn(BaseModel):
    gmail_id: str = Field(..., min_length=1)
    direction: str | None = Field(None, pattern="^(RECEIVED|SENT)$")


class ImportIdsIn(BaseModel):
    direction: str = Field("RECEIVED", pattern="^(RECEIVED|SENT)$")
    gmail_ids: list[str] = Field(..., min_length=1, max_length=500)
    force_reprocess: bool = False


class ImportRangeIn(BaseModel):
    direction: str = Field("RECEIVED", pattern="^(RECEIVED|SENT)$")
    start: int = Field(..., ge=1, le=500)
    end: int = Field(..., ge=1, le=500)
    force_reprocess: bool = False


def _user_public(row) -> dict:
    return {
        "id": row[0],
        "email": row[1],
        "first_name": row[2],
        "last_name": row[3],
        "company": row[4],
    }


def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Not authenticated")
    token = authorization.split(" ", 1)[1].strip()
    with conn() as c:
        row = c.execute(
            """
            SELECT u.id, u.email, u.first_name, u.last_name, u.company, s.expires_at
            FROM app_sessions s
            JOIN app_users u ON u.id = s.user_id
            WHERE s.token = %s
            """,
            (token,),
        ).fetchone()
    if not row:
        raise HTTPException(401, "Invalid session")
    exp = row[5]
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < datetime.now(timezone.utc):
        raise HTTPException(401, "Session expired")
    return _user_public(row)


def _bg_upload_and_import(token_bytes: bytes, max_sent: int, max_received: int) -> None:
    try:
        files = {"token": ("token.json", token_bytes, "application/json")}
        r = requests.post(f"{MAIL_IMPORTER_URL}/auth/upload", files=files, timeout=30)
        r.raise_for_status()
        r2 = requests.post(
            f"{MAIL_IMPORTER_URL}/import",
            json={
                "max_sent": max_sent,
                "max_received": max_received,
                "force_reprocess": False,
            },
            timeout=30,
        )
        logger.info("Background import trigger: %s %s", r2.status_code, r2.text[:300])
    except Exception:
        logger.exception("Background upload/import failed")


@router.get("/auth/bootstrap")
def bootstrap():
    with conn() as c:
        n = c.execute("SELECT COUNT(*) FROM app_users").fetchone()[0]
    return {"users_exist": n > 0, "first_setup": n == 0}


@router.post("/auth/register")
async def register(
    email: str = Form(...),
    password: str = Form(..., min_length=6),
    first_name: str = Form(...),
    last_name: str = Form(...),
    company: str = Form(""),
    max_received: int = Form(50, ge=0, le=500),
    max_sent: int = Form(50, ge=0, le=500),
    token_file: UploadFile | None = File(None),
):
    email_n = email.strip().lower()
    with conn() as c:
        if c.execute("SELECT COUNT(*) FROM app_users").fetchone()[0] > 0:
            raise HTTPException(400, "Un compte existe déjà — utilisez la connexion.")
        if c.execute("SELECT id FROM app_users WHERE email=%s", (email_n,)).fetchone():
            raise HTTPException(400, "Email déjà utilisé")
        pw_hash = hash_password(password)
        row = c.execute(
            """
            INSERT INTO app_users (email, password_hash, first_name, last_name, company)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING id, email, first_name, last_name, company
            """,
            (email_n, pw_hash, first_name.strip(), last_name.strip(), company.strip()),
        ).fetchone()
        session = new_session_token()
        c.execute(
            "INSERT INTO app_sessions (token, user_id, expires_at) VALUES (%s,%s,%s)",
            (session, row[0], session_expiry()),
        )

    import_status = "skipped"
    if token_file is not None and token_file.filename:
        raw = await token_file.read()
        threading.Thread(
            target=_bg_upload_and_import,
            args=(raw, max_sent, max_received),
            daemon=True,
        ).start()
        import_status = "started_background"

    return {
        "status": "registered",
        "session_token": session,
        "user": _user_public(row),
        "import": {"status": import_status},
    }


@router.post("/auth/login")
def login(payload: LoginIn):
    email_n = payload.email.strip().lower()
    with conn() as c:
        row = c.execute(
            """
            SELECT id, email, first_name, last_name, company, password_hash
            FROM app_users WHERE email=%s
            """,
            (email_n,),
        ).fetchone()
        if not row or not verify_password(payload.password, row[5]):
            raise HTTPException(401, "Email ou mot de passe incorrect")
        session = new_session_token()
        c.execute(
            "INSERT INTO app_sessions (token, user_id, expires_at) VALUES (%s,%s,%s)",
            (session, row[0], session_expiry()),
        )
    return {"status": "ok", "session_token": session, "user": _user_public(row[:5])}


@router.get("/auth/me")
def me(user: dict = Depends(get_current_user)):
    return user


@router.post("/auth/logout")
def logout(authorization: str | None = Header(default=None)):
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        with conn() as c:
            c.execute("DELETE FROM app_sessions WHERE token=%s", (token,))
    return {"status": "ok"}


@router.post("/import/run")
def import_run(payload: ImportTriggerIn, user: dict = Depends(get_current_user)):
    """Dashboard-triggered import (requires login)."""
    try:
        r = requests.post(
            f"{MAIL_IMPORTER_URL}/import",
            json={
                "max_sent": payload.max_sent,
                "max_received": payload.max_received,
                "force_reprocess": payload.force_reprocess,
            },
            timeout=30,
        )
        body = r.json() if r.content else {}
        return {"status": "ok", "upstream": body, "http": r.status_code}
    except Exception as exc:
        raise HTTPException(502, f"mail-importer unreachable: {exc}") from exc


@router.post("/import/preview")
def import_preview(payload: ImportPreviewIn, user: dict = Depends(get_current_user)):
    """Proxy: liste Gmail (range ou datetime) pour choix dans le dashboard."""
    body = payload.model_dump(exclude_none=True)
    try:
        r = requests.post(
            f"{MAIL_IMPORTER_URL}/import/preview",
            json=body,
            timeout=120,
        )
        data = r.json() if r.content else {}
        if r.status_code >= 400:
            raise HTTPException(r.status_code, data.get("detail") or data)
        return data
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(502, f"mail-importer unreachable: {exc}") from exc


@router.post("/import/ids")
def import_ids(payload: ImportIdsIn, user: dict = Depends(get_current_user)):
    """Proxy: importe les gmail_id sélectionnés."""
    try:
        r = requests.post(
            f"{MAIL_IMPORTER_URL}/import/ids",
            json=payload.model_dump(),
            timeout=180,
        )
        data = r.json() if r.content else {}
        if r.status_code >= 400:
            raise HTTPException(r.status_code, data.get("detail") or data)
        return data
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(502, f"mail-importer unreachable: {exc}") from exc


@router.post("/import/range")
def import_range(payload: ImportRangeIn, user: dict = Depends(get_current_user)):
    """Proxy: import direct par plage d'indices."""
    try:
        r = requests.post(
            f"{MAIL_IMPORTER_URL}/import/range",
            json=payload.model_dump(),
            timeout=30,
        )
        data = r.json() if r.content else {}
        if r.status_code >= 400:
            raise HTTPException(r.status_code, data.get("detail") or data)
        return {"status": "ok", "upstream": data, "http": r.status_code}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(502, f"mail-importer unreachable: {exc}") from exc


@router.post("/import/message")
def import_message(payload: ImportMessageIn, user: dict = Depends(get_current_user)):
    """Proxy: corps complet d'un mail Gmail pour la popup de lecture."""
    try:
        r = requests.post(
            f"{MAIL_IMPORTER_URL}/import/message",
            json=payload.model_dump(exclude_none=True),
            timeout=60,
        )
        data = r.json() if r.content else {}
        if r.status_code >= 400:
            raise HTTPException(r.status_code, data.get("detail") or data)
        return data
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(502, f"mail-importer unreachable: {exc}") from exc