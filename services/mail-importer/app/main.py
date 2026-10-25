"""mail-importer FastAPI + continuous background poll (no reprocess loop)."""
from __future__ import annotations

import logging
import threading

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, model_validator

from app.gmail_importer import (
    GmailAuthError,
    auth_status,
    continuous_poll_loop,
    get_message_detail,
    preview_candidates,
    run_import,
    run_import_ids,
    run_import_range,
    save_uploaded_token,
)

logging.basicConfig(level="INFO", format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Mail Importer")


class ImportRequest(BaseModel):
    max_sent: int = Field(50, ge=0, le=500)
    max_received: int = Field(50, ge=0, le=500)
    force_reprocess: bool = False


class PreviewRequest(BaseModel):
    direction: str = Field("RECEIVED", pattern="^(RECEIVED|SENT)$")
    mode: str = Field(..., pattern="^(range|datetime)$")
    start: int | None = Field(None, ge=1, le=500)
    end: int | None = Field(None, ge=1, le=500)
    day: str | None = None          # début de plage (YYYY-MM-DD)
    day_to: str | None = None       # fin de plage inclusive (défaut = day)
    hour: int | None = Field(None, ge=0, le=23)
    minute: int | None = Field(None, ge=0, le=59)

    @model_validator(mode="after")
    def _check(self):
        if self.mode == "range":
            if self.start is None or self.end is None:
                raise ValueError("start and end are required for mode=range")
            if self.end < self.start:
                raise ValueError("end must be >= start")
        if self.mode == "datetime":
            if not self.day:
                raise ValueError("day (YYYY-MM-DD) is required for mode=datetime")
            if self.day_to and self.day_to < self.day:
                raise ValueError("day_to must be >= day")
            if self.minute is not None and self.hour is None:
                raise ValueError("hour is required when minute is set")
        return self


class MessageDetailRequest(BaseModel):
    gmail_id: str = Field(..., min_length=1)
    direction: str | None = Field(None, pattern="^(RECEIVED|SENT)$")


class ImportIdsRequest(BaseModel):
    direction: str = Field("RECEIVED", pattern="^(RECEIVED|SENT)$")
    gmail_ids: list[str] = Field(..., min_length=1, max_length=500)
    force_reprocess: bool = False


class ImportRangeRequest(BaseModel):
    direction: str = Field("RECEIVED", pattern="^(RECEIVED|SENT)$")
    start: int = Field(..., ge=1, le=500)
    end: int = Field(..., ge=1, le=500)
    force_reprocess: bool = False

    @model_validator(mode="after")
    def _check(self):
        if self.end < self.start:
            raise ValueError("end must be >= start")
        return self


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


@app.post("/import/preview")
def import_preview(payload: PreviewRequest):
    if not auth_status()["token_json"]:
        raise HTTPException(400, "token.json missing")
    try:
        rows = preview_candidates(
            payload.direction,
            mode=payload.mode,
            start=payload.start,
            end=payload.end,
            day=payload.day,
            day_to=payload.day_to,
            hour=payload.hour,
            minute=payload.minute,
        )
    except GmailAuthError as exc:
        raise HTTPException(401, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        logger.exception("preview failed")
        raise HTTPException(500, f"preview failed: {exc}") from exc
    return {
        "count": len(rows),
        "direction": payload.direction,
        "mode": payload.mode,
        "messages": rows,
    }




@app.post("/import/message")
def import_message_detail(payload: MessageDetailRequest):
    """Corps complet d'un mail Gmail (prévisualisation UI)."""
    if not auth_status()["token_json"]:
        raise HTTPException(400, "token.json missing")
    try:
        return get_message_detail(payload.gmail_id, direction=payload.direction)
    except GmailAuthError as exc:
        raise HTTPException(401, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    except Exception as exc:
        logger.exception("message detail failed")
        raise HTTPException(500, f"message detail failed: {exc}") from exc

@app.post("/import/ids")
def import_by_ids(payload: ImportIdsRequest):
    if not auth_status()["token_json"]:
        raise HTTPException(400, "token.json missing")
    try:
        result = run_import_ids(
            payload.gmail_ids,
            payload.direction,
            force_reprocess=payload.force_reprocess,
        )
    except GmailAuthError as exc:
        raise HTTPException(401, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        logger.exception("import ids failed")
        raise HTTPException(500, f"import failed: {exc}") from exc
    return {"status": "ok", **result}


@app.post("/import/range")
def import_by_range(payload: ImportRangeRequest, background_tasks: BackgroundTasks):
    if not auth_status()["token_json"]:
        raise HTTPException(400, "token.json missing")

    def _job():
        try:
            result = run_import_range(
                payload.direction,
                payload.start,
                payload.end,
                force_reprocess=payload.force_reprocess,
            )
            logger.info("Range import done: %s", result)
        except Exception:
            logger.exception("Range import failed")

    background_tasks.add_task(_job)
    return {
        "status": "started",
        "direction": payload.direction,
        "start": payload.start,
        "end": payload.end,
        "message": "Range import running in background",
    }


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h1>Mail Importer</h1>
    <ul>
      <li>POST /auth/upload</li>
      <li>POST /import — last N sent + received</li>
      <li>POST /import/preview — range | datetime</li>
      <li>POST /import/ids — selected gmail ids</li>
      <li>POST /import/range — index range direct</li>
    </ul>
    """