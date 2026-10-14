from __future__ import annotations

import os

DATABASE_URL = os.environ["DATABASE_URL"]
ALLOWED_LABELS = frozenset(
    {"JOB_APPLICATION", "OTHER", "REJECTION", "INTERVIEW", "IN_REVIEW"}
)
