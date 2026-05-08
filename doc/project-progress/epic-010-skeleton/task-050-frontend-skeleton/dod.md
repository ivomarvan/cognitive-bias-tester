---
apm_category: dod
apm_ref: E010.T050
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Definition of Done: E010.T050 — Frontend Vue 3 + Vite + Tailwind skeleton

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [ ] `frontend/Dockerfile` is multi-stage (dev, build, production); each base image pinned
- [ ] Production stage runs nginx as non-root user
- [ ] `frontend/package.json` has `engines.node = ">=22.0.0"`
- [ ] All deps pinned with `^` major-stable ranges (per `11-vuejs-vite-tailwind.mdc`)
- [ ] `tsconfig.json` strict mode on
- [ ] Tailwind, Pinia, Router, vue-i18n all initialised in `main.ts`
- [ ] `HomePage.vue` uses Composition API (`<script setup>`) and renders i18n key
- [ ] `docker-compose.yml` `frontend` service has healthcheck and hot-reload bind-mount

## Test Criteria

- [ ] `npm run build` succeeds (dist/ exists)
- [ ] `npx vue-tsc --noEmit` exits 0
- [ ] `npx eslint src/` exits 0
- [ ] `npx vitest run` passes (≥ 2 tests including locale switch)
- [ ] `docker compose up frontend` reaches healthy
- [ ] Full test suite passes — no regressions to backend tests

## Code Quality Criteria

- [ ] No `any` types
- [ ] No `TODO`/`FIXME` left in committed code
- [ ] All public composables / utilities have TSDoc with `@example`
- [ ] No inline `style="..."` in templates — Tailwind only

## Documentation Criteria

- [ ] `report.md` written with all required sections (in Czech)
- [ ] Code references in report point to correct files and line numbers

---

**Filled by Coder:** <model-name>, <YYYY-MM-DD>
