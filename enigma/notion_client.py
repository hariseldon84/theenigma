"""Notion client for The Nexus — Knowledge Nuggets, Open Commitments, Transient Memory."""
from datetime import datetime, timezone
from typing import Optional

from notion_client import Client
from notion_client.helpers import collect_paginated_api

from enigma.config import NOTION_API_KEY, NOTION_NEXUS_DATABASE_ID


def get_client() -> Client:
    if not NOTION_API_KEY:
        raise ValueError("NOTION_API_KEY is required. Set it in .env")
    return Client(auth=NOTION_API_KEY)


def _get_data_source_id(database_id: str) -> str:
    """Get the first data source ID from a database (Notion API 2025-09-03+)."""
    client = get_client()
    db = client.databases.retrieve(database_id)
    data_sources = db.get("data_sources", []) if isinstance(db, dict) else getattr(db, "data_sources", []) or []
    if not data_sources:
        raise ValueError(
            f"Database {database_id} has no data sources. "
            "Ensure the database is shared with your integration."
        )
    return data_sources[0]["id"]


def query_nexus(
    database_id: Optional[str] = None,
    filter_obj: Optional[dict] = None,
    sorts: Optional[list] = None,
) -> list:
    """Query The Nexus database. Returns list of pages."""
    db_id = database_id or NOTION_NEXUS_DATABASE_ID
    if not db_id:
        raise ValueError("NOTION_NEXUS_DATABASE_ID is required. Set it in .env")

    client = get_client()
    data_source_id = _get_data_source_id(db_id)
    return collect_paginated_api(
        client.data_sources.query,
        data_source_id=data_source_id,
        filter=filter_obj,
        sorts=sorts,
    )


def _now_iso() -> str:
    """Current UTC time in Notion-friendly ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _rt(content: str, chunk_size: int = 1800) -> list:
    """Convert long text into Notion rich_text chunks (<= 2000 chars each)."""
    text = (content or "").strip()
    if not text:
        return []
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return [{"text": {"content": c}} for c in chunks]


def create_nugget(
    context: str,
    content: str,
    priority: str = "medium",
    sovereign_tag: str = "",
    database_id: Optional[str] = None,
) -> dict:
    """Create a Knowledge Nugget in The Nexus. Sets Last Updated to current UTC time."""
    db_id = database_id or NOTION_NEXUS_DATABASE_ID
    if not db_id:
        raise ValueError("NOTION_NEXUS_DATABASE_ID is required")

    client = get_client()
    properties = {
        "Context": {"title": [{"text": {"content": context[:2000]}}]},
        "Priority": {"select": {"name": priority}},
        "Sovereign Tag": {"rich_text": _rt(sovereign_tag[:2000])}
        if sovereign_tag
        else {"rich_text": []},
        "Content": {"rich_text": _rt(content)},
        "Last Updated": {"date": {"start": _now_iso(), "end": None}},
    }
    return client.pages.create(
        parent={"database_id": db_id},
        properties=properties,
    )


def get_open_commitments(database_id: Optional[str] = None) -> list:
    """Fetch Open Commitments (commitment-like tags)."""
    return query_nexus(
        database_id=database_id,
        filter_obj={
            "or": [
                {"property": "Sovereign Tag", "rich_text": {"contains": "commitment"}},
                {"property": "Sovereign Tag", "rich_text": {"contains": "task"}},
                {"property": "Sovereign Tag", "rich_text": {"contains": "meeting"}},
                {"property": "Sovereign Tag", "rich_text": {"contains": "decision"}},
            ]
        },
        sorts=[{"property": "Priority", "direction": "descending"}],
    )


def get_nexus_since(since_iso: str, database_id: Optional[str] = None) -> list:
    """Fetch Nexus pages with Last Updated on or after since_iso (e.g. 24h ago)."""
    db_id = database_id or NOTION_NEXUS_DATABASE_ID
    if not db_id:
        raise ValueError("NOTION_NEXUS_DATABASE_ID is required")
    return query_nexus(
        database_id=db_id,
        filter_obj={
            "property": "Last Updated",
            "date": {"on_or_after": since_iso},
        },
        sorts=[{"timestamp": "last_edited_time", "direction": "descending"}],
    )


def get_recent_nuggets(limit: int = 10, database_id: Optional[str] = None) -> list:
    """Fetch most recent Nexus pages (by last edited time). Returns list of page dicts."""
    db_id = database_id or NOTION_NEXUS_DATABASE_ID
    if not db_id:
        raise ValueError("NOTION_NEXUS_DATABASE_ID is required")
    client = get_client()
    data_source_id = _get_data_source_id(db_id)
    results = collect_paginated_api(
        client.data_sources.query,
        data_source_id=data_source_id,
        sorts=[{"timestamp": "last_edited_time", "direction": "descending"}],
    )
    return results[:limit] if results else []


def get_recent_thoughts(limit: int = 50, database_id: Optional[str] = None) -> list:
    """Fetch recent Thought Memory entries (Sovereign Tag contains 'thought'). Epic 5."""
    return get_recent_by_tag("thought", limit=limit, database_id=database_id)


def get_recent_by_tag(tag: str, limit: int = 50, database_id: Optional[str] = None) -> list:
    """Fetch recent Nexus entries by Sovereign Tag substring (case-insensitive matching in Notion)."""
    tag = (tag or "").strip()
    if not tag:
        return []
    return query_nexus(
        database_id=database_id,
        filter_obj={
            "property": "Sovereign Tag",
            "rich_text": {"contains": tag},
        },
        sorts=[{"timestamp": "last_edited_time", "direction": "descending"}],
    )[:limit]


def get_recent_people_context(limit: int = 50, database_id: Optional[str] = None) -> list:
    """Fetch recent People Context / conversation summary entries."""
    return get_recent_by_tag("people-context", limit=limit, database_id=database_id)


def get_recent_grandmas_closet(limit: int = 50, database_id: Optional[str] = None) -> list:
    """Fetch recent deferred ideas from Grandma's Closet (Epic 6)."""
    return get_recent_by_tag("grandmas-closet", limit=limit, database_id=database_id)


