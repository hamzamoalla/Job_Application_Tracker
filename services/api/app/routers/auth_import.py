from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.auth import APP_TOKEN, require_auth

router = APIRouter(tags=["auth-import"])

SECRETS_DIR = Path(os.getenv("GMAIL_SECRETS_DIR", "/secrets"))
SECRETS_DIR.mkdir(parents=True, exist_ok=True)


class LoginIn(BaseModel):
    token: str = Field(..., min_length=1)


@router.post("/auth/login")
def login(payload: LoginIn):
    if not APP_TOKEN:
        return {"status": "ok", "auth_required": False}
    if payload.token.strip() != APP_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"status": "ok", "auth_required": True}


@router.get("/auth/status")
def auth_status():
    return {
        "auth_required": bool(APP_TOKEN),
        "credentials_present": (SECRETS_DIR / "credentials.json").exists(),
        "token_present": (SECRETS_DIR / "token.json").exists(),
    }


@router.post("/import/secrets", dependencies=[Depends(require_auth)])
async def upload_secrets(
    credentials: UploadFile | None = File(None),
    token: UploadFile | None = File(None),
):
    saved = []
    if credentials is not None and credentials.filename:
        dest = SECRETS_DIR / "credentials.json"
        with dest.open("wb") as f:
            shutil.copyfileobj(credentials.file, f)
        saved.append("credentials.json")
    if token is not None and token.filename:
        dest = SECRETS_DIR / "token.json"
        with dest.open("wb") as f:
            shutil.copyfileobj(token.file, f)
        saved.append("token.json")
    if not saved:
        raise HTTPException(400, "Provide credentials and/or token file")
    return {"status": "saved", "files": saved}


@router.post("/import/run", dependencies=[Depends(require_auth)])
def run_import(
    max_received: int = Form(50, ge=0, le=500),
    max_sent: int = Form(50, ge=0, le=500),
):
    if not (SECRETS_DIR / "token.json").exists():
        raise HTTPException(400, "token.json missing — upload it first")
    if not (SECRETS_DIR / "credentials.json").exists():
        raise HTTPException(400, "credentials.json missing")

    request_file = SECRETS_DIR / "last_import_request.env"
    request_file.write_text(
        f"MAX_RECEIVED={max_received}\nMAX_SENT={max_sent}\n", encoding="utf-8"
    )

    cmd = os.getenv("MAIL_IMPORTER_CMD", "").strip()
    if not cmd:
        return {
            "status": "queued",
            "message": (
                "Counts saved. Run: docker compose --profile import run --rm "
                f"-e MAX_RECEIVED={max_received} -e MAX_SENT={max_sent} mail-importer"
            ),
            "max_received": max_received,
            "max_sent": max_sent,
        }

    env = os.environ.copy()
    env["MAX_RECEIVED"] = str(max_received)
    env["MAX_SENT"] = str(max_sent)
    env["CREDENTIALS_FILE"] = str(SECRETS_DIR / "credentials.json")
    env["TOKEN_FILE"] = str(SECRETS_DIR / "token.json")
    try:
        proc = subprocess.run(
            cmd, shell=True, env=env, capture_output=True, text=True,
            timeout=int(os.getenv("MAIL_IMPORTER_TIMEOUT", "3600")), check=False,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "Importer timed out")
    return {
        "status": "finished" if proc.returncode == 0 else "failed",
        "returncode": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-2000:],
        "stderr_tail": (proc.stderr or "")[-2000:],
        "max_received": max_received,
        "max_sent": max_sent,
    }
