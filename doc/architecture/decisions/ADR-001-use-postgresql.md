# ADR-001: PostgreSQL jako primární databáze

**Stav**: Přijato

**Datum**: 2026-05-08

## Kontext

Produkt ukládá postup uživatelů, Cases, záznamy LLM cache, hodnocení a příslušná metadata. Projektová specifikace (`doc/project-progress/spec.md`, **Klíčová technická rozhodnutí** — řádek **3**, **Databáze**) se zavazuje k **PostgreSQL 16 v Dockeru** pro vývojové i produkční prostředí, s odůvodněním zahrnujícím `JSONB` pro flexibilní Case payload a volitelné fulltextové vyhledávání.

Potřebujeme souběžný přístup, odolné ACID transakce a ověřenou migrační strategii, jak bude obsah a provoz růst. SQLite je lákavý pro lokální prototypy, ale stává se úzkým hrdlem při workloadech s více writery a pro operační nástroje sdílené mezi prostředími.

## Rozhodnutí

Použít **PostgreSQL 16** jako primární databázi, spouštěnou lokálně přes **Docker Compose**, a cílit na stejnou major verzi v produkci, aby chování schématu a dotazů bylo konzistentní napříč prostředími.

## Zvažované alternativy

- **SQLite (file-backed)** — zamítnuto pro MVP: sémantika jednoho writera a omezená souběžnost při webovém provozu; slabší fit pro víceinstanční API a background workery. Přijatelné pro jednorázové experimenty, ne pro hlavní aplikační store uvedený v `spec.md` řádek 3.
- **Managed MySQL/MariaDB** — životaschopné, ale týmový standard a zdokumentované projektové rozhodnutí se soustředí na PostgreSQL 16; přechod by vyžadoval přehodnocení JSON/query předpokladů a náklady na přizpůsobení bez zřejmého přínosu pro tuto codebase.

## Důsledky

- **Pozitivní:** Silná souběžnost, bohaté SQL + `JSONB`, ověřené migrační nástroje (např. Alembic) a soulad s `spec.md` a infrastrukturními rozhodnutími.
- **Negativní:** Lokální vývojáři musí spouštět Docker (nebo ekvivalentní Postgres instanci), což je projektovou Docker politikou pro víceslužbovou práci již vyžadováno.
