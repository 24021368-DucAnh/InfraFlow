# InfraFlow — Đức Anh W6→W7 Design & Planning Handoff (DUC-25/27/40/41)

**Recorded:** 20/10/2026 · **Owner:** Ngô Bùi Đức Anh · **Status:** PRE-G4 planning deliverables for review (not implementation approval).

## 0. Which 'weeks 6 and 7'?

Two scopes appear in the group's planning history:

- **Original report, week 6–7:** Đức Anh owns Web+DB Blueprint design ([DUC-25](https://linear.app/ducanh/issue/DUC-25); original estimate 22h over weeks 6–7) and fixed URL/sleeping experience ([DUC-27](https://linear.app/ducanh/issue/DUC-27); 10h in week 7). These are the two *component design* deliverables covered by this branch.
- **Rebased W6–W10 calendar:** W6 = 12–18/10, late baseline design; owner confirmed Technical Design/Contracts v1.2 on **19/10** (G0). W7 = 19–25/10, prepare P1–P6/G1, requirements→component→test mapping and G4 readiness. See [W7 GitHub issue #2](https://github.com/24021368-DucAnh/InfraFlow/issues/2), [DUC-40](https://linear.app/ducanh/issue/DUC-40) and [DUC-41](https://linear.app/ducanh/issue/DUC-41). W6's accepted G0 **must not be re-reviewed as if still unapproved**.

**Source authority:** [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) override historic issue text which still says 'architecture not yet finalized'. This repository cannot yet verify complete doc-section/wire names; defer exact details to a section-by-section review, **do not invent them**.

## 1. Reviewable outputs completed in this branch

| Workstream | Draft deliverable | Done here | Remains open |
|---|---|---|---|
| W6/W7 DUC-25 | [Blueprint component & safety review](../design/DUC-25-web-database-blueprint-review.md) | Logical graph, lifecycle & cost matrix, permission/state boundaries, BP-01…BP-12 test catalogue | Validate exact v1.2 contracts; G1/P3 evidence, reviewer acceptance |
| W7 DUC-27 | [Stable URL/sleeping page & P5 review](../design/DUC-27-url-sleeping-health-cutover-review.md) | User state matrix, auth/health invariants, DNS alternatives, URL-01…URL-12 tests | Validate domain authority and v1.2 semantics, G1/P5, G3 option decision, reviewer |
| W7 DUC-40 | Requirements→component→test mapping, below and existing [traceability draft](https://linear.app/ducanh/document/infraflow-requirementcomponenttest-traceability-v01-draft-2613bddb7173) | Cross-team coverage checklist, test IDs, blockers | Exact v1.2 section mapping and all-owner peer review |
| W7 DUC-41 | [Collaboration agreement v0.2](https://linear.app/ducanh/document/infraflow-github-collaboration-and-integration-v02-public-pr-1-open-8139b78c893a), actual Github [onboarding PR #1](https://github.com/24021368-DucAnh/InfraFlow/pull/1) and [W7–W10 plan PR #19](https://github.com/24021368-DucAnh/InfraFlow/pull/19) | Public repo PR policy documented, CI safety checklist below | Verify reviewer enforcement/rulesets, non-destructive CI setup and G4 review |

**Actual GitHub verification as of 20/10:** onboarding PR #1 was merged; weekly issue plan PR #19 was merged later. GitHub issues #2–#18 already exist. Do not confuse merged *documentation* with actual cloud/software implementation.

## 2. Review traceability matrix (design-level; wire mapping awaits full v1.2)

| Domain requirement | Owner / primary boundary | Acceptance test IDs in this branch | Additional test/PoC and owner |
|---|---|---|---|
| Create Web+DB / supported params | Đức Anh Blueprint → Hoàng API | BP-01, BP-02 | P3 (Hoàng/Đức Anh), full contract review |
| Register compatible workspace and handoff | Đạt state/ownership ↔ Đức Anh component compatibility | BP-03, BP-04 | P1/P2, DUC-38 (Đạt/Minh) |
| Resource inventory and ownership scope | Đạt/Minh validator ↔ Đức Anh Blueprint | BP-04, BP-07, BP-09 | P1/P2/P4 |
| Stable URL Create & Register | Đức Anh DNS ↔ Hoàng UI | URL-01, 02, 07, 08 | P5, domain/cert evidence |
| Sleep preserve data and return sleeping UX | Minh controller ↔ Đức Anh Blueprint/DNS | BP-05, URL-02, URL-09 | P3/P4/P5 |
| Wake auth/idempotency and health gate | Hoàng API ↔ Minh controller ↔ Đức Anh DNS | BP-06, URL-03, 04, 05, 10 | P4/P5 |
| Desired / Observed and drift | Đạt actual inventory ↔ Minh controller | BP-09, URL-09 | P1/P2/P4 |
| Concurrency/exclusive writer | Đạt state backend ↔ Minh controller | BP-11, URL-10 | P1/P2 |
| Permit/plan fail-closed | Đạt validator ↔ Minh safety | BP-07, BP-08 | P4 |
| Reclaim backup, ownership and Verify | Minh controller ↔ Đạt validator | BP-08, BP-10, URL-11 | P4 |
| Cost scenarios/remaining spend | Hoàng cost ↔ Đức Anh component matrix | BP-12, URL-12 | P6 with price/usage source |
| UI/API error and BLOCKED visibility | Hoàng Web/API ↔ Minh controller ↔ Đức Anh sleeping page | BP-04, URL-04, 05, 09 | Contract test after G4 |

**Not a v1.2 section citation.** The mapping above covers themes identifiable from DUC-25/27/29/38/40, not a literal extraction of undocumented signatures or enums. Reviewer must attach the precise section/contract table from the full approved docs.

## 3. W7 — explicit task checklist to finish

### W7-A: Baseline traceability (DUC-40)
- [x] Draft owner/component/test coverage and link BP/URL acceptance test IDs.
- [ ] Copy **exact approved v1.2 section references and wire tables** into DUC-40 traceability register.
- [ ] Identify all required lifecycle edge cases absent from these draft catalogues.
- [ ] Đạt/Minh/Hoàng review producer/consumer mapping; record review comments/approval.

### W7-B: PoC readiness and design evidence (DUC-24/37/43/44/45)
- [x] Prepare proposed P3 component and P5 DNS/health test matrices for G1 review.
- [ ] Obtain G1 account owner approval of account, region, IAM, budget/kill-switch, test domain, resource scope, test slots, rollback/cleanup.
- [ ] After G1: execute P1–P6 approved probes; record expected/actual/pass-fail, timing/cost, sanitized AWS inventory and cleanup.
- [ ] G2 review results; register G3 ADR for DNS option, backend strategy, retry/health/cost thresholds without altering already approved semantics.

### W7-C: CI/PR readiness (DUC-41) and G4 preparation (DUC-36)
- [x] Public onboarding and PR/issue procedure exists on GitHub.
- [x] Weekly work issues and team plan exist, including conditional W9/W10 tasks.
- [ ] Confirm exact team GitHub handles and collaborator permissions; validate main branch protection and independent reviewer enforcement.
- [ ] Agree on **non-destructive checks only** (Markdown/reference checks, future lint/unit/contract/static Terraform checks without live AWS credentials or apply/destroy); do not claim CI exists until workflow is merged and verified.
- [ ] After reviewed G2/G3: create bite-sized G4 implementation plan with concrete approved file paths, interfaces, TDD failures→fix→pass, reviewer, effort, dependencies, cleanup, fallback; owner approves **before code/IaC**.

## 4. G1–G4 decision ledger (only record explicit evidence/approval)

| Gate/decision | Status as of this draft | What evidence can close it |
|---|---|---|
| G0 baseline | Accepted 19/10/2026 (DUC-34/35) | Already closed; do not re-review semantics |
| G1 AWS PoC permission | **NOT VERIFIED / no authorization asserted** | Account owner, IAM, region, budget/alerts, scope, rollback and teardown sign-off |
| G2 P1–P6 measured evidence | **NOT RUN (this work)** | Approved probes executed and audited actual results/cleanup |
| G3 backend/DNS/limits ADR | **OPEN** | Group-reviewed decisions based on G2 evidence |
| G4 implementation plan | **NOT APPROVED** | Reviewed task plan with contract/test/rollback/cost; explicit owner approval |

## 5. Handoff / requested reviews

- **Đạt**: verify Register backend writer-lock/ownership and resource discovery boundary; give G1/P3 assumptions to BP matrix.
- **Minh**: verify Blocked/permit/backup/Verify, risk of false healthy/public cutover and operation races.
- **Hoàng**: verify Web/API Wake authorization, progress/error UX and costs from P6.
- **Project owner:** acknowledge this DUC-25/27 design-review draft; confirm any mismatches with authoritative v1.2 and approve corrections via Linear rather than merge semantics changes unreviewed.

## 6. Scope limitations

This work is documentation/preflight only: **no Terraform module, AWS account action, E2E run, valid state proof, real DNS/cert setup or cost optimization measurement**. BP/URL checks are proposed acceptance tests with status NOT RUN, not evidence of production behavior.
