# DUC-25/27 — P3 Blueprint and P5 Stable URL Evidence/Test Sheets

**Date:** 2026-10-20 · **Status:** TEST PLAN ONLY / NOT RUN · **Author:** Đức Anh (AI-assisted) · **Reviewers proposed:** Hoàng (P3/P5/cost), Đạt (state/exclusive writer), Minh (controller/safety).

These test sheets translate the design review into *repeatable verification recipes*. They **do not** choose AWS services, physical endpoints, DNS TTLs, cost limits or approved AWS credentials. The authoritative [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) were read in full on 21/10/2026; §2.1 fixes logical fields while physical wire mapping remains pending G4. External AWS constraints are marked explicitly below.

## 0. Mandatory gate and fixtures

- **No AWS action before G1.** The AWS account owner must approve account/region, authorized IAM identity, cost ceiling/alerts, test slot/duration, resource scope, synthetic data, DNS/test zone ownership, rollback, expiration and cleanup reviewer.
- **G2/G3 are evidence/decision gates**, not a substitute for G1. No product code/IaC or deployment before approved G4. Before approval only write test sheets and use local/mock reasoning.
- All tests must use an **isolated sandbox** and synthetic non-sensitive fixtures. No real tenant state/workspace, unrelated shared AWS resource, production domain, secrets, raw Terraform state or saved plans in public GitHub.
- **Preflight evidence:** reviewer-verified owner, resource inventory, one authorized Terraform state writer, known data retention/backup, DNS/cert authority, initial observed state and baseline version. Missing/unknown → BLOCKED/NOT RUN; do not attempt destructive operations.
- **Public safety:** do not paste account ID, VPC IDs, DB endpoints, cert identifiers, internal addresses, API bearer tokens, raw logs or unredacted billing screenshots. Evidence links here must be sanitized and stored only in an approved private location.

### Approved test-run record (complete before running)

| Field | Recorded value |
|---|---|
| Test case, date/time, runner, reviewer | `NOT RUN / UNASSIGNED` |
| G1 approval link + scope + expires at | `NOT APPROVED / UNKNOWN` |
| Authorized sandbox/region/IAM role reference | `NOT PROVIDED — private approval only` |
| Cost ceiling and stop/cleanup threshold | `UNDECIDED by account owner` |
| Synthetic dataset checksum before operations | `NOT RUN` |
| Accepted implementation choice (G3), contract section (v1.2) | `G3 NOT DECIDED; logical source mapped in DUC-40` |
| Expected result, observed result, PASS/FAIL/BLOCKED/NOT RUN | `NOT RUN` |
| Sanitized evidence + timestamps + billing observation | `NONE` |
| Rollback outcome, teardown inventory and reviewer sign-off | `NOT RUN` |

## 1. P3: Blueprint/Database lifecycle cases

