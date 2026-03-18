from paddleocr import PaddleOCR
from spellchecker import SpellChecker
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

ocr = PaddleOCR(use_angle_cls=True, lang="pt", show_log=False)
spell = SpellChecker(language="pt")
model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
