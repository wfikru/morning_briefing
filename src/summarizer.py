import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def summarize(news, markets):
    prompt = f"""
Create a concise morning market briefing for Telegram.

News:
{chr(10).join(news)}

Market Data:
{chr(10).join(markets)}

Requirements:
- Short and clear
- Bullet points
- Professional but friendly tone
- Include overall sentiment
- Separate sections for: Stock Market News, Crypto Market News, Top Stocks to Watch, Political News

Format exactly:
🌅 Morning Market Brief

📰 Top News
• ...

📊 Stock Markets
• ...

🪙 Crypto Markets
• ...

⭐ Top Stocks to Watch
• ...

🏛️ Political News
• ...

📈 Sentiment
...
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
