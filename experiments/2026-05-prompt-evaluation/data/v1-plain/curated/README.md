# Selected Good Examples

Ruční výběr příkladů z generačního experimentu (2026-05) jako základ pro few-shot prompt.

## Struktura

```
selected_good_examples/
├── anchoring/          — 6 příkladů (tier: good)
├── framing/            — 8 příkladů (tier: good)
├── loss_aversion/      — 8 příkladů (tier: good)
├── confirmation_bias/  — 3 příklady (tier: good)
├── sunk_cost_fallacy/  — 6 příkladů (tier: good)
└── borderline/
    ├── anchoring/          — 2 příklady (needs_minor_edit u obou hodnotitelů)
    ├── confirmation_bias/  — 5 příkladů (nejslabší sekce Opusu)
    └── sunk_cost_fallacy/  — 2 příklady
```

## Formát souboru

Každý soubor `<model>__<id>.json` obsahuje tři klíče:

| Klíč | Obsah |
|---|---|
| `example` | Původní vygenerovaný příklad (otázka, odpovědi, verdikty) |
| `evaluation` | Hodnocení dvěma modely: `sonnet4.6` a `gemini3.1pro` |
| `selection` | `tier` (good/borderline), `source_model`, `note` |

## Kritéria výběru

**Tier `good`** — příklad je přímo nebo téměř použitelný:
- Alespoň jeden hodnotitel doporučil `use_as_is`, nebo
- Oba hodnotitelé skórovali ≥ 84 a doporučili `needs_minor_edit`

**Tier `borderline`** — příklad vyžaduje drobné přeformulování:
- Oba hodnotitelé dali `needs_minor_edit` se skóre 81–84
- Vhodné pro ruční úpravu a zařazení do few-shot promptu

## Zdroj

Všechny příklady v tomto výběru pocházejí z generátoru **Claude Opus 4.7** (nejlepší model dle experimentu — průměr 85.5–85.7 / 100, 0 odmítnutých).

Hodnotitelé: Claude Sonnet 4.6 a Gemini 3.1 Pro.

## Poznámka k disagreementu

Dva příklady mají výrazně odlišná hodnocení:
- **framing-own-05**: Sonnet 93.0 vs Gemini 73.5 — Gemini vadí formulace "o 1 procentní bod nižší než 6 %", Sonnet oceňuje matematickou přesnost difficulty-5. Po drobné přeformulaci pojišťovny B bude příklad bezpečně v tier good.
- **loss_aversion-textbook-01**: Sonnet 84 (needs_minor_edit, difficulty podhodnocena) vs Gemini 90 (use_as_is).

## Postup ručního procházení

1. Projdi `anchoring/`, `framing/`, `loss_aversion/` — tyto sekce jsou nejsilnější.
2. Přesuň soubory, které nechceš použít, do podadresáře `rejected/`.
3. Z `borderline/` vezmi ty, které jsou po drobné úpravě použitelné.
4. Výsledek = few-shot sada pro Prompt A (generace příkladů s placeholdery).
