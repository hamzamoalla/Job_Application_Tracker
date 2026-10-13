import os
import re
import time
import logging
from difflib import SequenceMatcher
from email.utils import parseaddr

import joblib
import psycopg
from psycopg.rows import dict_row
from gliner import GLiNER
from text_cleaning import normalize, clean_reply, prepare_ml_text, clean_for_extraction

import ml_embedding  # noqa: F401

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://jobtracker:jobtracker@postgres:5432/jobtracker",
)
MODEL_DIR = os.getenv("MODEL_DIR", "/app/models")
APPLICATION_MODEL_PATH = os.path.join(MODEL_DIR, "application_model.joblib")
REPLY_MODEL_PATH = os.path.join(MODEL_DIR, "reply_model.joblib")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.80"))
REVIEW_CONFIDENCE_THRESHOLD = float(os.getenv("REVIEW_CONFIDENCE_THRESHOLD", "0.70"))
STALE_IN_REVIEW_DAYS = int(os.getenv("STALE_IN_REVIEW_DAYS", "30"))

application_model = None
reply_model = None
gliner_model = None

# ---------------------------------------------------------
# Mots-clés métiers & Filtres candidats
# ---------------------------------------------------------
JOB_KEYWORDS = {
    "developer", "engineer", "consultant", "analyst", "architect", "manager",
    "développeur", "ingénieur", "architecte", "stagiaire", "intern", "lead",
    "specialist", "spécialiste", "technician", "technicien", "administrator",
    "administrateur", "designer", "director", "directeur", "head", "officer",
    "consultante", "développeuse", "ingénieure", "expert", "data", "devops"
}

SECOND_LEVEL_SUFFIXES = {"com", "net", "org", "gov", "edu", "co", "or", "ac"}


def is_job_title_like(text: str) -> bool:
    """Vérifie si une chaîne ressemble à un titre de poste plutôt qu'à une entreprise."""
    if not text:
        return False
    words = set(re.findall(r"\w+", text.lower()))
    return bool(words & JOB_KEYWORDS)


def is_candidate_current_employer(company: str, full_text: str) -> bool:
    """Vérifie si l'entreprise extraite est l'employeur actuel du candidat."""
    if not company or not full_text:
        return False

    known_employers = {
        e.strip().lower() for e in os.getenv("CURRENT_EMPLOYERS", "KPIT").split(",") if e.strip()
    }
    if company.lower() in known_employers:
        logger.info("Entreprise '%s' ignorée : présente dans CURRENT_EMPLOYERS.", company)
        return True

    clean_text = re.sub(r"\s+", " ", full_text)
    escaped = re.escape(company)

    application_context_pattern = (
        r"(?i)\b(?:application|candidature|interest in|position|role|poste|applying|applied)\b.{0,100}?\b(?:at|chez|with|for|auprès de)\s+" + escaped
    )
    if re.search(application_context_pattern, clean_text):
        return False

    patterns = [
        r"(?i)\b(?:actuellement|en poste)\b.{0,100}?\b(?:chez|au sein de|à)\s+" + escaped,
        r"(?i)\bje suis\b.{0,80}?\bactuellement\b.{0,80}?\b(?:chez|au sein de|à)\s+" + escaped,
        r"(?i)\bmon employeur actuel\b",
        r"(?i)\bcurrently\b.{0,100}?\b(?:working|employed|working as)\b.{0,80}?\b(?:at|with)\s+" + escaped,
        r"(?i)\bI am\b.{0,80}?\bcurrently\b.{0,80}?\b(?:at|with)\s+" + escaped,
        r"(?i)\bmy current (?:employer|company)\b",
    ]

    for p in patterns:
        if re.search(p, clean_text):
            logger.info("Entreprise '%s' ignorée : détectée comme employeur actuel dans le texte.", company)
            return True

    return False


# ---------------------------------------------------------
# Patterns Regex
# ---------------------------------------------------------
COMPANY_PATTERNS = [
    r"(?i)\bthank you for applying (?:to|at|for)\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
    r"(?i)\bthank you for your application (?:to|at|for)\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
    r"(?i)\bwe have received your application (?:to|at|for)\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
    r"(?i)\bapplication (?:has been|was) received (?:at|by|for)\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
    r"(?i)\bregarding your application (?:at|to|for)\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
    r"(?i)\bcandidature (?:chez|auprès de)\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
    r"(?i)\bnous avons bien reçu votre candidature (?:chez|auprès de)\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
    r"(?i)\bvotre candidature chez\s+([A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ0-9&.'’\- ]{1,70})",
]

IGNORED_DOMAINS = {
    "gmail", "yahoo", "outlook", "hotmail", "icloud", "protonmail", "mail",
    "noreply", "no-reply", "donotreply", "jobs", "careers", "hr", "recruitment",
    "talent", "apply", "workday", "greenhouse", "lever", "smartrecruiters",
    "indeed", "linkedin", "mailchimp", "sendgrid", "amazon", "google",
}

