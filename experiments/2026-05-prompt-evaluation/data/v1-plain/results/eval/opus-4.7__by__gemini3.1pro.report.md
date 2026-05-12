# Report: Hodnocení příkladů kognitivních zkreslení

**Evaluátor:** Gemini 3.1 Pro
**Zdrojový soubor:** `/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/gen/opus-4.7.json`
**Generující model:** Claude Opus 4.7
**Datum hodnocení:** 2026-05-10 23:47:54

## Celkové shrnutí

Vyhodnoceno bylo celkem **40** příkladů. Sada obsahuje 15 učebnicových a 25 vlastních scénářů, které rovnoměrně pokrývají 5 kognitivních zkreslení (*anchoring*, *framing*, *loss aversion*, *confirmation bias*, *sunk cost fallacy*).

Model Claude Opus 4.7 odvedl nadprůměrnou práci a generuje velmi funkční pasti, aniž by prozrazoval účel úloh. Většina příkladů byla hodnocena jako `use_as_is`.

- **Průměrné skóre (celé sady):** 85.5/100
- **Učebnicové příklady (průměr):** 87.8/100
- **Vlastní příklady (průměr):** 84.1/100

## Slabiny a doporučení k úpravám
- U zkreslení *framing* se objevila tendence vytvořit "vlastní" pasti pomocí krkolomných procentních popisů (např. "o 1 procentní bod nižší než 6 %" místo "5 %"). To sice technicky funguje, ale v běžném dialogu působí neuvěřitelně a prozrazuje testovací povahu otázky. Tyto položky doporučujeme přeformulovat přirozeněji.
- U *loss aversion* jsou scénáře excelentně racionálně zakotveny (pomocí očekávané hodnoty zisku).
- Populační metriky jsou zcela v pořádku – vlastní příklady přesně pokrývají obtížnosti 1 až 5.

## Top 3 nejlepší příklady
confirmation_bias-textbook-02, confirmation_bias-textbook-01, loss_aversion-textbook-03

Sada je jako celek připravena k použití s pouze minimálními textovými úpravami u několika specifických položek.
