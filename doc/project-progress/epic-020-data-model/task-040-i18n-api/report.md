---
apm_category: task-report
apm_ref: E020.T040
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Report: E020.T040 — i18n API Endpoint

## Co bylo implementováno

Nový router `backend/src/api/i18n.py`: `GET /v1/i18n/{locale}` s modelem `I18nResponse`, závislostí `UiStringRepository` a čistou funkcí `build_i18n_payload` pro řešení fallbacků podle specu (en → vždy zdrojové tituly a prázdné `stale_keys`; jiné locale → chybějící řádek = anglický titul bez stale; shoda hashe = `title_translated`; neshoda = anglický titul + klíč v `stale_keys`). Validace `locale` regulárem z plánu + odmítnutí `/`, `..`, `.`. `main.py` registruje router. Testy: unit na payload + validaci, integrace proti Postgresu s izolovanými řádky `app_title` / `home_heading`.

## Vstupy a výstupy

- **Přečteno:** `task-040-i18n-api/spec.md`, `health.py`, `session.py`, `UiStringRepository`.
- **Vytvořeno:** `backend/src/api/i18n.py`, `backend/tests/api/test_i18n.py`, `backend/tests/api/__init__.py`, `report.md`.
- **Změněno:** `backend/src/main.py`, `doc/.../task-040-i18n-api/dod.md`.

## Použité metody a rozhodnutí

- **`Depends` + Ruff B008:** inline `# noqa: B008` u FastAPI dependency injection (konvence frameworku).
- **Integrace:** `ASGITransport(..., lifespan="on")` aby proběhl stejný start jako v produkci (včetně DB probe z lifespan).

## Reference do kódu

- `backend/src/api/i18n.py` — endpoint, `build_i18n_payload`, `validate_locale_path`
- `backend/src/main.py` — `include_router(i18n_router)`
- `backend/tests/api/test_i18n.py` — unit + integrace

## Výsledek regresního testu

✅ `ruff check`, `ruff format --check`, `mypy src/ --strict`, `pytest -m "not integration"` v kontejneru backend OK. Integrační sada vyžaduje běžící Postgres a `alembic upgrade head` v souladu s repozitářem (CI workflow).

## Definition of Done

Viz [dod.md](dod.md).
