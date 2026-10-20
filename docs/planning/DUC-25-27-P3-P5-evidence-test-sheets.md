# DUC-25/27 — P3 Blueprint and P5 Stable URL Evidence/Test Sheets

**Date:** 2026-10-20 · **Status:** TEST PLAN ONLY / NOT RUN · **Author:** Đức Anh (AI-assisted) · **Reviewers proposed:** Hoàng (P3/P5/cost), Đạt (state/exclusive writer), Minh (controller/safety).

These test sheets translate the design review into *repeatable verification recipes*. They **do not** choose AWS services, field names, endpoints, DNS TTLs, cost limits or approved AWS credentials. The authoritative [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) own semantics; exact sections/wire names require manual verification. External AWS constraints are marked explicitly below.

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
| Accepted implementation choice (G3), contract section (v1.2) | `NOT VERIFIED` |
| Expected result, observed result, PASS/FAIL/BLOCKED/NOT RUN | `NOT RUN` |
| Sanitized evidence + timestamps + billing observation | `NONE` |
| Rollback outcome, teardown inventory and reviewer sign-off | `NOT RUN` |

## 1. P3: Blueprint/Database lifecycle cases

| Case → acceptance IDs | Synthetic fixture and prerequisite | Probe steps after G1 (do not execute yet) | PASS oracle / failure oracle | Required evidence & cleanup |
|---|---|---|---|---|
| **P3-01** → BP-01, BP-02 | Approved supported Web+DB Blueprint parameters and one purposely unsupported parameter | Validate normal Create request; separately submit invalid parameter before any infrastructure action | Accept only authorized supported contract; invalid case rejects with no cloud mutation | Sanitized validation responses, inventory delta, expected/actual; destroy test resources **only under permit** |
| **P3-02** → BP-05, BP-06, URL-02, URL-08 | One approved Create environment with synthetic persisted DB row/hash and healthy app | Snapshot baseline data/health; Sleep using approved workflow; observe DB/compute/ingress; Wake; compare data and readiness | Data hash preserved, no early app routing, desired and actual reconciled; unsupported action must BLOCKED | Data checksum before/after (not raw data), health/duration/inventory, no secrets, teardown check |
| **P3-03** → BP-13, URL-16 | Eligible RDS DB instance/engine/topology, approved long-sleep boundary | Simulate/review the 7-day service auto-start event; a real 7-day test only if G1 explicitly authorizes the duration and budget | Controller notices drift from Desired sleep; never reports asleep solely from old operation success; documented permitted reconciliation, otherwise BLOCKED | Timestamped RDS event/Observed vs Desired, residual storage/backup price assumptions, no auto-restop assumption; verify cleanup |
| **P3-04** → BP-13 | Unsupported stop configuration (e.g. unsupported RDS topology) or missing required snapshot/backup confirmation | Request Sleep or Reclaim in safe validation/mock path with incompatible engine or missing backup | No unauthorized/destructive request is issued; validation denies/BLOCKED and reports reason | Denial audit + resource inventory unchanged, reviewer sign-off, rollback N/A |
| **P3-05** → BP-03, BP-04, BP-07, BP-15 | (A) Approved compatible test-only registered Web+DB workspace with owner/state writer handoff evidence; (B) one shared/out-of-scope component, conflicting owner or missing DNS right | For (A), verify state/backend lock, handoff and full permitted capability before any lifecycle; for (B), attempt only safe preflight/plan validation | (A) Register succeeds only after all ownership/capability evidence is confirmed; (B) reject/BLOCKED without out-of-scope mutation. Readable state alone is never ownership | Before/after sanitized inventory, exclusive writer proof per P1/P2, accepted/denial audit; cleanup/rollback of test handoff |
| **P3-06** → BP-09, BP-11 | Synthetic drift or old writer still active, duplicate operation on one environment | Reconcile before permit; schedule conflicting operations in allowed mock/testing scope | Exactly one authorized writer, no stale apply, no false success; unknown → BLOCKED | operation IDs redacted, lock/state event logs without raw tfstate |
| **P3-07** → BP-08, BP-10, BP-16 | Test environment with known backup/permit/Verify scope, plus deliberately incomplete inventory fixture | Attempt Reclaim preflight without backup; separately run permitted Reclaim/Verify only if G1 and explicit destroy scope exists | Missing backup/permit denies action; terminal Reclaimed only after AWS and Terraform inventory evidence; incomplete Verify remains unresolved | Backup confirmation reference, approved plan summary, before/after inventory, cleanup owner sign-off |
| **P3-08** → BP-12 | Same synthetic usage window for active, stop-only and deep-sleep candidates | Record region, service/instance classes, sample utilization and billable residual resources; compare estimate to measured cost if available | Transparent sources/assumptions, correct currency/time, no blanket zero-cost claim | Versioned pricing-source URL/date, telemetry, cost period, sampling limitations and teardown charges |

