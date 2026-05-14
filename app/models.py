from pydantic import BaseModel
from typing import Optional

class OCRResult(BaseModel):
    raw_text: list[str]
    detected_languages: list[str]

class MedicationMatch(BaseModel):
    id: int
    name_fr: str
    name_ar: str
    active_ingredient: str
    dosage: str
    form: str
    lab: str
    confidence_score: float
    indication: Optional[str] = None
    contre_indication: Optional[str] = None
    classe: Optional[str] = None
    posologie: Optional[str] = None

class RecognitionResponse(BaseModel):
    success: bool
    ocr_result: OCRResult
    best_match: Optional[MedicationMatch] = None
    message: str
