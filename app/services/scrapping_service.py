import os
import requests
from bs4 import BeautifulSoup

def search_on_web(query):
    url = "https://google.serper.dev/search"

    payload = {
        "q": query,
        "hl": "pt",
        "num": 10
    }

    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }

    headers_scrapping = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    if response.status_code != 200:
        print("[ERROR]: Houve erro na requisição da API: ", response.status_code)
        return []

    data = response.json()

    # Pegar os links #
    source_links = []
    scrapping_paragraphs = []

    organic_results = data.get("organic", [])
    if organic_results:
        for result in organic_results:
            link = result.get("link")
            if link:
                source_links.append(link)

    if not source_links:
        print("[WARN]: Nenhum link encontrado nos resultados da busca.")
        return []

    # Scrapping #
    for url in source_links:
        try:
            html = requests.get(url, headers=headers_scrapping, timeout=10, verify=False)

            if html.status_code != 200:
                continue

            soup = BeautifulSoup(html.text, "html.parser")
            paragraphs = soup.find_all("p")

            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                if text:
                    scrapping_paragraphs.append(text)

        except Exception as e:
            print(f"[ERROR]: Houve um erro no scrapping: {e}")

    return scrapping_paragraphs