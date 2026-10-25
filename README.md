# Job Application Tracker

CPU-only microservice application that imports your Gmail messages, classifies
them automatically with machine learning, and keeps a live picture of every
job application you have sent — status, company, position and the full
history of exchanges — without you having to maintain a spreadsheet by hand.

---

## 1. What the project does, in one paragraph

Gmail messages are imported (sent + received), cleaned, and run through two
ML models: one decides whether a **sent** email is a real job application
(`JOB_APPLICATION` vs `OTHER`), the other decides what a **received** reply
means (`INTERVIEW`, `IN_REVIEW`, `REJECTION`, or `OTHER`). A thread-matching
layer turns those predictions into `applications` rows with a status
(`SENT` → `IN_REVIEW` / `INTERVIEW` / `REJECTED`), and a small dashboard lets
you browse everything, correct wrong predictions, and feed those corrections
back into the training set for the next training run.

---

## 2. Architecture — the docker-compose services

| Service | Role | Port |
|---|---|---|
| `postgres` | Database for everything (app data + MLflow backend) | 5432 |
| `pgadmin` | Web UI to browse the Postgres database | 5050 |
| `mlflow-db-init` | One-shot job: creates the `mlflow` database if missing | – |
| `mlflow` | MLflow tracking server (experiment/run history, model registry) | 5000 |
| `api` | FastAPI REST API — single entry point for the frontend and for importing emails | 8000 |
| `classifier-worker` | Background loop: polls unprocessed emails, classifies them, updates applications | – |
| `frontend` | Static dashboard (nginx + `dashboard.html`) | 8080 |
| `mail-importer` | Talks to the Gmail API, imports messages into the DB via the `api` | 8081 |
| `trainer` | Trains/evaluates/publishes models (run on demand, not part of the normal stack — profile `train`) | – |

```
Gmail  ──▶  mail-importer  ──▶  api  ──▶  postgres (emails table)
                                              │
                                              ▼
                                   classifier-worker (polls every 15s)
                                   ├─ ML model (sentence-transformers + sklearn)
                                   ├─ GLiNER NER fallback (company/position)
                                   └─ thread-matching / status logic
                                              │
                                              ▼
                                   postgres (applications, processing_events)
                                              │
                                              ▼
                                   api  ──▶  frontend (dashboard)

                                   trainer (on demand) ──▶ mlflow (tracking)
                                                       ──▶ models_data volume
                                                           (consumed by api + classifier-worker)
```

Models are stored with `joblib` in the shared `models_data` volume and are
**hot-reloaded** by the classifier-worker (it checks the file's mtime on
every poll cycle) — you can retrain and publish a new model without
restarting the worker.

### Running it

```bash
docker compose up -d                 # postgres, pgadmin, mlflow, api, classifier-worker, frontend, mail-importer
docker compose --profile train run --rm trainer   # run a training job (see §5)
```

Default local URLs: API `http://localhost:8000`, dashboard
`http://localhost:8080`, MLflow UI `http://localhost:5000`, pgAdmin
`http://localhost:5050`.

The Gmail credentials (`credentials.json` / OAuth `token.json`) are uploaded
through the mail-importer's `/auth/upload` endpoint and persisted in the
`mail_auth_data` volume — they are never baked into the image.

---

## 3. Database schema (`db/schema.sql`)

> The schema evolved beyond the original `db/init.sql` (new tables
> `application_emails` and `review_queue`, extra columns on `emails` /
> `applications`). `db/schema.sql` is the up-to-date source of truth,
> reconstructed from the live database — use it to (re)create the schema
> from scratch.

