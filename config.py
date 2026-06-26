"""
config.py — Central config for the AI Newsletter Empire.
Loads everything from environment / .env file.
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


# --- Core credentials ---
GROQ_API_KEY = _get("GROQ_API_KEY")
# Gemini kept as optional fallback (not used by default)
GEMINI_API_KEY = _get("GEMINI_API_KEY", "")

# --- Email Provider ---
BEEHIIV_API_KEY = _get("BEEHIIV_API_KEY")
BEEHIIV_PUBLICATION_ID = _get("BEEHIIV_PUBLICATION_ID")

# --- Branding ---
NEWSLETTER_NAME = _get("NEWSLETTER_NAME", "The AI Hustle")
NEWSLETTER_TAGLINE = _get("NEWSLETTER_TAGLINE", "AI tools & money moves.")
TARGET_AUDIENCE = _get("TARGET_AUDIENCE", "people building income with AI")

# --- Output ---
POSTS_DIR = _get("WEBSITE_POSTS_DIR", "./posts")

# --- Affiliate links (parsed from JSON string in .env) ---
_aff_raw = _get("AFFILIATE_LINKS", "{}")
try:
    AFFILIATE_LINKS = json.loads(_aff_raw)
except json.JSONDecodeError:
    AFFILIATE_LINKS = {}

# --- Safety check ---
if not GROQ_API_KEY:
    print("⚠️  WARNING: GROQ_API_KEY is not set. Add it to .env")
