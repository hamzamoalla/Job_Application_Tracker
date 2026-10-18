"""mail-importer FastAPI + continuous background poll (no reprocess loop)."""
from __future__ import annotations

import logging
import threading

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.gmail_importer import (
    GmailAuthError,
    auth_status,
    continuous_poll_loop,
    run_import,
    save_uploaded_token,
)

logging.basicConfig(level="INFO", format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Mail Importer")


class ImportRequest(BaseModel):
    max_sent: int = Field(50, ge=0, le=500)
    max_received: int = Field(50, ge=0, le=500)
    # Manual re-import from dashboard can force worker reprocessing
    force_reprocess: bool = False


@app.on_event("startup")
def start_poller():
    t = threading.Thread(target=continuous_poll_loop, name="gmail-poll", daemon=True)
    t.start()
    logger.info("Background Gmail poller started")


@app.get("/health")
def health():
    return {"status": "ok", **auth_status()}


@app.get("/auth/status")
def get_auth_status():
    return auth_status()


@app.post("/auth/upload")
async def upload_auth_files(token: UploadFile = File(...)):
    data = await token.read()
    if not data:
        raise HTTPException(400, "Empty token.json")
    return save_uploaded_token(data)


@app.post("/import")
def trigger_import(payload: ImportRequest, background_tasks: BackgroundTasks):
    if not auth_status()["token_json"]:
        raise HTTPException(400, "token.json missing")

    force = bool(payload.force_reprocess)

    def _job():
        try:
            result = run_import(
                payload.max_sent,
                payload.max_received,
                force_reprocess=force,
            )
            logger.info("Import job done: %s", result)
        except GmailAuthError as exc:
            logger.error("Import auth error: %s", exc)
        except Exception:
            logger.exception("Import job failed")

    background_tasks.add_task(_job)
    return {
        "status": "started",
        "max_sent": payload.max_sent,
        "max_received": payload.max_received,
        "force_reprocess": force,
        "message": "Import running in background",
    }


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!doctype html><html><body style="font-family:system-ui;background:#0b0f17;color:#f1f5f9;padding:2rem">
    <h1>Mail Importer</h1>
    <p>POST /auth/upload + POST /import. Poll every minute without reprocessing unchanged mails.</p>
    </body></html>"""
