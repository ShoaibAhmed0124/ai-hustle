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

# --- Email: Resend (our own system, no Beehiiv) ---
RESEND_API_KEY = _get("RESEND_API_KEY")
# Use a verified sender. Free Resend accounts use onboarding@resend.dev
# Once you verify your domain, set this to newsletter@theaihustle.com
RESEND_FROM = _get("RESEND_FROM", "The AI Hustle <onboarding@resend.dev>")

# --- Public URLs ---
LANDING_URL = _get("LANDING_URL", "https://theaihustle.surge.sh")
BACKEND_URL = _get("BACKEND_URL", "")  # set after deploying server.py

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

# --- Safety checks ---
if not GROQ_API_KEY:
    print("⚠️  WARNING: GROQ_API_KEY is not set. Add it to .env")
if not RESEND_API_KEY:
    print("ℹ️  NOTE: RESEND_API_KEY not set yet. Emails will be skipped until configured.")
