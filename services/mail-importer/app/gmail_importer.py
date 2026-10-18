"""Gmail → API importer.

Modes:
  1) First / manual batch: last N SENT + last N RECEIVED (optional force_reprocess).
  2) Continuous poll: only messages NEWER than the stored watermark date
     (no fixed "last 20" window).
"""
from __future__ import annotations

import base64
import json
import logging
import os
import re
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
AUTH_DIR = Path(os.getenv("AUTH_DIR", "/app/auth"))
TOKEN_FILE = AUTH_DIR / "token.json"
STATE_FILE = AUTH_DIR / "sync_state.json"
API_URL = os.getenv("API_URL", "http://api:8000/emails")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))
# Safety cap per poll when fetching by date (not a "window of 20")
POLL_MAX_PER_DIR = int(os.getenv("POLL_MAX_PER_DIR", "500"))

LABEL_BY_DIRECTION = {"SENT": "SENT", "RECEIVED": "INBOX"}


class GmailAuthError(RuntimeError):
    pass


def auth_status() -> dict:
    return {"token_json": TOKEN_FILE.exists()}


def save_uploaded_token(token_bytes: bytes) -> dict:
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_bytes(token_bytes)
    logger.info("token.json saved to %s", TOKEN_FILE)
    return auth_status()


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_state(state: dict) -> None:
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def authenticate_gmail():
    if not TOKEN_FILE.exists():
        raise GmailAuthError("token.json missing — upload it first")
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        logger.info("token.json refreshed")
    if not creds or not creds.valid:
        raise GmailAuthError("token.json invalid — regenerate via OAuth on a browser host")
    return build("gmail", "v1", credentials=creds)


def get_header(headers, name):
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def decode_body(data):
    if not data:
        return ""
    try:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
    except (ValueError, TypeError):
        return ""


class HTMLTextExtractor(HTMLParser):
    BLOCK_TAGS = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text_parts = []
        self.hidden_tags = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden_tags.append(tag)
            return
        if not self.hidden_tags and tag in self.BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            for i in range(len(self.hidden_tags) - 1, -1, -1):
                if self.hidden_tags[i] == tag:
                    del self.hidden_tags[i]
                    break
            return
        if not self.hidden_tags and tag in self.BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_data(self, data):
        if not self.hidden_tags:
            self.text_parts.append(data)


def html_to_text(html):
    p = HTMLTextExtractor()
    p.feed(html)
    p.close()
    return "\n".join(l.strip() for l in "".join(p.text_parts).splitlines() if l.strip())


def clean_body_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(
        r"[\u0000-\u0008\u000B\u000C\u000E-\u001F\u200b-\u200f\u202a-\u202e"
        r"\u2060-\u2064\u2066-\u206f\ufeff\u00ad\u034f\u061c\u180e\u2000-\u200a]",
        "",
        text,
    )
    text = re.sub(r"\bNone\s*\[\d+\]", "", text)
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    lines = text.splitlines()
    while lines:
        last = lines[-1].strip()
        if not last:
            lines.pop()
            continue
        if re.match(r"^(mailto:|https?://|www\.)\S+$", last, re.I):
            lines.pop()
        else:
            break
    return "\n".join(lines).strip()


def collect_mime_bodies(part, plain_parts, html_parts):
    if part.get("filename"):
        return
    mime = part.get("mimeType", "").lower()
    data = part.get("body", {}).get("data")
    if data:
        decoded = decode_body(data)
        if mime == "text/plain":
            plain_parts.append(decoded)
        elif mime == "text/html":
            html_parts.append(decoded)
    for child in part.get("parts", []):
        collect_mime_bodies(child, plain_parts, html_parts)


def extract_body(payload):
    plain, html = [], []
    collect_mime_bodies(payload, plain, html)
    plain_text = "\n".join(p.strip() for p in plain if p.strip())
    if plain_text:
        return clean_body_text(plain_text)
    html_text = "\n".join(h for h in html if h.strip())
    if html_text:
        return clean_body_text(html_to_text(html_text))
    return ""


def parse_date(date_string):
    if not date_string:
        return None
    try:
        return parsedate_to_datetime(date_string).isoformat()
    except (TypeError, ValueError, OverflowError):
        return None