| Case → acceptance IDs | Synthetic fixture and prerequisite | Probe steps after G1 (do not execute yet) | PASS oracle / failure oracle | Required evidence & cleanup |
|---|---|---|---|---|
| **P3-01** → BP-01, BP-02 | Approved supported Web+DB Blueprint parameters and one purposely unsupported parameter | Validate normal Create request; separately submit invalid parameter before any infrastructure action | Accept only authorized supported contract; invalid case rejects with no cloud mutation | Sanitized validation responses, inventory delta, expected/actual; destroy test resources **only under permit** |
| **P3-02** → BP-05, BP-06, URL-02, URL-08 | One approved Create environment with synthetic persisted DB row/hash and healthy app | Snapshot baseline data/health; Sleep using approved workflow; observe DB/compute/ingress; Wake; compare data and readiness | Data hash preserved, no early app routing, desired and actual reconciled; unsupported action must BLOCKED | Data checksum before/after (not raw data), health/duration/inventory, no secrets, teardown check |
| **P3-03** → BP-13, URL-16 | Eligible RDS DB instance/engine/topology, approved long-sleep boundary | Simulate/review the 7-day service auto-start event; a real 7-day test only if G1 explicitly authorizes the duration and budget | Controller notices drift from Desired sleep; never reports asleep solely from old operation success; documented permitted reconciliation, otherwise BLOCKED | Timestamped RDS event/Observed vs Desired, residual storage/backup price assumptions, no auto-restop assumption; verify cleanup |
| **P3-04** → BP-13 | Unsupported stop configuration (for example, a DB instance with a read replica) or missing required snapshot/backup confirmation | Request Sleep or Reclaim in safe validation/mock path with incompatible topology or missing backup | No unauthorized/destructive request is issued; validation denies/BLOCKED and reports reason | Denial audit + resource inventory unchanged, reviewer sign-off, rollback N/A |
| **P3-05** → BP-03, BP-04, BP-07, BP-15 | (A) Approved compatible test-only registered Web+DB workspace with owner/state writer handoff evidence; (B) one shared/out-of-scope component, conflicting owner or missing DNS right | For (A), verify state/backend lock, handoff and full permitted capability before any lifecycle; for (B), attempt only safe preflight/plan validation | (A) Register succeeds only after all ownership/capability evidence is confirmed; (B) reject/BLOCKED without out-of-scope mutation. Readable state alone is never ownership | Before/after sanitized inventory, exclusive writer proof per P1/P2, accepted/denial audit; cleanup/rollback of test handoff |
| **P3-06** → BP-09, BP-11 | Synthetic drift or old writer still active, duplicate operation on one environment | Reconcile before permit; schedule conflicting operations in allowed mock/testing scope | Exactly one authorized writer, no stale apply, no false success; unknown → BLOCKED | operation IDs redacted, lock/state event logs without raw tfstate |
| **P3-07** → BP-08, BP-10, BP-16 | Test environment with known backup/permit/Verify scope, plus deliberately incomplete inventory fixture | Attempt Reclaim preflight without backup; separately run permitted Reclaim/Verify only if G1 and explicit destroy scope exists | Missing backup/permit denies action; terminal Reclaimed only after AWS and Terraform inventory evidence; incomplete Verify remains unresolved | Backup confirmation reference, approved plan summary, before/after inventory, cleanup owner sign-off |
| **P3-08** → BP-12 | Same synthetic usage window for active, stop-only and deep-sleep candidates | Record region, service/instance classes, sample utilization and billable residual resources; compare estimate to measured cost if available | Transparent sources/assumptions, correct currency/time, no blanket zero-cost claim | Versioned pricing-source URL/date, telemetry, cost period, sampling limitations and teardown charges |

**External AWS constraint:** RDS automatically restarts a stopped DB instance after seven consecutive days; storage and backup charges continue. Supported engines/topologies vary: the current RDS User Guide includes RDS Custom for SQL Server, while DB instances with read replicas cannot be stopped. Aurora has a separate cluster stop/start path. Test the **chosen** topology rather than treating all RDS Custom or Multi-AZ variants as unsupported. [AWS RDS stop guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html). This is input for design/P3, **not G2 evidence**.

## 2. P5: DNS, stable URL, sleeping page, Wake and cutover

