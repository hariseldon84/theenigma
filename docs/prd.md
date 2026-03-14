# Enigma OS — Product Requirements Document

**Version:** 0.3  
**Date:** 2026-03-10  
**Status:** Draft  
**Source:** basicidea.md, brainstorming-session-2026-03-10.md, mvp-roadmap.md

---

## 1. Product Overview

### 1.1 Vision

Enigma OS is a **Sovereign-Edge Cognitive Operating System** — a digital "exoskeleton" for the mind that acts as an ambient, proactive intelligence layer. It addresses "Information Debt": the gap between vast amounts of owned data (emails, chats, documents) and the ability to retrieve or act upon it in real-time.

### 1.2 Problem Statement

- Current AI tools are reactive and broad, lacking specific personal context
- Professionals own data across many sources but cannot query or act on it in real-time
- Commitments and sensitive assets are scattered and not organized or actionable automatically

### 1.3 Solution Summary

Enigma OS moves beyond the traditional "App" model into an integrated OS layer that:
- Indexes a lifetime of data via local/private cloud storage
- Uses RAG and autonomous agentic workflows
- Ensures every commitment and sensitive asset is organized and actionable automatically
- Acts as a "Sovereign Proxy" that anticipates needs and protects sensitive assets

---

## 2. Key Concepts (In Depth)

### 2.1 Information Debt

**Information Debt** is the gap between the data you *own* and your ability to *retrieve or act upon it* in real-time. It is the central problem Enigma OS exists to solve.

**What it looks like in practice:**
- You have years of emails, chats, documents, and notes — but no unified way to ask "What did I promise Sarah about the Q2 launch?" or "Where did I save that contract clause?"
- You make commitments in meetings, DMs, and calls — but they live in silos. You can't see "everything I owe" in one place.
- You switch between tools (Slack, Notion, Figma, email) — but there is no continuous thread of *what you were doing* that an AI can use for context.
- Current AI assistants are **reactive** (you must ask) and **broad** (trained on public data, not your personal corpus). They lack the specific, private context that would make them truly useful.

**Analogy:** Like technical debt, but for information. You accumulate data over time; without structure and retrieval, it becomes a liability. The "interest" you pay is time spent searching, forgotten commitments, and missed follow-ups.

**Enigma's approach:** Index what you own, structure it (The Nexus), and make it queryable (Life Query) and synthesizable (Sovereign Brief). Reduce the gap between owning data and acting on it.

---

### 2.2 Omni-Scribe (Desktop Sentinel)

**Omni-Scribe** is a background service — the "Desktop Sentinel" — that samples your active work environment to build a **Transient Memory** stream. It runs locally, captures low-fidelity but high-signal context, and pushes it to The Nexus every 15 minutes.

**What it captures:**
- **Active window titles** — Which app and which document/page you're focused on (e.g., "Figma - Landing Page v3", "Slack - #product", "Notion - Q2 Roadmap")
- **Clipboard contents** — What you've copied (snippets, links, text) as a proxy for what you're working with or sharing

**What it does *not* capture (by design):**
- Screen content, keystrokes, or full document text — to minimize privacy risk and complexity
- Real-time streaming — it batches and pushes every 15 min to balance freshness with API load and user privacy

**Why it matters:**
- **Context for Life Query:** "What was I working on yesterday?" → Omni-Scribe logs show your window/clipboard history.
- **Context for Sovereign Brief:** The LLM receives your recent activity to infer priorities and open threads.
- **Context for future features:** Proactive Draft Engine, research init, and other "Enigma knows what you're doing" features depend on this stream.

**MVP implementation:** Python script that polls active window (via platform APIs) and clipboard, formats as Knowledge Nuggets with Sovereign Tag `transient`, and pushes to Notion via the orchestration layer. Optional: basic vulnerability scan (OS patches, exposed `.env`) as a lightweight Cyber-Sentinel precursor.

---

### 2.3 Milan Minimalism — Design Goal

**Milan Minimalism** is the design language for Enigma OS. Its goal is **"Invisible Luxury"** — a digital experience that feels like an extension of a premium physical object, not a cluttered app.

