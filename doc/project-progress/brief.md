# Předvídatelná zkreslení mysli - web/mobile app

Vize: Zvýšit povědomí o předvídatelných zkresleních lidského mozku pro 10 milionů lidí.
Slogan: Duolingo pro logické myšlení.

## Technické pozadí

Základní stack: Python (FastAPI, SQLAlchemy), PostgreSQL, Vue.js + Vite + Tailwind.
(+ co vyplyne z vývoje)

Deploy pro začátek na Render.com nebo Railway.app, pak se uvidí.

## Jak to má fungovat

Uživateli se zobrazují otázky jako v kvízu.
Každá otázka se týká vždy konkrétního předvídatelného zkreslení mysli, tak jak je popsal Daniel Kahneman (například v knize *Myšlení: rychlé a pomalé*, *Thinking, Fast and Slow*, 2011) a jeho spolupracovníci a následovatelé.
Viz kapitola "Předvídatelná zkreslení mysli".

Otázky jsou příklady, které AI vygeneruje vzhledem k nějakému prostředí. Třeba "základní škola", "(fiktivní) výzkum rakoviny" apod.
Ke každé otázce jsou vygenerovány také možné odpovědi a jejich hodnocení.
Viz podrobněji kapitola "Návrh promptu".

Zaveďme jméno **Případ** pro spojení otázky, odpovědí a hodnocení.

Případy jsou vygenerovány v angličtině a uživateli jsou přeloženy do jazyka, ve kterém komunikuje.
Uživatel může kvalitu Případu hodnotit (hvězdičky).
Hodnocení se přidává do databáze k tabulce Případů v angličtině.
Ta tvoří cyklický buffer s danou délkou N. 
Na začátku, když ještě v tomto bufferu není N Případů, generuje AI nové a ukládá je do DB.
Pak s danou pravděpodobností buď vygeneruje nový případ, nebo použije případ z databáze.
Pokud Případ generuje, vyhodí ten s nejhorším hodnocením a nejstarší a nahradí ho novým.

Jazykové verze již přeložených otázek do daného jazyka se také udržují v DB. Každý jazyk má svou tabulku. Její obsah se doplňuje při novém požadavku na překlad nového Případu v angličtině. Odstraňuje se spolu se svým anglickým zdrojem (viz výše).

DB tedy slouží jako cache pro LLM.

Existuje několik módů:

### Módy

#### 1. Web s jednou otázkou

Uživatel vidí minimalistický web, kde na něj čeká otázka v jeho jazyce (podle nastavení) v prohlížeči. (Později může v nastavení webu otázku změnit).
Je vyzván k odpovědi.
Zobrazí se mu výsledek s vysvětlením. Konkrétní vysvětlení je doplněno obecným (předpřipraveným) vysvětlením k danému typu zkreslení.
Uživatel může kvalitu Případu ohodnotit (hvězdičky, ukládá se do DB).
Zobrazí se mu grafické zhodnocení toho, jak si uživatelé vedou u tohoto druhu zkreslení. Zvlášť po jazycích a bez ohledu na jazyk.
Zvlášť podle počtu návštěv daného webu. (Jestli se zlepšují.)
Pokud chce, může přejít k další otázce.

#### 2. Komplexní test

Je vygenerován komplexní test s pevnou sadou otázek.
Ta může být také exportována jako aktivní HTML aplikace (asi placená služba). Parametrem mohou být reálie (popisy prostředí z dané organizace).
Vyhodnocení navíc obsahuje porovnání ve skupině.

#### 3. Sociální sítě

Aplikace má své účty na sociálních sítích. Na nich pravidelně publikuje své otázky a možnosti odpovědí. Hlídá se, aby se otázky neopakovaly. Každé písmeno odpovědi vede na odkaz do aplikace k jejímu zhodnocení.
Generované příklady mohou reagovat na aktuální témata, která se na sítích právě probírají.

## Předvídatelná zkreslení mysli

