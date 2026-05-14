from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models import RecognitionResponse, OCRResult, MedicationMatch
from app.ocr import extract_text
from app.matcher import load_medications, find_best_match

app = FastAPI(
    title="Medication Box Recognition API",
    description="API pour reconnaître les médicaments à partir d'images de boîtes",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

medications = load_medications()

@app.get("/")
def root():
    return {"message": "Medication OCR API is running!", "version": "1.0.0"}

@app.get("/ui")
def ui():
    return FileResponse("app/static/index.html")

@app.get("/medications")
def get_medications():
    return {
        "total": len(medications),
        "medications": medications
    }

@app.get("/medications/search")
def search_medications(name: str):
    results = [
        med for med in medications
        if name.lower() in med["name_fr"].lower()
        or name.lower() in med["name_ar"]
        or name.lower() in med["active_ingredient"].lower()
        or name.lower() in med["classe"].lower()
    ]
    if not results:
        return {"total": 0, "results": [], "message": f"Aucun médicament trouvé pour '{name}'"}
    return {"total": len(results), "results": results}

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
        match = find_best_match(ocr_result["raw_text"], medications)
        if match:
            best_match = MedicationMatch(**match)
            message = f"Médicament détecté: {best_match.name_fr}"
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