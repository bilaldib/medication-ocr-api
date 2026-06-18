import cv2
import numpy as np
import logging
import time

logger = logging.getLogger(__name__)

# PaddleOCR instances
ocr_ar = None
ocr_fr = None

def get_ocr(): #charge les modeles ocr
    global ocr_ar, ocr_fr
    if ocr_ar is None or ocr_fr is None:
        from paddleocr import PaddleOCR
        logger.info("Chargement PaddleOCR arabe...")
        ocr_ar = PaddleOCR(use_angle_cls=True, lang="ar", show_log=False, use_gpu=False)
        logger.info("Chargement PaddleOCR francais...")
        ocr_fr = PaddleOCR(use_angle_cls=True, lang="fr", show_log=False, use_gpu=False)
        logger.info("PaddleOCR pret!")
    return ocr_ar, ocr_fr

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image invalide ou corrompue")

        # Resize si trop grande
        h, w = img.shape[:2]
        if w > 1200:
            scale = 1200 / w
            img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)

        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # CLAHE — ameliore le contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

        # Deskew — corrige l'inclinaison
        inv = cv2.bitwise_not(gray)
        coords = np.column_stack(np.where(inv > 50))
        if len(coords) > 100:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = 90 + angle
            if abs(angle) <= 15:
                center = (gray.shape[1]//2, gray.shape[0]//2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                gray = cv2.warpAffine(gray, M, (gray.shape[1], gray.shape[0]),
                    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Binarisation Otsu
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Retour en RGB pour PaddleOCR
        rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
        return rgb

    except Exception as e:
        raise ValueError(f"Erreur preprocessing: {str(e)}")

def extract_text(image_bytes: bytes) -> dict:
    try:
        start = time.time()
        processed = preprocess_image(image_bytes)
        ocr_ar, ocr_fr = get_ocr()

        texts = []
        langs = []

        # Passe arabe
        result_ar = ocr_ar.ocr(processed, cls=True)
        if result_ar and result_ar[0]:
            for line in result_ar[0]:
                if line and len(line) >= 2:
                    text, conf = line[1][0], line[1][1]
                    if conf > 0.3 and text.strip():
                        texts.append(text.strip())
                        if 'ar' not in langs:
                            langs.append('ar')

        # Passe francais
        result_fr = ocr_fr.ocr(processed, cls=True)
        if result_fr and result_fr[0]:
            for line in result_fr[0]:
                if line and len(line) >= 2:
                    text, conf = line[1][0], line[1][1]
                    if conf > 0.3 and text.strip() and text not in texts:
                        texts.append(text.strip())
                        if 'fr' not in langs:
                            langs.append('fr')

        processing_time = round((time.time() - start) * 1000, 2)

        return {
            "raw_text": texts,
            "detected_languages": langs,
            "processing_time_ms": processing_time
        }

    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Erreur OCR: {str(e)}")