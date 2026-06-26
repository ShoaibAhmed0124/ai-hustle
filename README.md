# ⚡ The AI Hustle — Autonomous Newsletter Empire

A fully automated AI newsletter. **4 AI agents** research → write → optimize → publish every day, hands-off.

**Total cost: $0.** Runs on free tiers of Gemini, Beehiiv, and GitHub Actions.

---

## 🏗️ How It Works

```
Researcher → Writer → Optimizer → Publisher
 (find news)  (draft it)  (polish+HTML)  (email+web)
```

| File | Role |
|------|------|
| `run.py` | **Orchestrator.** Chains all 4 agents. Run this. |
| `agent_researcher.py` | Scrapes RSS + Reddit, Gemini extracts top topics |
| `agent_writer.py` | Gemini drafts the newsletter in markdown |
| `agent_optimizer.py` | Gemini picks subject line, builds HTML, tags |
| `agent_publisher.py` | Saves locally + creates Beehiiv draft + web post |
| `llm.py` | Gemini client helper |
| `prompts.py` | All the agent prompts (tweak voice here) |
| `config.py` | Loads settings from `.env` |
| `.github/workflows/daily-newsletter.yml` | **Auto-runs daily for FREE** |
| `website/index.html` | Your landing page (free host on Netlify) |

---

## 🚀 Setup — 30 minutes, do it now

### Step 1: Get your FREE API keys

1. **Gemini API key** (the AI brain — FREE):
   - Go to https://aistudio.google.com/app/apikey
   - Click "Create API key" → copy it

2. **Beehiiv account** (sends emails — FREE up to 2500 subs):
   - Go to https://www.beehiiv.com → create a publication (name it "The AI Hustle" or your brand)
   - Settings → API → generate a key
   - Copy the **publication ID** from the URL of your dashboard

### Step 2: Configure

```bash
# In the project folder:
cp .env.example .env
```
Open `.env` and paste your keys.

### Step 3: Install + test locally

```bash
pip install -r requirements.txt
python run.py            # dry run — builds issue, prints it
python run.py --publish  # also sends a draft to Beehiiv
```

You'll see the full newsletter printed in your terminal. 🎉

### Step 4: Deploy the website (free)

1. Go to https://app.netlify.com/drop
2. Drag the `website/` folder onto the page
3. Done — your landing page is live with a URL like `https://quirky-xyz.netlify.app`
4. In Beehiiv, get your embeddable signup form URL, paste it into `index.html` where it says `REPLACE_WITH_YOUR_BEEHIIV_FORM_URL`

### Step 5: Automate it forever (free)

1. Create a **public** repo on GitHub (e.g. `ai-hustle`)
2. Upload all files from `ai-newsletter/`
3. In the repo: **Settings → Secrets and variables → Actions → New secret**. Add:
   - `GEMINI_API_KEY`
   - `BEEHIIV_API_KEY`
   - `BEEHIIV_PUBLICATION_ID`
4. Go to the **Actions** tab → enable the workflow
5. Now it runs **every day at 6 AM UTC automatically.** 🤖

> To change the time, edit the `cron:` line in `.github/workflows/daily-newsletter.yml`.

---

## 💰 How It Makes Money

1. **Sponsorships** — at 5K+ subscribers, charge $200–$500 per email. Agents write it, you forward to a sponsor.
2. **Affiliate links** — add links in `.env` under `AFFILIATE_LINKS`. Agents weave them in.
3. **Ads** — get AdSense approved (after traffic), put ad code in `website/index.html`.
4. **Premium tier** — Beehiiv lets you add a paid tier ($5–$10/mo).

---

## 🧠 Tweaking the Voice

Open `prompts.py`. The `BRAND_VOICE` block controls how it sounds. Make it more you.

To change the niche/topic focus, edit the source lists in `agent_researcher.py` (`RSS_FEEDS`, `REDDIT_SUBS`).

---

## ⚠️ Honest Truth

- **Month 1:** You build the list. No income. This is normal.
- **Month 2–3:** Traffic from social/SEO. First sponsor interest.
- **Month 6+:** The compounding kicks in. Audience is your moat.

The agents do the daily work. Your only job: **grow the audience** (post on X, Reddit, TikTok that you run an AI-written newsletter — that itself is a hook).

---

Built to run while you sleep. Now go deploy it. 💪