def convert_message(service, message, forced_direction: str | None = None):
    mid = message["id"] if isinstance(message, dict) else message
    try:
        full = service.users().messages().get(
            userId="me", id=mid, format="full"
        ).execute()
    except HttpError as exc:
        if getattr(exc, "resp", None) is not None and exc.resp.status == 404:
            logger.info("Skip deleted/missing Gmail message %s", mid)
            return None
        raise

    labels = set(full.get("labelIds") or [])
    if "TRASH" in labels or "SPAM" in labels:
        logger.info("Skip TRASH/SPAM message %s", mid)
        return None

    payload = full.get("payload", {})
    headers = payload.get("headers", [])
    direction = forced_direction or ("SENT" if "SENT" in labels else "RECEIVED")
    internal_ms = int(full.get("internalDate") or 0)

    return {
        "gmail_id": full["id"],
        "thread_id": full["threadId"],
        "direction": direction,
        "sender": get_header(headers, "From"),
        "recipient": get_header(headers, "To"),
        "subject": get_header(headers, "Subject"),
        "body": extract_body(payload),
        "sent_at": parse_date(get_header(headers, "Date")),
        "_internal_ms": internal_ms,
    }


def list_messages_by_label(service, label_id: str, max_results: int):
    """Last N messages for a label (signup / dashboard batch)."""
    if max_results <= 0:
        return []
    out, token = [], None
    while len(out) < max_results:
        remaining = max_results - len(out)
        params = {
            "userId": "me",
            "labelIds": [label_id],
            "maxResults": min(remaining, 100),
        }
        if token:
            params["pageToken"] = token
        resp = service.users().messages().list(**params).execute()
        out.extend(resp.get("messages") or [])
        token = resp.get("nextPageToken")
        if not token:
            break
    return out[:max_results]


def list_messages_after_ms(
    service,
    label_id: str,
    after_ms: int,
    max_results: int = POLL_MAX_PER_DIR,
):
    """
    Messages with internalDate > after_ms for a label.

    Gmail `q=after:YYYY/MM/DD` is day-granular; we still filter precisely
    with internalDate client-side.
    """
    if max_results <= 0:
        return []

    # after: uses calendar date in the mailbox timezone; use UTC day of watermark
    if after_ms > 0:
        dt = datetime.fromtimestamp(after_ms / 1000.0, tz=timezone.utc)
        # include the same day, filter more precisely below
        q_date = dt.strftime("%Y/%m/%d")
        query = f"after:{q_date}"
    else:
        query = ""

    out, token = [], None
    while len(out) < max_results:
        remaining = max_results - len(out)
        params = {
            "userId": "me",
            "labelIds": [label_id],
            "maxResults": min(remaining, 100),
        }
        if query:
            params["q"] = query
        if token:
            params["pageToken"] = token
        resp = service.users().messages().list(**params).execute()
        batch = resp.get("messages") or []
        if not batch:
            break
        out.extend(batch)
        token = resp.get("nextPageToken")
        if not token:
            break
    return out[:max_results]


