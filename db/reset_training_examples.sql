-- Recrée la table training_examples à partir de ZÉRO, puis la remplit
-- uniquement depuis db/training_examples/training_examples.csv.
--
-- Pourquoi un CSV séparé : pour ajouter/corriger des exemples
-- d'entraînement, vous n'éditez plus jamais ce fichier .sql — seulement
-- le CSV, avec n'importe quel éditeur ou tableur (Excel/LibreOffice
-- ouvrent un CSV directement, en gardant le guillemetage intact).
--
-- Usage (depuis la racine du projet, conteneur postgres déjà démarré) :
--   docker compose up -d postgres
--   docker exec -i job_application_tracker-postgres-1 \
--       psql -U jobtracker -d jobtracker -f /training_data/reset_training_examples.sql
--
-- Le dossier db/training_examples est monté dans le conteneur postgres
-- sur /training_data (voir docker-compose.yml), donc \copy peut lire le
-- CSV directement sans avoir besoin de le pousser manuellement.

BEGIN;

TRUNCATE TABLE training_examples RESTART IDENTITY;

\copy training_examples(task, label, text) FROM '/tmp/training_examples.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

COMMIT;

-- Petit résumé de contrôle après chargement.
SELECT task, label, COUNT(*) AS n
FROM training_examples
GROUP BY task, label
ORDER BY task, label;
