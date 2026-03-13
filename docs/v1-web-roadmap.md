# Enigma V1 — Web-first roadmap

**Goal:** Ship a full web version, deploy it, and polish the UI to a professional standard before building mobile (FlutterFlow or similar).

---

## Current state

- **Done:** Epics 1–4 (Memory, Ingestion, Brief, Life Query, Action Sphere), Brief-to-Query handoff, CRON, logging, docs.
- **Deferred for V1 web:** Flutter/FlutterFlow port (do after V1 web is live and polished).

---

## V1 web — next epics (in order)

### Phase A — Ship & polish (foundation)

| # | Theme | What | Why first |
|---|--------|-----|-----------|
| **A1** | **Deployment** | Deploy FastAPI + static assets to a host (e.g. Render, Fly.io, Railway). Env/secrets, single-user or optional Supabase Auth. | You need a live URL to share, test on real devices, and iterate on UI. |
| **A2** | **Web UI polish** | Refine Action Sphere + Milan Minimalism: responsive layout, typography, spacing, micro-interactions, accessibility, “professional” feel. Align with [docs/front-end-spec.md](front-end-spec.md) and Figma if used. | Makes the current orb/feed/Life Query/capture experience feel production-ready before adding more screens. |

**Outcome:** App is live and the existing UI looks and feels professional.

---

### Phase B — Full web experience (dashboard)

| # | Epic | What | Why |
|---|------|-----|-----|
| **B1** | **Epic 7 (first slice)** | **Dashboard shell + core views:** Navigation (e.g. sidebar or top nav); **Commitments** view (dedicated page or enhanced feed); **Brief archive** (store past briefs, list + read); **Life Query history** (store past Q&A, list + read). Milan Minimalism; optional **Supabase Auth** if you want multi-user or secure access. | This is the “full web app” experience: one place to see commitments, past briefs, and past queries. Doesn’t depend on Thought Memory or Grandma’s Closet. |
| **B2** | **Epic 4 — Auth (if needed)** | Supabase Auth for login/session so the deployed app can be used by you (or multiple users) without exposing data publicly. | Do in Phase B if you deploy for more than single-user or need protected access. |

**Outcome:** Single web app with Dashboard, Commitments, Brief archive, Life Query history, and optional auth.

---

### Phase C — Richer memory (thoughts & closet)

| # | Epic | What | Why |
|---|------|-----|-----|
| **C1** | **Epic 5 — Thought Memory** | FR-5.1–5.4: At audio capture, choice (or LLM) “Thought” vs “Commitment”; thoughts stored with tag `thought`; Life Query over thoughts; optional weekly LLM stitching; “Thoughts worth revisiting” in Brief. | Adds a second memory type and makes the Brief and dashboard more valuable. |
| **C2** | **Epic 6 — Grandma’s Closet** | FR-6.1–6.4: Tag `grandmas-closet`; “Act now or save to Grandma’s Closet?” after thought; weekly digest; Life Query over closet. | Completes the “defer ideas” loop and gives the dashboard a Grandma’s Closet section. |

**Outcome:** Dashboard can show Thoughts and Grandma’s Closet; Brief and Life Query use them.

---

### Phase D — Import (chat → people context)

| # | Epic | What | Why |
|---|------|-----|-----|
| **D1** | **Epic 8 — Chat Import** | FR-8.1–8.3: WhatsApp .txt parser; Telegram export parser; re-import = merge/refresh; **Epic 7.3** Import Chat UI (file picker, upload .txt / JSON). | Feeds people-context into Nexus; Import Chat section lives in the dashboard (FR-7.3). |
| **D2** | **Epic 7.1 (full)** | Dashboard sections for Thoughts, Commitments, Conversations (people context), Grandma’s Closet, plus existing Brief archive and Life Query history. | Full User View as in the PRD. |

**Outcome:** Users can import WhatsApp/Telegram and see Conversations/summaries in the dashboard; full Epic 7 dashboard.

---

## Summary order for V1 web

1. **A1** — Deployment  
2. **A2** — Web UI polish  
3. **B1** — Epic 7 first slice (Dashboard, Commitments, Brief archive, Life Query history) (+ **B2** Auth if needed)  
4. **C1** — Epic 5 (Thought Memory)  
5. **C2** — Epic 6 (Grandma’s Closet)  
6. **D1** — Epic 8 (Chat Import) + **D2** — Epic 7.1 full (all dashboard sections)  

After V1 web is live and polished, plan FlutterFlow/mobile as the next phase.

---

## References

- [tasks.md](../tasks.md) — Full task checklist  
- [docs/prd.md](prd.md) — Goals, FRs (Epics 5–8)  
- [docs/front-end-spec.md](front-end-spec.md) — Design tokens, component map (Figma ↔ code)
