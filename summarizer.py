from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_briefing(market_articles, political_articles):

    prompt = f"""
You are a professional financial news editor.

Create a concise morning briefing with:
- Market overview (2–3 bullets)
- Political developments (2–3 bullets)
- One short "What to watch today" section

MARKET NEWS:
{market_articles}

POLITICAL NEWS:
{political_articles}

Style:
- Neutral
- Clear
- Written for professionals
- No emojis
"""

    response = client.chat.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