- **`emails`** — every imported Gmail message. `gmail_id` is unique;
  `thread_id` is what links a sent application to its replies.
  `direction` is `SENT` or `RECEIVED`. Once classified: `classification`,
  `confidence`, `classified_by`, `processed`, and `review_dismissed` (for
  predictions you've marked as "not relevant, stop asking me").
- **`applications`** — one row per job application, keyed by `thread_id`.
  Holds `company`, `position`, `status`, `application_date`, `source`,
  `related_addresses`, and foreign keys to the sent email and the most
  recent email in the thread.
- **`application_emails`** — many-to-many link between `applications` and
  `emails` (an application can be tied to more than one relevant email),
  tagged with a `role` (`SENT` / `CONFIRMATION` / `INTERVIEW` /
  `REJECTION` / `OTHER`).
- **`training_examples`** — the labelled dataset used to train the models.
  `task` is `APPLICATION` or `REPLY`, `label` is the target class. Only the
  email **body** is stored in `text`; the subject is stored separately and
  the two are recombined at train/predict time (see §4.1 — this matters).
  A `UNIQUE (task, label, subject, text)` constraint prevents literal
  duplicates.
- **`processing_events`** — an audit log of what the classifier-worker did
  with each email (JSON `details`).
- **`review_history`** — every manual correction made from the dashboard
  (old label → new label, confidence before/after, whether it was added to
  the training set).
- **`review_queue`** — predictions awaiting manual review (`task`, raw
  `text`, `predicted_label`, `confidence`, `reviewed`, `correct_label`),
  feeding the dashboard's review screen.
- **`app_users` / `app_sessions`** — simple email+password auth for the
  dashboard, with a token-based session table.

---

## 4. The ML pipeline

### 4.1 Text preparation — the "golden rule"

A model is only as good as the consistency between training and inference.
`text_cleaning.py` defines `prepare_ml_text()` / `prepare_ml_text_full()`,
which rebuild the exact text the model sees (subject + cleaned body,
boilerplate/legal-footer stripped, HTML stripped, normalized whitespace)
from the raw `subject` + `text` columns. **The golden rule: training text
and prediction text must go through the exact same preparation function.**
This is why `training_examples.text` stores only the raw body — the wrapper
(subject + cleaning) is always rebuilt on the fly, never baked into storage,
so there is only one place that can drift.

Two models, two text strategies (`MODEL_TEXT_SOURCE` in `train.py`):

- **APPLICATION** model → `truncated` text (`prepare_ml_text`, capped
  length). Sent emails are short and the relevant signal is near the top.
- **REPLY** model → `full` text (`prepare_ml_text_full`, no truncation),
  because the decisive sentence in a recruiter reply ("unfortunately...",
  "we'd like to schedule a call...") can appear anywhere in a long email.

### 4.2 Embeddings

Both models turn text into vectors with a multilingual sentence-transformer
(handles English/French/German emails) before classifying with scikit-learn.

- The **code default** (`ml_embedding.py`, `DEFAULT_MODEL_NAME`) is
  `paraphrase-multilingual-MiniLM-L12-v2`.
- The **trainer service actually runs with**
  `EMBEDDING_MODEL_NAME=paraphrase-multilingual-mpnet-base-v2`
  (set in `docker-compose.yml`) — larger and more accurate, still CPU-only.
  Keep this in mind if you ever run the trainer script outside Docker: you
  need to set that environment variable yourself or you'll silently get the
  smaller default model.

### 4.3 Chunking and pooling (REPLY model)

Replies are split into **sentence-level chunks** (chunking strategy is
fixed to `"sentence"` for REPLY — other strategies were tried earlier in
this project and dropped), each chunk is embedded, and the chunk vectors
are combined ("pooled") into one vector per email. `ChunkPoolingEmbedder`
supports several pooling methods, because a recruiter email is usually
mostly boilerplate ("thank you for your interest...", legal footers) with
only one or two sentences actually carrying the signal — plain averaging
dilutes that signal:

| Pooling | Idea |
|---|---|
| `mean` | Average of all chunk vectors. Simple baseline; dilutes the signal in long emails. |
| `max` | Element-wise max across chunks. Keeps the strongest activation per dimension. |
| `mean_topk` | Average of only the `topk` most "extreme" chunks (keeps mean's stability, drops the most obviously irrelevant boilerplate chunks). |
| `em_local` | Fits a 2-component Gaussian Mixture **per email** on its own chunks, treats the smaller/majority "generic" component as boilerplate, and does a weighted mean favoring non-generic chunks. No labels needed. |
| `em_global` | Same idea, but the Gaussian Mixture is fit **once on the whole training set** (`fit()`), then reused (`transform()`) on every email — learns what "generic across all emails" looks like, not just within one email. |
| `sentence_attention_joint` | A pure NumPy attention + classifier trained jointly end-to-end (no separate pooling step) — learns which sentences matter *for classification*, using the labels directly. The only method that uses labels during pooling. |

On this project's real data, `em_global`/`em_local` did **not** beat plain
`mean`/`max` pooling (e.g. one real run: `mean`/`max` F1 ≈ 0.94 vs.
`em_global` ≈ 0.91, `em_local` ≈ 0.80–0.82) — they're kept as candidates the
comparison step evaluates, not because they're assumed to win.

`em_global` is evaluated carefully to avoid cross-validation leakage: unlike
the stateless poolings (precomputed once), it's wrapped in a full
`sklearn.Pipeline` and refit from scratch inside each CV fold, so the GMM
never "sees" validation-fold documents during its own fit.

### 4.4 Training and the manual publish workflow

`services/trainer/train/train.py` runs two independent flows:

- **`train_application()`** — unchanged automatic flow: builds the
  APPLICATION model, cross-validates (`StratifiedKFold`, scored on
  `f1_macro`, tracked in MLflow), and auto-publishes if it clears the
  quality gate (`MIN_F1_TO_PUBLISH=0.80` and no regression worse than
  `MAX_F1_REGRESSION=0.03` vs. the currently deployed model).

- **`train_reply()`** — **you choose what gets deployed.** It evaluates
  every pooling × classifier combination (plus the attention model) with
  cross-validation, writes a ranked report to
  `MODEL_DIR/reply_candidates_report.txt`, and logs everything to MLflow —
  but **does not publish anything** unless you explicitly tell it which
  candidate to deploy via the `PUBLISH_REPLY_CANDIDATE` environment
  variable:

  ```bash
  # 1) Explore candidates only (writes the report, publishes nothing)
  docker compose --profile train run --rm trainer

  # 2) Read reply_candidates_report.txt (or the MLflow UI), pick a key, then:
  docker compose --profile train run --rm \
    -e PUBLISH_REPLY_CANDIDATE=sentence_mean__linear_svm_calibrated \
    trainer
  ```

  The quality gate still runs on your chosen candidate, but only as a
  **safety floor** (it blocks publishing something below `0.80` F1 or a
  bad regression) — it never picks the model for you. An unknown key
  raises a clear error listing the valid keys from the last evaluation.

### 4.5 Quality gate & MLflow

Every training run is logged to MLflow (`jobtracker-classification`
experiment): params, CV fold scores, the final `f1_macro`, and the
published model artifact. `MIN_F1_TO_PUBLISH` and `MAX_F1_REGRESSION`
(both env vars on the `trainer` service) are the two guardrails that gate
any publish, for both models.

### 4.6 Debugging the pipeline

`services/trainer/debug_pipeline.py` runs real `training_examples` rows (or
emails) through raw → cleaned → chunked and writes a readable **file**
report (not just logs) so you can visually spot bad behavior: empty bodies
after cleaning, boilerplate-stripping that ate the whole email, chunks that
look wrong, etc. Worth running after any change to `text_cleaning.py` or to
the chunking logic.

---

## 5. The classifier-worker (runtime inference)

`services/classifier-worker/worker/main.py` polls `emails` every
`POLL_INTERVAL` seconds (default 15) for unprocessed rows, in batches of up
to 100:

1. **Sent emails** → APPLICATION model → `JOB_APPLICATION` or `OTHER`.
2. **Received emails**, only if their `thread_id` already matches an
   existing application (the model never decides on its own whether an
   unrelated incoming email belongs to an application) → REPLY model →
   `INTERVIEW` / `IN_REVIEW` / `REJECTION` / `OTHER`.
3. Predictions below `MIN_CONFIDENCE` (0.70) are still saved but flagged
   `NEEDS_REVIEW` via `REVIEW_CONFIDENCE_THRESHOLD`, so you can correct them
   from the dashboard instead of trusting a guess.
4. **Entity extraction** (`worker/extraction.py`) pulls company name and
   position out of sent emails using regex + sender domain heuristics, with
   a **GLiNER** NER model (`urchade/gliner_multi-v2.1`, multilingual) as a
   fallback when the heuristics come up empty — toggled with
   `ENABLE_GLINER_FALLBACK`.
5. **Thread matching & status** (`worker/matching.py`): a `JOB_APPLICATION`
   creates a new `applications` row (`status=SENT`); a classified reply
   updates the matching application's status via:

   | Reply label | New application status |
   |---|---|
   | `IN_REVIEW` | `IN_REVIEW` |
   | `INTERVIEW` | `INTERVIEW` |
   | `REJECTION` | `REJECTED` |

   Also handles deduplicating applications for the same company/thread and
   expiring stale ones.

Models are loaded with `joblib` from `MODEL_DIR` and **hot-reloaded**
whenever their file mtime changes — no worker restart needed after a new
model is published.

---

## 6. API (`services/api`)

FastAPI service, the only thing the frontend and mail-importer talk to.

- `GET /health`, `GET /stats` — service health and aggregate counts.
- `GET /applications`, `GET /applications/{id}` — browse tracked applications.
- `POST /emails`, `GET /emails`, `GET /emails/{id}` — ingest/list/view emails.
- `POST /emails/{id}/label` — manually correct a classification (feeds
  `review_history` and, optionally, `training_examples`).
- `POST /emails/{id}/dismiss` / `POST /emails/{id}/undismiss` — hide/unhide
  a prediction from the "needs review" queue without relabeling it.
- `POST /emails/batch-dismiss` — same, in bulk.
- `GET /review-history` — audit trail of manual corrections.
- `GET /auth/bootstrap`, `POST /auth/register`, `POST /auth/login`,
  `GET /auth/me`, `POST /auth/logout` — simple session-based auth for the
  dashboard.
- `POST /import/run` — trigger a Gmail import on demand (also runs
  automatically via the mail-importer's own poll loop).

---

## 7. Frontend

A static dashboard (`services/frontend/dashboard.html`, served by nginx) for
browsing applications and emails, reviewing low-confidence predictions, and
correcting labels — which is also how new, *real* training examples get
added over time instead of relying only on synthetic ones.

---

## 8. Seeding training data / labelling

- `scripts/seed_training.py` — load `training_examples` from a SQL/CSV seed.
- `db/add_synthetic_paragraph_examples.sql` — a curated set of realistic,
  multi-sentence, multilingual (EN/FR/DE) synthetic examples across all
  REPLY/APPLICATION labels, used to compensate for a shortage of real,
  manually-labelled data for some classes (notably `INTERVIEW`).
- `label.py` — a small CLI helper for manually labelling emails.
- The dashboard's manual correction flow (`/emails/{id}/label`) is the
  primary source of **real** training examples going forward — prefer it
  over synthetic data whenever you have genuine labelled emails, since
  several classes are currently majority-synthetic.

---

## 9. Reproducing the training set on a fresh deployment

`training_examples` contains real recruiter emails, so the plaintext export
is never committed to GitHub. Instead:

- `encrypt_training_data.py` encrypts a local `training_data.txt` export
  (PBKDF2-HMAC-SHA256 + Fernet/AES, password-derived key) into
  `training_data.enc` — that's the file that gets committed/pushed.
- `decrypt_and_insert_training.py` decrypts it and inserts the rows
  straight into `training_examples` (idempotent, thanks to the table's
  `UNIQUE` constraint — safe to re-run on every redeploy).

In both scripts the decryption/encryption key is **always typed in
interactively** (hidden input) — it is never hardcoded, passed as a CLI
argument, or committed anywhere.

```bash
pip install cryptography psycopg2-binary

# one-time, locally: produce the file that goes to GitHub
python encrypt_training_data.py training_data.txt training_data.enc

# on (re)deployment
export DATABASE_URL=postgresql://jobtracker:jobtracker@localhost:5432/jobtracker
python decrypt_and_insert_training.py training_data.enc
```

---

## 10. Quick local setup (no Docker, for iterating on the trainer)

```bash
# 1. Start Postgres (or use docker compose up -d postgres mlflow)
# 2. Apply the schema
psql -U jobtracker -d jobtracker -f db/schema.sql

# 3. Seed training examples
python scripts/seed_training.py

# 4. Train (make sure EMBEDDING_MODEL_NAME matches the Docker setup if you
#    want comparable results — see §4.2)
export EMBEDDING_MODEL_NAME=paraphrase-multilingual-mpnet-base-v2
export DATABASE_URL=postgresql://jobtracker:jobtracker@localhost:5432/jobtracker
export MLFLOW_TRACKING_URI=http://localhost:5000
python services/trainer/train/train.py
# then re-run with PUBLISH_REPLY_CANDIDATE=<key> once you've picked a model

# 5. Start API + worker, import emails, open the dashboard
docker compose up -d api classifier-worker frontend mail-importer
```

---

## 11. Design decisions worth knowing

- `gmail_id` is the uniqueness anchor for emails; `thread_id` is what
  stitches a sent application to its replies.
- The model **never** decides on its own that an unrelated incoming email
  belongs to an application — a reply is only classified if its thread
  already exists in `applications`.
- Low-confidence predictions are never silently trusted — they're surfaced
  as `NEEDS_REVIEW` so a human confirms them, and that confirmation is what
  grows the real (non-synthetic) training set.
- REPLY candidate selection is deliberately manual: cross-validated metrics
  are a guide, not an automatic decision — you look at the report/MLflow
  run and pick the model yourself before it's ever published.