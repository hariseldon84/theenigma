# Enigma OS — Development Tasks

**Last updated:** 2026-03-16  
**Source:** docs/prd/, docs/mvp-roadmap.md

---

## Legend

- `[x]` Done
- `[ ]` Todo
- `(MVP)` — 72h core
- `(P1)` — High-value if time
- `(P2+)` — Post-MVP

---

## Epic 1: Memory Foundation (MVP)

### Setup & Infrastructure

- [x] Notion workspace + database "The Nexus" created
- [x] Notion database properties: Context (Title), Content (Text), Priority (Select), Sovereign Tag (Text)
- [x] Notion Internal Integration created and shared with Nexus DB
- [x] Supabase project created
- [x] Supabase `vault` table created (id, created_at, key_type, encrypted_data, metadata)
- [x] Python venv + requirements.txt (notion-client, supabase, python-dotenv)
- [x] `.env.example` and `.env` with NOTION_API_KEY, NOTION_NEXUS_DATABASE_ID, SUPABASE_URL, SUPABASE_SERVICE_KEY

### Implementation

- [x] `enigma/config.py` — Load env vars from .env
- [x] `enigma/notion_client.py` — Client, query_nexus, create_nugget, get_open_commitments
- [x] `enigma/supabase_client.py` — Client, vault_insert, vault_query
- [x] `enigma/orchestrator.py` — health_check, push_to_nexus, fetch_commitments, store/read_from_vault
- [x] `enigma/main.py` — CLI: health, commitments, push
- [x] FR-1.2: AES-256 encryption at app layer for Vault inserts (encrypt before insert, decrypt on read)
- [x] Add `docs/setup-phase1.md` verification steps to README or CONTRIBUTING

---

## Epic 2: Ambient Ingestion (MVP)

### Omni-Scribe (Desktop Sentinel)

- [x] FR-2.1: Python script to capture active window title (platform API: macOS/Windows/Linux)
- [x] FR-2.1: Python script to capture clipboard content
- [x] FR-2.1: Format as Knowledge Nugget with Sovereign Tag `transient`
- [x] FR-2.1: Push to Notion every 15 min (CRON or daemon loop)
- [x] FR-2.1: Add `omni_scribe` module or `enigma/sentinel.py`
- [x] FR-2.1: Config: NEXUS_PUSH_INTERVAL_MIN (default 15)

### Manual Commitment Capture (P1)

- [x] FR-2.2: Audio recording (mobile/desktop — Flutter or web)
- [x] FR-2.2: Speech-to-text (Whisper / Google / other)
- [x] FR-2.2: Push transcribed text to Nexus with Sovereign Tag `commitment`
- [x] FR-2.2: One-tap record UX

### Audio Summary Bridge (P2)

- [x] FR-2.3: Same audio entry point; user selects "Commitment" vs "People Context"
- [x] FR-2.3: People Context → Nexus with Sovereign Tag `people-context`

---

## Epic 3: Strategic Executive Proxy (MVP)

### Sovereign Brief

- [x] FR-3.1: Fetch last 24h Nexus entries + Open Commitments
- [x] FR-3.1: LLM synthesis (Claude/GPT/Gemini) — priorities, open threads, suggested actions
- [x] FR-3.1: CRON job at 09:00 (or configurable)
- [x] FR-3.1: Delivery: Email (SMTP/SendGrid) + Telegram bot
- [x] FR-3.1: Add `enigma/brief.py` or similar

### Open Commitments Feed

- [x] FR-3.2: API/endpoint to return Open Commitments (already in orchestrator)
- [x] FR-3.2: UI consumes this for Action Sphere feed (Epic 4 — web Action Sphere)

### Life Query (P1)

- [x] FR-3.3: Voice input (orb long-press → Life Query panel; mic in panel for voice query)
- [x] FR-3.3: RAG over Nexus + Open Commitments (7-day Nexus window; Omni-Scribe data in Nexus)
- [x] FR-3.3: LLM answer → answer card in UI
- [x] FR-3.3: Add `enigma/query.py` (run_life_query), POST /api/query and /api/query/voice

### Brief-to-Query Handoff (P2)

- [x] FR-3.4: "Ask follow-up" link in Brief
- [x] FR-3.4: Opens Life Query with Brief context pre-loaded

