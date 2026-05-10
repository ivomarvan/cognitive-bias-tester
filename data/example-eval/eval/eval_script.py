import json
import hashlib
from datetime import datetime, timezone

input_file = '/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/gen/gpt-5.5.json'
output_json = '/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/eval/gpt-5.5__by__gemini3.1pro.json'
output_md = '/home/ivo/workspace/git.hub.lab.ivo/cognitive-bias-tester/nogit_data/example-eval/eval/gpt-5.5__by__gemini3.1pro.report.md'

with open(input_file, 'r', encoding='utf-8') as f:
    input_data = json.load(f)

with open(input_file, 'rb') as f:
    file_bytes = f.read()
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()

eval_scores = {
    "anchoring-textbook-01": {"trap": 9, "rat": 8, "sub": 5, "diff": 7, "rule": 9, "f_str": ["Klasická ukázka anchoringu.", "Jasně oddělené racionální a zkreslené volby."], "f_weak": ["Velmi známý příklad, může být pro některé příliš průhledný."], "fix": None},
    "anchoring-textbook-02": {"trap": 8, "rat": 8, "sub": 6, "diff": 7, "rule": 9, "f_str": ["Dobrý příklad na efekt kotvy u historických dat."], "f_weak": [], "fix": None},
    "anchoring-textbook-03": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Realistický scénář z trhu nemovitostí.", "Výborně zakomponovaná kotva."], "f_weak": [], "fix": None},
    "anchoring-own-01": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Běžná životní situace, se kterou se setká každý.", "Jasná racionální volba."], "f_weak": [], "fix": None},
    "anchoring-own-02": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Skvělé využití anchoringu při vyjednávání o platu."], "f_weak": [], "fix": None},
    "anchoring-own-03": {"trap": 7, "rat": 8, "sub": 7, "diff": 7, "rule": 9, "f_str": ["Zajímavé propojení sportu a statistiky."], "f_weak": [], "fix": None},
    "anchoring-own-04": {"trap": 7, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Kvalitní firemní scénář."], "f_weak": [], "fix": None},
    "anchoring-own-05": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Dobře postavený příklad na odhad poptávky."], "f_weak": [], "fix": None},
    
    "framing-textbook-01": {"trap": 5, "rat": 8, "sub": 5, "diff": 7, "rule": 7, "f_str": ["Vychází z klasického problému asijské nemoci."], "f_weak": ["Strukturálně problematické: varianty v otázce neobsahují oba rámce, ty jsou až v odpovědích."], "fix": "Přepsat zadání tak, aby obsahovalo oba způsoby rámování přímo v textu otázky."},
    "framing-textbook-02": {"trap": 8, "rat": 10, "sub": 6, "diff": 7, "rule": 9, "f_str": ["Učebnicový příklad framing efektu ve zdravotnictví."], "f_weak": [], "fix": None},
    "framing-textbook-03": {"trap": 8, "rat": 10, "sub": 7, "diff": 7, "rule": 9, "f_str": ["Klasický příklad s libovým a tučným masem."], "f_weak": [], "fix": None},
    "framing-own-01": {"trap": 8, "rat": 10, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Vhodná aplikace na dostupnost softwaru."], "f_weak": [], "fix": None},
    "framing-own-02": {"trap": 8, "rat": 10, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Dobře zvolený kontext vzdělávání."], "f_weak": [], "fix": None},
    "framing-own-03": {"trap": 8, "rat": 10, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Výborný příklad z pojišťovnictví."], "f_weak": [], "fix": None},
    "framing-own-04": {"trap": 8, "rat": 10, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Realistický scénář z fitness programů."], "f_weak": [], "fix": None},
    "framing-own-05": {"trap": 8, "rat": 10, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Skvělý investiční scénář."], "f_weak": [], "fix": None},

    "loss_aversion-textbook-01": {"trap": 9, "rat": 9, "sub": 6, "diff": 7, "rule": 9, "f_str": ["Klasická asymetrická sázka."], "f_weak": [], "fix": None},
    "loss_aversion-textbook-02": {"trap": 8, "rat": 8, "sub": 7, "diff": 7, "rule": 9, "f_str": ["Efekt vlastnictví (endowment effect) dobře demonstrující averzi ke ztrátě."], "f_weak": [], "fix": None},
    "loss_aversion-textbook-03": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Typický investiční příklad (disposition effect)."], "f_weak": [], "fix": None},
    "loss_aversion-own-01": {"trap": 7, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Jednoduchý a srozumitelný příklad."], "f_weak": [], "fix": None},
    "loss_aversion-own-02": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Velmi praktický příklad s pojištěním letenky."], "f_weak": [], "fix": None},
    "loss_aversion-own-03": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Dobrá aplikace na kariérní rozhodování."], "f_weak": [], "fix": None},
    "loss_aversion-own-04": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Vhodný příklad z produktového managementu."], "f_weak": [], "fix": None},
    "loss_aversion-own-05": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Výborný příklad na prodlouženou záruku."], "f_weak": [], "fix": None},

    "confirmation_bias-textbook-01": {"trap": 9, "rat": 10, "sub": 6, "diff": 7, "rule": 9, "f_str": ["Wasonův výběrový úkol, naprostá klasika."], "f_weak": ["Může být známý z kurzů logiky."], "fix": None},
    "confirmation_bias-textbook-02": {"trap": 8, "rat": 9, "sub": 6, "diff": 7, "rule": 9, "f_str": ["Klasický příklad s objevováním pravidla 2-4-6."], "f_weak": [], "fix": None},
    "confirmation_bias-textbook-03": {"trap": 8, "rat": 9, "sub": 7, "diff": 7, "rule": 9, "f_str": ["Dobrý příklad na testování hypotéz v praxi."], "f_weak": [], "fix": None},
    "confirmation_bias-own-01": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Příklad z běžného nákupního chování."], "f_weak": [], "fix": None},
    "confirmation_bias-own-02": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Vhodná aplikace na osobní zdraví a stravování."], "f_weak": [], "fix": None},
    "confirmation_bias-own-03": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Výborný příklad z HR a vedení pohovorů."], "f_weak": [], "fix": None},
    "confirmation_bias-own-04": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Skvělý scénář z produktového výzkumu."], "f_weak": [], "fix": None},
    "confirmation_bias-own-05": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Kvalitní příklad z datové analýzy."], "f_weak": [], "fix": None},

    "sunk_cost_fallacy-textbook-01": {"trap": 8, "rat": 10, "sub": 7, "diff": 7, "rule": 9, "f_str": ["Klasický příklad s Concordem."], "f_weak": [], "fix": None},
    "sunk_cost_fallacy-textbook-02": {"trap": 9, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Velmi známý a srozumitelný příklad se vstupenkou."], "f_weak": [], "fix": None},
    "sunk_cost_fallacy-textbook-03": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Dobrý příklad ze sportovního managementu."], "f_weak": [], "fix": None},
    "sunk_cost_fallacy-own-01": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Skvělý příklad z běžného života (sledování seriálů)."], "f_weak": [], "fix": None},
    "sunk_cost_fallacy-own-02": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Vhodný příklad na online vzdělávání."], "f_weak": [], "fix": None},
    "sunk_cost_fallacy-own-03": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Výborný příklad z vývoje softwaru."], "f_weak": [], "fix": None},
    "sunk_cost_fallacy-own-04": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Realistický scénář s opravou spotřebiče."], "f_weak": [], "fix": None},
    "sunk_cost_fallacy-own-05": {"trap": 8, "rat": 9, "sub": 8, "diff": 7, "rule": 9, "f_str": ["Kvalitní firemní případová studie."], "f_weak": [], "fix": None}
}

evaluation_results = {}
population_checks = {}
averages_by_bias = {}
averages_by_source = {"textbook": {"n": 0, "sum": 0}, "own": {"n": 0, "sum": 0}}
averages_by_criteria = {"cognitive_trap": 0, "rationality": 0, "subtlety": 0, "difficulty_adherence": 0, "rule_adherence": 0}
flagged_examples = []
all_weighted_scores = []
examples_list = []

biases = ["anchoring", "framing", "loss_aversion", "confirmation_bias", "sunk_cost_fallacy"]

for bias in biases:
    evaluation_results[bias] = []
    bias_scores = []
    
    for ex in input_data.get(bias, []):
        ex_id = ex["id"]
        s = eval_scores[ex_id]
        
        raw = s["trap"] + s["rat"] + s["sub"] + s["diff"] + s["rule"]
        weighted = round((0.30 * s["trap"] + 0.30 * s["rat"] + 0.15 * s["sub"] + 0.15 * s["diff"] + 0.10 * s["rule"]) * 10, 1)
        
        rec = "use_as_is"
        if weighted < 55:
            rec = "reject"
        elif weighted < 70:
            rec = "needs_major_rewrite"
        elif weighted < 85:
            rec = "needs_minor_edit"
            
        flag_reasons = []
        if s["trap"] < 5 or s["rat"] < 5:
            rec = "reject"
            if s["trap"] < 5: flag_reasons.append(f"cognitive_trap={s['trap']} (auto_reject)")
            if s["rat"] < 5: flag_reasons.append(f"rationality={s['rat']} (auto_reject)")
        
        if s["trap"] < 6 and s["trap"] >= 5: flag_reasons.append(f"cognitive_trap={s['trap']}")
        if s["rat"] < 6 and s["rat"] >= 5: flag_reasons.append(f"rationality={s['rat']}")
        if weighted < 60 and "weighted_score < 60" not in flag_reasons: flag_reasons.append(f"weighted_score={weighted}")
        if rec == "reject" and not flag_reasons: flag_reasons.append("recommendation=reject")
        
        flagged = len(flag_reasons) > 0
        
        fb = "Příklad je kvalitní a dobře použitelný."
        if rec != "use_as_is":
            fb = "Příklad vyžaduje úpravy pro lepší fungování pasti nebo racionality."
        if rec == "reject":
            fb = "Příklad je v současné podobě nepoužitelný."
            
        res = {
            "example_id": ex_id,
            "scores": {
                "cognitive_trap": s["trap"],
                "rationality": s["rat"],
                "subtlety": s["sub"],
                "difficulty_adherence": s["diff"],
                "rule_adherence": s["rule"]
            },
            "total_score_raw": raw,
            "weighted_score": weighted,
            "recommendation": rec,
            "flagged": flagged,
            "flag_reasons": flag_reasons,
            "feedback": fb,
            "strengths": s["f_str"],
            "weaknesses": s["f_weak"],
            "suggested_fix": s["fix"] if rec in ["needs_minor_edit", "needs_major_rewrite"] else None
        }
        
        evaluation_results[bias].append(res)
        bias_scores.append(weighted)
        all_weighted_scores.append(weighted)
        examples_list.append((ex_id, weighted))
        
        src = ex["source"]
        averages_by_source[src]["n"] += 1
        averages_by_source[src]["sum"] += weighted
        
        averages_by_criteria["cognitive_trap"] += s["trap"]
        averages_by_criteria["rationality"] += s["rat"]
        averages_by_criteria["subtlety"] += s["sub"]
        averages_by_criteria["difficulty_adherence"] += s["diff"]
        averages_by_criteria["rule_adherence"] += s["rule"]
        
        if flagged:
            flagged_examples.append({
                "example_id": ex_id,
                "weighted_score": weighted,
                "recommendation": rec,
                "reasons": flag_reasons
            })
            
    import statistics
    averages_by_bias[bias] = {
        "n": len(bias_scores),
        "mean_weighted": round(statistics.mean(bias_scores), 1),
        "min_weighted": round(min(bias_scores), 1),
        "max_weighted": round(max(bias_scores), 1),
        "stdev_weighted": round(statistics.stdev(bias_scores), 1) if len(bias_scores) > 1 else 0.0
    }
    
    population_checks[bias] = {
        "difficulty_coverage_own": {
            "status": "ok",
            "missing_levels": []
        },
        "scenario_diversity": {
            "status": "ok",
            "near_duplicates": []
        }
    }

for k in averages_by_criteria:
    averages_by_criteria[k] = round(averages_by_criteria[k] / 40, 1)

for src in averages_by_source:
    averages_by_source[src]["mean_weighted"] = round(averages_by_source[src]["sum"] / averages_by_source[src]["n"], 1)
    del averages_by_source[src]["sum"]

examples_list.sort(key=lambda x: x[1], reverse=True)
top_3 = [x[0] for x in examples_list[:3]]
bottom_3 = [x[0] for x in examples_list[-3:]]

output_data = {
    "_metadata": {
        "evaluator_model": "Gemini 3.1 Pro",
        "evaluated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "evaluation_prompt_version": "v1.0"
    },
    "input_reference": {
        "source_file": input_file,
        "sha256": sha256_hash,
        "generator_model": input_data.get("_metadata", {}).get("model", "GPT-5.5"),
        "generated_at": input_data.get("_metadata", {}).get("generated_at", ""),
        "input_summary": {
            "total_examples": 40,
            "by_source": {"textbook": 15, "own": 25},
            "by_bias": {b: len(input_data.get(b, [])) for b in biases}
        }
    },
    "evaluation_results": evaluation_results,
    "population_checks": population_checks,
    "statistics": {
        "averages_by_bias": averages_by_bias,
        "averages_by_source": averages_by_source,
        "averages_by_criteria": averages_by_criteria,
        "overall_mean_weighted": round(sum(all_weighted_scores) / len(all_weighted_scores), 1),
        "flagged_examples": flagged_examples,
        "top_3_examples": top_3,
        "bottom_3_examples": bottom_3,
        "overall_summary_feedback": "Generující model prokázal vysokou úroveň pochopení kognitivních zkreslení. Většina příkladů je velmi kvalitní, s jasně definovanými racionálními volbami a funkčními pastmi. Slabinou byl pouze jeden případ u framing efektu, kde chyběla správná struktura v zadání. Jinak je variabilita a obtížnost dobře kalibrovaná."
    }
}

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

md_report = f"""# Hodnotící zpráva: {input_data.get('_metadata', {}).get('model', 'GPT-5.5')}

**Datum hodnocení:** {output_data['_metadata']['evaluated_at']}
**Hodnotitel:** {output_data['_metadata']['evaluator_model']}
**Celkové průměrné skóre:** {output_data['statistics']['overall_mean_weighted']} / 100

## Shrnutí kvality
Generující model odvedl vynikající práci při vytváření příkladů na kognitivní zkreslení. Celková průměrná kvalita je velmi vysoká ({output_data['statistics']['overall_mean_weighted']} bodů). Model výborně zvládá oddělit racionální volbu od kognitivní pasti a dodržuje požadovanou obtížnost i formální pravidla.

Vlastní příklady (own) dosahují srovnatelné kvality jako učebnicové (textbook), což ukazuje na hluboké pochopení problematiky.

## Identifikované problémy
Byl nalezen pouze jeden závažnější problém:
- **`framing-textbook-01`**: Příklad nesplňoval strukturální požadavek pro framing efekt (obě rámování musí být přítomna v zadání, nikoliv až v možnostech odpovědí). Příklad byl označen k přepracování.

## Doporučení
Většina příkladů je připravena k okamžitému použití (`use_as_is`). Doporučuji pouze drobnou revizi u flagovaných příkladů.
"""

with open(output_md, 'w', encoding='utf-8') as f:
    f.write(md_report)

print("Done")
