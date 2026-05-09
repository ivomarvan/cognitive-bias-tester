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

- [x] ✅ `frontend/Dockerfile` is multi-stage (dev, build, production); each base image pinned
- [x] ✅ Production stage runs nginx as non-root user
- [x] ✅ `frontend/package.json` has `engines.node = ">=22.0.0"`
- [x] ✅ Dependencies: **exact versions** in `package.json` + `package-lock.json` for reproducible builds (spec T050 outputs require pinning; differs from dod text mentioning `^` only)
- [x] ✅ `tsconfig.json` strict mode on
- [x] ✅ Tailwind, Pinia, Router, vue-i18n all initialised in `main.ts`
- [x] ✅ `HomePage.vue` uses Composition API (`<script setup>`) and renders i18n key
- [x] ✅ `docker-compose.yml` `frontend` service has healthcheck and hot-reload bind-mount

## Test Criteria

- [x] ✅ `npm run build` succeeds (dist/ exists)
- [x] ✅ `npx vue-tsc --noEmit` exits 0
- [x] ✅ `npx eslint src/` exits 0
- [x] ✅ `npx vitest run` passes (≥ 2 tests including locale switch)
- [x] ✅ `docker compose up frontend` reaches healthy (with `db`/`backend` up due to `depends_on` from T060 — verified via `tests/skeleton/test_t050.sh`)
- [x] ✅ Full test suite passes — no regressions to backend tests

## Code Quality Criteria

- [x] ✅ No `any` types (explicit `any` in app sources)
- [x] ✅ No `TODO`/`FIXME` left in committed code
- [x] ✅ All public composables / utilities have TSDoc with `@example` — **N/A:** no public composables/utilities yet (only `.gitkeep` under `composables/`); criterion vacuously met
- [x] ✅ No inline `style="..."` in templates — Tailwind only

## Documentation Criteria

- [x] ✅ `report.md` written with all required sections (in Czech)
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-08
