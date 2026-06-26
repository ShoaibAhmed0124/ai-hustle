"""
llm.py — Groq client wrapper. One function: ask_llm().
All agents call this instead of dealing with the SDK directly.

Uses Groq (LLaMA 3.3 70B) — free, fast, reliable free tier.
"""
import json
import re
import time

from groq import Groq

import config

# Build the client once
_client = Groq(api_key=config.GROQ_API_KEY)

# LLaMA 3.3 70B — fast, smart, great on the free tier.
_MODEL = "llama-3.3-70b-versatile"


def _call_with_retry(model, prompt, temperature):
    """Call Groq, retrying on 429 (rate limit) with exponential backoff."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = _client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            retriable = "429" in str(e) or "503" in str(e) or "rate" in str(e).lower()
            if not retriable or attempt == max_retries - 1:
                raise
            wait = 2 ** (attempt + 1)  # 2, 4, 8, 16, 32 seconds
            print(f"  ⏳ Rate limited (attempt {attempt + 1}/{max_retries}). "
                  f"Waiting {wait}s...")
            time.sleep(wait)
    return ""


def ask_llm(prompt: str, context: str = "", temperature: float = 0.8) -> str:
    """Send prompt + context, return the raw text response."""
    full = f"{prompt}\n\n--- CONTEXT ---\n{context}" if context else prompt
    return _call_with_retry(_MODEL, full, temperature)


def ask_llm_json(prompt: str, context: str = "") -> dict:
    """Like ask_llm but parses JSON from the response (robust to code fences)."""
    raw = ask_llm(prompt, context, temperature=0.4)
    # Strip markdown code fences if the model added them
    raw = re.sub(r"^```(?:json)?\s*", "", raw).strip()
    raw = re.sub(r"\s*```$", "", raw).strip()
    return json.loads(raw)
