# 💊 Medication Box Recognition API

AI-powered system for recognizing medication boxes using OCR, Computer Vision and Fuzzy Matching.

---

## 👥 Project Team

| Name | Role |
|------|------|
| Bilal Dib | Développeur principal |
| Doha ElBadra | Développeur principal |

---

## 🎓 Academic Supervisors

| Name | Role |
|------|------|
| Pr. Abdelhak Mahmoudi | Encadrant |
| Pr. Yassine Lehmiani | Co-encadrant |

---

## 📌 Project Overview

This project uses **PaddleOCR** and **Computer Vision** techniques to extract and recognize medication names from medication box images. The system identifies medications from the **CNOPS database (2834 medications)** and returns detailed information including price, dosage, and reimbursement rate.

---

## ⚙️ Technologies Used

| Technology | Role |
|-----------|------|
| Python 3.9 | Langage principal |
| PaddleOCR 2.7.3 | OCR bilingue (Arabe + Français) |
| OpenCV | Preprocessing des images |
| FastAPI | API REST |
| RapidFuzz | Fuzzy Matching |
| Pydantic v2 | Validation des données |
| PostgreSQL | Base de données |
| SQLAlchemy | ORM asynchrone |

---

## 🚀 Features

- 📸 Upload medication box image
- 🔍 Bilingual OCR (Arabic + French)
- 🧠 Fuzzy matching with CNOPS database
- 💰 Price and reimbursement rate
- ✅ Confidence levels (recognized / probable / warning)
- 🏥 Health endpoint for API monitoring
- 📖 Swagger documentation

---

## 🧠 How It Works

1. Image uploaded via `POST /recognize`
2. Preprocessing: resize → CLAHE → deskew → binarisation Otsu
3. PaddleOCR extracts text (Arabic pass + French pass)
4. RapidFuzz compares with 2834 CNOPS medications
5. Returns best match with confidence score

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/bilaldib/medication-ocr-api.git
cd medication-ocr-api

# Create virtual environment (Python 3.9)
py -3.9 -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run the API
uvicorn app.main:app --reload
```

---

## 🧪 Testing

### Test via Swagger UI
```
http://127.0.0.1:8000/docs
```

### Test via Web Interface
```
http://127.0.0.1:8000/ui
```

### Test Health Endpoint
```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "ocr_engine": "PaddleOCR 2.7.3",
  "db_loaded": true,
  "db_records": 2834,
  "ocr_ready": true,
  "version": "2.0.0"
}
```

### Test Recognition
```bash
curl -X POST http://127.0.0.1:8000/recognize \
  -F "file=@image.jpg"
```

Expected response:
```json
{
  "success": true,
  "best_match": {
    "name_fr": "SMECTA",
    "active_ingredient": "DIOSMECTITE",
    "dosage": "3G",
    "ppv": "52.4",
    "taux_remboursement": "0%",
    "confidence_level": "recognized"
  }
}
```

---

## 📁 Project Structure

```
medication-ocr-api/
├── app/
│   ├── main.py        ← FastAPI + endpoints + Lifespan
│   ├── ocr.py         ← PaddleOCR + preprocessing
│   ├── matcher.py     ← RapidFuzz matching
│   ├── models.py      ← Pydantic schemas
│   └── static/
│       └── index.html ← Web interface
├── data/
│   ├── database.py    ← SQLAlchemy models
│   └── models.py      ← DB models
├── requirements.txt
└── .env
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | API status |
| GET | `/ui` | Web interface |
| GET | `/docs` | Swagger UI |
| POST | `/recognize` | Recognize medication |
| GET | `/medications` | List all medications |
| GET | `/medications/search` | Search medication |

---

*Master IT — Faculté des Sciences, Rabat — 2025/2026*
python app/main.py
