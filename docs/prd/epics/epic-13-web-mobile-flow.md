# Epic 13: Web & Mobile Flow (Mode-Based Shell)

Define the concrete screen inventory and navigation flows for Enigma’s **mode-based shell** across Web and Mobile, building on Epic 12’s design system. This epic focuses on **what screens exist, what each screen is for, and how they connect** in both Flow and Control modes, with enterprise/team views.

## 13.1 Web Screen Inventory — Flow Mode

| ID | Screen | Purpose |
|----|--------|---------|
| WF-1 | Flow Home (Orb + Today strip) | Default home in Flow mode; central orb with a "Now" strip (top commitments + key recommendations) and a "Next" teaser into the Today Board. Primary entry point for tap/long-press orb interactions and capture FAB. |
| WF-2 | Today Board | Focused view of "Must today", "Should this week", and "Inbox" lanes that combine Open Commitments and recommendation cards with `Accept / Edit / Defer / Reject` controls. Supports view toggle for `My / Team / Org` where permissions allow. |
| WF-3 | Life Query Panel (overlay) | Lightweight overlay opened via long-press on the orb to ask quick natural-language questions, see answers, and optionally convert them into commitments, thoughts, or people-context items without leaving the Flow Home context. |
| WF-4 | Life Query Full View | Full-screen query workspace showing richer answers with source traces, pinned queries, and side context (last brief snippet, related people-context, relevant Grandma’s Closet items). Enables promoting answers into tasks or thoughts and pinning to the Today Board. |
| WF-5 | Capture Overlay | Cross-cutting overlay accessible from the capture FAB to record audio or text for `Commitment`, `People context`, or `Thought`. Shows live destination preview (where the item will land) and offers quick tagging (project/person/timeframe). |
| WF-6 | Flow Inbox Slice | Slim, high-signal view of the Recommendation Inbox accessible from Flow Home (e.g., swipe or icon). Surfaces only the most important recommendation cards without switching into full Control-mode governance views. |
| WF-7 | Flow Scene View (optional) | Project- or theme-centric cluster view (e.g., "Q2 Launch") aggregating related commitments, thoughts, people-context, recent queries, and relevant brief snippets into a single "scene" for deep work blocks. |
| WF-8 | Flow Timeline Strip (optional) | Compact visual history of recent Omni-Scribe pulses (window titles + clipboard snapshots) rendered as a horizontal strip or timeline under Flow Home to support questions like "What was I doing earlier today?". |

## 13.2 Web Screen Inventory — Control Mode

| ID | Screen | Purpose |
|----|--------|---------|
| WC-1 | Control Home (Workspace Overview) | Landing surface in Control mode summarizing connection health (Notion, Supabase, LLM, Auth), data volumes, recent activity, recommendation system health, and org adoption metrics for the current workspace. |
| WC-2 | Workspaces & Tenancy List | List of workspaces/tenants showing deployment mode (bring-your-own vs Enigma-hosted), region, and status. Entry point for admins to manage multiple workspaces. |
| WC-3 | Workspace Detail & Connections | Detail page for a single workspace, including Notion database mapping, Supabase tables, encryption key configuration, LLM provider selection, and Auth settings. Includes a wizard branch for "Connect your own Notion + Supabase" vs "Use Enigma-managed infrastructure". |
| WC-4 | Memory Explorer | Tabbed explorer over `Thoughts`, `Commitments`, `Conversations`, `Grandma’s Closet`, and `All Nuggets`, with search, filters, and batch actions (promote to commitment, move to closet, merge, link to person, archive). |
| WC-5 | Brief Archive | List + detail view of past Sovereign Briefs showing summary, generated actions, and which actions were accepted/completed. Supports filtering by date, workspace, and owner. |
| WC-6 | Life Query History | History of Life Query sessions with questions, answers, and source context. Allows replay/rehydration, refinement, and conversion into commitments or thoughts. |
| WC-7 | Chat Import & People Context | Management surface for WhatsApp/Telegram imports, including upload/re-upload flows, per-contact status (last import, volume, last summary update), and deep links to People Context entries in the Memory Explorer. |
| WC-8 | Recommendation Governance | Configuration UI for recommendation policies (thresholds, risk bands, mode profiles, allowed actions) plus a timeline of recommendations with evidence, user decisions, and outcomes. Entrypoint for "Red team my memory" audits. |
| WC-9 | Health & Modes Configuration | Configuration for health connectors (Apple Health, wearables) with explicit opt-in and guardrails, and for operational modes (`Deep`, `Collaborative`, `Admin`, `Recovery`) including how they modulate recommendation intensity and interruption patterns. |
| WC-10 | Org & Roles | Org-level admin view for managing users, roles (User, Manager, Admin, Auditor), teams, and which memory domains are shared vs private. May surface team-level commitment and execution views for managers. |
| WC-11 | Settings | Personal and workspace-level settings including profile, notifications, theme appearance, export/delete tools, and security controls. |

