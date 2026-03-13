#!/usr/bin/env python3
"""
One-off auth flow test: sign in to Supabase with email/password, then call Enigma API.
Password must be passed via env ENIGMA_TEST_PASSWORD (never commit credentials).
Usage: ENIGMA_TEST_PASSWORD=yourpass python scripts/test_auth_flow.py
"""
import os
import sys
from pathlib import Path

# Load project .env
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

def main():
    email = os.environ.get("ENIGMA_TEST_EMAIL")
    password = os.environ.get("ENIGMA_TEST_PASSWORD")
    if not email or not password:
        print("ERROR: Set ENIGMA_TEST_EMAIL and ENIGMA_TEST_PASSWORD")
        print("  e.g. ENIGMA_TEST_EMAIL=you@example.com ENIGMA_TEST_PASSWORD=xxx python scripts/test_auth_flow.py")
        return 1

    from enigma.config import SUPABASE_URL, SUPABASE_ANON_KEY
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("ERROR: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")
        return 1

    try:
        from supabase import create_client
    except ImportError:
        print("ERROR: supabase package not installed (pip install supabase)")
        return 1

    base_url = os.environ.get("ENIGMA_BASE_URL", "http://127.0.0.1:5000")

    print("1. Signing in to Supabase...", end=" ")
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    resp = client.auth.sign_in_with_password({"email": email, "password": password})
    if resp.session is None or not getattr(resp.session, "access_token", None):
        err = getattr(resp, "error", None) or getattr(resp, "message", "Unknown error")
        print("FAILED:", err)
        return 1
    token = resp.session.access_token
    print("OK (got access token)")

    print("2. Calling Enigma API GET /api/commitments with Bearer token...", end=" ")
    try:
        import urllib.request
        req = urllib.request.Request(
            base_url + "/api/commitments",
            headers={"Authorization": "Bearer " + token},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            code = r.getcode()
            body = r.read().decode("utf-8", errors="replace")[:200]
    except urllib.error.HTTPError as e:
        code = e.code
        body = e.read().decode("utf-8", errors="replace")[:200]
    except Exception as e:
        print("FAILED:", e)
        return 1

    if code == 200:
        print("OK (200)")
        print("3. Auth flow test PASSED: login token accepted by Enigma API.")
        return 0
    else:
        print("FAILED (%s)" % code)
        print("   Response:", body)
        print("3. Auth flow test FAILED: API returned", code)
        return 1

if __name__ == "__main__":
    sys.exit(main())
