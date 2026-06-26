"""
run.py — THE ORCHESTRATOR.
Chains all 4 agents in order. This is the single entrypoint.

    python run.py            → generates today's issue (dry-run safe)
    python run.py --publish  → also pushes to Beehiiv

Think of this file as the factory floor manager.
"""
import sys

import agent_optimizer
import agent_publisher
import agent_researcher
import agent_writer


def build_issue(publish: bool = False) -> dict:
    """Run the full pipeline. Returns the final package dict."""
    print("=" * 55)
    print("🏭  AI NEWSLETTER EMPIRE — daily run starting")
    print("=" * 55)

    # 1. Research
    research = agent_researcher.run()

    # 2. Write
    draft_markdown = agent_writer.run(research)

    # 3. Optimize
    optimized = agent_optimizer.run(draft_markdown)

    # 4. Package everything together
    package = {
        **research,  # date, topics
        "draft_markdown": draft_markdown,
        **optimized,   # subject_line, preview_text, html_body, tags
    }

    # 5. Publish (saves locally always; sends only if --publish)
    if publish:
        agent_publisher.run(package)
    else:
        print("\n📝 Dry run. Issue built & previewed above.")
        print("   Add --publish to send to Beehiiv. Saved nothing.")

    print("\n" + "=" * 55)
    print("✅  PIPELINE COMPLETE")
    print("=" * 55)
    return package


if __name__ == "__main__":
    should_publish = "--publish" in sys.argv
    build_issue(publish=should_publish)
