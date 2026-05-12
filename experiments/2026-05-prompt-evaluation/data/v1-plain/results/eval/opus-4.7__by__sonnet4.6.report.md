# Hodnocení sady příkladů: Claude Opus 4.7

**Hodnotitel:** Claude Sonnet 4.6  
**Datum:** 2026-05-10  
**Celkové průměrné skóre:** 85,7 / 100  
**Flagovaných příkladů:** 0 z 40  

---

## Celkové hodnocení

Claude Opus 4.7 produkuje **nejkvalitnější sadu ze všech hodnocených modelů**. Sada se vyznačuje třemi výjimečnými vlastnostmi, které ji odlišují od všech ostatních:

1. **Framing sekce jako jediná systematicky demonstruje obě strany framingového efektu** — každý příklad obsahuje jak biased odpověď volící pozitivní rám, tak biased odpověď volící negativní rám. Tato struktura je edukačně výjimečně cenná.
2. **Celá loss_aversion sekce obsahuje explicitní EV výpočty** přímo ověřitelné z dat v otázce — žádný jiný model nedodal takto konzistentní numerickou podporu.
3. **Anchoring-textbook-02** (intuitivní odhad 8! = 40 320) je mimořádně originální příklad bez předchůdce v ostatních sadách.

Výstup je v češtině a správně používá lokalizované názvy zkreslení (ukotvení, rámování, averze ke ztrátě, konfirmační zkreslení, klam utopených nákladů).

---

## Výsledky podle bias kategorie

| Bias | N | Průměr | Min | Max | use_as_is | needs_edit | needs_rewrite | reject |
|---|---|---|---|---|---|---|---|---|
| anchoring | 8 | 86,6 | 84,5 | 89,0 | 6 | 2 | 0 | 0 |
| framing | 8 | 86,9 | 82,5 | 93,0 | 6 | 2 | 0 | 0 |
| loss_aversion | 8 | 86,4 | 84,0 | 88,5 | 7 | 1 | 0 | 0 |
| confirmation_bias | 8 | 83,1 | 81,0 | 88,5 | 1 | 7 | 0 | 0 |
| sunk_cost_fallacy | 8 | 87,0 | 81,0 | 91,5 | 4 | 4 | 0 | 0 |

---

## Top příklady (gold standard)

1. **sunk_cost_fallacy-own-05** (91,5) — Aplikace 200K€ investováno, odkup za 50K€ nebo dokončení za −10K€: explicitní numerická analýza, silná past, perfektní difficulty 5.
2. **framing-own-05** (93,0) — Pojišťovna A: 19/20 vs pojišťovna B: „o 1 procentní bod nižší než 6 %": genuinně difficulty-5 výpočet, dvě rafinované biased volby.
3. **anchoring-textbook-02** (89,0) — 8! faktoriál intuitivně: mimořádně originální anchor přes prvních pár číslic součinu.
4. **sunk_cost_fallacy-own-04** (90,0) — 5 let doktorátu, 2 zbývají, nabídka vysněné pozice: emocionálně nejsilnější past v celé sadě.

---

## Žádné flagované příklady

Žádný příklad nespadl pod prahové hodnoty pro flagování. Celá sada je nad 80 body — výjimečný výsledek srovnatelný s GPT-5.5 (80,3), ale s vyšším průměrem 85,7.

---

## Výjimečné konstrukční rysy

### 1. Framing: oboustranné biased volby
Všechny framing příklady obsahují alespoň dvě biased možnosti — jednu reagující na pozitivní rám, jednu na negativní. Tato struktura:
- Demonstruje, že framing efekt funguje v **obou směrech**
- Poskytuje kurátorovi bohatší materiál pro výběr
- Je edukačně hodnotnější než jednodirektivní design ostatních modelů

Příklady:
- framing-textbook-01: biased A (program je úspěch) + biased B (400 obětí je nepřijatelné)
- framing-textbook-02: biased A (95 % libové = zdravější) + biased B (5 % tuku = transparentnější)
- framing-own-05: biased A (19/20 = intuitivní spolehlivost) + biased B (odborný jazyk = důvěryhodnost)

