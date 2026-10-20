# InfraFlow — Đức Anh W6→W7 Design & Planning Handoff (DUC-25/27/40/41)

**Recorded:** 21/10/2026 · **Owner:** Ngô Bùi Đức Anh · **Status:** PRE-G4 planning deliverables for review (not implementation approval).

## 0. Which 'weeks 6 and 7'?

Two scopes appear in the group's planning history:

- **Original Action Plan, table 3.1 of `progress_1.pdf` (pp. 11–12):** Đức Anh owns the **implemented** Web+DB Blueprint with Terraform for network/egress/database/app/entry, `components.yaml`, dependencies and stable create/destroy (22h, W6–W7), plus **working** Route 53 URL switching, sleeping page, Wake button and progress (10h, W7). Those executable outcomes are **not completed by this documentation PR**. Its 172h total also differs from the table's 166h sum; Technical Design v1.2 §1 flags this as an unresolved estimate discrepancy.
- **Rebased W6–W10 calendar:** W6 = 12–18/10, late baseline design; owner confirmed Technical Design/Contracts v1.2 on **19/10** (G0). W7 = 19–25/10, prepare P1–P6/G1, requirements→component→test mapping and G4 readiness. See [W7 GitHub issue #2](https://github.com/24021368-DucAnh/InfraFlow/issues/2), [DUC-40](https://linear.app/ducanh/issue/DUC-40) and [DUC-41](https://linear.app/ducanh/issue/DUC-41). W6's accepted G0 **must not be re-reviewed as if still unapproved**.

**Rebased tracker supplied by owner:** W6 (12–18/10) is marked late and its G0 baseline completion was recorded on 19/10 as four W7-BU baseline acknowledgments; W7 (19–25/10) lists eight tasks, four acknowledged and four still unconfirmed in its snapshot. The tracker treats W7 PoC/implementation planning as dependent on G1→G2→G3→G4. Its 2h W6 per-person entry is an **estimate, not actual hours**. Do not turn the tracker snapshot into proof that tests or implementation ran.

**Source authority:** [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) were retrieved in full on 21/10 and override historical issue text that still says architecture is unfinalized. The v1.2 documents fix logical semantics and names in Contracts §2.1, but defer physical wire endpoints/types and measured AWS values. Section mapping is in [DUC-40](DUC-40-v12-contract-traceability-register.md); no implementation signature is inferred.

## 1. Reviewable outputs completed in this branch

| Workstream | Draft deliverable | Done here | Remains open |
|---|---|---|---|
| W6/W7 DUC-25 | [Blueprint component & safety review](../design/DUC-25-web-database-blueprint-review.md) | Logical graph, lifecycle & cost matrix, permission/state boundaries, BP-01…BP-16 test catalogue | Validate exact v1.2 contracts; G1/P3 evidence, reviewer acceptance |
| W7 DUC-27 | [Stable URL/sleeping page & P5 review](../design/DUC-27-url-sleeping-health-cutover-review.md) | User state matrix, auth/health invariants, DNS alternatives, URL-01…URL-16 tests | Validate domain authority and v1.2 semantics, G1/P5, G3 option decision, reviewer |
| W7 DUC-40 | [v1.2 Contract Traceability Register v0.3](DUC-40-v12-contract-traceability-register.md) plus original [traceability draft](https://linear.app/ducanh/document/infraflow-requirementcomponenttest-traceability-v01-draft-2613bddb7173) | **14** categories mapped to full v1.2 logical sections; CT-13 Unregister and CT-14 recovery have planned negative cases | Physical wire mapping after G3/G4 and all-owner peer review |
| W7 DUC-41 | [Collaboration agreement v0.2](https://linear.app/ducanh/document/infraflow-github-collaboration-and-integration-v02-public-pr-1-open-8139b78c893a), actual Github [onboarding PR #1](https://github.com/24021368-DucAnh/InfraFlow/pull/1) and [W7–W10 plan PR #19](https://github.com/24021368-DucAnh/InfraFlow/pull/19) | Public repo PR policy documented, CI safety checklist below | Verify reviewer enforcement/rulesets, non-destructive CI setup and G4 review |

**Actual GitHub verification as of 20/10:** onboarding PR #1 was merged; weekly issue plan PR #19 was merged later. GitHub issues #2–#18 already exist. Do not confuse merged *documentation* with actual cloud/software implementation.

## 2. Review traceability matrix (approved logical sections in DUC-40; physical wire pending)

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

**Section-level citations are in DUC-40 CT-01..14.** This summary intentionally omits physical endpoints, payload types and AWS choices, which v1.2 leaves for implementation planning and PoC.

## 3. W7 — explicit task checklist to finish

### W7-A: Baseline traceability (DUC-40)

- [x] Draft owner/component/test coverage and link BP/URL acceptance test IDs.
- [x] Created [DUC-40 v1.2 contract traceability register](DUC-40-v12-contract-traceability-register.md) with 14 CT categories, exact logical section references and owner review routing; physical wire remains pending G4.
- [x] Reconciled v1.2 logical state, error, permission and handoff rules; corrected URL-user Wake and identified Unregister/recovery test gaps.
- [ ] Finish physical producer/consumer schema mapping after G2/G3, then review for G4.
- [ ] Đạt/Minh/Hoàng review producer/consumer mapping; record review comments/approval.

### W7-B: PoC readiness and design evidence (DUC-24/37/43/44/45)

- [x] Prepare proposed P3/P5 test matrices and [reproducible evidence sheet](DUC-25-27-P3-P5-evidence-test-sheets.md) for G1 review (16 BP + 16 URL acceptance scenarios; **all NOT RUN**).
- [x] Prepared [G1 approval and P1–P6 readiness package](DUC-24-G1-poc-authorization-and-evidence.md), with go/no-go/stop/cleanup/evidence forms **not filled or approved**.
- [ ] Obtain G1 account owner approval of account, region, IAM, budget/kill-switch, test domain, resource scope, test slots, rollback/cleanup.
- [ ] After G1: execute P1–P6 approved probes; record expected/actual/pass-fail, timing/cost, sanitized AWS inventory and cleanup.
- [ ] G2 review results; register G3 ADR for DNS option, backend strategy, retry/health/cost thresholds without altering already approved semantics.

### W7-C: CI/PR readiness (DUC-41) and G4 preparation (DUC-36)

- [x] Public onboarding and PR/issue procedure exists on GitHub.
- [x] Weekly work issues and team plan exist, including conditional W9/W10 tasks.
- [ ] Confirm exact team GitHub handles and collaborator permissions; validate main branch protection and independent reviewer enforcement.
- [ ] Agree on **non-destructive checks only** (Markdown/reference checks, future lint/unit/contract/static Terraform checks without live AWS credentials or apply/destroy); do not claim CI exists until workflow is merged and verified.
- [ ] After reviewed G2/G3: create bite-sized G4 implementation plan with concrete approved file paths, interfaces, TDD failures→fix→pass, reviewer, effort, dependencies, cleanup, fallback; owner approves **before code/IaC**.

### W7 quality-review closure tracker (no fabricated sign-off)

An AI-assisted [GitHub PR #20 review](https://github.com/24021368-DucAnh/InfraFlow/pull/20) identified the following. These are **document changes**, not verified AWS test outcomes or independent peer approvals.

| Prior finding | Remediation now in PR #20 | Remaining acceptance gate |
|---|---|---|
| P1: blueprint contract had six UNVERIFIED mappings | Mapped six boundaries to full v1.2 logical sections and fields in [DUC-25](../design/DUC-25-web-database-blueprint-review.md); physical wire left pending | Independent peer confirmation and G4 wire mapping **OPEN** |
| P1: RDS 7-day auto-restart/long Sleep missing | DUC-25 RDS feasibility addendum and BP-13; P3-03 synthetic drift scenario | G1-authorized AWS evidence, G3 policy choice **NOT RUN** |
| P1: all-unhealthy ALB fail-open | DUC-27 independent public-route gate, URL-13 and P5-03 | Select/verify mechanism after G2/G3; no zero-traffic proof **NOT RUN** |
| P2: lifecycle ownership/component cost inputs vague | DUC-25 per-component evidence/cost table and P3-08 | Exact v1.2 schemas + region-aware AWS price/actual bill **OPEN** |
| P2: 24 cases not executable | [P3/P5 reproducible probe sheet](DUC-25-27-P3-P5-evidence-test-sheets.md) with fixtures, procedures, pass/fail/evidence/cleanup and versioned case mapping (now **32 planned IDs**) | Run only after G1/G4 as appropriate; all outcomes **NOT RUN** |
| P2: Register DNS ownership, Wake misuse/status leakage | Corrected URL-user Wake under Technical Design §1/Contracts §6; Register without DNS control cannot Activate; URL-15/P5-02/05 cover abuse/privacy | Independent review and actual P5 **OPEN** |

**21/10 review update:** [DUC-40 baseline-to-contract register](DUC-40-v12-contract-traceability-register.md) now maps 14 boundaries to the retrieved full baselines and names Unregister handback/recovery tests. [G1 authorization package](DUC-24-G1-poc-authorization-and-evidence.md) contains the unsigned AWS owner form and P1–P6 criteria. Both remain PRE-GATE: **physical wire, peer review and G1 approval are still absent**.

**Reference boundaries:**

- [DUC-34](https://linear.app/ducanh/issue/DUC-34) and [DUC-35](https://linear.app/ducanh/issue/DUC-35) record baseline acceptance; the full v1.2 documents supply the section references and logical contract fields. They do **not** prescribe physical wire endpoints.
- External AWS documents ([RDS stop/7-day restart](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_StopDBInstance.html), [ALB all-targets-unhealthy fail-open](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)) constrain feasibility; they do not override the approved functional contract.
- A formal review posted through project owner `24021368-DucAnh` is **AI-assisted feedback, not independent peer sign-off**. A reviewer must re-check this patch and decide if each GitHub thread is resolved.

### Owner pre-G4 completion criteria

- [x] Public GitHub repo/working rules, 16 weekly issues and team plan: documentation set up; onboarding PR #1 / weekly plan PR #19 merged.
- [x] DUC-25 and DUC-27 design review drafts, explicit RDS/ALB and Register/DNS risk scenarios, test sheets/evidence templates prepared on PR #20.
- [x] W7 traceability themes and responsibilities cross-referenced with 32 proposed BP/URL test IDs.
- [x] Author mapped approved v1.2 logical sections to CT-01..14; no physical wire claim.
- [ ] Peer reviewer confirms the mapping and G4 plan maps physical producer/consumer signatures.
- [ ] Independent review/sign-off by Đạt, Minh and Hoàng for relevant producer/consumer boundaries.
- [ ] G1 AWS PoC approval; G2/P1–P6 evidence; G3 ADR for implementation-only parameters; G4 implementation plan acceptance (not part of this documentation-only task).

**Decision:** W6 G0 is Done. DUC-25/27 design draft + W7 plan artifacts are **ready for peer review**, but official issue states remain **In Progress**. This is not authorization to merge PR #20 or start Terraform/AWS activity.

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
