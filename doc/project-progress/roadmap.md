---
apm_category: roadmap
apm_ref: PROJECT
apm_level: project
created_by: Planner
model: claude-opus-4-7
intended_for: All
created_at: 2026-05-08
updated_at: 2026-05-10
---

# Roadmap — Cognitive Bias Tester

> Ordered list of Epics. Numbered in steps of 10 — insert `E015` between `E010` and `E020` if needed.
> Review and update after each Epic closes (bump `updated_at`).
>
> **Monetized MVP scope = E010 → E130.** Everything from E140 onward is post-MVP and requires explicit Human re-approval before work begins.

---

## Strategic principle — order is non-negotiable

```
Foundation (A)  →  Monetisation Ready (B)  →  Server (C)  →  Public launch + viral (D)
```

Mode 3 (X publishing) **must not** go live before Stripe is integrated and tested in production. Reason: viral publishing without monetisation grows LLM costs without compensating revenue (the "Wordle problem").

---

## Phase A — Foundation (local, dockerised)

### Epic E010 — Repo & Infrastructure Skeleton

**Status:** pending  
**Complexity:** low  
**Depends on:** —  
**Description:** Bootstrap the repository: backend (FastAPI) and frontend (Vue 3 + Vite) skeletons, `docker-compose.yml` with PostgreSQL 16, Alembic, `.env.example`, `.gitignore`, `README.md`, `README.docker.md`, ruff + mypy + pytest pipeline. ADR-001 (PostgreSQL choice) and ADR-002 (ethics framework — list of B2B segments the project refuses to serve).

**MVP gate:** `docker compose up` brings up `backend`, `frontend`, `db`; `backend` `/health` returns 200; ruff + mypy + pytest all green on empty skeleton.

---

### Epic E020 — Data Model & Seed Cases

**Status:** pending  
**Complexity:** medium  
**Depends on:** E010  
**Description:** Domain model: `Case` (English), `CaseTranslation` (per-language), `BiasType`, `Rating`, `User`, `AnswerEvent`, `Subscription` placeholder, `UiString` (English source for UI chrome), `UiStringTranslation` (AI-translated per-locale cache). Alembic initial migration. Repository layer for all entities. Cyclic-buffer logic stub (interface only — fully implemented in E030). Author 25 gold-standard Cases (5 bias types × 5 variants) in English with parametric placeholders; seed initial `UiString` keys from existing `frontend/src/locales/en.json`. Backend endpoint `GET /v1/i18n/{locale}` with hash-based lookup and English fallback (AI translation wired in E040). Side task during this Epic: send first contact e-mail to a Czech university psychology department about future cooperation (informational, no commitment).

**MVP gate:** Migration `alembic upgrade head` succeeds; 25 seeded Cases queryable via repository; `GET /v1/i18n/en` returns all UI string keys with English values; `GET /v1/i18n/fr` returns English fallback for unknown locale; unit tests for cyclic-buffer interface pass.

---

### Epic E030 — LLM Pipeline & Cache

**Status:** pending  
**Complexity:** high  
**Depends on:** E020  
**Description:** ADR-003 (LLM provider comparison and choice) and ADR-004 (embedding model choice). Implement Case generator using selected LLM; embedding-based deduplication on insert; LLM-as-judge validation pass. Cyclic buffer fully implemented with eviction by `(rating_avg, age)` composite ordering. Prompt templates versioned in `backend/src/prompts/` (Git-tracked). Test fixtures use a recorded provider response (no live API calls in CI).

**MVP gate:** Generator + judge produce a new Case end-to-end with one provider; ≥ 90 % of generated Cases pass the judge; deduplication rejects ≥ 95 % of paraphrases in unit tests; LLM cost per Case logged.

---

### Epic E040 — Frontend Skeleton & Mode 1

**Status:** pending  
**Complexity:** medium  
**Depends on:** E030  
**Description:** Vue 3 + Tailwind frontend: anonymous-session landing, single-Case view, answer flow, evaluation, star rating, language switch (browser-detected or user-selected, any locale). Three-tier i18n implementation: `vue-i18n` fed by `GET /v1/i18n/{locale}` (Tier B — UI chrome, any language via DB-backed AI translation); runtime fetch + client cache for Case translations (Tier A); Tier C static strings (landing/legal, cs+en) remain in `frontend/src/locales/`. Wire AI translation call for locales that return `stale_keys`. Bias-resistance score display (per bias type). All Tier C keys human-authored in cs + en.

