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
    add_to_training: bool = Field(
        False,
        description="If true, insert into training_examples.",
    )
    edited_text: str | None = Field(
        None,
        description="Optional cleaned text for training when add_to_training=true.",
    )


class BatchIdsIn(BaseModel):
    ids: list[int] = Field(..., min_length=1, max_length=200)
