"""
email_sender.py — Sends emails via Resend API.
Professional branded HTML emails, dark theme, no "Powered by" nothing.

Resend: https://resend.com (free: 100 emails/day = 3,000/month)
Scale:   Resend Pro ($20/mo) at 10K+ subs → self-funded by sponsors.
"""
import requests

import config


_SEND_URL = "https://api.resend.com/emails"


def _brand_html(subject: str, body_html: str, preview: str = "") -> str:
    """Wrap newsletter content in our premium branded template."""
    unsubscribe_url = "https://theaihustle.surge.sh/unsubscribe.html"
    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
  body{{margin:0;padding:0;background:#060608;font-family:-apple-system,Segoe UI,sans-serif;color:#f4f4f6}}
  .wrap{{max-width:600px;margin:0 auto;padding:40px 24px}}
  .logo{{font-size:14px;letter-spacing:3px;color:#00ff9d;text-transform:uppercase;font-weight:700;margin-bottom:32px}}
  h1{{font-size:26px;margin-bottom:8px}}
  .meta{{color:#8a8a96;font-size:13px;margin-bottom:28px;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:16px}}
  .content{{font-size:15px;line-height:1.7;color:#c8c8d4}}
  .content h2{{color:#00ff9d;font-size:18px;margin-top:24px}}
  .content p{{margin-bottom:14px}}
  .cta{{display:inline-block;padding:12px 24px;border-radius:10px;background:#00ff9d;color:#000;font-weight:600;margin-top:20px;text-decoration:none}}
  .footer{{margin-top:40px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.08);font-size:12px;color:#555}}
  .footer a{{color:#00ff9d;text-decoration:none}}
</style></head>
<body>
<div class="wrap">
  <div class="logo">⚡ {config.NEWSLETTER_NAME}</div>
  {body_html}
  <div class="footer">
    You received this because you subscribed to <a href="https://theaihustle.surge.sh">{config.NEWSLETTER_NAME}</a>.<br>
    <a href="{unsubscribe_url}">Unsubscribe</a> · <a href="https://theaihustle.surge.sh">Website</a>
  </div>
</div>
</body>
</html>"""


def send_newsletter(to_emails: list[str], subject: str, body_html: str, preview: str = "") -> dict:
    """Send newsletter to a list of emails via Resend."""
    if not config.RESEND_API_KEY:
        print("  ℹ️  Resend not configured — skipping email send.")
        return {"status": "skipped"}

    full_html = _brand_html(subject, body_html, preview)

    # Resend supports batch send via array (free tier: 100/day)
    payload = {
        "from": config.RESEND_FROM,
        "to": to_emails,
        "subject": subject,
        "html": full_html,
    }

    headers = {
        "Authorization": f"Bearer {config.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(_SEND_URL, json=payload, headers=headers, timeout=30)
        if r.ok:
            data = r.json()
            print(f"  📧 Sent to {len(to_emails)} subscriber(s). ID: {data.get('id','?')}")
            return {"status": "sent", "id": data.get("id")}
        else:
            print(f"  ⚠️ Resend error {r.status_code}: {r.text[:200]}")
            return {"status": "error", "code": r.status_code}
    except Exception as e:
        print(f"  ⚠️ Resend request failed: {e}")
        return {"status": "error", "message": str(e)}


def send_single(to: str, subject: str, body_html: str) -> dict:
    """Send a single email (for welcome, confirmations etc)."""
    return send_newsletter([to], subject, body_html)
