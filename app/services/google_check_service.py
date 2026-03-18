import os
import requests

def google_fact_checking_claim(query):
    is_real = None
    qty_is_fake = 0
    qty_is_real = 0

    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    params = {
        "query": query,
        "languageCode": "pt",
        "key": os.getenv("API_KEY")
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("[ERROR]: Houve um erro na requisição: ", response.status_code)
        return
    
    data = response.json()

    if "claims" in data and data["claims"]:
        for claim in data["claims"]:
            reviews = claim["claimReview"]
            if reviews:
                match reviews[0]["textualRating"]:
                    case "Falso":
                        qty_is_fake += 1
                    case "Enganoso":
                        qty_is_fake += 1
                    case "Verdadeiro":
                        qty_is_real += 1
                    # Falta um default aqui pra caso não seja nenhum dos valores listados acima
            else:
                return None
        
        if qty_is_fake > qty_is_real:
            is_real = False
        else:
            is_real = True

        return is_real
    else:

        return None