## 13.3 Mobile Screen Inventory (Parity-Oriented)

On mobile, Enigma is a **full client** with near-parity flows, adapted into shorter, more linear journeys. A bottom-tab shell with a persistent capture FAB gives access to both Flow and Control behaviors.

### 13.3.1 Global Mobile Structure

| ID | Shell Element | Purpose |
|----|---------------|---------|
| MM-1 | Bottom Tabs | Primary navigation: `Home`, `Inbox`, `Memory`, `Org`, and `More` (exact labels subject to UX copy). Tabs aggregate related screen stacks while keeping the orb Flow entry and Control overviews reachable. |
| MM-2 | Mode Toggle (Flow / Control) | Mode selector (likely surfaced on Home and/or in a global header) that switches the primary default view within tabs between Flow-centric and Control-centric screens without changing the underlying navigation structure. |
| MM-3 | Capture FAB | Persistent floating mic/action button overlaying all tabs, opening a compact capture flow for `Commitment`, `People context`, or `Thought` regardless of current location. |

### 13.3.2 Mobile Tab Stacks

| ID | Screen | Tab | Purpose |
|----|--------|-----|---------|
| MH-1 | Mobile Flow Home | Home | Orb + Now strip on small screens; quick access to top commitments and recommendations plus orb tap/long-press behaviors. Mode toggle present to switch to Control Home overview. |
| MH-2 | Mobile Today Board | Home | Vertical or lightly columnar representation of the Today Board, optimized for thumb reach. Shows Must/Should/Inbox groupings with mixed commitment and recommendation cards. |
| MH-3 | Mobile Life Query Full | Home | Full-screen query experience on mobile (text + voice) with simplified answer context and key actions (create commitment, save as thought, pin). |
| MI-1 | Recommendation & Commitments List | Inbox | Combined list of recommendation and high-priority commitment cards with filters (e.g., by lane, by risk). Tightly scannable for quick triage sessions. |
| MI-2 | Recommendation/Commitment Detail | Inbox | Detail view for a single card showing context (sources, related memory, actions taken) and controls (`Accept / Edit / Defer / Reject`). |
| MMEM-1 | Thoughts List & Detail | Memory | List of Thought Memory entries with search/filter; detail view with related recommendations and actions (promote, link, move to closet). |
| MMEM-2 | Grandma’s Closet List & Detail | Memory | List of closet items; detail view with options to promote to commitment or thought, or leave deferred. |
| MMEM-3 | Conversations & People Context | Memory | People-context summaries stemming from chat imports and audio summaries, with per-person detail and quick links to related commitments. |
| MORG-1 | Org Overview | Org | High-level workspace and org status for admins (connections, health, user count, import health), skewed read-only on small screens with guarded edit affordances. |
| MORG-2 | Workspace Detail (Mobile) | Org | Condensed view of workspace detail and connections, allowing targeted edits (e.g., toggle BYO vs Enigma-hosted, rotate keys) with confirmation flows. |
| MMORE-1 | Brief Archive (Mobile) | More | List + detail of Sovereign Briefs on mobile with focus on reading and asking follow-up via Life Query. |
| MMORE-2 | Query History (Mobile) | More | List of past queries and answers; tap to re-open in Mobile Life Query Full with the previous context. |
| MMORE-3 | Settings (Mobile) | More | Combined personal/workspace settings tuned for mobile (profile, notifications, theme, security). |

## 13.4 Navigation & Mode Relationships

- Flow is the **default operating context**; Control is a first-class, always-available secondary mode, not a separate app.
- On web, a visible **Flow / Control toggle** in the header (plus subtle visual cues) makes mode state clear and switching cheap.
- On mobile, the Home tab and mode toggle coordinate: Flow Home and Control Home share the same tab but different initial surfaces.
- Team/manager views (e.g., `My / Team / Org`) are available in Flow where they aid execution (Today Board, Flow Home) but richer org dashboards and policies live in Control.

## 13.5 Dependencies

- Depends on Epic 4 (Action Sphere UI) for the existing orb, feed, and Life Query primitives.
- Depends on Epic 7 (User View) for basic dashboard sections and memory views.
- Strongly coupled to Epic 9 (Recommendation Governance) for recommendation cards and Inbox semantics.
- Strongly coupled to Epic 12 (Premium UI/UX System) for design tokens, typography, motion, and shell behaviors.

