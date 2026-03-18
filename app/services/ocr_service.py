from app.config.dependencies import ocr, spell
import pytesseract

def paddleOCR_analyze(img):
    result = ocr.ocr(img)
    extracted_text = " ".join([word[1][0] for line in result for word in line]).lower()

    words = extracted_text.split()
    words_unknow = spell.unknown(words)
    corrected_words = [spell.correction(word) or word if word in words_unknow else word for word in words]
    paddleOCR_claim = " ".join(corrected_words)
    
    return paddleOCR_claim


def tesseract_analyze(img):
    extracted_text = pytesseract.image_to_string(img).lower()
    words = extracted_text.split()
    words_unknow = spell.unknown(words)
    corrected_words = [spell.correction(word) or word if word in words_unknow else word for word in words]
    tesseract_text = " ".join(corrected_words)

    return tesseract_text


def check_claim_with_more_correct_words(text):
    words = text.split()
    unknow_word = spell.unknown(words)

    return len(unknow_word)


def getFinalClaim(img):
    paddle_claim = paddleOCR_analyze(img) # Ajeitar aqui
    tesseract_claim = tesseract_analyze(img) # Ajeitar aqui
    final_claim = ""

    if check_claim_with_more_correct_words(paddle_claim) < check_claim_with_more_correct_words(tesseract_claim):
        final_claim = paddle_claim
    else:
        final_claim = tesseract_claim

    return final_claim
