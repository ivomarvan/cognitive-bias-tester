# Zkušenosti s formulací příkladů kognitivních zkreslení

Tento dokument zachycuje poznatky z ruční tvorby a revize příkladů (v1-plain, jaro 2026).
Je přímým vstupem pro v2 generovací prompt — LLM musí tato pravidla zohledňovat.

---

## 1. Kognitivní past musí být prožita, ne popsána

Špatně: *„Kolo štěstí se zastavilo na čísle 65. Jaké procento zemí OSN je afrických?"*
Lépe: Interaktivní komponenta, kde uživatel kolo opravdu roztočí — viz `curated/interactive/`.

**Pravidlo:** Pokud příklad funguje jen tehdy, když uživatel nevědomě přijme kotvu / rám / tlak,
textový popis tento efekt oslabuje nebo zcela eliminuje. Pro silné demonstrace zvažovat
`case_type: interactive` nebo `multi_step` (viz ADR-004).

---

## 2. Marže rozhodnutí určuje sílu pasti

**Loss aversion — příklad:**

| Výhra | Cena | EV | Efekt averze ke ztrátě |
|---|---|---|---|
| 100 € | 5 € | +45 € | Slabý — bet je tak výhodný, že ho skoro každý vezme |
| 20 € | 5 € | +5 € | Silný — jistá ztráta 5 € váží stejně jako pravděpodobný zisk |

**Pravidlo:** Těsná marže (EV blízko nule, ale kladné) maximalizuje kognitivní past.
Příliš výhodná hra past eliminuje — racionální odpověď je pak triviální.

---

## 3. Výpočty patří do `explanation` u VŠECH options, nikdy do `answer`

Špatně (answer): *„Variantu B — průměrná hodnota 62 000 € převyšuje 50 000 €."*
Správně (answer): *„Variantu B — variabilní smlouva má statisticky vyšší výsledek."*
Správně (explanation biased): *„...strach z propadu psychologicky převáží EV=62 000 € > 50 000 €..."*
Správně (explanation rational): *„...0,6·80 000 + 0,4·35 000 = 62 000 € > 50 000 €."*
Správně (explanation neutral): *„...dostupná čísla (EV=62 000 €) ke srovnání postačují."*

**Pravidlo:** Výpočet v `answer` prozradí, která volba je „školsky správná", a zruší pedagogický efekt.
Výpočet musí být ve `explanation` **u všech options** — ne jen u rational — protože uživatel
vysvětlení čte teprve po výběru a v každém kontextu potřebuje vidět, jak čísla fungují.

**Přesnost výpočtu:** Vždy ověřit aritmetiku. Příklad: pojistka s 90% krytím a ztrátou 900 €
dává EV krytí = 0,05 × 810 = 40,50 €, nikoli 0,05 × 900 = 45 €.

### 3a. Pravidla transparentnosti výpočtu — pro v2 prompt

Každé číslo v `explanation` musí být **trasovatelné** zpět k číslu uvedenému v `question`.
Nikdy neskákej přes mezikroky — i triviální součet musí být explicitní.

**Derivační řetězec musí být úplný:**

```
❌  "EV krytí = 5 % × 810 € = 40,50 €"          ← odkud je 810?

✅  "celková ztráta = 750 + 150 = 900 €;
     krytí 90 % → 0,9 × 900 = 810 €;
     EV = 5 % × 810 = 40,50 €"
```

**Pravidla:**
1. Každá položka ze `question` použitá ve výpočtu musí být v `explanation` zmíněna jménem.
2. Součty více položek (např. záloha + nákupy) se vždy rozepíší: `750 + 150 = 900 €`.
3. Procentní přepočet se uvede explicitně: `90 % → 0,9 × 900`.
4. Pokud vznikne mezivýsledek (810 €), pojmenuj ho: `krytí pojistky = 810 €`.
5. Finální EV je vždy na posledním řádku derivace, ne uprostřed.

**Volitelně v `neutral` explanation — robustnostní test:**
Ukaž, že závěr platí i při změně klíčového předpokladu:
`"I při 2× vyšším riziku (10 %) by EV krytí (81 €) stále nepřekročilo cenu pojistky (120 €)."`
Tím se odstraní legitimní únikový argument „ale co kdyby..." a příklad pedagogicky posílí.

