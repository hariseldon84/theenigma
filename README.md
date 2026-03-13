# Enigma OS

Sovereign-Edge Cognitive Operating System — an ambient, proactive intelligence layer that reduces Information Debt (the gap between owned data and the ability to retrieve or act on it).

**Stack:** Notion (The Nexus) + Supabase (The Vault) + Python orchestration. See [docs/prd/](docs/prd/) for the full PRD.

---

## Quick start

1. **Setup** — Follow [docs/setup-phase1.md](docs/setup-phase1.md) for:
   - Notion database (The Nexus) + integration
   - Supabase project + `vault` table
   - Python venv: `python -m venv .venv`, `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows), `pip install -r requirements.txt`
   - **Environment:** Copy `.env.example` to `.env` and set at least: `NOTION_API_KEY`, `NOTION_NEXUS_DATABASE_ID`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`. See `.env.example` for optional vars (Vault, OpenAI, Brief, etc.).

2. **Verify** — After setup, run:

   ```bash
   python -m enigma.main health
   ```
   Expected: `Notion: OK`, `Supabase: OK`.

3. **Quick test** — Confirm Nexus and Vault:

   ```bash
   # Push a test nugget to The Nexus
   python -m enigma.main push "Test context" "Test content"

   # List Open Commitments (items with Sovereign Tag containing "commitment")
   python -m enigma.main commitments

   # Vault: store and read encrypted (requires VAULT_ENCRYPTION_KEY in .env)
   python -m enigma.main vault-set "test" "secret payload"
   python -m enigma.main vault-get
   ```

---

## CLI commands

| Command | Description |
|--------|-------------|
| `python -m enigma.main health` | Check Notion + Supabase connectivity |
| `python -m enigma.main push 'context' 'content'` | Create a Knowledge Nugget in The Nexus |
| `python -m enigma.main commitments` | Fetch Open Commitments from Nexus |
| `python -m enigma.main vault-set 'key_type' 'payload'` | Store encrypted payload in Vault |
| `python -m enigma.main vault-get [key_type]` | List Vault rows (decrypted); optional filter by key_type |
| `python -m enigma.main sentinel-once` | Omni-Scribe: push one sample (window + clipboard) to Nexus |
| `python -m enigma.main sentinel [min]` | Omni-Scribe: run loop, push every N min (default 15) |
| `python -m enigma.main nexus-recent [N]` | Show last N Nexus rows with Context and Last Updated |
| `python -m enigma.main web` | Run Commitment Capture web app at http://127.0.0.1:5000 |
| `python -m enigma.main brief` | Generate and deliver Sovereign Brief (email + Telegram if configured) |
| `python -m enigma.main brief-only` | Generate Brief and print to stdout (no delivery) |
| `python -m enigma.main thought-stitch` | Epic 5: themes/suggestions from Thought Memory |

### Commitment Capture (FR-2.2)

One-tap record in the browser; audio is transcribed (Whisper), translated to a default language, classified by AI, then saved to Nexus:

