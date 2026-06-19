# 💊 Medication Box Recognition API

AI-powered system for recognizing medication boxes using OCR, Computer Vision and Fuzzy Matching against the CNOPS database.

---

## 👥 Project Team

| Name | GitHub |
|------|--------|
| Bilal Dib | [@bilaldib](https://github.com/bilaldib) |
| Doha ElBadra | [@doha-elbadra](https://github.com/doha-elbadra) |

---

## 🎓 Academic Supervisor

| Name | Role |
|------|------|
| Pr. Abdelhak Mahmoudi | Supervisor |
| Dr. Yassine Lehmiani | Co-supervisor |

---

## 📌 Project Overview

This project uses **PaddleOCR** and **Computer Vision** to extract and recognize medication names from medication box images. The system identifies medications from the **CNOPS database (2834 medications)** and returns detailed information including price, dosage, and reimbursement rate.

---

## ⚙️ Technologies Used

| Technology | Role |
|-----------|------|
| Python 3.9 | Main language |
| PaddleOCR 2.7.3 | Bilingual OCR (Arabic + French) |
| OpenCV | Image preprocessing |
| FastAPI | REST API |
| RapidFuzz | Fuzzy Matching |
| Pydantic v2 | Data validation |
| PostgreSQL | Database |
| SQLAlchemy | Async ORM |

---

## 🚀 Features

- 📸 Upload medication box image
- 🔍 Bilingual OCR (Arabic + French)
- 🧠 Fuzzy matching with CNOPS database (2834 medications)
- 💰 Price and reimbursement rate
- ✅ Confidence levels (recognized / probable / warning)
- 🏥 Health endpoint for API monitoring
- 📖 Swagger auto-documentation

---

## 🧠 How It Works

1. Image uploaded via `POST /recognize`
2. Preprocessing: resize → CLAHE → deskew → Otsu binarisation
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

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run the API
uvicorn app.main:app --reload
```

---

## 🧪 Testing

### 1️⃣ Test via Swagger UI
Open your browser:
```
http://127.0.0.1:8000/docs
```

### 2️⃣ Test via Web Interface
```
http://127.0.0.1:8000/ui
```

### 3️⃣ Test Health Endpoint
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

### 4️⃣ Test Recognition — SMECTA
```bash
curl -X POST http://127.0.0.1:8000/recognize \
  -F "file=@smecta.jpg"
```
Expected response:
```json
{
  "success": true,
  "best_match": {
    "name_fr": "SMECTA",
    "name_ar": "سميكتا",
    "active_ingredient": "DIOSMECTITE",
    "dosage": "3G",
    "forme": "POUDRE POUR SUSPENSION BUVABLE",
    "ppv": "52.4",
    "taux_remboursement": "0%",
    "confidence_level": "recognized",
    "confidence_score": 1.0
  }
}
```

### 5️⃣ Test Recognition — AMOXIL
```bash
curl -X POST http://127.0.0.1:8000/recognize \
  -F "file=@amoxil.jpg"
```
Expected response:
```json
{
  "success": true,
  "best_match": {
    "name_fr": "AMOXIL 500MG",
    "name_ar": "أموكسيل 500 مج",
    "active_ingredient": "AMOXICILLINE",
    "dosage": "500",
    "unite_dosage": "MG",
    "forme": "GELULE",
    "ppv": "28.5",
    "taux_remboursement": "70%",
    "confidence_level": "recognized",
    "confidence_score": 0.95
  }
}
```

### 6️⃣ Test Search Endpoint
```bash
curl http://127.0.0.1:8000/medications/search?name=amoxil
```

---

## 📁 Project Structure

```
medication-ocr-api/
├── app/
│   ├── main.py        ← FastAPI + endpoints + Lifespan
│   ├── ocr.py         ← PaddleOCR + preprocessing image
│   ├── matcher.py     ← RapidFuzz fuzzy matching
│   ├── models.py      ← Pydantic v2 schemas
│   └── static/
│       └── index.html ← Interface web
├── data/
│   ├── database.py    ← SQLAlchemy async engine
│   └── models.py      ← ORM models
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | API health status |
| GET | `/ui` | Web interface |
| GET | `/docs` | Swagger UI |
| POST | `/recognize` | Recognize medication from image |
| GET | `/medications` | List all medications |
| GET | `/medications/search` | Search medication by name |

---

*Master IT — Faculté des Sciences, Rabat — 2025/2026*bat — 2025/2026*
python app/main.py