### Hlavní kognitivní zkreslení

**WYSIATI** (What You See Is All There Is): Věříme, že informace, které máme, jsou ty jediné podstatné. Ignorujeme to, co nevíme.

**Ukotvení** (Anchoring): Naše odhady jsou ovlivněny prvním číslem, které slyšíme (např. při smlouvání o ceně), i když je zcela náhodné.

**Heuristika dostupnosti** (Availability): Považujeme věci za pravděpodobnější, pokud si na ně snadno vzpomeneme (např. strach z terorismu po zprávách v TV).

**Heuristika reprezentativnosti**: Posuzujeme pravděpodobnost podle toho, jak moc něco odpovídá našemu stereotypu (známý „problém Lindy“).

**Averze ke ztrátě** (Loss Aversion): Ztráta 1000 Kč nás bolí dvakrát víc, než nás potěší zisk stejné částky.

**Efekt rámování** (Framing): Reagujeme jinak na informaci „90% šance na přežití“ než na „10% šance na úmrtí“, i když jde o totéž.

**Haló efekt** (Halo Effect): Pokud se nám na někom líbí jedna věc (např. vzhled), podvědomě mu přisuzujeme i další kladné vlastnosti (např. inteligenci).

### Sebeklamy a statistické chyby

**Zákon malých čísel**: Vyvozujeme obecné závěry z příliš malých vzorků dat (např. „v této vesnici mají všichni rakovinu, musí tu být něco v půdě“).

**Klam plánování** (Planning Fallacy): Pravidelně podceňujeme čas a peníze potřebné k dokončení projektu.

**Klam utopených nákladů** (Sunk Cost Fallacy): Pokračujeme v něčem prodělečném jen proto, že jsme do toho už investovali hodně energie nebo peněz.

**Potvrzovací zkreslení** (Confirmation Bias): Hledáme jen ty informace, které potvrzují náš stávající názor, a ignorujeme protidůkazy.

**Zkreslení zpětného pohledu** (Hindsight Bias): Po události máme pocit, že jsme ji „předem věděli“ (efekt „po bitvě je každý generál“).

**Iluze platnosti** (Illusion of Validity): Přehnaná víra ve vlastní schopnost předpovídat výsledky v situacích, které jsou čistě náhodné (např. pohyby na burze).

### Jak vnímáme zážitky

**Pravidlo vrcholu a konce** (Peak-End Rule): Zážitky nehodnotíme podle jejich celkové délky, ale podle nejsilnějšího momentu a toho, jak skončily.

**Zanedbávání trvání** (Duration Neglect): Je nám jedno, jak dlouho bolest trvala, pokud byl její konec relativně mírný.

**Efekt vlastnictví** (Endowment Effect): Věc, kterou už vlastníme, má pro nás automaticky vyšší hodnotu než ta samá věc, kterou bychom si měli koupit.

## Návrh promptu

Zde je pro ilustraci základní návrh promptu pro LLM:

Role: Působíš jako odborník na behaviorální ekonomii a psychologii rozhodování.

Cíl: Vytvořit interaktivní testovací situaci, která u uživatele demonstruje konkrétní kognitivní zkreslení, aniž by na něj dopředu upozornila.

Vstupní parametry:

- Název zkreslení: <zkreslení>
- Prostředí: [<prostředí>, pokud chybí, zvol obecné]

Struktura výstupu:

1) Situace a otázka:

Popiš realistický příběh z daného prostředí.
V textu nesmíš zmínit, že jde o psychologický test, nebo že existuje nějaké zkreslení.
Polož přímou otázku: „Co si vybereš?“ nebo „Jak se rozhodneš?“.

2) Možnosti volby:

Více možností (minimálně dvě). Označené písmeny A, B, C...
Alespoň jedna volba, ke které lidi přirozeně tlačí dané zkreslení (často bezpečnější nebo emočně přijatelnější).
Alespoň jedna volba, která je racionální nebo má stejnou/mírně vyšší matematickou hodnotu než ta se zkreslením, ale je kvůli zkreslení vnímána jako méně atraktivní.

