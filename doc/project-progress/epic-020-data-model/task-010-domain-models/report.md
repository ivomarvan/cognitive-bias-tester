---
apm_category: task-report
apm_ref: E020.T010
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Report: E020.T010 — Domain Models + Alembic Migration

## Co bylo implementováno

Přidáno devět SQLAlchemy 2.x modelů pod `backend/src/db/models/` podle `plan.md` § T010 (`Mapped` + `mapped_column`), včetně rezervovaných tabulek `case` a `user`. `models/__init__.py` exportuje všechny třídy pro `Base.metadata` a Alembic. Migrace **`0002_domain_model`**: obsah vychází z **`alembic revision --autogenerate`** (s bind-mountem `alembic/versions` na host), revize přepsána na **`revision = "0002"`**, **`down_revision = "0001"`**, název souboru **`0002_domain_model.py`**. Přidány **jednotkové testy** bez DB v `backend/tests/db/test_models.py` (9 testů + marker `unit`).

## Vstupy a výstupy

- **Přečteno:** `task-010-domain-models/spec.md`, `dod.md`, `epic-020-data-model/plan.md` § T010, `backend/src/db/base.py`, `alembic/env.py`.
- **Vytvořeno:** `backend/src/db/models/*.py` (9 entit), `backend/alembic/versions/0002_domain_model.py`, `backend/tests/db/test_models.py`, tento `report.md`.
- **Změněno:** `backend/src/db/models/__init__.py`.

## Použité metody a rozhodnutí

- **`bias_type.id` a `case.bias_type_id`:** plán uvádí `SmallInteger` pro PK bias type; při `autoincrement` mapuje PostgreSQL / SQLAlchemy kombinaci typicky na **`SERIAL` (= `integer`)**. Aby **`alembic check`** nehlásil nesoulad typů, používá **`Integer`** pro `BiasType.id` a **`case.bias_type_id`** (FK musí odpovídat PK). Funkčně stejné rozmezí ID jako u 32bit celých čísel.
- **Python vs DB `default`:** u declarativního mapování bez dataclass část výchozích hodnot zůstává na `server_default` / doplnění při INSERT; unit testy předávají explicitní hodnoty tam, kde kontrolujeme sémantiku (`User.is_premium`, `Case.source`, `Subscription.status`).
- **Generování migrace:** jednorázový autogenerate uvnitř kontejneru s **`-v repo/backend/alembic:/app/alembic`**, aby vzniklý soubor skončil v gitu (výchozí compose nemountuje `alembic/`).

## Reference do kódu

- `backend/src/db/models/__init__.py:1-24` — importy všech modelů a `__all__`
- `backend/src/db/models/case.py:1-73` — entita `Case` (bez `embedding`)
- `backend/src/db/models/rating.py:1-40` — `CheckConstraint` + `UniqueConstraint`
- `backend/alembic/versions/0002_domain_model.py:1-251` — DDL devíti tabulek, `downgrade`
- `backend/tests/db/test_models.py:1-123` — devět instančních unit testů

## Výsledek regresního testu

✅ V kontejneru: `ruff check`, `ruff format --check`, `mypy src/ alembic/env.py --strict`, `pytest -m "not integration"` — OK.  
✅ `alembic upgrade head`, `alembic check`, `alembic downgrade 0001`, `alembic upgrade head`, `alembic check` — OK (lokální stack s `.env`).  
✅ `bash tests/skeleton/test_t040.sh` — OK.

## Definition of Done

Viz [dod.md](dod.md) — všechna kritéria ✅.

## Ruční ověření (pro Humana)

1. **Závislosti a čistá DB:** `cp .env.example .env` (sladit heslo / `DATABASE_URL`), `docker compose up -d db`, případně `docker compose down -v` pro úplně prázdný svazek.
2. **Migrace:**  
   `docker compose run --rm backend sh -c "cd /app && alembic upgrade head && alembic check"`  
   Očekávání: žádná chyba; `alembic check` vypíše „No new upgrade operations“.
3. **Schéma v Postgresu:**  
   `docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\dt'`  
   Očekávání: tabulky `bias_type`, `case`, `case_translation`, `ui_string`, `ui_string_translation`, `user`, `answer_event`, `rating`, `subscription` (některé názvy mohou být v uvozovkách u `case`/`user` dle klienta).
4. **Kvalita a unit testy (bez integrace):**  
   `docker compose run --rm --no-deps backend sh -c "cd /app && ruff check . && ruff format --check . && mypy src/ alembic/env.py --strict && pytest -m 'not integration' -q"`
5. **Zpětný krok migrace:**  
   `docker compose run --rm backend sh -c "cd /app && alembic downgrade 0001"`  
   poté znovu `alembic upgrade head` a kontrola, že aplikace startuje (`docker compose up -d backend`).

Poznámka: úkolový spec v Context Bundle uváděl **„Do NOT modify: doc/**“**; **`report.md` a vyplněný `dod.md`** jsou zde na výslovnou žádost k uzavření APM úkolu.
