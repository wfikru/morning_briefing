from openai import OpenAI
import openai
import os
import time

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def generate_briefing(market_articles, political_articles):

    prompt = f"""
You are a professional financial news editor.

Create a concise morning briefing with:
- Market overview (10 bullets)
- Political developments (10 bullets)
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

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    max_attempts = 4
    for attempt in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=800,
            )

            return response.choices[0].message.content

        except openai.RateLimitError:
            if attempt == max_attempts - 1:
                return (
                    "Briefing unavailable: OpenAI quota exceeded. "
                    "Please check billing or try again later."
                )
            backoff = 2 ** attempt
            time.sleep(backoff)

        except Exception:
            raise