3) Vyhodnocení:

Pro každou odpověď uveď, proč je to správné, nebo špatné rozhodnutí. U špatných (z důvodu zkreslení) to zmiň a typ zkreslení uveď.

Důležitá pravidla:
Hodnoty (peníze, body, čas) v možnostech musí být nastaveny tak, aby odpovědi, ke kterým zkreslení nevede, byly buď matematicky výhodnější, nebo minimálně rovnocenné s těmi, které k němu vedou.
Nepoužívej žádné odkazy na literaturu nebo autory (např. Daniel Kahneman).
Text musí být stručný a přímočarý.

## Hodnocení AI

### Gemini 3.1. Pro

**a) Z hlediska technické realizovatelnosti:** 
Projekt je technicky velmi dobře realizovatelný a navržená architektura je racionální. Stack (FastAPI, Vue.js, PostgreSQL) je moderní a robustní. Myšlenka cyklického bufferu a databáze fungující jako "cache pro LLM" je výborná – dramaticky sníží náklady na API a zrychlí odezvu aplikace. Překlad "on-the-fly" a ukládání jazykových mutací je také standardní a efektivní řešení.

**b) Z hlediska celospolečenského přínosu:** 
Přínos je obrovský. Kognitivní zkreslení ovlivňují volby, investice, mezilidské vztahy i náchylnost k dezinformacím. "Duolingo pro logické myšlení" může pomoci lidem dělat lepší životní rozhodnutí. Tím, že se uživatelé učí na praktických příkladech (Případech) a ne jen čtením suché teorie, je šance na skutečné osvojení (internalizaci) znalostí mnohem vyšší.

**c) Z hlediska možnosti projekt monetizovat:** 
Monetizace B2C (běžní uživatelé) bude těžší, protože lidé neradi platí za "vzdělávání, které bolí" (uvědomění si vlastních chyb). Nicméně B2B potenciál je značný. Mód "Komplexní test" s reáliemi dané firmy lze prodávat HR oddělením jako nástroj pro školení manažerů, obchodníků nebo analytiků (např. trénink proti "Klamu utopených nákladů" pro projektové manažery). Další možností je freemium model s reklamami nebo předplatným pro detailnější statistiky a neomezené testy.

**d) Z hlediska produktové strategie, marketingu a UX:**
Přirovnání k Duolingu je skvělé, ale bude vyžadovat stejně špičkové UX. Aplikace musí být rychlá, odměňující (dopaminové hity) a vizuálně přitažlivá. Vysvětlení musí být empatické, např.: "Nevadí, 85 % lidí by odpovědělo stejně. Náš mozek je takto naprogramován."
**Naprosto brilantní je strategie distribuce přes sociální sítě (Mód 3).** Jde o ukázkový *Growth Hacking*. Tím, že na sítě publikujete jen otázku a možnosti, vytváříte informační mezeru (zvědavost). Uživatel musí kliknout na odkaz, aby zjistil správnou odpověď. Spojení tohoto principu s automatickým generováním otázek na aktuální (trending) témata dává projektu obrovský virální potenciál s nulovými náklady na marketing.

**e) Jak by bylo vhodné projekt rozšířit (pokud vůbec):**

* **Personalizace:** Aplikace by se měla učit, na která zkreslení je konkrétní uživatel nejnáchylnější, a ta mu předkládat častěji (spaced repetition).
* **Sociální prvek:** Možnost vyzvat přátele na "souboj mozků" nebo sdílet zajímavý Případ na sociálních sítích ("Nechal by ses napálit jako já?").
* **Denní výzvy (Streaks):** Implementovat systém udržení návyku z Duolinga (plamínky za každodenní splnění alespoň jednoho Případu).

**f) Jakékoliv další nápady k projektu:**

