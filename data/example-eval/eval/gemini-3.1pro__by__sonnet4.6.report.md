# Hodnocení sady příkladů: Gemini 3.1 Pro

**Hodnotitel:** Claude Sonnet 4.6  
**Datum:** 2026-05-10  
**Celkové průměrné skóre:** 75,0 / 100  
**Flagovaných příkladů:** 3 z 40  

---

## Celkové hodnocení

Gemini 3.1 Pro generuje strukturálně korektní příklady s přirozeným jazykem a dobrými narativními scénáři. Nejsilnější sekcí je **sunk_cost_fallacy** (průměr 82,0), kde všechny příklady splňují strukturní požadavek (utopené náklady explicitně v otázce) a biased volby jsou přirozené. Rovněž **confirmation_bias** a **loss_aversion** jsou nadprůměrné.

Systémová slabina leží v **kalibraci obtížnosti** — vlastní příklady se příliš hromadí na hodnotách 3–4 a krajní hodnoty (1 a 5) jsou buď nedostatečně naplněné nebo výrazně nadhodnocené. Druhá slabina je v **sekci framing**, kde se vyskytují matematické nepřesnosti a jeden příklad s nestandardní strukturou.

---

## Výsledky podle bias kategorie

| Bias | N | Průměr | Min | Max | use_as_is | needs_edit | needs_rewrite | reject |
|---|---|---|---|---|---|---|---|---|
| anchoring | 8 | 71,3 | 55,0 | 81,5 | 0 | 4 | 3 | 1 |
| framing | 8 | 67,4 | 53,0 | 83,0 | 0 | 1 | 5 | 2 |
| loss_aversion | 8 | 76,6 | 53,0 | 88,5 | 1 | 5 | 0 | 2 |
| confirmation_bias | 8 | 77,9 | 64,5 | 87,5 | 2 | 4 | 2 | 0 |
| sunk_cost_fallacy | 8 | 82,0 | 74,0 | 87,0 | 1 | 7 | 0 | 0 |

---

## Top příklady (vhodné k přímému použití)

1. **loss_aversion-own-04** (88,5) — ledniška + prodloužená záruka: EV opravy (200 Kč) vs. cena pojistky (3 000 Kč) je explicitně v otázce, vzorová past i doložitelnost.
2. **confirmation_bias-own-05** (87,5) — marketingová kampaň a korelace vs. kauzalita: silná past (grafy ukazující korelaci jsou přirozené), difficulty 5 přesná.
3. **sunk_cost_fallacy-textbook-01** (87,0) — kino: gold standard, všechny strukturní požadavky splněny vzorně.

---

## Flagované příklady (vyžadují pozornost)

| ID příkladu | Skóre | Doporučení | Hlavní důvod |
|---|---|---|---|
| **anchoring-textbook-02** | 55,0 | needs_major_rewrite | `cognitive_trap=5 (<6)`: "rodné číslo" je česko-slovenský kulturně specifický pojem; biased odpověď popisuje efekt meta-analyticky místo ho demonstrovat. |
| **framing-own-03** | 53,0 | reject | Dva články popisují různé veličiny (relativní snížení rizika vs. absolutní šance) — matematicky inkonzistentní; past nemá správnou strukturu. |
| **loss_aversion-own-02** | 53,0 | reject | Otázka "Proč to děláte?" — meta-analytický rámec eliminuje subtilitu; příklad popisuje chování místo aby ho vyvolával. |

---

## Systémové problémy

### 1. Kalibrace obtížnosti u vlastních příkladů
- `anchoring-own-04` (difficulty 4) a `anchoring-own-05` (difficulty 5) jsou fakticky difficulty 2–3.
- `framing-own-05` (difficulty 5) je přímé 90 % = not blocking 10 %, fakticky difficulty 2.
- `loss_aversion-own-05` (difficulty 4) je fakticky difficulty 2–3.

### 2. Framing sekce — matematické chyby
- `framing-own-02`: 99 % uptime ≠ 3,5 dne výpadku (99 % = 3,65 dne). Racionální odpověď tvrdí ekvivalenci, která je fakticky nepřesná.
- `framing-own-03`: "50% snížení rizika" a "50% šance na nemoc s očkováním" jsou kompatibilní jen při 100% základním riziku — nereálný předpoklad.

### 3. Zakázaná doména
- `confirmation_bias-textbook-02`: explicitně politický kontext ("politické opatření"). Rule adherence = 0.

### 4. Strukturální anomálie ve framing
- `framing-textbook-03` (opt-in/opt-out): příklad popisuje jedno systémové uspořádání místo dvou formulací téhož výsledku.
- `framing-own-04`: racionální odpověď má meta-analytický tón ("Vybírá si...") místo přímé volby.

---

## Doporučení pro kurátora

**Přijmout bez úprav (3 příklady):** loss_aversion-own-04, confirmation_bias-own-05, sunk_cost_fallacy-textbook-01.

**Přijmout s drobnými úpravami (~20 příkladů):** Většina sunk_cost a loss_aversion příkladů — opravit délky vysvětlení, drobné formulační přesnosti.

**Přepsat (cca 12 příkladů):** Zejména anchoring-textbook-02, všechny problematické framing příklady.

**Odmítnout (3 příklady):** framing-own-03, loss_aversion-own-02, a pokud nelze opravit: confirmation_bias-textbook-02 (politická doména).
