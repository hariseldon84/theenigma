"""Supabase client for The Vault — encrypted sensitive storage."""
from typing import Optional

from supabase import create_client, Client

from enigma.config import SUPABASE_URL, SUPABASE_SERVICE_KEY, VAULT_ENCRYPTION_KEY
from enigma.vault_crypto import decrypt_to_data, encrypt


def get_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY are required. Set them in .env")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def vault_insert(
    table: str,
    data: dict,
    *,
    encrypt_payload: bool = True,
) -> dict:
    """Insert into a Vault table.

    If encrypt_payload is True (default), data must have:
      - key_type: str
      - payload: str | dict (encrypted before store)
      - metadata: optional dict (stored plain)
    The row stored is: key_type, encrypted_data, metadata.

    If encrypt_payload is False, data is inserted as-is (legacy; not recommended).
    """
    client = get_client()
    if not encrypt_payload:
        result = client.table(table).insert(data).execute()
        return result.data[0] if result.data else {}

    key_type = data.get("key_type")
    payload = data.get("payload")
    metadata = data.get("metadata", {})
    if key_type is None or payload is None:
        raise ValueError("vault_insert with encryption requires data['key_type'] and data['payload']")

    if not VAULT_ENCRYPTION_KEY:
        raise ValueError(
            "VAULT_ENCRYPTION_KEY is required for encrypted vault storage. "
            "Generate with: python -c \"import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())\""
        )
    encrypted_data = encrypt(payload, VAULT_ENCRYPTION_KEY)
    row = {
        "key_type": key_type,
        "encrypted_data": encrypted_data,
        "metadata": metadata,
    }
    result = client.table(table).insert(row).execute()
    return result.data[0] if result.data else {}


def vault_query(
    table: str,
    filters: Optional[dict] = None,
    *,
    decrypt_payload: bool = True,
) -> list[dict]:
    """Query a Vault table. When decrypt_payload is True, each row gets a 'data' key with decrypted payload."""
    client = get_client()
    query = client.table(table).select("*")
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    result = query.execute()
    rows = result.data or []

    if not decrypt_payload or not VAULT_ENCRYPTION_KEY:
        return rows

    out = []
    for row in rows:
        row = dict(row)
        enc = row.pop("encrypted_data", None)
        if enc:
            try:
                row["data"] = decrypt_to_data(enc, VAULT_ENCRYPTION_KEY)
            except Exception:
                row["data"] = None
        out.append(row)
    return out
