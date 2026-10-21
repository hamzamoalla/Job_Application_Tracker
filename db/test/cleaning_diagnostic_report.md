# Rapport diagnostic — nettoyage & chunking

- Emails analysés: **30**
- MAX_BODY_CHARS: `600`
- Chunking: `split_sentences` (min_words=4)

Pour chaque mail: brut → étapes de clean → final full/truncated → chunks.
Les ⚠️ signalent un comportement suspect (texte vidé, legal restant, trop de chunks).

---
## Email #1
**Subject:** Suppression de vos données personnelles
**label prédit/attendu:** `OTHER` · **confidence:** `0.657`

- Longueur brut: **718** car.
- Longueur full (après clean): **328** car.
- Longueur truncated (600): **328** car.
- Nombre de chunks (sentence): **2**

### Étapes de nettoyage
#### 0 — Body BRUT
*(718 caractères)*
```
Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
Cordialement,
L'administrateur de la plateforme de recrutement Safran
Vous recevez cet email car vous aviez créé un compte sur la plateforme de recrutement Safran.
Si vous souhaitez postuler à une de nos offres ou déposer une candidature spontanée, veuillez créer votre compte candidat via notre plateforme de recrutement.
Cette boite mail n'a pas vocation à recevoir les demandes d'emploi et de stage. Ces demandes ne seront donc pas traitées.
```

#### 1 — Après remove_invisible_chars
*(718 caractères)*
```
Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
Cordialement,
L'administrateur de la plateforme de recrutement Safran
Vous recevez cet email car vous aviez créé un compte sur la plateforme de recrutement Safran.
Si vous souhaitez postuler à une de nos offres ou déposer une candidature spontanée, veuillez créer votre compte candidat via notre plateforme de recrutement.
Cette boite mail n'a pas vocation à recevoir les demandes d'emploi et de stage. Ces demandes ne seront donc pas traitées.
```

#### 2 — Après clean_reply (citations)
*(718 caractères)*
```
Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
Cordialement,
L'administrateur de la plateforme de recrutement Safran
Vous recevez cet email car vous aviez créé un compte sur la plateforme de recrutement Safran.
Si vous souhaitez postuler à une de nos offres ou déposer une candidature spontanée, veuillez créer votre compte candidat via notre plateforme de recrutement.
Cette boite mail n'a pas vocation à recevoir les demandes d'emploi et de stage. Ces demandes ne seront donc pas traitées.
```

#### 3 — Après strip_trailing_signature_block
*(287 caractères)*
```
Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
Cordialement,
```

#### 4 — Après strip_boilerplate
*(273 caractères)*
```
Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
```

#### 5 — Après strip_urls
*(273 caractères)*
```
Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
```

#### 6 — FINAL full (Subject + Body) → chunking
*(328 caractères)*
```
Subject: Suppression de vos données personnelles
Body: Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(328 caractères)*
```
Subject: Suppression de vos données personnelles
Body: Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
```

### Chunks (split_sentences, min_words=4)
**chunk[1/2]** — 197 car., 31 mots
```
Subject: Suppression de vos données personnelles
Body: Bonjour,
Il y a 10 jours, nous vous avons sollicité pour vous demander le renouvellement de la conservation de vos données dans notre système.
```

**chunk[2/2]** — 130 car., 21 mots
```
Sans réponse de votre part, nous vous informons que nous avons procédé à la suppression de l'ensemble de vos données personnelles.
```

---

## Email #2
**Subject:** Votre candidature – DevOps Engineer (H/F)| 2N Solution
**label prédit/attendu:** `IN_REVIEW` · **confidence:** `0.940`

- Longueur brut: **572** car.
- Longueur full (après clean): **561** car.
- Longueur truncated (600): **561** car.
- Nombre de chunks (sentence): **3**

### Étapes de nettoyage
#### 0 — Body BRUT
*(572 caractères)*
```
Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 https://2nsolution.com/jobs
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
Cordialement,
L’équipe 2N Solution
© 2026 2N Solution
```

#### 1 — Après remove_invisible_chars
*(572 caractères)*
```
Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 https://2nsolution.com/jobs
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
Cordialement,
L’équipe 2N Solution
© 2026 2N Solution
```

#### 2 — Après clean_reply (citations)
*(572 caractères)*
```
Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 https://2nsolution.com/jobs
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
Cordialement,
L’équipe 2N Solution
© 2026 2N Solution
```

#### 3 — Après strip_trailing_signature_block
*(532 caractères)*
```
Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 https://2nsolution.com/jobs
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
Cordialement,
```

#### 4 — Après strip_boilerplate
*(518 caractères)*
```
Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 https://2nsolution.com/jobs
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
```

#### 5 — Après strip_urls
*(491 caractères)*
```
Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
```

#### 6 — FINAL full (Subject + Body) → chunking
*(561 caractères)*
```
Subject: Votre candidature – DevOps Engineer (H/F)| 2N Solution
Body: Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(561 caractères)*
```
Subject: Votre candidature – DevOps Engineer (H/F)| 2N Solution
Body: Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
```

### Chunks (split_sentences, min_words=4)
**chunk[1/3]** — 215 car., 33 mots
```
Subject: Votre candidature – DevOps Engineer (H/F)| 2N Solution
Body: Bonjour,
Nous avons bien reçu votre candidature pour le poste de DevOps Engineer (H/F) chez 2N Solution, suite à votre candidature sur Tanitjobs.
```

**chunk[2/3]** — 226 car., 35 mots
```
Afin de poursuivre le processus de recrutement, nous vous invitons à postuler directement sur notre plateforme via le lien suivant :
👉 
Merci de compléter votre candidature sur la plateforme afin que nous puissions l’examiner.
```

**chunk[3/3]** — 118 car., 19 mots
```
Nous vous remercions pour votre intérêt envers 2N Solution et vous souhaitons bonne chance pour la suite du processus.
```

---

## Email #3
**Subject:** Senior data pros are learning AI faster than juniors
**label prédit/attendu:** `OTHER` · **confidence:** `0.995`

- Longueur brut: **3004** car.
- Longueur full (après clean): **2447** car.
- Longueur truncated (600): **672** car.
- Nombre de chunks (sentence): **25**