**External AWS constraint:** `StopDBInstance` restarts a stopped DB instance automatically after seven days and does not apply to RDS Custom or Aurora clusters; Aurora uses cluster stop/start with its own constraints. [AWS API](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_StopDBInstance.html), [AWS supported stop limitations](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automatically-stop-and-start-an-amazon-rds-db-instance-using-aws-systems-manager-maintenance-windows.html). This is input for design/P3, **not G2 evidence**.

## 2. P5: DNS, stable URL, sleeping page, Wake and cutover

| Case → acceptance IDs | Synthetic fixture and prerequisite | Probe steps after G1 (or mock) | PASS oracle / failure oracle | Required evidence & cleanup |
|---|---|---|---|---|
| **P5-01** → URL-01, URL-02 | Owned sandbox hostname and test TLS certificate, healthy app and reachable sleeping endpoint | Observe response under Awake; perform authorized Sleep; sample hostname/TLS/status and public origin | User-recognizable host stable in supported policy; only correct approved destination is served | Resolvers/HTTP/TLS checks with timestamps, destination inventory and price |
| **P5-02** → URL-03, URL-04, URL-15 | Authenticated authorized owner and anonymous/unauthorized actor; synthetic operation identifiers | Wake once and duplicate; try unauthenticated/CSRF/replayed/flooded requests in local/mocked controlled test | One permitted operation; unauthorized and duplicate requests cause no new cloud writes; no sensitive status leak | Redacted response codes/rate-limit/operation/audit; remove synthetic records |
| **P5-03** → URL-05, URL-13, BP-14 | App target group with all targets unhealthy (mock preferred before G1); front door fallback candidate | Prove ALB fail-open risk at health layer; independently test entry route remains safe under all-unhealthy and during cutover | No routing to unverified app via approved public path; document any direct-origin bypass, otherwise BLOCKED/design fail | External probes + ALB target states + routing config, negative evidence; rollback entry to safe status |
| **P5-04** → URL-06, URL-14 | Test zone with sample resolvers/clients and known initial route | Switch and restore only authorized DNS/edge route; sample resolvers and persistent sessions over interval **decided at G3** | Report actual stale routes, HTTP/TLS errors and rollback behavior without claiming zero delay | DNS record values sanitized, TTL config, propagation/error timestamps and cleanup proof |
| **P5-05** → URL-07 | Registered Web+DB with unowned DNS/cert or missing handoff evidence | Exercise preflight before route mutation | No write to unowned zone/cert, explicit compatible alternate/reject/BLOCKED according to **approved v1.2**; if missing decision mark unresolved | Preflight denial and unchanged zone/cert inventory, authorized-owner evidence |
| **P5-06** → URL-08, URL-09 | Synthetic fixture retained across two Sleep/Wake cycles; inject fail/timeout/partial return | Probe health/data/route in normal and failed Wake while client polls progress | No fake Awake, no untrusted health switch; evidence about retry/rollback and visible status | Client observations, state history, DB hash, failure records and cleanup |
| **P5-07** → URL-10, URL-11 | Concurrent approved manual/scheduled Wake or Reclaim operation on same Environment | Simulate conflict and partial Reclaim/Verify; query public routing afterward | Conflict denied/serialized; no stale app exposed after Reclaim; incomplete Verify not marked terminal success | Idempotency/lock audit + DNS/health check + final inventory |
| **P5-08** → URL-12 | Candidate front-door architecture with asleep period and synthetic comparable workload | Document recurring edge cost, certificate/DNS/data transfer and AWS resources billed in Sleep; measure if G1 permits | Cost comparison correctly includes persistent route and one-off actions; source and uncertainty stated | Region-specific pricing links, time window, bill data if verified, cleanup |