**MVP gate:** End-to-end flow works locally for both `cs` and `en` UI; switching to a third language (e.g. `sk`) shows English Tier B + LLM-translated Tier A content.

---

## Phase B — Monetisation Ready (still local)

### Epic E050 — Auth, Sessions & GDPR

**Status:** pending  
**Complexity:** medium  
**Depends on:** E040  
**Description:** ADR-006 (auth flow: passwordless magic link). Anonymous session cookie; optional account upgrade by entering e-mail and clicking magic link. Consent capture (analytics on/off, cookies). GDPR endpoints: `POST /v1/me/export`, `DELETE /v1/me/account`. Audit log of consent changes. Privacy Policy + ToS draft (Tier B human-curated, cs + en).

**MVP gate:** User can: register via magic link, see anonymous-history merged into account, export their data as JSON, delete their account. All operations have audit-log entries.

---

### Epic E060 — Payments

**Status:** pending  
**Complexity:** medium  
**Depends on:** E050  
**Description:** ADR-007 (Stripe integration plan). Stripe Checkout subscription, webhook handler with idempotency, `Subscription` entity. Multi-currency: Stripe auto-detect by user country. Single global price 3.99 € / month. Test mode end-to-end with Stripe test cards.

**MVP gate:** Test-mode subscription flow works: free user → Stripe Checkout → webhook → user upgraded → premium feature unlocks → cancellation downgrade.

---

### Epic E070 — Premium Features & Free-Tier Limits

**Status:** pending  
**Complexity:** low  
**Depends on:** E060  
**Description:** Daily limit enforcement (5 Cases / day for free). Premium-only: case history, per-bias resistance score with 30-day trend, on-demand Case generation (free uses cached only). Paywall UX (graceful: "you've reached today's limit, come back tomorrow or upgrade").

**MVP gate:** Free user hits 5/day limit and sees paywall; premium user has no limit; premium downgrade reverts limit immediately.

---

### Epic E080 — Anti-Abuse & Rate Limiting

**Status:** pending  
**Complexity:** low  
**Depends on:** E070  
**Description:** Per-IP rate limit (Redis or in-Postgres token bucket — decide in design). Lightweight cookie-less fingerprint (browser + headers hash, not invasive). hCaptcha or Turnstile on free Case generation. Idempotency key on rating endpoint. Logging of suspected abuse events.

**MVP gate:** Synthetic load test (100 reqs / s from one IP) is shaped to ≤ rate limit; rating duplicate is rejected; captcha is required only for free generation, not for premium.

---

## Phase C — Server (production, beta-private)

### Epic E090 — Production Deploy

**Status:** pending  
**Complexity:** medium  
**Depends on:** E080  
**Description:** ADR-005 (Render.com vs Fly.io decision). HTTPS, custom domain (or temporary `*.onrender.com` / `*.fly.dev`), production Postgres, Sentry integration, structured JSON log shipping, secrets management. CI / CD pipeline that deploys on `main` branch push.

**MVP gate:** Production URL serves the app over HTTPS; deploy from CI succeeds; Sentry captures a deliberately thrown test error; backups configured.

---

### Epic E100 — Analytics, Feature Flags & Beta Access

**Status:** pending  
**Complexity:** low  
**Depends on:** E090  
**Description:** ADR-008 (Plausible vs PostHog). Funnel: anonymous → answered first Case → registered → paying. Feature flag for Mode 3 (default off). Invite-only access (5–10 trusted users) for one week; collect Case quality ratings and feedback.

**MVP gate:** Funnel events visible in dashboard; feature flag toggles Mode 3 endpoints; beta users active for ≥ 7 days; median Case rating ≥ 3.5 / 5.

---

## Phase D — Public Launch + Viral

### Epic E110 — Open Graph Image Generator

