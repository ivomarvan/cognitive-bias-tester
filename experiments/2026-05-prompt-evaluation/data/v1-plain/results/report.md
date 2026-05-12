# Cognitive Bias Example Evaluation

**Rows = M1 (generator)** · **Columns = M2 (evaluator)**

Cell: **weighted score** / ✅ use_as_is / ❌ reject / ⚑ flagged / json2 link

Score legend: ≥80 · 65–80 · 50–65 · <50 · missing (v HTML verzi odpovídá podbarvení `#c8e6c9`, `#fff9c4`, `#ffe0b2`, `#ffcdd2`, `#e0e0e0`)

<table>
<thead>
<tr>
  <th>M1 \ M2</th>
  <th>gemini3.1pro</th>
  <th>sonnet4.6</th>
</tr>
</thead>
<tbody>
<tr>
  <td><b>Gemini 3.1 Pro</b><br><small>2026-05-10</small><br><a href="gen/gemini-3.1pro.json">json1</a></td>
  <td><b>83.0</b><br><span title="use_as_is / total">✅ 20/40</span> <span title="reject">❌ 2</span> <span title="flagged">⚑ 3</span><br><small>Generující model Gemini 3.1 Pro zvládl velmi dobře vytvořit logické a věcně správné scénáře, obzvláště u confirmation bi…</small><br><a href="eval/gemini-3.1pro__by__gemini3.1pro.json">json</a></td>
  <td><b>75.0</b><br><span title="use_as_is / total">✅ 4/40</span> <span title="reject">❌ 2</span> <span title="flagged">⚑ 3</span><br><small>Gemini 3.1 Pro generuje strukturálně korektní příklady s dobrými sunk_cost a confirmation_bias sekcemi. Systémová slabin…</small><br><a href="eval/gemini-3.1pro__by__sonnet4.6.json">json</a></td>
</tr>
<tr>
  <td><b>GPT-4</b><br><small>2023-10-01</small><br><a href="gen/gpt-4o.json">json1</a></td>
  <td><b>41.5</b><br><span title="use_as_is / total">✅ 0/16</span> <span title="reject">❌ 15</span> <span title="flagged">⚑ 16</span><br><small>Modely selhaly v generování objektivně racionálních odpovědí, obzvláště u anchoringu zaváděly nevyslovené předpoklady (r…</small><br><a href="eval/gpt-4o__by__gemini3.1pro.json">json</a></td>
  <td><b>43.8</b><br><span title="use_as_is / total">✅ 0/16</span> <span title="reject">❌ 12</span> <span title="flagged">⚑ 14</span><br><small>POZOR: Soubor je NEÚPLNÝ — obsahuje pouze anchoring a framing sekce. Chybí loss_aversion, confirmation_bias a sunk_cost_…</small><br><a href="eval/gpt-4o__by__sonnet4.6.json">json</a></td>
</tr>
<tr>
  <td><b>GPT-4.0</b><br><small>2023-10-09</small><br><a href="gen/gpt-4o-mini.json">json1</a></td>
  <td><b>41.7</b><br><span title="use_as_is / total">✅ 0/40</span> <span title="reject">❌ 27</span> <span title="flagged">⚑ 28</span><br><small>Generující model GPT-4o-mini hrubě selhal ve většině kategorií. Největším problémem je naprostá absence 'objektivní raci…</small><br><a href="eval/gpt-4o-mini__by__gemini3.1pro.json">json</a></td>
  <td><b>39.1</b><br><span title="use_as_is / total">✅ 0/40</span> <span title="reject">❌ 37</span> <span title="flagged">⚑ 37</span><br><small>GPT-4o-mini (identifikován jako GPT-4.0) produkuje závažně defektní výstup s rozsáhlými systémovými chybami: (1) Celá an…</small><br><a href="eval/gpt-4o-mini__by__sonnet4.6.json">json</a></td>
</tr>
<tr>
  <td><b>GPT-5.5</b><br><small>2026-05-10</small><br><a href="gen/gpt-5.5.json">json1</a></td>
  <td><b>81.8</b><br><span title="use_as_is / total">✅ 7/40</span> <span title="reject">❌ 0</span> <span title="flagged">⚑ 1</span><br><small>Generující model prokázal vysokou úroveň pochopení kognitivních zkreslení. Většina příkladů je velmi kvalitní, s jasně d…</small><br><a href="eval/gpt-5.5__by__gemini3.1pro.json">json</a></td>
  <td><b>80.3</b><br><span title="use_as_is / total">✅ 3/40</span> <span title="reject">❌ 0</span> <span title="flagged">⚑ 0</span><br><small>GPT-5.5 generuje konzistentně kvalitní sadu příkladů — nejlepší ze srovnávaných modelů. Anchoring sekce je vzorová s exp…</small><br><a href="eval/gpt-5.5__by__sonnet4.6.json">json</a></td>
</tr>
<tr>
  <td><b>Claude Opus 4.7</b><br><small>2026-05-10</small><br><a href="gen/opus-4.7.json">json1</a></td>
  <td><b>85.5</b><br><span title="use_as_is / total">✅ 22/40</span> <span title="reject">❌ 0</span> <span title="flagged">⚑ 0</span><br><small>Celkově model Claude Opus 4.7 odvedl výbornou práci. Podařilo se mu generovat silné a funkční pasti, které odpovídají za…</small><br><a href="eval/opus-4.7__by__gemini3.1pro.json">json</a></td>
  <td><b>85.7</b><br><span title="use_as_is / total">✅ 24/40</span> <span title="reject">❌ 0</span> <span title="flagged">⚑ 0</span><br><small>Claude Opus 4.7 produkuje nejkvalitnější sadu ze všech hodnocených modelů. Výjimečné rysy: (1) framing sekce jako jediná…</small><br><a href="eval/opus-4.7__by__sonnet4.6.json">json</a></td>
</tr>
<tr>
  <td><b>Claude Sonnet 4.6</b><br><small>2026-05-10</small><br><a href="gen/sonet-4.6.json">json1</a></td>
  <td><b>83.4</b><br><span title="use_as_is / total">✅ 10/40</span> <span title="reject">❌ 0</span> <span title="flagged">⚑ 0</span><br><small>Generující model (Claude Sonnet 4.6) odvedl vynikající práci. Příklady jsou vysoce kvalitní, srozumitelné a racionální v…</small><br><a href="eval/sonet-4.6__by__gemini3.1pro.json">json</a></td>
  <td><b>77.9</b><br><span title="use_as_is / total">✅ 0/40</span> <span title="reject">❌ 0</span> <span title="flagged">⚑ 0</span><br><small>Claude Sonnet 4.6 produkuje konzistentní, dobře strukturované příklady. Silné stránky: anchoring a sunk_cost sekce mají …</small><br><a href="eval/sonet-4.6__by__sonnet4.6.json">json</a></td>
</tr>
</tbody>
</table>

---

*Generated from: nogit_data/example-eval*

*Regenerate:* `python pipeline.py report`
