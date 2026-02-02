import os
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def summarize(news, markets):
    # include date + time for a clean header (local time)
    day_of_week = datetime.now().strftime("%A, %B %d, %Y %H:%M")

    prompt = f"""
You are a professional financial news editor creating a high-signal Telegram morning briefing for active traders and investors.

Using ONLY the inputs provided, generate ONE finished Telegram-ready briefing.
The summary MUST include BOTH political news and stock market news.
Political items do NOT need to be market-related unless the connection is explicit.
DO NOT invent market impact for political news.
DO NOT include analysis, explanations, meta commentary, or raw inputs.
Return ONLY the final briefing text.

SOURCE MATERIAL:
NEWS:
{chr(10).join(news)}

MARKETS:
{chr(10).join(markets)}

DATE/TIME:
{day_of_week}

GLOBAL RULES:
• Audience: serious traders and investors
• Tone: calm, factual, professional — no hype
• Mobile-first: optimized for <12 second skim
• Total length target: 16–22 lines
• Prioritize clarity and signal over completeness
• Use simple Markdown (**bold**, `monospace`)
• No emojis in price or percentage lines

REQUIRED STRUCTURE (EXACT ORDER):

1) Header  
   • Single clean line (max 2 lines)  
   • Must include the date/time exactly as provided  

2) Top Summary  
   • 4–6 bullets TOTAL  
   • MUST include:
     – Political developments (domestic or global)
     – Stock market / macro / asset-class news
   • Political bullets:
     – May be standalone (no market angle required)
   • Market bullets:
     – Focus on equities, rates, FX, sectors, or flows
   • Each bullet:
     – 10–16 words
     – Factual, sourceable, no speculation

3) Major Indices  
   • Monospace aligned table or code block  
   • One row per index  
   • Format EXACTLY:  
     Name | Value | ▲/▼ Percent  
   • Use ▲ for up, ▼ for down  

4) Crypto & Commodities  
   • 2–4 short bullets OR aligned rows  
   • Focus on BTC, ETH, Gold, Oil  
   • No emojis in numeric lines  

5) Market Sentiment  
   • ONE short line only  
   • Describes overall tone (e.g., “Risk-On — selective”)

6) Stocks in Focus  
   • 5–7 names MAX  
   • Ordered by % move or importance  
   • Highlight the TOP mover using **bold** or ★  
   • Format:  
     TICKER — key catalyst or headline — ▲/▼ %  

7) Quick Take / What to Watch  
   • 1–2 concise lines  
   • Key events, levels, or headlines for today  

8) Sources + Disclaimer  
   • ONE small line only  
   • Format:  
     Sources: … | Disclaimer: Not investment advice  

STYLE CONSTRAINTS:
• Use 3–5 emojis TOTAL (max)
• No animal, party, or decorative emojis
• Title Case for section headers
• Bold ONLY:
  – Section headers
  – Top stock mover
• Percentages MUST use ▲ / ▼ symbols
• No forced correlations or inferred causality
• Avoid repetition across sections

FINAL INSTRUCTION:
Rewrite the briefing using the source material above.
Return ONLY the finished Telegram-ready briefing.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