---

## 4. Ekvivalence nesmí být explicitní v zadání

**Framing — příklad:**
Špatně: *„Program zachrání 200 z 600 osob / Program nechá zemřít 400 z 600 osob."*
Lépe: *„Program zachrání 200 osob. / Při programu zemře 400."*

**Pravidlo:** Jakmile zadání explicitně uvede stejný jmenovatel (600 z 600), ekvivalence je
transparentní a past nefunguje. Formulace musí ekvivalenci skrývat — uživatel ji musí sám odhalit.

---

## 5. Neutrální odpověď nesmí odhalit past

Špatně (neutral): *„Obě kliniky popisují tutéž statistiku různými slovy — vyberu jinak."*
— tato odpověď prozrazuje klíčový poznatek, který má přijít až při reveal.

Správně (neutral): *„Vyžádám si absolutní počty — procenta bez kontextu nestačí."*
— je epistemicky obezřetná, ale nezmiňuje ekvivalenci.

**Pravidlo:** Neutrální odpověď musí být ospravedlnitelná jako rozumná volba bez toho,
aby odkryla, proč jsou biased odpovědi chybné.

---

## 6. Biased odpověď musí znít přirozeně

Špatně: *„Odmítám operaci, 10 % lidí umírá!"* — přehnaná, neautentická.
Správně: *„Kliniku B vyloučím — varování, že 10 % zemře, zní příliš riskantně."* — realistická.

**Pravidlo:** Biased odpověď musí být ta, kterou by si naivní, ale inteligentní člověk
skutečně vybral. Pokud vypadá iracionálně na první pohled, past nefunguje.

---

## 7. Scénář porovnání: dvě nové nabídky, ne zůstat vs. odejít

Špatně: *„Stávající stabilní místo vs. nová firma."*
Správně: *„Dostali jste dvě pracovní nabídky. Která je výhodnější?"*

**Pravidlo:** Volba „zůstat vs. odejít" přináší konfundující faktory nesouvisející s finančním
rozhodnutím (loajalita, sociální vztahy, jistota, averze ke změně). Porovnání dvou nových
nabídek tyto faktory eliminuje a soustředí uživatele čistě na numerické rozhodnutí.

---

## 7a. Temporální struktura příjmu jako vrstvená averze ke ztrátě

Efektivní past lze vytvořit rozdělením roku na dvě části s různou strukturou odměn:

- **H1 (první půlrok):** jen základní plat — garantovaný okamžitý pokles oproti alternativě
- **H2 (druhý půlrok):** základní plat + odměna s určitou pravděpodobností

**Výhody:**
- Dvě oddělené složky averze ke ztrátě: okamžitá (vidíš ji každou výplatou) + nejistá (budoucí)
- Výplata vždy měsíčně — žádná ambiguita o tom, kdy a jak jsou peníze vypláceny
- Kulturně neutrální — bonusy jsou standard v ČR i v zahraničí
- Realistické pro moderní pracovní trh (onboarding bez plné odměny v prvních měsících)

**Vzorová čísla:**
- Firma A: 3 500 €/m (jistých 42 000 €/rok)
- Firma B: 3 000 €/m základ; H1 bez odměn; H2: 70% × +2 500 €/m
- EV Firmy B: 18 000 + 28 500 = 46 500 € (+4 500 € vs. A)
- Past: H1 garantovaný pokles −500 €/m + 30% riziko H2 bez odměny (36 000 € < 42 000 €)

---

## 8. Hodnotné vs. bezcenné protihodnoty

**Loss aversion:** Výhra musí být v hotovosti nebo v jednoznačně ocenitelném zboží.
Dárek „v hodnotě X €" má nejistou subjektivní hodnotu — výpočet EV pak nesedí.

**Pravidlo:** Pokud příklad pracuje s číselnou hodnotou, musí být hodnota jednoznačná
a pro uživatele objektivně ohodnotitelná.

---

## 8. Uzavření prostoru pravidel (confirmation bias)

