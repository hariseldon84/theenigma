# Figma ↔ Cursor (Enigma) — MCP setup & continuous workflow

## Security first

- **Never commit tokens.** Keep them only in `.env` (gitignored) or your shell profile.
- If a token was ever pasted into chat or committed, **revoke it in Figma** immediately:  
  **Figma → Settings → Security → Personal access tokens** → revoke → create a new one.

---

## Environment variables

Add to **`.env`** (never commit):

| Variable | Used by | Notes |
|----------|--------|--------|
| **`FIGMA_API_TOKEN`** | `figma-mcp` (Python) CLI | **Required by this package** — personal access token (`figd_...`) |
| `FIGMA_ACCESS_TOKEN` / `FIGMA_API_KEY` | Aliases some tools use | Same value as `FIGMA_API_TOKEN` if a tool expects these names |
| `FIGMA_OAUTH_TOKEN` | Official streamable HTTP MCP | Same token often works as bearer; see Figma docs for OAuth if required |

`.env.example` contains placeholders only.

---

## Option A — Python `figma-mcp` (personal access token)

Good if you want a **command-based** MCP that reads files via the Figma API using a **Personal access token**.

**Requires Python ≥ 3.12** (the PyPI package does not install on 3.9). This repo already has a dedicated venv installed at **`.venv-figma-mcp/`** (gitignored).

1. **Already installed in this project**

   ```bash
   # If you ever need to recreate it (uv was used because pipx wasn’t available):
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv --python 3.12 .venv-figma-mcp
   uv pip install --python .venv-figma-mcp figma-mcp
   ```

2. **Token env var:** `FIGMA_API_TOKEN` (or pass `--figma-api-key=...`).

3. **Cursor MCP config:** use **full path** to the binary so Cursor doesn’t rely on PATH:

   - **Command:** `/Users/anandarora/thenigma/.venv-figma-mcp/bin/figma-mcp`
   - **Args:** (empty) if you set `FIGMA_API_TOKEN` in the MCP server `env` block in `.cursor/mcp.json`.

   Copy `.cursor/mcp.json.example` → `.cursor/mcp.json`, fill `FIGMA_API_TOKEN`, restart Cursor.

4. **Install (alternative — global pipx, Python 3.12+):**

   ```bash
   pipx install figma-mcp
   ```

5. **Cursor MCP — command + env (if not using project venv path):**

   Cursor Settings → **MCP** → Add server, **type: command**:

   - **Command:** `figma-mcp`
   - **Args:** `--figma-api-key` + *your token* **or** use env and no literal key:
     - Preferred: set `FIGMA_API_KEY` in the environment that launches Cursor, then args can be `--figma-api-key` with value from env if the server supports it — **check package docs**; many examples pass the key directly (use Cursor’s env injection if available).

   **Project file:** copy `.cursor/mcp.json.example` → `.cursor/mcp.json` and put your token **only** in the `args` value locally, **or** prefer **Cursor Settings → MCP → Add server** and set environment there so nothing secret lives in a file. `.cursor/mcp.json` is gitignored when it contains secrets. Use shell env:

   ```bash
   export FIGMA_API_KEY="your_token_here"
   ```

   Then configure the MCP to run with that env (Cursor often inherits your shell when started from terminal).

3. **Verify**

   In Cursor, ask the agent to list MCP tools or to fetch a Figma file by **file key** from a link you provide.

**Link-based workflow:** Paste a Figma frame/layer link; the agent uses the file + node ID from the URL.

---

## Option B — Official Figma streamable HTTP MCP (Codex-style)

Used by tools that support **streamable HTTP** with bearer auth.

1. **Env**

   ```bash
   export FIGMA_OAUTH_TOKEN="your_token_here"
   ```

2. **Config (Codex `config.toml` pattern — adapt for Cursor if it supports HTTP MCP)**

   - URL: `https://mcp.figma.com/mcp`
   - Bearer: from `FIGMA_OAUTH_TOKEN`
   - Header: `X-Figma-Region: us-east-1` (match your org region)

   Cursor’s UI may label this as **Streamable HTTP** / custom URL — point it at the same URL and set the bearer header from env.

3. **Restart** the IDE after changing MCP config.

---

## Continuous push/pull workflow

Figma doesn’t auto-push *into* Cursor; the **bridge** is:

1. **Design in Figma** → export or keep frames updated.
2. **Pull into repo** via MCP + prompts (inspect node, variables, screenshots).
3. **Single source of truth for code tokens** → `docs/front-end-spec.md` (updated when Sally/UX pulls hex/blur from Figma).
4. **Implement** in `enigma/static/` (or Flutter later) by reading the spec, not by pasting full Figma dumps into code.

### Sally (UX) prompt — pull from Figma into the spec

```text
Use the Figma MCP to inspect the 'Enigma Home' frame (paste Figma link).
I changed backdrop blur and the cerulean accent. Identify exact hex codes and blur values
and update docs/front-end-spec.md only — do not rewrite whole components.
```

### Dev prompt — apply spec to code

```text
Review docs/front-end-spec.md and apply the new design tokens to enigma/static/action-sphere.html
(and any shared CSS). Keep Milan Minimalism; only change token values (e.g. --cerulean, blur).
```

### Naming convention (1:1 mapping)

Use **stable layer names** in Figma that match code anchors, e.g.:

| Figma layer name | Code anchor |
|------------------|-------------|
| `#ActionSphere_Orb` | `.orb` / orb button |
| `#ActionSphere_Feed` | `.feed` / commitments list |
| `#ActionSphere_AudioFAB` | `#audio-fab` |

Then Sally can say “Orb uses #00A3FF” and dev updates the matching variable only.

---

## Troubleshooting

| Issue | What to try |
|-------|-------------|
| Token not picked up | Export var in the same shell that starts Cursor; or set in Cursor env for MCP. |
| 401 / OAuth | Regenerate token; confirm scope includes file read. |
| Wrong file | Always paste the **frame link** so node ID is unambiguous. |
| Codex vs Cursor | Codex uses `config.toml`; Cursor uses MCP UI or `.cursor/mcp.json` — same token, different wiring. |

---

## Files in this repo

| File | Purpose |
|------|--------|
| `docs/front-end-spec.md` | Canonical tokens + component map for Figma ↔ code |
| `docs/figma-mcp-setup.md` | This doc |
| `.env.example` | Placeholders for `FIGMA_*` |
| `.cursor/mcp.json.example` | Template — copy to `mcp.json`, fill locally, don’t commit secrets |
