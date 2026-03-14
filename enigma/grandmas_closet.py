"""Epic 6: Grandma's Closet helpers (deferred ideas, digest)."""
from datetime import datetime, timezone, timedelta
from typing import Dict, List

from enigma.notion_client import get_recent_grandmas_closet, _get_prop
from enigma.orchestrator import push_to_nexus

SOVEREIGN_TAG_GRANDMAS_CLOSET = "grandmas-closet"
CONTEXT_GRANDMAS_CLOSET = "Grandma's Closet"


def save_to_grandmas_closet(content: str, context: str = "") -> dict:
    """Persist deferred idea into Nexus with grandmas-closet tag."""
    text = (content or "").strip()
    if not text:
        raise ValueError("Content is required to save into Grandma's Closet.")
    ctx = (context or "").strip() or CONTEXT_GRANDMAS_CLOSET
    page = push_to_nexus(
        context=ctx[:120],
        content=text,
        priority="low",
        tag=SOVEREIGN_TAG_GRANDMAS_CLOSET,
    )
    return {
        "id": page.get("id"),
        "context": ctx,
        "content": text,
        "tag": SOVEREIGN_TAG_GRANDMAS_CLOSET,
    }


def list_grandmas_closet(limit: int = 100) -> List[Dict[str, str]]:
    """Return recent grandmas-closet entries in API-friendly shape."""
    pages = get_recent_grandmas_closet(limit=limit)
    out: List[Dict[str, str]] = []
    for p in pages:
        out.append(
            {
                "id": p.get("id"),
                "context": _get_prop(p, "Context"),
                "content": _get_prop(p, "Content"),
                "tag": _get_prop(p, "Sovereign Tag"),
                "last_updated": _get_prop(p, "Last Updated"),
            }
        )
    return out


def weekly_closet_digest(days: int = 7) -> Dict[str, object]:
    """Build a simple weekly digest from saved deferred ideas."""
    items = list_grandmas_closet(limit=300)
    threshold = datetime.now(timezone.utc) - timedelta(days=max(1, days))
    recent = []
    for item in items:
        d = (item.get("last_updated") or "").strip()
        if not d:
            continue
        try:
            dt = datetime.fromisoformat(d.replace("Z", "+00:00"))
            if dt >= threshold:
                recent.append(item)
        except Exception:
            continue

    promoted = []
    for item in recent[:5]:
        txt = (item.get("content") or "").strip()
        if txt:
            promoted.append(f"- Consider promoting: {txt[:120]}")

    lines = [
        f"Grandma's Closet weekly digest ({len(recent)} ideas in last {max(1, days)} days)",
    ]
    if not recent:
        lines.append("- No deferred ideas added this week.")
    else:
        lines.append("- Highlights:")
        for item in recent[:10]:
            lines.append(f"  - {item.get('content', '')[:140]}")
    if promoted:
        lines.append("- Promote to action:")
        lines.extend(promoted)

    return {
        "count": len(recent),
        "items": recent,
        "digest": "\n".join(lines),
    }

