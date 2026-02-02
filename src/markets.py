import yfinance as yf

INDEXES = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI"
}

TOP_STOCKS = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL"]
CRYPTO_SYMBOLS = ["BTC-USD", "ETH-USD"]  # Bitcoin and Ethereum

def fetch_market_summary():
    """Fetch market indices, top stocks, and crypto prices."""
    summary = []

    # Fetch stock indices
    tickers = list(INDEXES.values())
    data = yf.download(tickers, period="2d", interval="1d", progress=False)

    summary.append("=== STOCK INDICES ===")
    for name, ticker in INDEXES.items():
        close_today = data["Close"][ticker].iloc[-1]
        close_yesterday = data["Close"][ticker].iloc[-2]
        change_pct = ((close_today - close_yesterday) / close_yesterday) * 100
        summary.append(f"{name}: {round(close_today, 2)} ({change_pct:+.2f}%)")

    # Fetch top stocks to watch
    summary.append("\n=== TOP STOCKS TO WATCH ===")
    for symbol in TOP_STOCKS:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d")
            if len(data) >= 2:
                close_today = data["Close"].iloc[-1]
                close_yesterday = data["Close"].iloc[-2]
                change_pct = ((close_today - close_yesterday) / close_yesterday) * 100
                summary.append(f"{symbol}: ${round(close_today, 2)} ({change_pct:+.2f}%)")
        except Exception as e:
            print(f"Warning: Could not fetch {symbol}: {e}")

    # Fetch crypto prices
    summary.append("\n=== CRYPTO MARKET ===")
    for crypto in CRYPTO_SYMBOLS:
        try:
            ticker = yf.Ticker(crypto)
            data = ticker.history(period="2d")
            if len(data) >= 2:
                close_today = data["Close"].iloc[-1]
                close_yesterday = data["Close"].iloc[-2]
                change_pct = ((close_today - close_yesterday) / close_yesterday) * 100
                symbol_name = "Bitcoin" if "BTC" in crypto else "Ethereum"
                summary.append(f"{symbol_name}: ${round(close_today, 2)} ({change_pct:+.2f}%)")
        except Exception as e:
            print(f"Warning: Could not fetch {crypto}: {e}")

    return summary
