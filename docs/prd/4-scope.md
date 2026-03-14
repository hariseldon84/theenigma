# 4. Scope

## 4.1 In Scope (MVP — 72 hours)

| Area | Scope |
|------|-------|
| **Memory** | Notion (The Nexus) + Supabase (The Vault) + Python orchestration |
| **Ingestion** | Omni-Scribe (window titles + clipboard → Notion every 15 min) |
| **Synthesis** | Sovereign Brief (LLM, CRON 09:00, Email + Telegram) |
| **UI** | Action Sphere (orb, Open Commitments feed, Milan Minimalism) |
| **Capture** | Manual Commitment (one-tap audio → Nexus) |
| **Query** | Life Query (orb long-press → voice → RAG → answer) — if time permits |

## 4.2 Post-MVP / Roadmap (Post 72h)

| Area | Scope |
|------|-------|
| **Thought Memory** | Thought capture via audio; LLM stitching; "Thoughts worth revisiting" in Brief |
| **Grandma's Closet** | Someday/maybe storage; audio "idea but not now"; weekly digest |
| **User View (Web Dashboard)** | Dashboard, Thoughts, Commitments, Conversations & Summaries, Grandma's Closet, Brief archive, Life Query history |
| **Chat Import (WhatsApp)** | Manual export + import; "Import Chat" in web; parser + dedupe; re-import updates latest context (no auto-append) |
| **Chat Import (Telegram)** | Manual export + import; or AutoCapture via Takeout API (user auth once, periodic sync) |
| **Recommendation Governance** | Recommendation Inbox (Accept/Modify/Defer/Reject), explainability receipts, noise-pruned suggestion delivery |
| **Health-Adaptive Cognitive Ops** | Apple Health/Google Fit opt-in connectors; health-informed recommendation-only scheduling with guardrails |
| **Trust & Enterprise Readiness** | Policy-as-code checks, evidence ledger, zero-trust context access, enterprise deployment options |

## 4.3 Out of Scope (MVP)

| Area | Deferred |
|------|----------|
| Comm-Mirror (real-time) | Replaced by Audio Summary Bridge + Chat Import |
| Always-on Ambient Awareness | Replaced by Manual Commitment Capture |
| Proactive Draft Engine | Post-MVP |
| Digital Bodyguard (Whisper Vault, Cyber-Sentinel, Stealth Lock) | Post-MVP |
| Legacy & Life Continuity | Post-MVP |

## 4.4 Constraints

- **Tech stack:** Notion + Supabase + Python Desktop Sentinel (fixed); LLM (Claude/GPT preferred); UI (FlutterFlow/Flutter)
- **Design:** Milan Minimalism (Obsidian Black #050505, Titanium White, Electric Cerulean, Liquid Glass, Zero-UI)
- **Timeline:** 72-hour MVP target

---
