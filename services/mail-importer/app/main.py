"""
mail-importer: containerized replacement for running mail_reader.py by hand.

Workflow:
  1. Generate token.json once on your own machine (the OAuth consent screen
     needs a browser, which this container doesn't have).
  2. Upload token.json through the page served at "/". credentials.json is
     not needed: google-auth embeds the client_id/client_secret/refresh
     token inside token.json itself when it saves it, so token.json alone
     is enough to authenticate and self-refresh here.
  3. Enter how many SENT and RECEIVED emails to import and submit — this
     service fetches them from Gmail and posts each one to the main API
     (POST {API_URL}), exactly like the old mail_reader.py did.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.gmail_importer import GmailAuthError, auth_status, run_import, save_uploaded_token

logging.basicConfig(level="INFO", format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Mail Importer")


class ImportRequest(BaseModel):
    max_sent: int = 50
    max_received: int = 50


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/auth/status")
def get_auth_status():
    return auth_status()


@app.post("/auth/upload")
async def upload_auth_files(token: UploadFile = File(...)):
    token_bytes = await token.read()
    if not token_bytes:
        raise HTTPException(400, "Uploaded token.json is empty")

    return save_uploaded_token(token_bytes)


@app.post("/import")
def trigger_import(payload: ImportRequest):
    try:
        return run_import(payload.max_sent, payload.max_received)
    except GmailAuthError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:
        logger.exception("Import failed")
        raise HTTPException(500, f"Import failed: {exc}") from exc


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Mail Importer</title>
<style>
  :root { color-scheme: dark; }
  body { font-family: system-ui, sans-serif; max-width: 640px; margin: 48px auto; padding: 0 20px;
         background: #0b0f17; color: #f1f5f9; }
  h1 { font-size: 1.4rem; }
  section { background: #131b2e; border: 1px solid rgba(255,255,255,.08); border-radius: 10px;
            padding: 20px; margin-bottom: 20px; }
  label { display: block; margin: 12px 0 4px; font-size: .9rem; color: #94a3b8; }
  input[type=file], input[type=number] { width: 100%; padding: 8px; border-radius: 6px;
            border: 1px solid rgba(255,255,255,.15); background: #0b0f17; color: #f1f5f9; }
  button { margin-top: 16px; padding: 10px 18px; border: none; border-radius: 6px;
           background: #6366f1; color: white; font-weight: 600; cursor: pointer; }
  button:hover { background: #4f46e5; }
  pre { white-space: pre-wrap; background: #090d16; padding: 12px; border-radius: 6px;
        font-size: .85rem; }
  .status { font-size: .85rem; color: #94a3b8; }
  .ok { color: #22c55e; } .missing { color: #f87171; }
</style>
</head>
<body>
  <h1>Gmail Import</h1>

  <section>
    <h2>1. Authentication</h2>
    <p class="status">token.json is generated on your own machine (the OAuth consent
      screen needs a browser). It already contains the client id/secret and refresh
      token, so it's the only file this container needs — just upload it below.</p>
    <p id="auth-status" class="status">Checking status…</p>
    <label>token.json</label>
    <input id="token-file" type="file" accept=".json" />
    <button onclick="uploadAuth()">Upload</button>
  </section>

  <section>
    <h2>2. Import</h2>
    <label>Number of SENT emails to import</label>
    <input id="max-sent" type="number" min="0" value="50" />
    <label>Number of RECEIVED emails to import</label>
    <input id="max-received" type="number" min="0" value="50" />
    <button onclick="runImport()">Import now</button>
  </section>

  <section>
    <h2>Result</h2>
    <pre id="result">—</pre>
  </section>

<script>
async function refreshStatus() {
  const r = await fetch('/auth/status');
  const s = await r.json();
  document.getElementById('auth-status').innerHTML =
    'token.json: ' + (s.token_json ? '<span class="ok">present</span>' : '<span class="missing">missing</span>');
}

async function uploadAuth() {
  const t = document.getElementById('token-file').files[0];
  if (!t) { alert('Choose token.json'); return; }
  const fd = new FormData();
  fd.append('token', t);
  const r = await fetch('/auth/upload', { method: 'POST', body: fd });
  document.getElementById('result').textContent = JSON.stringify(await r.json(), null, 2);
  refreshStatus();
}

async function runImport() {
  const max_sent = parseInt(document.getElementById('max-sent').value || '0', 10);
  const max_received = parseInt(document.getElementById('max-received').value || '0', 10);
  document.getElementById('result').textContent = 'Importing…';
  const r = await fetch('/import', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ max_sent, max_received }),
  });
  const body = await r.json();
  document.getElementById('result').textContent = JSON.stringify(body, null, 2);
}

refreshStatus();
</script>
</body>
</html>"""
