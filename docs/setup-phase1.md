# Phase 1 Setup — Notion + Supabase + Python

**Goal:** Memory foundation (The Nexus + The Vault) with Python orchestration.

---

## 1. Notion — The Nexus

### Create the database

1. In Notion, create a new **database** (full page).
2. Name it **The Nexus**.
3. Add these properties:

| Property      | Type     | Options / Notes                    |
|---------------|----------|------------------------------------|
| **Context**   | Title    | Primary column; short label        |
| **Content**   | Text     | Full nugget/commitment content     |
| **Priority**  | Select   | high, medium, low                  |
| **Sovereign Tag** | Text | e.g. `commitment`, `nugget`, `transient` |

4. **Copy the database ID** from the URL (see [Finding the database ID](#finding-the-database-id) below).

### Finding the database ID

Notion URLs vary. The database ID is a **32-character alphanumeric string**. Extract it as follows:

| URL format | Where the ID is |
|------------|-----------------|
| `https://www.notion.so/workspace-name/abc123def456...?v=xyz` | Between the last `/` and `?` — use `abc123def456...` (32 chars) |
| `https://www.notion.so/abc123def45678901234567890123456` | The 32-char string after the last `/` |
| `https://notion.so/abc123def45678901234567890123456?v=...` | Same — before `?` or to end of URL |

**Rules:**
- The ID is **32 characters** (letters and numbers).
- Ignore any `?v=...` (view ID) or `?p=...` (share) parameters.
- If the ID has hyphens (UUID format like `e604f78c-4145-4444-b7d5-1adea4fa5d08`), remove them for some API calls, or use as-is — the Notion API accepts both.

**Example:** From `https://www.notion.so/myworkspace/a1b2c3d4e5f6789012345678abcdef12?v=xyz`, the database ID is `a1b2c3d4e5f6789012345678abcdef12`.

### Create an integration (Internal — recommended for Enigma MVP)

**Internal integrations** are workspace-only and simpler. Use this for Enigma MVP.

1. Go to **[notion.so/my-integrations](https://www.notion.so/my-integrations)**  
   - Or: Notion → **Settings** (sidebar) → **Integrations** → **"Develop your own integrations"**
2. Click **+ New integration**
3. **Integration type:** Select **Internal**
4. **Name:** e.g. `Enigma`
5. **Associated workspace:** Choose your workspace (must be Workspace Owner)
6. Click **Submit** (or **Create**)
7. Open the **Configuration** tab → copy the **Internal Integration Secret** (starts with `secret_`)

**That’s it for Internal.** No Company Name, Website, or Privacy Policy required.

### Public integration (alternative)

If you need **Public** (OAuth, for any workspace), you’ll need:

- **Company Name**
- **Website URL**
- **Privacy Policy URL**
- **Terms of Use URL**
- **Support Email**
- **Redirect URI(s)** for OAuth

Enigma MVP does **not** require a Public integration.

### Share the database with the integration

1. Open **The Nexus** database in Notion
2. Click the **⋯** (More) menu (top right)
3. Scroll to **+ Add connections**
4. Search for your integration (e.g. `Enigma`) and select it
5. Confirm access — the integration can now read/write this database

---

## 2. Supabase — The Vault

### Create project

1. [supabase.com](https://supabase.com) → New project
2. Note **Project URL** and **Service Role Key** (Settings → API)

### Create Vault table

Run in SQL Editor:

```sql
CREATE TABLE vault (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  key_type TEXT NOT NULL,
  encrypted_data TEXT,
  metadata JSONB DEFAULT '{}'
);
```

For AES-256 encryption, add `pgcrypto` and encrypt at application layer before insert.

---

## 3. Python environment

```bash
cd /Users/anandarora/thenigma
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 4. Environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```
NOTION_API_KEY=secret_xxx
NOTION_NEXUS_DATABASE_ID=xxx

SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx

# Vault AES-256 encryption (required for vault store/read)
VAULT_ENCRYPTION_KEY=<base64-encoded-32-bytes>
```

Use your **Internal Integration Secret** for `NOTION_API_KEY` and **Service Role Key** (from Supabase → Settings → API) for `SUPABASE_SERVICE_KEY`.

**VAULT_ENCRYPTION_KEY:** Generate a 32-byte key:  
`python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"`  
Paste the output into `.env`. Keep it secret; without it, encrypted vault data cannot be decrypted.

---

## 5. Verify

```bash
python -m enigma.main health
```

Expected: `Notion: OK`, `Supabase: OK`.

---

## 6. Quick test

```bash
# Push a test nugget
python -m enigma.main push "Test context" "Test content"

# Fetch commitments (if any tagged)
python -m enigma.main commitments

# Vault: store and read encrypted (requires VAULT_ENCRYPTION_KEY in .env)
python -m enigma.main vault-set "test" "secret payload"
python -m enigma.main vault-get
```

---

## Next: Phase 2 — Omni-Scribe

After Phase 1 works, add the Desktop Sentinel (window + clipboard scraper) that pushes to Notion every 15 minutes.
