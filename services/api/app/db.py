from __future__ import annotations

import psycopg

from app.config import DATABASE_URL


def conn():
    return psycopg.connect(DATABASE_URL)
