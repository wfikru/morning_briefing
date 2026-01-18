import requests
import os

def get_stock_news(polygon_api_key):
    url = f"https://api.polygon.io/v3/reference/news?limit=5&order=desc&sort=published_utc&apiKey={polygon_api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error fetching stock news."
    data = response.json()
    news_items = []
    for article in data.get('results', []):
        title = article.get('title', 'No title')
        publisher = article['publisher'].get('name', 'Unknown')
        description = article.get('description', 'No description')
        news_items.append(f"{title} - {publisher}: {description}")
    return '\n\n'.join(news_items)

def get_political_news(newsapi_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=politics&pageSize=5&apiKey={newsapi_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return "Error fetching political news."
    data = response.json()
    news_items = []
    for article in data.get('articles', []):
        title = article.get('title', 'No title')
        source = article['source'].get('name', 'Unknown')
        description = article.get('description', 'No description')
        news_items.append(f"{title} - {source}: {description}")
    return '\n\n'.join(news_items)

def send_to_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'  # Optional: For better formatting if needed
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        print("Error sending message:", response.text)

# Replace these with your actual values
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Compile the briefing
stock_news = get_stock_news(POLYGON_API_KEY)
political_news = get_political_news(NEWSAPI_KEY)
briefing = (
    "<b>Morning Briefing - Stock Market and Political News</b>\n\n"
    "<b>Stock Market News:</b>\n" + stock_news + "\n\n"
    "<b>Political News:</b>\n" + political_news
)

# Send it
send_to_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, briefing)
print("Briefing sent!")  # For console feedback when running manually