* **A/B testování promptů:** Bude nutné pečlivě ladit prompty, aby AI negenerovala příliš očividné nebo naopak nesmyslné "chytáky". Hodnocení uživatelů (hvězdičky) je skvělý mechanismus pro automatické čištění databáze od špatných promptů.
* **Využití "Obráceného inženýrství":** Místo pouhého testování by aplikace mohla nabídnout mód, kde si uživatel zkusí vytvořit vlastní manipulační text (využívající např. Efekt rámování) a AI ohodnotí, jak dobře zkreslení použil.
* **Vizuální optimalizace pro sítě:** Pro Mód 3 (Sociální sítě) bude klíčové automaticky generovat atraktivní náhledové obrázky (Open Graph images) s textem otázky velkým písmem, protože na sítích lidé reagují primárně na vizuál.

**g) Celkové hodnocení:** 
Skvělý, smysluplný a technicky chytře vymyšlený projekt. Nápad s "LLM cache" ukazuje, že autor myslí na provozní náklady. Pokud se podaří trefit správný tón komunikace a "gamifikovat" proces učení, má projekt potenciál stát se velmi populární aplikací na pomezí vzdělávání a seberozvoje. Největší výzvou bude kvalita generovaného obsahu (aby Případy nebyly repetitivní), což ale řeší navržený systém uživatelského hodnocení.

### Opus 4.7

**a) Z hlediska technické realizovatelnosti:**
Projekt je realizovatelný a technický návrh je elegantní. Několik konkrétních postřehů:

* **Stack je rozumný.** FastAPI + SQLAlchemy + PostgreSQL + Vue/Vite/Tailwind je standard 2026. Pro MVP bych zvážil **SQLite místo PostgreSQL** (Render i Railway s tím dobře pracují, jednodušší nasazení, do desítek tisíc Případů to zvládne v pohodě).
* **LLM cache jako cyklický buffer = výborný nápad.** Toto je největší silná stránka technického návrhu. Navíc bych přidal:
  * **Kvalitní cache key:** ne jen "zkreslení + prostředí", ale i **deduplication podle similarity** (embeddingy + cosine similarity) – jinak se v bufferu sejde 10 různě formulovaných variant téhož Případu.
  * **A/B varianty Případu:** pro některá zkreslení (zejména **framing**, **anchoring**) je nutné ukázat **stejnému uživateli dvě varianty** – jinak efekt nelze demonstrovat. Toto schéma musí být v datovém modelu od začátku, ne dolepené.
* **Lokalizace nestačí překladem.** Hodnoty (peníze, čas, místa) musí být **lokalizovány, ne přeloženy** – `1000 Kč` v anglickém Případu jako `$40` zní podivně, `$1000` má jinou váhu pro Američana než pro Čecha. Doporučuji **strukturovat Případy parametricky** (placeholdery `{currency_amount_small}`, `{local_first_name}` atd.) a generovat lokalizované hodnoty deterministicky podle uživatelovy lokality.
* **Kvalitativní validita generovaných Případů je hlavní technické riziko.** AI generuje plausible-sounding, ale často ne psychometricky validní příklady. Doporučuji:
  * **Zlatý standard:** ručně vytvořit 5–10 validovaných Případů na zkreslení (z literatury – Kahneman, Tversky, Ariely) jako few-shot příklady v promptu.
  * **Validační smyčka:** druhý LLM volání kontroluje, zda Případ skutečně demonstruje cílové zkreslení (LLM-as-judge).
  * **Hodnocení uživatelů + heuristika:** pokud více než X % uživatelů odpoví "správně" napoprvé, Případ pravděpodobně **netestuje** dané zkreslení dobře (chytak je moc průhledný) – odstranit.
