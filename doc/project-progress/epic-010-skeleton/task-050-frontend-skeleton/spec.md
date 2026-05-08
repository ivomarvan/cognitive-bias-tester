---
apm_category: task-spec
apm_ref: E010.T050
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Specification: E010.T050 — Frontend Vue 3 + Vite + Tailwind skeleton + ESLint/Vitest

## Goal

Add the `frontend/` service: multi-stage `Dockerfile`, `package.json` with pinned dependencies, Vue 3 + TypeScript-strict + Tailwind + Pinia + vue-router + vue-i18n skeleton, ESLint and Vitest configured. A minimal landing page renders. Wire frontend into `docker-compose.yml`.

## Inputs

- `.cursor/rules/04-docker-standards.mdc`
- `.cursor/rules/11-vuejs-vite-tailwind.mdc`
- `.cursor/skills/vuejs-dev/SKILL.md`
- T020 outputs: `docker-compose.yml`, `.env.example` with `FRONTEND_PORT`
- T030 may exist by the time this Task runs; if so, append the `frontend` service after the `backend` service in `docker-compose.yml`

## Outputs

- `frontend/Dockerfile` — multi-stage:
  - `dev` (FROM `node:22.11-alpine`): `npm ci`, exposes Vite dev server
  - `build` (FROM `node:22.11-alpine`): `npm ci && npm run build` → `dist/`
  - `production` (FROM `nginx:1.27-alpine`): copies `dist/` to nginx root; pinned base image; non-root user
- `frontend/.dockerignore` — `node_modules`, `dist`, `.vite`, `coverage`, `.env*`, `.git`
- `frontend/package.json` with `engines.node = ">=22.0.0"` and pinned versions of core deps:
  - `vue@^3.5.13`, `vue-router@^4.5.0`, `pinia@^2.3.0`, `vue-i18n@^10.0.5`
  - `tailwindcss@^3.4.14`, `autoprefixer@^10.4.20`, `postcss@^8.4.49`
  - dev: `vite@^5.4.10`, `@vitejs/plugin-vue@^5.2.1`, `typescript@^5.6.3`, `vue-tsc@^2.1.10`, `vitest@^2.1.4`, `@vue/test-utils@^2.4.6`, `eslint@^9.14.0`, `eslint-plugin-vue@^9.30.0`, `@typescript-eslint/parser@^8.13.0`, `@typescript-eslint/eslint-plugin@^8.13.0`, `@vueuse/core@^11.2.0`, `jsdom@^25.0.1`
  - scripts: `dev`, `build`, `preview`, `test`, `lint`, `typecheck`
- `frontend/tsconfig.json` — `"strict": true`, `"noUncheckedIndexedAccess": true`, modern target
- `frontend/vite.config.ts` — Vue plugin, alias `@` → `src/`, port 5173
- `frontend/tailwind.config.ts` — `content: ["./index.html", "./src/**/*.{vue,ts}"]`, default theme, `darkMode: "class"`
- `frontend/postcss.config.cjs` — Tailwind + autoprefixer
- `frontend/eslint.config.js` (flat config) — Vue + TypeScript rules
- `frontend/vitest.config.ts` — `environment: "jsdom"`, globals true
- `frontend/index.html` — standard Vite template, mount `<div id="app">`
- `frontend/src/main.ts` — create app, install Pinia, Router, i18n, mount on `#app`; import `./assets/main.css`
- `frontend/src/App.vue` — root layout; uses `<RouterView />`
- `frontend/src/assets/main.css` — `@tailwind base; @tailwind components; @tailwind utilities;`
- `frontend/src/router/index.ts` — single route `/` → `HomePage`
- `frontend/src/i18n/index.ts` — vue-i18n init reading from `locales/`
- `frontend/src/locales/en.json` — `{"app": {"title": "Cognitive Bias Tester"}, "home": {"heading": "Welcome"}}`
- `frontend/src/locales/cs.json` — translated values
- `frontend/src/pages/HomePage.vue` — `<script setup lang="ts">` + `<template>` with Tailwind classes; uses `t('home.heading')`
- `frontend/src/components/.gitkeep`
- `frontend/src/composables/.gitkeep`
- `frontend/src/stores/.gitkeep`
- `frontend/src/types/.gitkeep`
- `frontend/src/pages/HomePage.test.ts` — Vitest test mounts the page and asserts heading text appears (use `@vue/test-utils`)
- `docker-compose.yml` updated — append `frontend` service:
  - `build: { context: ./frontend, target: dev }`
  - `ports: ["${FRONTEND_PORT:-5173}:5173"]`
  - `volumes: ["./frontend/src:/app/src"]` (dev hot reload)
  - `command: npm run dev -- --host 0.0.0.0`
  - `healthcheck: { test: ["CMD", "wget", "-q", "--spider", "http://localhost:5173/"], interval: 10s, timeout: 5s, retries: 5 }`
  - `restart: unless-stopped`

## Context Bundle

**Files to read:**
- All rule files / skill listed in *Inputs*
- `docker-compose.yml` (after T030 if available; otherwise after T020)
- `.env.example` from T020 (`FRONTEND_PORT` already there)

**Files NOT to modify:**
- `backend/**`, `doc/**`, `.cursor/**`, `LICENSE`
- root `README.md` (T060 finalises READMEs)

**Interfaces from prior Tasks:**
- T020: `docker-compose.yml` baseline and `FRONTEND_PORT` in `.env.example`
- T030 (if already done): the `backend` service entry — append `frontend` after it cleanly

## Dependencies

T020. (Logically independent of T030 — but if T030 is done first, both Tasks share `docker-compose.yml`; Coder edits the same file appending `frontend` after `backend`.)

## Test Specification

- **Happy path:** `npm run build` succeeds (production bundle in `dist/`); `npx vitest run` passes (`HomePage.test.ts`); `npx vue-tsc --noEmit` returns 0; `npx eslint src/` returns 0.
- **Edge case (locale switch):** mount `HomePage.vue` with locale `cs` and assert Czech heading text. Add as a second test in `HomePage.test.ts`.
- **Manual:** `docker compose up frontend` and visit `http://localhost:${FRONTEND_PORT}/` — landing page renders with Tailwind styling visible.

## Definition of Done

See `dod.md`. Summary:
- [ ] `docker compose up frontend` serves landing page on `${FRONTEND_PORT}`
- [ ] `npm run build` succeeds
- [ ] `npx vue-tsc --noEmit` returns 0
- [ ] `npx eslint src/` returns 0
- [ ] `npx vitest run` passes
- [ ] All public composables / utilities have TSDoc
- [ ] Tailwind classes work (visible styling)
- [ ] `vue-i18n` configured with `cs` and `en`
- [ ] All new tests pass; full suite passes (backend + frontend)

## Recommended Coder Model

Composer-2.
