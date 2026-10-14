from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


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
    label: str = Field(
        ...,
        description="One of: JOB_APPLICATION, OTHER, REJECTION, INTERVIEW, IN_REVIEW",
    )