### Alertes
- ℹ️  Beaucoup de chunks (25) — risque de dilution mean-pool

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp ( https://www.datacamp.com?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners. In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.

Both groups are learning AI. They're learning different parts of it.

We examined what each group studied over two 12-month windows. Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps. Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI. You'd assume the newest agentic tooling would be picked up by people newest to the field. It isn't. Claude Code 101 is studied more by experienced professionals than by people early in their careers.

Production work still falls to the people who've been doing it longest.

 

42% of senior data professionals started an AI course this year. Only 25% of juniors did. ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

 

That pattern doesn't hold in every role. Juniors are gaining ground in data science and AI/ML, where AI is already the work. In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead. Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.

Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking. This is the applied, judgment-heavy end of the work, and the end juniors are studying least.

Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.

Early in your AI skills journey? Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well. AI Funda […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp ( https://www.datacamp.com?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners. In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.

Both groups are learning AI. They're learning different parts of it.

We examined what each group studied over two 12-month windows. Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps. Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI. You'd assume the newest agentic tooling would be picked up by people newest to the field. It isn't. Claude Code 101 is studied more by experienced professionals than by people early in their careers.

Production work still falls to the people who've been doing it longest.

 

42% of senior data professionals started an AI course this year. Only 25% of juniors did. ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

 

That pattern doesn't hold in every role. Juniors are gaining ground in data science and AI/ML, where AI is already the work. In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead. Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.

Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking. This is the applied, judgment-heavy end of the work, and the end juniors are studying least.

Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.

Early in your AI skills journey? Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well. AI Funda […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp ( https://www.datacamp.com?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners. In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.

Both groups are learning AI. They're learning different parts of it.

We examined what each group studied over two 12-month windows. Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps. Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI. You'd assume the newest agentic tooling would be picked up by people newest to the field. It isn't. Claude Code 101 is studied more by experienced professionals than by people early in their careers.

Production work still falls to the people who've been doing it longest.

 

42% of senior data professionals started an AI course this year. Only 25% of juniors did. ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

 

That pattern doesn't hold in every role. Juniors are gaining ground in data science and AI/ML, where AI is already the work. In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead. Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.

Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking. This is the applied, judgment-heavy end of the work, and the end juniors are studying least.

Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.

Early in your AI skills journey? Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well. AI Funda […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp ( https://www.datacamp.com?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners. In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.

Both groups are learning AI. They're learning different parts of it.

We examined what each group studied over two 12-month windows. Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps. Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI. You'd assume the newest agentic tooling would be picked up by people newest to the field. It isn't. Claude Code 101 is studied more by experienced professionals than by people early in their careers.

Production work still falls to the people who've been doing it longest.

 

42% of senior data professionals started an AI course this year. Only 25% of juniors did. ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

 

That pattern doesn't hold in every role. Juniors are gaining ground in data science and AI/ML, where AI is already the work. In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead. Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.

Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking. This is the applied, judgment-heavy end of the work, and the end juniors are studying least.

Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.

Early in your AI skills journey? Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well. AI Funda […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp ( https://www.datacamp.com?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners. In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.

Both groups are learning AI. They're learning different parts of it.

We examined what each group studied over two 12-month windows. Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps. Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI. You'd assume the newest agentic tooling would be picked up by people newest to the field. It isn't. Claude Code 101 is studied more by experienced professionals than by people early in their careers.

Production work still falls to the people who've been doing it longest.

 

42% of senior data professionals started an AI course this year. Only 25% of juniors did. ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261020_1-senior-vs-junior-data-prof--na--engagement_2-mix_6-tier-2_8-emal-ci_11-weekly-news&dc_euid=20788339 )

 

That pattern doesn't hold in every role. Juniors are gaining ground in data science and AI/ML, where AI is already the work. In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead. Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.

Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking. This is the applied, judgment-heavy end of the work, and the end juniors are studying least.

Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.

Early in your AI skills journey? Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well. AI Funda […]
```

#### 5 — Après strip_urls
*(2379 caractères)*
```
Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp 

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now 

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners. In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.

Both groups are learning AI. They're learning different parts of it.

We examined what each group studied over two 12-month windows. Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps. Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI. You'd assume the newest agentic tooling would be picked up by people newest to the field. It isn't. Claude Code 101 is studied more by experienced professionals than by people early in their careers.

Production work still falls to the people who've been doing it longest.

 

42% of senior data professionals started an AI course this year. Only 25% of juniors did. 

 

That pattern doesn't hold in every role. Juniors are gaining ground in data science and AI/ML, where AI is already the work. In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead. Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.

Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking. This is the applied, judgment-heavy end of the work, and the end juniors are studying least.

Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.

Early in your AI skills journey? Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well. AI Funda […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(2447 caractères)*
```
Subject: Senior data pros are learning AI faster than juniors
Body: Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp 

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now 

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners. In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.

Both groups are learning AI. They're learning different parts of it.

We examined what each group studied over two 12-month windows. Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps. Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI. You'd assume the newest agentic tooling would be picked up by people newest to the field. It isn't. Claude Code 101 is studied more by experienced professionals than by people early in their careers.

Production work still falls to the people who've been doing it longest.

 

42% of senior data professionals started an AI course this year. Only 25% of juniors did. 

 

That pattern doesn't hold in every role. Juniors are gaining ground in data science and AI/ML, where AI is already the work. In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead. Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.

Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking. This is the applied, judgment-heavy end of the work, and the end juniors are studying least.

Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.

Early in your AI skills journey? Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well. AI Funda […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(672 caractères)*
```
Subject: Senior data pros are learning AI faster than juniors
Body: Our platform data revealed: Who’s learning what, and the one place juniors are ahead.

The Output by DataCamp 

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan! Save Now 

*****************************************************************************************
42% of senior data professionals started an AI course this year. Only 25% of juniors did.
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/25]** — 153 car., 25 mots
```
Subject: Senior data pros are learning AI faster than juniors
Body: Our platform data revealed: Who’s learning what, and the one place juniors are ahead.
```

**chunk[2/25]** — 125 car., 23 mots
```
The Output by DataCamp 

A weekly dispatch for AI + Data Practitioners · #018

Calendar

Flash Sale | 50% Off on Yearly Plan!
```

**chunk[3/25]** — 165 car., 14 mots
```
Save Now 

*****************************************************************************************
42% of senior data professionals started an AI course this year.
```

**chunk[4/25]** — 24 car., 5 mots
```
Only 25% of juniors did.
```

**chunk[5/25]** — 206 car., 19 mots
```
*****************************************************************************************

 

Four in ten senior data professionals started an AI course this year, against one in four early-career learners.
```

**chunk[6/25]** — 145 car., 24 mots
```
In AI and machine learning roles, juniors are moving faster: their adoption grew by 19.3 percentage points in a year, against 14.3 among seniors.
```

**chunk[7/25]** — 28 car., 5 mots
```
Both groups are learning AI.
```

**chunk[8/25]** — 39 car., 6 mots
```
They're learning different parts of it.
```

**chunk[9/25]** — 62 car., 10 mots
```
We examined what each group studied over two 12-month windows.
```

**chunk[10/25]** — 112 car., 15 mots
```
Early-career learners lean toward the building blocks: the OpenAI API, prompt engineering, Hugging Face, LLMOps.
```

**chunk[11/25]** — 114 car., 14 mots
```
Seniors prioritise the finished tools: Microsoft Copilot, scalable agentic systems, LangChain, and responsible AI.
```

**chunk[12/25]** — 89 car., 16 mots
```
You'd assume the newest agentic tooling would be picked up by people newest to the field.
```

**chunk[13/25]** — 99 car., 16 mots
```
Claude Code 101 is studied more by experienced professionals than by people early in their careers.
```

**chunk[14/25]** — 71 car., 12 mots
```
Production work still falls to the people who've been doing it longest.
```

**chunk[15/25]** — 64 car., 11 mots
```
42% of senior data professionals started an AI course this year.
```

**chunk[16/25]** — 24 car., 5 mots
```
Only 25% of juniors did.
```

**chunk[17/25]** — 40 car., 7 mots
```
That pattern doesn't hold in every role.
```

**chunk[18/25]** — 83 car., 15 mots
```
Juniors are gaining ground in data science and AI/ML, where AI is already the work.
```

**chunk[19/25]** — 124 car., 18 mots
```
In analytics, BI, and data engineering, where most early-career data people actually sit, seniors are pulling further ahead.
```

**chunk[20/25]** — 108 car., 20 mots
```
Data engineering shows the widest gap: seniors are now 2x more likely than juniors to be learning AI for it.
```

**chunk[21/25]** — 140 car., 22 mots
```
Separately, PwC finds the most AI-exposed entry-level roles are now 7x more likely to ask for skills like leadership and strategic thinking.
```

**chunk[22/25]** — 92 car., 16 mots
```
This is the applied, judgment-heavy end of the work, and the end juniors are studying least.
```

**chunk[23/25]** — 146 car., 24 mots
```
Put the two together, and the pattern is clear: employers are asking more of entry-level roles, and junior upskilling isn't keeping pace just yet.
```

**chunk[24/25]** — 32 car., 6 mots
```
Early in your AI skills journey?
```

**chunk[25/25]** — 99 car., 17 mots
```
Focus on the applied end: machine learning, LLMs, generative AI, and the judgment to use them well.
```

---

## Email #4
**Subject:** Alerte de sécurité
**label prédit/attendu:** `OTHER` · **confidence:** `0.962`

- Longueur brut: **843** car.
- Longueur full (après clean): **641** car.
- Longueur truncated (600): **638** car.
- Nombre de chunks (sentence): **5**

### Étapes de nettoyage
#### 0 — Body BRUT
*(843 caractères)*
```
[image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<https://accounts.google.com/AccountChooser?Email=hamza.moalla@ensi-uma.tn&continue=https://myaccount.google.com/alert/nt/1792501639304?rfn%3D325%26rfnc%3D1%26eid%3D-1948001101565303025%26et%3D0>
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :
https://myaccount.google.com/notifications
Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

#### 1 — Après remove_invisible_chars
*(843 caractères)*
```
[image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<https://accounts.google.com/AccountChooser?Email=hamza.moalla@ensi-uma.tn&continue=https://myaccount.google.com/alert/nt/1792501639304?rfn%3D325%26rfnc%3D1%26eid%3D-1948001101565303025%26et%3D0>
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :
https://myaccount.google.com/notifications
Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

#### 2 — Après clean_reply (citations)
*(843 caractères)*
```
[image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<https://accounts.google.com/AccountChooser?Email=hamza.moalla@ensi-uma.tn&continue=https://myaccount.google.com/alert/nt/1792501639304?rfn%3D325%26rfnc%3D1%26eid%3D-1948001101565303025%26et%3D0>
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :
https://myaccount.google.com/notifications
Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

#### 3 — Après strip_trailing_signature_block
*(843 caractères)*
```
[image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<https://accounts.google.com/AccountChooser?Email=hamza.moalla@ensi-uma.tn&continue=https://myaccount.google.com/alert/nt/1792501639304?rfn%3D325%26rfnc%3D1%26eid%3D-1948001101565303025%26et%3D0>
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :
https://myaccount.google.com/notifications
Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

#### 4 — Après strip_boilerplate
*(843 caractères)*
```
[image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<https://accounts.google.com/AccountChooser?Email=hamza.moalla@ensi-uma.tn&continue=https://myaccount.google.com/alert/nt/1792501639304?rfn%3D325%26rfnc%3D1%26eid%3D-1948001101565303025%26et%3D0>
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :
https://myaccount.google.com/notifications
Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

#### 5 — Après strip_urls
*(607 caractères)*
```
[image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :

Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

#### 6 — FINAL full (Subject + Body) → chunking
*(641 caractères)*
```
Subject: Alerte de sécurité
Body: [image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :

Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(638 caractères)*
```
Subject: Alerte de sécurité
Body: [image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows. Si c'était vous, aucune action de votre part n'est requise. Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
Consulter l'activité
<
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :

Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 940 […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/5]** — 195 car., 26 mots
```
Subject: Alerte de sécurité
Body: [image: Google]
Nouvelle connexion depuis un Windows

hamza.moalla@ensi-uma.tn
Nous avons détecté une nouvelle connexion à votre compte Google depuis un
Windows.
```

**chunk[2/5]** — 59 car., 10 mots
```
Si c'était vous, aucune action de votre part n'est requise.
```

**chunk[3/5]** — 67 car., 11 mots
```
Dans
le cas contraire, nous vous aiderons à sécuriser votre compte.
```

**chunk[4/5]** — 242 car., 40 mots
```
Consulter l'activité
<
Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :

Cet e-mail vous a été envoyé pour vous informer de modifications
importantes apportées à votre compte et aux services Google que vous
utilisez.
```

**chunk[5/5]** — 74 car., 12 mots
```
© 2026 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
```

---

## Email #5
**Subject:** Tanitjobs.com: Alerte Emploi
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **1891** car.
- Longueur full (après clean): **1935** car.
- Longueur truncated (600): **648** car.
- Nombre de chunks (sentence): **1**

### Étapes de nettoyage
#### 0 — Body BRUT
*(1891 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 1 — Après remove_invisible_chars
*(1891 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 2 — Après clean_reply (citations)
*(1891 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 3 — Après strip_trailing_signature_block
*(1891 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 4 — Après strip_boilerplate
*(1891 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 5 — Après strip_urls
*(1891 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1935 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(648 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-n […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/1]** — 1935 car., 250 mots
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne
kairouan, Kairouan, Tunisie
Anonyme
Chargé(e) de Marketing Digital
Tunis, Tunis, Tunisie
HEXASTRA
Vendeur(se)
sfax, majida boulila
pom de commerce
Technicien PAO & Prépresse Polyvalent (H/F)
Charguia 1, Ariana, Tunis
SC
Technicien de Maintenance Industrielle (H)
Charguia 1, Ariana, Tunis
SC
Technicien de maintenance
Kelibia, Nabeul, Tunisie
Sgss
Responsable Showroom & Développement Commercial – Meubles sur Mesure
Soukra, Ariana, Tunisie
Société de promotion de meubles (Le Dix-neuvième)
Senior Graphic Designer
Les Berges du Lac 1, Tunis, Tunisie
Taniterra
Technicien production Teinture
Ksar Hellal, Monastir, Tunisie
SARTEX
Responsable Contrôle Qualité Confection
Monastir, Monastir, Tunisie
DM Confection
Responsable Magasin Confection
Sahline, Monastir, Tunisie
DM Confection
Technicien Maintenance
Mghira, Ben Arous, Tunisie
PLAST ALFIN
Chargé(e) d’Affaires B2B – Solutions d’Impression et de Personnalisation (H/F)
Charguia 1, Ariana, Tunis
SC
Conducteur(rice) de Machines d’Impression Numérique (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
Télétravail
Novalys Call
Repasseuse / Employée de pressing expérimentée
Bizerte, Bizerte, Tunisie
OPAPURE
Responsable Café-Pâtisserie 'Mall SFAX'
Mall Of Sfax., Sfax, Tunisie
IFF
Technico-commercial SAV – Informatique & Imprimantes à Cartes (H/F)
Charguia 1, Ariana, Tunis
SC
Téléconseillers(ères) / Télévendeurs(ses) expérimenté(e)s – 100 % TÉLÉTRAVAIL
100 % TÉLÉTRAVAIL
Novalys Call
Téléopérateur·trice BtoB — Secteur pharmaceutique (H/F)
Tunis, Tunis, Tunisie
NEXIPHARM
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

---

## Email #6
**Subject:** Hamza, 15 offres récentes proches de votre recherche
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **2157** car.
- Longueur full (après clean): **2225** car.
- Longueur truncated (600): **672** car.
- Nombre de chunks (sentence): **6**

### Étapes de nettoyage
#### 0 — Body BRUT
*(2157 caractères)*
```
Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches ! 👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

#### 1 — Après remove_invisible_chars
*(2157 caractères)*
```
Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches ! 👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

#### 2 — Après clean_reply (citations)
*(2157 caractères)*
```
Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches ! 👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

#### 3 — Après strip_trailing_signature_block
*(2157 caractères)*
```
Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches ! 👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

#### 4 — Après strip_boilerplate
*(2157 caractères)*
```
Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches ! 👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

#### 5 — Après strip_urls
*(2157 caractères)*
```
Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches ! 👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

#### 6 — FINAL full (Subject + Body) → chunking
*(2225 caractères)*
```
Subject: Hamza, 15 offres récentes proches de votre recherche
Body: Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches ! 👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(672 caractères)*
```
Subject: Hamza, 15 offres récentes proches de votre recherche
Body: Hello Hamza !
15 nouvelles offres
s'approchent de vos recherches.
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Ma […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/6]** — 81 car., 13 mots
```
Subject: Hamza, 15 offres récentes proches de votre recherche
Body: Hello Hamza !
```

**chunk[2/6]** — 51 car., 7 mots
```
15 nouvelles offres
s'approchent de vos recherches.
```

**chunk[3/6]** — 1553 car., 285 mots
```
Responsable Cloud Center Of Excellence Ccoe H/F
Ramery
Erquinghem-Lys - 59
CDI
65 000 - 75 000 € / an
Voir l’offre
Responsable Cloud et Cybersécurité H/F
Neyrial Informatique
Clermont-Ferrand - 63
CDI
40 000 - 60 000 € / an
Voir l’offre
Consultant Cloud Ops H/F
Devoteam France
Marcq-en-Barœul - 59
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
CDI
Voir l’offre
Consultant Cloud Aws - DevOps Landing Zone & Kubernetes H/F
Stabilis ITSuper recruteur
Lyon - 69
CDI
Voir l’offre
Manager - Senior Manager Cloud Business Transformation - Paris - Toulouse H/F
PwC France et Maghreb
Neuilly-sur-Seine - 92
CDI
Voir l’offre
Consultant Senior Openstack - Vmware H/F
Caveo Consulting
Lyon - 69
Freelance
Voir l’offre
Stage - Consultant Cloud & Data H/F
Talan
Paris - 75
Stage
Voir l’offre
Chef de Projet Cloud & DevOps H/F
Randstad Digital
Issy-les-Moulineaux - 92
CDI
Voir l’offre
Architecte Solutions Cloud & Iot H/F
Up Technologies
Isère - 38
CDI
Voir l’offre
Architecte Cloud & Data - Llm - IA Agentique H/F
Orange
Lannion - 22
CDI
Voir l’offre
Expert Cloud Azure - DevOps H/F
SOCASS - Société d'Assistance de Service et de Support
Toulouse - 31
CDI
35 000 - 40 000 € / an
Voir l’offre
Architecte Cloud - Openstack - Vmware H/F
Fokus
Lyon 9e - 69
Freelance
60 000 - 75 000 € / an
Voir l’offre
Ingénieur Linux H/F
AIS
Nantes - 44
CDI
40 000 - 48 000 € / an
Voir l’offre
Ingénieur Système Linux H/F
Talents Digital
Brest - 29
CDI
30 000 - 40 000 € / an
Voir l’offre
Voir toutes les offres
À très vite dans vos recherches !
```

**chunk[4/6]** — 220 car., 34 mots
```
👋
L'équipe Hellowork
Téléchargez notre application
Espace candidat
Aide et contact
CGU
Si vous ne souhaitez plus recevoir ce type d’e-mail de la part de Hellowork, vous pouvez modifier vos préférences ou vous désabonner.
```

**chunk[5/6]** — 214 car., 32 mots
```
Conformément au règlement général sur la protection des données à caractère personnel du 25 mai 2018, vous pouvez exercer vos droits d’accès, de suppression et de rectification aux informations qui vous concernent.
```

**chunk[6/6]** — 101 car., 18 mots
```
Hellowork.com est un service édité par Hellowork
Hellowork SASU • 2 rue de la Mabilais • 35000 RENNES
```

---

## Email #7
**Subject:** Prêt pour IBM Full Stack Software Developer ?
**label prédit/attendu:** `OTHER` · **confidence:** `0.989`

- Longueur brut: **1588** car.
- Longueur full (après clean): **1649** car.
- Longueur truncated (600): **665** car.
- Nombre de chunks (sentence): **11**

### Alertes
- ℹ️  Beaucoup de chunks (11) — risque de dilution mean-pool

### Étapes de nettoyage
#### 0 — Body BRUT
*(1588 caractères)*
```
✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur. Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement. Ne peut pas être cumulée avec d’autres offres. Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation. Annulez à tout moment dans les paramètres du compte.
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

#### 1 — Après remove_invisible_chars
*(1588 caractères)*
```
✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur. Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement. Ne peut pas être cumulée avec d’autres offres. Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation. Annulez à tout moment dans les paramètres du compte.
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

#### 2 — Après clean_reply (citations)
*(1588 caractères)*
```
✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur. Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement. Ne peut pas être cumulée avec d’autres offres. Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation. Annulez à tout moment dans les paramètres du compte.
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

#### 3 — Après strip_trailing_signature_block
*(1588 caractères)*
```
✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur. Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement. Ne peut pas être cumulée avec d’autres offres. Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation. Annulez à tout moment dans les paramètres du compte.
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

#### 4 — Après strip_boilerplate
*(1588 caractères)*
```
✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur. Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement. Ne peut pas être cumulée avec d’autres offres. Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation. Annulez à tout moment dans les paramètres du compte.
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

#### 5 — Après strip_urls
*(1588 caractères)*
```
✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur. Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement. Ne peut pas être cumulée avec d’autres offres. Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation. Annulez à tout moment dans les paramètres du compte.
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1649 caractères)*
```
Subject: Prêt pour IBM Full Stack Software Developer ?
Body: ✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur. Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement. Ne peut pas être cumulée avec d’autres offres. Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation. Annulez à tout moment dans les paramètres du compte.
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(665 caractères)*
```
Subject: Prêt pour IBM Full Stack Software Developer ?
Body: ✨ Limited time! 3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours. Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis. Trouvez les cours recommandés pour vous.
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/11]** — 54 car., 9 mots
```
Subject: Prêt pour IBM Full Stack Software Developer ?
```

**chunk[2/11]** — 21 car., 4 mots
```
Body: ✨ Limited time!
```

**chunk[3/11]** — 105 car., 21 mots
```
3 months of Google AI Pro at no extra cost
 
| Coursera
 
Découvrez plus de 10 000 cours pendant 7 jours.
```

**chunk[4/11]** — 90 car., 13 mots
```
Essayer gratuitement
Recommandations pour vous
Vous êtes prêt à relever de nouveaux défis.
```

**chunk[5/11]** — 40 car., 6 mots
```
Trouvez les cours recommandés pour vous.
```

**chunk[6/11]** — 766 car., 104 mots
```
Spécialisations et cours
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM Full Stack Software Developer
S’inscrire
Cours
IBM
Introduction to Software Engineering
S’inscrire
Certificat Professionnel · 15 cours · Offre des crédits universitaires
IBM
IBM DevOps and Software Engineering
S’inscrire
Cours
IBM
Application Development using Microservices and Serverless
S’inscrire
Spécialisation · 6 cours
IBM
Information Technology (IT) and Cloud Fundamentals
S’inscrire
Cours
IBM
Introduction to Cloud Computing
S’inscrire
Certificat Professionnel · 4 cours · Offre des crédits universitaires
Amazon Web Services
AWS Cloud Solutions Architect
S’inscrire
Voir le catalogue
Les essais gratuits Coursera Plus sont limités à un par utilisateur.
```

**chunk[7/11]** — 124 car., 22 mots
```
Une fois qu'un essai a été utilisé, il ne peut pas être activé à nouveau, mais vous pouvez toujours commencer un abonnement.
```

**chunk[8/11]** — 46 car., 8 mots
```
Ne peut pas être cumulée avec d’autres offres.
```

**chunk[9/11]** — 226 car., 37 mots
```
Si vous n'annulez pas pendant la période d'essai gratuit, vous serez facturé 59 $ USD ou l'équivalent en devise locale (taxes applicables en sus) après l'essai gratuit de 7 jours et mensuellement par la suite, sauf annulation.
```

**chunk[10/11]** — 52 car., 9 mots
```
Annulez à tout moment dans les paramètres du compte.
```

**chunk[11/11]** — 115 car., 19 mots
```
Aide
Notification de confidentialité
Follow
Coursera | 2440 W El Camino Real 5th floor, Mountain View, CA 94040 USA
```

---

## Email #8
**Subject:** Tanitjobs.com: Alerte Emploi
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **349** car.
- Longueur full (après clean): **393** car.
- Longueur truncated (600): **393** car.
- Nombre de chunks (sentence): **1**

### Étapes de nettoyage
#### 0 — Body BRUT
*(349 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 1 — Après remove_invisible_chars
*(349 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 2 — Après clean_reply (citations)
*(349 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 3 — Après strip_trailing_signature_block
*(349 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 4 — Après strip_boilerplate
*(349 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 5 — Après strip_urls
*(349 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 6 — FINAL full (Subject + Body) → chunking
*(393 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(393 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

### Chunks (split_sentences, min_words=4)
**chunk[1/1]** — 393 car., 52 mots
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Chef de Ligne de Production
Kairouan, Kairouan, Tunisie
Anonyme
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

---

## Email #9
**Subject:** Bouh ! On vous a fait peur, Hamza ? 👻
**label prédit/attendu:** `OTHER` · **confidence:** `0.979`

- Longueur brut: **3004** car.
- Longueur full (après clean): **450** car.
- Longueur truncated (600): **450** car.
- Nombre de chunks (sentence): **2**

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t0/h001.OT7Qsq8Tkdx0C0UDbMctbfqhgIuO9y1sJ_txab42nqU
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t1/h001.v5CI4iB_PWRzdCsVVaKqY5UmE9Yui-Fq9vrhx7HHS9k
)

**********************************

********************************** (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t2/h001.QNSf18BcERIn5ddDrX4Xud5e_w2CUFBTQIDTp1aKZnI
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t3/h001.P6mdiw4s3HgEK6s4sSjiNc-mz1guqjMFF1IYRlqeAeg
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t4/h001.arWqzDXHISCHvYLu8_rUgx6PUaOTW-hI8n5moUN37is
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t5/h001.kMW5Fe6_v4fFsIIL9QW1vN165eMXPtPgpGjF0eq45xs
)

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t6/h001.BqH89SNGnvk-oqoI7jMoOuXh_vRa8xcuLD1UrRXOl9Q
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t7/h001.54N9lQ2vqyFYVhryqP2amCWwI9XAuaTh9837o6M500M
) 

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxL6xPjIaptv4JKdyXfjH9riQc1BzkUAbW8W1QVirvV_eg/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t8/h001.QJ9ryNA53VP6VHlCDiMVKQty1v4YImtts8o0S9v_Hug )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI_iTAOgzG3O8mWZLjufH2j94XqrAsavqU5fFVCv_Ed0g/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t9/h001.neY5MDjUfGa8AkrP1MXuhce0sNT6fKyjGpGx6uION2M )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzNT_CRIeE1IOHBd4p_qdy3A/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t10/h001.Faay3ahhYIYTZ8fwRpoZFF3OGYHZg-G1ybFVhIcv6YQ )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t0/h001.OT7Qsq8Tkdx0C0UDbMctbfqhgIuO9y1sJ_txab42nqU
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t1/h001.v5CI4iB_PWRzdCsVVaKqY5UmE9Yui-Fq9vrhx7HHS9k
)

**********************************

********************************** (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t2/h001.QNSf18BcERIn5ddDrX4Xud5e_w2CUFBTQIDTp1aKZnI
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t3/h001.P6mdiw4s3HgEK6s4sSjiNc-mz1guqjMFF1IYRlqeAeg
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t4/h001.arWqzDXHISCHvYLu8_rUgx6PUaOTW-hI8n5moUN37is
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t5/h001.kMW5Fe6_v4fFsIIL9QW1vN165eMXPtPgpGjF0eq45xs
)

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t6/h001.BqH89SNGnvk-oqoI7jMoOuXh_vRa8xcuLD1UrRXOl9Q
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t7/h001.54N9lQ2vqyFYVhryqP2amCWwI9XAuaTh9837o6M500M
) 

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxL6xPjIaptv4JKdyXfjH9riQc1BzkUAbW8W1QVirvV_eg/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t8/h001.QJ9ryNA53VP6VHlCDiMVKQty1v4YImtts8o0S9v_Hug )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI_iTAOgzG3O8mWZLjufH2j94XqrAsavqU5fFVCv_Ed0g/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t9/h001.neY5MDjUfGa8AkrP1MXuhce0sNT6fKyjGpGx6uION2M )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzNT_CRIeE1IOHBd4p_qdy3A/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t10/h001.Faay3ahhYIYTZ8fwRpoZFF3OGYHZg-G1ybFVhIcv6YQ )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t0/h001.OT7Qsq8Tkdx0C0UDbMctbfqhgIuO9y1sJ_txab42nqU
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t1/h001.v5CI4iB_PWRzdCsVVaKqY5UmE9Yui-Fq9vrhx7HHS9k
)

**********************************

********************************** (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t2/h001.QNSf18BcERIn5ddDrX4Xud5e_w2CUFBTQIDTp1aKZnI
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t3/h001.P6mdiw4s3HgEK6s4sSjiNc-mz1guqjMFF1IYRlqeAeg
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t4/h001.arWqzDXHISCHvYLu8_rUgx6PUaOTW-hI8n5moUN37is
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t5/h001.kMW5Fe6_v4fFsIIL9QW1vN165eMXPtPgpGjF0eq45xs
)

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t6/h001.BqH89SNGnvk-oqoI7jMoOuXh_vRa8xcuLD1UrRXOl9Q
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t7/h001.54N9lQ2vqyFYVhryqP2amCWwI9XAuaTh9837o6M500M
) 

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxL6xPjIaptv4JKdyXfjH9riQc1BzkUAbW8W1QVirvV_eg/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t8/h001.QJ9ryNA53VP6VHlCDiMVKQty1v4YImtts8o0S9v_Hug )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI_iTAOgzG3O8mWZLjufH2j94XqrAsavqU5fFVCv_Ed0g/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t9/h001.neY5MDjUfGa8AkrP1MXuhce0sNT6fKyjGpGx6uION2M )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzNT_CRIeE1IOHBd4p_qdy3A/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t10/h001.Faay3ahhYIYTZ8fwRpoZFF3OGYHZg-G1ybFVhIcv6YQ )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t0/h001.OT7Qsq8Tkdx0C0UDbMctbfqhgIuO9y1sJ_txab42nqU
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t1/h001.v5CI4iB_PWRzdCsVVaKqY5UmE9Yui-Fq9vrhx7HHS9k
)

**********************************

********************************** (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t2/h001.QNSf18BcERIn5ddDrX4Xud5e_w2CUFBTQIDTp1aKZnI
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t3/h001.P6mdiw4s3HgEK6s4sSjiNc-mz1guqjMFF1IYRlqeAeg
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t4/h001.arWqzDXHISCHvYLu8_rUgx6PUaOTW-hI8n5moUN37is
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t5/h001.kMW5Fe6_v4fFsIIL9QW1vN165eMXPtPgpGjF0eq45xs
)

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t6/h001.BqH89SNGnvk-oqoI7jMoOuXh_vRa8xcuLD1UrRXOl9Q
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t7/h001.54N9lQ2vqyFYVhryqP2amCWwI9XAuaTh9837o6M500M
) 

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxL6xPjIaptv4JKdyXfjH9riQc1BzkUAbW8W1QVirvV_eg/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t8/h001.QJ9ryNA53VP6VHlCDiMVKQty1v4YImtts8o0S9v_Hug )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI_iTAOgzG3O8mWZLjufH2j94XqrAsavqU5fFVCv_Ed0g/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t9/h001.neY5MDjUfGa8AkrP1MXuhce0sNT6fKyjGpGx6uION2M )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzNT_CRIeE1IOHBd4p_qdy3A/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t10/h001.Faay3ahhYIYTZ8fwRpoZFF3OGYHZg-G1ybFVhIcv6YQ )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t0/h001.OT7Qsq8Tkdx0C0UDbMctbfqhgIuO9y1sJ_txab42nqU
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQB92PkiV_NK2P66AJC-3v_H/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t1/h001.v5CI4iB_PWRzdCsVVaKqY5UmE9Yui-Fq9vrhx7HHS9k
)

**********************************

********************************** (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t2/h001.QNSf18BcERIn5ddDrX4Xud5e_w2CUFBTQIDTp1aKZnI
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJo7rPIn3V6FwbaInntUsKdOaRtnzIwbfQIiN_RiZqa_B/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t3/h001.P6mdiw4s3HgEK6s4sSjiNc-mz1guqjMFF1IYRlqeAeg
) (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t4/h001.arWqzDXHISCHvYLu8_rUgx6PUaOTW-hI8n5moUN37is
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJjvGj789bxXajCuTMcoiiBiwfqCs-0udU6_nw0u4UT6W/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t5/h001.kMW5Fe6_v4fFsIIL9QW1vN165eMXPtPgpGjF0eq45xs
)

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t6/h001.BqH89SNGnvk-oqoI7jMoOuXh_vRa8xcuLD1UrRXOl9Q
)

**********************************

**********************************

 (
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9l9gJVY21ua7MxB6MvYVyQBhVwMmUvLqwCW-53viX62xn5Y1HMyI-UqVXcaccxFhJrd7_s4IMemSjIGJ0BcEqcWbS4WUBSgvJUJfW733VxO6/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t7/h001.54N9lQ2vqyFYVhryqP2amCWwI9XAuaTh9837o6M500M
) 

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxL6xPjIaptv4JKdyXfjH9riQc1BzkUAbW8W1QVirvV_eg/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t8/h001.QJ9ryNA53VP6VHlCDiMVKQty1v4YImtts8o0S9v_Hug )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI_iTAOgzG3O8mWZLjufH2j94XqrAsavqU5fFVCv_Ed0g/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t9/h001.neY5MDjUfGa8AkrP1MXuhce0sNT6fKyjGpGx6uION2M )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzNT_CRIeE1IOHBd4p_qdy3A/4v0/J9DGWX3gRa-uFFSXOUn9-Q/t10/h001.Faay3ahhYIYTZ8fwRpoZFF3OGYHZg-G1ybFVhIcv6YQ )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxI […]
```

#### 5 — Après strip_urls
*(397 caractères)*
```
Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 

**********************************

********************************** 

**********************************

**********************************

 

**********************************

**********************************

 

 

**********************************

**********************************

 

 

 

 

 
( […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(450 caractères)*
```
Subject: Bouh ! On vous a fait peur, Hamza ? 👻
Body: Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 

**********************************

********************************** 

**********************************

**********************************

 

**********************************

**********************************

 

 

**********************************

**********************************

 

 

 

 

 
( […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(450 caractères)*
```
Subject: Bouh ! On vous a fait peur, Hamza ? 👻
Body: Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 

**********************************

********************************** 

**********************************

**********************************

 

**********************************

**********************************

 

 

**********************************

**********************************

 

 

 

 

 
( […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/2]** — 28 car., 7 mots
```
On vous a fait peur, Hamza ?
```

**chunk[2/2]** — 405 car., 23 mots
```
👻
Body: Créez des invitations effrayantes, des affiches lugubres et bien plus encore
 

**********************************

********************************** 

**********************************

**********************************

 

**********************************

**********************************

 

 

**********************************

**********************************

 

 

 

 

 
( […]
```

---

## Email #10
**Subject:** s shared a chat with you
**label prédit/attendu:** `OTHER` · **confidence:** `0.998`

- Longueur brut: **327** car.
- Longueur full (après clean): **367** car.
- Longueur truncated (600): **367** car.
- Nombre de chunks (sentence): **3**

### Étapes de nettoyage
#### 0 — Body BRUT
*(327 caractères)*
```
A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

#### 1 — Après remove_invisible_chars
*(327 caractères)*
```
A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

#### 2 — Après clean_reply (citations)
*(327 caractères)*
```
A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

#### 3 — Après strip_trailing_signature_block
*(327 caractères)*
```
A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

#### 4 — Après strip_boilerplate
*(327 caractères)*
```
A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

#### 5 — Après strip_urls
*(327 caractères)*
```
A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

#### 6 — FINAL full (Subject + Body) → chunking
*(367 caractères)*
```
Subject: s shared a chat with you
Body: A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(367 caractères)*
```
Subject: s shared a chat with you
Body: A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this? You can ignore this email, or report this chat.
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

### Chunks (split_sentences, min_words=4)
**chunk[1/3]** — 239 car., 41 mots
```
Subject: s shared a chat with you
Body: A chat was shared with you
s (sultan.frikha@ensi-uma.tn) has invited you to a view only copy of
Text classification from embeddings
This invite will expire after 30 days
Open chat
Didn't expect this?
```

**chunk[2/3]** — 47 car., 9 mots
```
You can ignore this email, or report this chat.
```

**chunk[3/3]** — 79 car., 14 mots
```
Anthropic, PBC
548 Market St, PMB 90375, San Francisco, CA 94104
Help · Privacy
```

---

## Email #11
**Subject:** Tanitjobs.com: Alerte Emploi
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **1495** car.
- Longueur full (après clean): **1539** car.
- Longueur truncated (600): **648** car.
- Nombre de chunks (sentence): **1**

### Étapes de nettoyage
#### 0 — Body BRUT
*(1495 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 1 — Après remove_invisible_chars
*(1495 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 2 — Après clean_reply (citations)
*(1495 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 3 — Après strip_trailing_signature_block
*(1495 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 4 — Après strip_boilerplate
*(1495 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 5 — Après strip_urls
*(1495 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1539 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(648 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir cen […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/1]** — 1539 car., 228 mots
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Commercial back office
Ain Zaghouan, Tunis, Tunisie
Maison Farida
Agent Commercial Comptoir
Megrine, Ben Arous, Tunisie
GEOCONCEPT
Assistant(e)
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Responsable Maintenance
Tunis
RH PRO PLUS
Ingénieur Génie Civil ou Architecte Senior
Tunis
RH PRO PLUS
Architectes BIM- Revit & Naviswors
Tunis
RH PRO PLUS
Assistante Veterinaire
mourouj 6, Av 14 janvier
VETO MED
Ingénieur Structure BIM
Tunis
RH PRO PLUS
Aide Magasinier (H/F) - Monastir Centre ville
Monastir centre ville
Annajeh plus
Head of Engineering & Development
Tunis
RH PRO PLUS
Agent de Contrôle qualité des pièces mécaniques usinées
Hammam-Sousse
Cadyou
Head of IT PMO
Tunis
RH PRO PLUS
Offre de Stage – Développeur Web (React / Node.js)
Sfax
Tamkeen
Technicien Génie Climatique et Fluides -Revit
Tunis
RH PRO PLUS
Plant Controller Assistant
Tunis
RH PRO PLUS
Agents expérimentés Prise de RDV + Vente Energie
cité les pins
Lucid prosolution
Senior BIM MEP Engineer
Tunis
RH PRO PLUS
Responsable d’Exploitation Restauration (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable des Ressources Humaines (H)
LAC 1
Solitaire Food Service
Directeur de Restaurant (H/F)
LAC 1
Solitaire Food Service
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

---

## Email #12
**Subject:** Donnez vie à vos designs grâce aux animations
**label prédit/attendu:** `OTHER` · **confidence:** `0.986`

- Longueur brut: **3004** car.
- Longueur full (après clean): **659** car.
- Longueur truncated (600): **659** car.
- Nombre de chunks (sentence): **3**

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

(
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tZCzu9JMGAxYUjnJaK1fL_PL2oQ-cSH1M6x556rJCy3xKPaIkI7CWq149w6pQ58aGoK33XL0h79bzjetL9FBPrCcMhfYy2Onw-chTZVMY07o21Zb0MbcTyKXwnvMojd7rBS2QAx9egPGhimS_Sr7HY8thL8NOME0j7zXVSfXxD4VowaN5zz50nthVXooUboE3JmGxznOohOPwcb6GVlv6rKx7DUrqQk769vIW-Fzmqz/4uz/45nFfunERoC_eFeatpIASA/t0/h001.QZUs0-PV-MQlztsCzQPXtKq0VmegWAL5cILnkOhJmHg )

Canva ( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23b-J8QDNblugYZ-eQiRfS0/4uz/45nFfunERoC_eFeatpIASA/t1/h001.mdHXYfQ85Dn-8BLxUYccL5nLIZb12rdqXtkBO0uLqlE )
Pro Canva 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22jC3-XsnRdPbTolue3iutc/4uz/45nFfunERoC_eFeatpIASA/t2/h001.G21HXFks3-tTTvlT4xQS3Q4oJ1ZQAscz2nu8D-2S9sg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9jSYjQmDyWZrqxUXjHgaLPLrZ8tIb_ozLBO7iNkCjuk7u8v3ndXBmFTNN9lyll-yZN2Ra8C7vLmmmKfl0djrZRzpgS3nfCTD70Gsh9WZLhvX/4uz/45nFfunERoC_eFeatpIASA/t3/h001.jhcIWE6S32lNgwcxcn29M6UBUr5DYd4L14kE_dLbeHI )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23nNuwKY-rvKqgCNsn7o4pZ/4uz/45nFfunERoC_eFeatpIASA/t4/h001.ACyD96iOoM2d0rK2VzCj0xFDb9B4u_yTQJmz0aTKMiQ )Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLEoJySw1yTHQmN1oFASN5UvlCsoVUCkxRjgj4Kxex3uA/4uz/45nFfunERoC_eFeatpIASA/t5/h001.29w3cmUYy0KlKQ81zxACwjsdhTzXhOedvpxG4fFQ3VU )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJTf3aG5iw-c-28PhxuQdDWT5lp00_Pc5hRCfMDwoQghA/4uz/45nFfunERoC_eFeatpIASA/t6/h001.rEJuPjbhkG7HS-o4vbtBSe0WkRBS-xrpFPZgAUZAOCg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzvUX-7bJF-x04dtuBjh0kVA/4uz/45nFfunERoC_eFeatpIASA/t7/h001.wcZG6D7xP6lg0NqE1Ii97nyT67YOdmAPAumzo3UU8ok )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLFZcEK6xF5SkfoB3o4tx6-ZQTZgvs0AhOga3UiQEyTkQ/4uz/45nFfunERoC_eFeatpIASA/t8/h001.ECbBuoSOq44pGzPXXkTg8wou_yFveC5oaqlELTMiUj0 )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxIgwxa6pVAlidlWdrQ6dk-MTz1G6TSuJ8ZisA5gb1mmcw/4uz/45nFfunERoC_eFeatpIASA/t9/h001.zCK_Mc8BN96nCnIQX-zohQNrPnNSNpjNs_c-9Z8x6VQ )
 app store 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22oe6PFqbTqvNQIMynldEYi/4uz/45nFfunERoC_eFeatpIASA/t10/h001.LDF-NJD0RNRv3uW […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

(
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tZCzu9JMGAxYUjnJaK1fL_PL2oQ-cSH1M6x556rJCy3xKPaIkI7CWq149w6pQ58aGoK33XL0h79bzjetL9FBPrCcMhfYy2Onw-chTZVMY07o21Zb0MbcTyKXwnvMojd7rBS2QAx9egPGhimS_Sr7HY8thL8NOME0j7zXVSfXxD4VowaN5zz50nthVXooUboE3JmGxznOohOPwcb6GVlv6rKx7DUrqQk769vIW-Fzmqz/4uz/45nFfunERoC_eFeatpIASA/t0/h001.QZUs0-PV-MQlztsCzQPXtKq0VmegWAL5cILnkOhJmHg )

Canva ( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23b-J8QDNblugYZ-eQiRfS0/4uz/45nFfunERoC_eFeatpIASA/t1/h001.mdHXYfQ85Dn-8BLxUYccL5nLIZb12rdqXtkBO0uLqlE )
Pro Canva 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22jC3-XsnRdPbTolue3iutc/4uz/45nFfunERoC_eFeatpIASA/t2/h001.G21HXFks3-tTTvlT4xQS3Q4oJ1ZQAscz2nu8D-2S9sg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9jSYjQmDyWZrqxUXjHgaLPLrZ8tIb_ozLBO7iNkCjuk7u8v3ndXBmFTNN9lyll-yZN2Ra8C7vLmmmKfl0djrZRzpgS3nfCTD70Gsh9WZLhvX/4uz/45nFfunERoC_eFeatpIASA/t3/h001.jhcIWE6S32lNgwcxcn29M6UBUr5DYd4L14kE_dLbeHI )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23nNuwKY-rvKqgCNsn7o4pZ/4uz/45nFfunERoC_eFeatpIASA/t4/h001.ACyD96iOoM2d0rK2VzCj0xFDb9B4u_yTQJmz0aTKMiQ )Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLEoJySw1yTHQmN1oFASN5UvlCsoVUCkxRjgj4Kxex3uA/4uz/45nFfunERoC_eFeatpIASA/t5/h001.29w3cmUYy0KlKQ81zxACwjsdhTzXhOedvpxG4fFQ3VU )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJTf3aG5iw-c-28PhxuQdDWT5lp00_Pc5hRCfMDwoQghA/4uz/45nFfunERoC_eFeatpIASA/t6/h001.rEJuPjbhkG7HS-o4vbtBSe0WkRBS-xrpFPZgAUZAOCg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzvUX-7bJF-x04dtuBjh0kVA/4uz/45nFfunERoC_eFeatpIASA/t7/h001.wcZG6D7xP6lg0NqE1Ii97nyT67YOdmAPAumzo3UU8ok )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLFZcEK6xF5SkfoB3o4tx6-ZQTZgvs0AhOga3UiQEyTkQ/4uz/45nFfunERoC_eFeatpIASA/t8/h001.ECbBuoSOq44pGzPXXkTg8wou_yFveC5oaqlELTMiUj0 )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxIgwxa6pVAlidlWdrQ6dk-MTz1G6TSuJ8ZisA5gb1mmcw/4uz/45nFfunERoC_eFeatpIASA/t9/h001.zCK_Mc8BN96nCnIQX-zohQNrPnNSNpjNs_c-9Z8x6VQ )
 app store 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22oe6PFqbTqvNQIMynldEYi/4uz/45nFfunERoC_eFeatpIASA/t10/h001.LDF-NJD0RNRv3uW […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

(
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tZCzu9JMGAxYUjnJaK1fL_PL2oQ-cSH1M6x556rJCy3xKPaIkI7CWq149w6pQ58aGoK33XL0h79bzjetL9FBPrCcMhfYy2Onw-chTZVMY07o21Zb0MbcTyKXwnvMojd7rBS2QAx9egPGhimS_Sr7HY8thL8NOME0j7zXVSfXxD4VowaN5zz50nthVXooUboE3JmGxznOohOPwcb6GVlv6rKx7DUrqQk769vIW-Fzmqz/4uz/45nFfunERoC_eFeatpIASA/t0/h001.QZUs0-PV-MQlztsCzQPXtKq0VmegWAL5cILnkOhJmHg )

Canva ( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23b-J8QDNblugYZ-eQiRfS0/4uz/45nFfunERoC_eFeatpIASA/t1/h001.mdHXYfQ85Dn-8BLxUYccL5nLIZb12rdqXtkBO0uLqlE )
Pro Canva 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22jC3-XsnRdPbTolue3iutc/4uz/45nFfunERoC_eFeatpIASA/t2/h001.G21HXFks3-tTTvlT4xQS3Q4oJ1ZQAscz2nu8D-2S9sg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9jSYjQmDyWZrqxUXjHgaLPLrZ8tIb_ozLBO7iNkCjuk7u8v3ndXBmFTNN9lyll-yZN2Ra8C7vLmmmKfl0djrZRzpgS3nfCTD70Gsh9WZLhvX/4uz/45nFfunERoC_eFeatpIASA/t3/h001.jhcIWE6S32lNgwcxcn29M6UBUr5DYd4L14kE_dLbeHI )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23nNuwKY-rvKqgCNsn7o4pZ/4uz/45nFfunERoC_eFeatpIASA/t4/h001.ACyD96iOoM2d0rK2VzCj0xFDb9B4u_yTQJmz0aTKMiQ )Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLEoJySw1yTHQmN1oFASN5UvlCsoVUCkxRjgj4Kxex3uA/4uz/45nFfunERoC_eFeatpIASA/t5/h001.29w3cmUYy0KlKQ81zxACwjsdhTzXhOedvpxG4fFQ3VU )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJTf3aG5iw-c-28PhxuQdDWT5lp00_Pc5hRCfMDwoQghA/4uz/45nFfunERoC_eFeatpIASA/t6/h001.rEJuPjbhkG7HS-o4vbtBSe0WkRBS-xrpFPZgAUZAOCg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzvUX-7bJF-x04dtuBjh0kVA/4uz/45nFfunERoC_eFeatpIASA/t7/h001.wcZG6D7xP6lg0NqE1Ii97nyT67YOdmAPAumzo3UU8ok )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLFZcEK6xF5SkfoB3o4tx6-ZQTZgvs0AhOga3UiQEyTkQ/4uz/45nFfunERoC_eFeatpIASA/t8/h001.ECbBuoSOq44pGzPXXkTg8wou_yFveC5oaqlELTMiUj0 )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxIgwxa6pVAlidlWdrQ6dk-MTz1G6TSuJ8ZisA5gb1mmcw/4uz/45nFfunERoC_eFeatpIASA/t9/h001.zCK_Mc8BN96nCnIQX-zohQNrPnNSNpjNs_c-9Z8x6VQ )
 app store 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22oe6PFqbTqvNQIMynldEYi/4uz/45nFfunERoC_eFeatpIASA/t10/h001.LDF-NJD0RNRv3uW […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

(
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tZCzu9JMGAxYUjnJaK1fL_PL2oQ-cSH1M6x556rJCy3xKPaIkI7CWq149w6pQ58aGoK33XL0h79bzjetL9FBPrCcMhfYy2Onw-chTZVMY07o21Zb0MbcTyKXwnvMojd7rBS2QAx9egPGhimS_Sr7HY8thL8NOME0j7zXVSfXxD4VowaN5zz50nthVXooUboE3JmGxznOohOPwcb6GVlv6rKx7DUrqQk769vIW-Fzmqz/4uz/45nFfunERoC_eFeatpIASA/t0/h001.QZUs0-PV-MQlztsCzQPXtKq0VmegWAL5cILnkOhJmHg )

Canva ( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23b-J8QDNblugYZ-eQiRfS0/4uz/45nFfunERoC_eFeatpIASA/t1/h001.mdHXYfQ85Dn-8BLxUYccL5nLIZb12rdqXtkBO0uLqlE )
Pro Canva 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22jC3-XsnRdPbTolue3iutc/4uz/45nFfunERoC_eFeatpIASA/t2/h001.G21HXFks3-tTTvlT4xQS3Q4oJ1ZQAscz2nu8D-2S9sg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9jSYjQmDyWZrqxUXjHgaLPLrZ8tIb_ozLBO7iNkCjuk7u8v3ndXBmFTNN9lyll-yZN2Ra8C7vLmmmKfl0djrZRzpgS3nfCTD70Gsh9WZLhvX/4uz/45nFfunERoC_eFeatpIASA/t3/h001.jhcIWE6S32lNgwcxcn29M6UBUr5DYd4L14kE_dLbeHI )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23nNuwKY-rvKqgCNsn7o4pZ/4uz/45nFfunERoC_eFeatpIASA/t4/h001.ACyD96iOoM2d0rK2VzCj0xFDb9B4u_yTQJmz0aTKMiQ )Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLEoJySw1yTHQmN1oFASN5UvlCsoVUCkxRjgj4Kxex3uA/4uz/45nFfunERoC_eFeatpIASA/t5/h001.29w3cmUYy0KlKQ81zxACwjsdhTzXhOedvpxG4fFQ3VU )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJTf3aG5iw-c-28PhxuQdDWT5lp00_Pc5hRCfMDwoQghA/4uz/45nFfunERoC_eFeatpIASA/t6/h001.rEJuPjbhkG7HS-o4vbtBSe0WkRBS-xrpFPZgAUZAOCg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzvUX-7bJF-x04dtuBjh0kVA/4uz/45nFfunERoC_eFeatpIASA/t7/h001.wcZG6D7xP6lg0NqE1Ii97nyT67YOdmAPAumzo3UU8ok )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLFZcEK6xF5SkfoB3o4tx6-ZQTZgvs0AhOga3UiQEyTkQ/4uz/45nFfunERoC_eFeatpIASA/t8/h001.ECbBuoSOq44pGzPXXkTg8wou_yFveC5oaqlELTMiUj0 )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxIgwxa6pVAlidlWdrQ6dk-MTz1G6TSuJ8ZisA5gb1mmcw/4uz/45nFfunERoC_eFeatpIASA/t9/h001.zCK_Mc8BN96nCnIQX-zohQNrPnNSNpjNs_c-9Z8x6VQ )
 app store 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22oe6PFqbTqvNQIMynldEYi/4uz/45nFfunERoC_eFeatpIASA/t10/h001.LDF-NJD0RNRv3uW […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

(
https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tZCzu9JMGAxYUjnJaK1fL_PL2oQ-cSH1M6x556rJCy3xKPaIkI7CWq149w6pQ58aGoK33XL0h79bzjetL9FBPrCcMhfYy2Onw-chTZVMY07o21Zb0MbcTyKXwnvMojd7rBS2QAx9egPGhimS_Sr7HY8thL8NOME0j7zXVSfXxD4VowaN5zz50nthVXooUboE3JmGxznOohOPwcb6GVlv6rKx7DUrqQk769vIW-Fzmqz/4uz/45nFfunERoC_eFeatpIASA/t0/h001.QZUs0-PV-MQlztsCzQPXtKq0VmegWAL5cILnkOhJmHg )

Canva ( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23b-J8QDNblugYZ-eQiRfS0/4uz/45nFfunERoC_eFeatpIASA/t1/h001.mdHXYfQ85Dn-8BLxUYccL5nLIZb12rdqXtkBO0uLqlE )
Pro Canva 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22jC3-XsnRdPbTolue3iutc/4uz/45nFfunERoC_eFeatpIASA/t2/h001.G21HXFks3-tTTvlT4xQS3Q4oJ1ZQAscz2nu8D-2S9sg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9jSYjQmDyWZrqxUXjHgaLPLrZ8tIb_ozLBO7iNkCjuk7u8v3ndXBmFTNN9lyll-yZN2Ra8C7vLmmmKfl0djrZRzpgS3nfCTD70Gsh9WZLhvX/4uz/45nFfunERoC_eFeatpIASA/t3/h001.jhcIWE6S32lNgwcxcn29M6UBUr5DYd4L14kE_dLbeHI )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC23nNuwKY-rvKqgCNsn7o4pZ/4uz/45nFfunERoC_eFeatpIASA/t4/h001.ACyD96iOoM2d0rK2VzCj0xFDb9B4u_yTQJmz0aTKMiQ )Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLEoJySw1yTHQmN1oFASN5UvlCsoVUCkxRjgj4Kxex3uA/4uz/45nFfunERoC_eFeatpIASA/t5/h001.29w3cmUYy0KlKQ81zxACwjsdhTzXhOedvpxG4fFQ3VU )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJTf3aG5iw-c-28PhxuQdDWT5lp00_Pc5hRCfMDwoQghA/4uz/45nFfunERoC_eFeatpIASA/t6/h001.rEJuPjbhkG7HS-o4vbtBSe0WkRBS-xrpFPZgAUZAOCg )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxJ0huWxsBizj11xBs5Tf8pzvUX-7bJF-x04dtuBjh0kVA/4uz/45nFfunERoC_eFeatpIASA/t7/h001.wcZG6D7xP6lg0NqE1Ii97nyT67YOdmAPAumzo3UU8ok )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxLFZcEK6xF5SkfoB3o4tx6-ZQTZgvs0AhOga3UiQEyTkQ/4uz/45nFfunERoC_eFeatpIASA/t8/h001.ECbBuoSOq44pGzPXXkTg8wou_yFveC5oaqlELTMiUj0 )
 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9inNSLfUvwU6C00u-AIKuxIgwxa6pVAlidlWdrQ6dk-MTz1G6TSuJ8ZisA5gb1mmcw/4uz/45nFfunERoC_eFeatpIASA/t9/h001.zCK_Mc8BN96nCnIQX-zohQNrPnNSNpjNs_c-9Z8x6VQ )
 app store 