**Status:** pending  
**Complexity:** medium  
**Depends on:** E100  
**Description:** Server-side rendered preview images (1200×630) for X cards, embedding the Case question and answer letters A/B/C/D in large brand-styled typography. Image generated on-the-fly with HTTP cache (CDN-friendly headers). Fallback static image for branding.

**MVP gate:** Sharing a Case URL on X, LinkedIn, Threads renders a correct preview image with question text legible at thumbnail size.

---

### Epic E120 — Mode 3: Social Publishing (X)

**Status:** pending  
**Complexity:** high  
**Depends on:** E110  
**Description:** Scheduled publishing pipeline to X (posts via API, fallback to Buffer if API tier insufficient). Cron + queue to schedule posts; anti-duplicate (no Case posted twice within `M` days); deep-link `?case=…&answer=…&utm_source=x` carries attribution. Operator dashboard: "what posts when, with which Case, expected reach". Posting frequency is A/B-tested in this Epic.

**MVP gate:** ≥ 7 unattended days of automated posting; click-through tracked back to specific Cases; deduplication holds in synthetic test of 50 posts.

---

### Epic E130 — Public Launch

**Status:** pending  
**Complexity:** low  
**Depends on:** E120  
**Description:** Switch Stripe to live mode (real charges). Newsletter announcement to whatever list exists. Public posts on ProductHunt + IndieHackers + first wave of X posts via Mode 3. Customer-support inbox monitoring. Daily metrics review for first 14 days.

**MVP gate:** First **real** paying user (not internal test); 14 days of post-launch monitoring with no Sentry-level critical bugs; landing page finalised.

---

# Post-MVP — Phase E (Growth & B2B)

> ⚠ **Each Epic below requires explicit Human re-approval before work begins.**
> Sequencing depends on data from MVP launch (which Mode 1 / Mode 3 metrics moved, which user segment paid).

---

### Epic E140 — Mode 2: Comprehensive Test

**Status:** pending (post-MVP)  
**Complexity:** medium  
**Description:** Fixed-set test, exportable as standalone HTML, parametrisable environment ("school", "fictional cancer research", etc.), in-group comparison statistics. First step toward B2B.

---

### Epic E150 — B2B Custom Environments & White-Label

**Status:** pending (post-MVP)  
**Complexity:** high  
**Description:** Multi-tenant: a company can configure its own environment vocabulary, logo, custom Cases. "Contact Sales" → manual onboarding pipeline. Pricing tier(s) for B2B published.

---

### Epic E160 — Personalisation (Spaced Repetition)

**Status:** pending (post-MVP)  
**Complexity:** medium  
**Description:** Anki-style: identify per-user weak biases, schedule them more frequently, decay schedule for mastered ones.

---

### Epic E165 — PPP-Localised Pricing

**Status:** pending (post-MVP — gated on first 100 paying users)  
**Complexity:** medium  
**Description:** "Price of 2 beers in your country" — manually maintained `country → price` JSON for ~10 markets. Anti-arbitrage policy. Stripe Adaptive Pricing or custom price-list integration.

---

### Epic E170 — Formal Academic Validation

**Status:** pending (post-MVP)  
**Complexity:** high  
**Description:** Formal cooperation agreement with a Czech university psychology department (FF UK / FSS MUNI). Psychometric validation of generated Cases. Joint publication potential. Initial informal contact made during E020.

---

### Epic E180 — Open Data Export & Public Research API

**Status:** pending (post-MVP — gated on ≥ 1 000 active users)  
**Complexity:** medium  
**Description:** Anonymised anonymous-aggregated dataset for researchers. Public read-only API. Open-data licence.

---

### Epic E190 — Persona / Bias Profile Report

**Status:** pending (post-MVP)  
**Complexity:** medium  
**Description:** After 30 Cases, generate a personal "cognitive profile" — shareable, virally attractive (16Personalities-style).

---

## Phase F (deferred, undated)

Items deliberately not yet in the roadmap, listed in `spec.md` Non-Goals: native mobile, multi-LLM abstraction, reverse-engineering manipulation mode, audio podcast, Bias Cards physical product, journaling integrations, additional social networks beyond X.

These will be added to the roadmap if and when post-MVP data justifies them.
