import os
import re
import base64
import requests

from datetime import datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ============================================================
# CONFIGURATION
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

API_URL = "http://localhost:8000/emails"

MAX_EMAILS = 100
REQUEST_TIMEOUT = 20

MY_EMAIL = None


# ============================================================
# GMAIL AUTHENTICATION
# ============================================================

def authenticate_gmail():
    """Authenticate with the Gmail API."""

    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    elif not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES
        )

        creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "w", encoding="utf-8") as token:
        token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


# ============================================================
# HEADER HELPERS
# ============================================================

def get_header(headers, name):
    """Return a header value, ignoring case."""

    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")

    return ""


# ============================================================
# DECODE GMAIL BODY
# ============================================================

def decode_body(data):
    """Decode Gmail base64url data into UTF-8 text."""

    if not data:
        return ""

    try:
        decoded = base64.urlsafe_b64decode(data)
        return decoded.decode("utf-8", errors="replace")

    except (ValueError, TypeError):
        return ""


# ============================================================
# HTML TO TEXT
# ============================================================

class HTMLTextExtractor(HTMLParser):
    """Convert HTML content into readable text."""

    BLOCK_TAGS = {
        "p", "div", "br", "tr", "li",
        "h1", "h2", "h3", "h4", "blockquote"
    }

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
            for index in range(len(self.hidden_tags) - 1, -1, -1):
                if self.hidden_tags[index] == tag:
                    del self.hidden_tags[index]
                    break
            return

        if not self.hidden_tags and tag in self.BLOCK_TAGS:
            self.text_parts.append("\n")

    def handle_data(self, data):
        if not self.hidden_tags:
            self.text_parts.append(data)


def html_to_text(html):
    """Extract readable text from HTML."""

    parser = HTMLTextExtractor()
    parser.feed(html)
    parser.close()

    lines = [
        line.strip()
        for line in "".join(parser.text_parts).splitlines()
        if line.strip()
    ]

    return "\n".join(lines)


# ============================================================
# NETTOYAGE DU BODY
# ============================================================

def clean_body_text(text: str) -> str:
    """
    Nettoie le texte extrait :
    1. Supprime les caractères invisibles.
    2. Nettoie les artefacts de liens [1].
    3. Supprime les blocs d'URL isolées en bas de page (mailto:, http://).
    4. Supprime le preheader (ex: Much) même s'il a des sauts de ligne différents.
    """
    if not text:
        return ""

    # 1. Caractères invisibles / zero-width
    text = re.sub(
        r"[\u0000-\u0008\u000B\u000C\u000E-\u001F"
        r"\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u206f"
        r"\ufeff\u00ad\u034f\u061c\u180e\u2000-\u200a]",
        "",
        text,
    )

    # 2. Artefacts de liens
    text = re.sub(r"\bNone\s*\[\d+\]", "", text)
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # 3. Supprime les URL brutes isolées à la fin de l'e-mail
    lines = text.splitlines()
    while lines:
        last_line = lines[-1].strip()
        if not last_line:
            lines.pop()
            continue
        if re.match(r"^(mailto:|https?://|http://|www\.)\S+$", last_line, re.IGNORECASE):
            lines.pop()
        else:
            break
    text = "\n".join(lines).strip()

    # 4. Suppression robuste du preheader (gestion des espaces/sauts de ligne)
    parts = re.split(r"\n{2,}", text)
    if len(parts) >= 2:
        p0 = parts[0].strip()
        rest = "\n\n".join(parts[1:]).strip()

        has_ellipsis = bool(re.search(r"(\[\s*\.\.\.\s*\]|\.\.\.|\…)\s*$", p0))
        p0_clean = re.sub(r"(\[\s*\.\.\.\s*\]|\.\.\.|\…|\*)\s*$", "", p0).strip()

        # Normalisation des espaces et sauts de ligne pour comparer p0 et rest
        def norm(s):
            return re.sub(r"\s+", " ", s).strip().lower()

        p0_norm = norm(p0_clean)
        rest_norm = norm(rest)

        if p0_norm and len(p0_norm) < 400:
            if has_ellipsis and rest_norm.startswith(p0_norm[:40]):
                text = rest
            elif rest_norm.startswith(p0_norm):
                text = rest

    return text.strip()


# ============================================================
# EXTRACT BODY FROM MIME PAYLOAD
# ============================================================

def collect_mime_bodies(part, plain_parts, html_parts):
    """
    Recursively collect text/plain and text/html MIME parts.
    Ignore file attachments.
    """

    if part.get("filename"):
        return

    mime_type = part.get("mimeType", "").lower()
    body_data = part.get("body", {}).get("data")

    if body_data:
        decoded = decode_body(body_data)

        if mime_type == "text/plain":
            plain_parts.append(decoded)

        elif mime_type == "text/html":
            html_parts.append(decoded)

    for child in part.get("parts", []):
        collect_mime_bodies(
            child,
            plain_parts,
            html_parts
        )