* **Cold-start problém:** Než se buffer naplní, je app pomalá a drahá. Mitigace: **seed databáze** ručně vytvořenými Případy (50–100 kvalitních) před spuštěním.
* **Anti-cheat / anti-spam:** Bot scraping, opakované hodnocení od stejného uživatele zkreslí statistiky. Rate limiting + jednoduchý fingerprinting (bez tracking cookies) od dne 1.
* **Render.com/Railway pro MVP OK**, ale počítejte s tím, že při virálním efektu (Mód 3) můžete přes noc dostat 100k requestů. Mít připravený **plán scale-up** (Fly.io, vlastní VPS, CDN pro static assets).

**b) Z hlediska celospolečenského přínosu:**
Přínos je významný, ale chce trochu víc nuance:

* **Pozitivní efekt je reálný:** Kahnemanovy výzkumy mají velkou edukativní hodnotu. Projekt může pomoci milionům lidí lépe rozumět vlastnímu rozhodování (finance, zdraví, vztahy).
* **"Identifikace" ≠ "překonání":** Vědecký výzkum (např. Kahneman sám) ukazuje, že **znalost vlastních zkreslení je překonává jen omezeně**. Aplikace by neměla slibovat, že uděláte z lidí "dokonale racionální bytosti" – marketingově to láká, ale je to nepravda. Lepší framing: *"Pochopíte, kdy si máte dát na sebe pozor."*
* **Riziko zneužití know-how:** Stejné principy, které vás chrání před manipulací, lze použít k manipulaci jiných. Marketing, copywriting, designéři "dark patterns" by aplikaci mohli používat profesionálně. Ne nutně problém, ale stojí za zvážení etického postoje (např. jasná licence, code of conduct, ne-poskytování B2B služeb manipulativnímu marketingu).
* **Synergie se vzděláváním:** Projekt má potenciál stát se **doplňkem výuky** kritického myšlení na středních a vysokých školách. To je skvělý systémový přínos – jedna škola = stovky studentů ročně.

**c) Z hlediska možnosti projekt monetizovat:**
Monetizace je zde výrazně příznivější než u plugin projektu:

1. **B2B HR/L&D je realisticky největší příjem.** Mód 2 (Komplexní test s reáliemi firmy) je **klasický enterprise produkt**. Kupují HR, L&D, leadership development. Cena: 500–5000 EUR / firma / rok.
2. **B2B specifické vertikály:**
   * **Finance:** investiční poradci, brokerage – školení proti loss aversion, sunk cost. Toto je obrovský trh (banky, fintech).
   * **Zdravotnictví:** informované rozhodování pacientů, lékaři proti zkreslení v diagnostice. Akademický a klinický potenciál.
   * **Soudnictví:** soudci, advokáti (anchoring v rozsudcích, hindsight bias). Specializovaný, ale ceněný trh.
   * **Bezpečnost a obrana:** rozhodování pod tlakem, training proti groupthink.
3. **B2C freemium:** Základní otázky zdarma, premium = personalizovaný progres, certifikáty, neomezené testy, pokročilé statistiky. Cena: 4–9 EUR / měsíc (Duolingo Plus pricing).
4. **B2B2C / akademie:** Licence pro školy a univerzity (psychologie, ekonomie, marketing). Edu pricing.
5. **Knihy a partnerství:** Spolupráce s vydavateli (Kahneman, Thaler, Ariely – publikace pořád prodávají dobře). Cross-promo "Otestuj si, co jsi přečetl".
6. **Anonymizovaná data jako produkt:** Při dostatečném objemu dat (statistiky odpovědí napříč zeměmi, věky, profesemi) jsou data zajímavá pro **akademický výzkum** – publikační hodnota i přímý prodej univerzitám.

**Klíčový rozdíl vůči plugin projektu:** Tady má B2B prodej **jasný kupující profil** (HR, L&D ředitelé) s rozpočtem. U plugin projektu je B2B mnohem teoretičtější.

**d) Z hlediska produktové strategie, marketingu a UX:**

