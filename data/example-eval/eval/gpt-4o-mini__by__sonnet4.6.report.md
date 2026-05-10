# Hodnocení sady příkladů: GPT-4o-mini

**Hodnotitel:** Claude Sonnet 4.6  
**Datum:** 2026-05-10  
**Celkové průměrné skóre:** 39,1 / 100  
**Flagovaných příkladů:** 37 z 40  

---

## Celkové hodnocení

GPT-4o-mini (identifikován v metadatech jako "GPT-4.0") produkuje **závažně defektní výstup** s rozsáhlými systémovými chybami, které zasahují celé bias sekce. Sada **není vhodná jako zdroj gold examples** a vyžaduje kompletní přepis.

---

## Výsledky podle bias kategorie

| Bias | N | Průměr | Min | Max | use_as_is | needs_edit | needs_rewrite | reject |
|---|---|---|---|---|---|---|---|---|
| anchoring | 8 | 24,4 | 17,5 | 34,5 | 0 | 0 | 0 | 8 |
| framing | 8 | 43,6 | 12,0 | 65,0 | 0 | 1 | 0 | 7 |
| loss_aversion | 8 | 28,6 | 24,0 | 39,0 | 0 | 0 | 0 | 8 |
| confirmation_bias | 8 | 49,1 | 44,5 | 53,5 | 0 | 0 | 0 | 8 |
| sunk_cost_fallacy | 8 | 49,4 | 46,0 | 62,5 | 0 | 2 | 0 | 6 |

---

## Kritické systémové chyby

### 1. Anchoring — kompletní selhání designu (8/8 REJECT)
**Celá anchoring sekce má prohozené verdikty.** Ve všech 8 příkladech platí: biased volba je číslo NIŽŠÍ než kotva, rational volba je KOTVA SAMA. To je přesně opačně — racionální chování by mělo ignorovat kotvu, nikoli ji přijmout.

Příklady chyb:
- textbook-01: kotva 500 Kč, biased=300 Kč, rational=500 Kč → rational JE kotva
- own-03: průměr 800 Kč, biased=600 Kč, rational=800 Kč → rational JE historický průměr (sám kotvou)
- own-05: konkurent +20 %, biased=+10 %, rational=+20 % → rational kopíruje konkurenta (kotvu)

Navíc anchoring-textbook-02 ("80 % přežití, kolik zemře?") zcela nedemonstruje anchoring — biased i rational odpovědi jsou matematicky totožné.

### 2. Framing — chybějící struktura + prohozené verdikty (7/8 REJECT)
- 5 z 8 framing příkladů prezentuje **jedinou statistiku** bez alternativní formulace. Strukturní požadavek framing (dvě formulace téhož výsledku) není splněn.
- framing-own-01, framing-own-03, framing-own-04: verdikty prohozeny — "racionální" odpověď je ta, která přijímá pozitivní rám.
- framing-textbook-03: **zakázaná doména** (politika, daně). Navíc obě odpovědi jsou labeled "biased" — žádná rational možnost neexistuje.

### 3. Loss aversion — chybějící datová podpora (8/8 REJECT)
6 z 8 loss_aversion příkladů neuvádí klíčová data pro ověření racionální volby:
- "invest with 70% profit" — chybí výše profitu, nelze spočítat EV
- "pay 2000 Kč for health checkup" — chybí pravděpodobnost a výše komplikací
- "bet again after lottery win" — podmínky nové sázky nejsou specifikovány

### 4. Confirmation bias — příliš generické (8/8 REJECT)
Všechny příklady jsou abstraktní bez konkrétní hypotézy nebo scénáře:
- "Věříte, že investice je skvělá..." bez specifikace jaká investice
- "Věříte, že dieta funguje..." bez konkrétní diety
Obtížnost nelze kalibrovat na generická přesvědčení.

### 5. Sunk cost — nejlepší sekce, ale stále slabá
Sunk_cost_fallacy má nejvyšší skóre (průměr 49,4), ale stále nesplňuje kritéria:
- Příklady uvádějí sunk cost implicitně nebo nedostatečně explicitně
- Chybí kvantifikace (čísla) pro porovnání alternativ
- Difficulty distribution: **chybí úroveň 1** (own-01=2, own-05=2 — duplicate)

---

## Jediný hodnotný příklad

**framing-own-05** (65,0): "5 % vs. 6 % s 1% poplatkem" — jedinou korekní framing příklad v celé sadě. Ekvivalence 5 % = 6 %−1 % je přesná a racionální volba je doložitelná.

---

## Doporučení

Sada není vhodná pro výběr gold examples. Doporučujeme přegenerovat celý soubor s jasnějšími instrukcemi pro GPT-4o-mini, zejména:
1. Anchoring: explicitně vysvětlit, že rational odpověď musí ignorovat kotvu, ne ji přijmout
2. Framing: vyžadovat dvě formulace TÉHOŽ výsledku v jedné otázce
3. Loss aversion: vyžadovat explicitní EV čísla v každé otázce
4. Povinné pravidlo: žádná politická témata
