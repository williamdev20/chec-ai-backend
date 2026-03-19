import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_url(url):
    headers_scrapping = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    try:
        html = requests.get(url, headers=headers_scrapping, timeout=5, verify=False)  # timeout 5 ao invés de 10
        if html.status_code != 200:
            return []
        soup = BeautifulSoup(html.text, "html.parser")
        return [p.get_text(strip=True) for p in soup.find_all("p")]
    except Exception as e:
        print(f"[ERROR]: Houve um erro no scrapping: {e}")
        return []

def search_on_web(query):
    url = "https://google.serper.dev/search"
    payload = {"q": query, "hl": "pt", "num": 5}
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("[ERROR]: Houve erro na requisição da API: ", response.status_code)
        return []

    data = response.json()
    source_links = [result["link"] for result in data.get("organic", [])]

    scrapping_paragraphs = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(scrape_url, url): url for url in source_links}
        for future in as_completed(futures):
            scrapping_paragraphs.extend(future.result())

    return scrapping_paragraphs