"""AES-256-GCM encryption for The Vault. Encrypt at app layer before insert."""
import base64
import json
import os
from typing import Union

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# GCM nonce size (96 bits recommended)
_NONCE_SIZE = 12


def _get_key(key_b64: str) -> bytes:
    """Decode base64 key to 32 bytes. Raises if invalid."""
    raw = base64.urlsafe_b64decode(key_b64)
    if len(raw) != 32:
        raise ValueError("VAULT_ENCRYPTION_KEY must decode to 32 bytes (256 bits)")
    return raw


def encrypt(plaintext: Union[str, dict], key_b64: str) -> str:
    """Encrypt plaintext (str or dict) with AES-256-GCM. Returns base64(nonce || ciphertext)."""
    key = _get_key(key_b64)
    if isinstance(plaintext, dict):
        plaintext = json.dumps(plaintext)
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")
    nonce = os.urandom(_NONCE_SIZE)
    cipher = AESGCM(key)
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    blob = nonce + ciphertext
    return base64.urlsafe_b64encode(blob).decode("ascii")


def decrypt(ciphertext_b64: str, key_b64: str) -> str:
    """Decrypt base64(nonce || ciphertext) to UTF-8 string."""
    key = _get_key(key_b64)
    blob = base64.urlsafe_b64decode(ciphertext_b64)
    if len(blob) < _NONCE_SIZE:
        raise ValueError("Invalid encrypted payload")
    nonce = blob[:_NONCE_SIZE]
    ciphertext = blob[_NONCE_SIZE:]
    cipher = AESGCM(key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


def decrypt_to_data(ciphertext_b64: str, key_b64: str) -> Union[str, dict]:
    """Decrypt and return as str or dict (if JSON)."""
    raw = decrypt(ciphertext_b64, key_b64)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw
