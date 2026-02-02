import os
import requests

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news():
    """Fetch business and political news."""
    api_key = os.environ["NEWS_API_KEY"]
    news_items = []

    # Fetch business news
    params = {
        "category": "business",
        "language": "en",
        "pageSize": 5,
        "apiKey": api_key,
    }

    response = requests.get(NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()

    articles = response.json().get("articles", [])
    for a in articles:
        title = a.get("title")
        description = a.get("description")
        if title:
            news_items.append(f"{title}. {description or ''}")

    # Fetch political news
    params_politics = {
        "category": "politics",
        "language": "en",
        "pageSize": 3,
        "apiKey": api_key,
    }

    try:
        response_politics = requests.get(NEWS_API_URL, params=params_politics, timeout=10)
        response_politics.raise_for_status()
        politics_articles = response_politics.json().get("articles", [])
        for a in politics_articles:
            title = a.get("title")
            description = a.get("description")
            if title:
                news_items.append(f"[POLITICS] {title}. {description or ''}")
    except Exception as e:
        print(f"Warning: Could not fetch political news: {e}")

    return news_items