---

## Epic 4: Action Sphere UI (MVP)

### Web Action Sphere (MVP)

- [x] FR-4.1: Central orb — tap = Open Commitments (scroll to feed), long-press = Life Query placeholder
- [x] FR-4.2: Milan Minimalism theme — #050505 bg, glassmorphism, Electric Cerulean accent
- [x] FR-4.3: Zero-UI — minimal chrome, content-driven feed
- [x] FR-4.4: Audio button for Manual Commitment / Audio Summary (Commitment vs People context)
- [x] FR-4.1: Fetch Open Commitments from backend (GET /api/commitments)
- [x] FR-4.1: Gesture routing (tap vs long-press)

### Backend for UI

- [x] REST API for commitments, push (GET /api/commitments, POST /api/commitment)
- [x] Auth: Supabase Auth for future multi-user (optional for MVP single-user)

### Flutter / FlutterFlow (optional later)

- [ ] Port Action Sphere to Flutter/FlutterFlow for native mobile

---

## Epic 5: Thought Memory & Audio Thought Capture (Post-MVP)

- [x] FR-5.1: Audio tap → "Thought" vs "Commitment" choice (or LLM auto-classify)
- [x] FR-5.2: Thoughts stored with Sovereign Tag `thought`
- [x] FR-5.3: LLM stitching job (weekly) — themes, links, suggested actions
- [x] FR-5.4: Sovereign Brief section "Thoughts worth revisiting"

---

## Epic 6: Grandma's Closet (Post-MVP)

- [x] FR-6.1: Store deferred ideas with Sovereign Tag `grandmas-closet`
- [x] FR-6.2: UX: "Act now or save to Grandma's Closet?" after thought capture
- [x] FR-6.3: Weekly Grandma's Closet digest
- [x] FR-6.4: Life Query: "What's in my Grandma's Closet?"

---

## Epic 7: User View (Web Dashboard) (Post-MVP)

- [x] FR-7.1: Web app — Dashboard, Thoughts, Commitments, Conversations, Grandma's Closet
- [x] FR-7.2: Brief archive + Life Query history
- [x] FR-7.3: Import Chat section — file picker for .txt (WhatsApp) / JSON (Telegram)

---

## Epic 8: Chat Import (Post-MVP)

- [x] FR-8.1: WhatsApp .txt parser — `[DD/MM/YYYY, HH:MM:SS] Sender: Message`
- [x] FR-8.1: Extract contact from filename, dedupe, LLM summarize → Nexus `people-context`
- [x] FR-8.2: Re-import: merge existing summary + new messages → single refreshed entry
- [x] FR-8.3: Telegram export parser (JSON/HTML/TXT)
- [ ] FR-8.4: Optional: Telegram Takeout API AutoCapture
- [x] FR-8.5: Optional: "Remind me to export WhatsApp" in Brief

---

## Epic 9: Recommendation Governance & Adaptive Planning (Post-MVP)

- [ ] FR-9.1: Recommendation Inbox with explicit actions (`Accept`, `Modify`, `Defer`, `Reject`)
- [ ] FR-9.2: Recommendation receipts (source trace, confidence, expected impact)
- [ ] FR-9.3: Commitment Compiler from Gmail/Telegram/WhatsApp/voice/calendar
- [ ] FR-9.4: Probabilistic due-date estimation with confidence bands
- [ ] FR-9.5: Noise pruning via decision-value thresholds
- [ ] FR-9.6: Mode-based recommendation aggressiveness (Focus/Routine/Recovery/Crisis)

---

## Epic 10: Health-Adaptive Cognitive Ops (Post-MVP)

- [ ] FR-10.1: Apple Health / Google Fit / wearable integrations with explicit opt-in
- [ ] FR-10.2: Health-informed planning as recommendations (no forced schedule changes)
- [ ] FR-10.3: Vital-state work modes (`Deep`, `Collaborative`, `Admin`, `Recovery`)
- [ ] FR-10.4: Burnout-risk detection + preventive intervention playbooks
- [ ] FR-10.5: Recovery-first rescheduling + stakeholder communication drafts
- [ ] FR-10.6: Health guardrails (non-clinical framing and policy boundaries)

---

