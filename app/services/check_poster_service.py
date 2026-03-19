import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.services.ocr_service import getFinalClaim
from app.services.google_check_service import google_fact_checking_claim
from app.services.similarity_service import get_scrapping_paragraphs_embedding, check_poster_with_cosine_similarity, get_final_claim_embedding
from app.services.scrapping_service import search_on_web
from app.services.agent_service import check_with_agent

executor = ThreadPoolExecutor()

def check_poster(img):
    claim = getFinalClaim(img)

    with ThreadPoolExecutor() as pool:
        future_google = pool.submit(google_fact_checking_claim, claim)
        future_embedding = pool.submit(get_final_claim_embedding, claim)

        google_check_result = future_google.result()
        claim_embedding = future_embedding.result()

    if google_check_result is not None:
        return google_check_result

    paragraphs = search_on_web(claim)

    paragraph_embedding = get_scrapping_paragraphs_embedding(paragraphs)

    cosine_similarity_result = check_poster_with_cosine_similarity(
        claim_embedding, paragraph_embedding, paragraphs
    )

    if isinstance(cosine_similarity_result, dict):
        agent_result = check_with_agent(claim, cosine_similarity_result["paragraph"]).strip().upper() #type: ignore
        return agent_result == "TRUE"
    else:
        return cosine_similarity_result
