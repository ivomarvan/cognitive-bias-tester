# Role
Jste expert na kognitivní psychologii, behaviorální ekonomii a návrh vzdělávacího obsahu.

# Úkol
Pro každý typ zkreslení z následujícího seznamu vygenerujte:
- **3 učebnicové příklady** — klasické případy známé z literatury (např. Linda problem, Tverského pricing efekty, Monty Hall, Asijská nemoc atd.). Záměrně chceme klasiku jako kalibrační referenční bod.
- **5 vlastních příkladů**, které se navzájem ani s těmi učebnicovými výrazně nepodobají.

Celkem tedy 8 příkladů na jeden typ zkreslení.

> **Účel tohoto promptu:** výstup neslouží přímo uživatelům aplikace. Slouží jako **kandidátní materiál**, ze kterého lidský autor vybere nejkvalitnější příklady jako vzorové (few-shot) pro finální produkční prompt. Tomu odpovídá kombinace „učebnicové + vlastní" i požadavek na rozmanitou obtížnost.

Seznam typů zkreslení:
1. anchoring — Ukotvení
2. framing — Rámování
3. loss_aversion — Averze ke ztrátě
4. confirmation_bias — Konfirmační zkreslení
5. sunk_cost_fallacy — Klam utopených nákladů

# Kontext a cíle
Cílem příkladů je test, který ověří, zda je uživatel pozorný na obvyklá zkreslení mysli. Při výběru odpovědi ho test konfrontuje s tím, zda očekávanému zkreslení podlehl.

Situace a možnosti musí být navrženy jako **kognitivní past (cognitive trap)**. Záměrně se snažíme uživatele nachytat: jedna (nebo více) z odpovědí musí působit velmi lákavě a intuitivně právě díky danému zkreslení, ačkoliv racionální rozbor ukazuje, že je jiná odpověď objektivně lepší (nebo minimálně stejně dobrá). Racionálních odpovědí může být i více.

> Pole `explanation` v každé možnosti se uživateli zobrazí **až po jeho volbě**, nikdy předem. Lze v něm proto pojmenovat zkreslení.

# Pravidla pro tvorbu příkladů

1. **Rozmanitost situací (mezi 5 vlastními):** Pět vlastních příkladů jednoho typu zkreslení si nesmí být příliš podobné — ani s sebou, ani s 3 učebnicovými. Doménu (běžný nákup, sport, rodinné rozhodování, pracovní pohovor, finance, zdraví, volný čas atd.) volí model sám a uvádí ji v JSON. Domény u 5 vlastních se mohou opakovat — důležitější než variace domény je variace obtížnosti.

2. **Různá obtížnost (povinné rozpětí):** Generujte záměrně příklady s **rozdílnou obtížností v rozsahu 1–5**:
   - 1 = past je při pozornosti zjevná, vhodné pro úvodní motivaci,
   - 2 = snadno přehlédnutelná při zběžném čtení,
   - 3 = vyžaduje vědomou analýzu, středoškolák zvládne do ~30 s,
   - 4 = past je rafinovaná, naletí i pozorný čtenář bez propočtu,
   - 5 = expertní úroveň, vyžaduje explicitní výpočet nebo strukturovanou úvahu.
   U každého příkladu uveďte odhad v poli `difficulty`. V rámci 5 vlastních příkladů jednoho zkreslení musí obtížnosti **skutečně pokrývat rozpětí**, ne se hromadit kolem jedné hodnoty.

3. **Zatajení účelu (jen v question a answer):** V poli `question` ani v poli `answer` nesmí být ani náznak toho, že testujeme kognitivní zkreslení, ani název zkreslení (v žádném pádě, ani opisem). Pole `explanation` toto omezení nemá — zobrazuje se až po volbě.

4. **Objektivní hodnota (nutná podmínka edukace):** Všechny „zkreslené" varianty MUSÍ tvořit kognitivní past. Racionální volba musí být objektivně doložitelná jako logicky, fakticky nebo matematicky nejlepší řešení situace. „Zkreslená" volba přináší suboptimální výsledek, byť lidské intuici připadá přirozená. Bez této tvrdé podmínky se uživatel nemůže ze své chyby reálně poučit.

5. **Označení verdiktu u každé odpovědi:** Každá `option` má pole `verdict ∈ {"rational", "biased", "neutral"}`:
   - `rational` — odpověď, kterou by zvolil pozorný racionální uvažovatel.
   - `biased` — past konkrétně demonstrující daný typ zkreslení.
   - `neutral` — ani jednoznačně racionální, ani projev daného zkreslení (např. defenzivní vyhnutí se rozhodnutí).

6. **Pozice past odpovědi:** V poli `options` umístěte past (`verdict: "biased"`) **náhodně**, ne mechanicky vždy první nebo poslední.

7. **Strukturní rady pro konkrétní zkreslení** (kde to plyne z definice daného zkreslení — jinde ponechte modelu volnost):
   - **anchoring** — `question` musí obsahovat výrazné číslo (kotvu) dříve, než se ptáme na odhad či volbu.
   - **framing** — alespoň dvě možnosti popisují fakticky tutéž situaci, ale jedna pozitivně (zisk, přežití, úspěšnost), druhá negativně (ztráta, úmrtnost, neúspěšnost).
   - **sunk_cost_fallacy** — `question` musí explicitně zmiňovat již vynaloženou investici (čas, peníze, úsilí), která je pro budoucí rozhodnutí fakticky irelevantní.
   - **loss_aversion** a **confirmation_bias** — strukturu volí model. (Tip pro inspiraci, ne pravidlo: loss_aversion často funguje s numerickým srovnáním jistého vs. pravděpodobnostního výsledku se srovnatelnou očekávanou hodnotou (expected value); confirmation_bias často s volbou, jakou informaci hledat či testovat — racionální je hledat *vyvracející* evidenci.)

8. **Vyloučené domény:** Nepoužívejte morálně či politicky nabité scénáře (politika, náboženství, etnicita, sex, drogy, ozbrojené konflikty). Test má působit neutrálně, ne jako test hodnot uživatele.

9. **Kulturní neutralita:** Vyhněte se výhradně českým reáliím, které se ztrácejí v překladu (SIPO, MHD pásmo P, OSVČ-paušál). Scénář má fungovat i pro mezinárodní publikum.

10. **Možnosti odpovědí:** Počet odpovědí u každého příkladu zvolte tak, jak to pro daný typ zkreslení a situaci dává logický smysl (typicky 2–5).

11. **Způsob vysvětlování:** Ke každé možné odpovědi vytvořte stručné vyhodnocení (orientačně do ~30 slov). Ve vyhodnocení neuvádějte obecné vysvětlení kognitivního zkreslení.
    Vysvětlení formulujte takto: „Tato volba je racionální, protože…" nebo „Tato volba ukazuje podlehnutí zkreslení, protože se rozhodujete na základě…". Můžete doplnit: „Jedná se o typ zkreslení: <jen název>." Nikdy nepište, co <jen název> znamená (podrobné vysvětlení dodá aplikace jiným mechanismem).

12. **Délkový rámec:** `question` orientačně do ~60 slov, `answer` do ~15 slov, `explanation` do ~30 slov. Krátké formulace bývají elegantnější; dlouhé bývají manipulativní.

13. **Rodově neutrální tvar:** Používejte buď generické tvary („rozhodl/a jste se"), nebo neosobní vazbu („je třeba zvolit").

# Self-check před výstupem
Před vlastním JSON výstupem ověřte u **každého** příkladu:
- a) past odpověď je intuitivně lákavá při prvním přečtení,
- b) racionální odpověď je objektivně doložitelná (čísly, faktem nebo logikou) — ne jen subjektivně preferovaná,
- c) `question` a `answer` neprozrazují název zkreslení (ani v jiném pádě, ani opisem),
- d) verdikty (`rational` / `biased` / `neutral`) jsou konzistentní s textem `explanation`,
- e) past odpověď není v `options` mechanicky vždy na téže pozici,
- f) u 5 vlastních příkladů obtížnosti `difficulty` skutečně pokrývají rozsah 1–5, ne se hromadí na jedné hodnotě,
- g) scénář není kulturně specifický, morálně či politicky nabitý.

# Výstupní formát
Vygenerujte výsledek jako platný JSON, vhodný pro uložení do samostatného souboru. Výstup musí být ve stejném jazyce, v jakém je napsán tento prompt (čeština). JSON zformátujte tak, aby byl dobře čitelný člověkem (použijte odsazení a zalomení řádků).

Klíčem na nejvyšší úrovni je název zkreslení; hodnotou je seznam (pole) příkladů.

Použijte následující strukturu (počet `options` je proměnlivý):

```json
{
  "_metadata": {
    "model": "Název a verze vašeho modelu (např. Claude 3.5 Sonnet, GPT-4o atd.)",
    "generated_at": "YYYY-MM-DD HH:MM:SS"
  },
  "anchoring": [
    {
      "id": "anchoring-textbook-01",
      "bias": "anchoring",
      "source": "textbook",
      "domain": "nákup",
      "difficulty": 2,
      "question": "Text otázky nebo popis situace.",
      "options": [
        {
          "answer": "Text první možné odpovědi (volby).",
          "verdict": "biased",
          "explanation": "Stručné vysvětlení pro tuto konkrétní volbu."
        },
        {
          "answer": "Text druhé možné odpovědi (volby).",
          "verdict": "rational",
          "explanation": "Stručné vysvětlení pro tuto konkrétní volbu."
        }
        // libovolný další počet možností
      ]
    }
    // další 2 textbook + 5 own příkladů pro anchoring
  ],
  "framing": [
    // 3 textbook + 5 own
  ]
  // další zkreslení v pořadí ze seznamu výše
}
```

**Konvence hodnot:**
- `id` formát: `<bias>-<source>-<NN>`, kde NN je dvouciferné pořadí v rámci dané (bias, source) dvojice. Příklady: `anchoring-textbook-01`, `anchoring-own-03`, `framing-own-05`.
- `source ∈ {"textbook", "own"}` — `textbook` označuje klasický případ z literatury, `own` vlastní vygenerovaný příklad.
- `domain` — krátký český název domény (např. `"nákup"`, `"sport"`, `"rodina"`, `"pracovní pohovor"`, `"finance"`, `"zdraví"`, `"volný čas"`).
- `difficulty ∈ {1, 2, 3, 4, 5}` dle stupnice v pravidle 2.
