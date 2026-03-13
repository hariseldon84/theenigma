# 2. Key Concepts (In Depth)

## 2.1 Information Debt

**Information Debt** is the gap between the data you *own* and your ability to *retrieve or act upon it* in real-time. It is the central problem Enigma OS exists to solve.

**What it looks like in practice:**
- You have years of emails, chats, documents, and notes — but no unified way to ask "What did I promise Sarah about the Q2 launch?" or "Where did I save that contract clause?"
- You make commitments in meetings, DMs, and calls — but they live in silos. You can't see "everything I owe" in one place.
- You switch between tools (Slack, Notion, Figma, email) — but there is no continuous thread of *what you were doing* that an AI can use for context.
- Current AI assistants are **reactive** (you must ask) and **broad** (trained on public data, not your personal corpus). They lack the specific, private context that would make them truly useful.

**Analogy:** Like technical debt, but for information. You accumulate data over time; without structure and retrieval, it becomes a liability. The "interest" you pay is time spent searching, forgotten commitments, and missed follow-ups.

**Enigma's approach:** Index what you own, structure it (The Nexus), and make it queryable (Life Query) and synthesizable (Sovereign Brief). Reduce the gap between owning data and acting on it.

---

## 2.2 Omni-Scribe (Desktop Sentinel)

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

## 2.3 Milan Minimalism — Design Goal

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

## 2.4 Thought Memory — Interweaving Layer

**Thought Memory** is a separate memory layer for reflective, generative, exploratory ideas — distinct from commitments (action-oriented) and nuggets (facts). Thoughts build over time; the system "stitches" them to find themes, link related thoughts, and suggest "Thought A + Thought B → possible action?"

**Key behaviors:**
- **Storage:** Nexus with Sovereign Tag `thought` (or dedicated database)
- **Stitching:** LLM periodically analyzes thought corpus; finds themes, links, suggests actions
- **Surfacing:** Sovereign Brief includes "Thoughts worth revisiting"; Life Query: "What have I been thinking about lately?"
- **Unique value:** Active synthesis layer — turns scattered reflections into coherent insights and suggested actions

**Capture:** Same audio tap as commitments; user selects "Thought" or LLM auto-classifies. Thoughts route to Thought Memory.

---

## 2.5 Grandma's Closet

**Grandma's Closet** is a "someday/maybe" store for ideas that are good but you don't want to act on now. System or user decides via audio ("I have an idea but not now") or manual move from Nexus/Thoughts.

**Key behaviors:**
- **Population:** Audio capture, manual move, or system suggestion ("This thought might belong in Grandma's Closet")
- **Review:** Weekly digest — "Here are ideas you saved for later." User can promote to action
- **Life Query:** "What's in my Grandma's Closet?"
- **Sovereign Tag:** `grandmas-closet`

---