## Epic 11: Trust, Compliance & Enterprise Readiness (Post-MVP)

- [ ] FR-11.1: Policy-as-code checks for all AI recommendations/actions
- [ ] FR-11.2: Evidence ledger for provenance of suggestions and outcomes
- [ ] FR-11.3: "Red Team My Memory" audit mode with quarantine for unverifiable items
- [ ] FR-11.4: Zero-trust context access controls
- [ ] FR-11.5: Delegation and approval chains for high-risk actions
- [ ] FR-11.6: Hybrid deployment options (cloud/private VPC/on-prem/regional)

---

## Epic 12: Premium UI/UX System (Web + Mobile) (Post-MVP)

- [ ] FR-12.1: Define and implement premium design thesis (enterprise trust + human warmth)
- [ ] FR-12.2: Typography system: `Sohne` UI + `Tiempos Text` accents (section headers, key cards)
- [ ] FR-12.3: Warm-neutral tokenized color system (stone/ink + subtle copper/gold accents)
- [ ] FR-12.4: Dual-mode parity (light and dark are equal-quality and production-grade)
- [ ] FR-12.5: Refined motion grammar across primary interactions (180-240ms)
- [ ] FR-12.6: Web contextual pane shell (focus center + collapsible intelligence side pane)
- [ ] FR-12.7: Mobile shell with bottom tabs + persistent floating capture/action button
- [ ] FR-12.8: Recommendation interaction pattern (`Accept` / `Edit` / `Defer`) across web/mobile
- [ ] FR-12.9: Responsive QA across desktop/tablet/mobile breakpoints
- [ ] FR-12.10: UI consistency/accessibility quality gates for enterprise-ready UX

---

## Epic 13: Web & Mobile Flow (Mode-Based Shell) (Post-MVP)

- [ ] FR-13.1: Define Flow-mode web screen inventory and navigation (WF-1–WF-8) as per [docs/prd/epics/epic-13-web-mobile-flow.md](docs/prd/epics/epic-13-web-mobile-flow.md).
- [ ] FR-13.2: Define Control-mode web screen inventory and navigation (WC-1–WC-11) as per [docs/prd/epics/epic-13-web-mobile-flow.md](docs/prd/epics/epic-13-web-mobile-flow.md).
- [ ] FR-13.3: Define mobile shell structure (tabs, mode toggle, capture FAB) and mobile screen stacks (MH-1–MMORE-3) as per [docs/prd/epics/epic-13-web-mobile-flow.md](docs/prd/epics/epic-13-web-mobile-flow.md).
- [ ] FR-13.4: Map all FR-13.x screens to existing epics (4, 7, 9, 10, 11, 12) and update design/implementation owners.
- [ ] FR-13.5: Produce Figma screen list and flow diagrams corresponding to the Epic 13 inventory (web + mobile), ready for detailed UI design under Epic 12.

---

## Cross-Cutting

### DevOps & Ops

- [x] CRON setup for Sovereign Brief (09:00)
- [x] Logging (structured, env-based level)
- [ ] Error handling + alerting (optional for MVP)

### Documentation

- [x] README with quickstart, env setup, run instructions
- [x] API docs (if REST layer added)

---

## Suggested Order (Next Steps)

1. **Epic 12 (FR-12.1/12.2/12.3/12.6):** Design system baseline + typography/tokens + contextual pane shell
2. **Epic 12 (FR-12.4/12.5/12.7/12.8/12.9):** Dual-mode polish + motion system + mobile shell + recommendation interaction + responsive QA
3. **Epic 9 (FR-9.1/9.2/9.5):** Recommendation Inbox + receipts + noise pruning
4. **Epic 9 (FR-9.3/9.4):** Commitment Compiler + confidence-based due dates
5. **Epic 11 (FR-11.1/11.2):** Policy checks + evidence ledger for recommendation actions
6. **Epic 10 (FR-10.1/10.2):** Health connectors (opt-in) + recommendation-only health adaptation
7. **Epic 10 (FR-10.3/10.4/10.5):** Vital-state modes + burnout prevention + recovery rescheduler
8. **Epic 11 (FR-11.3/11.4/11.5/11.6):** Red-team audits + zero-trust + approvals + enterprise deployment modes