**External AWS constraint:** an Application Load Balancer *fails open* when all registered targets in a target group are unhealthy. Thus ALB target health status by itself is **not** a safe traffic-blocking guard. [AWS ALB target health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html). Choose and verify a front-door strategy only via G2/G3; prohibit bypass and record propagation/error windows.

## 3. Pass/fail discipline and approval matrix

| Classification | Rule |
|---|---|
| `PASS` | Expected and actual compared; all mandatory checks met within a *reviewed* metric/threshold where applicable; sanitized evidence and cleanup verified |
| `FAIL` | Test ran under approved scope and violated stated acceptance or caused unsafe partial operation; investigate and escalate |
| `BLOCKED` | Ownership/permit/backup/lock/DNS rights invalid or unknown; no unsafe mutation; human policy escalation needed |
| `NOT RUN` | No G1/fixture/owner approval, unexecuted test, or only conceptual reasoning; **must not be counted as PASS** |

**Do not fabricate:** explicit timeouts, numeric SLA/health thresholds, DNS TTL, resource pricing, Terraform wire names or chosen AWS deployment topology. Those require precise v1.2 mapping, AWS measurements/G2 and G3 decision.

## 4. Exact interface mapping / remaining blockers

| Contract category (semantics confirmed via DUC-34/35, not original wire text) | Mapping required from full v1.2 | Review/test owner | Status |
|---|---|---|---|
| Create Blueprint parameters/capability/ownership | Section ID, schema/types, error result for unknown component, tag ownership | Đức Anh + Hoàng | **UNVERIFIED** |
| Register Handoff/compatible workspace | State/backend owner, preflight/permit contract and denial/error mapping | Đạt + Minh | **UNVERIFIED** |
| Desired/Observed and Operation | State enum, operation transition, actor role, idempotency key, denial/conflict/error | Minh + Hoàng | **UNVERIFIED** |
| Terraform validator/permit | Policy scope, plan binding, backup evidence, fail-closed behavior and audited outcome | Đạt + Minh | **UNVERIFIED** |
| Stable URL/Wake/progress | Status visibility, anonymous vs authorized data, DNS/cert ownership, idempotent Wake, progress | Đức Anh + Hoàng | **UNVERIFIED** |
| Reclaim/Verify/Unregister | Final backup, cleanup and ownership boundary, terminal state and handback | Minh + Đạt | **UNVERIFIED** |

**Review is blocked on the exact full v1.2 document content**: Linear `list_documents` returned only an abbreviated preview and `get_document` returned empty for the authoritative two documents. We have verified the *scope/semantics categories* from DUC-34/35 and issue descriptions; exact field names, schema and section numbers must be supplied by the team, not guessed.

## 5. Audit & responsibilities

- **Đức Anh**: host P3/P5 design review, verify Blueprint/DNS component contract before adding implementable fields.
- **Hoàng**: review API/UI Wake, guest status, DNS user experience and P6 cost assumptions.
- **Đạt**: review Register/writer lock, Terraform state integrity, state ownership and backend probes.
- **Minh**: review fail-closed, backup/permit, partial failure, Reclaim and Verify.
- **Account owner**: decide G1 test scope/budget/cleanup; **project owner**: approve G3 architectural implementation choice and G4 planning after evidence.

> **Current disposition:** test sheets prepared for review; **all P3/P5 tests NOT RUN; no G1, G2, G3 or G4 approval is asserted**. Do not mark implementation done because a test matrix has been drafted.
