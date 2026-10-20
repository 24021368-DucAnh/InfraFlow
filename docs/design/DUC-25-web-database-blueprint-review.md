# DUC-25 — Web + Database Blueprint: component and safety review (W6–W7)

**Owner:** Ngô Bùi Đức Anh · **Reviewer proposal:** Trần Quý Đạt (Terraform/state) + Nguyễn Huy Minh (safety) · **Status:** REVIEW DRAFT, not an approved replacement for baseline v1.2 · **Date:** 2026-10-20

> **Purpose:** produce a reviewable, evidence-oriented blueprint/component design for [DUC-25](https://linear.app/ducanh/issue/DUC-25). The approved [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) were read in full on 21/10/2026 and remain authoritative. The references below identify approved **logical** contract sections; physical wire/API and Terraform module inputs/outputs remain for G3/G4 mapping.

## 1. Scope and non-goals

- **In MVP:** Create a supported Terraform-managed AWS Web + Database environment from an InfraFlow blueprint; support compatible AWS Terraform Web + Database environments originating from **Register**, but only after the separate ownership/state/capability handoff proves them safe.
- **Shared lifecycle:** approved operations Sleep, Wake, Reclaim and Verify belong to one lifecycle core with per-environment capability/permission preflight; origin changes preflight, not the baseline semantics.
- **Not in this deliverable:** product Terraform module, account IAM policy, executable AWS probe, architecture/spec change, arbitrary multi-cloud support, arbitrary custom Terraform components, implementation of state migration.
- **Separate tracks:** [DUC-38 Register/handoff](https://linear.app/ducanh/issue/DUC-38) and [DUC-43 backend/writer-lock PoC](https://linear.app/ducanh/issue/DUC-43). Register-compatible does **not** mean all preexisting workspaces are eligible or must share the Create module's source tree.

## 2. Logical component graph — design coverage

```text
Environment scope / owner + lease + policy (from InfraFlow control plane)
             |
          network
         /       \
      egress    database
         \       /
            app
             |
           entry  ----> Stable URL / traffic handoff (DUC-27)

Terraform workspace/backend -> managed resource set and recorded state
AWS inventory/health      -> observed resource existence and readiness
InfraFlow desired state   -> target lifecycle state and authorized operation
```

Dependency direction shown here follows DUC-25 planning baseline; **not** a final Terraform module graph or chosen AWS networking design. The distinction between Terraform configuration, Terraform state, AWS actual state and InfraFlow desired state must remain explicit.

## 3. Component responsibilities and lifecycle review matrix

| Logical unit | Contract/responsibility to verify | Awake / Create check | Sleep check (proposed test, not guaranteed action) | Wake check | Reclaim/Verify & risk |
|---|---|---|---|---|---|
| **network** | Environment-scoped VPC/subnets/route/SG boundaries, ownership inventory, external/shared resource classification | Address space/isolation, app↔DB access, ingress egress policy | Distinguish network objects retained from removable paid infrastructure | Dependencies available before app connectivity is restored | Never delete shared or outside-scope network resources; compare state/tags/AWS actual |
| **egress** | Outbound access/dependencies and chargeable NAT/other egress choices | Internet/dependency requirements validated | Can egress be removed/paused without losing critical jobs? List residual charges | Re-establish required path before health check | Resource ownership & post-delete inventory; costs vary by option |
| **database** | Data/backup/retention/ownership and DB service compatibility | Connectivity, data fixture, protection, backup policy | Only data-preserving actions with verified constraints; do **not** assume RDS stays stopped indefinitely | Restore DB availability, reconcile data and consistency | Backup+permit before destructive action; Verify recorded resources and backups |
| **app** | Compute image/runtime/health/capacity dependencies | Service works against DB; test expected responses | Determine allowed stop/deprovision semantics from baseline plus P3 experiment | Bring up after dependencies; health before traffic | Image/data retention and service endpoint drift; no accidental deletion of DB-owned data |
| **entry** | Public ingress, cert/domain association, ALB/edge capability, health cutover | URL routes only to healthy app | Preserve stable customer-facing URL by approved sleeping-route strategy | Do not switch from sleeping page to unhealthy app | Detach/cert/DNS ownership and cost; see DUC-27 |

**Cost classification proposal:** for each component record (a) billed while active, (b) retained fixed cost while asleep, (c) pay-per-use, (d) possible one-off snapshot/storage charges. Fill this table from AWS region, P3/P6 evidence, not guesses. NAT, ALB, RDS and storage behavior may dominate total cost; the blueprint's benefit must be **measured** against 24/7 and stop-only.

### AWS feasibility notes and component evidence (review addendum)

**Source distinction:** the table above comes from DUC-25 planning scope. The next items are *external AWS constraints to verify*; they do not amend v1.2 semantics or select a particular implementation.

| Component | Preflight/input evidence (semantic, not field names) | Observed output and safe stop/rollback checks | Residual cost or restriction to measure |
|---|---|---|---|
| network | Approved owner/resource boundary, subnets, shared dependency inventory, SG/route constraints | Diff must not mutate external/shared VPC dependencies; verify AWS inventory and state after operation | VPC endpoints, IP/traffic charges and egress requirements vary by topology |
| egress | Required outbound destinations, billable NAT choice and app/database dependency | Check whether it can be detached safely and then recovered; failed egress reconnection must not route unhealthy app | NAT or alternative connection charges may continue even when app is stopped |
| database | Engine/topology supports intended operation, confirmed owner, backup/retention evidence, persistent data fixture | Record AWS DB state transitions and independent data read after Wake; on unsupported/unknown topology deny or BLOCKED | **RDS DB-instance stop is temporary (automatic restart after 7 days)**; retained storage/backup still billed. Read replica / Multi-AZ restrictions require review |
| app | Reviewed software/image and stateful data map, dependencies, readiness probe; exclusive writer for IaC-controlled changes | Assert app health **and DB readiness** before public cutover; scope app rollback and restore status | Compute/EBS/ALB/capacity charges may not become zero while asleep |
| entry | Proven zone/certificate/hostname and environment ownership; public status data classification | Confirm reversible routing authority and safe fallback; ALB health alone cannot enforce a health gate if all targets unhealthy | Edge/DNS/ALB/cert and data-transfer charges may remain |

**RDS-specific edge case:** A stopped Amazon RDS DB instance automatically restarts after seven days; the operation and supported DB types differ between RDS instances, Aurora clusters, RDS Custom and read replicas. Therefore 'Sleep' cannot assume DB remains stopped indefinitely. The lifecycle controller must *observe and reconcile* AWS changes with authorized policy while protecting data; whether/how to renew Sleep without restarting or breaching constraints requires P3 evidence and G3 design choice. Do **not** propose periodic restop as an approved solution. External references: [StopDBInstance API](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_StopDBInstance.html), [AWS RDS stop/start limitations](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automatically-stop-and-start-an-amazon-rds-db-instance-using-aws-systems-manager-maintenance-windows.html).

**ALB-specific edge case:** If the implementation exposes an ALB directly while every registered target is unhealthy, AWS can route to all of them ('fail open'). Therefore application availability must be guarded *upstream of any potentially fail-open route*; the exact safe entry mechanism is a P5/G3 decision. Reference: [ALB target-group health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html).

**Cost evidence form (P6; values intentionally not invented):** for each actual AWS resource classify owner/env binding, hourly/usage/storage/transfer pricing source, region/currency/as-of date, active spend, sleep retained spend, one-off snapshot/restore spend, cleanup verification, and estimate versus measured totals. A claim of savings requires a clear observation window and comparable workload assumptions.

## 4. Ownership, state and permission boundaries

1. Create source belongs to the reviewed InfraFlow blueprint. Each Environment must have an unambiguous Terraform state/workspace/backend and a finite authoritative ownership/resource set. Interface Contracts v1.2 §2.1 fixes the logical `Environment`, `Observation` and `HandoffRecord` information; physical Terraform structure and tag naming are not fixed there.
2. Register does **not** silently transfer ownership because state is readable. Verify compatible Web+DB topology, backend access, exclusive writer, permissions, external/shared resources, domain authority and rollback before allowing destructive capabilities.
3. No operation may assume a successful Terraform command implies AWS actual convergence. Verify post-operation inventory, service health and environmental ownership.
4. Validator denies operations if missing permit/backup, unreadable or out-of-scope plan, unverified ownership, unknown drift, conflicting writer or unreconciled partial completion. Report BLOCKED / review-needed as required by the authoritative baseline.
5. Terraform changes should be reviewed and executed by the **authorized executor** only. The control-plane/API must not become a second uncontrolled state writer. The exact lock/lease mechanism is a P1/P2A/P2B G2/G3 implementation decision.
6. Data retention is a policy obligation, not inferred from `terraform destroy` or the presence of an RDS snapshot. Define who verifies backups/restores and evidence of finished cleanup.

## 5. Boundary contract checklist (approved logic; physical wire pending)

| Boundary | Producer → consumer | Approved v1.2 source and logical data/result | Physical wire status |
|---|---|---|---|
| Create request → Blueprint validation | Web/API → onboarding | Technical Design §§3–4; Contracts §§2.1, 3: `Lease`, Blueprint/version, Environment list, policy and schedule; return IDs/`operationId`; invalid input rejects before cloud mutation | Endpoint, JSON types and Terraform inputs **PENDING G4** |
| Component inventory/capability | Blueprint/Register adapter → lifecycle preflight | Technical Design §§3–4; Contracts §§2.1–2.2, 3: `componentInventory`, `resourceOwnershipClass`, `capabilities`, `HandoffRecord`; Register Activate requires complete handoff and all three lifecycle capabilities | Adapter schema and tags **PENDING G3/G4** |
| Desired/Observed & Operation | Lease/API/controller → executor + Web | Technical Design §§2, 5; Contracts §§2–4: `desiredState`, `terraformStateObservation`, `awsObservation`, `Operation`, three separate status axes; same-key/same-payload returns existing `operationId`, conflicting goal denies | Event transport and physical types **PENDING G4** |
| Plan review/permit | Validator/policy → executor | Technical Design §§3, 5; Contracts §§2.1, 5, 8: `ScopedPermit` binds operation, action, resource scope, ownership class, allowed steps, plan fingerprint and evidence; unsafe or stale evidence → `BLOCKED` | Permit encoding and AWS allowlist representation **PENDING G4** |
| Health/DNS | Controller/entry → sleeping/status service | Technical Design §§5–7; Contracts §§3, 6, 8: stable URL; safe public status; URL holder may request Wake with valid Lease and abuse limits; `HEALTH_GATE_FAILED`/`CUTOVER_UNVERIFIED` prevent false Awake/Sleep | Route mechanism, status endpoint and numeric limits **PENDING G2/G3/G4** |
| Reclaim/Verify | Executor/inventory → API/audit | Technical Design §§4–5; Contracts §§2.1, 3, 5, 8: Lease version/confirmation, backup, scoped plan and AWS actions; `RECLAIMED` only after Terraform and AWS Verify; `VERIFY_INCOMPLETE` otherwise | Executor messages and evidence storage **PENDING G4** |

**Do not generate `components.yaml`, Terraform modules or API endpoints from this draft.** The named logical fields above are copied from Contracts v1.2; no physical wire format is claimed. See [P3/P5 test-sheet supplement](../planning/DUC-25-27-P3-P5-evidence-test-sheets.md). Complete physical interface mapping after G2/G3 **in the implementation plan submitted for G4 approval**; do not start product code or IaC before that approval.

## 6. Acceptance scenarios / test catalogue (planned; all NOT RUN)

| ID | Scenario | Expected design-level observation | Gate/probe |
|---|---|---|---|
| BP-01 | New supported Create environment | Owner/lease bound to bounded resource set; configuration checked | W7 review → G4 implementation |
| BP-02 | Unsupported blueprint parameters | Rejected with clear validation, no AWS action | Contract test after G4 |
| BP-03 | Register compatible Web+DB | Only after state writer/ownership/handoff/capability pass | P1/P2 → G2/G3 |
| BP-04 | Register incompatible/unverifiable workspace | Reject or BLOCKED, no destruction | P1/P2/P4 |
| BP-05 | Sleep Web+DB | Requested cost-saving state retains required data and stable URL | P3/P5/P6 |
| BP-06 | Wake data-preserved environment | DB/app healthy before traffic; preserve persisted fixture | P3/P5 |
| BP-07 | Shared/out-of-scope resource in plan | Validator denies; no apply/destroy | P4 |
| BP-08 | Backup incomplete/unknown | Destructive operation denied; BLOCKED or equivalent v1.2 outcome | P4 |
| BP-09 | Terraform state vs AWS drift | Detect, report and choose safe remediation; no false success | P1/P2/P4 |
| BP-10 | Reclaim + Verify | Backup/permit before deletion; verify actual resources and state before terminal success | P4 + E2E |
| BP-11 | Two operations/old writer | Exactly one authorized writer; different-goal conflict returns `CONCURRENT_OPERATION` without queueing; same-goal retry returns the existing operation | P1/P2 |
| BP-12 | Cost accounting awake vs asleep | Show measured/bounded assumptions and residual charges | P6 |
| BP-13 | DB auto-start after seven days or unsupported stop topology | Desired and AWS Observed mismatch is surfaced; no false SLEEPING claim, review-safe reconciliation/operation policy | P3/P4 + AWS RDS constraint |
| BP-14 | All ALB targets unhealthy during/after Wake | No unauthorized direct app serving through fail-open; independent public cutover gate or explicit BLOCKED | P3/P5 |
| BP-15 | Registered Web+DB includes external/shared route or unmanaged cert | No destructive/URL mutation outside owner-controlled scope | P2/P4/P5 |
| BP-16 | Final Verify inventory incomplete/unavailable | Terminal Reclaimed status not asserted; evidence gap and safe escalation recorded | P4 + E2E |

**Current test state:** NOT RUN for BP-01…BP-16. No AWS resource has been created or destroyed as part of this document.

**Execution gates:** All AWS PoC probes require explicit **G1** authorization (account/region/IAM/budget/cleanup). Real product code/IaC, Terraform deployment, and the implementing interface/file mapping require approved **G4** after reviewed G2/G3 evidence.

## 7. Review questions, ownership and handoff

| Question to confirm | Responsible / reviewer | Evidence source |
|---|---|---|
| Exact topology support and component names/types, Terraform configuration split and tags | Đức Anh + Đạt | Full v1.2, DUC-25, P3 |
| State/backend strategy for Register and exclusive writer | Đạt + Minh | DUC-43 P1/P2 → DUC-37 |
| Sleep-preserved DB/data, NAT/ALB and cost behavior in chosen AWS region | Đức Anh + Hoàng | DUC-45 P3/P6 |
| Permit, backup, deletion and hard-fail behavior | Minh + Đạt | DUC-44 P4 |
| DNS authority, URL strategy and health/cutover | Đức Anh + Hoàng | DUC-27, P5 |

## 8. Definition of done for DUC-25 DESIGN task

- [x] Prepared responsibilities/dependencies, ownership/permissions and lifecycle/cost comparison matrix as a review draft.
- [x] Prepared scenario and fail-closed catalogue with traceability to PoC P1–P6; status NOT RUN.
- [x] Full v1.2 section and logical contract mapping added; physical wire remains explicitly pending.
- [ ] Đạt/Minh independently confirm section mapping and correct any mismatches.
- [ ] Group reviews component behavior, DB retention, costs and Register boundary from test evidence; G2/G3 remains open until evidence exists.
- [ ] Record approved version/decision or requested revisions in DUC-25; only then mark design Done. Product code/IaC remains blocked until G4.
