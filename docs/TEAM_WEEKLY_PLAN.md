# InfraFlow — Weekly Team Work Plan (W7–W10)

**Version:** 0.1 · **Created:** 20 October 2026 · **Status:** review draft · **Repository:** PUBLIC

> **Start here:** [GitHub master issue #18 — W7–W10 task index](https://github.com/24021368-DucAnh/InfraFlow/issues/18). Each cell in the table links to a real GitHub Issue with a detailed actionable checklist. **Linear is the source of truth for architectural decisions, approvals, gate outcomes and official progress.**

## Week-by-week ownership

| Week | Đức Anh — Blueprint/DNS/integration | Đạt — state/backend/validator | Minh — controller/safety | Hoàng — Web/API/cost |
|---|---|---|---|---|
| **W7** · 19–25 Oct | [#2 Traceability + PR/G4 planning](https://github.com/24021368-DucAnh/InfraFlow/issues/2) | [#3 P1/P2A/P2B experiment plan](https://github.com/24021368-DucAnh/InfraFlow/issues/3) | [#4 P4 safety/failure matrix](https://github.com/24021368-DucAnh/InfraFlow/issues/4) | [#5 P3/P5/P6 experiment plan](https://github.com/24021368-DucAnh/InfraFlow/issues/5) |
| **W8** · 26 Oct–1 Nov | [#6 Blueprint/Register/DNS evidence](https://github.com/24021368-DucAnh/InfraFlow/issues/6) | [#7 Backend, lock, state PoC evidence](https://github.com/24021368-DucAnh/InfraFlow/issues/7) | [#8 P4/Verify PoC evidence](https://github.com/24021368-DucAnh/InfraFlow/issues/8) | [#9 DNS/Cost/API mapping evidence](https://github.com/24021368-DucAnh/InfraFlow/issues/9) |
| **W9** · 2–8 Nov | [#10 Blueprint+DNS implementation after G4](https://github.com/24021368-DucAnh/InfraFlow/issues/10) | [#11 Register state/backend/validator after G4](https://github.com/24021368-DucAnh/InfraFlow/issues/11) | [#12 Controller/Sleep/Wake/Reclaim after G4](https://github.com/24021368-DucAnh/InfraFlow/issues/12) | [#13 Web/API/Lease/cost after G4](https://github.com/24021368-DucAnh/InfraFlow/issues/13) |
| **W10** · 9–15 Nov | [#14 Blueprint/DNS/health integrated evidence](https://github.com/24021368-DucAnh/InfraFlow/issues/14) | [#15 State/lock/retry/cleanup regression](https://github.com/24021368-DucAnh/InfraFlow/issues/15) | [#16 Reclaim/Verify/BLOCKED E2E](https://github.com/24021368-DucAnh/InfraFlow/issues/16) | [#17 UI/cost/demo/report](https://github.com/24021368-DucAnh/InfraFlow/issues/17) |

## Outputs and stage conditions

| Period | Deliverable | Evidence to attach | Must be true before execution |
|---|---|---|---|
| W7: preparation | G1 readiness request, P1–P6 test sheets, traceability, interface review | Reviewed docs/test matrix + open questions | No AWS action before G1 |
| W8: PoC and decisions | Approved limited P1–P6 AWS probes, G2 evidence, draft/approved G3 ADRs | Expected/actual, pass/fail/NOT RUN, sanitized inventory, cost/time, cleanup | AWS actions only after explicit G1; G3 conclusions need G2 evidence |
| W9: implementation | Blueprint/DNS, state/backend, controller/safety, Web/API MVP | Design-specific tasks after G4 with TDD, unit/contract tests, PR reviews | **Product code and IaC only after G4**; AWS access also requires G1 |
| W10: integration/demo | Two Create/Register journeys, Sleep/Wake/Reclaim/Verify and BLOCKED tests, cost comparison | URL/health/data checks, ownership/backup/Verify evidence, cleanup, demo report | Actual E2E only if G1 + G4 and deployed test build; otherwise mark NOT RUN or mock |

**These are planning windows, not promised deadlines.** If G1, G2, G3 or G4 is delayed, keep implementation issues BLOCKED; reschedule through [Linear DUC-36](https://linear.app/ducanh/issue/DUC-36) with owner decision. Do not remove tests or bypass a gate to meet a weekly calendar.

## Design and operational constraints

- The accepted baseline is [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) (19 October 2026).
- InfraFlow supports the approved MVP goal of Create from Web+DB Blueprint and Register a compatible existing AWS Terraform Web+DB workspace, then authorized shared lifecycle. Do not assume all Terraform workspaces are compatible.
- Never assume state ownership/lock, AWS budget, Terraform plan safety or ability to stop/start/remove RDS without test evidence.
- For destructive actions and recovery, missing permit/backup/ownership, unknown drift or incomplete Verify must fail closed (BLOCKED), never be represented as success.
- Source repository is **Public**. Do not upload AWS secrets/keys, raw Terraform state/plan, private inventory, user data or sensitive logs.
- **G0** accepted. **G1** AWS PoC authorization; **G2** PoC evidence; **G3** ADR reviews; **G4** approved implementation plan. Do not equate the existence of this plan with an approved gate.

## How each student works

1. Open this week's issue with your name and check gate/dependency conditions.
2. Complete checkboxes and add real deliverable links, test evidence status and any BLOCKED reasons; do not tick something merely because it is planned.
3. If post-G4 code work: create an issue-linked feature branch, implement the approved small task, document tests, open a PR, request peer review and update Linear.
4. Never place secrets or raw AWS evidence into public GitHub issues/commits.
5. Update the linked Linear issue with review/approval and official status; GitHub issue checkboxes are not architectural approvals.

**GitHub assignees:** `24021368-DucAnh` is assigned to issues #2/#6/#10/#14. Đạt/Minh/Hoàng are named as proposed owners but their exact GitHub logins are unverified; do not assign by guessed usernames. Once owner confirms collaborator identities, update assignees and review policy.

## Related project tracking

- [Linear project InfraFlow](https://linear.app/ducanh/project/infraflow-31b8c3b2d1ad)
- [DUC-24 — PoC questions & G1](https://linear.app/ducanh/issue/DUC-24)
- [DUC-37 — G2 evidence review & G3 decision](https://linear.app/ducanh/issue/DUC-37)
- [DUC-36 — G4 plan readiness](https://linear.app/ducanh/issue/DUC-36)
- [DUC-33 — Integration/test/demo](https://linear.app/ducanh/issue/DUC-33)
- [Repo onboarding PR #1](https://github.com/24021368-DucAnh/InfraFlow/pull/1), still awaiting review/merge.
