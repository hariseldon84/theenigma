# Enigma OS — MVP Roadmap

**Source:** Brainstorming session 2026-03-10  
**Target:** 72-hour MVP

---

## Tech Stack (Locked)

| Layer | Choice |
|-------|--------|
| **Memory** | Notion (Nexus) + Supabase (Vault) |
| **Desktop** | Python (Omni-Scribe) |
| **UI** | FlutterFlow / Flutter |
| **LLM** | Claude 3.5 Sonnet or GPT-4o (Gemini optional) |

---

## Priority Tiers

### P0 — Must-Have (72h core)
- Notion Nexus + Supabase Vault
- Python Desktop Sentinel (Omni-Scribe)
- Sovereign Brief (CRON 09:00)
- Action Sphere UI (orb, Open Commitments, Milan Minimalism)

### P1 — High-Value (if time)
- Manual Commitment Capture
- Life Query (orb long-press)

### P2 — Quick Wins (post-MVP)
- Audio Summary Bridge
- Brief-to-Query Handoff

### P3 — Later
- Proactive Draft Engine (reply + research init)

---

## Build Order

| # | Phase | Deliverable |
|---|-------|-------------|
| 1 | Foundation | Notion + Supabase + Python orchestration |
| 2 | Ingestion | Omni-Scribe → Notion every 15 min |
| 3 | Brief | Sovereign Brief (LLM, CRON, Email/Telegram) |
| 4 | UI | Action Sphere (orb, Open Commitments) |
| 5 | Capture | Manual Commitment (audio → Nexus) |
| 6 | Query | Life Query (orb long-press → RAG → answer) |

---

## UX Summary

- **Orb tap** → Open Commitments
- **Orb long-press** → Life Query (voice)
- **Audio button** → Manual Commitment or Audio Summary
- **Sovereign Brief** → "Ask follow-up" → Life Query with context
