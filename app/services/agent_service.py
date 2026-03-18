from app.config.dependencies import client

def check_with_agent(query, top_paragraph):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Você é um agente de IA responsável por checar a veracidade de uma informação retirada de um cartaz para saber se ela se trata de uma fake news ou não. Você receberá uma query (texto/pergunta) e um parágrafo com instrução. Você deve analisar essa query e o parágrafo que foi fornecido e verificar se é uma fake news ou não. Para a confirmação das informações fornecidas, você não deve verificar apenas se o parágrafo concorda com a query, mas sim verificar se a informação do parágrafo é um fato real baseado em conhecimento científico. Se o parágrafo contiver informação falsa, pseudociência ou desinformação, retorne 'FALSE'. Mesmo que o parágrafo concorde com a query, se ambos estiverem errados, retorne 'FALSE'. Só retorne 'TRUE' se a informação for comprovadamente verdadeira. Você dever retornar apenas, e somente apenas, 'TRUE' ou 'FALSE'"
            },
            {
                "role": "user",
                "content":
                f"""
                    Query: {query}. Parágrafo: {top_paragraph}

                    Pergunta:
                    O parágrafo responde corretamente a query com base no mundo real e em conhecimento científico e conhecimento confiável? É preciso que a informação seja cientificamente correta, e não verificar apenas a semelhança semântica da query e o parágrafo.

                """
            }
        ],
        temperature=0,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
        stop=None
    )

    return completion.choices[0].message.content