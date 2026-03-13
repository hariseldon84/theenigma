"""Supabase Auth: verify JWT and optional FastAPI dependency for protecting routes."""
import logging
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from enigma.config import AUTH_REQUIRED, SUPABASE_JWT_SECRET, SUPABASE_URL

logger = logging.getLogger(__name__)
_security = HTTPBearer(auto_error=False)


def _verify_with_jwks(token: str) -> Optional[dict]:
    """Verify JWT using Supabase JWKS (new signing keys). Used when legacy secret fails."""
    url = (SUPABASE_URL or "").strip().rstrip("/")
    if not url:
        return None
    jwks_uri = url + "/auth/v1/.well-known/jwks.json"
    try:
        header = jwt.get_unverified_header(token)
        alg = header.get("alg")
        if alg not in ("RS256", "ES256"):
            return None
        jwks_client = PyJWKClient(jwks_uri)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=[alg],
            audience="authenticated",
        )
        return payload
    except Exception as e:
        logger.debug("JWKS verification failed: %s", e)
        return None


def verify_supabase_jwt(token: str) -> Optional[dict]:
    """
    Verify a Supabase access token (JWT). Returns decoded payload if valid, else None.
    Tries Legacy JWT secret (HS256) first; if that fails, tries JWKS (RS256/ES256) for new signing keys.
    """
    if not token:
        return None
    # 1. Try legacy secret (HS256)
    if SUPABASE_JWT_SECRET:
        try:
            payload = jwt.decode(
                token,
                SUPABASE_JWT_SECRET,
                audience="authenticated",
                algorithms=["HS256"],
            )
            return payload
        except jwt.PyJWTError as e:
            logger.debug("Legacy JWT verification failed: %s", e)
    # 2. Fallback: new JWT Signing Keys (JWKS)
    payload = _verify_with_jwks(token)
    if payload is None and SUPABASE_JWT_SECRET:
        logger.warning("JWT verification failed (legacy and JWKS)")
    return payload


async def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(_security),
) -> dict:
    """
    FastAPI dependency: require valid Supabase JWT and return user payload.
    When AUTH_REQUIRED is False, always returns a minimal 'anon' user (no 401).
    """
    if not AUTH_REQUIRED:
        return {"sub": "anon", "email": None, "role": "anon"}

    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = verify_supabase_jwt(cred.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role", "authenticated"),
    }
