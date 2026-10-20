-- Exemples réels (vérifiés à la main par Hamza) ajoutés au jeu
-- d'entraînement REPLY, en complément de db/training_examples.csv.
--
-- Ne fait PAS un TRUNCATE (contrairement à reset_training_examples.sql) :
-- c'est un ajout additif. ON CONFLICT DO NOTHING s'appuie sur la
-- contrainte UNIQUE(task, label, subject, text) ajoutée dans init.sql,
-- donc relancer ce script plusieurs fois est sans danger (pas de doublon).
--
-- Usage (depuis la racine du projet, conteneur postgres déjà démarré) :
--   docker compose cp db/add_real_examples.sql postgres:/tmp/add_real_examples.sql
--   docker exec -i job_application_tracker-postgres-1 \
--       psql -U jobtracker -d jobtracker -f /tmp/add_real_examples.sql
--
-- NOTE : task='REPLY' pour toutes ces lignes car ce sont des emails
-- REÇUS (recruteurs / ATS / newsletters), jamais du texte envoyé par
-- Hamza — donc jamais task='APPLICATION' (voir le fix de
-- routers/emails.py : task doit suivre la direction de l'email, pas le
-- label).
--
-- Dédupliqué à la main par rapport au fichier fourni : les templates
-- quasi-identiques (Quanthouse x2, much Consulting x2, much GmbH x2,
-- Proximus x2, Tanitjobs.com x10+, DataCamp/Grok promos...) n'ont
-- qu'une seule occurrence ici, pour ne pas fausser la cross-validation
-- avec des quasi-doublons. Les lignes clairement inutilisables (corps
-- vide/absurde, PDF CamScanner, "aaa"/"bbb") et les 4 emails
-- "Cognira Interview Schedule" (direction ambiguë dans les données
-- fournies) ont été exclus — à ajouter séparément si besoin une fois
-- la direction confirmée.

BEGIN;

INSERT INTO training_examples (task, label, subject, text) VALUES