1. Add `OPENAI_API_KEY` to `.env` (from [platform.openai.com](https://platform.openai.com)).
2. Optional: set `NEXUS_DEFAULT_LANGUAGE=en` (or `English`, `hi`, etc.) so all content is stored in that language. Default is English.
3. Run `python -m enigma.main web` (or `.venv/bin/python -m enigma.main web`).
4. Open http://127.0.0.1:5000 in your browser (or http://127.0.0.1:8000 if you set `PORT=8000`).

**If port 5000 is in use** (e.g. "address already in use", or macOS AirPlay using 5000): set `PORT=8000` in `.env` and restart; then open http://127.0.0.1:8000. — choose **Commitment** or **People context** (Audio Summary Bridge), then click mic to start, click again to stop and send.  
   - **Commitment:** transcribed, translated, AI-classified, then saved with a sovereign tag (commitment, tasks, meetings, etc.).  
   - **People context:** transcribed, translated, and saved with tag `people-context` (chat/people summary).  
   - **Thought (Epic 5):** transcribed, translated, and saved with tag `thought` (Thought Memory). Life Query can answer “What have I been thinking about?”; the Sovereign Brief includes “Thoughts worth revisiting.”

### Sovereign Brief (FR-3.1)

Daily digest: last 24h Nexus + Open Commitments, synthesized by LLM, delivered by email and/or Telegram.

1. Optional: set in `.env`: `BRIEF_EMAIL_TO`, `BRIEF_SMTP_*`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (see `.env.example`).
2. Run manually: `python -m enigma.main brief` (generates and sends), or `python -m enigma.main brief-only` (prints only).
3. **Schedule daily:** see [CRON setup for Sovereign Brief](#cron-setup-for-sovereign-brief) below.

For **testing** (see raw context sent to the LLM) and **configuring Email + Telegram**, see [docs/brief-testing-and-delivery.md](docs/brief-testing-and-delivery.md).

#### CRON setup for Sovereign Brief

To deliver the Sovereign Brief every day at 09:00 (P0 delivery per PRD):

1. **Use the project venv** so the same Python and env as your manual runs are used:
   ```bash
   cd /path/to/thenigma   # replace with your repo path
   .venv/bin/python -m enigma.main brief
   ```
   Run that once manually to confirm it works (and that `.env` is in the repo root).

2. **Add a CRON job** (run at 09:00 every day):
   ```bash
   crontab -e
   ```
   Add this line (replace `/path/to/thenigma` with your actual path):
   ```
   0 9 * * * cd /path/to/thenigma && .venv/bin/python -m enigma.main brief
   ```
   Times are in the **system time zone** of the machine. For UTC 09:00, ensure the server TZ is UTC or use a wrapper that sets `TZ=UTC`.

3. **Optional:** Set `BRIEF_DELIVERY_TIME=09:00` in `.env` for documentation; the CRON expression controls when the job runs.

4. **Verify:** After saving crontab, run `crontab -l` to confirm the line is present. Check email/Telegram after 09:00 on the next run, or temporarily use a 2-minute schedule (e.g. `*/2 * * * *`) to test.

See [docs/cron-brief.md](docs/cron-brief.md) for more detail and troubleshooting.

### Auth (Supabase) — optional

To protect `/api/*` with Supabase Auth:

1. In Supabase: enable Auth, create a user (email/password). Copy **Project URL**, **anon key**, and **JWT Secret** (Settings → API).
2. In `.env`: set `AUTH_REQUIRED=1`, `SUPABASE_ANON_KEY=...`, `SUPABASE_JWT_SECRET=...` (and `SUPABASE_URL` if not already set).
3. Restart the web app. Opening `/` or `/capture` will redirect to `/login` until you sign in. All API requests require `Authorization: Bearer <access_token>` (the login page stores the token in `localStorage`).

If `AUTH_REQUIRED` is unset or 0, the app runs without auth (single-user / local use).

**Local testing:** On the login page you can "Create an account" (sign up) or sign in. If Supabase has "Confirm email" enabled (Authentication → Providers → Email), new users must confirm before signing in; for local testing you can turn that off so sign-up works immediately. Use "Sign out" in the Action Sphere header to test the flow again.

**"Could not load auth config":** See [docs/auth-troubleshooting.md](docs/auth-troubleshooting.md). Common causes: opening the app from `file://` or another port (use http://127.0.0.1:5000), or the server not running.

### Open Commitments API (FR-3.2)

`GET http://127.0.0.1:5000/api/commitments` returns JSON list of open commitments (for Action Sphere / Epic 4).

---

## API reference

Base URL when running the web app: `http://127.0.0.1:5000`.

| Method | Path | Description | Request / Response |
|--------|------|-------------|--------------------|
| **GET** | `/api/commitments` | Open Commitments for Action Sphere feed (FR-3.2) | No body. Returns `[{ "id", "context", "content", "tag" }, ...]`. |
| **POST** | `/api/commitment` | Manual Commitment, People Context, or Thought (FR-2.2, FR-2.3, Epic 5) | `multipart/form-data`: `audio` (file), `type` (`commitment`, `people_context`, or `thought`). Returns `{ "id", "context", "preview", "tag" }`. |
| **GET** | `/api/brief/context` | Last delivered Sovereign Brief for Life Query follow-up (FR-3.4) | No body. Returns `{ "brief": "<text>" \| null }`. |
| **POST** | `/api/query` | Life Query: RAG over Nexus + Commitments (FR-3.3) | JSON: `{ "question": string, "brief_context": string \| null }`. Returns `{ "answer": string }`. |
| **POST** | `/api/query/voice` | Life Query via voice: transcribe then RAG (FR-3.3) | `multipart/form-data`: `audio` (file), optional `brief_context` (string). Returns `{ "question", "answer" }`. |

All POST endpoints return JSON errors with `detail` on failure (4xx/5xx).

---

## Docs

| Document | Purpose |
|----------|---------|
| [docs/setup-phase1.md](docs/setup-phase1.md) | Notion + Supabase + Python setup |
| [docs/ui-testing-guide.md](docs/ui-testing-guide.md) | UI-level testing — Action Sphere, Life Query, capture, follow-up |
| [docs/v1-web-roadmap.md](docs/v1-web-roadmap.md) | V1 web roadmap — deploy, UI polish, dashboard, Thought Memory, Chat Import |
| [docs/prd/](docs/prd/) | Product requirements (sharded) |
| [docs/mvp-roadmap.md](docs/mvp-roadmap.md) | MVP build order |
| [tasks.md](tasks.md) | Development task list |
| [cardinal_rules.md](cardinal_rules.md) | Development rules (architecture, SaaS-ready) |
