from news import fetch_news
from markets import fetch_market_summary
from summarizer import summarize
from telegram_sender import send_to_telegram

def main():
    news = fetch_news()
    markets = fetch_market_summary()
    summary = summarize(news, markets)
    send_to_telegram(summary)

if __name__ == "__main__":
    main()
