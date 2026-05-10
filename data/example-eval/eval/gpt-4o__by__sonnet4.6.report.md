# Hodnocení sady příkladů: GPT-4o

**Hodnotitel:** Claude Sonnet 4.6  
**Datum:** 2026-05-10  
**Celkové průměrné skóre:** 43,8 / 100 *(pouze ze 16 dostupných příkladů)*  
**Flagovaných příkladů:** 14 z 16  

---

## ⚠️ KRITICKÉ UPOZORNĚNÍ: Neúplný soubor

**Soubor obsahuje pouze 2 ze 5 požadovaných bias kategorií** (anchoring a framing). Chybí:
- `loss_aversion` (8 příkladů)
- `confirmation_bias` (8 příkladů)
- `sunk_cost_fallacy` (8 příkladů)

Celkem je k dispozici pouze **16 z 40 příkladů** (40 %). Hodnocení je proto neúplné a statistiky nelze srovnávat s ostatními modely na stejné bázi.

---

## Celkové hodnocení (z dostupných 16 příkladů)

Ze 16 dostupných příkladů je **14 flagovaných** (87,5 %). Sada vykazuje závažné problémy v obou přítomných sekcích. Celkový průměr 43,8 / 100 je hluboko pod použitelnou úrovní.

---

## Výsledky podle bias kategorie

| Bias | N | Průměr | Min | Max | use_as_is | needs_edit | needs_rewrite | reject |
|---|---|---|---|---|---|---|---|---|
| anchoring | 8 | 40,4 | 23,0 | 60,5 | 0 | 2 | 0 | 6 |
| framing | 8 | 47,1 | 30,5 | 68,0 | 0 | 1 | 0 | 7 |
| loss_aversion | — | — | — | — | — | — | — | — |
| confirmation_bias | — | — | — | — | — | — | — | — |
| sunk_cost_fallacy | — | — | — | — | — | — | — | — |

---

## Kritické problémy v anchoring sekci (6/8 REJECT)

### Systémová chyba: biased a rational verdikty
Podobně jako u gpt-4o-mini, i zde se vyskytují příklady s prohozenenými nebo nelogickými verdikty:

- **anchoring-own-01**: Letadlo first class (3000 USD) vs. economy (500 USD). Biased = economy, rational = first class "pokud oceníte komfort". **Economy je zpravidla racionální volba** — verdikty jsou prohozeny nebo zcela chybně zdůvodněny.
- **anchoring-own-05**: Operace 95% úspěšnost — biased = "5% riziko" (matematicky správná odpověď!), rational = "celé zdraví pacienta". Příklad nedemonstruje anchoring a biased odpověď je fakticky správná.
- **anchoring-textbook-02**: Aukce se vyvolávací cenou 1M — rational = "pod 1M", biased = "nad 1M". V aukcích výsledek překračuje vyvolávací cenu běžně; rational není doložitelná.
- **anchoring-textbook-01**: Hotel 200 USD → 150 USD — rational = "příliš drahé pro budget". To není anchoring reasoning — jde o budget constraint.

### Pozitivní příklady:
- **anchoring-own-02** (60,5): Dům 800K → po inspekci 700K — správná struktura, byť domain je anglicky.
- **anchoring-own-04** (57,0): Učebnice 50K → 30K — jednoduchý, ale funkční příklad.

---

## Kritické problémy ve framing sekci (7/8 REJECT)

### Systémový problém: chybějící druhá formulace
7 z 8 framing příkladů prezentuje **jednu statistiku** a ptá se na její interpretaci (pozitivně vs. negativně). Strukturní požadavek framing — že **alespoň dvě možnosti popisují tutéž situaci jednou pozitivně, jednou negativně** — není splněn.

Vzor: "90 % úspěšnost léčby → biased = uzdravení jisté, rational = existuje 10% riziko."

Toto není framing bias — je to jen interpretace jednoho čísla z různých perspektiv. Chybí rozhodovací kontext a alternativní formulace.

### Výjimka:
- **framing-own-05** (68,0): "5 % vs. 6 % s 1% poplatkem" — jediný příklad s plnohodnotnou framing strukturou. Ekvivalence je přesná.

---

## Srovnání s gpt-4o-mini

Obě sady sdílí podobné systémové problémy v anchoring a framing. GPT-4o mírně lépe skóruje v framing (průměr 47 vs. 44), ale sdílí stejnou konceptuální chybu v anchoring designu. GPT-4o navíc neposkytl chybějící 3 sekce, takže celkový obraz je ještě horší.

---

## Doporučení

Sada není vhodná pro výběr gold examples — ani z 16 dostupných příkladů, ani jako základ pro doplnění chybějících sekcí. Doporučujeme:
1. Přegenerovat celý soubor s GPT-4o s explicitnějšími instrukcemi
2. Ověřit, proč soubor skončil po framing sekci (možný timeout nebo kontext limit)
3. Pokud je dostupný GPT-4o s delším kontextovým oknem, zkusit celý prompt znovu
