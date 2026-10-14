"""Company & position extraction (regex + GLiNER + email domain)."""

from __future__ import annotations

import logging
import os
import re
from email.utils import parseaddr

from text_cleaning import normalize

logger = logging.getLogger(__name__)

JOB_KEYWORDS = {
    "developer", "engineer", "consultant", "analyst", "architect", "manager",
    "développeur", "ingénieur", "architecte", "stagiaire", "intern", "lead",
    "specialist", "spécialiste", "technician", "technicien", "administrator",
    "administrateur", "designer", "director", "directeur", "head", "officer",
    "consultante", "développeuse", "ingénieure", "expert", "data", "devops",
}

SECOND_LEVEL_SUFFIXES = {"com", "net", "org", "gov", "edu", "co", "or", "ac"}

IGNORED_DOMAINS = {
    "gmail", "yahoo", "outlook", "hotmail", "icloud", "protonmail", "mail",
    "noreply", "no-reply", "donotreply", "jobs", "careers", "hr", "recruitment",
    "talent", "apply", "workday", "greenhouse", "lever", "smartrecruiters",
    "indeed", "linkedin", "mailchimp", "sendgrid", "amazon", "google",
}

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

# Module-level GLiNER instance (set by main.load_models)
gliner_model = None


def is_job_title_like(text: str) -> bool:
    if not text:
        return False
    words = set(re.findall(r"\w+", text.lower()))
    return bool(words & JOB_KEYWORDS)


def is_candidate_current_employer(company: str, full_text: str) -> bool:
    if not company or not full_text:
        return False

    known = {
        e.strip().lower()
        for e in os.getenv("CURRENT_EMPLOYERS", "KPIT").split(",")
        if e.strip()
    }
    if company.lower() in known:
        logger.info("Entreprise '%s' ignorée (CURRENT_EMPLOYERS).", company)
        return True

    clean_text = re.sub(r"\s+", " ", full_text)
    escaped = re.escape(company)

    application_context = (
        r"(?i)\b(?:application|candidature|interest in|position|role|poste|"
        r"applying|applied)\b.{0,100}?\b(?:at|chez|with|for|auprès de)\s+"
        + escaped
    )
    if re.search(application_context, clean_text):
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
            logger.info("Entreprise '%s' ignorée (employeur actuel).", company)
            return True
    return False


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


def domain_company_from_email(address: str) -> str | None:
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


def extract_company_regex(subject: str, body: str) -> str | None:
    text = f"{subject or ''}\n{body or ''}"
    for pattern in COMPANY_PATTERNS:
        match = re.search(pattern, text)
        if match:
            name = clean_company_name(match.group(1))
            if len(name) >= 2 and not is_job_title_like(name):
                return name
    return None


def extract_position_regex(subject: str, body: str) -> str | None:
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


def extract_company_and_position(
    email_addr: str | None, subject: str | None, body: str | None
):
    company, company_src = None, None
    position, position_src = None, None
    full_text = f"{subject or ''}\n{body or ''}"

    c_reg = extract_company_regex(subject or "", body or "")
    if c_reg and not is_candidate_current_employer(c_reg, full_text):
        company, company_src = c_reg, "REGEX"

    p_reg = extract_position_regex(subject or "", body or "")
    if p_reg:
        position, position_src = p_reg, "REGEX"

    if not company or not position:
        gl_c, gl_p = extract_with_gliner(subject or "", body or "")
        if not company and gl_c:
            if not is_job_title_like(gl_c) and not is_candidate_current_employer(
                gl_c, full_text
            ):
                company, company_src = gl_c, "GLINER"
        if not position and gl_p:
            position, position_src = gl_p, "GLINER"

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
        company or "INCONNU",
        company_src or "NONE",
        position or "INCONNU",
        position_src or "NONE",
    )
    return company, position, company_src, position_src