-- ===================== REJECTION =====================
('REPLY', 'REJECTION',
 'Site Reliability Engineer (Guardicore AI Platform) - Remote 3497 at Akamai Technologies',
 'Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
Talent Acquisition
Akamai Technologies'),

('REPLY', 'REJECTION',
 'FIS Application Update - Hamza Moalla - JR0308866 Product Technical Support Analyst',
 'Dear Hamza,
Thank you for your time and interest in FIS. Unfortunately, given the timing of your application, your resume wasn''t reviewed prior to the hiring decision being made. We''re sorry that we missed you!
While you are not being considered further for this position, you may qualify for a number of our other posted positions. We invite you to join our Talent Network to receive job alerts with new job opportunities that match your interests.
We hope you''ll keep us in mind, and we encourage you to apply again!
We sincerely appreciate the time you invested in the application process and wish you every success in future endeavors.
Kind Regards,
FIS Talent Acquisition'),

('REPLY', 'REJECTION',
 'Your application at Proximus Luxembourg',
 'Dear Hamza MOALLA,
We thank you for showing interest in Proximus Luxembourg.
We have thoroughly examined your CV for the PAT Platform Developer - C position.
Unfortunately, your profile does not correspond to the needs we currently have. We regret that we cannot give a positive response to your application. Given these high numbers of applicants, we are afraid that we are not in a position to give detailed feedback to individual candidates.
In the meantime, we wish you the best in your professional life.
Sincerely,
Recruitment Team'),

('REPLY', 'REJECTION',
 'Response to your job application for Junior Business Analyst at Quanthouse',
 'Dear Hamza Moalla,
Thank you for your interest in QuantHouse Tunisia and for taking the time to apply for BA Junior position.
After careful consideration, we regret to inform you that we have decided to move forward with other candidates whose profiles more closely match our current requirements for this role.
We were nevertheless impressed by your background and would like to keep your profile in our database. Should a suitable opportunity matching your qualifications open up in the future, we will not hesitate to reach out to you.
We truly appreciate the time and effort you dedicated to your application and wish you every success in your job search and professional projects.
Best regards,
Dalia Hentati'),

('REPLY', 'REJECTION',
 'Your application for DevOps Engineer (m/w/d) - Cloud & Platform Engineering at My Project Box',
 'Hello Hamza,
Thank you for taking the time to apply for the DevOps Engineer (m/w/d) - Cloud & Platform Engineering position at My Project Box. After careful consideration, we regret to inform you that we will not be moving forward with your application at this time.
We truly appreciate the effort you put into applying and encourage you to stay connected with My Project Box for future opportunities.
We wish you all the best in your job search and future endeavors.
Sincerely,
My Project Box Recruiting Team'),

('REPLY', 'REJECTION',
 'Petit retour sur ta candidature SFEIR 🇱🇺',
 'Hello Hamza
Un grand merci pour ta candidature et pour l''intérêt que tu portes à SFEIR Luxembourg !
J''ai pris le temps d''étudier ta candidature et j''ai beaucoup apprécié ton parcours et tes projets !
Malheureusement, notre marché actuel ne correspond pas encore parfaitement à ton profil pour l''instant car il requiert un peu plus d''expérience post-étude,
Ce n''est en rien un jugement sur la qualité de ta candidature, bien au contraire ! Je garde ton profil en tête (et dans notre base) pour de futures opportunités, et je serais ravie de te recontacter le moment venu.
En attendant, on te souhaite plein de réussite dans ta recherche, et encore merci d''avoir pensé à nous !
Belle journée à toi'),

('REPLY', 'REJECTION',
 'Re:Your application at Alpitronic - DevOps Engineer (m/f/d) - hamza moalla',
 'Dear hamza,
thank you for your interest in Alpitronic.
We regret to inform you that you were not shortlisted for the open position of DevOps Engineer (m/f/d). The selection process is highly competitive, and we have decided to move forward with candidates whose qualifications better meet our needs at this time.
We hope that, despite this decision, you will continue to have a positive impression of our company and we would be pleased if you would continue to check our website for job vacancies.
We regret that we will not be able to follow up on your application and wish you all the best for your professional future.
Kind regards,
Team HR
Alpitronic GmbH | Srl'),

('REPLY', 'REJECTION',
 'Your Job Application | much. Consulting',
 'Dear Hamza Moalla,
Thank you again for applying for the Software Engineer PT position at much.
Unfortunately, we have to let you know that we will not proceed with your application. We wish you all the best in your job search and hope we will have the chance to consider you for another role in the future.
Any other application at much. Consulting is not affected by this refusal. We wish you all the best and good luck in your job search!
Best regards,
Duarte Gomes Viana
Managing Director'),

('REPLY', 'REJECTION',
 'hamza moalla and SingleStore',
 'Hi hamza,
Thank you for your interest in the Site Reliability Engineer role at SingleStore, and for the time you invested in getting to know us.
After reviewing your experience, we''ve decided not to move forward with your application for this role.
We know a hiring process asks something of you—time, preparation, and attention—and we''re grateful you chose to spend some of yours with us.
While this role wasn''t the right match, we''d be glad to keep the door open. Teams change, new challenges emerge, and another opportunity may bring our paths together again.
Wishing you all the best in what comes next.
Rhaysa Pereira'),

('REPLY', 'REJECTION',
 'Thank you',
 'Dear hamza,
Thank you for your interest in the Infrastructure Engineer II (Fixed-Term 24 months) position at LNDS. We are very sorry to inform you that other candidate profiles were deemed to be a better match for the criteria that have been defined for this position. Therefore, your application has not been selected for additional consideration at this time.
However, we would gladly consider your profile for future openings and invite you to regularly check our career page.
We thank you again for your consideration and interest in LNDS and wish you the best of luck in your job search.
Best regards,
Milica Lapcevic
Talent Acquisition Partner'),

('REPLY', 'REJECTION',
 'Thank you for interest in Ingénieur Développement -6012999408112026',
 'Hi Hamza,
Thank you for taking the time to apply for this role with ADP. We appreciate the time you''ve invested in this process.
While we were impressed with your experience, we have decided to move forward with other candidates.
We hope to connect again soon!
The ADP Talent Acquisition Team'),

-- ===================== IN_REVIEW =====================
('REPLY', 'IN_REVIEW',
 'Distribusion Technologies - Confirmation of your application',
 'Dear Hamza,
Thanks for your interest in Distribusion Technologies! Our mission as an organisation is to make ground transportation accessible. We enable global travel brands to connect seamlessly with hundreds of bus, airport transfer, train, and ferry providers.
Important Action Required: As you have applied via a different platform (Wellfound, Email, direct outreach, others), we need you to give us your GDPR consent in order to process your application in our Talent pool.
Thanks again for your interest in us!
Sincerely,
The Distribusion Technologies Talent Team'),

('REPLY', 'IN_REVIEW',
 'Thank you for applying to Redwood Materials',
 'Hi hamza,
Thank you for your interest in Redwood Materials! Your email has been received and we''re excited that you would consider joining our team.
Redwood''s goal is to develop and deploy new technologies for dramatically increasing the scope and scale of recycled and sustainable materials in global supply chains.
We will review your information as soon as we can and we''ll be in touch if your qualifications align with our needs. Due to the volume of emails received, we want to be respectful of your time and let you know that we will only be reaching out to candidates whose skillsets best match our roles.
Thanks,
Redwood Recruiting'),

('REPLY', 'IN_REVIEW',
 '¡Gracias por tu interés en REVEL! 🚀',
 '¡Hola, hamza!
¡Muchísimas gracias por tu interés en sumarte a REVEL! Te confirmamos que hemos recibido tu candidatura correctamente.
En los próximos días, nuestro equipo de People revisará con detalle tu perfil. Si vemos que tu experiencia se ajusta a lo que estamos buscando para esta posición, nos pondremos en contacto contigo para avanzar a la siguiente etapa del proceso.
Agradecemos mucho el tiempo dedicado a postularte.
¡Un saludo!
Beatriz de Las Heras
Drive Revel, S.L'),

('REPLY', 'IN_REVIEW',
 'Thank you for your application to My Project Box',
 'Hello Hamza,
Thank you for applying to the DevOps Engineer (m/w/d) - Cloud & Platform Engineering position at My Project Box. We appreciate your interest in joining our team. Our hiring team is reviewing your application and will be in touch soon to let you know about the next steps.
Thank you again for your interest in My Project Box.
Best regards,
My Project Box Recruiting Team'),

('REPLY', 'IN_REVIEW',
 'Thank you for applying to DXC Technology for the position of AI / ML Engineer (Agent Developer)',
 'Dear Hamza Moalla
Thank you for applying for the position of AI / ML Engineer (Agent Developer). A DXC Technology recruiter will review your candidate file and resume and contact you if your experience and qualifications match the requirements for the position.
Thank you again for your interest in employment with DXC Technology and best wishes for a successful job search.
Best regards,
DXC Technology Global Talent Acquisition'),

('REPLY', 'IN_REVIEW',
 'Thank you for applying to SingleStore!',
 'Hi hamza,
Thanks for applying to SingleStore. Your application is in, and our team will be taking a closer look.
If your experience lines up with what we''re looking for, someone from our Talent team will be in touch.
We''re glad you found us.
The SingleStore-LinkedIn Talent Team
This inbox isn''t monitored, so please don''t reply directly to this email.'),

('REPLY', 'IN_REVIEW',
 'We received your application for a position at much. GmbH',
 'Hi Hamza,
You have successfully submitted your application for this position: Junior Python Software Engineer (m/f/d)
Someone will review your qualifications shortly. Should your profile match our requirements, we will be in touch to schedule the next steps in the process.
Thank you for your interest in much. GmbH.
Sincerely,
much. GmbH'),

('REPLY', 'IN_REVIEW',
 'Prise de compte de votre candidature',
 'Bonjour hamza,
Nous avons bien reçu votre candidature et nous vous remercions de l''intérêt que vous portez à ADDINN Group.
Nous allons étudier votre dossier avec la plus grande attention et nous vous donnerons une réponse dans les brefs délais.
Si votre profil correspond à nos attentes, un membre de notre équipe entrera en contact avec vous.
Cependant, si vous n''avez pas de retour dans les trois semaines à compter d''aujourd''hui, veuillez noter que votre candidature a bien été gardée dans nos bases et sera réétudiée par d''éventuels futurs besoins.
Cordialement,
Equipe RH'),

('REPLY', 'IN_REVIEW',
 'Thank you for your application at Alpitronic',
 'Dear hamza,
thank you for your interest in the open position DevOps Engineer (m/f/d) at Alpitronic and for taking the initiative to apply.
We have received your application and will process it as soon as possible. Thank you for your patience.
In the meanwhile, we will be happy to answer any further questions regarding the open position or our application process you might have.
Best regards
Alpitronic GmbH | Srl'),

-- ===================== OTHER (REPLY, non liée au statut de candidature) =====================
('REPLY', 'OTHER',
 'Tanitjobs.com: Alerte Emploi',
 'Bonjour,
Voici les dernières offres d''emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Agent Commercial Comptoir
Assistant(e)
Responsable Maintenance
Ingénieur Génie Civil ou Architecte Senior
Si vous ne souhaitez plus recevoir d''alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L''équipe Tanitjobs.com'),

('REPLY', 'OTHER',
 'Hamza, 15 offres récentes proches de votre recherche',
 'Hello Hamza !
15 nouvelles offres s''approchent de vos recherches.
Alternance - Technicien Cloud - BTS S.I.O H/F
Product Manager Cloud - Socle et Plateforme H/F
Consultant·e Cloud Aws & DevOps H/F
Voir toutes les offres
À très vite dans vos recherches !
L''équipe Hellowork
Si vous ne souhaitez plus recevoir ce type d''e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.'),

('REPLY', 'OTHER',
 'Dernières opportunités sur Free-Work !',
 'Dernières offres d''emploi
CDI - AI Engineer - 💶 Jusqu''à 79k €/an - Île-de-France
CDI - Business Analyst - 💶 51k - 61k €/an - Paris
CDI - Responsable ERP - 💶 55k - 65k €/an - Toulouse
Découvrez les offres qui correspondent le mieux avec votre profil.
Bilan Q3 2026 : les métiers et technos qui ont vraiment recruté'),

('REPLY', 'OTHER',
 '[GitHub] Please verify your device',
 'Hey hamzamoalla!
A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.
Device: Chrome on Windows
Verification code: 289537
If you did not attempt to sign in to your account, your password may be compromised.
Thanks,
The GitHub Team'),

('REPLY', 'OTHER',
 'Here''s your verification code from ADP',
 'Verification code
051893
This code expires in 15 minutes.
Enter this code to access ADP services.
The email is sent from an automated system so please do not reply.
ADP and the ADP logo are trademarks of ADP, Inc.'),

('REPLY', 'OTHER',
 'Demande de renouvellement de la conservation de vos données personnelles',
 'Bonjour,
Afin de garantir une meilleure gestion des candidatures, dans le respect des règlementations applicables, Safran a mis à jour sa plateforme de recrutement et a uniformisé sa politique de protection des données personnelles des candidats.
Si vous souhaitez la suppression de votre compte, vous pouvez réaliser cette action sur votre espace candidat ou via ce lien.
L''administrateur de la plateforme de recrutement Safran'),

('REPLY', 'OTHER',
 'The skills that pay more, at half the price.',
 'Skill tracks that change what you''re worth, now at 50% off a month. Ends Thursday.
AI skills now command a 23% higher advertised salary. In comparison, a bachelor''s degree adds 8%. A master''s, 13%. Right now, the market pays more for the skill than for the degree.
Skill tracks help you build a salary premium through a guided, expert-curated curriculum.
Last days remaining at 50% off. After Thursday, it''s back to full price.
DataCamp'),

('REPLY', 'OTHER',
 'Get more out of OpenAI, in 3 free live sessions',
 'Oct 13-15. One registration unlocks everything.
You''ve asked ChatGPT plenty of questions. Next week we show you how to hand it a job instead.
Three live code-alongs, three working builds, and you keep each one. Free, and the recordings are yours if you miss one.
DataCamp'),

('REPLY', 'OTHER',
 'Ask Grok what''s happening now',
 'It checks the web and X before it answers.
Grok searches the web and X before it answers. Start with a topic, a draft, or a screenshot, then keep going in the same thread.
Catch up on a topic. Ask for the latest and get an answer with sources.
Sharpen a draft. Paste an email or a paragraph and ask what''s weak before you send it.
Ask Grok'),

('REPLY', 'OTHER',
 'Prêt pour AWS Cloud Solutions Architect ?',
 'Limited time! 3 months of Google AI Pro at no extra cost
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous. Vous êtes prêt à relever de nouveaux défis.
AWS Cloud Solutions Architect - Certificat Professionnel
Coursera'),

('REPLY', 'OTHER',
 '3 new courses: Azure AI-901, Amazon Bedrock and Grafana Loki',
 'Hi Hamza,
We''ve added three new courses in the last fortnight, covering Microsoft''s new AI-901 exam, building generative AI apps on Amazon Bedrock, and centralized logging on Kubernetes with Grafana Loki.
AI-901: Microsoft Azure AI Fundamentals
Introduction to Amazon Bedrock
Grafana Loki')

ON CONFLICT (task, label, subject, text) DO NOTHING;

COMMIT;

-- Résumé de contrôle après chargement.
SELECT task, label, COUNT(*) AS n
FROM training_examples
GROUP BY task, label
ORDER BY task, label;