## 13.6 Out of Scope

- Defining visual design tokens, typography scales, or motion specs (covered by Epic 12).
- Implementing new LLM behaviors, recommendation algorithms, or health signal processing (covered by Epics 9–10).
- Hardware-specific flows (docks, wearables) — reserved for future hardware/ambient interface work.

## 13.7 Implementation Notes (Routes & Components)

This section links the screen IDs in this epic to **routes and components** in the current FastAPI + static HTML implementation. It is intentionally high-level; concrete component names may evolve with the front-end refactor under Epic 12.

### 13.7.1 Web (FastAPI + Static HTML)

- **Base app & static root**
	- `GET /` → serves the Action Sphere shell (currently backed by `enigma/static/action-sphere.html`).
	- `GET /dashboard` → serves the dashboard shell (existing or to-be-extended HTML/JS).
	- `GET /capture` → serves the standalone capture UI.

Mapping (initial):

- **WF-1 Flow Home (Orb + Today strip)**
	- Route: `/` (Flow mode default view).
	- Implementation: evolve the existing Action Sphere markup in `action-sphere.html` into a React/HTMX/Vue-like component tree (per front-end stack choice) with:
		- Orb component (tap/long-press behavior).
		- Now/Next strip component fetching commitments and recommendations via `/api/commitments` and future recommendation APIs.
		- Embedded Flow/Control mode toggle in the header.

- **WF-2 Today Board**
	- Route: `/today` or section within `/` (e.g., hash/scroll target `/#today`).
	- Implementation: board component consuming commitments + recommendation cards from `/api/commitments` and (later) `/api/recommendations`, with `My / Team / Org` toggle using auth/context from `enigma.auth`.

- **WF-3 Life Query Panel (overlay)**
	- Invoked from WF-1 via orb long-press; no separate route (client-side overlay).
	- APIs: `POST /api/query`, `POST /api/query/voice`, `GET /api/brief/context`.
	- Implementation: JS module managing the panel lifecycle and backend calls.

- **WF-4 Life Query Full View**
	- Route: `/life-query` (or `/` plus `#life-query` deep-link as today).
	- Implementation: larger panel/shell reusing the same API calls but with pinned queries and richer context panes.

- **WF-5 Capture Overlay**
	- Invoked from capture FAB on `/` and `/dashboard`; shares implementation with `/capture` page.
	- APIs: `POST /api/commitment` (and related capture endpoints in `enigma.web`).
	- Implementation: modular capture component that can mount as overlay or full page.

- **WF-6 Flow Inbox Slice**
	- Likely implemented as a drawer component on `/` that consumes future `/api/recommendations` plus existing commitments endpoints.

- **WF-7 Flow Scene View & WF-8 Flow Timeline Strip (optional)**
	- Scene view route: `/scene/:id` (or `/?scene=...`).
	- Timeline strip: embedded component within WF-1 consuming Omni-Scribe data (via a new endpoint built on top of `enigma.sentinel` outputs / Notion data).

- **WC-1 Control Home (Workspace Overview)**
	- Route: `/dashboard` (Control mode default view).
	- Implementation: new dashboard shell page consuming a set of summary APIs (existing `health` semantics from `enigma.main`/`enigma.orchestrator`, plus new org metrics endpoints as they are added).

- **WC-2/3 Workspaces & Tenancy / Workspace Detail**
	- Routes: `/org/workspaces`, `/org/workspaces/:id`.
	- Implementation: admin views over configuration stored in environment and/or a Supabase admin table; will likely require new endpoints in `enigma.web`.

- **WC-4 Memory Explorer**
	- Route: `/dashboard/memory` with internal tabs.
	- Implementation: uses existing Notion-facing functions in `enigma.notion_client` (e.g., `get_recent_thoughts`, people context queries) and new APIs (`/api/thoughts`, `/api/conversations`, `/api/grandmas-closet`) already exposed in `enigma.web`.

- **WC-5 Brief Archive & WC-6 Life Query History**
	- Routes: `/dashboard/briefs`, `/dashboard/queries`.
	- APIs: `GET /api/brief/archive`, `GET /api/query/history` from `enigma.web`.

- **WC-7 Chat Import & People Context**
	- Route: `/dashboard/import`.
	- APIs: `POST /api/import/chat` + future status endpoints; deep links into Memory Explorer.

- **WC-8 Recommendation Governance, WC-9 Health & Modes, WC-10 Org & Roles**
	- Routes: `/dashboard/recommendations`, `/dashboard/health-modes`, `/dashboard/org`.
	- Implementation: will require new FastAPI endpoints in `enigma.web` backed by configuration stored in Supabase (policy tables, health connectors, org metadata).

