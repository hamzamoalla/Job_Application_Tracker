# Job Application Tracker

CPU-only microservice MVP for tracking job applications from Gmail.

## Architecture

- PostgreSQL: persistent database
- API: FastAPI REST API
- classifier-worker: continuously processes unprocessed emails
- trainer: trains TF-IDF + Multinomial Naive Bayes models
- Gmail reader: your existing step 1/2 code imports messages into `emails`

Important design:
- `gmail_id` uniquely identifies an email.
- `thread_id` connects the initial application and recruiter replies.
- The ML model does NOT decide whether an unrelated incoming email belongs to an application.
- Replies are classified only when their `thread_id` already exists in `applications`.
- Low-confidence predictions become `NEEDS_REVIEW`.

## 1. Start PostgreSQL

From this directory:

```bash
docker compose up -d postgres
```

## 2. Seed initial training examples

Install dependencies locally, or run:

```bash
docker compose run --rm trainer python -c "print('trainer image ready')"
```

Seed the initial examples inside the trainer container:

```bash
docker compose run --rm trainer python seed_training.py
```

The seed data is intentionally small. Replace/expand it with your own labelled emails.

## 3. Train

```bash
docker compose run --rm trainer
```

This writes two models into the shared Docker volume:

- `application_model.joblib`
- `reply_model.joblib`

## 4. Start API and worker

```bash
docker compose up -d api classifier-worker
```

API:
http://localhost:8000

Swagger:
http://localhost:8000/docs

## 5. Import emails

Modify your existing Gmail reader so that after reading each email it calls the logic in:

`scripts/import_gmail.py`

For every Gmail message, preserve:

- Gmail `id`
- Gmail `threadId`
- direction
- sender
- recipient
- subject
- body
- date

Do NOT discard `threadId`.

## 6. Useful API calls

Health:

```bash
curl http://localhost:8000/health
```

Applications:

```bash
curl http://localhost:8000/applications
```

Statistics:

```bash
curl http://localhost:8000/stats
```

## 7. Manual labelling / active learning

If a prediction is wrong, label the email:

```bash
curl -X POST http://localhost:8000/emails/123/label \
  -H "Content-Type: application/json" \
  -d '{"label":"REJECTION"}'
```

Then retrain:

```bash
docker compose run --rm trainer
```

Restart the worker if needed:

```bash
docker compose restart classifier-worker
```

## Suggested next step

Build a small web dashboard on top of `/applications` and add:
- filters by status/company/date
- confidence indicator
- "correct classification" buttons
- application details with the whole Gmail thread
- manual company/position editing
