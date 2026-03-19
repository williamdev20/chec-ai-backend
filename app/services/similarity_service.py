from app.config.dependencies import get_model

def get_final_claim_embedding(text):
    model = get_model()

    sentence = text
    embedding = model.encode(sentence)

    return embedding

def get_scrapping_paragraphs_embedding(paragraphs: list[str]):
    model = get_model()

    sentences = []
    for paragraph in paragraphs:
        sentences.append(paragraph)

    paragraphs_embedding = model.encode(sentences)

    return paragraphs_embedding


def check_poster_with_cosine_similarity(query_embedding, paragraphs_embedding, paragraphs: list[str]):
    if not paragraphs:
        return {"paragraph": ""}

    model = get_model()
    similarities = model.similarity(query_embedding, paragraphs_embedding)
    score = similarities.max().item()
    top_paragraph_index = int(similarities.argmax().item())
    top_paragraph = paragraphs[top_paragraph_index]

    if score >= 0.85:
        return True
    elif score >= 0.30:
        return False
    else:
        return {"paragraph": top_paragraph}