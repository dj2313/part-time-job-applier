#PRD: Minijob Auto-Apply Agent Overview Agent finds Berlin cafes/restaurants. Auto-applies minijobs. Notifies via Telegram. Goal Automate minijob applications. Save manual search time. Target Berlin food/service businesses. ### In Scope

Discover Berlin cafes/restaurants via **OSM**. Crawl sites for job/contact pages. AI decides: form or email. Auto-fill+submit forms (Playwright). Auto-send emails (Gmail **SMTP**) + CV. Telegram notify per attempt. Dedupe applied places.

Out of Scope

LinkedIn/Indeed/job boards. **CAPTCHA**-protected forms. Multi-step applications. Phone-based outreach.

### Tech Stack

Python 3.11, Playwright, Groq **API**, Gmail **SMTP**, Telegram Bot **API**, Overpass **API**. Architecture (files)

config.py — env vars, bbox, keywords, paths profile.json — your data, CV path, positions discovery.py — Overpass query → places.json crawler.py — finds Jobs/Bewerbung/Kontakt page decision.py — Groq: form vs email, field mapping cover_letter.py — Groq: short German message apply_form.py — Playwright fill+submit apply_email.py — Gmail **SMTP** send+CV notifier.py — Telegram status messages main.py — orchestrator, dedupe via applied.json

Non-Functional

Free/low-cost APIs only. Daily cron via GitHub Actions. Best-effort form fill, failures logged.

Risks

Partial **OSM** coverage. Form-fill unreliable per site. Generic msgs may feel spammy.

### Success Metrics

Applications sent/week. Telegram log per attempt. Zero duplicate applications.