Wasonův 2-4-6 úkol funguje v laboratoři, protože experimentátor implicitně garantuje:
- Pravidlo platí pro celou třídu trojic (ne pro jednu konkrétní)
- Pravidlo lze popsat jednou větou o číselném vztahu

Bez tohoto omezení je prostor pravidel nekonečný (Lagrangeova interpolace, Goodmanův problém)
a žádná testovací strategie není formálně nadřazená jiné.

**Pravidlo:** Příklady využívající discovery tasks musí v zadání explicitně uzavřít třídu pravidel.
Alternativně: přejít na `multi_step` formát, kde se hodnotí empirické chování (počet
potvrzujících vs. vyvracejících testů), nikoli formální optimalita.

---

## 9. Konfirmační zkreslení — textové příklady: biased strategie musí být kognitivně pohodlnější

Biased odpověď = test, který **potvrdí** aktuální hypotézu (8-10-12 při H₀ = „+2").
Rational odpověď = test, který **překvapivě vyvrátí nebo rozšíří** hypotézu (5-10-20).

Biased volba musí být intuitivně přirozenější: *„Ověřím, že mám pravdu."*

---

## 10. Difficulty kalibrace

| Situation | Difficulty |
|---|---|
| Biased odpověď zní jednoznačně špatně i bez přemýšlení | 1 |
| Biased odpověď zní přirozeně, rational vyžaduje vědomou úvahu | 2–3 |
| Rational vyžaduje výpočet nebo netriviální inferenci | 4 |
| Prostor odpovědí je sám o sobě epistemicky složitý | 5 |

**Pravidlo:** Čím těsnější marže nebo čím méně zřejmá ekvivalence, tím vyšší difficulty.
Difficulty by měla odpovídat skutečnému kognitivnímu úsilí, ne povrchové složitosti textu.

---

## 11. Počet odpovědí

- **3 odpovědi** (biased + rational + neutral) jsou optimální pro většinu příkladů.
- **4 odpovědi** jsou vhodné, pokud existují dvě odlišné biased reakce (pozitivní vs. negativní rámování).
- **2 odpovědi** (biased + rational, bez neutral) jsou vhodné pro přímé binární rozhodnutí.

Neutral odpověď se přidává, pokud existuje legitimní obezřetná reakce, která není ani
biased, ani plně racionální — „Chci víc informací" nebo „Deleguju rozhodnutí".

---

## 13. Schéma příkladu — pole `global_explanation`

Finální schéma příkladu obsahuje pole `global_explanation` mezi `question` a `options`.

**Obsah:** sdílený výpočet, logická premisa nebo kontextuální fakt platný pro všechny options.
Příklady: EV výpočet (loss aversion), ekvivalence rámce (framing), podmínka smysluplnosti úlohy (confirmation bias).

**Smí být `null`** pro příklady bez sdíleného numerického kontextu (kvalitativní sunk cost scénáře).

**Důsledek pro `explanation` u options:** po přesunu sdíleného výpočtu do `global_explanation`
jsou option-specific `explanation` kratší a zaměřené čistě na mechanismus zkreslení nebo volby.

```json
{
  "question": "...",
  "global_explanation": "EV varianty B = 0,6·80 000 + 0,4·35 000 = 62 000 € > 50 000 €.",
  "options": [
    { "verdict": "rational", "explanation": "Volba se opírá o vyšší EV." },
    { "verdict": "biased",   "explanation": "Strach z propadu převáží EV. Zkreslení: averze ke ztrátě." },
    { "verdict": "neutral",  "explanation": "Odkládá rozhodnutí přes dostupná čísla." }
  ]
}
```

**Kdy zavést:** před krokem 2 roadmapy (překlad do češtiny / angličtiny),
aby v2 prompt generoval příklady přímo ve finálním schématu.

**Příklady již s `global_explanation`:** `anchoring-own-02` (viz `good/anchoring/`).
Ostatní soubory budou doplněny v kroku 1.5 roadmapy — nemusí být všechny JSON struktury
shodné ve stejnou dobu.

**Vhodné použití `global_explanation` u anchoring příkladů:** pokud existuje vědomé
racionální využití kotvy (např. vyjednávací strategie „říct více, abych měl/a prostor
k ústupku"), `global_explanation` je správné místo, kde toto vědomé použití popsat
a odlišit ho od nevědomého podlehnutí. Tím se zabrání dojmu, že příklad zavrhuje
každé odchýlení od tržní ceny.

## 12. U anchoring příkladů: kotva musí pocházet ze zjevně irelevantního zdroje

Kotva funguje jako demonstrace zkreslení pouze tehdy, když ji uživatel nemůže racionálně
zdůvodnit jako relevantní informaci. Pokud je zdroj kotvy strategický nebo jinak legitimně
informativní, příklad neurčuje zkreslení — ukazuje racionální reakci na (potenciálně) užitečná data.

**Zakázané zdroje kotvy:**

| Zdroj | Problém |
|---|---|
| Personalista zmíní číslo předchozího kandidáta | Strategická ambiguita: co tím sleduje? Informace o rozpočtu? Tlak dolů? |
| Protistrana v obchodním jednání uvede číslo | Kotva = záměrná vyjednávací taktika → racionální protistrategii lze obhájit |
| Odborný poradce zmíní referenční hodnotu | Může jít o legitimní benchmark |

**Doporučené zdroje kotvy:**

| Zdroj | Proč funguje |
|---|---|
| Inzerát na jiný senioritní level / jiný obor | Zjevně jiná kategorie — irelevance je jasná |
| Náhodné číslo z kontextu (kolo štěstí, PSČ, rodné číslo) | Explicitní nesmyslnost kotvy |
| Číslo z jiného rozhodnutí ve stejném sezení | Efekt přenosu kotvy přes kontexty |
| Číslo z média o jiném trhu / jiné geografii | Irelevance je fakticky doložitelná |

**Lokalizační pozor:** příklady kotvy vázané na geografii (Praha/Brno, NY/Cleveland)
jsou obtížně přeložitelné a fakticky nepřesné při neznalosti lokálního trhu.
Preferovat zdroje bez geografické specifičnosti.

```
❌ „Personalista řekl, že předchozí kandidát požadoval 95 000 Kč."
   → Strategická informace, ne náhodná kotva

✅ „Na portálu jste viděl/a inzerát pro seniory (8+ let praxe) s rozmezím 90–100 000 Kč."
   → Zjevně jiná kategorie — ukotvení je čistě iracionální
```

---

## 13. U sunk cost příkladů: uzavři všechny zdroje budoucí hodnoty z cesty „pokračovat"

Sunk cost příklady selžou, pokud cesta „pokračovat" nabízí jakoukoli implicitní budoucí hodnotu,
kterou otázka neadresuje. Uživatel pak může racionálně zdůvodnit pokračování — a příklad
nedemonstruje zkreslení, ale legitimní strategické uvažování.

**Typické skryté zdroje hodnoty, které je třeba explicitně uzavřít:**

| Skrytá hodnota | Příklad | Jak uzavřít v otázce |
|---|---|---|
| Credentiální hodnota titulu | Doktorát | „Náboráři potvrdili, že titul hodnocení neovlivní." |
| Opce návratu k původní kariéře | Akademická dráha | „K akademické kariéře se vracet nechcete." |
| Přenositelné dovednosti | Kurz zastaralé technologie | „Nabyté znalosti nejsou v jiných oblastech využitelné." |
| Síťové kontakty | Projekt s vlivnými partnery | „Kontakty z projektu již máte a přechod je neohrozí." |

**Testovací otázka při psaní sunk cost příkladu:** *Existuje budoucí stav světa, ve kterém
by pokračování bylo racionální — ne kvůli minulým nákladům, ale kvůli dosud nezmíněné
budoucí hodnotě?* Pokud ano, doplnit do otázky větu, která tuto hodnotu explicitně uzavře.

---

## 13. Otázka musí explicitně omezit subjektivní preference uživatele

Pokud existuje legitimní důvod zvolit kteroukoli z nabízených odpovědí (jiný cíl, jiná
preference, jiný kontext), nejde o demonstraci zkreslení — jde o racionálně odůvodněnou
volbu. Příklad musí takové alternativní interpretace předem uzavřít.

**Pravidlo:** Jsou-li v otázce možné subjektivní preference, které by měnily správnost
volby, musí být explicitně omezeny přímo v zadání. Neomezuj je až v odpovědích — tam
uživatel musí správně číst celý text, zatímco otázka ho ukotvuje od začátku.

```
❌ "Které balení vložíte do košíku?"
   → uživatel, který chce tučnější maso, legitimně vybere '5 % tuku' a není to zkreslení

✅ "Jde vám o zdravé dietnější jídlo. Které balení vložíte do košíku?"
   → cíl je zakotven; obě volby na základě etikety jsou pak projevem rámování
```

**Obecná technika:** Před psaním odpovědí si polož otázku: *Existuje uživatel,
pro kterého by „biased" odpověď byla racionální, kdyby měl jiné preference nebo cíle?*
Pokud ano, doplň do otázky předpoklad, který tyto preference uzavře.

---

## 13. Odpovědi nesmějí obsahovat nápovědu k zkreslení

Uživatel vidí otázku **a zároveň všechny nabízené odpovědi** dříve, než se rozhodne.
Jakákoli formulace odpovědi, která naznačuje povahu zkreslení, může uživatele navést zpět
k zadání a umožnit mu odhalit past intelektem místo prožitku.

**Pravidlo:** Text odpovědi popisuje rozhodnutí nebo postoj, ne jeho zdůvodnění.
Zdůvodnění — včetně odhalení ekvivalence, výpočtu EV nebo pojmenování zkreslení — patří
výhradně do pole `explanation`, které se zobrazí až po výběru.

```
❌ "Oba programy popisují identický výsledek — vyberu podle jiných kritérií."
   → slovo "identický" okamžitě prozradí pointu

✅ "Abych se mohl/a rozhodnout, potřebuji znát podrobnosti obou programů — tato tisková sdělení vlády nestačí."
   → přirozený postoj bez zmínky o ekvivalenci
```

**Testovací otázka při psaní odpovědí:** *Může uživatel pouhým přečtením textu odpovědi
odvodit, o jaké zkreslení jde, aniž by klikl na „Potvrdit"?* Pokud ano, přeformulovat.

---

## 13. Kulturně specifické idiomy — poznámky pro překladatele

Některé výrazy v příkladech jsou idiomatické a nemají doslovný ekvivalent v cílovém jazyce.
AI překladač je obvykle zvládne správně v kontextu, ale při lokalizaci do méně obvyklých
jazyků nebo při překladu izolovaných částí textu hrozí chyba.

**Pravidlo:** Příklady obsahující kulturně specifické idiomy označit v lokalizačním souboru
`selected_with_context.cs` poznámkou `translator_note`. Nevkládej poznámku přímo do
produkčního JSON — patří do lokalizačního kontextu, ne do schématu příkladu.

**Přehled zjištěných idiomů:**

| Výraz v příkladu | Problematický překlad | Správný ekvivalent (EN) | Poznámka |
|---|---|---|---|
| `panna` / `orel` (hod mincí) | maiden / eagle | heads / tails | CZ idiom; DE: Kopf/Zahl; FR: face/pile |

**Vzor poznámky pro `selected_with_context.cs`:**

```json
"translator_note": "CZ 'panna/orel' = EN 'heads/tails'; DE 'Kopf/Zahl'; FR 'face/pile'. Do NOT translate literally."
```

**Kdy přidat poznámku:** kdykoliv příklad obsahuje:
- idiomy hod mincí / losování / karetní hry
- místní instituce nebo právní pojmy (pojišťovna, exekuce, sociální dávky)
- měnové a cenové konvence specifické pro zemi

---

## 14. Interaktivní příklady — kdy je textová verze nedostatečná

| Bias | Problém textové verze | Řešení |
|---|---|---|
| Anchoring | Kotva je přečtena jako informace, ne prožita | `WheelOfFortune` komponenta |
| Confirmation bias (discovery) | Prostý výběr jednoho testu nedemonstruje tendenci | `RuleDiscovery` multi-step hra |
| Framing | Obě verze jsou zobrazeny najednou → ekvivalence je viditelná | `FramingReveal` — verze A se zobrazí nejdřív |
| Loss aversion | Výpočet EV zracionalizuje rozhodnutí před prožitkem ztráty | `TokenBet` micro-hra |
