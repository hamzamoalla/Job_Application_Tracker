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
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_emails_thread_id ON emails(thread_id);
CREATE INDEX IF NOT EXISTS idx_emails_processed ON emails(processed);
CREATE INDEX IF NOT EXISTS idx_emails_sent_at ON emails(sent_at DESC);


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

-- ============================================================
-- 2. DONNÉES D'ENTRAÎNEMENT
-- ============================================================
-- Ancien bloc INSERT supprimé : la base training_examples n'est plus
-- seedée ici. Pour la peupler avec les exemples propres, après le premier
-- démarrage du conteneur postgres :
--
--   docker exec -i job_application_tracker-postgres-1 \
--       psql -U jobtracker -d jobtracker -f /training_data/reset_training_examples.sql
--
-- Source de vérité unique : db/training_examples/training_examples.csv
-- (le script SQL ne fait que TRUNCATE + charger ce CSV — pour ajouter ou
-- corriger un exemple, on édite uniquement le CSV, jamais de SQL).
