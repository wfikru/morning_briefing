from openai import OpenAI
import openai
import os
import time
import requests
import traceback

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_API_MODEL", "gemini-1.0-pro-001")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = os.getenv("GROK_API_URL", "https://api.grok.ai/v1/generate")

def generate_briefing(market_articles, political_articles):

    prompt = f"""
You are a professional financial news editor. Produce a concise, factual morning briefing for institutional/professional readers.

Output plain text only with these sections (in this order):

- HEADLINE: one-line summary (<= 20 words)
- TL;DR: one-sentence summary (<= 30 words)
- MARKET OVERVIEW: 3 bullets (each 12–20 words). Include one key market statistic or percentage change if present.
- POLITICAL DEVELOPMENTS: 2–3 bullets (each 12–20 words). Note material policy, regulatory, or geopolitical items.
- WHAT TO WATCH TODAY: 3 short bullets listing events/times/indicators to monitor (or "None").
- SOURCES: up to 3 short attributions or headlines (if available).

Rules:
- Use neutral, precise language; no emojis or sensational phrasing.
- Prefer active voice and concrete numbers (e.g., "S&P 500 down 1.2%", "inflation 3.4% year-on-year").
- If a claim is uncertain, mark it as "reporting: unconfirmed" or similar.
- Keep the total briefing under ~300 words.
- Do not invent facts. If no relevant data exists, state "No data available" for that item.

MARKET NEWS:
{market_articles}

POLITICAL NEWS:
{political_articles}
"""

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    # helper: Gemini (Google Generative Language API) fallback
    def call_gemini(input_text: str) -> str | None:
        if not GEMINI_API_KEY:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta2/{GEMINI_MODEL}:generate?key={GEMINI_API_KEY}"
        body = {
            "prompt": {"text": input_text},
            "temperature": 0.3,
            "maxOutputTokens": 800,
        }
        try:
            r = requests.post(url, json=body, timeout=30)
            r.raise_for_status()
            data = r.json()
            # candidates -> content
            candidates = data.get("candidates") or []
            if candidates:
                return candidates[0].get("content")
            # older responses may use "output"
            return data.get("output", {}).get("text")
        except Exception as e:
            print("DEBUG: Gemini call failed:", repr(e))
            try:
                print("DEBUG: Gemini response:", r.status_code, r.text)
            except Exception:
                pass
            print(traceback.format_exc())
            return None

    # helper: Grok fallback (generic HTTP POST). Configure GROK_API_URL and GROK_API_KEY.
    def call_grok(input_text: str) -> str | None:
        if not GROK_API_KEY:
            return None
        url = GROK_API_URL
        headers = {"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"}
        payload = {"prompt": input_text}
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            # common response keys
            for key in ("generated_text", "output", "result", "text", "content"):
                if isinstance(data, dict) and key in data:
                    val = data.get(key)
                    if isinstance(val, str) and val:
                        return val
            # if candidates list present
            candidates = data.get("candidates") if isinstance(data, dict) else None
            if candidates and isinstance(candidates, list) and candidates:
                first = candidates[0]
                if isinstance(first, dict):
                    return first.get("content") or first.get("text")
            return None
        except Exception as e:
            print("DEBUG: Grok call failed:", repr(e))
            try:
                print("DEBUG: Grok response:", r.status_code, r.text)
            except Exception:
                pass
            print(traceback.format_exc())
            return None

    # 1) Try Grok first
    grok_out = call_grok(prompt)
    if grok_out:
        return grok_out

    # 2) Try primary OpenAI with retries/backoff
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=800,
            )
            return response.choices[0].message.content

        except (openai.RateLimitError, openai.NotFoundError) as e:
            print("DEBUG: OpenAI rate limit or model error on attempt", attempt, repr(e))
            print(traceback.format_exc())
            if attempt < max_attempts - 1:
                time.sleep(2 ** attempt)
                continue
            break
        except Exception as e:
            print("DEBUG: OpenAI unknown error:", repr(e))
            print(traceback.format_exc())
            break

    # 3) Try Gemini API
    gemini_out = call_gemini(prompt)
    if gemini_out:
        return gemini_out

    # Final fallback: return the raw news content so the caller can still send something
    print("DEBUG: All AI providers failed — returning raw news content")
    raw = "MARKET NEWS:\n" + (market_articles or "") + "\n\nPOLITICAL NEWS:\n" + (political_articles or "")
    return raw
