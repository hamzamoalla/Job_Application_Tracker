-- ============================================================
-- 1. TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS emails (
    id BIGSERIAL PRIMARY KEY,
    gmail_id TEXT UNIQUE NOT NULL,
    thread_id TEXT NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('SENT', 'RECEIVED')),
    sender TEXT,
    recipient TEXT,
    subject TEXT,
    body TEXT,
    sent_at TIMESTAMPTZ,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    classification TEXT,
    confidence DOUBLE PRECISION,
    -- Ignorer un email dans la file de relabellisation (sans changer label/confiance)
    review_dismissed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_emails_thread_id ON emails(thread_id);
CREATE INDEX IF NOT EXISTS idx_emails_processed ON emails(processed);
CREATE INDEX IF NOT EXISTS idx_emails_sent_at ON emails(sent_at DESC);
CREATE INDEX IF NOT EXISTS idx_emails_review_dismissed
    ON emails (review_dismissed)
    WHERE review_dismissed = TRUE;


CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    thread_id TEXT UNIQUE NOT NULL,
    company TEXT,
    position TEXT,
    application_date TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'SENT',
    confidence DOUBLE PRECISION,
    sent_email_id BIGINT REFERENCES emails(id),
    last_email_id BIGINT REFERENCES emails(id),
    source TEXT NOT NULL DEFAULT 'UNKNOWN',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);


CREATE TABLE IF NOT EXISTS training_examples (
    id BIGSERIAL PRIMARY KEY,
    task TEXT NOT NULL CHECK (task IN ('APPLICATION', 'REPLY')),
    text TEXT NOT NULL,
    label TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS processing_events (
    id BIGSERIAL PRIMARY KEY,
    email_id BIGINT REFERENCES emails(id),
    event_type TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- Historique des actions manuelles (dashboard : LABEL, DISMISS, UNDISMISS)
CREATE TABLE IF NOT EXISTS review_history (
    id                   BIGSERIAL PRIMARY KEY,
    email_id             BIGINT NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    action               TEXT NOT NULL,
    -- LABEL | DISMISS | UNDISMISS
    old_classification   TEXT,
    new_classification   TEXT,
    old_confidence       DOUBLE PRECISION,
    new_confidence       DOUBLE PRECISION,
    add_to_training      BOOLEAN NOT NULL DEFAULT FALSE,
    details              JSONB,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_review_history_created
    ON review_history (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_review_history_email
    ON review_history (email_id);

CREATE TABLE IF NOT EXISTS app_users (
    id              BIGSERIAL PRIMARY KEY,
    email           TEXT UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    first_name      TEXT NOT NULL DEFAULT '',
    last_name       TEXT NOT NULL DEFAULT '',
    company         TEXT NOT NULL DEFAULT '',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS app_sessions (
    token       TEXT PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at  TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_app_sessions_user ON app_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_app_sessions_expires ON app_sessions(expires_at);
