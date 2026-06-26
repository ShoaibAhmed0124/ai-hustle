"""
agent_researcher.py — AGENT 1: The Researcher.
Gathers raw AI news from free sources, then asks Gemini to extract
the 3-5 freshest, most actionable topics.

Sources (all free, no API keys):
  - RSS feeds (news sites)
  - Hacker News Algolia API (always works, no auth, no 403)
"""
import json
from datetime import datetime, timezone

import feedparser
import requests

from llm import ask_llm_json
from prompts import RESEARCHER_PROMPT

# A real browser UA so feeds don't block us.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# --- Free news sources (RSS = no API key, no rate-limit headaches) ---
RSS_FEEDS = [
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://news.google.com/rss/search?q=AI+tools+OR+AI+side+hustle&hl=en-US&gl=US&ceid=US:en",
]


def _fetch_rss() -> list[str]:
    """Pull recent items from all RSS feeds as plain text chunks."""
    items = []
    for url in RSS_FEEDS:
        # feedparser doesn't use our headers, so try requests first for HTML feeds.
        try:
            r = requests.get(url, headers=_HEADERS, timeout=15)
            feed = feedparser.parse(r.content)
        except Exception:
            feed = feedparser.parse(url)
        for entry in feed.entries[:8]:  # last 8 per feed is plenty
            items.append(
                f"[{entry.get('title', 'untitled')}] {entry.get('summary', '')[:300]}"
            )
    return items


def _fetch_hackernews() -> list[str]:
    """Pull top recent AI stories from Hacker News via the free Algolia API."""
    items = []
    url = (
        "https://hn.algolia.com/api/v1/search_by_date"
        "?tags=story&query=AI+OR+GPT+OR+LLM+OR+agent&hitsPerPage=15"
    )
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        for hit in r.json().get("hits", []):
            title = hit.get("title") or hit.get("story_title") or "untitled"
            points = hit.get("points") or 0
            items.append(f"[Hacker News, {points} pts] {title}")
    except Exception as e:
        print(f"  ⚠️ Hacker News fetch failed: {e}")
    return items


def run() -> dict:
    """Agent entrypoint. Returns {topics: [...], date: ...}."""
    print("🔍 [Researcher] Gathering raw intel...")
    raw = _fetch_rss() + _fetch_hackernews()
    print(f"  → {len(raw)} raw items found.")

    blob = "\n\n".join(raw)
    result = ask_llm_json(RESEARCHER_PROMPT, context=blob)

    # Stamp with today's date for reference
    result["date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"  ✅ {len(result.get('topics', []))} topics extracted.")
    return result
