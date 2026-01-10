import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query, page_size=15):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }
    return requests.get(url, params=params).json()["articles"]

def clean_articles(articles):
    seen = set()
    cleaned = []

    for a in articles:
        title = a["title"]
        if title not in seen:
            seen.add(title)
            cleaned.append({
                "title": title,
                "description": a["description"]
            })
    return cleaned