### 2. Loss aversion: explicitní EV v každém příkladu
Každý loss_aversion příklad uvádí kompletní EV výpočet přímo v textu odpovědi nebo vysvětlení:
- textbook-01: `0,5·150 − 0,5·100 = +25 €`
- textbook-03: `0,85·1 000 = 850 €`
- own-01: `0,5·100 − 5 = 45 €`
- own-02: `0,6·80 000 + 0,4·35 000 = 62 000 €`
- own-03: `0,7·60 000 + 0,3·30 000 = 51 000 €`
- own-04: `EV držení 4 500 € vs alternativa 5 250 €`
- own-05: `0,05·900 ≈ 45 € vs pojistné 120 €`

### 3. Anchoring: reálné numerické kotvení
Všechny anchoring příklady obsahují konkrétní číselnou kotvu v otázce a srovnávací data pro ověření racionální volby. Žádný jiný model nedodal takto konzistentně kompletní anchoring strukturu.

---

## Systémové slabiny (minoritní)

### 1. Framing tematická blízkost
- framing-textbook-02 (mleté maso, 95 % libové vs 5 % tuk) a framing-own-01 (jogurt, 98 % bez tuku vs 2 % tuk) sdílejí stejnou strukturu i doménu (potraviny + framing složení tuků). Doporučujeme nahradit framing-own-01 příkladem z jiné domény.

### 2. Confirmation bias — nejslabší sekce (průměr 83,1 vs 86–87 u ostatních)
- Textbookové příklady (Wason, 2-4-6, extrovert test) mají nižší subtilitu (průměr sub ≈ 7) než ostatní sekce — klasické psychologické úlohy jsou snáze identifikovatelné jako testy.
- confirmation_bias-own-01: otázka explicitně klade cíl „nejpravdivější obraz", čímž signalizuje správnou odpověď.

### 3. Loss aversion difficulty kalibrace
- loss_aversion-textbook-01 (EV=+25€ z mince): difficulty 2 je mírně podhodnocena — výpočet EV vyžaduje vědomou analýzu (spíše difficulty 3).
- loss_aversion-own-02 (sportovní smlouva, EV=62K): difficulty 2 mírně podhodnocena.

---

## Srovnání s ostatními modely

| Model | Průměr | Flagovaných | REJECT | use_as_is |
|---|---|---|---|---|
| **Claude Opus 4.7** | **85,7** | **0/40** | **0** | **24/40** |
| GPT-5.5 | 80,3 | 0/40 | 0 | 14/40 |
| Claude Sonnet 4.6 | 77,9 | 0/40 | 0 | 0/40 |
| Gemini 3.1 Pro | 75,0 | 3/40 | 2 | 4/40 |
| GPT-4o | 43,8* | 14/16* | 13* | 0/16 |
| GPT-4o-mini | 39,1 | 37/40 | 30 | 0/40 |

\* pouze 16 příkladů z 40 (neúplný soubor)

---

## Doporučení pro kurátora

Tato sada je **nejlepší výchozí základna pro výběr gold examples**. Doporučujeme:

1. **Přijmout bez úprav 24 příkladů** — zejména celou framing, loss_aversion a anchoring sekci.
2. **Drobné úpravy (16 příkladů)** — zejména confirmation_bias sekce (7/8 needs_minor_edit): mírně snížit abstraktnost otázek, přeformulovat own-01 bez explicitního cíle.
3. **Framing-own-01 nahradit** příkladem z nepotravinářské domény (framing-textbook-02 a framing-own-01 jsou strukturálně příliš blízké).
4. **Loss_aversion-textbook-01 a own-02**: zvážit navýšení difficulty na 3 pro přesnější kalibraci.

Celkově je Opus 4.7 sada vhodná k přímé produkci s minimálními editorskými zásahy.
