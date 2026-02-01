import yfinance as yf

INDEXES = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI"
}

def fetch_market_summary():
    tickers = list(INDEXES.values())
    data = yf.download(tickers, period="2d", interval="1d", progress=False)

    summary = []
    for name, ticker in INDEXES.items():
        close_today = data["Close"][ticker].iloc[-1]
        close_yesterday = data["Close"][ticker].iloc[-2]
        change_pct = ((close_today - close_yesterday) / close_yesterday) * 100

        summary.append(
            f"{name}: {round(close_today, 2)} ({change_pct:+.2f}%)"
        )

    return summary
