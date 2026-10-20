---
name: "InfraFlow gated task"
about: "Track one reviewable InfraFlow work item with Linear traceability and G0–G4 guards"
title: "[W?][Owner] "
---

## Owner / reviewer / schedule
- Week (dates):
- Owner (exact person / GitHub assignee only when confirmed):
- Reviewer:
- Linear issue:
- Component/interface in Technical Design / Interface Contracts v1.2:

## Preconditions
- [ ] Approval gates identified (G1 for AWS tests; G2/G3 for decisions; G4 for product code/IaC).
- [ ] Work is within approved scope and upstream blockers are resolved.

## Tasks
- [ ] Define expected behavior and evidence.
- [ ] Execute allowed planning/testing/implementation steps and record *actual* results.
- [ ] Request peer review and record deliverable links.

## Definition of Done
- [ ] Acceptance scenarios passed or declared NOT RUN/BLOCKED truthfully.
- [ ] Public-safe evidence and PR linked.
- [ ] Reviewer and Linear status updated.

## Safety
No secret, state, saved plan, PII or sensitive inventory. Never perform AWS PoC before G1 or product implementation before G4.
