from app.config.dependencies import get_ocr, get_spell
import pytesseract
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def paddleOCR_analyze(img_np):
    ocr = get_ocr()
    spell = get_spell()
    result = ocr.ocr(img_np)
    extracted_text = " ".join([word[1][0] for line in result for word in line]).lower()
    words = extracted_text.split()
    words_unknow = spell.unknown(words)
    corrected_words = [spell.correction(word) or word if word in words_unknow else word for word in words]
    return " ".join(corrected_words)

def tesseract_analyze(img):
    spell = get_spell()
    extracted_text = pytesseract.image_to_string(img).lower()
    words = extracted_text.split()
    words_unknow = spell.unknown(words)
    corrected_words = [spell.correction(word) or word if word in words_unknow else word for word in words]
    return " ".join(corrected_words)

def check_claim_with_more_correct_words(text):
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