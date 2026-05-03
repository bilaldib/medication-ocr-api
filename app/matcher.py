import json
from rapidfuzz import fuzz, process

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

        score_fr = fuzz.partial_ratio(query, name_fr)
        score_ar = fuzz.partial_ratio(query, name_ar)
        score_active = fuzz.partial_ratio(query, active)

        best_score = max(score_fr, score_ar, score_active)
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