import os
import requests

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news():
    api_key = os.environ["NEWS_API_KEY"]

    params = {
        "category": "business",
        "language": "en",
        "pageSize": 7,
        "apiKey": api_key,
    }

    response = requests.get(NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()

    articles = response.json().get("articles", [])

    news_items = []
    for a in articles:
        title = a.get("title")
        description = a.get("description")
        if title:
            news_items.append(f"{title}. {description or ''}")

    return news_items