def _get_prop(page: dict, name: str, kind: str = "plain") -> str:
    """Extract a property value from a Notion page for display."""
    props = page.get("properties") or {}
    p = props.get(name)
    if not p or not isinstance(p, dict):
        return ""
    if p.get("type") == "title":
        titles = (p.get("title") or [])
        if titles and isinstance(titles[0], dict):
            return (titles[0].get("plain_text") or "").strip()
        return ""
    if p.get("type") == "date":
        d = p.get("date")
        if d and d.get("start"):
            return d.get("start", "")
        return ""
    if p.get("type") == "rich_text":
        rt = (p.get("rich_text") or [])
        if not rt:
            return ""
        parts = []
        for node in rt:
            if isinstance(node, dict):
                parts.append(node.get("plain_text") or "")
        return "".join(parts).strip()
    return ""


def find_people_context_page(contact_key: str, database_id: Optional[str] = None) -> Optional[dict]:
    """Find latest canonical people-context page for a contact key."""
    key = (contact_key or "").strip()
    if not key:
        return None
    pages = query_nexus(
        database_id=database_id,
        filter_obj={
            "and": [
                {"property": "Sovereign Tag", "rich_text": {"contains": "people-context"}},
                {"property": "Context", "title": {"contains": key}},
            ]
        },
        sorts=[{"timestamp": "last_edited_time", "direction": "descending"}],
    )
    return pages[0] if pages else None


def update_page_fields(
    page_id: str,
    *,
    context: Optional[str] = None,
    content: Optional[str] = None,
    priority: Optional[str] = None,
    sovereign_tag: Optional[str] = None,
) -> dict:
    """Update selected Notion page properties."""
    if not page_id:
        raise ValueError("page_id is required")
    client = get_client()
    props = {"Last Updated": {"date": {"start": _now_iso(), "end": None}}}
    if context is not None:
        props["Context"] = {"title": [{"text": {"content": context[:2000]}}]}
    if content is not None:
        props["Content"] = {"rich_text": _rt(content)}
    if priority is not None:
        props["Priority"] = {"select": {"name": priority}}
    if sovereign_tag is not None:
        props["Sovereign Tag"] = {"rich_text": _rt(sovereign_tag)}
    return client.pages.update(page_id=page_id, properties=props)