**Core principles:**

| Principle | Meaning |
|-----------|---------|
| **Invisible Luxury** | The interface recedes; the content and intelligence feel present. Like a high-end watch: you notice the quality, not the UI. |
| **Obsidian Black (#050505)** | Deep, rich black as the primary background. Reduces visual noise and creates a calm, focused environment. |
| **Titanium White + Electric Cerulean** | White for text; a single accent color (Electric Cerulean) for active states, CTAs, and highlights. Restraint in color = clarity. |
| **Liquid Glass** | Elements use ~80% backdrop blur. Cards and panels feel layered and depth-heavy, not flat. Sophisticated, tactile. |
| **Zero-UI** | No traditional menus, sidebars, or chrome. Information fades in and out based on importance. The orb is the primary entry point; content appears when needed and disappears when not. |
| **Typography** | Bold, high-contrast San Francisco or Inter. Readable in low-light; confident, not timid. |

**Why it matters for Enigma:**
- **Cognitive load:** A busy professional doesn't need another noisy app. Milan Minimalism keeps the interface quiet so the *intelligence* (Brief, Commitments, Life Query) stands out.
- **Differentiation:** Most productivity tools are cluttered. Enigma aims to feel like a premium, focused instrument.
- **Trust:** A restrained, high-quality aesthetic signals that the product takes your data and attention seriously.

---

### 2.4 Thought Memory — Interweaving Layer

**Thought Memory** is a separate memory layer for reflective, generative, exploratory ideas — distinct from commitments (action-oriented) and nuggets (facts). Thoughts build over time; the system "stitches" them to find themes, link related thoughts, and suggest "Thought A + Thought B → possible action?"

**Key behaviors:**
- **Storage:** Nexus with Sovereign Tag `thought` (or dedicated database)
- **Stitching:** LLM periodically analyzes thought corpus; finds themes, links, suggests actions
- **Surfacing:** Sovereign Brief includes "Thoughts worth revisiting"; Life Query: "What have I been thinking about lately?"
- **Unique value:** Active synthesis layer — turns scattered reflections into coherent insights and suggested actions

**Capture:** Same audio tap as commitments; user selects "Thought" or LLM auto-classifies. Thoughts route to Thought Memory.

---

### 2.5 Grandma's Closet

**Grandma's Closet** is a "someday/maybe" store for ideas that are good but you don't want to act on now. System or user decides via audio ("I have an idea but not now") or manual move from Nexus/Thoughts.

**Key behaviors:**
- **Population:** Audio capture, manual move, or system suggestion ("This thought might belong in Grandma's Closet")
- **Review:** Weekly digest — "Here are ideas you saved for later." User can promote to action
- **Life Query:** "What's in my Grandma's Closet?"
- **Sovereign Tag:** `grandmas-closet`

---

## 3. Goals

### 3.1 Product Goals

| ID | Goal | Success Metric |
|----|------|----------------|
| G1 | Reduce Information Debt | User can ask "What do I owe?" and get an accurate answer in &lt;30s |
| G2 | Surface Open Commitments daily | Sovereign Brief delivered by 09:00 with priorities and commitments |
| G3 | Capture context without friction | Omni-Scribe + Manual Capture feed The Nexus with minimal user effort |
| G4 | Enable natural-language query over personal data | Life Query returns relevant answers from Nexus + Omni-Scribe + Commitments |
| G5 | Capture thoughts and defer ideas | Thought Memory + Grandma's Closet; audio capture for both |
| G6 | Provide unified view of all data | User View (Web Dashboard) with Thoughts, Commitments, Conversations, Grandma's Closet |
| G7 | Ingest WhatsApp/Telegram for People Context | Manual import (WhatsApp); AutoCapture (Telegram via Takeout API) |

### 3.2 Business Goals

| ID | Goal |
|----|------|
| B1 | Validate core value prop (commitment tracking + query) within 72-hour MVP |
| B2 | Establish Milan Minimalism as differentiated design language |
| B3 | Prove tech stack (Notion + Supabase + Python + FlutterFlow + LLM) for rapid iteration |

---

## 4. Scope

### 4.1 In Scope (MVP — 72 hours)

| Area | Scope |
|------|-------|
| **Memory** | Notion (The Nexus) + Supabase (The Vault) + Python orchestration |
| **Ingestion** | Omni-Scribe (window titles + clipboard → Notion every 15 min) |
| **Synthesis** | Sovereign Brief (LLM, CRON 09:00, Email + Telegram) |
| **UI** | Action Sphere (orb, Open Commitments feed, Milan Minimalism) |
| **Capture** | Manual Commitment (one-tap audio → Nexus) |
| **Query** | Life Query (orb long-press → voice → RAG → answer) — if time permits |

### 4.2 Post-MVP / Roadmap (Post 72h)

| Area | Scope |
|------|-------|
| **Thought Memory** | Thought capture via audio; LLM stitching; "Thoughts worth revisiting" in Brief |
| **Grandma's Closet** | Someday/maybe storage; audio "idea but not now"; weekly digest |
| **User View (Web Dashboard)** | Dashboard, Thoughts, Commitments, Conversations & Summaries, Grandma's Closet, Brief archive, Life Query history |
| **Chat Import (WhatsApp)** | Manual export + import; "Import Chat" in web; parser + dedupe; re-import updates latest context (no auto-append) |
| **Chat Import (Telegram)** | Manual export + import; or AutoCapture via Takeout API (user auth once, periodic sync) |

### 4.3 Out of Scope (MVP)

| Area | Deferred |
|------|----------|
| Comm-Mirror (real-time) | Replaced by Audio Summary Bridge + Chat Import |
| Always-on Ambient Awareness | Replaced by Manual Commitment Capture |
| Proactive Draft Engine | Post-MVP |
| Digital Bodyguard (Whisper Vault, Cyber-Sentinel, Stealth Lock) | Post-MVP |
| Legacy & Life Continuity | Post-MVP |

### 4.4 Constraints

- **Tech stack:** Notion + Supabase + Python Desktop Sentinel (fixed); LLM (Claude/GPT preferred); UI (FlutterFlow/Flutter)
- **Design:** Milan Minimalism (Obsidian Black #050505, Titanium White, Electric Cerulean, Liquid Glass, Zero-UI)
- **Timeline:** 72-hour MVP target

---

## 5. Functional Requirements

### 5.1 Epic 1: Memory Foundation

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-1.1 | The Nexus (Notion) stores Knowledge Nuggets with Context, Content, Priority, Sovereign Tag | P0 | Create/query nuggets via API; properties match schema |
| FR-1.2 | The Vault (Supabase) stores encrypted sensitive data | P0 | Insert/query vault table; AES-256 at app layer |
| FR-1.3 | Python orchestration bridges Notion and Supabase | P0 | Health check passes; push/query work |

### 5.2 Epic 2: Ambient Ingestion

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-2.1 | Omni-Scribe captures active window titles and clipboard | P0 | Logs pushed to Notion every 15 min |
| FR-2.2 | Manual Commitment Capture records audio and pushes to Nexus | P1 | One-tap record → transcribe → Notion with Sovereign Tag |
| FR-2.3 | Audio Summary Bridge allows user to speak chat/people context | P2 | Audio → transcribe → Nexus as People Context |

### 5.3 Epic 3: Strategic Executive Proxy

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-3.1 | Sovereign Brief synthesizes last 24h of Nexus + Open Commitments | P0 | CRON 09:00; delivered via Email + Telegram |
| FR-3.2 | Open Commitments displayed at top of Action Sphere feed | P0 | Items with Sovereign Tag "commitment" shown first |
| FR-3.3 | Life Query answers natural-language questions from Nexus + Omni-Scribe + Commitments | P1 | Orb long-press → voice input → RAG → answer card |
| FR-3.4 | Brief-to-Query Handoff: "Ask follow-up" in Brief opens Life Query with context | P2 | Link in Brief → Life Query pre-loaded |

### 5.4 Epic 4: Action Sphere UI

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-4.1 | Central orb with tap = Open Commitments, long-press = Life Query | P0 | Gesture routing works; Milan Minimalism applied |
| FR-4.2 | Milan Minimalism: #050505 bg, glassmorphism, Electric Cerulean accent | P0 | Theme matches spec |
| FR-4.3 | Zero-UI: information fades by importance; no traditional menus | P0 | Minimal chrome; content-driven |
| FR-4.4 | Audio button for Manual Commitment and Audio Summary | P1 | Single entry; intent inferred or user choice |

### 5.5 Epic 5: Thought Memory & Audio Thought Capture

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-5.1 | Audio tap can capture thoughts (not just commitments) | P2 | User selects "Thought" or LLM auto-classifies; thoughts route to Thought Memory |
| FR-5.2 | Thought Memory stores thoughts with Sovereign Tag `thought` | P2 | Thoughts queryable; Life Query: "What have I been thinking about lately?" |
| FR-5.3 | LLM periodically stitches thoughts — themes, links, suggested actions | P3 | Weekly job; surfaces "Thought A + B → possible action?" |
| FR-5.4 | Sovereign Brief includes "Thoughts worth revisiting" | P3 | Brief section for thoughts not yet acted on |

### 5.6 Epic 6: Grandma's Closet

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-6.1 | Grandma's Closet stores deferred ideas with Sovereign Tag `grandmas-closet` | P2 | User can save "idea but not now" via audio or manual move |
| FR-6.2 | After capturing thought, prompt "Act now or save to Grandma's Closet?" | P2 | UX in orb flow and web dashboard |
| FR-6.3 | Weekly Grandma's Closet digest | P3 | "Here are ideas you saved for later"; optional "Promote to action?" |
| FR-6.4 | Life Query: "What's in my Grandma's Closet?" | P2 | RAG over Grandma's Closet entries |

### 5.7 Epic 7: User View (Web Dashboard)

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-7.1 | Web dashboard with Dashboard, Thoughts, Commitments, Conversations & Summaries, Grandma's Closet | P2 | Milan Minimalism; auth via Supabase |
| FR-7.2 | Brief archive and Life Query history | P2 | User can review past Briefs and queries |
| FR-7.3 | Import Chat section for WhatsApp/Telegram upload | P2 | File picker; upload .txt (WhatsApp) or JSON (Telegram) |

### 5.8 Epic 8: Chat Import (WhatsApp & Telegram)

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-8.1 | Parse WhatsApp .txt export (format: `[date] sender: message`) | P2 | Extract contact from filename; create Nexus entries with People Context |
| FR-8.2 | On re-import: do NOT auto-append — LLM updates latest context for that contact | P2 | One canonical entry per contact; existing summary + new messages → single refreshed summary |
| FR-8.3 | Parse Telegram export (JSON/HTML/TXT) | P2 | Same flow as WhatsApp; map to Nexus |
| FR-8.4 | Optional: Telegram AutoCapture via Takeout API | P3 | User auth once; periodic sync to Nexus |
| FR-8.5 | Optional: "Remind me to export WhatsApp" in Sovereign Brief weekly | P3 | Brief includes reminder; links to Import Chat |

**Chat Import workflow (WhatsApp):**
- User exports chat in WhatsApp (Chat → Export Chat → Without Media) → `.txt`
- Format: `[DD/MM/YYYY, HH:MM:SS] Sender: Message`
- User uploads in Enigma Web → Import Chat → Parser extracts contact from filename, dedupes → LLM summarizes → Nexus with `people-context` tag
- **Re-import:** Do not append. LLM receives existing summary + new messages → single refreshed summary; overwrite Nexus entry for that contact

**Chat Import workflow (Telegram):**
- Manual: Export via Telegram Desktop → upload JSON/HTML/TXT → same flow as WhatsApp
- AutoCapture (optional): User auth via Takeout API once → periodic sync to Nexus

### 5.9 Epic 9: Recommendation Governance & Adaptive Planning

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-9.1 | Recommendation Inbox with explicit actions (`Accept`, `Modify`, `Defer`, `Reject`) | P1 | All suggestions appear in one queue with user decision controls |
| FR-9.2 | Recommendation receipts (source trace, confidence, expected impact) | P1 | Each suggestion includes explainability metadata |
| FR-9.3 | Commitment Compiler builds daily task packages from integrations + voice | P1 | Task groups include owner, due date/confidence, dependency links |
| FR-9.4 | Probabilistic due-date estimation with confidence bands | P2 | Tasks show date + confidence range |
| FR-9.5 | Noise pruning via decision-value thresholds | P1 | Low-value recommendations are batched/summarized |
| FR-9.6 | Mode-based recommendation aggressiveness (Focus/Routine/Recovery/Crisis) | P2 | Suggestion intensity adapts to user mode |

### 5.10 Epic 10: Health-Adaptive Cognitive Ops

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-10.1 | Integrate Apple Health / Google Fit / supported wearables (opt-in) | P2 | User can connect health sources with explicit consent |
| FR-10.2 | Health-informed planning remains recommendation-only by default | P1 | No forced schedule/task changes without user approval |
| FR-10.3 | Vital-state work modes (`Deep`, `Collaborative`, `Admin`, `Recovery`) | P2 | Prioritization and prompt cadence adapt by mode |
| FR-10.4 | Burnout-risk detection and preventive playbooks | P2 | Enigma flags overload and proposes mitigation options |
| FR-10.5 | Recovery-first rescheduling + stakeholder communication drafts | P2 | Health/workload signal can trigger safe re-plan recommendations |
| FR-10.6 | Health guardrails (non-clinical framing and policy limits) | P1 | Product avoids medical claims outside certified modules |

### 5.11 Epic 11: Trust, Compliance & Enterprise Readiness

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-11.1 | Policy-as-code checks for all AI recommendations/actions | P1 | Runtime policy evaluation enforced before execution |
| FR-11.2 | Evidence ledger for AI actions and recommendation outcomes | P1 | Every action has traceable provenance |
| FR-11.3 | "Red Team My Memory" audit mode | P2 | User/admin can challenge outputs and quarantine unverifiable items |
| FR-11.4 | Zero-trust context access model | P1 | Sensitive context access requires verified identity and posture |
| FR-11.5 | Delegation and approval chains by risk tier | P2 | High-risk actions require configurable approvals |
| FR-11.6 | Hybrid deployment options (cloud/private VPC/on-prem/regional) | P2 | Deployment choices support compliance/data residency |

---

## 6. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Sovereign Brief delivery | By 09:00 daily |
| NFR-2 | Omni-Scribe push interval | Every 15 min |
| NFR-3 | Life Query response time | &lt;30s (LLM + RAG) |
| NFR-4 | Data residency | Notion + Supabase (user-controlled) |
| NFR-5 | Privacy | No auto-send; human-in-loop for drafts |

---

## 7. User Stories (MVP)

### 7.1 Morning Flow

| ID | Story | Acceptance |
|----|-------|------------|
| US-1 | As a user, I receive a Sovereign Brief by 09:00 so I know my priorities and Open Commitments | Brief in Email + Telegram |
| US-2 | As a user, I can tap "Ask follow-up" in the Brief to ask a clarifying question | Life Query opens with Brief context |

### 7.2 Commitment Flow

| ID | Story | Acceptance |
|----|-------|------------|
| US-3 | As a user, I can tap the orb to see my Open Commitments | Commitments at top of feed |
| US-4 | As a user, I can record a verbal commitment with one tap | Audio → Nexus with Sovereign Tag |

### 7.3 Query Flow

| ID | Story | Acceptance |
|----|-------|------------|
| US-5 | As a user, I can long-press the orb and ask "What do I owe?" | Answer from Nexus + Commitments |
| US-6 | As a user, I can ask "What was I working on yesterday?" | Answer from Omni-Scribe logs |

### 7.4 Capture Flow

| ID | Story | Acceptance |
|----|-------|------------|
| US-7 | As a user, I can speak a summary of a chat into the app | Audio Summary → Nexus (People Context) |

### 7.5 Post-MVP User Stories

| ID | Story | Epic |
|----|-------|------|
| US-8 | As a user, I want to capture thoughts via audio and have them stored separately from commitments | Thought Memory |
| US-9 | As a user, I want Enigma to surface themes across my thoughts and suggest actions | Thought Memory |
| US-10 | As a user, I want to save "someday/maybe" ideas without committing now | Grandma's Closet |
| US-11 | As a user, I want a weekly digest of ideas I saved for later | Grandma's Closet |
| US-12 | As a user, I want a web dashboard to see Thoughts, Commitments, Conversations, Grandma's Closet | User View |
| US-13 | As a user, I want to review past Briefs and Life Query history | User View |
| US-14 | As a user, I want to import WhatsApp chat exports so Enigma adds People Context to Nexus | Chat Import |
| US-15 | As a user, I want re-imports to update my existing context for that contact, not duplicate | Chat Import |
| US-16 | As a user, I want to import Telegram exports or auto-sync via Takeout | Chat Import |
| US-17 | As a user, I want Enigma suggestions in one inbox where I can Accept, Modify, Defer, or Reject | Recommendation Governance |
| US-18 | As a user, I want to see source and confidence for each suggestion before deciding | Recommendation Governance |
| US-19 | As a user, I want low-value interruptions suppressed and summarized | Recommendation Governance |
| US-20 | As a user, I want health-informed scheduling recommendations from opt-in health signals | Health-Adaptive Cognitive Ops |
| US-21 | As a user, I want health-based changes to remain recommendations, not forced actions | Health-Adaptive Cognitive Ops |
| US-22 | As a team admin, I want all AI actions to be policy-checked and auditable | Trust/Compliance/Enterprise |
| US-23 | As an enterprise user, I want approval chains for high-risk agent actions | Trust/Compliance/Enterprise |

---

## 8. UX Flows (Reference)

| State | Entry | Action | Outcome |
|-------|-------|--------|---------|
| Morning | Brief | Read → Ask follow-up | Life Query from brief context |
| Context switch | Orb long-press | Ask "What was I doing?" | Answer → Save or dismiss |
| Commitment moment | Audio button | Record commitment | → Nexus, Open Commitments |
| Reply needed | Orb / notification | Draft → Approve | Reply sent (post-MVP) |
| Chat summary | Audio button | Summarize people context | → Nexus |
| Thought capture | Audio button | Select "Thought" or auto-classify | → Thought Memory |
| Idea deferral | After thought / manual | "Save to Grandma's Closet?" | → Grandma's Closet |
| Chat import | Web Import Chat | Upload .txt (WhatsApp) or JSON (Telegram) | → Nexus People Context |
| Re-import | Same contact | LLM merges new + existing summary | Single refreshed entry |
| Deep work | (minimal) | Orb available but quiet | No interruption |

---

## 9. Dependencies & References

| Document | Purpose |
|----------|---------|
| `basicidea.md` | Original vision, four pillars, design inspiration |
| `docs/brainstorming-session-2026-03-10.md` | Constraint mapping, feature ideas, UX flows |
| `bmad_output/brainstorming/brainstorming-session-2026-03-13-194750.md` | Expanded ideation and strategic tracks for Epics 9–11 |
| `docs/mvp-roadmap.md` | Build order, priority tiers |
| `docs/setup-phase1.md` | Notion + Supabase setup |

---

## 10. Open Questions

1. **LLM choice:** Claude 3.5 Sonnet vs GPT-4o vs Gemini — final decision for Sovereign Brief and Life Query?
2. **FlutterFlow vs Flutter native:** For custom gestures and Zero-UI depth?
3. **Speech-to-text:** Which service for Manual Commitment and Audio Summary (Whisper, Google, other)?

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-03-10 | Product (BMAD-style) | Initial PRD from brainstorming + MVP roadmap |
| 0.2 | 2026-03-10 | Product | Added in-depth sections: Information Debt, Omni-Scribe, Milan Minimalism |
| 0.3 | 2026-03-10 | Product | Added Thought Memory (2.4), Grandma's Closet (2.5); Epics 5–8; Post-MVP scope; Chat Import workflow; User View; UX flows |
| 0.4 | 2026-03-14 | Product | Added Epics 9–11 (Recommendation Governance, Health-Adaptive Ops, Trust/Compliance/Enterprise) and related user stories/dependencies |
