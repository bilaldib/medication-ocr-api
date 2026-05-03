# Medication Box Recognition API

API intelligente pour la reconnaissance de médicaments à partir d'images de boîtes, en utilisant OCR et Computer Vision.

## Technologies utilisées

- **FastAPI** — Framework API
- **EasyOCR** — Extraction de texte (Arabe + Anglais)
- **OpenCV** — Prétraitement des images
- **RapidFuzz** — Matching avec la base de données

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/medication-ocr-api.git
cd medication-ocr-api
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn app.main:app --reload
```

L'API sera disponible sur : http://127.0.0.1:8000

## Documentation interactive

http://127.0.0.1:8000/docs

## Endpoint principal

### POST /recognize

Envoie une image d'une boîte de médicament et reçois le médicament détecté.

**Paramètres:**
- `file` — Image (JPEG, PNG, WEBP)

**Réponse:**
```json
{
  "success": true,
  "ocr_result": {
    "raw_text": ["SANOFI", "douleurs et fievre"],
    "detected_languages": ["fr"]
  },
  "best_match": {
    "name_fr": "Doliprane",
    "name_ar": "دوليبران",
    "active_ingredient": "Paracétamol",
    "dosage": "1000mg",
    "lab": "Sanofi",
    "confidence_score": 0.57
  },
  "message": "Médicament détecté: Doliprane"
}
```

## Supervised by
- Abdelhak Mahmoudi
- Co-supervised by: Saad Frihi and Yasine Lehmiani