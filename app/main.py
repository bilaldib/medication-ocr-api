from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import RecognitionResponse, OCRResult, MedicationMatch, HealthResponse
from app.ocr import extract_text, get_ocr
from app.matcher import initialize_matcher, find_best_match, AsyncSessionLocal, medication_to_dict
import app.ocr as ocr_module
from app import matcher
from sqlalchemy import select, or_
from data.models import Medication


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_ocr() #charge les modeles paddleocr
    await initialize_matcher()
    yield


app = FastAPI(
    title="Medication Box Recognition API",
    description="API pour reconnaître les médicaments à partir d'images de boîtes",
    version="2.0.0",
    lifespan=lifespan
) #creation de l'app

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Medication OCR API is running!",
        "version": "2.0.0",
        "ocr_engine": "PaddleOCR 2.7.3",
        "database": "medicaments_db PostgreSQL"
    }


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        ocr_engine="PaddleOCR 2.7.3",
        db_loaded=True,
        db_records=len(matcher.medications_cache),
        ocr_ready=ocr_module.ocr_ar is not None and ocr_module.ocr_fr is not None,
        version="2.0.0"
    )


@app.get("/ui")
def ui():
    return FileResponse("app/static/index.html")


@app.post("/recognize", response_model=RecognitionResponse)
async def recognize_medication(file: UploadFile = File(...)):

    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400,
            detail="Format non supporté. Utilisez JPEG, PNG ou WEBP."
        )

    try:
        image_bytes = await file.read()

        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Image vide.")

        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image trop grande. Maximum 10MB.")

        ocr_result = extract_text(image_bytes)

        if not ocr_result["raw_text"]:
            return RecognitionResponse(
                success=False,
                ocr_result=OCRResult(**ocr_result),
                best_match=None,
                message="Aucun texte détecté dans l'image."
            )

        match = find_best_match(ocr_result["raw_text"])

        if match:
            best_match = MedicationMatch(**match)
            nom = best_match.name_fr or best_match.search_name or best_match.name_ar or "Inconnu"
            message = f"Médicament détecté: {nom}"
        else:
            best_match = None
            message = "Aucun médicament reconnu dans la base de données."

        return RecognitionResponse(
            success=True,
            ocr_result=OCRResult(**ocr_result),
            best_match=best_match,
            message=message
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")