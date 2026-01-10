from news import fetch_news
from summarizer import generate_briefing
from telegram import send_message
from dotenv import load_dotenv
load_dotenv()

MARKET_QUERY = (
    "stock market OR stocks OR inflation OR interest rates "
    "OR Federal Reserve OR earnings"
)

POLITICS_QUERY = (
    "politics OR government OR congress OR senate "
    "OR election OR president"
)

market = fetch_news(MARKET_QUERY)
politics = fetch_news(POLITICS_QUERY)

briefing = generate_briefing(market, politics)

send_message(briefing)
