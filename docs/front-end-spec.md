# Enigma — Front-end spec (Figma ↔ code bridge)

**Purpose:** Single source of truth for **design tokens** and **component mapping** so UX (Sally) can update values after inspecting Figma via MCP, and dev only **changes variables** instead of rewriting entire UI blocks.

**Milan Minimalism:** Dark base, glass surfaces, Electric Cerulean accent, minimal chrome.

---

## Design tokens (CSS variables)

These are defined in `enigma/static/action-sphere.html` under `:root`. When Figma variables change, update **here first**, then sync into `:root`.

| Token | Current value | Figma variable (suggested name) | Notes |
|-------|----------------|----------------------------------|--------|
| `--bg` | `#050505` | Enigma / Background | Page background |
| `--surface` | `rgba(255,255,255,0.04)` | Enigma / Surface | Raised surfaces |
| `--surface-border` | `rgba(255,255,255,0.08)` | Enigma / Border | Subtle borders |
| `--cerulean` | `#00A3FF` | Enigma / Accent | Electric Cerulean primary |
| `--cerulean-dim` | `rgba(0,163,255,0.25)` | Enigma / Accent Dim | Glows, soft fills |
| `--text` | `#e5e5e5` | Enigma / Text | Primary text |
| `--text-muted` | `rgba(229,229,229,0.6)` | Enigma / Text Muted | Hints, labels |
| `--glass` | `rgba(255,255,255,0.06)` | Enigma / Glass | Glassmorphism fill |
| `--glass-border` | `rgba(255,255,255,0.1)` | Enigma / Glass Border | Glass cards |

**Backdrop blur (glass panels):** `backdrop-filter: blur(12px)` on `.feed-item` and life-query panels. If Figma specifies a different blur, record it here as **Enigma / Blur Glass** and update the `blur(...)` value in CSS.

---

## Component map (Figma layer ↔ code)

| Figma frame / layer | Code location | Notes |
|---------------------|---------------|--------|
| Enigma Home / Action Sphere | `action-sphere.html` | Main shell |
| Orb | `#orb`, `.orb` | Tap = commitments; long-press = Life Query |
| Open Commitments feed | `#feed-list`, `.feed-item` | Data from `GET /api/commitments` |
| Life Query panel | `#life-query`, `.life-query-panel` | Text + voice query |
| Audio FAB | `#audio-fab` | Opens commitment / people capture |
| Capture panel | `#capture-panel` | Commitment vs People context + mic |

Prefix layer names in Figma with `#ActionSphere_*` if you want strict 1:1 naming.

---

## Flows (no UI redesign in this doc)

1. **Orb tap** → scroll to Open Commitments.
2. **Orb long-press** → Life Query panel.
3. **Audio FAB** → Capture panel (Commitment / People context).
4. **Life Query** → Ask text or voice → answer card.

---

## When pulling from Figma

1. Paste **frame link** into the prompt.
2. MCP returns structure + screenshot — extract **hex**, **blur**, **radius**.
3. Update the **table above** and `:root` in `action-sphere.html` (or a future shared `theme.css`).
4. Prefer **variable substitution** only; avoid duplicating hex in multiple places.

---

## Related docs

- `docs/figma-mcp-setup.md` — MCP env, Cursor setup, Sally/dev prompts  
- `docs/prd/epics/epic-4-action-sphere-ui.md` — FR-4.x acceptance criteria  
