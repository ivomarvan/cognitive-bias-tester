import json
import glob

files = glob.glob("experiments/2026-05-prompt-evaluation/data/v1-plain/curated/**/*.json", recursive=True)

count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        eval_gemini = data.get("evaluation", {}).get("gemini3.1pro", {})
        weaknesses = eval_gemini.get("weaknesses", [])
        suggested_fix = eval_gemini.get("suggested_fix")
        
        # We need to find files that have NO weaknesses but DO have a suggested_fix
        if not weaknesses and suggested_fix and str(suggested_fix).strip().lower() not in ["none", "null", ""]:
            count += 1
            print(f"=== FOUND FILE: {f} ===")
            print(f"QUESTION: {data['example']['question']}")
            print(f"SUGGESTED_FIX: {suggested_fix}")
            print(f"HAS SUGGESTION BLOCK? {'Yes' if 'suggestion' in eval_gemini else 'No'}")
            print("--------------------------------------------------")

print(f"Found {count} files with suggested_fix but no weaknesses.")
