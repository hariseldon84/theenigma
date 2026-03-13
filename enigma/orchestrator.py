"""Central orchestration layer — bridges Notion (Nexus) and Supabase (Vault)."""
from typing import Optional

from enigma.notion_client import (
    get_client as get_notion_client,
    query_nexus,
    create_nugget,
    get_open_commitments,
)
from enigma.supabase_client import get_client as get_supabase_client, vault_insert, vault_query


def push_to_nexus(context: str, content: str, priority: str = "medium", tag: str = "") -> dict:
    """Push a Knowledge Nugget to The Nexus (Notion)."""
    return create_nugget(
        context=context,
        content=content,
        priority=priority,
        sovereign_tag=tag,
    )


def fetch_commitments() -> list[dict]:
    """Fetch Open Commitments from The Nexus."""
    return get_open_commitments()


def store_in_vault(
    table: str,
    data: dict,
    *,
    encrypt_payload: bool = True,
) -> dict:
    """Store encrypted data in The Vault (Supabase).

    For encrypted storage, data must include:
      key_type: str (e.g. 'credential', 'secret')
      payload: str | dict (encrypted at rest)
      metadata: optional dict (stored plain, e.g. user_id)
    """
    return vault_insert(table, data, encrypt_payload=encrypt_payload)


def read_from_vault(
    table: str,
    filters: Optional[dict] = None,
    *,
    decrypt_payload: bool = True,
) -> list:
    """Read from The Vault. Returns list of rows with decrypted 'data' field (payload)."""
    return vault_query(table, filters, decrypt_payload=decrypt_payload)


def health_check() -> dict:
    """Verify Notion and Supabase connectivity."""
    result = {"notion": False, "supabase": False, "errors": []}
    try:
        get_notion_client()
        result["notion"] = True
    except Exception as e:
        result["errors"].append(f"Notion: {e}")
    try:
        get_supabase_client()
        result["supabase"] = True
    except Exception as e:
        result["errors"].append(f"Supabase: {e}")
    return result
