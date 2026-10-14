"""Rule-based (regex) classification for received emails."""

from __future__ import annotations

import re

from text_cleaning import clean_for_extraction, normalize


def heuristic_classification(
    subject: str | None, body: str | None
) -> tuple[str, float] | None:
    subject, body = clean_for_extraction(subject, body)
    text = f"{subject or ''}\n{body or ''}"
    normalized = normalize(text)

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
        if re.search(
            r"\b(?:ne|n')\b.{0,80}\b(?:donner suite|retenu|retenue|poursuivre)\b",
            normalized,
        ):
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

    if re.search(
        r"camscanner|scan_\d+|document scanned|verification code|one-time code|otp",
        normalized,
    ):
        return "OTHER", 0.95
    if re.search(
        r"\b(?:job alert|alerte emploi|newsletter|webinar|unsubscribe|désinscription|"
        r"free-work|tanitjobs|dernières opportunités|nouvelles offres)\b",
        normalized,
    ):
        return "OTHER", 0.92

    return None
