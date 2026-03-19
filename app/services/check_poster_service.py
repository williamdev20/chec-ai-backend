import time
from app.services.ocr_service import getFinalClaim
from app.services.google_check_service import google_fact_checking_claim
from app.services.similarity_service import get_scrapping_paragraphs_embedding, check_poster_with_cosine_similarity, get_final_claim_embedding
from app.services.scrapping_service import search_on_web
from app.services.agent_service import check_with_agent
from concurrent.futures import ThreadPoolExecutor

def check_poster(img):
    t0 = time.time()

    claim = getFinalClaim(img)
    print(f"[TEMPO] OCR: {time.time() - t0:.2f}s | claim: {claim}")

    t1 = time.time()
    with ThreadPoolExecutor() as pool:
        future_google = pool.submit(google_fact_checking_claim, claim)
        future_embedding = pool.submit(get_final_claim_embedding, claim)
        google_check_result = future_google.result()
        claim_embedding = future_embedding.result()
    print(f"[TEMPO] Google check + embedding: {time.time() - t1:.2f}s")

    if google_check_result is not None:
        print(f"[TEMPO] TOTAL (google check): {time.time() - t0:.2f}s")
        return google_check_result

    t2 = time.time()
    paragraphs = search_on_web(claim)
    print(f"[TEMPO] Scraping: {time.time() - t2:.2f}s | {len(paragraphs)} parágrafos")

    if not paragraphs:
        print("[WARN] Scraping não retornou parágrafos, indo direto pro agente")
        agent_result = check_with_agent(claim, "Nenhum parágrafo encontrado.").strip().upper() #type: ignore
        print(f"[TEMPO] TOTAL: {time.time() - t0:.2f}s")
        return agent_result == "TRUE"

    t3 = time.time()
    paragraph_embedding = get_scrapping_paragraphs_embedding(paragraphs)
    print(f"[TEMPO] Paragraph embedding: {time.time() - t3:.2f}s")

    t4 = time.time()
    cosine_similarity_result = check_poster_with_cosine_similarity(claim_embedding, paragraph_embedding, paragraphs)
    print(f"[TEMPO] Cosine similarity: {time.time() - t4:.2f}s")

    if isinstance(cosine_similarity_result, dict):
        t5 = time.time()
        agent_result = check_with_agent(claim, cosine_similarity_result["paragraph"]).strip().upper() #type: ignore
        print(f"[TEMPO] Agent (Groq): {time.time() - t5:.2f}s")
        print(f"[TEMPO] TOTAL: {time.time() - t0:.2f}s")
        return agent_result == "TRUE"
    else:
        print(f"[TEMPO] TOTAL: {time.time() - t0:.2f}s")
        return cosine_similarity_result