def extract_body(payload):
    """Extract plain text or HTML and clean it safely."""

    plain_parts = []
    html_parts = []

    collect_mime_bodies(
        payload,
        plain_parts,
        html_parts
    )

    plain_text = "\n".join(
        part.strip()
        for part in plain_parts
        if part.strip()
    )

    if plain_text:
        return clean_body_text(plain_text)

    html_text = "\n".join(
        part
        for part in html_parts
        if part.strip()
    )

    if html_text:
        return clean_body_text(html_to_text(html_text))

    return ""


# ============================================================
# PARSE DATE
# ============================================================

def parse_date(date_string):
    """Convert an RFC 2822 date into an ISO 8601 string."""

    if not date_string:
        return None

    try:
        dt = parsedate_to_datetime(date_string)
        return dt.isoformat()

    except (TypeError, ValueError, OverflowError):
        return None


# ============================================================
# DETERMINE EMAIL DIRECTION
# ============================================================

def determine_direction(sender, label_ids):
    """
    Prefer Gmail's SENT label.
    """

    labels = set(label_ids or [])

    if "SENT" in labels:
        return "SENT"

    sender_lower = (sender or "").lower()

    if MY_EMAIL and MY_EMAIL.lower() in sender_lower:
        return "SENT"

    return "RECEIVED"


# ============================================================
# GET AUTHENTICATED GMAIL ADDRESS
# ============================================================

def get_my_email(service):
    """Retrieve the authenticated Gmail account address."""

    profile = service.users().getProfile(
        userId="me"
    ).execute()

    return profile["emailAddress"]


# ============================================================
# CONVERT GMAIL MESSAGE
# ============================================================

def convert_message(service, message):
    """Convert a Gmail API message into the FastAPI format."""

    message_id = message["id"]

    full_message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = full_message.get("payload", {})
    headers = payload.get("headers", [])

    sender = get_header(headers, "From")
    recipient = get_header(headers, "To")
    subject = get_header(headers, "Subject")
    date_string = get_header(headers, "Date")

    body = extract_body(payload)

    direction = determine_direction(
        sender,
        full_message.get("labelIds", [])
    )

    return {
        "gmail_id": full_message["id"],
        "thread_id": full_message["threadId"],
        "direction": direction,
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "sent_at": parse_date(date_string)
    }


# ============================================================
# GET GMAIL MESSAGES WITH PAGINATION
# ============================================================

def get_messages(service, max_results=100):
    """
    Retrieve up to max_results messages.
    """

    messages = []
    page_token = None

    while len(messages) < max_results:
        remaining = max_results - len(messages)

        params = {
            "userId": "me",
            "maxResults": min(remaining, 500)
        }

        if page_token:
            params["pageToken"] = page_token

        response = service.users().messages().list(
            **params
        ).execute()

        messages.extend(response.get("messages", []))

        page_token = response.get("nextPageToken")

        if not page_token:
            break

    messages = messages[:max_results]

    print(f"Found {len(messages)} Gmail messages.")

    return messages


# ============================================================
# SEND EMAIL TO FASTAPI
# ============================================================

def send_email_to_api(email):
    """Send one email to the FastAPI backend."""

    try:
        response = requests.post(
            API_URL,
            json=email,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        if response.content:
            try:
                return response.json()
            except ValueError:
                return {"success": True, "response": response.text}

        return {"success": True}

    except requests.exceptions.ConnectionError:
        print(
            "\nERROR: Cannot connect to FastAPI. "
            f"Check that the API is running at {API_URL}"
        )

    except requests.exceptions.Timeout:
        print("ERROR: API request timed out.")

    except requests.exceptions.HTTPError as error:
        print(f"ERROR: API returned HTTP error: {error}")

        if error.response is not None:
            print(error.response.text[:1000])

    except requests.exceptions.RequestException as error:
        print(f"ERROR sending email to API: {error}")

    return None


# ============================================================
# MAIN
# ============================================================

def main():
    global MY_EMAIL

    print("=" * 60)
    print("JOB APPLICATION TRACKER - GMAIL IMPORTER")
    print("=" * 60)

    print("\nAuthenticating with Gmail...")

    service = authenticate_gmail()

    print("Gmail authentication successful.")

    MY_EMAIL = get_my_email(service)

    print(f"Gmail account: {MY_EMAIL}")

    messages = get_messages(
        service,
        MAX_EMAILS
    )

    if not messages:
        print("No messages found.")
        return

    imported = 0
    failed = 0

    for index, message in enumerate(messages, start=1):
        print(f"\n[{index}/{len(messages)}]")

        try:
            email = convert_message(
                service,
                message
            )

            print(f"Direction : {email['direction']}")
            print(f"From      : {email['sender']}")
            print(f"Subject   : {email['subject']}")
            print(f"Thread ID : {email['thread_id']}")
            print(f"Body size : {len(email['body'])} characters")
            print(f"Body size : {email['body']}")

            result = send_email_to_api(email)

            if result is not None:
                print("Import request completed.")
                imported += 1
            else:
                print("Import failed.")
                failed += 1

        except Exception as error:
            print(f"ERROR processing message: {error}")
            failed += 1

    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"Import requests completed : {imported}")
    print(f"Failed                    : {failed}")
    print(f"Total                     : {len(messages)}")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()