"""Epic 5 FR-5.3: LLM stitching job — themes, links, suggested actions from Thought Memory.
Run manually or via CRON (e.g. weekly): python -m enigma.thought_stitch
Outputs a short summary to stdout; can be extended to store in Nexus or send via Brief."""
import logging
from typing import Optional

from enigma.config import OPENAI_API_KEY, configure_logging
from enigma.notion_client import get_recent_thoughts, _get_prop

configure_logging()
logger = logging.getLogger(__name__)


def _build_thoughts_text(thoughts: list, max_chars: int = 8000) -> str:
    lines = []
    for p in thoughts:
        content = _get_prop(p, "Content")
        if content:
            lines.append(content)
    text = "\n---\n".join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... (truncated)"
    return text


def run_stitch(limit: int = 50) -> Optional[str]:
    """
    Fetch recent thoughts, run LLM to find themes and suggested actions.
    Returns summary string or None on failure.
    """
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        logger.warning("OPENAI_API_KEY not set; skipping thought stitch")
        return None
    try:
        thoughts = get_recent_thoughts(limit=limit)
    except Exception as e:
        logger.exception("get_recent_thoughts failed: %s", e)
        return None
    if not thoughts:
        return "No thoughts in Thought Memory yet."
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY.strip())
    context = _build_thoughts_text(thoughts)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are analyzing a person's Thought Memory (reflective notes, not commitments). "
                    "Identify 1) recurring themes, 2) possible links between thoughts, 3) 1–3 suggested actions or follow-ups. "
                    "Keep the output under 200 words. Be concise and actionable."
                ),
            },
            {"role": "user", "content": "Thoughts:\n" + context},
        ],
        max_tokens=300,
    )
    out = (response.choices[0].message.content or "").strip()
    return out or None


if __name__ == "__main__":
    summary = run_stitch()
    if summary:
        print("Thought Stitch (themes & suggestions):")
        print(summary)
    else:
        print("Thought stitch produced no output.")
