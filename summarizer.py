from openai import OpenAI
import openai
import os
import time
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/text-bison-001")
HF_MODEL = os.getenv("HF_MODEL", "tiiuae/falcon-7b-instruct")
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
        except Exception:
            return None

    # helper: Hugging Face Inference API fallback
    def call_hf(input_text: str) -> str | None:
        hf_token = os.getenv("HF_API_TOKEN")
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}
        payload = {"inputs": input_text, "parameters": {"max_new_tokens": 400}}
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            data = r.json()
            # HF can return text or an array with generated_text
            if isinstance(data, list) and data and isinstance(data[0], dict):
                return data[0].get("generated_text") or data[0].get("generated_text", None)
            if isinstance(data, dict):
                return data.get("generated_text") or data.get("generated_text", None)
            return None
        except Exception:
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
        except Exception:
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

        except (openai.RateLimitError, openai.NotFoundError):
            # try next fallback after retries exhausted
            if attempt < max_attempts - 1:
                time.sleep(2 ** attempt)
                continue
            break
        except Exception:
            # unknown OpenAI error — proceed to fallbacks
            break

    # 3) Try Gemini API
    gemini_out = call_gemini(prompt)
    if gemini_out:
        return gemini_out

    # 3) Final fallback: Hugging Face Inference API
    hf_out = call_hf(prompt)
    if hf_out:
        return hf_out

    return (
        "Briefing unavailable: all AI providers failed or are unavailable. "
        "Please check API keys and quota, and try again later."
    )
