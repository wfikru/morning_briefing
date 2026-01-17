from openai import OpenAI
import os
import time
import traceback
import requests  # still needed for any extras, but minimized

# ────────────────────────────────────────────────
# Clients & Config (use env vars for security)
# ────────────────────────────────────────────────
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")          # or gpt-4o

# xAI / Grok — OpenAI compatible
grok_client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1",
)
GROK_MODEL = os.getenv("GROK_MODEL", "grok-4-1-fast-reasoning")         # fast & capable; alt: grok-4

# Gemini — native SDK (pip install google-generativeai)
try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")         # excellent 2026 default
except ImportError:
    print("WARNING: google-generativeai not installed → Gemini fallback disabled")
    GEMINI_API_KEY = None

def estimate_tokens(text: str) -> int:
    """Rough token estimator (~4 chars/token)"""
    return len(text) // 4 + 100  # conservative

def generate_briefing(market_articles, political_articles):
    """
    Generate morning briefing with multi-LLM fallback.
    Order: OpenAI → Grok → Gemini → raw text
    """
    # ────────────────────────────────────────────────
    # Prepare input text
    # ────────────────────────────────────────────────
    def _to_text(items):
        if not items:
            return ""
        out = []
        for item in items:
            if isinstance(item, dict):
                title = item.get("title") or item.get("headline") or ""
                desc = item.get("description") or item.get("summary") or item.get("content") or ""
                if title and desc:
                    out.append(f"{title} — {desc}")
                elif title:
                    out.append(title)
                elif desc:
                    out.append(desc)
            else:
                out.append(str(item))
        return "\n\n".join(out)

    market_text = _to_text(market_articles)
    political_text = _to_text(political_articles)

    full_input = f"MARKET NEWS:\n{market_text}\n\nPOLITICAL NEWS:\n{political_text}"
    token_est = estimate_tokens(full_input)

    if token_est > 80000:
        print(f"WARNING: Input very large (~{token_est} tokens) — may exceed limits or cost a lot")

    # ────────────────────────────────────────────────
    # Strong, consistent prompt
    # ────────────────────────────────────────────────
    prompt = f"""
You are a professional financial news editor. Produce a concise, factual morning briefing for institutional readers.

Output plain text only — use exactly these sections (in order):

- HEADLINE: one-line summary (≤20 words)
- TL;DR: one-sentence summary (≤30 words)
- MARKET OVERVIEW: 3 bullets (12–20 words each). Include ≥1 key stat/percentage if available.
- POLITICAL DEVELOPMENTS: 2–3 bullets (12–20 words each). Focus on policy, regulation, geopolitics.
- WHAT TO WATCH TODAY: 3 short bullets (events, times, indicators) or "None notable".
- SOURCES: up to 3 short attributions/headlines (if relevant).

Rules:
- Neutral, precise language. Active voice. Concrete numbers (e.g. "S&P 500 -1.2%").
- No emojis, hype, or invented facts.
- If uncertain: mark " (reporting)" or "unconfirmed".
- Total ≤ ~300 words.

Input news:
{full_input}
"""

    messages = [{"role": "user", "content": prompt}]

    # ────────────────────────────────────────────────
    # 1. Try OpenAI first (best format consistency)
    # ────────────────────────────────────────────────
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = openai_client.chat.completions.create(
                model=DEFAULT_OPENAI_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=900,
                # response_format={"type": "text"},  # can switch to "json_object" later
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI attempt {attempt+1} failed: {repr(e)}")
            traceback.print_exc()
            if attempt < max_attempts - 1:
                time.sleep(2 ** attempt * 1.5)  # backoff
            continue

    # ────────────────────────────────────────────────
    # 2. Fallback: Grok (xAI)
    # ────────────────────────────────────────────────
    if grok_client.api_key:
        try:
            response = grok_client.chat.completions.create(
                model=GROK_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=900,
                # reasoning_effort="medium",  # optional: low/medium/high/none (Grok 4+)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Grok failed: {repr(e)}")
            traceback.print_exc()

    # ────────────────────────────────────────────────
    # 3. Fallback: Gemini (native SDK)
    # ────────────────────────────────────────────────
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel(GEMINI_MODEL)
            gemini_response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=900,
                )
            )
            return gemini_response.text.strip()
        except Exception as e:
            print(f"Gemini failed: {repr(e)}")
            traceback.print_exc()

    # ────────────────────────────────────────────────
    # Final raw fallback
    # ────────────────────────────────────────────────
    print("All LLM providers failed → returning raw concatenated news")
    return (
        "MARKET NEWS:\n" + (market_text or "No market news") + "\n\n"
        "POLITICAL NEWS:\n" + (political_text or "No political news")
    )