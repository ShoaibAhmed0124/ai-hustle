"""
agent_writer.py — AGENT 2: The Writer.
Takes the research and drafts the actual newsletter (markdown).
"""
import config
from llm import ask_llm
from prompts import BRAND_VOICE, WRITER_PROMPT
import json


def run(research: dict) -> str:
    """Agent entrypoint. research = output of agent_researcher. Returns markdown."""
    print("✍️ [Writer] Drafting the newsletter...")
    context = (
        f"Date: {research.get('date','today')}\n"
        f"Research JSON:\n{json.dumps(research, indent=2)}\n\n"
        f"Affiliate links you may weave in naturally (only if relevant, max 2):\n"
        f"{json.dumps(config.AFFILIATE_LINKS, indent=2)}"
    )
    prompt = BRAND_VOICE + "\n\n" + WRITER_PROMPT
    draft = ask_llm(prompt, context=context)
    print("  ✅ Draft complete.")
    return draft
