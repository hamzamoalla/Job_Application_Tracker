-- Additional examples for the job_application_tracker reply classifier.
-- Safe to rerun: exact task/label/text duplicates are skipped.
-- Existing examples are preserved.

INSERT INTO training_examples (task, label, text)
SELECT v.task, v.label, v.text
FROM (VALUES
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
    ('REPLY', 'OTHER', 'Nous avons bien reçu votre demande de support. Un conseiller vous répondra prochainement.')
) AS v(task, label, text)
WHERE NOT EXISTS (
    SELECT 1
    FROM training_examples t
    WHERE t.task = v.task
      AND t.label = v.label
      AND t.text = v.text
);

-- After importing these examples, retrain the models using the project's existing
-- trainer command. Do not assume old emails are reclassified automatically.
