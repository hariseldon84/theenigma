# Epic 9: Recommendation Governance & Adaptive Planning

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-9.1 | Recommendation Inbox with explicit actions (`Accept`, `Modify`, `Defer`, `Reject`) | P1 | All Enigma-generated suggestions appear in one queue with user decision controls |
| FR-9.2 | Recommendation receipts (source trace, confidence, expected impact) | P1 | Each suggestion includes explainability metadata visible to user |
| FR-9.3 | Commitment Compiler builds daily task packages from Gmail/Telegram/WhatsApp/voice/calendar | P1 | Auto-created task groups include owner, due date (or confidence band), and dependency links |
| FR-9.4 | Probabilistic due-date estimation with confidence bands | P2 | Tasks can show `date + confidence`, not only single hard date |
| FR-9.5 | Noise pruning via decision-value thresholds | P1 | Low-value recommendations are batched/summarized instead of interrupting user |
| FR-9.6 | Mode-based recommendation aggressiveness (Focus/Routine/Recovery/Crisis) | P2 | Recommendation volume and automation level adapt to selected or inferred user mode |

## Notes

- Recommendation-first governance is a product principle: Enigma proposes first, user remains in control.
- This epic is the bridge between memory capture and execution-quality outcomes.
