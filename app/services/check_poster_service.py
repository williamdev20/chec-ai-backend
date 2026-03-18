from app.services.ocr_service import getFinalClaim
from app.services.google_check_service import google_fact_checking_claim
from app.services.similarity_service import get_scrapping_paragraphs_embedding, check_poster_with_cosine_similarity, get_final_claim_embedding
from app.services.scrapping_service import search_on_web
from app.services.agent_service import check_with_agent

def check_poster(img):
    claim = getFinalClaim(img)

    google_check_result = google_fact_checking_claim(claim)

    if google_check_result is None:
        claim_embedding = get_final_claim_embedding(claim)
        paragraphs = search_on_web(claim)
        paragraph_embedding = get_scrapping_paragraphs_embedding(paragraphs)

        cosine_similarity_result = check_poster_with_cosine_similarity(claim_embedding, paragraph_embedding, paragraphs)

        if isinstance(cosine_similarity_result, dict):
            agent_result = check_with_agent(claim, cosine_similarity_result["paragraph"])

            return agent_result
        else:
            return cosine_similarity_result
    else:
        return google_check_result