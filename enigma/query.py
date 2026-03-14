"""Life Query (FR-3.3): RAG over Nexus + Open Commitments, LLM answer."""
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from enigma.config import OPENAI_API_KEY
from enigma.history_store import append_query_history
from enigma.notion_client import (
    get_nexus_since,
    get_open_commitments,
    get_recent_nuggets,
    get_recent_grandmas_closet,
    _get_prop,
)

logger = logging.getLogger(__name__)


def _openai_client():
    from openai import OpenAI
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        raise ValueError("OPENAI_API_KEY is required for Life Query. Set it in .env")
    return OpenAI(api_key=OPENAI_API_KEY.strip())


def _since_iso(hours: int = 168) -> str:
    """Default 168 = 7 days of Nexus context for RAG."""
    t = datetime.now(timezone.utc) - timedelta(hours=hours)
    return t.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _build_rag_context(
    commitments: list,
    nexus_pages: list,
    grandmas_closet: list,
    max_chars: int = 12000,
) -> str:
    """Build a single text blob for the LLM from commitments, Nexus, and Grandma's Closet (Epic 6)."""
    lines = []
    lines.append("=== OPEN COMMITMENTS ===")
    for p in commitments:
        ctx = _get_prop(p, "Context")
        content = _get_prop(p, "Content")
        tag = _get_prop(p, "Sovereign Tag")
        lines.append(f"- [{tag}] {ctx}: {content}")
    if not commitments:
        lines.append("(none)")
    lines.append("")
    lines.append("=== NEXUS (RECENT ACTIVITY — notes, transient, decisions, etc.) ===")
    for p in nexus_pages:
        ctx = _get_prop(p, "Context")
        content = _get_prop(p, "Content")
        tag = _get_prop(p, "Sovereign Tag")
        lines.append(f"- [{tag}] {ctx}: {content}")
    if not nexus_pages:
        lines.append("(none)")
    lines.append("")
    lines.append("=== GRANDMA'S CLOSET (DEFERRED IDEAS) ===")
    for p in grandmas_closet:
        ctx = _get_prop(p, "Context")
        content = _get_prop(p, "Content")
        lines.append(f"- {ctx}: {content}")
    if not grandmas_closet:
        lines.append("(none)")
    text = "\n".join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... (truncated)"
    return text


def run_life_query(
    question: str,
    context_hours: int = 168,
    brief_context: Optional[str] = None,
    source: str = "text",
) -> str:
    """
    Answer the user's question using RAG over Nexus + Open Commitments.
    context_hours: how many hours of Nexus to include (default 7 days).
    brief_context: optional Sovereign Brief text for follow-up questions (FR-3.4).
    Returns the LLM answer string.
    """
    question = (question or "").strip()
    if not question:
        return "Please ask a question."
    logger.info("Life Query running question_len=%s brief_context=%s", len(question), bool(brief_context))
    commitments = get_open_commitments()
    grandmas_closet = get_recent_grandmas_closet(limit=80)
    since = _since_iso(hours=context_hours)
    try:
        nexus_pages = get_nexus_since(since)
    except Exception:
        nexus_pages = get_recent_nuggets(limit=80)
    context_text = _build_rag_context(commitments, nexus_pages, grandmas_closet)
    if brief_context and (brief_context := brief_context.strip()):
        context_text = (
            "=== SOVEREIGN BRIEF (for follow-up questions) ===\n"
            + brief_context
            + "\n\n=== NEXUS & COMMITMENTS ===\n"
            + context_text
        )
    client = _openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Life Query: you answer the user's question using ONLY the context below "
                    "from their personal Nexus (commitments, notes, recent activity, Omni-Scribe). "
                    "When Sovereign Brief context is present, treat follow-up questions as referring to that brief. "
                    "Be concise and direct. If the context does not contain enough information to answer, "
                    "say so clearly. Do not invent or assume facts. Quote or reference the context when relevant."
                ),
            },
            {"role": "user", "content": "Context:\n" + context_text + "\n\n---\n\nQuestion: " + question},
        ],
        max_tokens=500,
    )
    answer = (response.choices[0].message.content or "").strip()
    append_query_history(
        question=question,
        answer=answer,
        brief_context_used=bool(brief_context and brief_context.strip()),
        source=source,
    )
    return answer
