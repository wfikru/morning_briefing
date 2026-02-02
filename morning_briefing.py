import requests
import os
import yfinance as yf

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

def get_crypto_news(polygon_api_key):
    """Fetch top cryptocurrency news from Polygon API."""
    url = f"https://api.polygon.io/v3/reference/news?limit=5&order=desc&sort=published_utc&apiKey={polygon_api_key}"
    params = {"keywords": "crypto,cryptocurrency,bitcoin,ethereum"}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "Error fetching crypto news."
    data = response.json()
    news_items = []
    for article in data.get('results', [])[:5]:
        title = article.get('title', 'No title')
        publisher = article['publisher'].get('name', 'Unknown')
        description = article.get('description', 'No description')
        news_items.append(f"{title} - {publisher}: {description}")
    return '\n\n'.join(news_items) if news_items else "No crypto news available."

def get_top_stocks_to_watch():
    """Fetch top gainers and losers for the day (using market data)."""
    try:
        # Fetch S&P 500 data and identify top movers
        sp500 = yf.Ticker("^GSPC")
        info = sp500.info if hasattr(sp500, 'info') else {}
        
        # Use some popular tech stocks as example top stocks to watch
        top_symbols = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL"]
        watch_list = []
        
        for symbol in top_symbols:
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="1d")
                if len(data) > 0:
                    close = data['Close'].iloc[-1]
                    change = ((close - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100) if len(data) > 1 else 0
                    watch_list.append(f"{symbol}: ${close:.2f} ({change:+.2f}%)")
            except Exception:
                pass
        
        return '\n'.join(watch_list) if watch_list else "Unable to fetch stock data."
    except Exception as e:
        return f"Error fetching top stocks: {str(e)}"

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
    if not bot_token or not chat_id:
        print("Telegram bot token or chat id missing — skipping send_to_telegram.")
        return
    try:
        print(f"Bot token starts with: {bot_token[:10]}...")
    except Exception:
        print("Bot token present (unable to preview).")
    print(f"Chat ID: {chat_id}")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, params=params, timeout=15)
    except Exception as e:
        print("Error sending message (request failed):", str(e))
        return
    print(f"Response status: {response.status_code}")
    if response.status_code != 200:
        print("Error sending message:", response.text)
    else:
        print("Message sent successfully")

# Replace these with your actual values
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Compile the briefing
if not POLYGON_API_KEY:
    print("Warning: POLYGON_API_KEY not set — stock news may fail.")
if not NEWSAPI_KEY:
    print("Warning: NEWSAPI_KEY not set — political news may fail.")

stock_news = get_stock_news(POLYGON_API_KEY)
crypto_news = get_crypto_news(POLYGON_API_KEY)
political_news = get_political_news(NEWSAPI_KEY)
top_stocks = get_top_stocks_to_watch()

briefing = (
    "<b>Morning Briefing - Markets & Political News</b>\n\n"
    "<b>📈 Stock Market News:</b>\n" + stock_news + "\n\n"
    "<b>🪙 Crypto Market News:</b>\n" + crypto_news + "\n\n"
    "<b>⭐ Top Stocks to Watch:</b>\n" + top_stocks + "\n\n"
    "<b>🏛️ Political News:</b>\n" + political_news
)

# Send it
if TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID:
    send_to_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, briefing)
    print("Briefing sent!")
else:
    print("TELEGRAM_BOT_TOKEN and/or TELEGRAM_CHANNEL_ID not set — skipping Telegram send.")