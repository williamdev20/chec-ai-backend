from functools import lru_cache

@lru_cache(maxsize=1)
def get_ocr():
    from paddleocr import PaddleOCR
    return PaddleOCR(use_angle_cls=True, lang="pt", show_log=False)

@lru_cache(maxsize=1)
def get_spell():
    from spellchecker import SpellChecker
    return SpellChecker(language="pt")

@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

@lru_cache(maxsize=1)
def get_client():
    from groq import Groq
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return Groq(api_key=os.getenv("GROQ_API_KEY"))