POSITION_PATTERNS = [
    r"(?i)\bposition\s*[:\-–]\s*([^\n\r|;]{2,120})",
    r"(?i)\bjob title\s*[:\-–]\s*([^\n\r|;]{2,120})",
    r"(?i)\brole\s*[:\-–]\s*([^\n\r|;]{2,120})",
    r"(?i)\bposte\s*[:\-–]\s*([^\n\r|;]{2,120})",
    r"(?i)\bintitulé du poste\s*[:\-–]\s*([^\n\r|;]{2,120})",
    r"(?i)\binterest in the\s+([^\n\r|;,.]{2,120})\s+(?:position|role)\b",
    r"(?i)\bfor the (?:position|role) of\s+([^\n\r|;,.]{2,120})",
    r"(?i)\bfor the\s+([^\n\r|;,.]{2,120})\s+(?:position|role)\b",
    r"(?i)\bapplication for (?:the )?(?:position of )?\s*([^\n\r|;,.]{2,120})",
    r"(?i)\bau poste de\s+([^\n\r|;,.]{2,120})",
    r"(?i)(?:open application|spontaneous application|candidature spontanée|candidature)\s*[-–—:]\s*([^\n\r|;]{3,120})",
]


def clean_company_name(value: str) -> str:
    if not value:
        return ""
    value = value.strip(" \t\r\n-:|.,;•")
    value = re.split(
        r"\s+(?:for the position|for the role|for our|has been|was|is|regarding|about|"
        r"position|poste|role|job|application|candidature|update)\b",
        value,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    value = re.sub(r"^[\-–—]\s*", "", value)
    return value.strip(" \t\r\n-:|.,;")[:100]


def clean_position_title(value: str) -> str:
    if not value:
        return ""
    value = value.strip(" \t\r\n-:|.,;•–—")
    value = re.split(r"\s+(?:at|chez|@)\s+[A-Z]", value, maxsplit=1)[0]
    return re.sub(r"\s+", " ", value)[:120]


def email_address(value) -> str:
    return parseaddr(value or "")[1].lower().strip()


def domain_company_from_email(address: str):
    addr = email_address(address)
    if "@" not in addr:
        return None
    domain = addr.rsplit("@", 1)[1].lower()
    parts = domain.split(".")
    if len(parts) < 2:
        return None

    if len(parts) >= 3 and parts[-2] in SECOND_LEVEL_SUFFIXES:
        name = parts[-3]
    else:
        name = parts[-2]

    if name in IGNORED_DOMAINS or len(name) <= 2:
        return None
    return name.replace("-", " ").replace("_", " ").title()


# ---------------------------------------------------------
# Extraction Regex + GLiNER
# ---------------------------------------------------------
def extract_with_gliner(subject: str, body: str):
    if gliner_model is None:
        return None, None

    text = f"Subject: {subject or ''}\n\n{body or ''}"[:1200]
    labels = ["company name", "job title", "position"]

    try:
        entities = gliner_model.predict_entities(text, labels, threshold=0.30)
        company, position = None, None

        for ent in entities:
            label = ent["label"]
            val = ent["text"].strip()

            if label == "company name" and not company:
                cleaned = clean_company_name(val)
                if len(cleaned) >= 2 and cleaned.lower() not in IGNORED_DOMAINS:
                    company = cleaned

            elif label in ("job title", "position") and not position:
                cleaned = clean_position_title(val)
                if 3 <= len(cleaned) <= 120:
                    position = cleaned

        return company, position
    except Exception:
        logger.exception("Erreur extraction GLiNER")
        return None, None


def extract_company_regex(subject: str, body: str):
    text = f"{subject or ''}\n{body or ''}"
    for pattern in COMPANY_PATTERNS:
        match = re.search(pattern, text)
        if match:
            name = clean_company_name(match.group(1))
            if len(name) >= 2 and not is_job_title_like(name):
                return name
    return None


def extract_position_regex(subject: str, body: str):
    text = f"{subject or ''}\n{body or ''}"
    for pattern in POSITION_PATTERNS:
        match = re.search(pattern, text)
        if match:
            value = clean_position_title(match.group(1))
            if 3 <= len(value) <= 150:
                return value

    subject = (subject or "").strip()
    for sep in (" – ", " - ", " | ", ": "):
        if sep in subject:
            parts = [p.strip() for p in subject.split(sep) if p.strip()]
            for part in reversed(parts):
                if is_job_title_like(part) and 3 <= len(part) <= 150:
                    return part
    return None


def extract_company_and_position(email_addr: str, subject: str, body: str):
    company, company_src = None, None
    position, position_src = None, None
    full_text = f"{subject or ''}\n{body or ''}"

    # 1. Regex
    c_reg = extract_company_regex(subject, body)
    if c_reg and not is_candidate_current_employer(c_reg, full_text):
        company, company_src = c_reg, "REGEX"

    p_reg = extract_position_regex(subject, body)
    if p_reg:
        position, position_src = p_reg, "REGEX"

    # 2. GLiNER
    if not company or not position:
        gl_c, gl_p = extract_with_gliner(subject, body)
        if not company and gl_c:
            if not is_job_title_like(gl_c) and not is_candidate_current_employer(gl_c, full_text):
                company, company_src = gl_c, "GLINER"
        if not position and gl_p:
            position, position_src = gl_p, "GLINER"

    # 3. Domaine e-mail
    if not company and email_addr:
        dom_c = domain_company_from_email(email_addr)
        if dom_c and not is_candidate_current_employer(dom_c, full_text):
            company, company_src = dom_c, "EMAIL_DOMAIN"

    if company and position and company.lower() == position.lower():
        if email_addr:
            dom_c = domain_company_from_email(email_addr)
            if dom_c and not is_candidate_current_employer(dom_c, full_text):
                company, company_src = dom_c, "EMAIL_DOMAIN"
            else:
                company, company_src = None, None

    logger.info(
        "RESULTAT EXTRACTION -> Entreprise: '%s' (via %s) | Poste: '%s' (via %s)",
        company or "INCONNU", company_src or "NONE",
        position or "INCONNU", position_src or "NONE"
    )

    return company, position, company_src, position_src


# ---------------------------------------------------------
# Classification Heuristique
# ---------------------------------------------------------
def heuristic_classification(subject, body):
    
    # On nettoie aussi ici pour les heuristiques
    subject, body = clean_for_extraction(subject, body)
    text = f"{subject or ''}\n{body}"
    normalized = normalize(text)
    # ... le reste de la fonction ne change pas

    rejection_patterns_high = [
        r"\bwe regret to inform you\b",
        r"\bwe regret to let you know\b",
        r"\bregret to inform\b",
        r"\bnot moving forward with your application\b",
        r"\bwill not be moving forward\b",
        r"\bwe will not be progressing\b",
        r"\bdecided to pursue other candidates\b",
        r"\bother candidates whose qualifications\b",
        r"\bwe are unable to offer you\b",
        r"\byour application (?:has been|was) rejected\b",
        r"\bapplication rejected\b",
        r"\bnot selected for (?:the|this) position\b",
        r"\bposition has been filled\b",
        r"\bwe have decided not to proceed\b",
        r"\bwe will not be inviting you\b",
        r"\bunfortunately.{0,80}(?:not selected|not moving|not progressing|cannot move)\b",
        r"\bafter careful consideration.{0,60}(?:not|unable|will not)\b",
        r"\bwe have chosen to continue with other candidates\b",
        r"\byour application will not be progressing\b",
        r"\bupdate on your application\b.{0,150}\b(?:unfortunately|not successful|not moving forward|decided not to|will not)\b",
        r"\bapplication update\b.{0,150}\b(?:unfortunately|regret|not selected|not successful|not moving forward)\b",
        r"\bwe have decided to move forward with other candidates\b",
        r"\bwon't be moving (?:forward|ahead) with your application\b",
        r"\bcandidature n'a pas été retenue\b",
        r"\bcandidature n’est pas retenue\b",
        r"\bne donnerons pas suite à votre candidature\b",
        r"\bne pouvons pas donner suite\b",
        r"\bprofil ne correspond pas\b",
        r"\bcandidature refusée\b",
        r"\bpas retenu(?:e)? pour ce poste\b",
        r"\bmalheureusement.{0,100}(?:candidature|profil|poste)\b",
        r"\bnous avons choisi de poursuivre avec d'autres candidats\b",
        r"\ble poste ayant été pourvu\b",
        r"\bnous ne retenons pas votre candidature\b",
        r"\baprès étude de votre candidature.{0,40}ne donnerons pas suite\b",
        r"\bnous ne donnerons pas une suite favorable\b",
        r"\bne (?:pourrons|pourrez|pouvons|pourra) pas (?:te |vous )?donner suite\b",
        r"\bon ne va pas pouvoir donner suite\b",
        r"\bne donnera pas suite à (?:ta|votre) candidature\b",
        r"\bpas pu donner suite à (?:ta|votre) candidature\b",
        r"\bn'avons pas retenu (?:ta|votre) candidature\b",
        r"\bavons décidé de ne pas (?:donner suite|poursuivre)\b",
    ]
    if any(re.search(p, text, re.IGNORECASE) for p in rejection_patterns_high):
        return "REJECTION", 0.96

    if re.search(r"\bpetit retour sur (?:ta|votre) candidature\b", text, re.IGNORECASE):
        if re.search(r"\b(?:ne|n')\b.{0,80}\b(?:donner suite|retenu|retenue|poursuivre)\b", normalized):
            return "REJECTION", 0.85

    interview_patterns = [
        r"\binvitation to (?:an? )?interview\b",
        r"\binterview invitation\b",
        r"\bschedule (?:an? )?interview\b",
        r"\bwe would like to interview you\b",
        r"\binterview availability\b",
        r"\btechnical interview\b",
        r"\bphone interview\b",
        r"\bvideo interview\b",
        r"\bwe would like to invite you to (?:an? )?interview\b",
        r"\bnext stage of our recruitment process\b",
        r"\bentretien (?:téléphonique|technique|en visioconférence|vidéo)\b",
        r"\bconvocation à un entretien\b",
        r"\bnous souhaitons vous rencontrer\b",
        r"\bproposer un entretien\b",
        r"\bnous aimerions organiser un (?:premier )?entretien\b",
        r"\bseriez-vous disponible pour un entretien\b",
        r"\bvotre candidature a été présélectionnée\b",
    ]
    if any(re.search(p, text, re.IGNORECASE) for p in interview_patterns):
        return "INTERVIEW", 0.95

    confirmation_patterns = [
        r"\bthank you for applying\b",
        r"\bthank you for your application\b",
        r"\bapplication (?:has been|was) received\b",
        r"\bwe have received your application\b",
        r"\byour application has been submitted\b",
        r"\bapplication received\b",
        r"\bwe received your application\b",
        r"\byour application is (?:being )?reviewed\b",
        r"\byour application is under review\b",
        r"\bwe are currently reviewing\b",
        r"\byour profile is currently under review\b",
        r"\bapplication has been successfully submitted\b",
        r"\bwe will review your application\b",
        r"\byour application has been forwarded\b",
        r"\bcandidature bien reçue\b",
        r"\bnous avons bien reçu votre candidature\b",
        r"\bvotre candidature a bien été reçue\b",
        r"\bvotre candidature a été enregistrée\b",
        r"\baccusé de réception de votre candidature\b",
        r"\bnous accusons réception de votre candidature\b",
        r"\bvotre dossier est en cours d'étude\b",
        r"\bvotre candidature est (?:toujours )?à l'étude\b",
        r"\bnous allons l'examiner\b",
        r"\bnous avons bien reçu votre CV\b",
        r"\bgracias por (?:tu|su) interés\b",
        r"\bgracias por postular\b",
        r"\bhemos recibido tu candidatura\b",
    ]
    if any(re.search(p, text, re.IGNORECASE) for p in confirmation_patterns):
        return "IN_REVIEW", 0.94

    if re.search(r"\byour application (?:at|to|for)\b", subject or "", re.IGNORECASE):
        return "IN_REVIEW", 0.60
    if re.search(r"\bapplication update\b", subject or "", re.IGNORECASE):
        return "IN_REVIEW", 0.55

    if re.search(r"camscanner|scan_\d+|document scanned|verification code|one-time code|otp", normalized):
        return "OTHER", 0.95
    if re.search(
        r"\b(?:job alert|alerte emploi|newsletter|webinar|unsubscribe|désinscription|"
        r"free-work|tanitjobs|dernières opportunités|nouvelles offres)\b",
        normalized,
    ):
        return "OTHER", 0.92

    return None


# ---------------------------------------------------------
# Modèles ML
# ---------------------------------------------------------
def load_models():
    global application_model, reply_model, gliner_model

    if os.path.exists(APPLICATION_MODEL_PATH):
        application_model = joblib.load(APPLICATION_MODEL_PATH)
        logger.info("Modèle chargé : application_model (%s)", APPLICATION_MODEL_PATH)
    else:
        logger.warning("Modèle de candidature introuvable : %s", APPLICATION_MODEL_PATH)

    if os.path.exists(REPLY_MODEL_PATH):
        reply_model = joblib.load(REPLY_MODEL_PATH)
        logger.info("Modèle chargé : reply_model (%s)", REPLY_MODEL_PATH)
    else:
        logger.warning("Modèle de réponse introuvable : %s", REPLY_MODEL_PATH)

    try:
        logger.info("Chargement du modèle GLiNER (urchade/gliner_multi-v2.1)...")
        gliner_model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")
        logger.info("Modèle GLiNER chargé avec succès.")
    except Exception:
        logger.exception("Échec du chargement de GLiNER. Fallback sur Regex/Domaine uniquement.")


def model_predict(model, text, model_name: str = "unknown"):
    if model is None:
        logger.warning("Modèle '%s' non chargé → fallback OTHER", model_name)
        return "OTHER", 0.0
    try:
        probabilities = model.predict_proba([text])[0]
        index = probabilities.argmax()
        label = str(model.classes_[index])
        confidence = float(probabilities[index])
        logger.info("ML [%s] → label=%s  confidence=%.3f", model_name, label, confidence)
        return label, confidence
    except Exception:
        logger.exception("Erreur prédiction ML (%s)", model_name)
        return "OTHER", 0.0


def classify_sent(email):
    text = prepare_ml_text(email.get("subject"), email.get("body"))
    return model_predict(application_model, text, model_name="application_model")


def classify_received(email):
    subject = email.get("subject") or ""
    body = email.get("body") or ""

    rule_result = heuristic_classification(subject, body)
    text = prepare_ml_text(subject, body)
    label, confidence = model_predict(reply_model, text, model_name="reply_model")

    allowed = {"INTERVIEW", "IN_REVIEW", "REJECTION", "OTHER"}
    if label not in allowed:
        label, confidence = "OTHER", confidence

    if rule_result is None:
        return label, confidence

    rule_label, rule_confidence = rule_result
    if rule_confidence >= 0.90:
        logger.info("Heuristique prioritaire → %s (%.2f)", rule_label, rule_confidence)
        return rule_label, rule_confidence
    if label == rule_label:
        return label, min(0.95, max(confidence, rule_confidence) + 0.10)
    if confidence < rule_confidence:
        return rule_label, rule_confidence
    return label, confidence


# ---------------------------------------------------------
# Matching & Base de données
# ---------------------------------------------------------
def company_similarity(left, right):
    a, b = normalize(left or ""), normalize(right or "")
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:
        return 0.90
    return SequenceMatcher(None, a, b).ratio()


def position_similarity(left, right):
    a, b = normalize(left or ""), normalize(right or "")
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:
        return 0.90
    wa, wb = set(a.split()), set(b.split())
    union = wa | wb
    if not union:
        return 0.0
    return len(wa & wb) / len(union)


ROLE_BY_LABEL = {
    "JOB_APPLICATION": "SENT",
    "IN_REVIEW": "CONFIRMATION",
    "INTERVIEW": "INTERVIEW",
    "REJECTION": "REJECTION",
    "OTHER": "OTHER",
}


def link_email(conn, application_id, email_id, role, addresses=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO application_emails (application_id, email_id, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (application_id, email_id) DO UPDATE SET role = EXCLUDED.role
        """, (application_id, email_id, role))

        if addresses:
            clean = [a for a in (email_address(x) for x in addresses) if a]
            if clean:
                cur.execute("""
                    UPDATE applications
                    SET related_addresses = (
                            SELECT ARRAY(
                                SELECT DISTINCT unnest(
                                    COALESCE(related_addresses, '{}') || %s::text[]
                                )
                            )
                        ),
                        last_email_id = %s,
                        updated_at = NOW()
                    WHERE id = %s
                """, (clean, email_id, application_id))
            else:
                cur.execute("""
                    UPDATE applications
                    SET last_email_id = %s, updated_at = NOW()
                    WHERE id = %s
                """, (email_id, application_id))
        else:
            cur.execute("""
                UPDATE applications
                SET last_email_id = %s, updated_at = NOW()
                WHERE id = %s
            """, (email_id, application_id))


def insert_processing_event(conn, email_id, event_type, details):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO processing_events (email_id, event_type, details)
            VALUES (%s, %s, %s)
        """, (email_id, event_type, psycopg.types.json.Jsonb(details)))


def find_applications_by_company(conn, company, open_only=True):
    if not company:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT id, thread_id, company, position, status, source,
                   sent_email_id, last_email_id, related_addresses
            FROM applications
            WHERE company IS NOT NULL
            ORDER BY updated_at DESC NULLS LAST, id DESC
        """)
        rows = cur.fetchall()

    matches = []
    for app in rows:
        if company_similarity(company, app["company"]) < 0.82:
            continue
        if open_only and app["status"] in ("REJECTED",):
            continue
        matches.append(app)
    return matches


def find_matching_application(conn, company, position, address=None):
    candidates = find_applications_by_company(conn, company, open_only=True)
    if not candidates:
        return None

    addr = email_address(address) if address else None

    # 1. Matching direct par adresse e-mail
    if addr:
        for app in candidates:
            related = [email_address(x) for x in (app.get("related_addresses") or [])]
            if addr in related:
                return app

    # 2. Matching par similarité de poste
    if position:
        scored = []
        for app in candidates:
            if not app["position"]:
                scored.append((app, 0.75))
                continue
            p = position_similarity(position, app["position"])
            if p >= 0.40:
                scored.append((app, 0.60 + 0.40 * p))

        scored.sort(key=lambda x: x[1], reverse=True)
        if scored and scored[0][1] >= 0.70:
            if len(scored) > 1 and scored[0][1] - scored[1][1] < 0.08:
                logger.warning("Matching ambigu entreprise+poste : %s / %s", company, position)
                return None
            return scored[0][0]

    if len(candidates) == 1:
        return candidates[0]

    return None


def consolidate_duplicate_applications(conn):
    """
    Consolidation automatique en BDD :
    Recherche toute candidature 'IN_REVIEW' pour une entreprise qui possède DÉJÀ
    une candidature 'REJECTED' ou 'INTERVIEW'.
    Transfère tous ses e-mails vers la candidature principale et SUPPRIME la candidature IN_REVIEW.
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT a1.id AS stale_id, a1.company AS company, a2.id AS main_id, a2.status AS main_status, a2.position AS main_position
            FROM applications a1
            JOIN applications a2 ON LOWER(a1.company) = LOWER(a2.company) AND a1.id != a2.id
            WHERE a1.status = 'IN_REVIEW'
              AND a2.status IN ('REJECTED', 'INTERVIEW')
        """)
        duplicates = cur.fetchall()

    for dup in duplicates:
        stale_id = dup["stale_id"]
        main_id = dup["main_id"]
        logger.info(
            "Nettoyage automatique DB : Fusion de la candidature #%s (IN_REVIEW) dans #%s (%s - %s)",
            stale_id, main_id, dup["company"], dup["main_status"]
        )
        with conn.cursor() as cur:
            # Transfert propre des emails
            cur.execute("""
                INSERT INTO application_emails (application_id, email_id, role)
                SELECT %s, email_id, role
                FROM application_emails
                WHERE application_id = %s
                ON CONFLICT (application_id, email_id) DO NOTHING
            """, (main_id, stale_id))

            # Suppression des anciens liens
            cur.execute("DELETE FROM application_emails WHERE application_id = %s", (stale_id,))

            # Enrichir le poste si vide dans la candidature principale
            if dup["main_position"] is None:
                cur.execute("""
                    UPDATE applications
                    SET position = (SELECT position FROM applications WHERE id = %s)
                    WHERE id = %s AND position IS NULL
                """, (stale_id, main_id))

            # Suppression définitive de la candidature IN_REVIEW
            cur.execute("DELETE FROM applications WHERE id = %s", (stale_id,))


def apply_rejection(conn, email, company, position, confidence, company_src, position_src):
    sender = email_address(email.get("sender"))
    existing = find_matching_application(conn, company, position, address=sender)

    if existing:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE applications
                SET status = 'REJECTED',
                    position = COALESCE(position, %s),
                    confidence = %s,
                    last_email_id = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (position, confidence, email["id"], existing["id"]))

        link_email(conn, existing["id"], email["id"], "REJECTION", addresses=[sender])
        logger.info(
            "Candidature #%s mise à jour : %s / %s → REJECTED (Fusion mail de refus)",
            existing["id"], company, position or existing["position"] or "?"
        )
        insert_processing_event(conn, email["id"], "APPLICATION_STATUS_UPDATED", {
            "scope": "matched_fusion",
            "application_id": existing["id"],
            "company": company,
            "position": position,
            "company_source": company_src,
            "position_source": position_src,
            "confidence": confidence,
        })
        return [existing["id"]]

    candidates = find_applications_by_company(conn, company, open_only=True)

    if not candidates:
        return create_application(
            conn, email, company, position, "REJECTED", confidence, "WEBSITE_ASSUMED", "REJECTION", company_src, position_src
        )

    targeted = []
    for app in candidates:
        related = [email_address(x) for x in (app.get("related_addresses") or [])]
        if sender and sender in related:
            targeted.append(app)

    if targeted:
        to_reject = targeted
        scope = "targeted"
    elif position:
        to_reject = [
            app for app in candidates
            if app["position"] and position_similarity(position, app["position"]) >= 0.40
        ]
        if not to_reject:
            to_reject = candidates
            scope = "company_global_fallback"
        else:
            scope = "position"
    else:
        to_reject = candidates
        scope = "company_global"

    rejected_ids = []
    for app in to_reject:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE applications
                SET status = 'REJECTED',
                    position = COALESCE(position, %s),
                    confidence = %s,
                    last_email_id = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (position, confidence, email["id"], app["id"]))
        link_email(conn, app["id"], email["id"], "REJECTION", addresses=[sender])
        rejected_ids.append(app["id"])

    insert_processing_event(conn, email["id"], "APPLICATION_STATUS_UPDATED", {
        "scope": scope,
        "rejected_ids": rejected_ids,
        "company": company,
        "position": position,
        "company_source": company_src,
        "position_source": position_src,
        "confidence": confidence,
    })
    return rejected_ids


def create_application(conn, email, company, position, status, confidence, source, role, company_src, position_src):
    thread_id = email.get("thread_id") or f"external:{email['gmail_id']}"
    if source == "WEBSITE_ASSUMED":
        thread_id = f"external:{email['gmail_id']}"

    addresses = [email.get("recipient" if email.get("direction") == "SENT" else "sender")]

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            INSERT INTO applications (
                thread_id, company, position, application_date,
                status, confidence, sent_email_id, last_email_id,
                source, related_addresses
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s,
                CASE WHEN %s = 'SENT' THEN %s ELSE NULL END,
                %s, %s, %s
            )
            ON CONFLICT (thread_id) DO UPDATE SET
                company = COALESCE(applications.company, EXCLUDED.company),
                position = COALESCE(applications.position, EXCLUDED.position),
                status = CASE
                    WHEN applications.status IN ('INTERVIEW', 'REJECTED') AND EXCLUDED.status = 'IN_REVIEW'
                    THEN applications.status
                    ELSE EXCLUDED.status
                END,
                last_email_id = EXCLUDED.last_email_id,
                confidence = EXCLUDED.confidence,
                related_addresses = (
                    SELECT ARRAY(
                        SELECT DISTINCT unnest(
                            COALESCE(applications.related_addresses, '{}') || COALESCE(EXCLUDED.related_addresses, '{}')
                        )
                    )
                ),
                updated_at = NOW()
            RETURNING id
        """, (
            thread_id, company, position, email.get("sent_at"), status, confidence,
            role, email["id"], email["id"], source, [email_address(a) for a in addresses if a],
        ))
        row = cur.fetchone()
        app_id = row["id"]

    link_email(conn, app_id, email["id"], role, addresses=addresses)
    logger.info("Candidature #%s créée/MAJ : %s / %s → %s (Source extraction: Company=%s, Position=%s)",
                app_id, company, position or "?", status, company_src, position_src)
    return app_id


def update_application_status(conn, app, email, status, confidence, role, company, position, company_src, position_src):
    new_status = status
    if app["status"] in ("INTERVIEW", "REJECTED") and status == "IN_REVIEW":
        new_status = app["status"]

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE applications
            SET status = %s,
                company = COALESCE(company, %s),
                position = COALESCE(position, %s),
                confidence = %s,
                last_email_id = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (new_status, company, position, confidence, email["id"], app["id"]))

    addresses = [email.get("sender") or email.get("recipient")]
    link_email(conn, app["id"], email["id"], role, addresses=addresses)

    insert_processing_event(conn, email["id"], "APPLICATION_STATUS_UPDATED", {
        "application_id": app["id"],
        "old_status": app["status"],
        "new_status": new_status,
        "company": company,
        "position": position,
        "company_source": company_src,
        "position_source": position_src,
        "confidence": confidence,
    })


