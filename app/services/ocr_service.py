from app.config.dependencies import get_ocr, get_spell
import pytesseract
from PIL import Image
import numpy as np

def paddleOCR_analyze(img_stream):
    ocr = get_ocr()
    spell = get_spell()

    img_stream.seek(0)
    img = Image.open(img_stream)
    img_np = np.array(img)

    result = ocr.ocr(img_np)
    extracted_text = " ".join([word[1][0] for line in result for word in line]).lower()

    words = extracted_text.split()
    words_unknow = spell.unknown(words)
    corrected_words = [spell.correction(word) or word if word in words_unknow else word for word in words]
    paddleOCR_claim = " ".join(corrected_words)
    
    return paddleOCR_claim


def tesseract_analyze(img_stream):
    spell = get_spell()

    img_stream.seek(0)
    img = Image.open(img_stream)

    extracted_text = pytesseract.image_to_string(img).lower()
    words = extracted_text.split()
    words_unknow = spell.unknown(words)
    corrected_words = [spell.correction(word) or word if word in words_unknow else word for word in words]
    tesseract_text = " ".join(corrected_words)

    return tesseract_text


def check_claim_with_more_correct_words(text):
    spell = get_spell()

    words = text.split()
    unknow_word = spell.unknown(words)

    return len(unknow_word)


def getFinalClaim(img_stream):
    paddle_claim = paddleOCR_analyze(img_stream)
    tesseract_claim = tesseract_analyze(img_stream)
    final_claim = ""

    if check_claim_with_more_correct_words(paddle_claim) < check_claim_with_more_correct_words(tesseract_claim):
        final_claim = paddle_claim
    else:
        final_claim = tesseract_claim

    return final_claim
