"""
agent_optimizer.py — AGENT 3: The Optimizer.
Polishes the draft: picks a scroll-stopping subject line, builds clean HTML,
and tags the issue for SEO/segmentation.
"""
import config
from llm import ask_llm_json
from prompts import BRAND_VOICE, OPTIMIZER_PROMPT


def run(draft_markdown: str) -> dict:
    """Agent entrypoint. Returns {subject_line, preview_text, html_body, tags}."""
    print("✨ [Optimizer] Polishing + packaging...")
    prompt = BRAND_VOICE + "\n\n" + OPTIMIZER_PROMPT
    result = ask_llm_json(prompt, context=draft_markdown)

    # Hard-cap the subject line & preview to email-client limits
    result["subject_line"] = result.get("subject_line", "")[:50]
    result["preview_text"] = result.get("preview_text", "")[:90]
    print(f"  ✅ Subject: \"{result['subject_line']}\"")
    return result