def expire_stale_applications(conn):
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            UPDATE applications
            SET status = 'REJECTED', updated_at = NOW()
            WHERE status = 'IN_REVIEW'
              AND updated_at < NOW() - make_interval(days => %s)
            RETURNING id, company, position
        """, (STALE_IN_REVIEW_DAYS,))
        rows = cur.fetchall()

    for row in rows:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO processing_events (email_id, event_type, details)
                VALUES (NULL, 'APPLICATION_STALE_REJECTED', %s)
            """, (psycopg.types.json.Jsonb({
                "application_id": row["id"],
                "company": row["company"],
                "position": row["position"],
                "stale_days": STALE_IN_REVIEW_DAYS,
            }),))


# ---------------------------------------------------------
# Traitement des e-mails
# ---------------------------------------------------------
def process_sent_email(conn, email):
    label, confidence = classify_sent(email)

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE emails
            SET classification = %s, confidence = %s, processed = TRUE
            WHERE id = %s
        """, (label, confidence, email["id"]))

    if label != "JOB_APPLICATION" or confidence < MIN_CONFIDENCE:
        insert_processing_event(conn, email["id"], "SENT_EMAIL_CLASSIFIED", {
            "classification": label,
            "confidence": confidence,
            "application_created": False,
        })
        return

    # Nettoyage avant extraction
    subject, body = clean_for_extraction(email.get("subject"), email.get("body"))

    company, position, company_src, position_src = extract_company_and_position(
        email.get("recipient"), subject, body
    )
    # ... le reste de la fonction ne change pas

    if not company:
        insert_processing_event(conn, email["id"], "NEEDS_MANUAL_REVIEW", {
            "classification": label,
            "confidence": confidence,
            "reason": "Entreprise impossible à déterminer sur email envoyé.",
        })
        return

    existing = find_matching_application(
        conn, company, position, address=email.get("recipient")
    )

    if existing:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE applications
                SET company = COALESCE(company, %s),
                    position = COALESCE(position, %s),
                    sent_email_id = COALESCE(sent_email_id, %s),
                    source = CASE WHEN source IN ('WEBSITE_ASSUMED', 'UNKNOWN') THEN 'EMAIL' ELSE source END,
                    status = CASE WHEN status IN ('INTERVIEW', 'REJECTED') THEN status ELSE 'IN_REVIEW' END,
                    updated_at = NOW()
                WHERE id = %s
            """, (company, position, email["id"], existing["id"]))
        link_email(conn, existing["id"], email["id"], "SENT", addresses=[email.get("recipient")])
        insert_processing_event(conn, email["id"], "APPLICATION_FROM_SENT_EMAIL", {
            "application_id": existing["id"],
            "company": company,
            "position": position,
            "company_source": company_src,
            "position_source": position_src,
            "confidence": confidence,
        })
    else:
        create_application(
            conn, email, company, position, "IN_REVIEW", confidence, "EMAIL", "SENT", company_src, position_src
        )
        insert_processing_event(conn, email["id"], "APPLICATION_FROM_SENT_EMAIL", {
            "company": company,
            "position": position,
            "company_source": company_src,
            "position_source": position_src,
            "confidence": confidence,
            "status": "IN_REVIEW",
        })