( https://click.engage.canva.com/ss/c/u001.Note3it1gaozj0PIggVG9tplar3juom3GwdJknmjC22oe6PFqbTqvNQIMynldEYi/4uz/45nFfunERoC_eFeatpIASA/t10/h001.LDF-NJD0RNRv3uW […]
```

#### 5 — Après strip_urls
*(598 caractères)*
```
Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

Canva 
Pro Canva 

 

 
Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 

 

 

 

 

 app store 
( […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(659 caractères)*
```
Subject: Donnez vie à vos designs grâce aux animations
Body: Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

Canva 
Pro Canva 

 

 
Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 

 

 

 

 

 app store 
( […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(659 caractères)*
```
Subject: Donnez vie à vos designs grâce aux animations
Body: Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

Canva 
Pro Canva 

 

 
Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design. Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.

Animer vos designs

 

 

 

 

 

 app store 
( […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/3]** — 443 car., 60 mots
```
Subject: Donnez vie à vos designs grâce aux animations
Body: Les designs animés sont plus captivants, plus mémorables et ont plus de chances d’attirer l’attention

Canva 
Pro Canva 

 

 
Video**********************************
Animations photo et vidéo
**********************************Un design plus dynamique en un clic
Les animations vous permettent d’ajouter des effets visuels en un clic à n’importe quel photo ou vidéo de votre design.
```

**chunk[2/3]** — 161 car., 21 mots
```
Des ondulations aux transitions en passant par des entrées et révélations spectaculaires, transformez des designs statiques en contenus qui attirent l’attention.
```

**chunk[3/3]** — 52 car., 7 mots
```
Animer vos designs

 

 

 

 

 

 app store 
( […]
```

---

## Email #13
**Subject:** Tanitjobs.com: Alerte Emploi
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **2169** car.
- Longueur full (après clean): **2213** car.
- Longueur truncated (600): **648** car.
- Nombre de chunks (sentence): **1**

### Étapes de nettoyage
#### 0 — Body BRUT
*(2169 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 1 — Après remove_invisible_chars
*(2169 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 2 — Après clean_reply (citations)
*(2169 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 3 — Après strip_trailing_signature_block
*(2169 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 4 — Après strip_boilerplate
*(2169 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 5 — Après strip_urls
*(2169 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 6 — FINAL full (Subject + Body) → chunking
*(2213 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(648 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, T […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/1]** — 2213 car., 294 mots
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Technico-Commercial Data Center & Infrastructures Télécoms (H/F)
Les Berges du Lac 1, Tunis, Tunisie
CDS Cometa
Barista/serveur
Les Berges du Lac 1, Tunis, Tunisie
MARJ LUXURY DATES
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
CONTRÔLEUR des Tableaux Electrique ( Essai + Test fonctionnel )
Ben Arous, Ben Arous, Tunisie
SISIPLUS
Technico-Commercial B2B / B2G — Électronique, Électricité Industrielle & Robotique
Le Bardo, Tunis, Tunisie
COTHINGS
Commercial(e) B2B – Fixe + Commissions Déplafonnées– 100 % Télétravail CS01
Tunis, Tunis, Tunisie
DCM Solution
Modéliste | Couture & Relation Clientèle
Manar, Tunis, Tunisie
Société Espace Doniez Haute Couture
Technico-commercial(e) | Architecture d’intérieur, Design & Aménagement Paysager
Les berges du lac, Tunis, Tunisie
Floralies
Vendeuse passionnée d'animaux — Zanimax Aouina
Ben Arous, Ben Arous, Tunisie
Zanimax
Comptable ou aide comptable
Bab Bhar, Tunis, Tunisie
CEA
Technicien Opérateur
Hammam Sousse, Sousse, Tunisie
Complexe De Loisir Hannibal Park
assistantes de direction
Tunis, Tunis, Tunisie
Achab Recruitment INTL
Responsable production
Tunis, Tunis, Tunisie
AIRWIN Groupe F2A
Industrie agroalimentaire – Biscuiterie
kairouan, Kairouan, Tunisie
SPIC PAPAGALLO
Formateurs en Informatique et Économie-Gestion – Concours Technologue 2026
Tunis, Tunis, Tunisie
icct
Technico-commercial(e) terrain | Design, Architecture d’intérieur & aménagement paysager
Les Berges du Lac 3, Tunis, Tunisie
Floralies
agent de contrôle qualité
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Responsable de production
Ben Arous, Ben Arous, Tunisie
FLORITEX EXPORT
Technicien(ne) préleveur(se) – Laboratoire d’analyses médicales
La Marsa, Tunis, Tunisie
Laboratoire D'Analyses Medicales
Assistante Marketing Digital et Création de Contenus
Nabeul, Nabeul, Tunisie
Braino
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

---

## Email #14
**Subject:** ✨ New! Go beyond chat with Claude Code and Cowork
**label prédit/attendu:** `OTHER` · **confidence:** `0.990`

- Longueur brut: **3004** car.
- Longueur full (après clean): **1614** car.
- Longueur truncated (600): **669** car.
- Nombre de chunks (sentence): **6**

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
( https://link.coursera.org/f/a/EAOLYx4URCLmGyl7wO8k6g~~/AAQRxRA~/TdGmmjkpGJGtiGAW27J4zevN9tp9ki94_FPIrTdA9Bz00vQE0SOK4snZOuy6oOv5QvIv0pdSl0yt1Yhdi2TzsWNc2U3gzXOJ70QEo2UjzxEFpkaPHBTavPuWcFL9zp_-lZgvaHcPUSuGCmenktQyzQ~~ ) Claude Code and
Cowork skills 
( https://link.coursera.org/f/a/pnT9OZtgecTUsySuRAiM-A~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehsveWrX7BknV-xdaBhVfqF1OgzL0BLPuHo4nGPQuU1scAOX-__7uxInhRi6f4xEb3UJY3su9lwGr8LHavbGb0udutr4RpNWaDfj3YWUzzO_Q~ )

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 
( https://link.coursera.org/f/a/aQJAcORteVTotS4bjHfwGw~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDeh6muxveu7d2NJ76WxnteW9xD6R6mejddsX3yLjAtYNYFXy1HRhaCyfPwqb8OisRkacCcOFft1I47LelprppWrk_bxhXu7KWFJfKLu41_Yiu0~ )
 is how you get the full picture. Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing. Running workflows is another. Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations. It all begins with
enrolling.

Get started 
( https://link.coursera.org/f/a/9ozaFWrg19uQVA9emQL_Cg~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehZCfJFz1z9OL1bxMdq9WIzt-F7yFFFXeixPMqqJaayDscNfIRpRSjnpU4IwEYp5qF3zoc4epc1uSIhXYQjTCZTDoJKdJGrcaeF_3Q7mQZdSY~ )

------------------------------------
Explore more Claude & AI content
------------------------------------

 (https://link.coursera.org/f/a/PcfnebrKfxO6QSM2CkEs9Q~~/AAQRxRA~/PDwLvyCACoQFHf-LUs5YvctKNzdN_2Fv9na58IyTDnKlfjJ06O4yrVJdncLwOfRD1ZML8A0pJP_MFM8G3YfitaM_porcTuyvh93DNwVV7NF96ojjGE5iDC9wvftSki8xZpoXrpGzh6Zeb2oFuVfPn4pMVpQl-YDuxR-ykXtzy4yw_gRfdDhGr1JPl7TXfovKVMRUUiY6M6b7tZ4D8YV8fXF-H2bijCI1pWNwOXfxp9jksgDfz3SQQyUkXOHW4qCm) MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
( https://link.coursera.org/f/a/EAOLYx4URCLmGyl7wO8k6g~~/AAQRxRA~/TdGmmjkpGJGtiGAW27J4zevN9tp9ki94_FPIrTdA9Bz00vQE0SOK4snZOuy6oOv5QvIv0pdSl0yt1Yhdi2TzsWNc2U3gzXOJ70QEo2UjzxEFpkaPHBTavPuWcFL9zp_-lZgvaHcPUSuGCmenktQyzQ~~ ) Claude Code and
Cowork skills 
( https://link.coursera.org/f/a/pnT9OZtgecTUsySuRAiM-A~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehsveWrX7BknV-xdaBhVfqF1OgzL0BLPuHo4nGPQuU1scAOX-__7uxInhRi6f4xEb3UJY3su9lwGr8LHavbGb0udutr4RpNWaDfj3YWUzzO_Q~ )

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 
( https://link.coursera.org/f/a/aQJAcORteVTotS4bjHfwGw~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDeh6muxveu7d2NJ76WxnteW9xD6R6mejddsX3yLjAtYNYFXy1HRhaCyfPwqb8OisRkacCcOFft1I47LelprppWrk_bxhXu7KWFJfKLu41_Yiu0~ )
 is how you get the full picture. Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing. Running workflows is another. Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations. It all begins with
enrolling.

Get started 
( https://link.coursera.org/f/a/9ozaFWrg19uQVA9emQL_Cg~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehZCfJFz1z9OL1bxMdq9WIzt-F7yFFFXeixPMqqJaayDscNfIRpRSjnpU4IwEYp5qF3zoc4epc1uSIhXYQjTCZTDoJKdJGrcaeF_3Q7mQZdSY~ )

------------------------------------
Explore more Claude & AI content
------------------------------------

 (https://link.coursera.org/f/a/PcfnebrKfxO6QSM2CkEs9Q~~/AAQRxRA~/PDwLvyCACoQFHf-LUs5YvctKNzdN_2Fv9na58IyTDnKlfjJ06O4yrVJdncLwOfRD1ZML8A0pJP_MFM8G3YfitaM_porcTuyvh93DNwVV7NF96ojjGE5iDC9wvftSki8xZpoXrpGzh6Zeb2oFuVfPn4pMVpQl-YDuxR-ykXtzy4yw_gRfdDhGr1JPl7TXfovKVMRUUiY6M6b7tZ4D8YV8fXF-H2bijCI1pWNwOXfxp9jksgDfz3SQQyUkXOHW4qCm) MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
( https://link.coursera.org/f/a/EAOLYx4URCLmGyl7wO8k6g~~/AAQRxRA~/TdGmmjkpGJGtiGAW27J4zevN9tp9ki94_FPIrTdA9Bz00vQE0SOK4snZOuy6oOv5QvIv0pdSl0yt1Yhdi2TzsWNc2U3gzXOJ70QEo2UjzxEFpkaPHBTavPuWcFL9zp_-lZgvaHcPUSuGCmenktQyzQ~~ ) Claude Code and
Cowork skills 
( https://link.coursera.org/f/a/pnT9OZtgecTUsySuRAiM-A~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehsveWrX7BknV-xdaBhVfqF1OgzL0BLPuHo4nGPQuU1scAOX-__7uxInhRi6f4xEb3UJY3su9lwGr8LHavbGb0udutr4RpNWaDfj3YWUzzO_Q~ )

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 
( https://link.coursera.org/f/a/aQJAcORteVTotS4bjHfwGw~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDeh6muxveu7d2NJ76WxnteW9xD6R6mejddsX3yLjAtYNYFXy1HRhaCyfPwqb8OisRkacCcOFft1I47LelprppWrk_bxhXu7KWFJfKLu41_Yiu0~ )
 is how you get the full picture. Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing. Running workflows is another. Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations. It all begins with
enrolling.

Get started 
( https://link.coursera.org/f/a/9ozaFWrg19uQVA9emQL_Cg~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehZCfJFz1z9OL1bxMdq9WIzt-F7yFFFXeixPMqqJaayDscNfIRpRSjnpU4IwEYp5qF3zoc4epc1uSIhXYQjTCZTDoJKdJGrcaeF_3Q7mQZdSY~ )

------------------------------------
Explore more Claude & AI content
------------------------------------

 (https://link.coursera.org/f/a/PcfnebrKfxO6QSM2CkEs9Q~~/AAQRxRA~/PDwLvyCACoQFHf-LUs5YvctKNzdN_2Fv9na58IyTDnKlfjJ06O4yrVJdncLwOfRD1ZML8A0pJP_MFM8G3YfitaM_porcTuyvh93DNwVV7NF96ojjGE5iDC9wvftSki8xZpoXrpGzh6Zeb2oFuVfPn4pMVpQl-YDuxR-ykXtzy4yw_gRfdDhGr1JPl7TXfovKVMRUUiY6M6b7tZ4D8YV8fXF-H2bijCI1pWNwOXfxp9jksgDfz3SQQyUkXOHW4qCm) MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
( https://link.coursera.org/f/a/EAOLYx4URCLmGyl7wO8k6g~~/AAQRxRA~/TdGmmjkpGJGtiGAW27J4zevN9tp9ki94_FPIrTdA9Bz00vQE0SOK4snZOuy6oOv5QvIv0pdSl0yt1Yhdi2TzsWNc2U3gzXOJ70QEo2UjzxEFpkaPHBTavPuWcFL9zp_-lZgvaHcPUSuGCmenktQyzQ~~ ) Claude Code and
Cowork skills 
( https://link.coursera.org/f/a/pnT9OZtgecTUsySuRAiM-A~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehsveWrX7BknV-xdaBhVfqF1OgzL0BLPuHo4nGPQuU1scAOX-__7uxInhRi6f4xEb3UJY3su9lwGr8LHavbGb0udutr4RpNWaDfj3YWUzzO_Q~ )

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 
( https://link.coursera.org/f/a/aQJAcORteVTotS4bjHfwGw~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDeh6muxveu7d2NJ76WxnteW9xD6R6mejddsX3yLjAtYNYFXy1HRhaCyfPwqb8OisRkacCcOFft1I47LelprppWrk_bxhXu7KWFJfKLu41_Yiu0~ )
 is how you get the full picture. Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing. Running workflows is another. Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations. It all begins with
enrolling.

Get started 
( https://link.coursera.org/f/a/9ozaFWrg19uQVA9emQL_Cg~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehZCfJFz1z9OL1bxMdq9WIzt-F7yFFFXeixPMqqJaayDscNfIRpRSjnpU4IwEYp5qF3zoc4epc1uSIhXYQjTCZTDoJKdJGrcaeF_3Q7mQZdSY~ )

------------------------------------
Explore more Claude & AI content
------------------------------------

 (https://link.coursera.org/f/a/PcfnebrKfxO6QSM2CkEs9Q~~/AAQRxRA~/PDwLvyCACoQFHf-LUs5YvctKNzdN_2Fv9na58IyTDnKlfjJ06O4yrVJdncLwOfRD1ZML8A0pJP_MFM8G3YfitaM_porcTuyvh93DNwVV7NF96ojjGE5iDC9wvftSki8xZpoXrpGzh6Zeb2oFuVfPn4pMVpQl-YDuxR-ykXtzy4yw_gRfdDhGr1JPl7TXfovKVMRUUiY6M6b7tZ4D8YV8fXF-H2bijCI1pWNwOXfxp9jksgDfz3SQQyUkXOHW4qCm) MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
( https://link.coursera.org/f/a/EAOLYx4URCLmGyl7wO8k6g~~/AAQRxRA~/TdGmmjkpGJGtiGAW27J4zevN9tp9ki94_FPIrTdA9Bz00vQE0SOK4snZOuy6oOv5QvIv0pdSl0yt1Yhdi2TzsWNc2U3gzXOJ70QEo2UjzxEFpkaPHBTavPuWcFL9zp_-lZgvaHcPUSuGCmenktQyzQ~~ ) Claude Code and
Cowork skills 
( https://link.coursera.org/f/a/pnT9OZtgecTUsySuRAiM-A~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehsveWrX7BknV-xdaBhVfqF1OgzL0BLPuHo4nGPQuU1scAOX-__7uxInhRi6f4xEb3UJY3su9lwGr8LHavbGb0udutr4RpNWaDfj3YWUzzO_Q~ )

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 
( https://link.coursera.org/f/a/aQJAcORteVTotS4bjHfwGw~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDeh6muxveu7d2NJ76WxnteW9xD6R6mejddsX3yLjAtYNYFXy1HRhaCyfPwqb8OisRkacCcOFft1I47LelprppWrk_bxhXu7KWFJfKLu41_Yiu0~ )
 is how you get the full picture. Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing. Running workflows is another. Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations. It all begins with
enrolling.

Get started 
( https://link.coursera.org/f/a/9ozaFWrg19uQVA9emQL_Cg~~/AAQRxRA~/EY1pG4aakXQP7iqFj55k-KAI-BlyyeukPEhyAQmfRwFSP6k_AfDy5RD2cA86gPIuCEXHpFrt4bAD849TZNsfLvFl9CUJS_IZnoyC8db5PNHiYpm_Zf7L7faJdbgQdDehZCfJFz1z9OL1bxMdq9WIzt-F7yFFFXeixPMqqJaayDscNfIRpRSjnpU4IwEYp5qF3zoc4epc1uSIhXYQjTCZTDoJKdJGrcaeF_3Q7mQZdSY~ )

------------------------------------
Explore more Claude & AI content
------------------------------------

 (https://link.coursera.org/f/a/PcfnebrKfxO6QSM2CkEs9Q~~/AAQRxRA~/PDwLvyCACoQFHf-LUs5YvctKNzdN_2Fv9na58IyTDnKlfjJ06O4yrVJdncLwOfRD1ZML8A0pJP_MFM8G3YfitaM_porcTuyvh93DNwVV7NF96ojjGE5iDC9wvftSki8xZpoXrpGzh6Zeb2oFuVfPn4pMVpQl-YDuxR-ykXtzy4yw_gRfdDhGr1JPl7TXfovKVMRUUiY6M6b7tZ4D8YV8fXF-H2bijCI1pWNwOXfxp9jksgDfz3SQQyUkXOHW4qCm) MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

#### 5 — Après strip_urls
*(1549 caractères)*
```
Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
 Claude Code and
Cowork skills 

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 

 is how you get the full picture. Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing. Running workflows is another. Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations. It all begins with
enrolling.

Get started 

------------------------------------
Explore more Claude & AI content
------------------------------------

 ( MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1614 caractères)*
```
Subject: ✨ New! Go beyond chat with Claude Code and Cowork
Body: Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
 Claude Code and
Cowork skills 

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 

 is how you get the full picture. Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing. Running workflows is another. Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations. It all begins with
enrolling.

Get started 

------------------------------------
Explore more Claude & AI content
------------------------------------

 ( MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(669 caractères)*
```
Subject: ✨ New! Go beyond chat with Claude Code and Cowork
Body: Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
 Claude Code and
Cowork skills 

**************************************************
Turn conversations into collabo […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/6]** — 849 car., 110 mots
```
Go beyond chat with Claude Code and Cowork
Body: Explore skills for building with Claude Code and automating with
Cowork body, table, td, th, h1, h2, h3, div, span, strong,
b, i, p, ul, ol, li, a { font-family: Helvetica, sans-serif
!important;} sup { font-size: 100% !important; }
.nudge-component-icon-column { padding-left: 12px !important;
padding-right: 32px !important; } .nudge-component-text-column {
padding-bottom: 32px !important; padding-right: 12px !important;
} .mobile-only { display: none !important; } 96

 Coursera 
 Claude Code and
Cowork skills 

**************************************************
Turn conversations into collaborations with Claude
**************************************************

If you’ve only seen one side of Claude, The Complete Claude
Code & Claude Cowork Masterclass 

 is how you get the full picture.
```

**chunk[2/6]** — 331 car., 50 mots
```
Across project-based
experiences, you’ll grow your understanding of:

👉 Claude Code's terminal tools for full-stack development of
apps and websites

👉 Claude Cowork agents and how to form them into teams for
real-world tasks

👉 Model Context Protocol connections for Gmail, Slack,
Salesforce, and more

Shipping code is one thing.
```

**chunk[3/6]** — 29 car., 4 mots
```
Running workflows is another.
```

**chunk[4/6]** — 111 car., 21 mots
```
Use
Claude to do both with skills learned on Coursera, and those big
ideas you have can soon be real creations.
```

**chunk[5/6]** — 29 car., 5 mots
```
It all begins with
enrolling.
```

**chunk[6/6]** — 243 car., 20 mots
```
Get started 

------------------------------------
Explore more Claude & AI content
------------------------------------

 ( MicrosoftMicrosoft Generative AI Operations (GenAIOps)----------------------------------Intermediate ·Enroll now ( […]
```

---

## Email #15
**Subject:** Smile Group : 2 nouveaux postes correspondent à votre profil
**label prédit/attendu:** `OTHER` · **confidence:** `0.759`

- Longueur brut: **461** car.
- Longueur full (après clean): **430** car.
- Longueur truncated (600): **430** car.
- Nombre de chunks (sentence): **2**

### Étapes de nettoyage
#### 0 — Body BRUT
*(461 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
—
Smile Group
Recrutement propulsé par Teamtailor
—
En savoir plus
|
|
Supprimer mes données
```

#### 1 — Après remove_invisible_chars
*(461 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
—
Smile Group
Recrutement propulsé par Teamtailor
—
En savoir plus
|
|
Supprimer mes données
```

#### 2 — Après clean_reply (citations)
*(461 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
—
Smile Group
Recrutement propulsé par Teamtailor
—
En savoir plus
|
|
Supprimer mes données
```

#### 3 — Après strip_trailing_signature_block
*(368 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
```

#### 4 — Après strip_boilerplate
*(354 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

#### 5 — Après strip_urls
*(354 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

#### 6 — FINAL full (Subject + Body) → chunking
*(430 caractères)*
```
Subject: Smile Group : 2 nouveaux postes correspondent à votre profil
Body: Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(430 caractères)*
```
Subject: Smile Group : 2 nouveaux postes correspondent à votre profil
Body: Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

### Chunks (split_sentences, min_words=4)
**chunk[1/2]** — 375 car., 61 mots
```
Subject: Smile Group : 2 nouveaux postes correspondent à votre profil
Body: Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
```

**chunk[2/2]** — 54 car., 10 mots
```
Parcourez le site carrière ou Mettre à jour son profil
```

---

## Email #16
**Subject:** Smile Group : 2 nouveaux postes correspondent à votre profil
**label prédit/attendu:** `OTHER` · **confidence:** `0.759`

- Longueur brut: **461** car.
- Longueur full (après clean): **430** car.
- Longueur truncated (600): **430** car.
- Nombre de chunks (sentence): **2**

### Étapes de nettoyage
#### 0 — Body BRUT
*(461 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
—
Smile Group
Recrutement propulsé par Teamtailor
—
En savoir plus
|
|
Supprimer mes données
```

#### 1 — Après remove_invisible_chars
*(461 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
—
Smile Group
Recrutement propulsé par Teamtailor
—
En savoir plus
|
|
Supprimer mes données
```

#### 2 — Après clean_reply (citations)
*(461 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
—
Smile Group
Recrutement propulsé par Teamtailor
—
En savoir plus
|
|
Supprimer mes données
```

#### 3 — Après strip_trailing_signature_block
*(368 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
Cordialement,
```

#### 4 — Après strip_boilerplate
*(354 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

#### 5 — Après strip_urls
*(354 caractères)*
```
Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

#### 6 — FINAL full (Subject + Body) → chunking
*(430 caractères)*
```
Subject: Smile Group : 2 nouveaux postes correspondent à votre profil
Body: Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(430 caractères)*
```
Subject: Smile Group : 2 nouveaux postes correspondent à votre profil
Body: Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
Parcourez le site carrière ou Mettre à jour son profil
```

### Chunks (split_sentences, min_words=4)
**chunk[1/2]** — 375 car., 61 mots
```
Subject: Smile Group : 2 nouveaux postes correspondent à votre profil
Body: Smile Group
Hamza, 2 nouveaux postes correspondent à votre profil
Tech Lead JAVA H/F - Lille
Smile
·
Lille
·
Hybride
Développeur JAVA Fullstack/IA H/F – Lille
Smile
·
Lille
·
Hybride
En étant inscrit(e) auprès de Smile Group via Connect, vous êtes informé(e) des dernières offres vous correspondant.
```

**chunk[2/2]** — 54 car., 10 mots
```
Parcourez le site carrière ou Mettre à jour son profil
```

---

## Email #17
**Subject:** Fwd: Recherche de jeunes diplômés en développement .NET – Opportunités immédiates
**label prédit/attendu:** `OTHER` · **confidence:** `0.677`

- Longueur brut: **1030** car.
- Longueur full (après clean): **803** car.
- Longueur truncated (600): **701** car.
- Nombre de chunks (sentence): **5**

### Étapes de nettoyage
#### 0 — Body BRUT
*(1030 caractères)*
```
Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.

Bien cordialement,

*Ayet CHIDA*
Responsable recrutement

[image: icon] *0780905074 *[image: icon]* www.trendit.fr
<https://www.trendit.fr/> *

[image: icon]* ayet.chida@trendit.fr <ayet.chida@trendit.fr> *[image:
icon] 19, Rue de la paix 75002 Paris
<https://maps.google.com/?q=19,%20Rue%20de%20la%20paix%2075002%20Paris>
```

#### 1 — Après remove_invisible_chars
*(1030 caractères)*
```
Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.

Bien cordialement,

*Ayet CHIDA*
Responsable recrutement

[image: icon] *0780905074 *[image: icon]* www.trendit.fr
<https://www.trendit.fr/> *

[image: icon]* ayet.chida@trendit.fr <ayet.chida@trendit.fr> *[image:
icon] 19, Rue de la paix 75002 Paris
<https://maps.google.com/?q=19,%20Rue%20de%20la%20paix%2075002%20Paris>
```

#### 2 — Après clean_reply (citations)
*(1030 caractères)*
```
Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.

Bien cordialement,

*Ayet CHIDA*
Responsable recrutement

[image: icon] *0780905074 *[image: icon]* www.trendit.fr
<https://www.trendit.fr/> *

[image: icon]* ayet.chida@trendit.fr <ayet.chida@trendit.fr> *[image:
icon] 19, Rue de la paix 75002 Paris
<https://maps.google.com/?q=19,%20Rue%20de%20la%20paix%2075002%20Paris>
```

#### 3 — Après strip_trailing_signature_block
*(726 caractères)*
```
Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.

Bien cordialement,
```

#### 4 — Après strip_boilerplate
*(706 caractères)*
```
Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.
```

#### 5 — Après strip_urls
*(706 caractères)*
```
Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.
```

#### 6 — FINAL full (Subject + Body) → chunking
*(803 caractères)*
```
Subject: Fwd: Recherche de jeunes diplômés en développement .NET – Opportunités immédiates
Body: Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(701 caractères)*
```
Subject: Fwd: Recherche de jeunes diplômés en développement .NET – Opportunités immédiates
Body: Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.

Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.

À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.

Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.

Je vo […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/5]** — 200 car., 28 mots
```
Subject: Fwd: Recherche de jeunes diplômés en développement .NET – Opportunités immédiates
Body: Madame, Monsieur,

Je me permets de vous contacter en tant que Responsable Recrutement chez
*Trend-IT*.
```

**chunk[2/5]** — 132 car., 16 mots
```
Nous recrutons actuellement et dans l’immédiat *des ingénieurs fraîchement
diplômés* disposant de compétences en développement .NET.
```

**chunk[3/5]** — 205 car., 33 mots
```
À ce titre, je souhaiterais savoir s’il serait possible de nous mettre en
relation avec les jeunes diplômés de votre école ayant suivi une formation
ou réalisé des projets dans cet environnement technique.
```

**chunk[4/5]** — 147 car., 20 mots
```
Nous serions ravis de pouvoir échanger avec les profils intéressés et leur
proposer des opportunités professionnelles adaptées à leurs compétences.
```

**chunk[5/5]** — 111 car., 17 mots
```
Je vous remercie par avance pour votre aide et reste à votre disposition
pour toute information complémentaire.
```

---

## Email #18
**Subject:** The skills that pay more, at half the price.
**label prédit/attendu:** `OTHER` · **confidence:** `0.988`

- Longueur brut: **3004** car.
- Longueur full (après clean): **1135** car.
- Longueur truncated (600): **663** car.
- Nombre de chunks (sentence): **12**

### Alertes
- ℹ️  Beaucoup de chunks (12) — risque de dilution mean-pool

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp ( https://www.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

$ Limited Time Offer

50% Off Promo ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Upgrade Your Skills | 50% Off ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, but an increase in your own market value.

Last days remaining at 50% off. After Thursday, it’s back to full price.

Skills that raise your net worth

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do. Workers with AI skills earn a 62% wage premium over peers in the same role.

Explore Track ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Available on the Mobile App ( https://www.datacamp.com/mobile?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campai […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp ( https://www.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

$ Limited Time Offer

50% Off Promo ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Upgrade Your Skills | 50% Off ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, but an increase in your own market value.

Last days remaining at 50% off. After Thursday, it’s back to full price.

Skills that raise your net worth

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do. Workers with AI skills earn a 62% wage premium over peers in the same role.

Explore Track ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Available on the Mobile App ( https://www.datacamp.com/mobile?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campai […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp ( https://www.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

$ Limited Time Offer

50% Off Promo ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Upgrade Your Skills | 50% Off ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, but an increase in your own market value.

Last days remaining at 50% off. After Thursday, it’s back to full price.

Skills that raise your net worth

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do. Workers with AI skills earn a 62% wage premium over peers in the same role.

Explore Track ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Available on the Mobile App ( https://www.datacamp.com/mobile?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campai […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp ( https://www.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

$ Limited Time Offer

50% Off Promo ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Upgrade Your Skills | 50% Off ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, but an increase in your own market value.

Last days remaining at 50% off. After Thursday, it’s back to full price.

Skills that raise your net worth

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do. Workers with AI skills earn a 62% wage premium over peers in the same role.

Explore Track ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Available on the Mobile App ( https://www.datacamp.com/mobile?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campai […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp ( https://www.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

$ Limited Time Offer

50% Off Promo ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Upgrade Your Skills | 50% Off ( https://www.datacamp.com/promo/limited-time-sale-october-26?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, but an increase in your own market value.

Last days remaining at 50% off. After Thursday, it’s back to full price.

Skills that raise your net worth

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

AI Fundamentals ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do. Workers with AI skills earn a 62% wage premium over peers in the same role.

Explore Track ( https://www.datacamp.com/tracks/ai-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Available on the Mobile App ( https://www.datacamp.com/mobile?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campaign=261016_1-oct26-promo-t2--na--subscription_2-registered_6-tier-2_8-emal-ci_11-promo&dc_euid=20788339 )

Excel Fundamentals ( https://www.datacamp.com/tracks/excel-fundamentals?utm_source=customerio&utm_medium=email&utm_campai […]
```

#### 5 — Après strip_urls
*(1075 caractères)*
```
Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp 

$ Limited Time Offer

50% Off Promo 

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday 

Upgrade Your Skills | 50% Off 

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, but an increase in your own market value.

Last days remaining at 50% off. After Thursday, it’s back to full price.

Skills that raise your net worth

AI Fundamentals 

AI Fundamentals 

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do. Workers with AI skills earn a 62% wage premium over peers in the same role.

Explore Track 

Available on the Mobile App 

Excel Fundamentals 

Excel Fundamentals ( […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1135 caractères)*
```
Subject: The skills that pay more, at half the price.
Body: Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp 

$ Limited Time Offer

50% Off Promo 

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday 

Upgrade Your Skills | 50% Off 

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, but an increase in your own market value.

Last days remaining at 50% off. After Thursday, it’s back to full price.

Skills that raise your net worth

AI Fundamentals 

AI Fundamentals 

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do. Workers with AI skills earn a 62% wage premium over peers in the same role.

Explore Track 

Available on the Mobile App 

Excel Fundamentals 

Excel Fundamentals ( […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(663 caractères)*
```
Subject: The skills that pay more, at half the price.
Body: Skill tracks that change what you're worth, now at 50% off a month. Ends Thursday.

DataCamp 

$ Limited Time Offer

50% Off Promo 

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday 

Upgrade Your Skills | 50% Off 

AI skills now command a 23% higher advertised salary. In comparison, a bachelor’s degree adds 8%. A master’s, 13%. Right now, the market pays more for the skill than for the degree.

Skill tracks help you build a salary premium through a guided, expert-curated curriculum. That’s what $14 a month buys: not a subscription, […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/12]** — 53 car., 10 mots
```
Subject: The skills that pay more, at half the price.
```

**chunk[2/12]** — 73 car., 14 mots
```
Body: Skill tracks that change what you're worth, now at 50% off a month.
```

**chunk[3/12]** — 246 car., 37 mots
```
DataCamp 

$ Limited Time Offer

50% Off Promo 

*****************
AI skills now
out-earn a degree
*****************

Offer ends Thursday

Offer ends Thursday 

Upgrade Your Skills | 50% Off 

AI skills now command a 23% higher advertised salary.
```

**chunk[4/12]** — 43 car., 7 mots
```
In comparison, a bachelor’s degree adds 8%.
```

**chunk[5/12]** — 66 car., 13 mots
```
Right now, the market pays more for the skill than for the degree.
```

**chunk[6/12]** — 89 car., 13 mots
```
Skill tracks help you build a salary premium through a guided, expert-curated curriculum.
```

**chunk[7/12]** — 91 car., 17 mots
```
That’s what $14 a month buys: not a subscription, but an increase in your own market value.
```

**chunk[8/12]** — 31 car., 6 mots
```
Last days remaining at 50% off.
```

**chunk[9/12]** — 40 car., 7 mots
```
After Thursday, it’s back to full price.
```

**chunk[10/12]** — 189 car., 30 mots
```
Skills that raise your net worth

AI Fundamentals 

AI Fundamentals 

Skill Track

Certification Available

AI Fundamentals

9 hours · 6 courses

Use AI properly in the work you already do.
```

**chunk[11/12]** — 75 car., 15 mots
```
Workers with AI skills earn a 62% wage premium over peers in the same role.
```

**chunk[12/12]** — 91 car., 13 mots
```
Explore Track 

Available on the Mobile App 

Excel Fundamentals 

Excel Fundamentals ( […]
```

---

## Email #19
**Subject:** Tanitjobs.com: Alerte Emploi
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **1805** car.
- Longueur full (après clean): **1849** car.
- Longueur truncated (600): **648** car.
- Nombre de chunks (sentence): **1**

### Étapes de nettoyage
#### 0 — Body BRUT
*(1805 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 1 — Après remove_invisible_chars
*(1805 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 2 — Après clean_reply (citations)
*(1805 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 3 — Après strip_trailing_signature_block
*(1805 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 4 — Après strip_boilerplate
*(1805 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 5 — Après strip_urls
*(1805 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1849 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(648 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisi […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/1]** — 1849 car., 249 mots
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Centre médical d'exploration à Sousse
Sousse Hached, Sousse, Tunisie
Centre médical d'exploration
Assistante Agence de voyage
Hammamet, Nabeul, Tunisie
Jerba international travel
Fromagerie et charcuteries cherche vendeuse expérimenté
EL Menzah 9, Tunis, Tunisie
La croûte
Avocat Connect recrute un(e) Juriste en droit des étrangers (H/F)
Résidence jinen les jardins de Carthage, Tunis, Tunisie
novasolvd
Assistante administrative
Tunis, Tunisie
AYA CONNECT
commercial b2b
sahloul, Sousse, Tunisie
pingoware
Ingénieur génie civil
La Manouba, La Manouba, Tunisie
Société Nehdi
Expert Marketing
sahloul, Sousse, Tunisie
pingoware
DEVELOPPEUR SOFTWARE ‘HPC’ JUNIOR
centre ville, Tunis, Tunisie
ENNOLAB
Directeur d'usine
Sfax, Sfax, Tunisie
Soprocaf
TECHNICIEN MAINTENANCE MACHINES OUTILS
ZI Sidi Abdelhamid
Usinage de Précision
Développeur Confirmé .NET C# (H/F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
Commerciale en Assurance
Montplaisir , centre pacha bloc c1ere étage
karma solution
assistant comptable
sousse, Tunisie
cmk expertise
Comptable (F)
Centre Urbain Nord, Ariana, Tunisie
ISI Digital
MATEB recrute un(e) Technicien(ne) / Ingénieur(e) agronome – Conseil et vente
Bir Bouregba – Hammamet
MATEB
Chargé clientèle
Tunis centre ville
Tunibest cash
MATEB recrute un(e) Assistant(e) commercial(e) et administratif(ve)
Bir Bouregba – Hammamet
MATEB
Conducteur CT / Opérateur CU AMECAP THYNA
Sfax route de gabes km9 , cité Tyhna
amecap
ASSISTANTE ADMINISTRATIVE
Route kairouan km2 Msaken Sousse
Groupe Ghraieb
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

---

## Email #20
**Subject:** Site Reliability Engineer (Guardicore AI Platform) - Remote 3497 at Akamai Technologies
**label prédit/attendu:** `REJECTION` · **confidence:** `0.960`

- Longueur brut: **1071** car.
- Longueur full (après clean): **636** car.
- Longueur truncated (600): **636** car.
- Nombre de chunks (sentence): **5**

### Étapes de nettoyage
#### 0 — Body BRUT
*(1071 caractères)*
```
Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
Talent Acquisition
Akamai Technologies
This is a system generated email, replies to this message are undeliverable and will not reach the Talent Acquisition Team. Please do not reply.
Akamai Technologies is an Affirmative Action, Equal Opportunity Employer that values the strength that diversity brings to the workplace. All qualified applicants will receive consideration for employment and will not be discriminated against on the basis of gender, race/ethnicity, protected veteran status, disability, or other protected group status.
```

#### 1 — Après remove_invisible_chars
*(1071 caractères)*
```
Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
Talent Acquisition
Akamai Technologies
This is a system generated email, replies to this message are undeliverable and will not reach the Talent Acquisition Team. Please do not reply.
Akamai Technologies is an Affirmative Action, Equal Opportunity Employer that values the strength that diversity brings to the workplace. All qualified applicants will receive consideration for employment and will not be discriminated against on the basis of gender, race/ethnicity, protected veteran status, disability, or other protected group status.
```

#### 2 — Après clean_reply (citations)
*(1071 caractères)*
```
Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
Talent Acquisition
Akamai Technologies
This is a system generated email, replies to this message are undeliverable and will not reach the Talent Acquisition Team. Please do not reply.
Akamai Technologies is an Affirmative Action, Equal Opportunity Employer that values the strength that diversity brings to the workplace. All qualified applicants will receive consideration for employment and will not be discriminated against on the basis of gender, race/ethnicity, protected veteran status, disability, or other protected group status.
```

#### 3 — Après strip_trailing_signature_block
*(533 caractères)*
```
Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
```

#### 4 — Après strip_boilerplate
*(533 caractères)*
```
Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
```

#### 5 — Après strip_urls
*(533 caractères)*
```
Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
```

#### 6 — FINAL full (Subject + Body) → chunking
*(636 caractères)*
```
Subject: Site Reliability Engineer (Guardicore AI Platform) - Remote 3497 at Akamai Technologies
Body: Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(636 caractères)*
```
Subject: Site Reliability Engineer (Guardicore AI Platform) - Remote 3497 at Akamai Technologies
Body: Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497). After careful consideration, we regret to inform you that you have not been selected for this position.
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option. We also invite you to visit the Careers section on our website regularly.
We thank you for your interest in Akamai Technologies and wish you all the best.
Thank you,
```

### Chunks (split_sentences, min_words=4)
**chunk[1/5]** — 230 car., 34 mots
```
Subject: Site Reliability Engineer (Guardicore AI Platform) - Remote 3497 at Akamai Technologies
Body: Hi hamza,
Thank you for your interest regarding the Site Reliability Engineer (Guardicore AI Platform) - Remote (Job ID: 3497).
```

**chunk[2/5]** — 103 car., 17 mots
```
After careful consideration, we regret to inform you that you have not been selected for this position.
```

**chunk[3/5]** — 135 car., 24 mots
```
We will retain your information in our database and may inform you of job openings that match your profile if you selected this option.
```

**chunk[4/5]** — 73 car., 13 mots
```
We also invite you to visit the Careers section on our website regularly.
```

**chunk[5/5]** — 80 car., 15 mots
```
We thank you for your interest in Akamai Technologies and wish you all the best.
```

---

## Email #21
**Subject:** Hello
**label prédit/attendu:** `OTHER` · **confidence:** `0.770`

- Longueur brut: **13** car.
- Longueur full (après clean): **34** car.
- Longueur truncated (600): **34** car.
- Nombre de chunks (sentence): **1**

### Étapes de nettoyage
#### 0 — Body BRUT
*(13 caractères)*
```
Just for test
```

#### 1 — Après remove_invisible_chars
*(13 caractères)*
```
Just for test
```

#### 2 — Après clean_reply (citations)
*(13 caractères)*
```
Just for test
```

#### 3 — Après strip_trailing_signature_block
*(13 caractères)*
```
Just for test
```

#### 4 — Après strip_boilerplate
*(13 caractères)*
```
Just for test
```

#### 5 — Après strip_urls
*(13 caractères)*
```
Just for test
```

#### 6 — FINAL full (Subject + Body) → chunking
*(34 caractères)*
```
Subject: Hello
Body: Just for test
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(34 caractères)*
```
Subject: Hello
Body: Just for test
```

### Chunks (split_sentences, min_words=4)
**chunk[1/1]** — 34 car., 6 mots
```
Subject: Hello
Body: Just for test
```

---

## Email #22
**Subject:** 4 free live sessions to get more out of AI at work
**label prédit/attendu:** `OTHER` · **confidence:** `0.994`

- Longueur brut: **3004** car.
- Longueur full (après clean): **1561** car.
- Longueur truncated (600): **670** car.
- Nombre de chunks (sentence): **17**

### Alertes
- ℹ️  Beaucoup de chunks (17) — risque de dilution mean-pool

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp ( https://app.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Live Sessions

 

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.

We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself. Plus, what’s worked in roles from sales to legal.

Four free, live sessions for every role. No prior AI experience needed. One registration unlocks everything.

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

 

Pick your session

AI-Assisted Reporting with Word and Copilot ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway. Go from blank page to a finished report that’s checked and ready to send.

Register Now ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Make AI Accessible Across Your Org ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job. See how it’s being rolled out in sales, marketing, finance, and legal.

Register Now ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-ema […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp ( https://app.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Live Sessions

 

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.

We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself. Plus, what’s worked in roles from sales to legal.

Four free, live sessions for every role. No prior AI experience needed. One registration unlocks everything.

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

 

Pick your session

AI-Assisted Reporting with Word and Copilot ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway. Go from blank page to a finished report that’s checked and ready to send.

Register Now ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Make AI Accessible Across Your Org ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job. See how it’s being rolled out in sales, marketing, finance, and legal.

Register Now ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-ema […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp ( https://app.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Live Sessions

 

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.

We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself. Plus, what’s worked in roles from sales to legal.

Four free, live sessions for every role. No prior AI experience needed. One registration unlocks everything.

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

 

Pick your session

AI-Assisted Reporting with Word and Copilot ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway. Go from blank page to a finished report that’s checked and ready to send.

Register Now ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Make AI Accessible Across Your Org ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job. See how it’s being rolled out in sales, marketing, finance, and legal.

Register Now ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-ema […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp ( https://app.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Live Sessions

 

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.

We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself. Plus, what’s worked in roles from sales to legal.

Four free, live sessions for every role. No prior AI experience needed. One registration unlocks everything.

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

 

Pick your session

AI-Assisted Reporting with Word and Copilot ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway. Go from blank page to a finished report that’s checked and ready to send.

Register Now ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Make AI Accessible Across Your Org ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job. See how it’s being rolled out in sales, marketing, finance, and legal.

Register Now ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-ema […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp ( https://app.datacamp.com/?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Live Sessions

 

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.

We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself. Plus, what’s worked in roles from sales to legal.

Four free, live sessions for every role. No prior AI experience needed. One registration unlocks everything.

Register For Free ( https://events.datacamp.com/ai-for-knowledge-workers?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

 

Pick your session

AI-Assisted Reporting with Word and Copilot ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway. Go from blank page to a finished report that’s checked and ready to send.

Register Now ( https://www.datacamp.com/webinars/ai-assisted-reporting-with-word-and-copilot?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )

Make AI Accessible Across Your Org ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-emal-ci_11-franchise&dc_euid=20788339 )
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job. See how it’s being rolled out in sales, marketing, finance, and legal.

Register Now ( https://www.datacamp.com/webinars/make-ai-accessible-across-your-org?utm_source=customerio&utm_medium=email&utm_campaign=261015_1-ai-for-knowledge-workers--na--engagement_2-mix_6-tier-2_8-ema […]
```

#### 5 — Après strip_urls
*(1495 caractères)*
```
Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp 

Live Sessions

 

Register For Free 

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.

We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself. Plus, what’s worked in roles from sales to legal.

Four free, live sessions for every role. No prior AI experience needed. One registration unlocks everything.

Register For Free 

 

Pick your session

AI-Assisted Reporting with Word and Copilot 
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway. Go from blank page to a finished report that’s checked and ready to send.

Register Now 

Make AI Accessible Across Your Org 
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job. See how it’s being rolled out in sales, marketing, finance, and legal.

Register Now ( […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1561 caractères)*
```
Subject: 4 free live sessions to get more out of AI at work
Body: Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp 

Live Sessions

 

Register For Free 

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.

We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself. Plus, what’s worked in roles from sales to legal.

Four free, live sessions for every role. No prior AI experience needed. One registration unlocks everything.

Register For Free 

 

Pick your session

AI-Assisted Reporting with Word and Copilot 
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway. Go from blank page to a finished report that’s checked and ready to send.

Register Now 

Make AI Accessible Across Your Org 
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job. See how it’s being rolled out in sales, marketing, finance, and legal.

Register Now ( […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(670 caractères)*
```
Subject: 4 free live sessions to get more out of AI at work
Body: Learn to hand AI the busywork. No prior AI experience needed. Nov 3–6.

DataCamp 

Live Sessions

 

Register For Free 

**********************************************************
Hand AI the busywork so you can focus on what you do best.
**********************************************************

AI was supposed to take work off your plate. Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.

That changes when you stop asking it questions and start giving it work. It can already take the first pass at the admin, the draft, and the data pu […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/17]** — 96 car., 20 mots
```
Subject: 4 free live sessions to get more out of AI at work
Body: Learn to hand AI the busywork.
```

**chunk[2/17]** — 30 car., 5 mots
```
No prior AI experience needed.
```

**chunk[3/17]** — 166 car., 20 mots
```
DataCamp 

Live Sessions

 

Register For Free 

**********************************************************
Hand AI the busywork so you can focus on what you do best.
```

**chunk[4/17]** — 104 car., 10 mots
```
**********************************************************

AI was supposed to take work off your plate.
```

**chunk[5/17]** — 106 car., 19 mots
```
Instead, it added a step: you ask, rewrite what comes back, then check every line before it goes anywhere.
```

**chunk[6/17]** — 72 car., 13 mots
```
That changes when you stop asking it questions and start giving it work.
```

**chunk[7/17]** — 147 car., 28 mots
```
It can already take the first pass at the admin, the draft, and the data pull, leaving you time for the insights and delivery that get you noticed.
```

**chunk[8/17]** — 173 car., 30 mots
```
We’ve gathered speakers from Replit, the University of Michigan, and more to show you how to hand AI the drafting and the analysis, and keep the judgment calls for yourself.
```

**chunk[9/17]** — 49 car., 9 mots
```
Plus, what’s worked in roles from sales to legal.
```

**chunk[10/17]** — 40 car., 7 mots
```
Four free, live sessions for every role.
```

**chunk[11/17]** — 30 car., 5 mots
```
No prior AI experience needed.
```

**chunk[12/17]** — 36 car., 4 mots
```
One registration unlocks everything.
```

**chunk[13/17]** — 180 car., 28 mots
```
Register For Free 

 

Pick your session

AI-Assisted Reporting with Word and Copilot 
Nov 3

AI-Assisted Reporting with Word and Copilot

You end up rewriting the AI draft anyway.
```

**chunk[14/17]** — 73 car., 14 mots
```
Go from blank page to a finished report that’s checked and ready to send.
```

**chunk[15/17]** — 139 car., 25 mots
```
Register Now 

Make AI Accessible Across Your Org 
Nov 4

Make AI Accessible Across Your Org

AI can feel like it’s for someone else’s job.
```

**chunk[16/17]** — 70 car., 12 mots
```
See how it’s being rolled out in sales, marketing, finance, and legal.
```

**chunk[17/17]** — 18 car., 4 mots
```
Register Now ( […]
```

---

## Email #23
**Subject:** Tanitjobs.com: Alerte Emploi
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **1943** car.
- Longueur full (après clean): **1987** car.
- Longueur truncated (600): **648** car.
- Nombre de chunks (sentence): **2**

### Étapes de nettoyage
#### 0 — Body BRUT
*(1943 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 1 — Après remove_invisible_chars
*(1943 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 2 — Après clean_reply (citations)
*(1943 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 3 — Après strip_trailing_signature_block
*(1943 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 4 — Après strip_boilerplate
*(1943 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 5 — Après strip_urls
*(1943 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1987 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(648 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Desig […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/2]** — 251 car., 33 mots
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
Agent Stock
Soukra, Ariana, Tunisie
SPORT 1
Passionné(e) de Basketball ou Volleyball – Rejoignez-nous !
```

**chunk[2/2]** — 1735 car., 235 mots
```
Tunis, Tunis, Tunisie
LetsCode
Professeur(e) de Français - Cycle Primaire (3ème et 4ème année)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Télévendeur -Commercial sédentaire h/f
Sousse, Sousse, Tunisie
la ruche recrute
Station and QHSE Assistant
Gabès, Gabès, Tunisie
La Joie de Hicha
Animatrice Préscolaire Francophone
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Technicien / Designer Mobilier / Agencement
Soukra, Ariana, Tunisie
CDS
Assistante
Tunis, Tunis, Tunisie
PHARMACIE AZZOUZ
Stagiaire Développeur IA Agentique (H/F)
Tunis, Tunis, Tunisie
Dev Digital
Ingénieur FAO Mastercam – Programmation CNC & Optimisation des procédés d’usinage
Ariana, Ariana, Tunisie
3TF
Purchasing Support Technician
Mghira, Ben Arous, Tunisie
CMR GROUP
Gestionnaire de Paie & Administration du Personnel (H/F)
Les Berges du Lac 1, Tunis, Tunisie
Solitaire Food Service
Responsable UAP atelier traitement de surface
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Censeur d’Établissement Scolaire (Primaire & Collège)
Tunis, Tunis, Tunisie
FONDATION BOUEBDELLI TUNIS
Assistante de direction
Sfax, Sfax, Tunisie
Laboratoires GALPHARMA
Responsable SAV Automobile (Tunis)
Ben Arous, Ben Arous, Tunisie
Groupe ZOUARI
Responsable UAP peinture poudre
La Manouba, La Manouba, Tunisie
SURFAPROTEC
Chef de zone (Sahel, Kairouan)
La Manouba, La Manouba, Tunisie
Café Stella
Chef de zone (Grand Tunis, Bizerte)
La Manouba, La Manouba, Tunisie
Café Stella
MODELISTE INDUSTRIELLE (patronage CAO-Maille coupée-cousue et chaîne et trame flou)
Bembla/Mnara, Monastir, Tunisie
BGT
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

---

## Email #24
**Subject:** Dernières opportunités sur Free-Work !
**label prédit/attendu:** `OTHER` · **confidence:** `0.988`

- Longueur brut: **3004** car.
- Longueur full (après clean): **1877** car.
- Longueur truncated (600): **658** car.
- Nombre de chunks (sentence): **13**

### Alertes
- ℹ️  Beaucoup de chunks (13) — risque de dilution mean-pool

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Voir la version en ligne https://0pxgj.mjt.lu/nl3/Vr3lEBUzmZxBkRNlcXJY5w?m=EAAACYtP2xUAAc4aq4oAA7BQnY4AAAAAKuEAAg81ABwJdwBq0GqLVmQYRJE3SN6EMuvHdqaMjAAQJIA&b=ddb2e6ad&e=8e9a4d64&x=7kzCgjLFdOs7LMV9UDnxaH0MfROpUCFYSS401hYQsNI

<<freework logo>> [https://www.free-work.com/fr/tech-it]

Dernières offres d'emploi [https://www.free-work.com/fr/tech-it/jobs?contracts=permanent]

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/architecte-technique/architecte-technique-data-et-ia-h-f-6]

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/ingenieur-securite/lead-devsecops-h-f-1]

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/business-analyst/business-analyst-rpa-13]

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [https://www.free-work.com/fr/tech-it/jobs/suggested]

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data. Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
<<Faire le point>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]

--------------------------------------------------------------------------------

<<Gmes>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

Ils recrutent !
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA. Elle travaille pour EDF ou Generali, des Caraïbes au Canada. L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance. 

Pourquoi pas vous ?
<<Rejoindre la team Bugbusters>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

--------------------------------------------------------------------------------

Une question ? Allez voir ceux qui l’ont déjà vécue
<<Forum>> [https://www.free-work.com/fr/tech-it/forum/latest]
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
<<Découvrir les échanges>> [https://www.free-work.com/fr/tech-it/forum/latest]

--------------------------------------------------------------------------------

<<Industrie>> [https://www.free-work.com/fr/tech-it/blog/metiers-it/industrie-4-0-et-iot-les-me […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Voir la version en ligne https://0pxgj.mjt.lu/nl3/Vr3lEBUzmZxBkRNlcXJY5w?m=EAAACYtP2xUAAc4aq4oAA7BQnY4AAAAAKuEAAg81ABwJdwBq0GqLVmQYRJE3SN6EMuvHdqaMjAAQJIA&b=ddb2e6ad&e=8e9a4d64&x=7kzCgjLFdOs7LMV9UDnxaH0MfROpUCFYSS401hYQsNI

<<freework logo>> [https://www.free-work.com/fr/tech-it]

Dernières offres d'emploi [https://www.free-work.com/fr/tech-it/jobs?contracts=permanent]

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/architecte-technique/architecte-technique-data-et-ia-h-f-6]

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/ingenieur-securite/lead-devsecops-h-f-1]

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/business-analyst/business-analyst-rpa-13]

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [https://www.free-work.com/fr/tech-it/jobs/suggested]

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data. Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
<<Faire le point>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]

--------------------------------------------------------------------------------

<<Gmes>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

Ils recrutent !
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA. Elle travaille pour EDF ou Generali, des Caraïbes au Canada. L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance. 

Pourquoi pas vous ?
<<Rejoindre la team Bugbusters>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

--------------------------------------------------------------------------------

Une question ? Allez voir ceux qui l’ont déjà vécue
<<Forum>> [https://www.free-work.com/fr/tech-it/forum/latest]
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
<<Découvrir les échanges>> [https://www.free-work.com/fr/tech-it/forum/latest]

--------------------------------------------------------------------------------

<<Industrie>> [https://www.free-work.com/fr/tech-it/blog/metiers-it/industrie-4-0-et-iot-les-me […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Voir la version en ligne https://0pxgj.mjt.lu/nl3/Vr3lEBUzmZxBkRNlcXJY5w?m=EAAACYtP2xUAAc4aq4oAA7BQnY4AAAAAKuEAAg81ABwJdwBq0GqLVmQYRJE3SN6EMuvHdqaMjAAQJIA&b=ddb2e6ad&e=8e9a4d64&x=7kzCgjLFdOs7LMV9UDnxaH0MfROpUCFYSS401hYQsNI

<<freework logo>> [https://www.free-work.com/fr/tech-it]

Dernières offres d'emploi [https://www.free-work.com/fr/tech-it/jobs?contracts=permanent]

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/architecte-technique/architecte-technique-data-et-ia-h-f-6]

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/ingenieur-securite/lead-devsecops-h-f-1]

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/business-analyst/business-analyst-rpa-13]

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [https://www.free-work.com/fr/tech-it/jobs/suggested]

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data. Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
<<Faire le point>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]

--------------------------------------------------------------------------------

<<Gmes>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

Ils recrutent !
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA. Elle travaille pour EDF ou Generali, des Caraïbes au Canada. L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance. 

Pourquoi pas vous ?
<<Rejoindre la team Bugbusters>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

--------------------------------------------------------------------------------

Une question ? Allez voir ceux qui l’ont déjà vécue
<<Forum>> [https://www.free-work.com/fr/tech-it/forum/latest]
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
<<Découvrir les échanges>> [https://www.free-work.com/fr/tech-it/forum/latest]

--------------------------------------------------------------------------------

<<Industrie>> [https://www.free-work.com/fr/tech-it/blog/metiers-it/industrie-4-0-et-iot-les-me […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Voir la version en ligne https://0pxgj.mjt.lu/nl3/Vr3lEBUzmZxBkRNlcXJY5w?m=EAAACYtP2xUAAc4aq4oAA7BQnY4AAAAAKuEAAg81ABwJdwBq0GqLVmQYRJE3SN6EMuvHdqaMjAAQJIA&b=ddb2e6ad&e=8e9a4d64&x=7kzCgjLFdOs7LMV9UDnxaH0MfROpUCFYSS401hYQsNI

<<freework logo>> [https://www.free-work.com/fr/tech-it]

Dernières offres d'emploi [https://www.free-work.com/fr/tech-it/jobs?contracts=permanent]

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/architecte-technique/architecte-technique-data-et-ia-h-f-6]

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/ingenieur-securite/lead-devsecops-h-f-1]

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/business-analyst/business-analyst-rpa-13]

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [https://www.free-work.com/fr/tech-it/jobs/suggested]

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data. Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
<<Faire le point>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]

--------------------------------------------------------------------------------

<<Gmes>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

Ils recrutent !
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA. Elle travaille pour EDF ou Generali, des Caraïbes au Canada. L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance. 

Pourquoi pas vous ?
<<Rejoindre la team Bugbusters>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

--------------------------------------------------------------------------------

Une question ? Allez voir ceux qui l’ont déjà vécue
<<Forum>> [https://www.free-work.com/fr/tech-it/forum/latest]
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
<<Découvrir les échanges>> [https://www.free-work.com/fr/tech-it/forum/latest]

--------------------------------------------------------------------------------

<<Industrie>> [https://www.free-work.com/fr/tech-it/blog/metiers-it/industrie-4-0-et-iot-les-me […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Voir la version en ligne https://0pxgj.mjt.lu/nl3/Vr3lEBUzmZxBkRNlcXJY5w?m=EAAACYtP2xUAAc4aq4oAA7BQnY4AAAAAKuEAAg81ABwJdwBq0GqLVmQYRJE3SN6EMuvHdqaMjAAQJIA&b=ddb2e6ad&e=8e9a4d64&x=7kzCgjLFdOs7LMV9UDnxaH0MfROpUCFYSS401hYQsNI

<<freework logo>> [https://www.free-work.com/fr/tech-it]

Dernières offres d'emploi [https://www.free-work.com/fr/tech-it/jobs?contracts=permanent]

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/architecte-technique/architecte-technique-data-et-ia-h-f-6]

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/ingenieur-securite/lead-devsecops-h-f-1]

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [https://www.free-work.com/fr/tech-it/job-mission/business-analyst/business-analyst-rpa-13]

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [https://www.free-work.com/fr/tech-it/jobs/suggested]

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data. Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
<<Faire le point>> [https://www.free-work.com/fr/tech-it/blog/actualites-informatiques/quelles-sont-les-intentions-de-recrutement-tech-pour-2027]

--------------------------------------------------------------------------------

<<Gmes>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

Ils recrutent !
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA. Elle travaille pour EDF ou Generali, des Caraïbes au Canada. L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance. 

Pourquoi pas vous ?
<<Rejoindre la team Bugbusters>> [https://www.free-work.com/fr/companies/g-m-e-s-bugbusters]

--------------------------------------------------------------------------------

Une question ? Allez voir ceux qui l’ont déjà vécue
<<Forum>> [https://www.free-work.com/fr/tech-it/forum/latest]
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
<<Découvrir les échanges>> [https://www.free-work.com/fr/tech-it/forum/latest]

--------------------------------------------------------------------------------

<<Industrie>> [https://www.free-work.com/fr/tech-it/blog/metiers-it/industrie-4-0-et-iot-les-me […]
```

#### 5 — Après strip_urls
*(1823 caractères)*
```
Voir la version en ligne 

<<freework logo>> [

Dernières offres d'emploi [

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data. Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
<<Faire le point>> [

--------------------------------------------------------------------------------

<<Gmes>> [

Ils recrutent !
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA. Elle travaille pour EDF ou Generali, des Caraïbes au Canada. L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance. 

Pourquoi pas vous ?
<<Rejoindre la team Bugbusters>> [

--------------------------------------------------------------------------------

Une question ? Allez voir ceux qui l’ont déjà vécue
<<Forum>> [
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
<<Découvrir les échanges>> [

--------------------------------------------------------------------------------

<<Industrie>> [ […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1877 caractères)*
```
Subject: Dernières opportunités sur Free-Work !
Body: Voir la version en ligne 

<<freework logo>> [

Dernières offres d'emploi [

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data. Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
<<Faire le point>> [

--------------------------------------------------------------------------------

<<Gmes>> [

Ils recrutent !
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA. Elle travaille pour EDF ou Generali, des Caraïbes au Canada. L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance. 

Pourquoi pas vous ?
<<Rejoindre la team Bugbusters>> [

--------------------------------------------------------------------------------

Une question ? Allez voir ceux qui l’ont déjà vécue
<<Forum>> [
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
<<Découvrir les échanges>> [

--------------------------------------------------------------------------------

<<Industrie>> [ […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(658 caractères)*
```
Subject: Dernières opportunités sur Free-Work !
Body: Voir la version en ligne 

<<freework logo>> [

Dernières offres d'emploi [

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [

Découvrez les offres qui correspondent le mieux avec votre profil.
<<👉 Lancer le matching d'offres>> [

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
<<Intention recrutement>> [
Budgets serrés, recrutement […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/13]** — 47 car., 6 mots
```
Subject: Dernières opportunités sur Free-Work !
```

**chunk[2/13]** — 371 car., 58 mots
```
Body: Voir la version en ligne 

<<freework logo>> [

Dernières offres d'emploi [

CDI
Architecte Data & IA
 💶 75k - 90k €⁄an 

 📍Île-de-France
<<Postuler>> [

CDI
Lead Devsecops
 💶 65k - 72k €⁄an 

 📍Île-de-France
<<Postuler>> [

 CDI
Business Analyst
 💶 50k - 65k €⁄an 

 📍Île-de-France
<<Postuler>> [

Découvrez les offres qui correspondent le mieux avec votre profil.
```

**chunk[3/13]** — 178 car., 17 mots
```
<<👉 Lancer le matching d'offres>> [

--------------------------------------------------------------------------------

Quelles sont les intentions de recrutement tech pour 2027 ?
```

**chunk[4/13]** — 176 car., 25 mots
```
<<Intention recrutement>> [
Budgets serrés, recrutements au compte-gouttes : 2027 s’annonce prudente, sauf pour ceux qui maîtrisent la cybersécurité, l’IA, le cloud ou la data.
```

**chunk[5/13]** — 148 car., 23 mots
```
Salaires, compétences clés, marges de négociation : décryptage de ce qui vous attend pour peser dans votre prochain entretien ou votre prochain TJM.
```

**chunk[6/13]** — 131 car., 10 mots
```
<<Faire le point>> [

--------------------------------------------------------------------------------

<<Gmes>> [

Ils recrutent !
```

**chunk[7/13]** — 152 car., 25 mots
```
De la Martinique au Canada, ils chassent les bugs… et les talents
G.m.e.s Bugbusters réunit aujourd’hui près de 40 experts en data, cybersécurité et IA.
```

**chunk[8/13]** — 60 car., 10 mots
```
Elle travaille pour EDF ou Generali, des Caraïbes au Canada.
```

**chunk[9/13]** — 83 car., 13 mots
```
L’équipe grandit et cherche ses prochaines pépites Tech, en CDI comme en freelance.
```

**chunk[10/13]** — 19 car., 4 mots
```
Pourquoi pas vous ?
```

**chunk[11/13]** — 132 car., 9 mots
```
<<Rejoindre la team Bugbusters>> [

--------------------------------------------------------------------------------

Une question ?
```

**chunk[12/13]** — 235 car., 40 mots
```
Allez voir ceux qui l’ont déjà vécue
<<Forum>> [
Quand vous cherchez un retour concret, un ressenti honnête ou un avis basé sur du vécu, le forum Free-Work vous ouvre les portes d’une communauté qui partage ses expériences sans filtre.
```

**chunk[13/13]** — 131 car., 8 mots
```
<<Découvrir les échanges>> [

--------------------------------------------------------------------------------

<<Industrie>> [ […]
```

---

## Email #25
**Subject:** New login to your SpaceXAI account
**label prédit/attendu:** `OTHER` · **confidence:** `0.977`

- Longueur brut: **499** car.
- Longueur full (après clean): **549** car.
- Longueur truncated (600): **549** car.
- Nombre de chunks (sentence): **2**

### Étapes de nettoyage
#### 0 — Body BRUT
*(499 caractères)*
```
Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

#### 1 — Après remove_invisible_chars
*(499 caractères)*
```
Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

#### 2 — Après clean_reply (citations)
*(499 caractères)*
```
Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

#### 3 — Après strip_trailing_signature_block
*(499 caractères)*
```
Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

#### 4 — Après strip_boilerplate
*(499 caractères)*
```
Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

#### 5 — Après strip_urls
*(499 caractères)*
```
Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

#### 6 — FINAL full (Subject + Body) → chunking
*(549 caractères)*
```
Subject: New login to your SpaceXAI account
Body: Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(549 caractères)*
```
Subject: New login to your SpaceXAI account
Body: Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

### Chunks (split_sentences, min_words=4)
**chunk[1/2]** — 480 car., 66 mots
```
Subject: New login to your SpaceXAI account
Body: Hi Hamza,
We're notifying you by email of a new login to your SpaceXAI account:
Time: Wed, 14 Oct 2026 14:33:39 +0000
IP address: 2c0f:f3a0:12b:c9d0:18de:6b20:163d:29d3
Location: Tunis, TN
Browser: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Mobile Safari/537.36
If you notice any suspicious activity on your account, please change your password and enable two-factor authentication.
```

**chunk[2/2]** — 68 car., 10 mots
```
SpaceXAI Team
© 2026 SpaceXAI LLC
For questions contact support@x.ai
```

---

## Email #26
**Subject:** AI Transformation Consultant: Get Ahead on This Business-Critical Curve
**label prédit/attendu:** `OTHER` · **confidence:** `0.828`

- Longueur brut: **3004** car.
- Longueur full (après clean): **2682** car.
- Longueur truncated (600): **691** car.
- Nombre de chunks (sentence): **19**

### Alertes
- ℹ️  Beaucoup de chunks (19) — risque de dilution mean-pool

### Étapes de nettoyage
#### 0 — Body BRUT
*(3004 caractères)*
```
Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value. 

They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in. They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.

You can hear the sighs of relief around the board table as you read, eh?

Want to become that highly sought-after professional?

If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
<https://link.coursera.org/f/a/m00b-d4exMAo1ckUkj0j8g~~/AAQRxRA~/dh32dxMs-CmHEyzlfuqIWDLmsep3Qoad8aTsD3DQYebofre01LL-DsnlLDp1NX5bB-Ng_YGok5cyxMP0fM-RzjX6abJIjfQMEH3WdcCatI3hCZf7AWMAnV-nt7b7ZtVP7qTaH2DeK27JQHVTLGoCARcLiphl_rJoUcDRkHPUwPlDd38YQbrqnBjAJ1K_7KtJAws4qTlChC_0c7zxgB9DJdyBQvLjz4-EHyjLgUztkr22AuYEGN6TS_gW0LvoFlP-POx6BYyKl1YW44lFMZY5WM7rzLoGmaegabnlD4T8Sr8_KxbKp4TdofM0dGwEWdJyvTBdZtonbQaYzS98QLiJIA~~> 
is for you. 

Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need. 

You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.

Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.

You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.

Businesses are hunting for people who can turn AI ambition into business 
results. If you'd like to be one of them, now is the perfect time to get 
started.

Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

#### 1 — Après remove_invisible_chars
*(3004 caractères)*
```
Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value. 

They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in. They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.

You can hear the sighs of relief around the board table as you read, eh?

Want to become that highly sought-after professional?

If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
<https://link.coursera.org/f/a/m00b-d4exMAo1ckUkj0j8g~~/AAQRxRA~/dh32dxMs-CmHEyzlfuqIWDLmsep3Qoad8aTsD3DQYebofre01LL-DsnlLDp1NX5bB-Ng_YGok5cyxMP0fM-RzjX6abJIjfQMEH3WdcCatI3hCZf7AWMAnV-nt7b7ZtVP7qTaH2DeK27JQHVTLGoCARcLiphl_rJoUcDRkHPUwPlDd38YQbrqnBjAJ1K_7KtJAws4qTlChC_0c7zxgB9DJdyBQvLjz4-EHyjLgUztkr22AuYEGN6TS_gW0LvoFlP-POx6BYyKl1YW44lFMZY5WM7rzLoGmaegabnlD4T8Sr8_KxbKp4TdofM0dGwEWdJyvTBdZtonbQaYzS98QLiJIA~~> 
is for you. 

Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need. 

You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.

Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.

You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.

Businesses are hunting for people who can turn AI ambition into business 
results. If you'd like to be one of them, now is the perfect time to get 
started.

Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

#### 2 — Après clean_reply (citations)
*(3004 caractères)*
```
Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value. 

They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in. They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.

You can hear the sighs of relief around the board table as you read, eh?

Want to become that highly sought-after professional?

If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
<https://link.coursera.org/f/a/m00b-d4exMAo1ckUkj0j8g~~/AAQRxRA~/dh32dxMs-CmHEyzlfuqIWDLmsep3Qoad8aTsD3DQYebofre01LL-DsnlLDp1NX5bB-Ng_YGok5cyxMP0fM-RzjX6abJIjfQMEH3WdcCatI3hCZf7AWMAnV-nt7b7ZtVP7qTaH2DeK27JQHVTLGoCARcLiphl_rJoUcDRkHPUwPlDd38YQbrqnBjAJ1K_7KtJAws4qTlChC_0c7zxgB9DJdyBQvLjz4-EHyjLgUztkr22AuYEGN6TS_gW0LvoFlP-POx6BYyKl1YW44lFMZY5WM7rzLoGmaegabnlD4T8Sr8_KxbKp4TdofM0dGwEWdJyvTBdZtonbQaYzS98QLiJIA~~> 
is for you. 

Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need. 

You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.

Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.

You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.

Businesses are hunting for people who can turn AI ambition into business 
results. If you'd like to be one of them, now is the perfect time to get 
started.

Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

#### 3 — Après strip_trailing_signature_block
*(3004 caractères)*
```
Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value. 

They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in. They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.

You can hear the sighs of relief around the board table as you read, eh?

Want to become that highly sought-after professional?

If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
<https://link.coursera.org/f/a/m00b-d4exMAo1ckUkj0j8g~~/AAQRxRA~/dh32dxMs-CmHEyzlfuqIWDLmsep3Qoad8aTsD3DQYebofre01LL-DsnlLDp1NX5bB-Ng_YGok5cyxMP0fM-RzjX6abJIjfQMEH3WdcCatI3hCZf7AWMAnV-nt7b7ZtVP7qTaH2DeK27JQHVTLGoCARcLiphl_rJoUcDRkHPUwPlDd38YQbrqnBjAJ1K_7KtJAws4qTlChC_0c7zxgB9DJdyBQvLjz4-EHyjLgUztkr22AuYEGN6TS_gW0LvoFlP-POx6BYyKl1YW44lFMZY5WM7rzLoGmaegabnlD4T8Sr8_KxbKp4TdofM0dGwEWdJyvTBdZtonbQaYzS98QLiJIA~~> 
is for you. 

Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need. 

You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.

Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.

You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.

Businesses are hunting for people who can turn AI ambition into business 
results. If you'd like to be one of them, now is the perfect time to get 
started.

Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

#### 4 — Après strip_boilerplate
*(3004 caractères)*
```
Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value. 

They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in. They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.

You can hear the sighs of relief around the board table as you read, eh?

Want to become that highly sought-after professional?

If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
<https://link.coursera.org/f/a/m00b-d4exMAo1ckUkj0j8g~~/AAQRxRA~/dh32dxMs-CmHEyzlfuqIWDLmsep3Qoad8aTsD3DQYebofre01LL-DsnlLDp1NX5bB-Ng_YGok5cyxMP0fM-RzjX6abJIjfQMEH3WdcCatI3hCZf7AWMAnV-nt7b7ZtVP7qTaH2DeK27JQHVTLGoCARcLiphl_rJoUcDRkHPUwPlDd38YQbrqnBjAJ1K_7KtJAws4qTlChC_0c7zxgB9DJdyBQvLjz4-EHyjLgUztkr22AuYEGN6TS_gW0LvoFlP-POx6BYyKl1YW44lFMZY5WM7rzLoGmaegabnlD4T8Sr8_KxbKp4TdofM0dGwEWdJyvTBdZtonbQaYzS98QLiJIA~~> 
is for you. 

Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need. 

You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.

Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.

You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.

Businesses are hunting for people who can turn AI ambition into business 
results. If you'd like to be one of them, now is the perfect time to get 
started.

Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

#### 5 — Après strip_urls
*(2595 caractères)*
```
Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value. 

They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in. They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.

You can hear the sighs of relief around the board table as you read, eh?

Want to become that highly sought-after professional?

If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
< 
is for you. 

Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need. 

You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.

Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.

You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.

Businesses are hunting for people who can turn AI ambition into business 
results. If you'd like to be one of them, now is the perfect time to get 
started.

Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(2682 caractères)*
```
Subject: AI Transformation Consultant: Get Ahead on This Business-Critical Curve
Body: Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value. 

They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in. They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.

You can hear the sighs of relief around the board table as you read, eh?

Want to become that highly sought-after professional?

If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
< 
is for you. 

Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need. 

You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.

Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.

You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.

Businesses are hunting for people who can turn AI ambition into business 
results. If you'd like to be one of them, now is the perfect time to get 
started.

Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(691 caractères)*
```
Subject: AI Transformation Consultant: Get Ahead on This Business-Critical Curve
Body: Dear Hamza Moalla,

Many business leaders are scratching their heads. They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.

To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success. 

And they need them now.

Enter the AI Transformation Consultant.

AI Transformation Consultants clear that fog. 

Sitting at the intersection of business and technology, they help business 
leaders see where AI can cre […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/19]** — 156 car., 21 mots
```
Subject: AI Transformation Consultant: Get Ahead on This Business-Critical Curve
Body: Dear Hamza Moalla,

Many business leaders are scratching their heads.
```

**chunk[2/19]** — 116 car., 22 mots
```
They know they should be 
looking at AI, but they're unsure what, how, or where it can add value to 
their business.
```

**chunk[3/19]** — 191 car., 27 mots
```
To resolve this conundrum, they need people who can separate hype from 
opportunity, identify the right use cases, assess organizational readiness, 
and create practical roadmaps for success.
```

**chunk[4/19]** — 23 car., 5 mots
```
And they need them now.
```

**chunk[5/19]** — 39 car., 5 mots
```
Enter the AI Transformation Consultant.
```

**chunk[6/19]** — 45 car., 6 mots
```
AI Transformation Consultants clear that fog.
```

**chunk[7/19]** — 114 car., 18 mots
```
Sitting at the intersection of business and technology, they help business 
leaders see where AI can create value.
```

**chunk[8/19]** — 168 car., 23 mots
```
They evaluate which opportunities are worth pursuing, assess readiness 
across people, processes, and technology, and build the business cases 
needed to secure buy-in.
```

**chunk[9/19]** — 108 car., 16 mots
```
They then create the roadmaps that turn AI 
ambitions into actionable plans that deliver measurable results.
```

**chunk[10/19]** — 72 car., 15 mots
```
You can hear the sighs of relief around the board table as you read, eh?
```

**chunk[11/19]** — 53 car., 7 mots
```
Want to become that highly sought-after professional?
```

**chunk[12/19]** — 172 car., 24 mots
```
If you'd like to position yourself for this emerging business-critical 
role, IBM’s new Enterprise AI Transformation and Consulting Professional 
Certificate
< 
is for you.
```

**chunk[13/19]** — 251 car., 33 mots
```
Designed specifically for business professionals, consultants, analysts, 
project managers, and operations professionals who want to leverage their 
experience in a fast-growing AI career, this program gives you the AI 
transformation skills you need.
```

**chunk[14/19]** — 272 car., 36 mots
```
You'll learn how to:

 * Identify and prioritize AI opportunities

 * Assess organizational readiness

 * Build ROI-focused business cases

 * Develop transformation roadmaps

 * Apply governance frameworks

 * Communicate recommendations that business leaders can act on.
```

**chunk[15/19]** — 343 car., 45 mots
```
Plus, you’ll build portfolio-worthy proof of your AI transformation skills 
and knowledge

Throughout the program, you'll create the kinds of deliverables businesses 
want to see, including:

 * Opportunity assessments

 * Readiness reports

 * Transformation roadmaps

 * ROI business cases

 * Governance plans

 * Executive recommendations.
```

**chunk[16/19]** — 276 car., 39 mots
```
You'll also complete a capstone project in which you develop a complete AI 
transformation strategy for a realistic organization that showcases how 
your strategic thinking, business analysis, and transformation planning 
skills are fine-tuned to the AI focus businesses need.
```

**chunk[17/19]** — 82 car., 13 mots
```
Businesses are hunting for people who can turn AI ambition into business 
results.
```

**chunk[18/19]** — 73 car., 16 mots
```
If you'd like to be one of them, now is the perfect time to get 
started.
```

**chunk[19/19]** — 90 car., 12 mots
```
Explore the new IBM Enterprise AI Transformation and Consulting 
Professional Certific […]
```

---

## Email #27
**Subject:** Tanitjobs.com: Alerte Emploi
**label prédit/attendu:** `OTHER` · **confidence:** `0.920`

- Longueur brut: **1780** car.
- Longueur full (après clean): **1824** car.
- Longueur truncated (600): **648** car.
- Nombre de chunks (sentence): **2**

### Étapes de nettoyage
#### 0 — Body BRUT
*(1780 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 1 — Après remove_invisible_chars
*(1780 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 2 — Après clean_reply (citations)
*(1780 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 3 — Après strip_trailing_signature_block
*(1780 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 4 — Après strip_boilerplate
*(1780 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 5 — Après strip_urls
*(1780 caractères)*
```
Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 6 — FINAL full (Subject + Body) → chunking
*(1824 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(648 caractères)*
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Ca […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/2]** — 943 car., 122 mots
```
Subject: Tanitjobs.com: Alerte Emploi
Body: Bonjour,
Voici les dernières offres d'emploi publiées sur Tanitjobs.com qui pourraient vous intéresser:
magasinier
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
responsable sécurité
Tunis, Monastir, Tunisie
Sotufab Ksar Helal
Project Manager Officer
Tunis, Tunis, Tunisie
PURE BEAUTY LABS
Assistante Administrative – Éligible CIVP
La Soukra, Tunis, Tunisie
PURE BEAUTY LABS
Réviseur Comptable Confirmé(e) en Comptabilité Française
La Charguia 2, Tunis, Tunisie
FINOPTI TN
Technicien en Electricite
Sousse, Monastir, Tunisie
Sotufab Ksar Helal
Comptable - Auditeur
Centre Urbain Nord, Ariana, Tunisie
Cabinet IBC
assisstante commerciale
Monastir, Monastir, Tunisie
ste mouayed produit alimentaire
Responsable Support Informatique
Tunis, Tunis, Tunisie
Lumiere Consulting
Auditeur
Centre Urbain Nord, Tunis, Tunisie
FBZ
ROYAL POOL GROUP RECRUTE !une praticienne en massage bien-être, drainage et Kobido.
```

**chunk[2/2]** — 880 car., 121 mots
```
Soukra, Ariana, Tunisie
ste royal pool group
Collaborateur Comptable (Comptabilité Française)
CHARGUIA 2, Tunis, Tunisie
FINOPTI TN
Comptable Analytique Junior — H/F
Monastir, Monastir, Tunisie
We Work Consulting
Chargé(e) de clientèle
Riadh El Andalous, Ariana, Tunisie
SRP
AGENT D’EMBALLAGE
Aouina , Ariana, Tunisie
Med HR Solutions
Coordinateur SMT
Radès, Ben Arous, Tunisie
Ben Yedder consulting
Chargée Recrutement
Charguia, Ariana, Tunisie
Ben Yedder consulting
Responsable Administratif et Financier (H/F)
Sfax, Sfax, Tunisie
MESSI
Secrétaire Médicale dans un cabinet dentaire
Les Berges du Lac 2, Tunis, Tunisie
cabinet dentaire
Un(e) Commercial(e) B2B & B2C
Sousse, Sousse, Tunisie
Virtide
Si vous ne souhaitez plus recevoir d'alertes par courrier électronique, veuillez vous désabonner en utilisant le lien ci-dessous:
Merci pour votre confiance,
L' équipe Tanitjobs.com
```

---

## Email #28
**Subject:** Five things to make with Grok Imagine
**label prédit/attendu:** `OTHER` · **confidence:** `0.945`

- Longueur brut: **3003** car.
- Longueur full (après clean): **896** car.
- Longueur truncated (600): **657** car.
- Nombre de chunks (sentence): **18**

### Alertes
- ℹ️  Beaucoup de chunks (18) — risque de dilution mean-pool

### Étapes de nettoyage
#### 0 — Body BRUT
*(3003 caractères)*
```
Headshots, product shots, posters, and more. Included with your
plan. Grok ( https://click.email.grok.com/f/a/qF-al3SKJkUl0_Y46r17Ng~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMYfj6NU9NhKr8ud6DLdJb2noIvM83aRByJo-KhD_PqL3h4UPIdb-eUr1dzYjrLf5MmnukHZXFOw0J6zKimvsJ5LiRkdAVrI-9xaWJKsySo3B )
Grok Imagine feature ( https://click.email.grok.com/f/a/TdgHJ4aWYBPSpKQJbnmyQw~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gKDNn9mMt4VzXZnY9rw1FZ7RbGZAJVtcCk1GBqPo9LHJPa-mPCT6wnKQLj5zsIvTYaqdPbGdyTrj2tegMXqZzVTKmbMbkESr1Ky7tL6vpGkA~~ ) Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 
( https://click.email.grok.com/f/a/Kctis879WvIcBdKeaKWWNw~~/AAQRxRA~/GsFICxuvDhN4YIZbAOynqe0givCQxMZhox-RlQcyaGYlnfj6XeB0u7wMf53HZOBhRn--_Z85ofER91iAWhWYOgEayL2BGGAjOVYzVRjlqJEKnIzyzXA1cIoGPiVJEkT8sZ1B00kDW3iluAdjdqpAU3WDw6dcry9GRI3i3RhrA6xG4w6NFad8nI2uuUl0vZLD )
. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 
( https://click.email.grok.com/f/a/Gq5FC9mc6V1l0nzapDeelA~~/AAQRxRA~/pUhxtuUtHqXXfnbwn9JFexGioWs0fiPbERToYMDVsHbxLxjDNCHZYzzWGuN3WgqlW0TUiiQVO5R_uOCwdA1rPSSgc64XPewqrjWw9xHZRgwtJ4OBtNzn0kHkvZoXSA81tix2v87GtXr95rI4wc0nv_MM3DOBtLzHyiyMbfxHX7MzU74Xpyey2boJxzCpyMsv )
. Make listing shots for a product you sell. • Editorial
Product Poster 
( https://click.email.grok.com/f/a/qYpl0Zdrt8LpNgQfqjmuPw~~/AAQRxRA~/j2F4kG4f4txKa1x2J7XoBuik9TvWmp1RYg4nghGVthZgU_1khSVOIFCpsiBWo3TZ0w0lESqLwj0kbstBb4cxsa_V_7FKFRyLWL7-lrshbfUoHfHLmFWS4VCSFEFXevZdiceN2oPeA93U6ie2Z_WhRLCr_oKMGNP6Ygig1o3r-3mXqeEBTDK6PLgC92tScmGD )
. Put your product on a magazine-style poster, headline
included. • Mascot Maker 
( https://click.email.grok.com/f/a/SDtjHblel8vXJnvMejTmOg~~/AAQRxRA~/n2JjGVT-cAgn8ocUokly6hjYFBdKmZiJyKKlHocSAeO9OgiKu7YgwRPEAaIMsOeYbUrmTrP2fOlnpxscg4IVDCy-Ud-EUy3_PFRNvdNmMdQWT87-Sd3fLFt7cwhZJvHpdPvAfAhxZYQEMbdaDi-h6McTGfnUZKA4VynxwIofHwtujISPHW-CfjCWsiTvTXFm )
. Design a character for a brand, a team, or a channel. •
Emoji Creator 
( https://click.email.grok.com/f/a/Jn3ikQInYCW_m4VygZ8FXA~~/AAQRxRA~/5oaD1WBpbMS4tGC5GVTpPkXG-zNSD209B4XQ_O0sASudBeFSd2zv82-uk4a3jmcLMSxiG_tlQKuYwcxcWKRF9PCIa2X6_XgzciIeO_fvtESrt2HndaFt2-wFIBAk6n_bKIBuhE9IoHOelIlRMm6gxQHEuuGtISPRDC5MoEBvy_JepxvBOmo-JWd-C15Hy2EG )
. Make a custom emoji of your own. Find more templates for
icons, merch, and collages in Imagine. Open Imagine →
Open Imagine → ( https://click.email.grok.com/f/a/1gKiIV3D5u7Sb829vYR8nQ~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gRPjYSz0ecufqJraPFXwVHka3cKsOeZEytIByLBhQ30e8_7XxcnKcDjl9IiLo7s0eXJKXqN9RnygAFEgxD5q6qmVVScUvlyEQEdCdPRscI1Q~~ )
Best,
SpaceXAI Team Grok 
( https://click.email.grok.com/f/a/iqt05Mc6zl1kIqRHs6ipWg~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMZKfoXYnvDx0G7GqJHggBt-u55L_gK59EjuxMX42c7BsyQ8fBKK24vR1oyPn9AxSd9_KLJiduy5IeePPYemUMSHwyUoieuAQugKYIyzNr2wo ) […]
```

#### 1 — Après remove_invisible_chars
*(3003 caractères)*
```
Headshots, product shots, posters, and more. Included with your
plan. Grok ( https://click.email.grok.com/f/a/qF-al3SKJkUl0_Y46r17Ng~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMYfj6NU9NhKr8ud6DLdJb2noIvM83aRByJo-KhD_PqL3h4UPIdb-eUr1dzYjrLf5MmnukHZXFOw0J6zKimvsJ5LiRkdAVrI-9xaWJKsySo3B )
Grok Imagine feature ( https://click.email.grok.com/f/a/TdgHJ4aWYBPSpKQJbnmyQw~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gKDNn9mMt4VzXZnY9rw1FZ7RbGZAJVtcCk1GBqPo9LHJPa-mPCT6wnKQLj5zsIvTYaqdPbGdyTrj2tegMXqZzVTKmbMbkESr1Ky7tL6vpGkA~~ ) Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 
( https://click.email.grok.com/f/a/Kctis879WvIcBdKeaKWWNw~~/AAQRxRA~/GsFICxuvDhN4YIZbAOynqe0givCQxMZhox-RlQcyaGYlnfj6XeB0u7wMf53HZOBhRn--_Z85ofER91iAWhWYOgEayL2BGGAjOVYzVRjlqJEKnIzyzXA1cIoGPiVJEkT8sZ1B00kDW3iluAdjdqpAU3WDw6dcry9GRI3i3RhrA6xG4w6NFad8nI2uuUl0vZLD )
. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 
( https://click.email.grok.com/f/a/Gq5FC9mc6V1l0nzapDeelA~~/AAQRxRA~/pUhxtuUtHqXXfnbwn9JFexGioWs0fiPbERToYMDVsHbxLxjDNCHZYzzWGuN3WgqlW0TUiiQVO5R_uOCwdA1rPSSgc64XPewqrjWw9xHZRgwtJ4OBtNzn0kHkvZoXSA81tix2v87GtXr95rI4wc0nv_MM3DOBtLzHyiyMbfxHX7MzU74Xpyey2boJxzCpyMsv )
. Make listing shots for a product you sell. • Editorial
Product Poster 
( https://click.email.grok.com/f/a/qYpl0Zdrt8LpNgQfqjmuPw~~/AAQRxRA~/j2F4kG4f4txKa1x2J7XoBuik9TvWmp1RYg4nghGVthZgU_1khSVOIFCpsiBWo3TZ0w0lESqLwj0kbstBb4cxsa_V_7FKFRyLWL7-lrshbfUoHfHLmFWS4VCSFEFXevZdiceN2oPeA93U6ie2Z_WhRLCr_oKMGNP6Ygig1o3r-3mXqeEBTDK6PLgC92tScmGD )
. Put your product on a magazine-style poster, headline
included. • Mascot Maker 
( https://click.email.grok.com/f/a/SDtjHblel8vXJnvMejTmOg~~/AAQRxRA~/n2JjGVT-cAgn8ocUokly6hjYFBdKmZiJyKKlHocSAeO9OgiKu7YgwRPEAaIMsOeYbUrmTrP2fOlnpxscg4IVDCy-Ud-EUy3_PFRNvdNmMdQWT87-Sd3fLFt7cwhZJvHpdPvAfAhxZYQEMbdaDi-h6McTGfnUZKA4VynxwIofHwtujISPHW-CfjCWsiTvTXFm )
. Design a character for a brand, a team, or a channel. •
Emoji Creator 
( https://click.email.grok.com/f/a/Jn3ikQInYCW_m4VygZ8FXA~~/AAQRxRA~/5oaD1WBpbMS4tGC5GVTpPkXG-zNSD209B4XQ_O0sASudBeFSd2zv82-uk4a3jmcLMSxiG_tlQKuYwcxcWKRF9PCIa2X6_XgzciIeO_fvtESrt2HndaFt2-wFIBAk6n_bKIBuhE9IoHOelIlRMm6gxQHEuuGtISPRDC5MoEBvy_JepxvBOmo-JWd-C15Hy2EG )
. Make a custom emoji of your own. Find more templates for
icons, merch, and collages in Imagine. Open Imagine →
Open Imagine → ( https://click.email.grok.com/f/a/1gKiIV3D5u7Sb829vYR8nQ~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gRPjYSz0ecufqJraPFXwVHka3cKsOeZEytIByLBhQ30e8_7XxcnKcDjl9IiLo7s0eXJKXqN9RnygAFEgxD5q6qmVVScUvlyEQEdCdPRscI1Q~~ )
Best,
SpaceXAI Team Grok 
( https://click.email.grok.com/f/a/iqt05Mc6zl1kIqRHs6ipWg~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMZKfoXYnvDx0G7GqJHggBt-u55L_gK59EjuxMX42c7BsyQ8fBKK24vR1oyPn9AxSd9_KLJiduy5IeePPYemUMSHwyUoieuAQugKYIyzNr2wo ) […]
```

#### 2 — Après clean_reply (citations)
*(3003 caractères)*
```
Headshots, product shots, posters, and more. Included with your
plan. Grok ( https://click.email.grok.com/f/a/qF-al3SKJkUl0_Y46r17Ng~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMYfj6NU9NhKr8ud6DLdJb2noIvM83aRByJo-KhD_PqL3h4UPIdb-eUr1dzYjrLf5MmnukHZXFOw0J6zKimvsJ5LiRkdAVrI-9xaWJKsySo3B )
Grok Imagine feature ( https://click.email.grok.com/f/a/TdgHJ4aWYBPSpKQJbnmyQw~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gKDNn9mMt4VzXZnY9rw1FZ7RbGZAJVtcCk1GBqPo9LHJPa-mPCT6wnKQLj5zsIvTYaqdPbGdyTrj2tegMXqZzVTKmbMbkESr1Ky7tL6vpGkA~~ ) Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 
( https://click.email.grok.com/f/a/Kctis879WvIcBdKeaKWWNw~~/AAQRxRA~/GsFICxuvDhN4YIZbAOynqe0givCQxMZhox-RlQcyaGYlnfj6XeB0u7wMf53HZOBhRn--_Z85ofER91iAWhWYOgEayL2BGGAjOVYzVRjlqJEKnIzyzXA1cIoGPiVJEkT8sZ1B00kDW3iluAdjdqpAU3WDw6dcry9GRI3i3RhrA6xG4w6NFad8nI2uuUl0vZLD )
. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 
( https://click.email.grok.com/f/a/Gq5FC9mc6V1l0nzapDeelA~~/AAQRxRA~/pUhxtuUtHqXXfnbwn9JFexGioWs0fiPbERToYMDVsHbxLxjDNCHZYzzWGuN3WgqlW0TUiiQVO5R_uOCwdA1rPSSgc64XPewqrjWw9xHZRgwtJ4OBtNzn0kHkvZoXSA81tix2v87GtXr95rI4wc0nv_MM3DOBtLzHyiyMbfxHX7MzU74Xpyey2boJxzCpyMsv )
. Make listing shots for a product you sell. • Editorial
Product Poster 
( https://click.email.grok.com/f/a/qYpl0Zdrt8LpNgQfqjmuPw~~/AAQRxRA~/j2F4kG4f4txKa1x2J7XoBuik9TvWmp1RYg4nghGVthZgU_1khSVOIFCpsiBWo3TZ0w0lESqLwj0kbstBb4cxsa_V_7FKFRyLWL7-lrshbfUoHfHLmFWS4VCSFEFXevZdiceN2oPeA93U6ie2Z_WhRLCr_oKMGNP6Ygig1o3r-3mXqeEBTDK6PLgC92tScmGD )
. Put your product on a magazine-style poster, headline
included. • Mascot Maker 
( https://click.email.grok.com/f/a/SDtjHblel8vXJnvMejTmOg~~/AAQRxRA~/n2JjGVT-cAgn8ocUokly6hjYFBdKmZiJyKKlHocSAeO9OgiKu7YgwRPEAaIMsOeYbUrmTrP2fOlnpxscg4IVDCy-Ud-EUy3_PFRNvdNmMdQWT87-Sd3fLFt7cwhZJvHpdPvAfAhxZYQEMbdaDi-h6McTGfnUZKA4VynxwIofHwtujISPHW-CfjCWsiTvTXFm )
. Design a character for a brand, a team, or a channel. •
Emoji Creator 
( https://click.email.grok.com/f/a/Jn3ikQInYCW_m4VygZ8FXA~~/AAQRxRA~/5oaD1WBpbMS4tGC5GVTpPkXG-zNSD209B4XQ_O0sASudBeFSd2zv82-uk4a3jmcLMSxiG_tlQKuYwcxcWKRF9PCIa2X6_XgzciIeO_fvtESrt2HndaFt2-wFIBAk6n_bKIBuhE9IoHOelIlRMm6gxQHEuuGtISPRDC5MoEBvy_JepxvBOmo-JWd-C15Hy2EG )
. Make a custom emoji of your own. Find more templates for
icons, merch, and collages in Imagine. Open Imagine →
Open Imagine → ( https://click.email.grok.com/f/a/1gKiIV3D5u7Sb829vYR8nQ~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gRPjYSz0ecufqJraPFXwVHka3cKsOeZEytIByLBhQ30e8_7XxcnKcDjl9IiLo7s0eXJKXqN9RnygAFEgxD5q6qmVVScUvlyEQEdCdPRscI1Q~~ )
Best,
SpaceXAI Team Grok 
( https://click.email.grok.com/f/a/iqt05Mc6zl1kIqRHs6ipWg~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMZKfoXYnvDx0G7GqJHggBt-u55L_gK59EjuxMX42c7BsyQ8fBKK24vR1oyPn9AxSd9_KLJiduy5IeePPYemUMSHwyUoieuAQugKYIyzNr2wo ) […]
```

#### 3 — Après strip_trailing_signature_block
*(3003 caractères)*
```
Headshots, product shots, posters, and more. Included with your
plan. Grok ( https://click.email.grok.com/f/a/qF-al3SKJkUl0_Y46r17Ng~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMYfj6NU9NhKr8ud6DLdJb2noIvM83aRByJo-KhD_PqL3h4UPIdb-eUr1dzYjrLf5MmnukHZXFOw0J6zKimvsJ5LiRkdAVrI-9xaWJKsySo3B )
Grok Imagine feature ( https://click.email.grok.com/f/a/TdgHJ4aWYBPSpKQJbnmyQw~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gKDNn9mMt4VzXZnY9rw1FZ7RbGZAJVtcCk1GBqPo9LHJPa-mPCT6wnKQLj5zsIvTYaqdPbGdyTrj2tegMXqZzVTKmbMbkESr1Ky7tL6vpGkA~~ ) Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 
( https://click.email.grok.com/f/a/Kctis879WvIcBdKeaKWWNw~~/AAQRxRA~/GsFICxuvDhN4YIZbAOynqe0givCQxMZhox-RlQcyaGYlnfj6XeB0u7wMf53HZOBhRn--_Z85ofER91iAWhWYOgEayL2BGGAjOVYzVRjlqJEKnIzyzXA1cIoGPiVJEkT8sZ1B00kDW3iluAdjdqpAU3WDw6dcry9GRI3i3RhrA6xG4w6NFad8nI2uuUl0vZLD )
. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 
( https://click.email.grok.com/f/a/Gq5FC9mc6V1l0nzapDeelA~~/AAQRxRA~/pUhxtuUtHqXXfnbwn9JFexGioWs0fiPbERToYMDVsHbxLxjDNCHZYzzWGuN3WgqlW0TUiiQVO5R_uOCwdA1rPSSgc64XPewqrjWw9xHZRgwtJ4OBtNzn0kHkvZoXSA81tix2v87GtXr95rI4wc0nv_MM3DOBtLzHyiyMbfxHX7MzU74Xpyey2boJxzCpyMsv )
. Make listing shots for a product you sell. • Editorial
Product Poster 
( https://click.email.grok.com/f/a/qYpl0Zdrt8LpNgQfqjmuPw~~/AAQRxRA~/j2F4kG4f4txKa1x2J7XoBuik9TvWmp1RYg4nghGVthZgU_1khSVOIFCpsiBWo3TZ0w0lESqLwj0kbstBb4cxsa_V_7FKFRyLWL7-lrshbfUoHfHLmFWS4VCSFEFXevZdiceN2oPeA93U6ie2Z_WhRLCr_oKMGNP6Ygig1o3r-3mXqeEBTDK6PLgC92tScmGD )
. Put your product on a magazine-style poster, headline
included. • Mascot Maker 
( https://click.email.grok.com/f/a/SDtjHblel8vXJnvMejTmOg~~/AAQRxRA~/n2JjGVT-cAgn8ocUokly6hjYFBdKmZiJyKKlHocSAeO9OgiKu7YgwRPEAaIMsOeYbUrmTrP2fOlnpxscg4IVDCy-Ud-EUy3_PFRNvdNmMdQWT87-Sd3fLFt7cwhZJvHpdPvAfAhxZYQEMbdaDi-h6McTGfnUZKA4VynxwIofHwtujISPHW-CfjCWsiTvTXFm )
. Design a character for a brand, a team, or a channel. •
Emoji Creator 
( https://click.email.grok.com/f/a/Jn3ikQInYCW_m4VygZ8FXA~~/AAQRxRA~/5oaD1WBpbMS4tGC5GVTpPkXG-zNSD209B4XQ_O0sASudBeFSd2zv82-uk4a3jmcLMSxiG_tlQKuYwcxcWKRF9PCIa2X6_XgzciIeO_fvtESrt2HndaFt2-wFIBAk6n_bKIBuhE9IoHOelIlRMm6gxQHEuuGtISPRDC5MoEBvy_JepxvBOmo-JWd-C15Hy2EG )
. Make a custom emoji of your own. Find more templates for
icons, merch, and collages in Imagine. Open Imagine →
Open Imagine → ( https://click.email.grok.com/f/a/1gKiIV3D5u7Sb829vYR8nQ~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gRPjYSz0ecufqJraPFXwVHka3cKsOeZEytIByLBhQ30e8_7XxcnKcDjl9IiLo7s0eXJKXqN9RnygAFEgxD5q6qmVVScUvlyEQEdCdPRscI1Q~~ )
Best,
SpaceXAI Team Grok 
( https://click.email.grok.com/f/a/iqt05Mc6zl1kIqRHs6ipWg~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMZKfoXYnvDx0G7GqJHggBt-u55L_gK59EjuxMX42c7BsyQ8fBKK24vR1oyPn9AxSd9_KLJiduy5IeePPYemUMSHwyUoieuAQugKYIyzNr2wo ) […]
```

#### 4 — Après strip_boilerplate
*(3003 caractères)*
```
Headshots, product shots, posters, and more. Included with your
plan. Grok ( https://click.email.grok.com/f/a/qF-al3SKJkUl0_Y46r17Ng~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMYfj6NU9NhKr8ud6DLdJb2noIvM83aRByJo-KhD_PqL3h4UPIdb-eUr1dzYjrLf5MmnukHZXFOw0J6zKimvsJ5LiRkdAVrI-9xaWJKsySo3B )
Grok Imagine feature ( https://click.email.grok.com/f/a/TdgHJ4aWYBPSpKQJbnmyQw~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gKDNn9mMt4VzXZnY9rw1FZ7RbGZAJVtcCk1GBqPo9LHJPa-mPCT6wnKQLj5zsIvTYaqdPbGdyTrj2tegMXqZzVTKmbMbkESr1Ky7tL6vpGkA~~ ) Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 
( https://click.email.grok.com/f/a/Kctis879WvIcBdKeaKWWNw~~/AAQRxRA~/GsFICxuvDhN4YIZbAOynqe0givCQxMZhox-RlQcyaGYlnfj6XeB0u7wMf53HZOBhRn--_Z85ofER91iAWhWYOgEayL2BGGAjOVYzVRjlqJEKnIzyzXA1cIoGPiVJEkT8sZ1B00kDW3iluAdjdqpAU3WDw6dcry9GRI3i3RhrA6xG4w6NFad8nI2uuUl0vZLD )
. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 
( https://click.email.grok.com/f/a/Gq5FC9mc6V1l0nzapDeelA~~/AAQRxRA~/pUhxtuUtHqXXfnbwn9JFexGioWs0fiPbERToYMDVsHbxLxjDNCHZYzzWGuN3WgqlW0TUiiQVO5R_uOCwdA1rPSSgc64XPewqrjWw9xHZRgwtJ4OBtNzn0kHkvZoXSA81tix2v87GtXr95rI4wc0nv_MM3DOBtLzHyiyMbfxHX7MzU74Xpyey2boJxzCpyMsv )
. Make listing shots for a product you sell. • Editorial
Product Poster 
( https://click.email.grok.com/f/a/qYpl0Zdrt8LpNgQfqjmuPw~~/AAQRxRA~/j2F4kG4f4txKa1x2J7XoBuik9TvWmp1RYg4nghGVthZgU_1khSVOIFCpsiBWo3TZ0w0lESqLwj0kbstBb4cxsa_V_7FKFRyLWL7-lrshbfUoHfHLmFWS4VCSFEFXevZdiceN2oPeA93U6ie2Z_WhRLCr_oKMGNP6Ygig1o3r-3mXqeEBTDK6PLgC92tScmGD )
. Put your product on a magazine-style poster, headline
included. • Mascot Maker 
( https://click.email.grok.com/f/a/SDtjHblel8vXJnvMejTmOg~~/AAQRxRA~/n2JjGVT-cAgn8ocUokly6hjYFBdKmZiJyKKlHocSAeO9OgiKu7YgwRPEAaIMsOeYbUrmTrP2fOlnpxscg4IVDCy-Ud-EUy3_PFRNvdNmMdQWT87-Sd3fLFt7cwhZJvHpdPvAfAhxZYQEMbdaDi-h6McTGfnUZKA4VynxwIofHwtujISPHW-CfjCWsiTvTXFm )
. Design a character for a brand, a team, or a channel. •
Emoji Creator 
( https://click.email.grok.com/f/a/Jn3ikQInYCW_m4VygZ8FXA~~/AAQRxRA~/5oaD1WBpbMS4tGC5GVTpPkXG-zNSD209B4XQ_O0sASudBeFSd2zv82-uk4a3jmcLMSxiG_tlQKuYwcxcWKRF9PCIa2X6_XgzciIeO_fvtESrt2HndaFt2-wFIBAk6n_bKIBuhE9IoHOelIlRMm6gxQHEuuGtISPRDC5MoEBvy_JepxvBOmo-JWd-C15Hy2EG )
. Make a custom emoji of your own. Find more templates for
icons, merch, and collages in Imagine. Open Imagine →
Open Imagine → ( https://click.email.grok.com/f/a/1gKiIV3D5u7Sb829vYR8nQ~~/AAQRxRA~/o1VVKCwi1dhOVYsNgxAZa75uSfcSDGCqyZtIxZG3e6gRPjYSz0ecufqJraPFXwVHka3cKsOeZEytIByLBhQ30e8_7XxcnKcDjl9IiLo7s0eXJKXqN9RnygAFEgxD5q6qmVVScUvlyEQEdCdPRscI1Q~~ )
Best,
SpaceXAI Team Grok 
( https://click.email.grok.com/f/a/iqt05Mc6zl1kIqRHs6ipWg~~/AAQRxRA~/Gu4PpELGPNqvrK6U_xFdMZKfoXYnvDx0G7GqJHggBt-u55L_gK59EjuxMX42c7BsyQ8fBKK24vR1oyPn9AxSd9_KLJiduy5IeePPYemUMSHwyUoieuAQugKYIyzNr2wo ) […]
```

#### 5 — Après strip_urls
*(843 caractères)*
```
Headshots, product shots, posters, and more. Included with your
plan. Grok 
Grok Imagine feature Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 

. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 

. Make listing shots for a product you sell. • Editorial
Product Poster 

. Put your product on a magazine-style poster, headline
included. • Mascot Maker 

. Design a character for a brand, a team, or a channel. •
Emoji Creator 

. Make a custom emoji of your own. Find more templates for
icons, merch, and collages in Imagine. Open Imagine →
Open Imagine → 
Best,
SpaceXAI Team Grok 
 […]
```

#### 6 — FINAL full (Subject + Body) → chunking
*(896 caractères)*
```
Subject: Five things to make with Grok Imagine
Body: Headshots, product shots, posters, and more. Included with your
plan. Grok 
Grok Imagine feature Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 

. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 

. Make listing shots for a product you sell. • Editorial
Product Poster 

. Put your product on a magazine-style poster, headline
included. • Mascot Maker 

. Design a character for a brand, a team, or a channel. •
Emoji Creator 

. Make a custom emoji of your own. Find more templates for
icons, merch, and collages in Imagine. Open Imagine →
Open Imagine → 
Best,
SpaceXAI Team Grok 
 […]
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(657 caractères)*
```
Subject: Five things to make with Grok Imagine
Body: Headshots, product shots, posters, and more. Included with your
plan. Grok 
Grok Imagine feature Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet. The easiest way to
start is with a template. Pick one, add a photo or a few details,
and Imagine makes the finished image. Here are five to try. •
Professional Headshot 

. Turn a casual photo into a headshot for your profile or bio.
• E-Commerce Photos 

. Make listing shots for a product you sell. • Editorial
Product Poster 

. Put your product on a magazine-style poster, headline
included. • Masco […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/18]** — 97 car., 15 mots
```
Subject: Five things to make with Grok Imagine
Body: Headshots, product shots, posters, and more.
```

**chunk[2/18]** — 24 car., 4 mots
```
Included with your
plan.
```

**chunk[3/18]** — 126 car., 23 mots
```
Grok 
Grok Imagine feature Start from a template in Grok Imagine Grok Imagine now
runs on Image 2.0, our best image model yet.
```

**chunk[4/18]** — 44 car., 9 mots
```
The easiest way to
start is with a template.
```

**chunk[5/18]** — 77 car., 15 mots
```
Pick one, add a photo or a few details,
and Imagine makes the finished image.
```

**chunk[6/18]** — 21 car., 5 mots
```
Here are five to try.
```

**chunk[7/18]** — 27 car., 4 mots
```
•
Professional Headshot 

.
```

**chunk[8/18]** — 60 car., 12 mots
```
Turn a casual photo into a headshot for your profile or bio.
```

**chunk[9/18]** — 23 car., 4 mots
```
• E-Commerce Photos 

.
```

**chunk[10/18]** — 42 car., 8 mots
```
Make listing shots for a product you sell.
```

**chunk[11/18]** — 30 car., 5 mots
```
• Editorial
Product Poster 

.
```

**chunk[12/18]** — 63 car., 9 mots
```
Put your product on a magazine-style poster, headline
included.
```

**chunk[13/18]** — 18 car., 4 mots
```
• Mascot Maker 

.
```

**chunk[14/18]** — 53 car., 11 mots
```
Design a character for a brand, a team, or a channel.
```

**chunk[15/18]** — 19 car., 4 mots
```
•
Emoji Creator 

.
```

**chunk[16/18]** — 32 car., 7 mots
```
Make a custom emoji of your own.
```

**chunk[17/18]** — 62 car., 10 mots
```
Find more templates for
icons, merch, and collages in Imagine.
```

**chunk[18/18]** — 61 car., 11 mots
```
Open Imagine →
Open Imagine → 
Best,
SpaceXAI Team Grok 
 […]
```

---

## Email #29
**Subject:** [GitHub] A first-party GitHub OAuth application has been added to your account
**label prédit/attendu:** `OTHER` · **confidence:** `0.995`

- Longueur brut: **486** car.
- Longueur full (après clean): **424** car.
- Longueur truncated (600): **424** car.
- Nombre de chunks (sentence): **4**

### Étapes de nettoyage
#### 0 — Body BRUT
*(486 caractères)*
```
Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit https://github.com/settings/connections/applications/0120e057bd645470c1ed for more information.

To see this and other security events for your account, visit https://github.com/settings/security-log

If you run into problems, please contact support by visiting https://github.com/contact

Thanks,
The GitHub Team
```

#### 1 — Après remove_invisible_chars
*(486 caractères)*
```
Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit https://github.com/settings/connections/applications/0120e057bd645470c1ed for more information.

To see this and other security events for your account, visit https://github.com/settings/security-log

If you run into problems, please contact support by visiting https://github.com/contact

Thanks,
The GitHub Team
```

#### 2 — Après clean_reply (citations)
*(486 caractères)*
```
Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit https://github.com/settings/connections/applications/0120e057bd645470c1ed for more information.

To see this and other security events for your account, visit https://github.com/settings/security-log

If you run into problems, please contact support by visiting https://github.com/contact

Thanks,
The GitHub Team
```

#### 3 — Après strip_trailing_signature_block
*(470 caractères)*
```
Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit https://github.com/settings/connections/applications/0120e057bd645470c1ed for more information.

To see this and other security events for your account, visit https://github.com/settings/security-log

If you run into problems, please contact support by visiting https://github.com/contact

Thanks,
```

#### 4 — Après strip_boilerplate
*(470 caractères)*
```
Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit https://github.com/settings/connections/applications/0120e057bd645470c1ed for more information.

To see this and other security events for your account, visit https://github.com/settings/security-log

If you run into problems, please contact support by visiting https://github.com/contact

Thanks,
```

#### 5 — Après strip_urls
*(330 caractères)*
```
Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit for more information.

To see this and other security events for your account, visit 

If you run into problems, please contact support by visiting 

Thanks,
```

#### 6 — FINAL full (Subject + Body) → chunking
*(424 caractères)*
```
Subject: [GitHub] A first-party GitHub OAuth application has been added to your account
Body: Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit for more information.

To see this and other security events for your account, visit 

If you run into problems, please contact support by visiting 

Thanks,
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(424 caractères)*
```
Subject: [GitHub] A first-party GitHub OAuth application has been added to your account
Body: Hey hamzamoalla!

A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
Visit for more information.

To see this and other security events for your account, visit 

If you run into problems, please contact support by visiting 

Thanks,
```

### Chunks (split_sentences, min_words=4)
**chunk[1/4]** — 110 car., 16 mots
```
Subject: [GitHub] A first-party GitHub OAuth application has been added to your account
Body: Hey hamzamoalla!
```

**chunk[2/4]** — 148 car., 21 mots
```
A first-party GitHub OAuth application (Git Credential Manager) with gist, repo, and workflow scopes was recently authorized to access your account.
```

**chunk[3/4]** — 27 car., 4 mots
```
Visit for more information.
```

**chunk[4/4]** — 134 car., 22 mots
```
To see this and other security events for your account, visit 

If you run into problems, please contact support by visiting 

Thanks,
```

---

## Email #30
**Subject:** [GitHub] Please verify your device
**label prédit/attendu:** `OTHER` · **confidence:** `0.950`

- Longueur brut: **925** car.
- Longueur full (après clean): **763** car.
- Longueur truncated (600): **654** car.
- Nombre de chunks (sentence): **9**

### Étapes de nettoyage
#### 0 — Body BRUT
*(925 caractères)*
```
Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit https://github.com/settings/security to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit https://docs.github.com/articles/configuring-two-factor-authentication to learn about two-factor authentication.

If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods. See https://docs.github.com/articles/configuring-two-factor-authentication-recovery-methods in the GitHub Help.

Thanks,
The GitHub Team
```

#### 1 — Après remove_invisible_chars
*(925 caractères)*
```
Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit https://github.com/settings/security to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit https://docs.github.com/articles/configuring-two-factor-authentication to learn about two-factor authentication.

If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods. See https://docs.github.com/articles/configuring-two-factor-authentication-recovery-methods in the GitHub Help.

Thanks,
The GitHub Team
```

#### 2 — Après clean_reply (citations)
*(925 caractères)*
```
Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit https://github.com/settings/security to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit https://docs.github.com/articles/configuring-two-factor-authentication to learn about two-factor authentication.

If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods. See https://docs.github.com/articles/configuring-two-factor-authentication-recovery-methods in the GitHub Help.

Thanks,
The GitHub Team
```

#### 3 — Après strip_trailing_signature_block
*(909 caractères)*
```
Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit https://github.com/settings/security to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit https://docs.github.com/articles/configuring-two-factor-authentication to learn about two-factor authentication.

If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods. See https://docs.github.com/articles/configuring-two-factor-authentication-recovery-methods in the GitHub Help.

Thanks,
```

#### 4 — Après strip_boilerplate
*(909 caractères)*
```
Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit https://github.com/settings/security to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit https://docs.github.com/articles/configuring-two-factor-authentication to learn about two-factor authentication.

If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods. See https://docs.github.com/articles/configuring-two-factor-authentication-recovery-methods in the GitHub Help.

Thanks,
```

#### 5 — Après strip_urls
*(713 caractères)*
```
Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit to learn about two-factor authentication.

If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods. See in the GitHub Help.

Thanks,
```

#### 6 — FINAL full (Subject + Body) → chunking
*(763 caractères)*
```
Subject: [GitHub] Please verify your device
Body: Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit to learn about two-factor authentication.

If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods. See in the GitHub Help.

Thanks,
```

#### 7 — FINAL truncated 600 (APPLICATION)
*(654 caractères)*
```
Subject: [GitHub] Please verify your device
Body: Hey hamzamoalla!

A sign in attempt requires further verification because we did not recognize your device. To complete the sign in, enter the verification code on the unrecognized device.

Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised. Visit to create a new, strong password for your GitHub account.

If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account. Visit to learn about two-factor authentication.

If you decide to enable two-factor a […]
```

### Chunks (split_sentences, min_words=4)
**chunk[1/9]** — 66 car., 9 mots
```
Subject: [GitHub] Please verify your device
Body: Hey hamzamoalla!
```

**chunk[2/9]** — 89 car., 14 mots
```
A sign in attempt requires further verification because we did not recognize your device.
```

**chunk[3/9]** — 80 car., 13 mots
```
To complete the sign in, enter the verification code on the unrecognized device.
```

**chunk[4/9]** — 137 car., 23 mots
```
Device: Chrome on Windows
Verification code: 289537

If you did not attempt to sign in to your account, your password may be compromised.
```

**chunk[5/9]** — 63 car., 11 mots
```
Visit to create a new, strong password for your GitHub account.
```

**chunk[6/9]** — 121 car., 17 mots
```
If you'd like to automatically verify devices in the future, consider enabling two-factor authentication on your account.
```

**chunk[7/9]** — 47 car., 6 mots
```
Visit to learn about two-factor authentication.
```

**chunk[8/9]** — 116 car., 18 mots
```
If you decide to enable two-factor authentication, ensure you retain access to one or more account recovery methods.
```

**chunk[9/9]** — 23 car., 5 mots
```
See in the GitHub Help.
```

---