| Case → acceptance IDs | Synthetic fixture and prerequisite | Probe steps after G1 (or mock) | PASS oracle / failure oracle | Required evidence & cleanup |
|---|---|---|---|---|
| **P5-01** → URL-01, URL-02 | Owned sandbox hostname and test TLS certificate, healthy app and reachable sleeping endpoint | Observe response under Awake; perform authorized Sleep; sample hostname/TLS/status and public origin | User-recognizable host stable in supported policy; only correct approved destination is served | Resolvers/HTTP/TLS checks with timestamps, destination inventory and price |
| **P5-02** → URL-03, URL-04, URL-15 | Valid URL visitor with active Lease and Wake capability, plus invalid URL/expired Lease/absent capability and manager-only action attempts; synthetic operation identifiers | Request Wake once and duplicate; test conflicting key payload, replay/CSRF/rate abuse and private-status read in local/mocked scope | Valid URL visitor can request bounded Wake without AWS account; same request/same goal yields one operation; invalid/abusive or manager-only action causes no new cloud write; no private status leak | Redacted Lease/capability decision, operation/status/audit and rate-limit evidence; remove synthetic records |
| **P5-03** → URL-05, URL-13, BP-14 | App target group with all targets unhealthy (mock preferred before G1); front door fallback candidate | Prove ALB fail-open risk at health layer; independently test entry route remains safe under all-unhealthy and during cutover | No routing to unverified app via approved public path; document any direct-origin bypass, otherwise BLOCKED/design fail | External probes + ALB target states + routing config, negative evidence; rollback entry to safe status |
| **P5-04** → URL-06, URL-14 | Test zone with sample resolvers/clients and known initial route | Switch and restore only authorized DNS/edge route; sample resolvers and persistent sessions over interval **decided at G3** | Report actual stale routes, HTTP/TLS errors and rollback behavior without claiming zero delay | DNS record values sanitized, TTL config, propagation/error timestamps and cleanup proof |
| **P5-05** → URL-07 | Registered Web+DB with unowned DNS/cert or missing handoff evidence | Exercise read-only Validate/preflight before route mutation | No write to unowned zone/cert and **no Register Activate** for MVP without DNS/URL control (Technical Design §4; Contracts §§3, 8 `DNS_CONTROL_MISSING`) | Preflight denial and unchanged zone/cert inventory, authorized-owner evidence |
| **P5-06** → URL-08, URL-09 | Synthetic fixture retained across two Sleep/Wake cycles; inject fail/timeout/partial return | Probe health/data/route in normal and failed Wake while client polls progress | No fake Awake, no untrusted health switch; evidence about retry/rollback and visible status | Client observations, state history, DB hash, failure records and cleanup |
| **P5-07** → URL-10, URL-11 | Concurrent approved manual/scheduled Wake or Reclaim operation on same Environment | Simulate different-goal conflict, same-goal retry and partial Reclaim/Verify; query public routing afterward | Different-goal conflict returns `CONCURRENT_OPERATION` without queueing; same-goal retry returns the existing operation; no stale app exposed after Reclaim; incomplete Verify not marked terminal success | Idempotency/lock audit + DNS/health check + final inventory |
| **P5-08** → URL-12 | Candidate front-door architecture with asleep period and synthetic comparable workload | Document recurring edge cost, certificate/DNS/data transfer and AWS resources billed in Sleep; measure if G1 permits | Cost comparison correctly includes persistent route and one-off actions; source and uncertainty stated | Region-specific pricing links, time window, bill data if verified, cleanup |

**External AWS constraint:** an Application Load Balancer *fails open* when all registered targets in a target group are unhealthy. Thus ALB target health status by itself is **not** a safe traffic-blocking guard. [AWS ALB target health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html). Choose and verify a front-door strategy only via G2/G3; prohibit bypass and record propagation/error windows.

## 2.1. Canonical primary coverage (one planned owner recipe per acceptance ID)

The P3/P5 tables above may mention one ID in multiple experiments as a **secondary observation**. This matrix assigns exactly one primary evidence owner recipe to each of the 32 acceptance IDs. It is a planning map, **not** a record that any recipe ran.

| Blueprint ID | Primary recipe | URL ID | Primary recipe |
|---|---|---|---|
| BP-01 | P3-01 | URL-01 | P5-01 |
| BP-02 | P3-01 | URL-02 | P5-01 |
| BP-03 | P3-05 | URL-03 | P5-02 |
| BP-04 | P3-05 | URL-04 | P5-02 |
| BP-05 | P3-02 | URL-05 | P5-03 |
| BP-06 | P3-02 | URL-06 | P5-04 |
| BP-07 | P3-05 | URL-07 | P5-05 |
| BP-08 | P3-07 | URL-08 | P5-06 |
| BP-09 | P3-06 | URL-09 | P5-06 |
| BP-10 | P3-07 | URL-10 | P5-07 |
| BP-11 | P3-06 | URL-11 | P5-07 |
| BP-12 | P3-08 | URL-12 | P5-08 |
| BP-13 | P3-03 | URL-13 | P5-03 |
| BP-14 | P5-03 | URL-14 | P5-04 |
| BP-15 | P3-05 | URL-15 | P5-02 |
| BP-16 | P3-07 | URL-16 | P3-03 |

