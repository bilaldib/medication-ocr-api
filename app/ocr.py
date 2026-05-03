import easyocr
import cv2
import numpy as np

reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['ar', 'en'], gpu=False)
    return reader

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image invalide ou corrompue")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary
    except Exception as e:
        raise ValueError(f"Erreur preprocessing: {str(e)}")

def extract_text(image_bytes: bytes) -> dict:
    try:
        processed = preprocess_image(image_bytes)
        r = get_reader()
        results = r.readtext(processed)
        texts = [text for (_, text, conf) in results if conf > 0.3]
        langs = []
        for text in texts:
            if any('\u0600' <= c <= '\u06ff' for c in text):
                if 'ar' not in langs:
                    langs.append('ar')
            else:
                if 'fr' not in langs:
                    langs.append('fr')
        return {
            "raw_text": texts,
            "detected_languages": langs
        }
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Erreur OCR: {str(e)}")