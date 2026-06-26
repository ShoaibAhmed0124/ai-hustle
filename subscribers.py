"""
subscribers.py — Custom subscriber database.

No Beehiiv. No third-party. Our own system.
Stores subscribers in a JSON file. Handles subscribe, unsubscribe, list.

Scale path:
  - 0-5K subs:   JSON file (this file) ← FREE
  - 5K-50K subs: SQLite              ← FREE
  - 50K+ subs:    Supabase / Postgres  ← FREE tier
"""

import json
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

_SUBS_FILE = Path("data/subscribers.json")

# Disposable / spammy email domains we reject outright.
_BLOCKED_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "10minutemail.com", "tempmail.com",
    "temp-mail.org", "throwaway.email", "trashmail.com", "yopmail.com",
    "getnada.com", "maildrop.cc", "sharklasers.com", "dispostable.com",
    "fakeinbox.com", "spam4.me", "mohmal.com", "emailondeck.com",
}
# Basic valid email pattern
_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")


def _is_valid_email(email: str) -> bool:
    """Server-side check: valid format + not a known disposable domain."""
    email = email.strip().lower()
    if not _EMAIL_RE.match(email):
        return False
    domain = email.split("@")[-1]
    if domain in _BLOCKED_DOMAINS:
        return False
    return True


def _load() -> dict:
    """Load the subscriber database. Creates empty if missing."""
    _SUBS_FILE.parent.mkdir(exist_ok=True)
    if _SUBS_FILE.exists():
        with open(_SUBS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"subscribers": []}


def _save(db: dict) -> None:
    _SUBS_FILE.parent.mkdir(exist_ok=True)
    with open(_SUBS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def add(email: str) -> dict:
    """Subscribe an email. Returns {status, message}."""
    email = email.strip().lower()

    # Server-side spam protection
    if not _is_valid_email(email):
        return {"status": "error", "message": "Please use a valid email address."}

    db = _load()

    # Already subscribed?
    for sub in db["subscribers"]:
        if sub["email"] == email and sub["active"]:
            return {"status": "exists", "message": "Already subscribed! ✅"}

        # Re-subscribe if previously unsubscribed
        if sub["email"] == email and not sub["active"]:
            sub["active"] = True
            sub["unsubscribed_at"] = None
            _save(db)
            return {"status": "reactivated", "message": "Welcome back! 🎉"}

    db["subscribers"].append({
        "email": email,
        "token": secrets.token_urlsafe(32),  # for unsubscribe link
        "subscribed_at": datetime.now(timezone.utc).isoformat(),
        "active": True,
        "unsubscribed_at": None,
    })
    _save(db)
    return {"status": "subscribed", "message": "You're in! 🎉"}


def unsubscribe(token: str) -> dict:
    """Unsubscribe using the unique token."""
    db = _load()
    for sub in db["subscribers"]:
        if sub["token"] == token:
            sub["active"] = False
            sub["unsubscribed_at"] = datetime.now(timezone.utc).isoformat()
            _save(db)
            return {"status": "unsubscribed", "message": "Done. You won't hear from us again."}
    return {"status": "error", "message": "Token not found."}


def get_active() -> list[dict]:
    """Return list of active subscriber dicts."""
    db = _load()
    return [s for s in db["subscribers"] if s["active"]]


def count() -> int:
    """Return count of active subscribers."""
    return len(get_active())


def stats() -> dict:
    """Return subscriber statistics."""
    db = _load()
    active = [s for s in db["subscribers"] if s["active"]]
    total = len(db["subscribers"])
    return {
        "active": len(active),
        "total": total,
        "unsubscribed": total - len(active),
    }
