import os
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def summarize(news, markets):
    # include date + time for a clean header (local time)
    day_of_week = datetime.now().strftime("%A, %B %d, %Y %H:%M")

    prompt = f"""
You are an expert financial Telegram channel designer specializing in high-signal, extremely scannable morning market briefings.
Transform the provided inputs into two finished Telegram-ready briefings (Version A and Version B) that follow the exact design, tone, and formatting rules below.
Do NOT output any analysis, commentary, or extra text — return only the two versions clearly labeled "Version A" and "Version B".

Inputs (use as source material):
--- News Items ---
{chr(10).join(news)}

--- Market Items ---
{chr(10).join(markets)}

Top-level requirements:
- Audience: serious traders and investors. Tone: calm, factual, professional. No hype.
- Mobile-first: maximize scannability (most readers skim in <12s).
- Keep total length short (ideal: 18–25 lines). If necessary, be concise.
- Produce two variants:
  - Version A: Balanced, clean, professional (default).
  - Version B: Ultra-compact, ultra-scannable (shorter, denser).

Formatting and structural rules (follow exactly):
1) Exact section order:
   Header line with date and time (very clean)
   Macro & Political Highlights (3–6 bullets max)
   Major Indices (table-like with name, value, change)
   Crypto & Commodities Snapshot (short)
   Market Sentiment (very short — 1 line ideal)
   Stocks in Focus (5–7 names max, ordered by % change or importance, highlight top mover)
   Quick Take / Levels to Watch (1–2 very concise lines)
   Sources + Disclaimer (tiny single line)

2) Header:
   - Must include the date/time exactly as provided: {day_of_week}
   - Keep header minimal and clean (single line or two lines max).

3) Political/Macro bullets:
   - 3–6 bullets max.
   - Each bullet 8–14 words ideally — short, sourceable claim + direct market implication if relevant.

4) Major Indices:
   - Present as a monospace table or aligned code block for numbers.
   - One row per index: Name | Value | directional symbol + percent change
   - Use directional arrows: ▲ for up, ▼ for down (never parentheses).
   - Example row style (use monospaced alignment):
     `S&P 500     5,123.45   ▲ 0.43%`

5) Crypto & Commodities:
   - 2–4 short bullets or 1–2 aligned rows for major assets (BTC, ETH, Gold, Oil).
   - No emojis in price/percent lines.

6) Sentiment:
   - One short line: overall market tone (e.g., "Risk-On — cautious" or "Risk-Off — defensive").

7) Stocks in Focus:
   - 5–7 tickers/names max.
   - Order by % move or importance.
   - Highlight the top mover (bold or a leading ★).
   - Each line: TICKER — short note (1 clause) — % change (use ▲/▼).

8) Quick Take / Levels to Watch:
   - 1–2 lines only. Very actionable: key levels, catalysts, or headline to watch today.

9) Sources + Disclaimer:
   - One very small line at the end: "Sources: ... | Disclaimer: Not investment advice."

Visual / stylistic rules:
- Use at most 4–6 carefully chosen emojis total. No emoji spam.
- Use thin horizontal separator lines: ───────────────────── between major sections.
- Use Title Case for section headers.
- Use monospace-style number alignment (code block or inline backticks) for index/price lines.
- Percentage changes should use directional symbols: ▲ 0.43% or ▼ 0.43% (no ± sign, no parentheses).
- No animal or party emojis; avoid decorative emojis. No emojis in price/percent lines.
- Bold only section headers and the top mover. Italic for small notes if helpful.
- Keep each bullet/line focused and short.

Output requirements:
- Produce two clearly labeled sections: "Version A — Balanced" and "Version B — Compact".
- Each version must follow all the rules above.
- Do not include the raw prompt, source lists, or any meta commentary in the output.
- The content should be Telegram-ready plain text using simple Markdown-like formatting: **bold** for headers, `monospace` for numeric alignment, and minimal emojis as allowed.

Now rewrite the briefing using the inputs above. Return only the two versions as the final output.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