- **WC-11 Settings**
	- Route: `/settings` (global) and/or `/dashboard/settings` (workspace-specific).
	- Implementation: surfaces config from `.env` and any user-specific preferences stored in Supabase.

### 13.7.2 Mobile (Future Client)

- Native implementation detail (Flutter/FlutterFlow vs React Native vs web wrapper) is out of scope for this epic; here we only ensure that:
	- Every `MH-*`, `MI-*`, `MMEM-*`, `MORG-*`, `MMORE-*` screen has a **clear backing API** in the FastAPI layer.
	- The bottom-tab structure mirrors the conceptual grouping in this epic.
- Mobile can initially ship as a **responsive PWA** using the same routes (`/`, `/dashboard`, `/capture`, `/life-query`, `/dashboard/*`) with mobile-specific layouts driven by CSS + media queries (and later be wrapped or ported to Flutter/FlutterFlow per the roadmap).

## 13.8 Figma Page & Frame Structure (Initial Proposal)

To keep design and implementation in sync, Epic 13 should be reflected in a **Figma file structure** that maps 1:1 to the screen IDs above.

Suggested Figma organization:

- **Page 01 – Foundations (Epic 12)**
	- Tokens: colors, type scales, spacing, elevation, motion primitives.
	- Components: orb, cards, buttons, inputs, panels, drawers, nav elements.
	- Modes: Flow vs Control header treatments and background patterns.

- **Page 02 – Web / Flow Mode (Epic 13 WF-*)**
	- Frame group: `WF-1 Flow Home` (desktop + tablet variants).
	- Frame group: `WF-2 Today Board` (desktop + tablet variants).
	- Frame group: `WF-3 Life Query Panel` (overlay states on top of Flow Home).
	- Frame group: `WF-4 Life Query Full` (standalone screen).
	- Frame group: `WF-5 Capture Overlay` (Commitment / People / Thought modes).
	- Frame group: `WF-6 Flow Inbox Slice` (drawer expansion states).
	- Optional groups: `WF-7 Flow Scene View`, `WF-8 Flow Timeline Strip` attached as alternate flows.

- **Page 03 – Web / Control Mode (Epic 13 WC-*)**
	- Frame group: `WC-1 Control Home` (workspace overview).
	- Frame group: `WC-2/3 Workspaces & Workspace Detail` (list + detail).
	- Frame group: `WC-4 Memory Explorer` (tabs for Thoughts, Commitments, Conversations, Closet, All).
	- Frame group: `WC-5 Brief Archive` and `WC-6 Life Query History`.
	- Frame group: `WC-7 Chat Import & People Context`.
	- Frame group: `WC-8 Recommendation Governance`.
	- Frame group: `WC-9 Health & Modes Configuration`.
	- Frame group: `WC-10 Org & Roles`.
	- Frame group: `WC-11 Settings`.

- **Page 04 – Mobile / Flow Mode (Epic 13 MH-* + MI-*)**
	- Frame group: `MH-1 Mobile Flow Home` (iOS/Android key breakpoints).
	- Frame group: `MH-2 Mobile Today Board`.
	- Frame group: `MH-3 Mobile Life Query Full`.
	- Frame group: `MI-1 Recommendation & Commitments List` and `MI-2 Detail`.
	- Include bottom-tab + capture FAB patterns reused across frames.

- **Page 05 – Mobile / Control & Org (Epic 13 MMEM-*, MORG-*, MMORE-*)**
	- Frame group: `MMEM-1 Thoughts`, `MMEM-2 Closet`, `MMEM-3 Conversations` views.
	- Frame group: `MORG-1 Org Overview`, `MORG-2 Workspace Detail (Mobile)`.
	- Frame group: `MMORE-1 Brief Archive`, `MMORE-2 Query History`, `MMORE-3 Settings`.

- **Page 06 – Flows & Prototypes**
	- User journey flows:
		- Morning/Anytime Flow: Flow Home → Today Board → Life Query → Accept/Defer.
		- Capture Flow: any screen → Capture Overlay → confirmation → return.
		- Admin Flow: Control Home → Workspaces → Workspace Detail → Memory Explorer.
		- Mobile quick triage: Mobile Flow Home → Inbox tab → card detail → action.
	- Connect frames with interactive prototyping links that mirror the navigation relationships defined in sections 13.1–13.4.

This structure should give design and engineering a shared, screen-level contract: every table row in sections 13.1–13.3 has a corresponding Figma frame, a URL route (for web), and a backing API surface.

