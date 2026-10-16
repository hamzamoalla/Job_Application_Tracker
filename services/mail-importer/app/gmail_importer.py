"""Gmail → API importer (token.json only, continuous poll)."""
from __future__ import annotations

import base64
import logging
import os
import re
import time
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
AUTH_DIR = Path(os.getenv("AUTH_DIR", "/app/auth"))
TOKEN_FILE = AUTH_DIR / "token.json"
API_URL = os.getenv("API_URL", "http://api:8000/emails")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))
DEFAULT_MAX_RECEIVED = int(os.getenv("MAX_RECEIVED", "50"))
DEFAULT_MAX_SENT = int(os.getenv("MAX_SENT", "50"))
# After first full import, subsequent polls use smaller windows
POLL_MAX_RECEIVED = int(os.getenv("POLL_MAX_RECEIVED", "20"))
POLL_MAX_SENT = int(os.getenv("POLL_MAX_SENT", "20"))

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
    full = service.users().messages().get(
        userId="me", id=message["id"], format="full"
    ).execute()
    payload = full.get("payload", {})
    headers = payload.get("headers", [])
    direction = forced_direction
    if not direction:
        labels = set(full.get("labelIds") or [])
        direction = "SENT" if "SENT" in labels else "RECEIVED"
    return {
        "gmail_id": full["id"],
        "thread_id": full["threadId"],
        "direction": direction,
        "sender": get_header(headers, "From"),
        "recipient": get_header(headers, "To"),
        "subject": get_header(headers, "Subject"),
        "body": extract_body(payload),
        "sent_at": parse_date(get_header(headers, "Date")),
    }


def list_messages(service, label_id: str, max_results: int):
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


def send_email_to_api(email: dict) -> dict | None:
    try:
        r = requests.post(API_URL, json=email, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json() if r.content else {"ok": True}
    except requests.RequestException as exc:
        logger.warning("Failed to send email %s to API: %s", email.get("gmail_id"), exc)
        return None


def run_import(max_sent: int, max_received: int) -> dict:
    service = authenticate_gmail()
    imported = failed = skipped = 0
    details = []

    for direction, max_n in (("RECEIVED", max_received), ("SENT", max_sent)):
        label = LABEL_BY_DIRECTION[direction]
        messages = list_messages(service, label, max_n)
        logger.info("%s: %s messages to process", direction, len(messages))
        for msg in messages:
            try:
                email = convert_message(service, msg, forced_direction=direction)
                result = send_email_to_api(email)
                if result is None:
                    failed += 1
                else:
                    imported += 1
                    if result.get("reprocessed"):
                        skipped += 1  # counted as reprocessed existing
                    details.append(
                        {
                            "gmail_id": email["gmail_id"],
                            "direction": direction,
                            "status": result.get("status", "ok"),
                        }
                    )
            except Exception:
                logger.exception("Error on message %s", msg.get("id"))
                failed += 1

    return {
        "imported": imported,
        "failed": failed,
        "reprocessed_hint": skipped,
        "max_sent": max_sent,
        "max_received": max_received,
    }


def continuous_poll_loop():
    """Background loop: every POLL_INTERVAL seconds, fetch recent mail."""
    logger.info(
        "Continuous poll started (interval=%ss, poll max R=%s S=%s)",
        POLL_INTERVAL,
        POLL_MAX_RECEIVED,
        POLL_MAX_SENT,
    )
    while True:
        time.sleep(POLL_INTERVAL)
        if not TOKEN_FILE.exists():
            logger.debug("No token yet — skip poll")
            continue
        try:
            result = run_import(POLL_MAX_SENT, POLL_MAX_RECEIVED)
            logger.info("Poll result: %s", result)
        except GmailAuthError as exc:
            logger.warning("Poll auth: %s", exc)
        except Exception:
            logger.exception("Poll failed")