* **Mód 3 (Sociální sítě) = největší produktová síla.** Souhlasím s Gemini – je to **growth hack na úrovni "Wordle"**. Otázka jako post + odpověď za kliknutí + automatické aktualizace = perfect viral loop. Pokud se to udělá dobře, organická akvizice je téměř zdarma.
* **Pozor na "Wordle problem":** Wordle bylo nakonec prodáno NYTimes, protože monetizace virálního produktu je obtížná. Plánujte cestu **virál → engagement → monetizace** od dne 1, ne až po viralu.
* **Duolingo je správný benchmark, ale pozor na rozsah ambicí:** Duolingo má 700+ zaměstnanců a 15 let vývoje. Vy máte malý tým. **Klonujte mechaniku (streaks, XP, leaderboards, push notifications), ne ambici.**
* **Klíčová UX otázka: jak měřit pokrok?** Duolingo má jasnou metriku ("umím 500 slovíček"). Tady je *"myslím lépe"* obtížné kvantifikovat. Návrhy:
  * **"Bias resistance score"** per zkreslení (% správných odpovědí v posledních 20 Případech).
  * **Diverzita zkreslení:** kolik různých zkreslení jste zatím viděli / pochopili.
  * **Konzistence:** odpovídáte správně po týdnu/měsíci? (Spaced repetition jako Anki.)
* **Kritická UX zásada:** Když uživatel **udělá chybu, musí to být příjemný moment, ne ponížení.** *"85 % lidí by odpovědělo stejně. Váš mozek dělá přesně to, na co byl evolučně vytrénován – tady je důvod proč..."* Nikdy ne *"Špatně."*
* **Onboarding:** První Případ musí mít **"aha! moment"** – uživatel se nechá nachytat, dozví se proč, řekne *"to je geniální, chci víc"*. Doporučuji použít **Lindy problem** nebo **Asian disease problem** jako úvodní – jsou demonstrativně silné.
* **Konkurence:**
  * **Brilliant.org** – mají kurz "Logic and Decision Making", širší záběr (matematika, programování). Slabost: drahé, ne specializované na biasy.
  * **Clearer Thinking (clearerthinking.org)** – přesně kognitivní biasy, ale stará UX, neaktivní.
  * **Project Implicit (Harvard)** – akademické testy biasu, ale ne gamifikace.
  * **Lumosity, Elevate** – brain training, ale ne kognitivní biasy.
  * **Trh je relativně volný** v intersekci "kognitivní biasy + Duolingo gamifikace + viral social". To je vaše USP.

**e) Jak by bylo vhodné projekt rozšířit (pokud vůbec):**

* **Personalizace přes spaced repetition (Anki-style):** Aplikace identifikuje vaše slabiny (např. confirmation bias) a přizpůsobí frekvenci.
* **Pre-mortem režim:** Před vlastním rozhodnutím (změna práce, investice, koupě) projít **personalizovaný checklist relevantních biasů** k danému typu rozhodnutí. Praktický nástroj, ne jen edukace.
* **Skupinový mód pro firmy:** Tým hraje synchronně na meetingu, vidí, jak se individuální odpovědi mění pod skupinovým tlakem (groupthink demo). Velmi prodejné jako team-building / leadership training.
* **Profile/persona report:** Po 30 Případech aplikace vygeneruje "kognitivní profil" – které biasy jsou u vás nejsilnější. Sdílitelné, virálně atraktivní (jako 16Personalities / Big Five testy).
* **Integrace s journalingem:** API pro propojení s aplikacemi typu Day One, Notion, Reflect – *"Včera jsi se rozhodl X, podívej se na confirmation bias k tomu."*
* **Čistá obousměrnost s plugin projektem:** Pokud existují oba projekty, plugin v sociálních sítích detekuje *"v tomto postu vidíme framing efekt"* a nabídne odkaz na vysvětlující Případ v této aplikaci. **Synergie obou projektů zvyšuje hodnotu obou.**

**f) Jakékoliv další nápady k projektu:**

