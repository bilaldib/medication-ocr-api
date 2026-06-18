from pydantic import BaseModel, Field
from typing import Optional, List

class OCRResult(BaseModel):
    raw_text: List[str] = Field(description="Textes extraits par PaddleOCR")
    detected_languages: List[str] = Field(description="Langues détectées: ar, fr")
    processing_time_ms: Optional[float] = Field(None, description="Temps de traitement en ms")

class MedicationMatch(BaseModel):
    #id: int = Field(description="Identifiant unique CNOPS")
    name_fr: str = Field(description="Nom officiel français")
    name_ar: str = Field(description="Nom en arabe")
    dci1: str = Field(description="Dénomination Commune Internationale (principe actif)")
    #active_ingredient: str = Field(description="Principe actif (DCI)")
    dosage: str = Field(description="Dosage du médicament")
    unite_dosage: str = Field(description="unite de dosage")
    forme: str = Field(description="Forme pharmaceutique")
    presentation: str = Field(description="Conditionnement du médicament")
    #lab: str = Field(description="Laboratoire fabricant")
    confidence_score: float = Field(description="Score de confiance entre 0 et 1")
    confidence_level: Optional[str] = Field(None, description="recognized / probable / warning / not_recognized")
    #indication: Optional[str] = Field(None, description="Indication thérapeutique")
    #contre_indication: Optional[str] = Field(None, description="Contre-indications")
    #classe: Optional[str] = Field(None, description="Classe thérapeutique")
    #posologie: Optional[str] = Field(None, description="Posologie recommandée")
    ppv: Optional[float] = Field(None, description="Prix Public de Vente en MAD")
    ph: Optional[float] = Field(None, description="Prix Hospitalier")
    prix_br: Optional[float] = Field(None, description="Base de remboursement")
    princeps_generique: Optional[str] = Field(description="un princeps ou un générique")
    taux_remboursement: Optional[str] = Field(None, description="Taux de remboursement CNOPS")
    search_name: Optional[str] = Field(None, description="Nom normalisé pour la recherche")

class RecognitionResponse(BaseModel):
    success: bool = Field(description="True si médicament identifié")
    ocr_result: OCRResult = Field(description="Résultat brut de l'OCR")
    best_match: Optional[MedicationMatch] = Field(None, description="Meilleur médicament trouvé")
    message: str = Field(description="Message lisible en français")

class HealthResponse(BaseModel):
    status: str = Field(description="Statut de l'API: ok")
    ocr_engine: str = Field(description="Moteur OCR utilisé")
    db_loaded: bool = Field(description="Base de données chargée")
    db_records: int = Field(description="Nombre de médicaments en base")
    ocr_ready: bool = Field(description="Modèles OCR prêts")
    version: str = Field(description="Version de l'API")

class SearchResponse(BaseModel):
    total: int = Field(description="Nombre de résultats trouvés")
    results: List[MedicationMatch] = Field(description="Liste des médicaments trouvés")
    message: Optional[str] = Field(None, description="Message si aucun résultat") 