from app.config.dependencies import get_ocr
import pytesseract
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def paddleOCR_analyze(img_np):
    ocr = get_ocr()
    result = ocr.ocr(img_np)
    return " ".join([word[1][0] for line in result for word in line]).lower()

def tesseract_analyze(img):
    return pytesseract.image_to_string(img).lower().strip()

def check_claim_with_more_correct_words(text):
    from app.config.dependencies import get_spell
    spell = get_spell()
    return len(spell.unknown(text.split()))

def getFinalClaim(img_stream):
    img_stream.seek(0)
    img = Image.open(img_stream)
    img_np = np.array(img)

    with ThreadPoolExecutor(max_workers=2) as pool:
        future_paddle = pool.submit(paddleOCR_analyze, img_np)
        future_tesseract = pool.submit(tesseract_analyze, img)
        paddle_claim = future_paddle.result()
        tesseract_claim = future_tesseract.result()

    if check_claim_with_more_correct_words(paddle_claim) < check_claim_with_more_correct_words(tesseract_claim):
        return paddle_claim
    return tesseract_claim