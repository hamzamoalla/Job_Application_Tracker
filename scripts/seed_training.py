import os
import psycopg

DB = os.getenv(
    "DATABASE_URL",
    "postgresql://jobtracker:jobtracker@localhost:5432/jobtracker"
)

APPLICATIONS = [
    ("I would like to apply for the Python Developer position. Please find attached my CV.", "JOB_APPLICATION"),
    ("I am writing to apply for the Software Engineer position.", "JOB_APPLICATION"),
    ("Please find attached my resume for the DevOps Engineer vacancy.", "JOB_APPLICATION"),
    ("I would like to submit my application for this position.", "JOB_APPLICATION"),
    ("Candidature au poste de développeur Python. Vous trouverez mon CV en pièce jointe.", "JOB_APPLICATION"),
    ("Je souhaite vous adresser ma candidature pour le poste proposé.", "JOB_APPLICATION"),
    ("Application – Cloud DevOps Engineer – Hamza Moalla", "JOB_APPLICATION"),
    ("Candidature spontanée – Ingénieur informatique", "JOB_APPLICATION"),
    ("Thank you for your message regarding our meeting tomorrow.", "OTHER"),
    ("Please find the project report attached.", "OTHER"),
    ("Can we schedule a meeting next week?", "OTHER"),
    ("Here is the information you requested.", "OTHER"),
    ("The deployment has been completed successfully.", "OTHER"),
    ("Please review the attached document.", "OTHER"),
    ("Happy birthday and have a great day!", "OTHER"),
    ("Reminder: the team meeting starts at 10.", "OTHER"),
]

REPLIES = [
    ("Unfortunately, we have decided to move forward with another candidate.", "REJECTION"),
    ("We regret to inform you that your application was not selected.", "REJECTION"),
    ("After careful consideration, we will not be proceeding with your application.", "REJECTION"),
    ("Thank you for your interest, but we have chosen another candidate.", "REJECTION"),
    ("Nous regrettons de vous informer que votre candidature n'a pas été retenue.", "REJECTION"),
    ("Votre candidature n'a malheureusement pas été retenue.", "REJECTION"),

    ("We would like to invite you to a technical interview.", "INTERVIEW"),
    ("Your profile has been shortlisted. Are you available for an interview?", "INTERVIEW"),
    ("We would like to schedule an interview with you.", "INTERVIEW"),
    ("Congratulations, you have been selected for the next step of our process.", "INTERVIEW"),
    ("Nous souhaitons vous inviter à un entretien technique.", "INTERVIEW"),
    ("Votre profil a retenu notre attention et nous souhaitons échanger avec vous.", "INTERVIEW"),

    ("We are currently reviewing your application and will get back to you.", "IN_REVIEW"),
    ("Your application is still under consideration.", "IN_REVIEW"),
    ("We have received your application and are reviewing your profile.", "IN_REVIEW"),
    ("Nous étudions actuellement votre candidature.", "IN_REVIEW"),
    ("Nous reviendrons vers vous dès que possible concernant votre candidature.", "IN_REVIEW"),

    ("Thank you for your email.", "OTHER"),
    ("Thank you for contacting us.", "OTHER"),
    ("We have received your message.", "OTHER"),
    ("Please contact our HR department for more information.", "OTHER"),
]


def insert(task, examples):
    with psycopg.connect(DB) as c:
        for text, label in examples:
            c.execute("""
                INSERT INTO training_examples(task, text, label)
                VALUES (%s,%s,%s)
            """, (task, text, label))


if __name__ == "__main__":
    insert("APPLICATION", APPLICATIONS)
    insert("REPLY", REPLIES)
    print("Seed data inserted.")
