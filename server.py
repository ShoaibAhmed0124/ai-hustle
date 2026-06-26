"""
server.py — Backend API for subscriptions.

Handles:
  POST /subscribe          → add subscriber
  GET  /unsubscribe?token= → remove subscriber
  GET  /stats              → subscriber count (for admin dashboard)
  GET  /list               → list subscribers (for admin)

Deploy this free on Render.com (or Railway / Fly.io).
The landing page form posts here.
"""
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import config
import subscribers

app = Flask(__name__)
# Allow the landing page (surge.sh) to call this API from the browser
CORS(app, origins=[config.LANDING_URL, "http://localhost:5500", "http://127.0.0.1:5500"])


@app.post("/subscribe")
def subscribe_route():
    """Add a subscriber. Called by the landing page form."""
    data = request.get_json(silent=True) or request.form.to_dict()
    email = (data.get("email") or "").strip()
    if not email:
        return jsonify({"ok": False, "message": "Email is required."}), 400
    result = subscribers.add(email)
    status_code = 200 if result["status"] != "error" else 400
    return jsonify({"ok": True, **result}), status_code


@app.get("/unsubscribe")
def unsubscribe_route():
    """Unsubscribe via token. ?token=xxx  (link in every email)."""
    token = request.args.get("token", "")
    result = subscribers.unsubscribe(token)
    # Redirect to a friendly page after unsubscribing
    return redirect(f"{config.LANDING_URL}/unsubscribed.html?status={result['status']}", code=302)


@app.get("/stats")
def stats_route():
    """Public-ish stats for the admin dashboard."""
    return jsonify({"ok": True, **subscribers.stats()})


@app.get("/")
def health():
    return jsonify({"ok": True, "service": config.NEWSLETTER_NAME, "subs": subscribers.count()})


if __name__ == "__main__":
    # Render sets PORT env var
    port = int(__import__("os").getenv("PORT", 5000))
    print(f"🚀 {config.NEWSLETTER_NAME} backend running on port {port}")
    app.run(host="0.0.0.0", port=port)
