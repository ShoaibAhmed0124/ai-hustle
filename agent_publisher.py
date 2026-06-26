"""
agent_publisher.py — AGENT 4: The Publisher.
- Always: saves the issue as local files (HTML you can open + JSON backup).
- If WEBSITE_POSTS_DIR is set: writes a dated .md file there too.
- If Resend is configured: emails all active subscribers directly.
  (Our OWN system — no Beehiiv, no third-party branding.)
"""
import json
import os
from datetime import datetime, timezone

import config

# Simple inline CSS so the saved HTML looks good when opened in a browser.
_STYLE = """
body{font-family:-apple-system,Segoe UI,sans-serif;background:#0a0a0a;color:#f5f5f5;
     max-width:640px;margin:0 auto;padding:40px 20px;line-height:1.7}
h1{font-size:28px;line-height:1.2}
h2{color:#00ff88;font-size:20px;margin-top:28px}
a{color:#00ff88}
.meta{color:#888;font-size:13px;margin-bottom:24px;border-bottom:1px solid #222;padding-bottom:16px}
pre{white-space:pre-wrap;font-family:inherit}
"""


def _wrap_html(package: dict) -> str:
    """Wrap the generated HTML body in a full viewable HTML document."""
    body = package.get("html_body") or f"<pre>{package.get('draft_markdown','')}</pre>"
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{package.get('subject_line','Newsletter')}</title>"
        f"<style>{_STYLE}</style></head><body>"
        f"<div class='meta'>{config.NEWSLETTER_NAME} · {package.get('date','')}</div>"
        f"{body}"
        "</body></html>"
    )


def _save_local(package: dict) -> str:
    """Always save a viewable HTML + a JSON backup. Returns the HTML path."""
    os.makedirs("archive", exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    json_path = os.path.join("archive", f"issue-{stamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=2, ensure_ascii=False)

    html_path = os.path.join("archive", f"issue-{stamp}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(_wrap_html(package))

    print(f"  💾 Saved viewable HTML → {os.path.abspath(html_path)}")
    return html_path


def _save_to_website(package: dict) -> None:
    """If a posts dir is configured, drop a markdown file there for static site."""
    if not config.POSTS_DIR:
        return
    os.makedirs(config.POSTS_DIR, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = os.path.join(config.POSTS_DIR, f"{stamp}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"---\n")
        f.write(f"title: \"{package['subject_line']}\"\n")
        f.write(f"date: {stamp}\n")
        f.write(f"tags: [{', '.join(package.get('tags', []))}]\n")
        f.write(f"---\n\n")
        f.write(package["draft_markdown"])
    print(f"  🌐 Wrote website post → {path}")


def _email_subscribers(package: dict) -> None:
    """Send the issue to every active subscriber via Resend (our own system)."""
    # Import lazily so local dry-runs don't require Resend to be set up.
    try:
        import email_sender
        import subscribers
    except Exception as e:
        print(f"  ⚠️ Could not load email/subscriber modules: {e}")
        return

    active = subscribers.get_active()
    if not active:
        print("  ℹ️  No active subscribers yet — skipping email send.")
        return

    emails = [s["email"] for s in active]
    print(f"  📧 Sending to {len(emails)} subscriber(s)...")

    # Resend free tier = 100 emails/day. Batch in chunks of 100.
    BATCH = 100
    sent_ok = 0
    for i in range(0, len(emails), BATCH):
        batch = emails[i:i + BATCH]
        result = email_sender.send_newsletter(
            to_emails=batch,
            subject=package["subject_line"],
            body_html=package.get("html_body") or "",
            preview=package.get("preview_text", ""),
        )
        if result.get("status") == "sent":
            sent_ok += len(batch)
        elif result.get("status") == "skipped":
            print("  ℹ️  Resend not configured — saved issue locally but did not email.")
            return

    print(f"  ✅ Emailed {sent_ok} subscriber(s).")


def run(package: dict) -> None:
    """Agent entrypoint. package = full merged dict of all prior outputs."""
    print("📤 [Publisher] Shipping the issue...")
    _save_local(package)
    _save_to_website(package)
    _email_subscribers(package)
    print("  ✅ Done.")
