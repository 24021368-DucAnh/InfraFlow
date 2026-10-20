# DUC-27 — Stable URL, Sleeping Page, Wake & Health-Gated Cutover (W7)

**Owner:** Ngô Bùi Đức Anh · **Reviewer proposal:** Hà Hải Hoàng (UI/API) + Nguyễn Huy Minh (controller/safety) · **Status:** DESIGN REVIEW DRAFT / P5 NOT RUN · **Date:** 2026-10-20

> This is a **companion test/design review** to approved [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a). It does **not** redefine stable-state semantics, API names, wire fields, DNS provider or health timeouts. [DUC-27](https://linear.app/ducanh/issue/DUC-27) governs review; [DUC-38](https://linear.app/ducanh/issue/DUC-38) governs Register DNS/domain ownership.

## 1. Success criteria and user experience

An Environment exposes a user-recognizable **stable external URL** for an authorized lifecycle across Sleep/Wake, subject to ownership/capability. The DNS destination, certificate and routing mechanics may change behind the scenes, but the user should not be misled into thinking an unavailable or unhealthy app is available.

State/experience review (the *display labels below are descriptive, not authoritative v1.2 enum names*):

| Observed phase | Public result | User action and permission rule | Technical safety condition |
|---|---|---|---|
| Awake + app healthy | App content under agreed URL | Normal app access as authorized | Only origin proven healthy/ready receives app traffic |
| Sleep completed | Sleeping page at agreed URL | Clearly inform user the app is asleep; offer an **authorized** Wake route when supported | Sleeping endpoint remains reachable, app/db safe state confirmed |
| Waking / pending | Sleeping/progress page or safe pending response | Show real operation progress; duplicate Wake requests handled idempotently | Do not expose unhealthy or partially restored app origin |
| Wake failed, BLOCKED or unknown | Safe error/status and operator guidance | Never promise the app is ready; operator/admin escalation as required | No unsafe retry or arbitrary state modification from anonymous page |
| Reclaim initiated / terminal | Explicit policy-based terminal notice or unavailable URL (defined by v1.2) | No implied Wake capability | Authorization/backup/Verify rules apply; no stale app link |

**Auth rule:** a public page may show a status but must not permit anonymous infrastructure mutation. Wake is a privileged operation; mechanism of login/session/token, anti-CSRF/rate limiting and scope is mapped from approved Interface Contracts, not invented here.

## 2. High-level routing & control/data plane separation

```text
User browser ---- stable hostname / TLS ----> Public entry route (implementation TBD by P5)
                                         |
                                      ┌──┴───────────────────────┐
                               sleeping/status path       healthy app origin
                                         ↑                       ↑
                                    status read             validated health
                                         |                       |
                                 InfraFlow control plane ---- Controller (authorized)
                                            |
                                    idempotent Wake request
                                            |
                                    preflight/lock/permits
                                            |
                                   Terraform/AWS executor
                                            |
                                     AWS actual inventory
```

**Important:** a DNS record change does not prove health. A successful Terraform action does not prove cutover success. A stable hostname may still have propagation/cache delays; the PoC must measure the user-visible behavior, not assume instant DNS coherence.

## 3. Implementation candidates — deliberately undecided

| Candidate for P5 | Benefits | Failure/cost trade-off to test | Decision status |
|---|---|---|---|
| DNS-switch strategy | Potentially retire costly app ingress while sleeping, stable hostname | DNS TTL/propagation/resolver caching, rollback, TLS/cert attachment, zone authority, transient mixed traffic | **NOT CHOSEN** |
| Persistent public edge/front-door | Endpoint stays live while app ingress is removed/paused | Edge service cost, routing and origins when app is asleep, auth for wake, cache invalidation, TLS compatibility | **NOT CHOSEN** |
| Persistent app ingress + sleeping handler | Simple URL and cutover semantics | ALB/ingress remains billable; savings must account for it; app health false positives | **NOT CHOSEN** |

Do not silently pick Route 53, CloudFront, API Gateway, ALB or a domain architecture from examples in the original report. These are candidate AWS services; the selected topology and DNS control model require P5 evidence and G3 review. No cutover implementation or IaC before G4.

### P5 safety supplement — upstream routing gate and change propagation

**Externally verified AWS behavior, not a change to the v1.2 semantics:** ALB target groups can **fail open** if all registered targets are unhealthy. In that state, ALB routes requests to those unhealthy targets rather than preventing all access ([AWS target group health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)). A target-group health check by itself therefore **cannot** guarantee that an app is never exposed while unhealthy.

**Candidate safety invariant to test:** the public entry path must have an *independent, authorized route gate* upstream of the application origin. A candidate decision could be a safe default route to a sleeping/status endpoint until the controller obtains readiness evidence and authorizes changing that route; the exact service, fail-safe mechanism, consistency model and permission boundaries remain **P5/G3 undecided**. Any path that bypasses the gate (direct ALB hostname or stale DNS/cache) must be identified and constrained by the approved topology. Do **not** assert an absolute zero-request guarantee without validating these bypasses and propagation windows.

**Cutover sequence for a test, not implementation authorization:** (1) verify environment ownership, DNS/TLS rights, permit and exclusive operation; (2) confirm DB dependencies, app health/functional probe and matching environment identity; (3) verify that public entry configuration will not expose unhealthy or wrong-origin endpoints; (4) initiate reversible cutover and observe from client resolvers over a bounded period; (5) continuously check origin/route and fall back to safe status when checks fail; (6) record actual error windows and cleanup. A cached DNS response, old client connection, TLS mismatch or late health failure must be captured, not silently counted as success.

**User-visible status privacy:** distinguish unauthenticated visitor content (minimal generic availability message) from authenticated owner/operator details (environment ID, tenant, state, operational logs, cost and controls). An unauthenticated Wake or guessed environment URL must never enable infrastructure mutation. The actual permission and status fields must be copied from approved Interface Contracts v1.2; this is a test boundary, not a new role/schema design.

## 4. Create versus Register URL ownership

| Check | Create origin | Register origin | Unsafe/unknown outcome |
|---|---|---|---|
| Hostname/zone ownership | Owner-provided or InfraFlow-managed approved domain route | Existing workspace may already own the hostname/zone | No DNS mutation; do not claim stable managed URL |
| TLS/cert scope | Cert/cname/origin rights must be verified | Confirm domain proof and existing ACM/cert ownership and renewal path | BLOCKED or restrict management per approved policy |
| App origin inventory | InfraFlow Blueprint output scoped to Env | Derived from compatible registered state + real AWS inventory | No guessed ALB or unverified health target |
| Traffic switching | Allowed only with matching authorization/preflight | Only when handoff includes DNS capability and rollback | No partial takeover |
| Wake entry | Authorized operation according to v1.2 | Authorized only after Register handoff/capability | Reject/deny ambiguous Wake without side effects |

Register MVP expects compatible AWS Terraform Web+DB but **must not assume the existing tenant's domain belongs to InfraFlow**. A custom/unowned domain cannot be treated as managed without explicit handoff; record compatibility/ownership blockers in DUC-38.

## 5. Proposed cutover invariants

1. Do not direct user traffic to the app origin until health validation and all required dependencies are ready.
2. The requested operation is permitted for the Environment and identity, and old/concurrent state writers cannot conflict.
3. Avoid exposing stale app ingress, stale DNS or an origin from another Environment (scope/ownership checks).
4. On failed Wake, keep the safe public route/status rather than announcing Awake. Retry/compensation follows baseline policy.
5. During Sleep transition, respect policy for active traffic, data integrity, draining and URL availability; determine P5 timing.
6. Any DNS mutation must be reversible or have a documented safe rollback/failure decision; insufficient capability → reject/BLOCKED.
7. URL verification tests must use real client lookup/TLS/app health observations and account for propagation and caching; tests may only run in G1-authorized sandbox.

## 6. P5 test design — all NOT RUN

| ID | Preconditions/test input | Expected observable result | Evidence required |
|---|---|---|---|
| URL-01 | Awake app healthy + permitted URL | Correct app traffic, TLS valid, no wrong Environment | Sanitized browser response/health, DNS/cert observations |
| URL-02 | Confirmed Sleep and supported public endpoint | Stable hostname shows sleeping page without exposed app origin | DNS result, HTTP/TLS, cost/runtime inventory |
| URL-03 | Wake requested by authorized actor | One authorized operation, status moves through Waking | Redacted operation status and audit record |
| URL-04 | Anonymous/unauthorized Wake | No cloud mutation; explicit denial | HTTP/status mock or real sanitized evidence |
| URL-05 | App launch but health fails | Routing remains safe; never serve unhealthy app as ready | Health checks and routing observations |
| URL-06 | DNS TTL/cache not settled | User sees documented transitional behavior, not a false success claim | Measured propagation across supported sample resolvers |
| URL-07 | DNS/cert rights missing in Register | Mutation refused/BLOCKED; existing domain not hijacked | Ownership/proof preflight and audit |
| URL-08 | Consecutive Sleep/Wake cycles | Hostname stable, healthy-only traffic, preserved DB fixture | URL/TLS and DB check per cycle |
| URL-09 | Failure midway through Sleep or Wake | Safe fallback route/status and auditable retry/manual recovery | Fault-injection/mock result + authorized AWS evidence after G1 |
| URL-10 | Race: manual Wake vs scheduler or Reclaim | Only authorized state transition; no conflicting traffic update | Operation/lock audit + final AWS observed state |
| URL-11 | Reclaim complete/incomplete | No stale traffic pointing to removed app; no false terminal success | Verify evidence and DNS/inventory checks |
| URL-12 | Cost of public endpoint during Sleep | Residual cost included in comparison, not assumed zero | P6 usage/pricing source, measured cost where feasible |
| URL-13 | All targets in an exposed ALB target group become unhealthy | Upstream app route remains safely gated or fails to status; capture ALB fail-open behavior, wrong-route exposure and mitigation | ALB target health records + external probes + public-entry configuration |
| URL-14 | Cached DNS record and persistent connection during Sleep/cutover | Record propagation/connection exposure duration and safe rollback, do not claim instantaneous switching | Resolver samples + HTTP/TLS result timestamps + retry/error window |
| URL-15 | Anonymous enumeration/status/CSRF/replay/rate abuse of Wake | No tenant/private status leakage or unauthorized/duplicate operation; approved rate policy enforced | Sanitized access/operation logs and authz results |
| URL-16 | RDS restarts independently during long Sleep | Public entry does not implicitly expose app; controller identifies actual-versus-desired drift and follows approved policy | DB events/state, health/route checks, retained cost |


**Evidence status:** NOT RUN for URL-01…URL-16; expected behaviors are **test criteria**, not measurements or claims of AWS capabilities.

**Execution details:** [P3/P5 evidence and acceptance test sheets](../planning/DUC-25-27-P3-P5-evidence-test-sheets.md) define fixtures, actions, pass/fail, failure conditions and cleanup without inventing API endpoints or AWS credentials.

## 7. Week-7 design-review handoff

- [x] Prepared proposed user-journey, authentication, origin separation, candidate strategies and negative P5 test catalogue.
- [ ] Review against **complete** Interface Contracts v1.2 for exact statuses, operations, permissions, errors and state transitions; resolve section identifiers with owner.
- [ ] Review with Minh on BLOCKED/cancel/retry/lock and with Hoàng on UI progress/URL status mapping.
- [ ] Obtain G1 approval (if tests require AWS); P5 experiment must specify test domain, sandbox, IAM, budget, snapshots, maximum latency and cleanup.
- [ ] Record P5 results and G3 option choice/ADR before G4 implementation plan.

**Definition of Done:** reviewed DUC-27 companion design & actual P5 evidence/decision or explicitly deferred unknowns per team's agreed scope; no `DONE` until reviewer acceptance. This draft introduces neither Terraform code nor live DNS changes.
