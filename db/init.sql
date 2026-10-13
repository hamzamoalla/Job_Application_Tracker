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
-- 2. DONNÉES D'ENTRAÎNEMENT (complètes)
-- ============================================================

INSERT INTO training_examples (task, label, text)
SELECT v.task, v.label, v.text
FROM (VALUES

-- ===================== REPLY / INTERVIEW =====================
('REPLY', 'INTERVIEW', 'We would like to arrange a first interview with you. Please let us know your availability.'),
('REPLY', 'INTERVIEW', 'Could you attend a video interview on Tuesday at 10:00?'),
('REPLY', 'INTERVIEW', 'Following our review, we would like to meet you to discuss your application.'),
('REPLY', 'INTERVIEW', 'You are invited to an interview with our recruitment team.'),
('REPLY', 'INTERVIEW', 'Please choose an available time slot for a conversation with the hiring manager.'),
('REPLY', 'INTERVIEW', 'Your application has been shortlisted and we would like to schedule a call.'),
('REPLY', 'INTERVIEW', 'Nous aimerions organiser un premier entretien avec vous. Quelles sont vos disponibilités ?'),
('REPLY', 'INTERVIEW', 'Seriez-vous disponible pour un entretien en visioconférence la semaine prochaine ?'),
('REPLY', 'INTERVIEW', 'Nous souhaitons vous rencontrer afin de discuter de votre parcours et du poste.'),
('REPLY', 'INTERVIEW', 'Votre candidature a été présélectionnée. Merci de nous communiquer vos disponibilités.'),
('REPLY', 'INTERVIEW', 'We would like to invite you to the next stage of our recruitment process: a technical assessment and interview.'),
('REPLY', 'INTERVIEW', 'Please confirm whether you can attend the interview scheduled for Thursday.'),
('REPLY', 'INTERVIEW', 'We would like to invite you to a first interview. Please let us know your availability for next week.'),
('REPLY', 'INTERVIEW', 'Congratulations, your application has been shortlisted. We would like to schedule a video interview.'),
('REPLY', 'INTERVIEW', 'You are invited to take part in the next stage of our recruitment process: a technical interview.'),
('REPLY', 'INTERVIEW', 'We were impressed by your profile and would like to meet you for an interview.'),
('REPLY', 'INTERVIEW', 'Please choose a time slot for a conversation with the hiring manager.'),
('REPLY', 'INTERVIEW', 'Nous aimerions vous rencontrer pour un premier entretien. Quelles sont vos disponibilités ?'),
('REPLY', 'INTERVIEW', 'Votre candidature a été présélectionnée. Seriez-vous disponible pour un entretien en visioconférence ?'),
('REPLY', 'INTERVIEW', 'Nous souhaitons organiser un entretien technique avec vous. Merci de nous indiquer vos créneaux.'),
('REPLY', 'INTERVIEW', 'Convocation à un entretien pour le poste. Merci de confirmer votre présence.'),
('REPLY', 'INTERVIEW', 'Following our review, we would like to invite you to the next stage of the process.'),

-- ===================== REPLY / IN_REVIEW =====================
('REPLY', 'IN_REVIEW', 'This is to confirm that we have received your application. Our team will review it and contact you if there is a match.'),
('REPLY', 'IN_REVIEW', 'Thank you for applying. Your application has been successfully submitted and is being considered.'),
('REPLY', 'IN_REVIEW', 'Your profile is currently under review. We will update you when there is news.'),
('REPLY', 'IN_REVIEW', 'We have received your CV for the advertised position. The recruitment team will review your details.'),
('REPLY', 'IN_REVIEW', 'Your application is being assessed by the hiring team.'),
('REPLY', 'IN_REVIEW', 'We are still considering candidates and have not made a final decision yet.'),
('REPLY', 'IN_REVIEW', 'Nous accusons réception de votre candidature et allons l’examiner avec attention.'),
('REPLY', 'IN_REVIEW', 'Votre dossier est en cours d’étude. Nous vous tiendrons informé de la suite du processus.'),
('REPLY', 'IN_REVIEW', 'Nous avons bien reçu votre CV pour le poste proposé. Notre équipe reviendra vers vous.'),
('REPLY', 'IN_REVIEW', 'Votre candidature est toujours à l’étude et aucune décision définitive n’a été prise.'),
('REPLY', 'IN_REVIEW', 'Thank you for your interest in the role. We will contact shortlisted candidates after reviewing applications.'),
('REPLY', 'IN_REVIEW', 'Your application has been forwarded to the relevant department for consideration.'),
('REPLY', 'IN_REVIEW', 'Thank you for applying to our company. We have received your application and it is currently under review.'),
('REPLY', 'IN_REVIEW', 'This email confirms that we have successfully received your application for the position.'),
('REPLY', 'IN_REVIEW', 'Your application has been submitted and is being reviewed by our recruitment team.'),
('REPLY', 'IN_REVIEW', 'We have received your CV. Our hiring team will review your profile and contact you if there is a match.'),
('REPLY', 'IN_REVIEW', 'Thank you for your interest. Your application is now being considered.'),
('REPLY', 'IN_REVIEW', 'Your application has been forwarded to the relevant hiring manager for review.'),
('REPLY', 'IN_REVIEW', 'We confirm receipt of your application. You will be contacted if you are shortlisted.'),
('REPLY', 'IN_REVIEW', 'Application received. Our team is currently reviewing all applications.'),
('REPLY', 'IN_REVIEW', 'Nous avons bien reçu votre candidature et allons l''examiner avec attention.'),
('REPLY', 'IN_REVIEW', 'Votre candidature a bien été enregistrée. Elle est actuellement en cours d''étude.'),
('REPLY', 'IN_REVIEW', 'Accusé de réception de votre candidature. Notre équipe reviendra vers vous si votre profil correspond.'),
('REPLY', 'IN_REVIEW', 'Nous accusons réception de votre dossier. Il est en cours d''analyse par l''équipe recrutement.'),
('REPLY', 'IN_REVIEW', 'Merci pour votre candidature. Elle a été transmise au responsable du recrutement.'),
('REPLY', 'IN_REVIEW', 'Votre dossier est bien arrivé et est en cours d''examen.'),
('REPLY', 'IN_REVIEW', 'Thank you for applying to Redwood Materials. We have received your application.'),
('REPLY', 'IN_REVIEW', 'Thank you for applying to DXC Technology for the position of AI / ML Engineer.'),
('REPLY', 'IN_REVIEW', '¡Gracias por tu interés en REVEL! Hemos recibido tu candidatura.'),
('REPLY', 'IN_REVIEW', 'Your application at Proximus Luxembourg has been received and is under review.'),

-- ===================== REPLY / REJECTION =====================
('REPLY', 'REJECTION', 'After reviewing your profile, we have decided not to proceed with your application.'),
('REPLY', 'REJECTION', 'We appreciate your interest, but we will not be inviting you to the next stage.'),
('REPLY', 'REJECTION', 'Unfortunately, you have not been selected for this position.'),
('REPLY', 'REJECTION', 'We have decided to continue the recruitment process with other candidates.'),
('REPLY', 'REJECTION', 'The position has been filled, so we cannot move forward with your application.'),
('REPLY', 'REJECTION', 'We will not be progressing your application on this occasion.'),
('REPLY', 'REJECTION', 'Après étude de votre candidature, nous ne donnerons pas suite à votre demande.'),
('REPLY', 'REJECTION', 'Nous avons choisi de poursuivre le processus avec d’autres candidats.'),
('REPLY', 'REJECTION', 'Malheureusement, votre profil n’a pas été retenu pour ce poste.'),
('REPLY', 'REJECTION', 'Le poste ayant été pourvu, nous ne pouvons pas donner une suite favorable à votre candidature.'),
('REPLY', 'REJECTION', 'Nous vous remercions de votre intérêt, mais nous ne retenons pas votre candidature.'),
('REPLY', 'REJECTION', 'We regret to let you know that you will not be moving forward in the selection process.'),
('REPLY', 'REJECTION', 'After careful consideration, we have decided not to move forward with your application for this position.'),
('REPLY', 'REJECTION', 'We regret to inform you that your application has not been successful on this occasion.'),
('REPLY', 'REJECTION', 'Unfortunately, we will not be progressing your application any further.'),
('REPLY', 'REJECTION', 'Thank you for your interest. We have chosen to proceed with other candidates whose profiles more closely match our requirements.'),
('REPLY', 'REJECTION', 'We have filled the position and will not be moving forward with your candidacy.'),
('REPLY', 'REJECTION', 'After reviewing your application, we have decided that we will not be inviting you to interview.'),
('REPLY', 'REJECTION', 'We appreciate the time you took to apply. Unfortunately your profile was not selected for the next stage.'),
('REPLY', 'REJECTION', 'Your application was carefully reviewed. We will not be proceeding with your candidature.'),
('REPLY', 'REJECTION', 'Malheureusement, votre candidature n''a pas été retenue pour ce poste.'),
('REPLY', 'REJECTION', 'Après étude attentive de votre dossier, nous ne donnerons pas suite à votre candidature.'),
('REPLY', 'REJECTION', 'Nous vous remercions pour l''intérêt que vous nous avez porté. Votre profil n''a pas été retenu.'),
('REPLY', 'REJECTION', 'Le poste ayant été pourvu, nous ne pouvons donner une suite favorable à votre candidature.'),
('REPLY', 'REJECTION', 'Nous avons décidé de poursuivre le processus de recrutement avec d''autres candidats.'),
('REPLY', 'REJECTION', 'Suite à l''examen de votre candidature, nous ne souhaitons pas donner suite.'),
('REPLY', 'REJECTION', 'Malgré l''intérêt de votre parcours, nous ne retenons pas votre candidature pour ce poste.'),
('REPLY', 'REJECTION', 'Petit retour sur ta candidature : malheureusement on ne va pas pouvoir donner suite.'),
('REPLY', 'REJECTION', 'Response to your job application: after review we will not be moving forward.'),
('REPLY', 'REJECTION', 'Your Job Application | We have decided not to proceed with your application.'),

-- ===================== REPLY / OTHER =====================
('REPLY', 'OTHER', 'Your one-time verification code is 482913. Do not share this code with anyone.'),
('REPLY', 'OTHER', 'Your verification code is valid for the next ten minutes.'),
('REPLY', 'OTHER', 'Your weekly job alert: new Python and DevOps vacancies match your preferences.'),
('REPLY', 'OTHER', 'Here are the latest job offers selected for you. Manage your job alert preferences here.'),
('REPLY', 'OTHER', 'This is the monthly newsletter with product updates, events, and articles.'),
('REPLY', 'OTHER', 'Register now for our upcoming webinar on cloud technologies.'),
('REPLY', 'OTHER', 'Discover our latest articles, tutorials, and upcoming online sessions.'),
('REPLY', 'OTHER', 'Your account security code is below. If you did not request it, you can ignore this email.'),
('REPLY', 'OTHER', 'Please confirm your email address to activate your account.'),
('REPLY', 'OTHER', 'Thank you for subscribing to our newsletter.'),
('REPLY', 'OTHER', 'Voici votre alerte emploi : de nouvelles offres correspondent à vos critères de recherche.'),
('REPLY', 'OTHER', 'Découvrez les actualités de notre plateforme et les prochains événements.'),
('REPLY', 'OTHER', 'Votre code de vérification est 482913. Ne le communiquez à personne.'),
('REPLY', 'OTHER', 'Confirmez votre adresse e-mail pour activer votre compte.'),
('REPLY', 'OTHER', 'Thank you for contacting support. Your support request has been registered under ticket number 12345.'),
('REPLY', 'OTHER', 'We have received your message and forwarded it to the appropriate department.'),
('REPLY', 'OTHER', 'Your subscription has been renewed successfully.'),
('REPLY', 'OTHER', 'This is an automated notification about a new feature release.'),
('REPLY', 'OTHER', 'Votre inscription à notre newsletter a bien été prise en compte.'),
('REPLY', 'OTHER', 'Nous avons bien reçu votre demande de support. Un conseiller vous répondra prochainement.'),
('REPLY', 'OTHER', 'Your verification code is 847291. This code will expire in 10 minutes.'),
('REPLY', 'OTHER', 'Here is your one-time password. Do not share it with anyone.'),
('REPLY', 'OTHER', 'Your weekly job alert: 12 new offers match your criteria.'),
('REPLY', 'OTHER', 'Tanitjobs.com: Alerte Emploi - Nouvelles offres correspondant à votre recherche.'),
('REPLY', 'OTHER', 'Discover our latest newsletter with product updates and upcoming webinars.'),
('REPLY', 'OTHER', 'Please confirm your email address by clicking the link below.'),
('REPLY', 'OTHER', 'Your subscription has been successfully renewed.'),
('REPLY', 'OTHER', 'This is an automated message regarding your account security.'),
('REPLY', 'OTHER', 'Dernières opportunités sur Free-Work ! Consultez les nouvelles offres.'),
('REPLY', 'OTHER', 'Is coding still worth it? Join our free live session this week.'),
('REPLY', 'OTHER', 'Lens Extensions are back, and AI builds them.'),
('REPLY', 'OTHER', 'Get more out of OpenAI, in 3 free live sessions.'),
('REPLY', 'OTHER', 'Infolettre aux scientifiques - Octobre 2026'),
('REPLY', 'OTHER', 'The best way to learn AI? Practice it yourself.'),
('REPLY', 'OTHER', 'Les 8 et 9 octobre : 6ᵉ édition du Salon RDV Emploi.'),

-- ===================== APPLICATION =====================
('APPLICATION', 'JOB_APPLICATION', 'Subject: Candidature spontanée – Ingénieur DevOps\nBody: Madame, Monsieur, Je me permets de vous adresser ma candidature spontanée pour un poste d''ingénieur DevOps au sein de votre entreprise.'),
('APPLICATION', 'JOB_APPLICATION', 'Subject: Application - Python Developer\nBody: Dear Hiring Manager, I am writing to apply for the Python Developer position. Please find attached my CV and cover letter.'),
('APPLICATION', 'JOB_APPLICATION', 'Subject: Candidature – Consultant SAP FICO\nBody: Bonjour, suite à votre offre d''emploi, je vous prie de trouver ci-joint mon CV pour le poste de Consultant SAP FICO.'),
('APPLICATION', 'JOB_APPLICATION', 'Subject: Job Application - DevOps Engineer\nBody: Hello, I would like to submit my application for the DevOps Engineer role. My resume is attached.'),
('APPLICATION', 'JOB_APPLICATION', 'Subject: Candidature spontanée – Développement, Automatisation & Intégration\nBody: Madame, Monsieur, Actuellement en recherche d''opportunités, je souhaite vous proposer ma candidature pour un poste en développement et automatisation.'),
('APPLICATION', 'OTHER', 'Subject: Re: Meeting tomorrow\nBody: Yes, I will be available at 10am. See you then.'),
('APPLICATION', 'OTHER', 'Subject: Invoice #4587\nBody: Please find attached the invoice for the services provided last month.'),
('APPLICATION', 'OTHER', 'Subject: Weekend plans\nBody: Are you free this Saturday for a coffee?'),
('APPLICATION', 'OTHER', 'Subject: Password reset\nBody: Click here to reset your password.'),
('APPLICATION', 'OTHER', 'Subject: Newsletter subscription\nBody: Thank you for subscribing to our newsletter.')

) AS v(task, label, text)
WHERE NOT EXISTS (
    SELECT 1
    FROM training_examples t
    WHERE t.task = v.task
      AND t.label = v.label
      AND t.text = v.text
);