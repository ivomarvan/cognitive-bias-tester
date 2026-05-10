# Hodnocení sady příkladů: GPT-5.5

**Hodnotitel:** Claude Sonnet 4.6  
**Datum:** 2026-05-10  
**Celkové průměrné skóre:** 80,3 / 100  
**Flagovaných příkladů:** 0 z 40  

---

## Celkové hodnocení

GPT-5.5 je **nejkvalitnější sada ze srovnávaných modelů**. Všechny sekce jsou strukturálně korektní, verdikty jsou konzistentní a racionální odpovědi jsou objektivně doložitelné. Příklady mají přirozený tón a realistické scénáře napříč doménami.

Klíčová silná stránka je **explicitnost dat** — anchoring sekce vždy uvádí konkrétní kotevní číslo i srovnávací data; loss_aversion sekce explicitně uvádí EV výpočty; sunk_cost sekce vždy explicitně zmiňuje nevratnou investici.

Jedinou systematickou slabinou je **nadhodnocení obtížnosti ve framing sekci** — většina příkladů jsou variace na "X% pozitivně = Y% negativně", jejichž ekvivalence je při vědomém čtení relativně rychle viditelná, přesto jsou označeny jako difficulty 4–5.

---

## Výsledky podle bias kategorie

| Bias | N | Průměr | Min | Max | use_as_is | needs_edit | needs_rewrite | reject |
|---|---|---|---|---|---|---|---|---|
| anchoring | 8 | 81,9 | 72,5 | 89,0 | 2 | 6 | 0 | 0 |
| framing | 8 | 76,3 | 71,0 | 82,5 | 0 | 8 | 0 | 0 |
| loss_aversion | 8 | 80,8 | 75,5 | 84,5 | 3 | 5 | 0 | 0 |
| confirmation_bias | 8 | 82,4 | 75,5 | 87,0 | 5 | 3 | 0 | 0 |
| sunk_cost_fallacy | 8 | 83,1 | 78,5 | 87,0 | 4 | 4 | 0 | 0 |

---

## Top příklady (vhodné k přímému použití)

1. **anchoring-textbook-03** (89,0) — nemovitost 520K vs. tržní 410–430K: plně doložitelná kotva i racionální volba, přirozený scénář.
2. **sunk_cost_fallacy-own-05** (87,0) — software migrace 120K sunk vs. 90K alternativa: explicitní numerické srovnání, silná profesionální past.
3. **confirmation_bias-own-05** (87,0) — analýza dat, selektivní zastavení u příznivého segmentu: výborná difficulty-5 s věrohodnou profesionální pastí.

---

## Žádné flagované příklady

Žádný příklad nespadl pod prahové hodnoty pro flagování. Toto je jediná sada v testu bez flagovaných příkladů.

---

## Systémový problém: kalibrace difficulty ve framing

Všechny framing "own" příklady (own-01 až own-05) jsou variace na formát "X % = Y % vyjádřeno jinak":
- own-01: 99% uptime = 1% downtime (difficulty 1 → spíše 2)
- own-02: 80% dokončí = 20% nedokončí (difficulty 2 → OK)
- own-03: 95% pokryje = 5% spoluúčast (difficulty 3 → OK)
- own-04: 70% udrží = 30% opustí (difficulty 4 → spíše 2–3)
- own-05: 6/10 překoná = 4/10 nepřekoná index (difficulty 5 → spíše 3)

Všechny jsou správné jako framing příklady, ale obtížnostní škála není věrně podána. Pro difficulty 4–5 by bylo vhodné použít složitější scénáře (např. absolutní vs. relativní riziko, NNT, kombinace více statistik).

---

## Pozitivní vzory hodné replikace

- **Anchoring s explicitními tržními daty:** Každý anchoring příklad uvádí kotvu I srovnávací benchmark (tržní ceny, historické průměry, odborné odhady). To je vzorová praxe.
- **Loss aversion s EV:** Všechny loss_aversion příklady uvádí explicitní EV výpočet — edukačně i evaluačně je to gold standard.
- **Sunk cost explicitní zmínka:** Každý sunk_cost příklad explicitně uvádí nevratnou investici v otázce — přesně dle pravidla.
- **Confirmation bias s falsifikací:** Příklady systematicky testují schopnost hledat vyvracející evidenci, ne jen hledat potvrzení.

---

## Doporučení pro kurátora

Tato sada je **nejvhodnější ze všech srovnávaných** jako základ pro gold examples. Doporučujeme:

1. Přijmout bez úprav 14+ příkladů (confirmation_bias a sunk_cost sekce).
2. Provést drobné úpravy difficulty ve framing own příkladech (snížit difficulty 4→2–3, 5→3).
3. Zvážit rozšíření framing sekce o komplexnější framing vzory pro difficulty 4–5 (viz doporučení výše).