STATUS_BY_LABEL = {
    "IN_REVIEW": "IN_REVIEW",
    "REJECTION": "REJECTED",
    "INTERVIEW": "INTERVIEW",
}


def process_received_email(conn, email):
    label, confidence = classify_received(email)

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE emails
            SET classification = %s, confidence = %s, processed = TRUE
            WHERE id = %s
        """, (label, confidence, email["id"]))

    target_status = STATUS_BY_LABEL.get(label)
    role = ROLE_BY_LABEL.get(label, "OTHER")

    if not target_status:
        insert_processing_event(conn, email["id"], "RECEIVED_EMAIL_CLASSIFIED", {
            "classification": label,
            "confidence": confidence,
            "application_updated": False,
            "reason": "Email non lié à une étape de candidature.",
        })
        return

    min_for_action = 0.70 if label in ("REJECTION", "INTERVIEW", "IN_REVIEW") else MIN_CONFIDENCE
    if confidence < min_for_action:
        event_type = "NEEDS_MANUAL_REVIEW"
        reason = "Confiance insuffisante (< 0.70)."
        insert_processing_event(conn, email["id"], event_type, {
            "classification": label,
            "confidence": confidence,
            "reason": reason,
        })
        return

    # Nettoyage avant extraction
    subject, body = clean_for_extraction(email.get("subject"), email.get("body"))

    company, position, company_src, position_src = extract_company_and_position(
        email.get("sender"), subject, body
    )
    # ... le reste de la fonction ne change pas

    if not company:
        insert_processing_event(conn, email["id"], "NEEDS_MANUAL_REVIEW", {
            "classification": label,
            "confidence": confidence,
            "reason": "Entreprise impossible à identifier sur email reçu.",
            "sender": email.get("sender"),
            "subject": email.get("subject"),
        })
        return

    if label == "REJECTION":
        apply_rejection(conn, email, company, position, confidence, company_src, position_src)
        return

    existing = find_matching_application(
        conn, company, position, address=email.get("sender")
    )

    if existing:
        update_application_status(
            conn, existing, email, target_status, confidence, role, company, position, company_src, position_src
        )
    else:
        create_application(
            conn, email, company, position, target_status, confidence, "WEBSITE_ASSUMED", role, company_src, position_src
        )
        insert_processing_event(conn, email["id"], "APPLICATION_CREATED_FROM_RECEIVED_EMAIL", {
            "company": company,
            "position": position,
            "company_source": company_src,
            "position_source": position_src,
            "status": target_status,
            "source": "WEBSITE_ASSUMED",
            "confidence": confidence,
        })


def process_email(conn, email):
    if email["direction"] == "SENT":
        process_sent_email(conn, email)
    elif email["direction"] == "RECEIVED":
        process_received_email(conn, email)
    else:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE emails
                SET classification = 'OTHER', confidence = 0.0, processed = TRUE
                WHERE id = %s
            """, (email["id"],))


def main():
    load_models()
    while True:
        try:
            with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
                with conn.transaction():
                    expire_stale_applications(conn)
                    consolidate_duplicate_applications(conn)

                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, gmail_id, thread_id, direction,
                               sender, recipient, subject, body, sent_at
                        FROM emails
                        WHERE processed = FALSE
                        ORDER BY id ASC
                        LIMIT %s
                        FOR UPDATE SKIP LOCKED
                    """, (BATCH_SIZE,))
                    emails = cur.fetchall()

                if not emails:
                    time.sleep(POLL_INTERVAL)
                    continue

                for email in emails:
                    try:
                        with conn.transaction():
                            process_email(conn, email)
                    except Exception:
                        logger.exception("Erreur email id=%s", email["id"])
        except Exception:
            logger.exception("Erreur boucle worker")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()