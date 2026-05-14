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
git clone https://github.com/bilaldib/medication-ocr-api.git
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

## Interface Web

http://127.0.0.1:8000/ui

## Documentation interactive

http://127.0.0.1:8000/docs

## Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Health check |
| GET | /medications | Liste des 20 médicaments |
| GET | /medications/search?name=doli | Recherche par nom ou classe |
| GET | /ui | Interface web MedScan |
| POST | /recognize | Reconnaissance par image |

## Exemple de réponse

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
    "indication": "Douleurs et fièvre",
    "contre_indication": "Insuffisance hépatique grave",
    "posologie": "1 comprimé toutes les 6h, max 4/jour",
    "confidence_score": 1.0
  },
  "message": "Médicament détecté: Doliprane"
}
```

## Supervised by
- Abdelhak Mahmoudi
- Co-supervised by: Saad Frihi and Yasine Lehmiani