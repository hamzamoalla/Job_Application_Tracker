"""Simple shared-secret Bearer auth for API + dashboard."""
from __future__ import annotations
import os
from fastapi import Header, HTTPException

APP_TOKEN = os.getenv("APP_TOKEN", "").strip()


def require_auth(authorization: str | None = Header(default=None)) -> None:
    if not APP_TOKEN:
        return
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if token != APP_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
