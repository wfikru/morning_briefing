# Morning Briefing

An automated daily briefing bot that compiles and sends market and political news via Telegram.

## Features

- **Stock Market News**: Top 5 latest stock market news articles via Polygon API
- **Crypto Market News**: Top 5 cryptocurrency and blockchain news articles
- **Top Stocks to Watch**: Daily movers for major tech stocks (AAPL, MSFT, NVDA, TSLA, GOOGL)
- **Political News**: Top 5 US political news headlines via NewsAPI
- **Telegram Integration**: Automatically sends compiled briefing to your Telegram channel daily

## Setup

### Prerequisites

- Python 3.12+
- API Keys:
  - [Polygon.io API Key](https://polygon.io/) (for stock and crypto news)
  - [NewsAPI Key](https://newsapi.org/) (for political news)
  - [Telegram Bot Token](https://core.telegram.org/bots#6-botfather)
  - Telegram Chat ID or Channel

### Installation

1. Clone the repository:
```bash
git clone https://github.com/fikruworku/morning_briefing.git
cd morning_briefing
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export POLYGON_API_KEY="your_polygon_key"
export NEWSAPI_KEY="your_newsapi_key"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHANNEL_ID="your_chat_id"
```

### Running Locally

```bash
python morning_briefing.py
```

### GitHub Actions Workflow

The project includes a GitHub Actions workflow (`daily_notify.yml`) that runs daily at 8:00 AM UTC.

To enable it, add the following secrets to your GitHub repository settings:
- `POLYGON_API_KEY`
- `NEWSAPI_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHANNEL_ID`

## Project Structure

```
.
├── morning_briefing.py      # Main briefing compilation and send logic
├── telegram.py              # Telegram utility functions
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `POLYGON_API_KEY` | Polygon.io API key for stock/crypto data | Yes |
| `NEWSAPI_KEY` | NewsAPI key for political headlines | Yes |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | Yes |
| `TELEGRAM_CHANNEL_ID` | Target Telegram chat/channel ID | Yes |

## Error Handling

The script includes robust error handling:
- Missing API keys are detected and logged with warnings
- Network failures are caught with timeouts
- Missing Telegram credentials skip sending but don't crash the program
- Detailed error messages are printed to console

## License

MIT
