# DUC-25/27 — W8 Blueprint, Register and URL evidence review

**As of:** 31 October 2026 · **Window:** W8, 26 October–1 November · **Tracking:** [GitHub #6](https://github.com/24021368-DucAnh/InfraFlow/issues/6), [DUC-25](https://linear.app/ducanh/issue/DUC-25), [DUC-27](https://linear.app/ducanh/issue/DUC-27), [DUC-40](https://linear.app/ducanh/issue/DUC-40) · **Status:** REVIEW DRAFT / P3 AND P5 NOT RUN

This review uses the accepted [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a). The [W6–W7 review package](../design/DUC-25-web-database-blueprint-review.md), [URL design](../design/DUC-27-url-sleeping-health-cutover-review.md), [traceability](DUC-40-v12-contract-traceability-register.md) and [P3/P5 sheets](DUC-25-27-P3-P5-evidence-test-sheets.md) remain drafts. This document records W8 acceptance boundaries and evidence still needed; it does not change v1.2 semantics.

## Gate and evidence ledger

| Gate or result | Verified status in reviewed project/issue records | W8 consequence |
|---|---|---|
| G0 design/contracts | v1.2 accepted 19 October | Use their logical behavior as the test oracle. |
| G1 AWS PoC authorization | [DUC-24](https://linear.app/ducanh/issue/DUC-24) is Backlog; the G1 request in the review package is unsigned | No AWS P3/P5 execution. |
| G2 P1–P6 evidence / G3 ADR | [DUC-37](https://linear.app/ducanh/issue/DUC-37) is Backlog; P3/P5 sheets contain no observed results | Mark every P3/P5 case **NOT RUN**, not PASS. Keep implementation choices open. |
| G4 implementation approval | [DUC-36](https://linear.app/ducanh/issue/DUC-36) is Backlog | No product code, Terraform IaC or deployment. Local documentation QA is allowed. |
| Independent review | [PR #20](https://github.com/24021368-DucAnh/InfraFlow/pull/20) remains open with unresolved threads | Design and traceability issues remain In Progress; no peer sign-off inferred from author/AI comments. |

## Compatibility and outcome matrix

The outcome column describes the **v1.2 logical requirement**, not a tested AWS result. `BLOCKED` concerns an operation needing human resolution; an invalid candidate can also be rejected during read-only validation. Every row needs actual preflight and after-state evidence before a PASS claim.

| Input and precondition | Expected outcome before mutation | Planned test / source | Evidence still required |
|---|---|---|---|
| Create uses a supported Web+DB Blueprint, valid Lease policy and isolated Environment | Accept Create operation; `ACTIVE/PREPARED` is possible, with sleeping URL until Wake and health verification | BP-01/02, P3-01; Design §§1, 3–4; Contracts §§2.1–2.2, 3 | Component inventory and ownership, state/AWS observation, operation and URL result |
| Create parameter or Lease policy is invalid | Reject before cloud mutation | BP-02, P3-01; Contracts §3 | Denial response and unchanged inventory |
| Register workspace has compatible Web+DB inventory and proven owner, exclusive writer/lock, state, IAM, data and DNS handoff | Read-only Validate first; Activate only when full Sleep/Wake/Reclaim capability is proven; availability comes from AWS observation | BP-03, P3-05; Design §4; Contracts §§2.1–2.2, 3, 5 | Signed handoff reference, state/actual comparison, lock and writer proof, DNS rights |
| Register lacks DNS/URL control, full lifecycle capability, or supported DB behavior | Do not Activate MVP Register; return `DNS_CONTROL_MISSING` or `LIFECYCLE_UNSUPPORTED` as applicable | BP-04/13/15, URL-07, P3-03/04/05, P5-05; Design §§4, 7; Contracts §§3, 8 | Read-only denial and unchanged zone, cert, state and AWS inventory |
| State/AWS evidence is stale or conflicting, old writer remains, or plan touches shared resource | Reject or `BLOCKED`; no Terraform apply or direct AWS action outside permit | BP-07/09/11, P3-05/06; Contracts §§2, 5, 8 | Timestamped observations, writer/lock proof, scoped plan summary and no-mutation check |
| Wake health fails or all ALB targets are unhealthy | Public entry stays on safe status route; do not claim `AWAKE` from target health alone | URL-05/13, P5-03; Design §§5, 7–8; Contracts §§5–6, 8 | External route probes, target health, bypass assessment and rollback result |
| DNS cache or persistent connections still reach old app route during Sleep | Do not remove app or report `SLEEPING` until the approved cutover/drain oracle is met; unresolved state is `CUTOVER_UNVERIFIED` | URL-06/14, P5-04; Design §§5, 8; Contracts §§6, 8 | Timestamped resolver/client samples and reviewed threshold |
| Register is being Unregistered | Stop new operations and verify reverse state/DNS/IAM handoff; never destroy as a side effect of Unregister | CT-13-U, Design §4; Contracts §§2.1, 3, 9 | Handback, no-destroy inventory and reviewer evidence |

## G4 logical task-boundary proposal (no implementation authorization)

The following packages are planning boundaries for the later G4 implementation plan. They deliberately name logical responsibilities and acceptance cases only; exact repository paths, endpoint/payload schemas, AWS services, thresholds and Terraform modules remain unset until G2/G3 evidence and owner review. Each package must be split into small TDD tasks in DUC-36 after those inputs are approved.

| Package | Scope and dependency | Primary reviewer | Planned verification (NOT RUN) |
|---|---|---|---|
| Blueprint validation and Create inventory | Supported Web+DB inputs, Lease/policy validation, bounded Environment/resource ownership and dependency ordering; depends on DUC-25 review and G3 component choices | Đạt (state/resource scope), Hoàng (Create/API boundary) | BP-01/02/07/09; reject invalid or shared-resource scope before mutation |
| Database-preserving Sleep/Wake | DB/app dependency, persistent-data fixture, observed-vs-desired reconciliation, unsupported topology and seven-day RDS restart handling; depends on P3/G2 and G3 policy | Minh (lifecycle/failure), Đạt (AWS/state evidence) | BP-05/06/13; P3-02/03/04; no false SLEEPING/healthy claim |
| Register compatibility and handoff | Read-only validation of inventory, state, exclusive writer, ownership, lifecycle capability and DNS handoff; depends on DUC-38 and P1/P2 G2/G3 decisions; do not force Register into the Create module | Đạt (backend/lock), Minh (handoff safety) | BP-03/04/07/11/15; P3-05/06; missing proof rejects or BLOCKED without mutation |
| Stable URL and sleeping experience | Public-safe status and bounded URL-holder Wake; preserve URL ownership for Create and Register; depends on DUC-27/DUC-38 and P5/G2/G3 route choice | Hoàng (UI/API/Wake), Minh (authorization/state) | URL-01/02/03/04/07/15; P5-01/02/05; no private status leakage or unauthorized DNS mutation |
| Health-gated route cutover and recovery | Keep app traffic behind an independently verified public-route gate, handle stale DNS/persistent clients and rollback; depends on P5/G2 and G3 decision because ALB health alone can fail open | Minh (controller/rollback), Hoàng (public behavior) | URL-05/06/13/14; P5-03/04/06; all-targets-unhealthy and stale-route cases stay safe |
| Cross-package integration and evidence | Contract-test both origins and multiple lifecycle cycles; collect sanitized expected/actual, cleanup, and cost estimate-vs-actual labels; depends on the above approved packages plus DUC-33 | Reviewer not the implementing owner; group review | BP-10/12/16, URL-08/09/10/11/12/16; P3-07/08, P5-07/08; no terminal success before Verify |

**Task-boundary status:** proposal prepared for DUC-36; no package is implementation-ready or authorized. The owners must confirm boundaries/reviewers, and DUC-36 must receive explicit G4 approval before product code, Terraform IaC or deployment.

## Decisions and review still needed

| Open item | Owner / reviewer proposed in Contracts §9.1 | Required source before G3/G4 |
|---|---|---|
| Retain or migrate Register Terraform backend, exclusive lock and rollback | Đạt + Minh; Đức Anh reviews compatibility | P1/P2A/P2B comparison under G1, then [DUC-37](https://linear.app/ducanh/issue/DUC-37) decision |
| Supported DB topology and long Sleep after the RDS seven-day auto-restart | Đức Anh + Đạt; Minh reviews safety | P3-03/04 actual or approved simulation evidence, observed-versus-desired policy and cost |
| Safe public routing when all ALB targets are unhealthy; DNS/TLS authority and propagation | Đức Anh + Hoàng; Minh reviews controller boundary | P5-03/04/05 probes and a G3 routing decision |
| Wake abuse thresholds and public status projection | Hoàng + Minh; Đức Anh reviews sleeping-page boundary | P5-02 local/mock contract checks, then reviewed quantitative limits |
| Residual and one-off costs compared with 24/7 and stop-only | Hoàng + Đạt | P3/P5 inventory plus P6 prices, region, period and measured versus estimated labels |

**Next review handoff:** Đạt checks state/backend, component ownership and lock; Minh checks permit, BLOCKED and cutover failure; Hoàng checks DNS/status/Wake and cost. Record each person's actual review on [DUC-25](https://linear.app/ducanh/issue/DUC-25), [DUC-27](https://linear.app/ducanh/issue/DUC-27) or [PR #20](https://github.com/24021368-DucAnh/InfraFlow/pull/20). Until then, the W8 matrix is planning evidence only.
