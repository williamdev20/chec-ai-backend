from app.config.dependencies import model

def get_scrapping_paragraphs_embedding(paragraphs: list[str]):
    sentences = []
    for paragraph in paragraphs:
        sentences.append(paragraph)

    paragraphs_embedding = model.encode(sentences)

    return paragraphs_embedding


def check_poster_with_cosine_similarity(query_embedding, paragraphs_embedding, paragraphs: list[str]):
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