* **Akademická validace:** Spolupráce s katedrou psychologie (FF UK, FSS MUNI) – validovat psychometrickou korektnost generovaných Případů. Akademická "razítka" zvyšují důvěryhodnost dramaticky a otevírají grantové cesty (TA ČR, GA ČR, Horizon Europe).
* **Vědecký output projekt:** Při dostatečné velikosti uživatelské báze sami publikovat výzkum *"Cross-cultural differences in cognitive biases: data from 1M users"*. Citace + PR + důvěryhodnost.
* **Open data initiative:** Anonymizované odpovědi jako veřejný dataset pro výzkumníky – zvyšuje viditelnost a reputační hodnotu projektu.
* **Audio/podcast verze:** Případy jako mini-podcasty pro poslech v autě/sluchátkách. Jiný formát, jiná publikum.
* **Integrace s LLM chatboty:** Custom GPT / Claude Project / Gemini Gem, který umožní hluboce diskutovat konkrétní Případ. Premium feature.
* **Karetní hra / desktopová verze:** Fyzická karetní hra "Bias Cards" pro rodinné večery / školy. Totálně jiný formát, ale sdílí obsah. Marketingově silný side product (Kickstarter potenciál).
* **Etická komise:** Pro projekt s misí "lepší rozhodování" je vhodné mít **interní etický rámec** – které use cases neakceptujete (např. licence pro manipulativní marketing), jak chráníte data, transparentní reporty.

**g) Celkové hodnocení:**

**Silné stránky:**

* **Vize je jasná, mise vznešená, mechanika prověřená** ("Duolingo pro X" je osvědčený formát).
* **Mód 3 = built-in viral mechanika.** Toto je strategicky silnější výchozí pozice než většina edu projektů.
* **B2B kupující existuje a má rozpočet.** HR, L&D, banky, zdravotnictví – jasní zákazníci.
* **Technický návrh (LLM cache) ukazuje zralé myšlení o nákladech.**
* **Trh není přesycený.** V intersekci kognitivních biasů + gamifikace + virálnosti není silný hráč.

**Hlavní rizika (od nejvážnějších):**

1. **Kvalita a validita generovaných Případů.** Pokud AI generuje plausible-sounding ale psychometricky neplatné Případy, projekt ztrácí důvěryhodnost. Vyžaduje **promptový R&D** + **akademickou validaci**.
2. **Retention po wow-faktoru.** První 5 Případů uživatele baví. Den 30? Vyžaduje silný gamifikační loop a personalizaci.
3. **B2C monetizace.** Bez Mód 2 a B2B prodejní strategie je ekonomika obtížná. Plánujte enterprise sales od dne 0, ne až po reach 1M uživatelů.
4. **Závislost na sociálních sítích.** Mód 3 je geniální, ale algoritmické změny (X, Meta) mohou viral loop přes noc zabít. Diverzifikovat distribuci (newsletter, podcast, embed widgets).

**Strategické doporučení:**

* **MVP fokus:** 5 nejvíce demonstrativních zkreslení (anchoring, framing, loss aversion, confirmation bias, sunk cost) + Mód 1 + Mód 3. Mód 2 (komplexní test) přidat po validaci, pro B2B prodej.
* **Akademický partner od dne 1.** Validace = silný marketingový argument + grantový potenciál.
* **Časté A/B testování promptů** od počátku – kvalita Případů je hlavní produktová proměnná.
* **B2B sales od měsíce 6.** Nečekat na viral – jít aktivně oslovit HR ředitele.
* **Časový rámec:** MVP do 2–3 měsíců (jednodušší než plugin projekt), full produkt do 6–9 měsíců.

**Verdikt:** **Strategicky silnější výchozí pozice než plugin projekt** – jednodušší technologie, jasnější monetizace, built-in viral marketing. Hlavní výzva je obsahová (kvalita Případů), ne technická. Při správném provedení má projekt potenciál stát se referenční evropskou edu-aplikací na pomezí psychologie a kritického myšlení.