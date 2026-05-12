# Popisy kognitivních zkreslení

Textové popisy kognitivních zkreslení ve dvou jazycích.

## Účel

Tyto soubory slouží dvěma účelům:

1. **Podklad pro hodnocení příkladů** — při ruční kurátorské revizi příkladů v
   `experiments/2026-05-prompt-evaluation/data/curated/` slouží jako referenční popis
   toho, co by kvalitní příklad měl ilustrovat.

2. **Obsah pro aplikaci** — každá otázka zobrazuje konkrétní vysvětlení odpovědi
   (součást příkladu). Tyto soubory poskytují obecné vysvětlení celého zkreslení,
   které se zobrazí jako doplněk (např. informační bublina). Budou načteny do DB
   jako UI překlad (`source_hash`-invalidated, viz `GENERATION_CONCEPT.md`).

## Struktura

```
data/biases/
├── README.md
├── supported/              ← zkreslení implementovaná v aktuální verzi aplikace
│   ├── anchoring.en.md
│   ├── anchoring.cs.md
│   ├── framing.en.md
│   ├── framing.cs.md
│   ├── loss_aversion.en.md
│   ├── loss_aversion.cs.md
│   ├── confirmation_bias.en.md
│   ├── confirmation_bias.cs.md
│   ├── sunk_cost_fallacy.en.md
│   └── sunk_cost_fallacy.cs.md
└── not-yet-supported/      ← připravené popisy pro budoucí rozšíření aplikace
```

## Formát souborů

Každý soubor obsahuje:
- **Definici** — jedno klíčové tvrzení vystihující podstatu zkreslení
- **Jak to funguje** — psychologický mechanismus (2–3 věty)
- **Příklady z běžného života** — 4 konkrétní příklady
- **Jak se bránit** — 4 praktické rady

Soubory se záměrně nepřekládají automaticky — obecné vysvětlení zkreslení vyžaduje
přirozeně znějící formulaci, ne strojový překlad.

## Přidání nového zkreslení

1. Vytvořte `supported/<slug>.en.md` a `supported/<slug>.cs.md`.
2. Slug musí odpovídat hodnotám `bias_type` v databázi a v seed datech.
3. Po schválení textů proveďte migraci do DB (tabulka UI překladů).
