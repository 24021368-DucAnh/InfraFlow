# G1 — InfraFlow AWS PoC Authorization and P1–P6 Review Package (DRAFT)

**Prepared:** 2026-10-21 · **Owner for permission decision:** AWS account owner (must be confirmed) · **Technical coordinator:** Đạt, Đức Anh · **Status:** REQUEST TEMPLATE ONLY; **G1 NOT APPROVED / NO AWS ACTIONS AUTHORIZED**

**Primary tracking:** [DUC-24](https://linear.app/ducanh/issue/DUC-24), [DUC-43](https://linear.app/ducanh/issue/DUC-43), [DUC-44](https://linear.app/ducanh/issue/DUC-44), [DUC-45](https://linear.app/ducanh/issue/DUC-45). G2/G3 disposition: [DUC-37](https://linear.app/ducanh/issue/DUC-37). [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) are the approved *logic baseline* (G0), not permission to operate cloud resources.

## 1. Approval decision form — do not pre-fill unverified values

| Required entry | Current value | Evidence location / decision owner |
|---|---|---|
| Account owner identity and test account alias (**not raw AWS account ID in public repo**) | **PENDING** | Private DUC-24 G1 approval evidence |
| Account type and bounded tenant/resource scope | **PENDING** | AWS owner must confirm sandbox and no production/shared workloads |
| AWS region and allowed services/sizes/quotas | **PENDING** | Owner-approved region, ECR/EC2/ASG/ALB/RDS/Route 53/IAM/etc *only if explicitly needed* |
| IAM execution role and least privilege, trust boundary, credential expiry | **PENDING** | Security reviewer checks role in private configuration; no keys in public issue |
| Budget ceiling, remaining account credits, charges/alerts and stop condition | **PENDING** | Written currency, upper test-cost expectation, alert recipient and manual shutdown plan |
| Domain/test zone and ACM certificate rights | **PENDING** | Owner proofs DNS write or selected alternative; do not touch real domains |
| Terraform backend/workspace origin and isolated writer | **PENDING** | State test clone/copy, backup/restore authority, lock check, old-writer exclusion |
| Allowed destructive actions and backup/restore checks | **PENDING** | Explicit allowlist per test resource/workspace, no real/shared/production deletion |
| Test slot/start/expiry, resource expiry and daily cleanups | **PENDING** | Approved schedule, monitoring owner and stop/cleanup contact |
| Evidence storage/privacy/redaction and proof of cleanup | **PENDING** | Storage destination with restricted access; sanitized public links only |
| G1 approver sign-off (identity/date/scope/version) | **NO SIGN-OFF** | Owner must approve in Linear/private record |

**G1 rule:** Do not run AWS PoC before **all required approvals** have been collected and validated, especially IAM, budget, state ownership, data/backup, domain rights and cleanup. A checked box in GitHub, a draft budget alert or an AI answer is **not** consent or technical enforcement. AWS Budgets/alerts alone do not guarantee an instantaneous hard spending limit; choose enforceable controls/stop responsibility appropriate to the approved account.

## 2. Minimum PoC matrix aligned to G0 design

| Probe | Hypothesis (to verify, not assert) | Negative cases / stop criteria | Actual evidence needed | Technical owner/reviewer |
|---|---|---|---|---|
| **P1:** Terraform state and ownership | Read test state, compare Terraform-managed resources with real inventory, maintain writer exclusivity | State unreadable, drift, shared/unowned resources, writer lock conflict → no mutation/BLOCKED | Sanitized state/plan summary, IAM denial, lock events, inventory before/after, rollback | Đạt / Minh |
| **P2A:** keep existing backend on Register | Handoff can isolate writers and preserve plan consistency while keeping test backend | Old writer can still apply, no exclusive lock, privilege uncertainty, plan drift → reject/BLOCKED | Pre/post plan summaries, test backend lock, authorization changes, evidence of fencing and rollback | Đạt / Minh |
| **P2B:** migration alternative | Controlled test-state copy/migration supports backup, new exclusive writer, consistent plan and restore | Unrecoverable state, wrong version, ghost resources, two active writers, plan change → stop/rollback; never destroy real resources | Backup verification, lock trace, plan comparison, safe restore and cleanup | Đạt / Minh |
| **P3:** Web+DB, data-preserving Sleep/Wake | Supported selected AWS DB/app topology can transition while retaining data/health | Unsupported stop topology, RDS 7-day auto-start drift, data loss, app unhealthy → BLOCKED/FAIL | [P3 test sheets](DUC-25-27-P3-P5-evidence-test-sheets.md), DB fixture hash, AWS health before/after and cost | Hoàng / Đức Anh |
| **P4:** guardrails, Reclaim/Verify | Ownership, backup, scoped permit, stable state and inventory verification prevent unauthorized deletion | Missing backup/permit, shared resource, unknown drift, partial remove, no Verify → stop/BLOCKED | Denial paths, permitted synthetic cleanup, inventory before/after, audit/failure matrix | Minh / Đạt |
| **P5:** stable URL/health cutover | Sleep status endpoint and authorized Wake can preserve supported URL without exposing unhealthy origins | ALB all targets unhealthy fail-open, stale DNS/TLS, unknown domain ownership, anonymous Wake → safe fallback or BLOCKED | [P5 test sheets](DUC-25-27-P3-P5-evidence-test-sheets.md), external TLS/HTTP/resolver observations, rollback | Hoàng + Đức Anh / Minh |
| **P6:** Cloud cost model | Compare baseline 24/7 vs stop-only vs InfraFlow with residual charges | Unpriced retained resource, unverifiable spend, hidden NAT/ALB/RDS/backup costs → mark UNKNOWN | Region/date/currency-specific pricing, sampled usage, bounded period, actual AWS bill if allowed | Hoàng / Đức Anh |

**Dependency order:** G1 permission → P1/P2 for safe Register state assumptions → P3/P4/P5/P6 within explicitly isolated approved scopes → G2 review (pass/fail with evidence) → G3 ADR decisions, or BLOCKED/alternate if not feasible. Exact probe ordering can be adjusted by the approved PoC plan, but never bypass G1 or old-writer fencing.

## 3. Minimal evidence record for each actual probe

```text
PoC_ID: P1 / P2A / P2B / P3 / P4 / P5 / P6
Source_requirement: DUC-xx + approved v1.2 section/table (pending full text)
G1_approval_id_and_expiry: PENDING
Operator_and_independent_reviewer: PENDING
Sandbox_scope: private reference (no AWS identifiers in public GitHub)
Preconditions: account/region/IAM/workspace/ownership/backup/lease/domain/budget
Expected_observation: write BEFORE running
Negative_or_STOP_condition: write BEFORE running
Steps_executed_and_timestamps: NOT RUN
Actual_observation: NOT RUN
Result: NOT RUN | PASS | FAIL | BLOCKED
Sanitized_evidence_uri: NONE
Backups_and_rollback_outcome: NOT RUN
Cleanup_inventory_and_spend: NOT RUN
Reviewer_decision: PENDING
```

**Do not upload raw Terraform state/saved plan, access keys, RDS credentials, billing identifiers, private DNS data, real tenant workloads or unredacted logs to the PUBLIC repository.** Store them only in owner-approved restricted storage and link sanitized summaries.

## 4. Approver's go/no-go checklist

- [ ] Signed G1 scope names the account owner, valid test-account alias, IAM role, budget and stop owner.
- [ ] Test-only workspace/synthetic data and sole authorized writer have been verified; backup/restore proof exists.
- [ ] Defined bounded resource inventory and destructive-action list; protected shared resources excluded.
- [ ] Region/service quotas, DNS/cert authority, scheduled test slot and expiry, cleanup/rollback operator are approved.
- [ ] Each permitted probe defines preconditions, actual negative test, stop triggers and evidence owner.
- [ ] All public artifacts/screen captures can be sanitized; private evidence storage and access are approved.
- [ ] G1 approval URL and approving human decision are linked to DUC-24.

**All boxes currently unchecked.** No AWS command, Terraform state change, billing exposure or destructive operation has been executed by preparing this form.

## 5. Rulings and deferred decisions

- **Ruling:** Do not pick a Terraform state backend, AWS workflow executor, edge routing architecture, SQL engine/topology or numerical health/DNS thresholds from a template. Those are implementation choices tested at G2 and selected at G3, within the fixed v1.2 semantics.
- **Ruling:** Source text v1.2 not fully retrievable from Linear via this connection. Any exact contract fields/permissions for the probes must be copied and reviewed against the owner's canonical docs; DUC-34/35 are summaries only.
- **Ruling:** G4 product implementation plan must be a separate, reviewed artifact after G2/G3. This G1 package is neither G4 approval nor permission to deploy.

## 6. Hand-off actions

| Action | Owner | Required next artifact/status |
|---|---|---|
| Complete and sign G1 form privately | AWS account owner + Đức Anh/Đạt | Human approval link in DUC-24 |
| Prepare P1/P2A/P2B state backend test details | Đạt, reviewed by Minh | DUC-43, NOT RUN until G1 |
| Prepare P4 safety/backup/Verify detailed matrix | Minh, reviewed by Đạt | DUC-44, NOT RUN until G1 |
| Check P3/P5/P6 experiment and cost evidence design | Hoàng + Đức Anh | DUC-45, P3/P5 sheets, NOT RUN until G1 |
| Review G2 PoC outcomes and decide only implementation variants | Whole group | DUC-37 + ADR, preserve v1.2 or explicitly approve version change |
| Prepare exact implementation plan and request G4 approval | Đức Anh | DUC-36; no product code before approval |
