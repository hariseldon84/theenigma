# 12. UI/UX Foundation (Web + Mobile)

## 12.1 Design Thesis

Enigma should feel like a premium cognitive workspace that combines enterprise-grade trust with human warmth. The UI should be intentional, calm, and high-signal: always clear for operational work, but never cold or mechanical.

## 12.2 Direction Lock-Ins

- **Core style direction:** Premium warmth (editorial + human)
- **Primary typography personality:** Modern humanist
- **Web shell:** Focus mode with collapsible contextual intelligence pane
- **Mobile shell:** Bottom tabs + persistent floating capture/action button
- **Motion level:** Refined premium micro-interactions
- **Theme baseline:** Dual-mode parity (light and dark both first-class)

## 12.3 Typography System

- **Primary UI font:** `Sohne`
- **Accent font:** `Tiempos Text`
- **Density:** Balanced enterprise
- **Usage rules:**
  - `Sohne` for navigation, controls, forms, data views, and dense operational surfaces
  - `Tiempos Text` for section headers and selected key insight cards only

## 12.4 Color and Surface System

- **Mood:** Warm neutral
- **Base direction:** Stone/linen neutrals + ink/charcoal structure
- **Accent direction:** Subtle copper/gold highlights for premium emphasis
- **Semantic behavior:** Success/warning/error colors should harmonize with the warm-neutral palette

## 12.5 Motion Grammar

- **Default duration band:** 180-240ms
- **Purpose:** Communicate hierarchy/state changes, not decoration
- **Preferred patterns:** Context pane transitions, card focus/elevation cues, restrained staggered reveals

## 12.6 Web Architecture Pattern

- Primary center pane remains dominant for active work
- Contextual side pane supports recommendations, traces, risk signals, and query context
- Side pane must be collapsible and non-obstructive to primary task execution

## 12.7 Mobile Architecture Pattern

- Bottom-tab structure for core modules
- Floating action button for one-tap capture and quick action entry
- Recommendation cards with explicit `Accept`, `Edit`, `Defer` actions

## 12.8 Quality and Accessibility Guardrails

- Light and dark mode parity for all primary workflows
- Maintain readable hierarchy and contrast for functional text and controls
- Keep motion subtle and accessible with reduced-motion support
- Preserve responsive consistency across desktop, tablet, and mobile breakpoints

## 12.9 Delivery Notes

- This foundation maps directly to Epic 12 functional requirements.
- The source calibration was captured in the brainstorming session dated 2026-03-13 (extended on 2026-03-16).
