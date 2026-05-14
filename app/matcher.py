import json
from rapidfuzz import fuzz

def load_medications(path: str = "data/medications.json") -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_best_match(texts: list[str], medications: list) -> dict | None:
    if not texts:
        return None

    query = " ".join(texts).lower()
    candidates = {}

    for med in medications:
        name_fr = med["name_fr"].lower()
        name_ar = med["name_ar"]
        active = med["active_ingredient"].lower()
        classe = med.get("classe", "").lower()
        indication = med.get("indication", "").lower()
        lab = med.get("lab", "").lower()

        score_fr = fuzz.partial_ratio(query, name_fr)
        score_ar = fuzz.partial_ratio(query, name_ar)
        score_active = fuzz.partial_ratio(query, active)
        score_token = fuzz.token_sort_ratio(query, name_fr)
        score_classe = fuzz.partial_ratio(query, classe)
        score_indication = fuzz.partial_ratio(query, indication)

        bonus = 20 if name_fr in query else 0
        bonus += 15 if lab in query else 0

        best_score = max(
            score_fr * 1.0,
            score_ar * 1.0,
            score_active * 0.9,
            score_token * 0.95,
            score_classe * 0.7,
            score_indication * 0.6
        ) + bonus

        best_score = min(best_score, 100)
        candidates[med["id"]] = (best_score, med)

    if not candidates:
        return None

    best_id = max(candidates, key=lambda x: candidates[x][0])
    best_score, best_med = candidates[best_id]

    if best_score < 40:
        return None

    return {
        **best_med,
        "confidence_score": round(best_score / 100, 2)
    }