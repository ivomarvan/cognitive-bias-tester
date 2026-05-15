# ADR-005: Simulační widget pro ověření pravděpodobnostních tvrzení

**Stav**: Nápad / Backlog
**Datum**: 2026-05-15

## Kontext

Příklady demonstrující averzi ke ztrátě a další zkreslení opírající se o pravděpodobnosti
(hody mincí, kostky, loterie) obsahují tvrzení jako „očekávaná hodnota je +5 €". Část uživatelů
tato tvrzení nezpochybňuje, ale část — říkejme jim *nevěřící Tomáši* — chce čísla empiricky ověřit.

Pro tuto skupinu je textový výpočet nedostatečný: „Proč by mince padla přesně 50:50?" Simulace
může tuto pochybnost odstranit a zároveň přidat zážitkovou vrstvu, která správné rozhodnutí
internalizuje jinak než čtení vzorce.

Vedlejší přínos: simulace může demonstrovat **Gambler's Fallacy** — uživatel, který hodil pět
pannen za sebou, může empiricky ověřit, zda je šesté hození ovlivněno minulými výsledky.

## Návrh: SimulationWidget komponenta

Vue komponenta `<SimulationWidget>` dostupná jako `case_type: "simulation"` v `ui_hint`,
nebo jako volitelné rozšíření za `global_explanation` u stávajících textových příkladů.

### Dva módy

**Mód A — Jednotlivé pokusy**

Uživatel hází simulovanou mincí / kostkou opakovaně. Po každém hodu se zobrazí:
- výsledek hodu
- kumulativní statistika (počet hodů, průměrný výsledek, průběžné EV)
- „teplotní" vizualizace konvergence k teoretické hodnotě

Uživatel musí provést statisticky dostatečný počet pokusů (konfigurovatelný práh,
např. 30 nebo 50 hodů), aby byl povolen přechod dál. Pokud předčasně odejde,
zobrazí se varování o nedostatečném vzorku.

**Mód B — Dávkový experiment**

Uživatel jedním kliknutím spustí N simulovaných pokusů (konfigurovatelné, např. 1 000).
Výsledek se zobrazí jako histogram + souhrnná statistika.

**Kombinace módů (doporučeno):**
Nejdřív pár jednotlivých hodů → pak tlačítko „simuluj 1 000×". Tento přechod
od prožitku k statistice je pedagogicky nejsilnější.

### Rozšíření schématu `ui_hint`

```json
"ui_hint": {
  "case_type": "simulation",
  "component": "SimulationWidget",
  "experiment": {
    "type": "coin",
    "sides": [
      { "label": "panna", "probability": 0.5, "payoff": 150 },
      { "label": "orel",  "probability": 0.5, "payoff": -100 }
    ]
  },
  "modes": ["individual", "batch"],
  "batch_size": 1000,
  "min_individual_trials": 30,
  "reveal_text_cs": "Po 1 000 hodech: průměrný výsledek ≈ +25 € na hod. Matematika funguje — i když jedna ztráta bolí víc než stejný zisk těší."
}
```

### Kandidátní příklady

| Příklad | Zkreslení | Přínos simulace |
|---|---|---|
| `loss_aversion-textbook-01` (mince: +150/−100) | Averze ke ztrátě | Empirické ověření EV = +25 € |
| `loss_aversion-own-01` (los: +20/−5) | Averze ke ztrátě | Empirické ověření EV = +5 € |
| `loss_aversion-own-05` (pojistka) | Averze ke ztrátě | Ověření nevýhodnosti pojistky (EV = −35,50 €) |

## Výhody

- Nízká implementační náročnost (pure JS/Vue, žádný backend)
- Oslovuje empiricky orientované uživatele, kteří textovým výpočtům nedůvěřují
- Internalizace EV prožitkem, ne pouze čtením
- Snadno rozšiřitelné na kostky, karty nebo libovolné diskrétní rozdělení

## Nevýhody / rizika

- Může odvést pozornost od kognitivního zkreslení k čisté statistice
- Nutnost frámovat simulaci explicitně jako „ověření předpokladu", ne jako hlavní obsah
- Přidává UI komplexitu — widget musí být vizuálně přehledný i na mobilu

## Stav a další kroky

Tento ADR je čistě plánovací — **žádná implementace zatím**. Zvážit při implementaci
interaktivních komponent (viz ADR-004). Prioritizovat po dokončení datové pipeline
(roadmap kroku 1–7, viz `experiments/2026-05-prompt-evaluation/README.md`).