## 3. Pass/fail discipline and approval matrix

| Classification | Rule |
|---|---|
| `PASS` | Expected and actual compared; all mandatory checks met within a *reviewed* metric/threshold where applicable; sanitized evidence and cleanup verified |
| `FAIL` | Test ran under approved scope and violated stated acceptance or caused unsafe partial operation; investigate and escalate |
| `BLOCKED` | Ownership/permit/backup/lock/DNS rights invalid or unknown; no unsafe mutation; human policy escalation needed |
| `NOT RUN` | No G1/fixture/owner approval, unexecuted test, or only conceptual reasoning; **must not be counted as PASS** |

**Do not fabricate:** explicit timeouts, numeric SLA/health thresholds, DNS TTL, resource pricing, Terraform wire names or chosen AWS deployment topology. Those require precise v1.2 mapping, AWS measurements/G2 and G3 decision.

## 4. Exact interface mapping / remaining blockers

| Contract category | Full v1.2 logical source and pending implementation detail | Review/test owner | Status |
|---|---|---|---|
| Create Blueprint parameters/capability/ownership | Technical Design §§3–4; Contracts §§2.1–2.2, 3; physical Blueprint inputs and endpoint remain G4 work | Đức Anh + Hoàng | **BASELINE LOGIC MAPPED; physical wire PENDING** |
| Register Handoff/compatible workspace | Technical Design §4; Contracts §§2.1–2.2, 3, 5, 8; backend selection needs G2/G3 | Đạt + Minh | **BASELINE LOGIC MAPPED; backend PENDING** |
| Desired/Observed and Operation | Technical Design §§2, 5; Contracts §§2–4, 8; three status axes and idempotency are fixed, transport pending | Minh + Hoàng | **BASELINE LOGIC MAPPED; physical wire PENDING** |
| Terraform validator/permit | Technical Design §§3, 5; Contracts §§2.1, 5, 8; `ScopedPermit` and deny semantics fixed, implementation pending | Đạt + Minh | **BASELINE LOGIC MAPPED; physical wire PENDING** |
| Stable URL/Wake/progress | Technical Design §§1, 5–7; Contracts §§2.2, 3, 6, 8: URL visitor may request bounded Wake, public status restricted, `operationId`/progress and health gate | Đức Anh + Hoàng | **BASELINE LOGIC MAPPED; physical wire/limits PENDING** |
| Reclaim/Verify/Unregister | Technical Design §§4–5; Contracts §§2.1, 3, 5, 7–9; `CT-13-U` handback and `CT-14-R` recovery cases are planned in G1 package | Minh + Đạt | **BASELINE LOGIC MAPPED; tests NOT RUN** |

**Review status:** Full v1.2 documents were retrieved and read on 21/10/2026; [DUC-40 traceability register](DUC-40-v12-contract-traceability-register.md) carries section-level logic mapping. Physical endpoint/payload types, topology-specific AWS behavior and thresholds still require G2/G3/G4 work and independent team review.

## 5. Audit & responsibilities

- **Đức Anh**: host P3/P5 design review, verify Blueprint/DNS component contract before adding implementable fields.
- **Hoàng**: review API/UI Wake, guest status, DNS user experience and P6 cost assumptions.
- **Đạt**: review Register/writer lock, Terraform state integrity, state ownership and backend probes.
- **Minh**: review fail-closed, backup/permit, partial failure, Reclaim and Verify.
- **Account owner**: decide G1 test scope/budget/cleanup; **project owner**: approve G3 architectural implementation choice and G4 planning after evidence.

> **Current disposition:** test sheets prepared for review; **all P3/P5 tests NOT RUN; no G1, G2, G3 or G4 approval is asserted**. Do not mark implementation done because a test matrix has been drafted.
