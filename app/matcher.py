from data.database import AsyncSessionLocal
from data.models import Medication
from sqlalchemy import select, or_
import re
from typing import Optional, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from rapidfuzz import fuzz
vectorizer = None
tfidf_matrix = None
medications_cache = []
async def initialize_matcher():
    global vectorizer
    global tfidf_matrix
    global medications_cache

    medications_cache = await get_medications_from_db()

    corpus = [
    " ".join([
        m.get("search_name") or "",
        m.get("name_ar") or "",
        m.get("dci1") or "",
        str(m.get("dosage") or ""),
        m.get("unite_dosage") or ""
    ]).lower()
    for m in medications_cache
    ]

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2,4)
    )

    tfidf_matrix = vectorizer.fit_transform(corpus)

    print(f"Matcher initialisé avec {len(corpus)} médicaments")
def medication_to_dict(med) -> dict:
    """Convertit le modèle DB vers le format attendu par MedicationMatch"""
    return {
       
        "name_fr": med.nom or "",          
        "name_ar": med.nom_ar or "",
        "dci1": med.dci1 or "",
        "dosage": med.dosage or "",
        "unite_dosage": med.unite_dosage or "",
        "forme": med.forme or "",
        "presentation": med.presentation or "",                
        "ppv": float(med.ppv) if med.ppv is not None else None,
        "ph":float(med.ph) if med.ph is not None else None,
        "prix_br": float(med.prix_br) if med.prix_br is not None else None,
        "princeps_generique": med.princeps_generique,
        "taux_remboursement": med.taux_remboursement,
        "search_name": med.search_name ,
    }
async def get_medications_from_db() -> list:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Medication))
        return [medication_to_dict(row) for row in result.scalars().all()]
def get_confidence_level(score: float) -> str:
    if score >= 90:
        return "recognized"
    elif score >= 80:
        return "probable"
    elif score >= 70:
        return "warning"
    else:
        return "not_recognized"

def find_best_match(texts: List[str]) -> Optional[dict]:
    global vectorizer
    global tfidf_matrix
    global medications_cache

    if vectorizer is None or tfidf_matrix is None:
        return None
    if not medications_cache:
        return None
    
    if not texts:
      return None

    query = " ".join(texts).lower()
    query = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', query) # supprim les caractere inutules
    query = re.sub(r'\s+', ' ', query).strip() # transforme en vecteur numerique

    query_vector = vectorizer.transform([query])
    
    scores = cosine_similarity(
    query_vector,
    tfidf_matrix
    )[0] # compare limage ocr avec 2834 medicaments

    top_indices = np.argsort(scores)[-10:] #selection des 10 meilleurs
    top_medications = [
    ( i , medications_cache[i] )
    for i in reversed(top_indices)
    ]
    candidates = {}
    for idx, med in top_medications:
        tfidf_score = scores[idx] * 100
        search_name = med.get("search_name", "")
        name_ar = med.get("name_ar", "")
        active = (med.get("dci1") or "").lower()
       

        score_fr = fuzz.WRatio(query, search_name) 
        score_ar = fuzz.WRatio(query, name_ar)
        score_active = fuzz.WRatio(query, active) * 0.9
        med_dosage = (f"{med.get('dosage','')} "f"{med.get('unite_dosage','')}").lower()
        score_partial = fuzz.partial_ratio(query, search_name)
        score_token = fuzz.token_sort_ratio(query, search_name) * 0.95
        score_dosage = fuzz.partial_ratio( query, med_dosage)
        score_word = 0
        for word in query.split():
            if len(word) > 3:
                s = fuzz.partial_ratio(word, search_name)
                if s > score_word:
                    score_word = s

        bonus = 20 if search_name and search_name in query else 0
        bonus += 20 if name_ar and name_ar in query else 0
        bonus += 15 if active and active in query else 0

        fuzzy_score = max(
            score_fr,
            score_ar,
            score_active,
            score_dosage,
            score_partial,
            score_token,
            score_word
        ) 
        best_score = (
            0.4 * tfidf_score +
            0.6 * fuzzy_score
        ) + bonus
        best_score = min(best_score, 100)
        candidates[med["name_fr"]] = (best_score, med)

    if not candidates:
        return {
    "recognized": False,
    "message": "Aucun médicament reconnu. Veuillez prendre une photo plus nette et réessayer."
    }

    best_name = max(candidates, key=lambda x: candidates[x][0])
    best_score, best_med = candidates[best_name]

    if best_score < 55:
        return {
    "recognized": False,
    "message": "Aucun médicament reconnu. Veuillez prendre une photo plus nette et réessayer."
    }
           
    return {
        **best_med,
        "confidence_score": round(best_score / 100, 2),
        "confidence_level": get_confidence_level(best_score)
    }