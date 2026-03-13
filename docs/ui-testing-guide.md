# Enigma — UI-level testing guide

**Prerequisites:** Server running at http://127.0.0.1:5000 (run `cd /path/to/thenigma && .venv/bin/python -m enigma.main web`).  
**Required in `.env`:** `NOTION_API_KEY`, `NOTION_NEXUS_DATABASE_ID`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`.  
**For audio / Life Query / Brief:** `OPENAI_API_KEY`.

---

## 1. Action Sphere (main UI)

**URL:** http://127.0.0.1:5000/

| What to test | Steps | Expected |
|--------------|--------|----------|
| **Page loads** | Open `/` in the browser | Dark theme (Milan Minimalism), “ACTION SPHERE” header, central orb, “Open Commitments” section. |
| **Open Commitments feed** | Load page | List of commitments from Nexus (or “No open commitments.” if empty). If you see “Could not load commitments”, check Notion env and backend logs. |
| **Orb tap** | Click the orb once | Page scrolls to the Open Commitments feed. |
| **Orb long-press** | Mouse: press and hold orb ~0.5s. Touch: press and hold. | Life Query panel opens (overlay with “Life Query”, text area, Ask button, mic). |
| **Life Query (text)** | Long-press orb → type a question (e.g. “What are my open commitments?”) → click **Ask** | Status “Asking…” then an answer card below with the reply (from Nexus + commitments). |
| **Life Query (voice)** | Long-press orb → click mic → allow microphone → speak → click mic again | “Recording…” then “Transcribing & asking…” then answer card with question and answer. |
| **Close Life Query** | Click **Close** in the Life Query panel | Panel closes, back to orb and feed. |
| **Audio FAB** | Click the blue mic button (bottom-right) | Capture panel opens: “Commitment” / “People context” toggle and large mic. |
| **Commitment capture** | Audio FAB → leave “Commitment” selected → click mic → speak → click mic again | “Recording…” then “Sending…” then “Saved to Nexus [tag]: …”. Commitments list refreshes; new item appears (after reload if needed). |
| **People context capture** | Audio FAB → click “People context” → record as above | Same flow; saved with people-context tag. |
| **Close capture** | Click **Close** in the capture panel | Panel closes. |

---

## 2. Brief follow-up (FR-3.4)

**URL:** http://127.0.0.1:5000/?followup=1#life-query

| What to test | Steps | Expected |
|--------------|--------|----------|
| **Follow-up link** | Open the URL above (after running `brief` at least once so a brief exists) | Life Query panel opens automatically; placeholder “Ask a follow-up about your Sovereign Brief…”; status “Brief context loaded — ask a follow-up.” |
| **Ask with brief context** | Type a follow-up (e.g. “Summarize the top priority”) → **Ask** | Answer is based on the last delivered brief plus Nexus/commitments. |

To have a brief available: run `python -m enigma.main brief` or `brief-only` once; the app stores the last brief for this flow.

---

## 3. Standalone commitment capture

**URL:** http://127.0.0.1:5000/capture

| What to test | Steps | Expected |
|--------------|--------|----------|
| **Capture page** | Open `/capture` | Same capture UI as in Action Sphere (Commitment / People context + mic). |
| **Record and send** | Choose mode, click mic, speak, click mic again | Same behavior as Audio FAB flow; entry appears in Nexus and in the commitments feed on `/`. |

---

## 4. Quick checklist (no audio)

If you can’t use a mic or don’t want to call OpenAI:

1. **Health:** Run `python -m enigma.main health` → Notion and Supabase OK.
2. **Feed:** Open http://127.0.0.1:5000 → commitments load or “No open commitments.”
3. **Orb tap:** Click orb → scrolls to feed.
4. **Orb long-press:** Hold orb → Life Query panel opens.
5. **Life Query (needs OPENAI_API_KEY):** Type “What commitments do I have?” → Ask → answer card or error if key missing.
6. **Follow-up URL:** Open http://127.0.0.1:5000/?followup=1#life-query → Life Query opens; if no brief yet, status may still show “Brief context loaded” with no extra context.

---

## 5. Common issues

| Issue | Check |
|-------|--------|
| “Could not load commitments” | Notion env vars; `python -m enigma.main health` and `commitments`. |
| Life Query “Request failed” / 500 | `OPENAI_API_KEY` in `.env`; server logs. |
| Voice / capture “Microphone access denied” | Browser permission for mic; HTTPS or localhost. |
| Follow-up link shows no “Brief context loaded” | Run `python -m enigma.main brief` or `brief-only` once so a brief is stored. |
| Blank or 404 | Server running on port 5000; correct URL (no typo in path). |

---

## 6. API-only smoke test (optional)

From a terminal (server running):

```bash
curl -s http://127.0.0.1:5000/api/commitments
curl -s http://127.0.0.1:5000/api/brief/context
curl -s -X POST http://127.0.0.1:5000/api/query -H "Content-Type: application/json" -d '{"question":"What do I have?"}'
```

Expected: JSON responses (commitments list, `{"brief":...}`, `{"answer":...}`).
