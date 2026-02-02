import os
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def summarize(news, markets):
    day_of_week = datetime.now().strftime("%A, %B %d, %Y")
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
- 4-5 bullets for political news
- Combine stock and crypto markets in one section, including relevant news and current market state
- Reorder sections as: Political News first, then Markets, then Sentiment, then Stocks to Watch
- Include the date at the top

Format exactly:
🌅 Morning Market Brief
📅 {day_of_week}

🏛️ Political News
• ...
• ...
• ...
• ...
• ...

📊 Markets (Stock & Crypto)
• [Include relevant market news and current indices/prices]
• ...
• ...

📈 Sentiment
...

⭐ Top Stocks to Watch
• ...
• ...
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
