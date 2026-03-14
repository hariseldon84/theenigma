# Epic 10: Health-Adaptive Cognitive Ops

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-10.1 | Integrate Apple Health / Google Fit / supported wearables (opt-in) | P2 | Users can connect health sources with explicit consent and clear data scope |
| FR-10.2 | Health-informed schedule/task suggestions are recommendation-only by default | P1 | Enigma never force-applies health-driven changes without user approval |
| FR-10.3 | Vital-state work modes (`Deep`, `Collaborative`, `Admin`, `Recovery`) | P2 | Task prioritization and suggestion cadence adapt to current mode |
| FR-10.4 | Burnout-risk detection and preventive intervention playbooks | P2 | Enigma flags overload early and proposes mitigations (reschedule, delegate, reduce noise) |
| FR-10.5 | Recovery-first rescheduling with stakeholder communication drafts | P2 | Health + workload signals can generate safe re-plan recommendations and draft follow-ups |
| FR-10.6 | Health guardrails: non-clinical framing and policy limits | P1 | Product prevents medical claims unless certified modules are enabled |

## Notes

- This epic should preserve user sovereignty while increasing sustainable execution quality.
- Health signals are context inputs, not deterministic authority.