def send_email_to_api(email: dict, force_reprocess: bool = False) -> dict | None:
    payload = {k: v for k, v in email.items() if not k.startswith("_")}
    try:
        params = {"force_reprocess": "true"} if force_reprocess else {}
        r = requests.post(API_URL, json=payload, params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json() if r.content else {"ok": True}
    except requests.RequestException as exc:
        logger.warning("Failed to send email %s to API: %s", email.get("gmail_id"), exc)
        return None


def _process_message_list(
    service,
    messages: list,
    direction: str,
    force_reprocess: bool,
    min_internal_ms: int = 0,
) -> tuple[dict, int]:
    """Returns (counters, max_internal_ms_seen)."""
    created = exists = reprocessed = failed = skipped = 0
    max_ms = min_internal_ms

    for msg in messages:
        try:
            email = convert_message(service, msg, forced_direction=direction)
            if email is None:
                skipped += 1
                continue
            internal_ms = int(email.get("_internal_ms") or 0)
            # Strict: only strictly newer than watermark on date-based sync
            if min_internal_ms and internal_ms and internal_ms <= min_internal_ms:
                skipped += 1
                continue
            result = send_email_to_api(email, force_reprocess=force_reprocess)
            if result is None:
                failed += 1
                continue
            status = result.get("status", "")
            if status == "created":
                created += 1
            elif status == "exists":
                exists += 1
            elif status == "reprocessed":
                reprocessed += 1
            else:
                created += 1
            if internal_ms > max_ms:
                max_ms = internal_ms
        except Exception:
            logger.exception("Error on message %s", msg.get("id"))
            failed += 1

    return {
        "created": created,
        "exists_unchanged": exists,
        "reprocessed": reprocessed,
        "failed": failed,
        "skipped": skipped,
    }, max_ms


def run_import(
    max_sent: int,
    max_received: int,
    *,
    force_reprocess: bool = False,
    update_watermark: bool = True,
) -> dict:
    """
    Batch import: last N per direction (signup / dashboard).
    Updates date watermark so the continuous poll only fetches newer mail.
    """
    service = authenticate_gmail()
    state = _load_state()
    totals = {
        "created": 0,
        "exists_unchanged": 0,
        "reprocessed": 0,
        "failed": 0,
        "skipped": 0,
    }
    max_ms = int(state.get("last_internal_ms") or 0)

    for direction, max_n in (("RECEIVED", max_received), ("SENT", max_sent)):
        label = LABEL_BY_DIRECTION[direction]
        messages = list_messages_by_label(service, label, max_n)
        logger.info("Batch %s: %s messages (last N)", direction, len(messages))
        counters, dir_max = _process_message_list(
            service, messages, direction, force_reprocess, min_internal_ms=0
        )
        for k, v in counters.items():
            totals[k] = totals.get(k, 0) + v
        if dir_max > max_ms:
            max_ms = dir_max

    # Recompute watermark: max internalDate among all processed this run
    # (process_message_list already returned max_ms progressive — but we passed min 0
    #  so max_ms is max seen). Update if higher.
    if update_watermark and max_ms > int(state.get("last_internal_ms") or 0):
        state["last_internal_ms"] = max_ms
        state["last_internal_iso"] = datetime.fromtimestamp(
            max_ms / 1000.0, tz=timezone.utc
        ).isoformat()
        state["last_import_at"] = time.time()
        _save_state(state)
        logger.info(
            "Watermark updated → %s (%s)",
            state["last_internal_iso"],
            max_ms,
        )

    totals.update(
        {
            "mode": "batch_last_n",
            "force_reprocess": force_reprocess,
            "max_sent": max_sent,
            "max_received": max_received,
            "watermark_ms": state.get("last_internal_ms"),
            "watermark_iso": state.get("last_internal_iso"),
        }
    )
    logger.info("Batch summary: %s", totals)
    return totals


def run_import_since_watermark() -> dict:
    """
    Continuous mode: only Gmail messages with internalDate > last watermark.
    No fixed '20 mail' window — date-based query + precise filter.
    """
    service = authenticate_gmail()
    state = _load_state()
    after_ms = int(state.get("last_internal_ms") or 0)

    if after_ms <= 0:
        logger.info(
            "No watermark yet — skip date poll (run a batch import / signup first)"
        )
        return {"status": "no_watermark", "created": 0}

    logger.info(
        "Date poll since %s (%s)",
        state.get("last_internal_iso"),
        after_ms,
    )

    totals = {
        "created": 0,
        "exists_unchanged": 0,
        "reprocessed": 0,
        "failed": 0,
        "skipped": 0,
    }
    new_max = after_ms

    for direction, label in LABEL_BY_DIRECTION.items():
        # RECEIVED / SENT
        messages = list_messages_after_ms(
            service, label, after_ms, max_results=POLL_MAX_PER_DIR
        )
        logger.info(
            "Date poll %s: %s candidates after watermark", direction, len(messages)
        )
        counters, dir_max = _process_message_list(
            service,
            messages,
            direction,
            force_reprocess=False,
            min_internal_ms=after_ms,
        )
        for k, v in counters.items():
            totals[k] = totals.get(k, 0) + v
        if dir_max > new_max:
            new_max = dir_max

    if new_max > after_ms:
        state["last_internal_ms"] = new_max
        state["last_internal_iso"] = datetime.fromtimestamp(
            new_max / 1000.0, tz=timezone.utc
        ).isoformat()
        state["last_import_at"] = time.time()
        _save_state(state)
        logger.info("Watermark advanced → %s", state["last_internal_iso"])

    totals.update(
        {
            "mode": "since_date",
            "since_ms": after_ms,
            "since_iso": state.get("last_internal_iso"),
            "watermark_ms": state.get("last_internal_ms"),
        }
    )
    logger.info("Date poll summary: %s", totals)
    return totals


def continuous_poll_loop():
    logger.info(
        "Continuous poll by DATE every %ss (cap %s/dir) — not last-20 window",
        POLL_INTERVAL,
        POLL_MAX_PER_DIR,
    )
    while True:
        time.sleep(POLL_INTERVAL)
        if not TOKEN_FILE.exists():
            continue
        try:
            result = run_import_since_watermark()
            logger.info("Poll result: %s", result)
        except GmailAuthError as exc:
            logger.warning("Poll auth: %s", exc)
        except Exception:
            logger.exception("Poll failed")
