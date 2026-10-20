# DUC-40 — Baseline v1.2 → Contract → Acceptance Traceability Register v0.2

**Maintainer:** Ngô Bùi Đức Anh · **Date:** 2026-10-21 · **State:** reviewable traceability *register*, **NOT fully verified** and **not G4 approval**

> **Authority discipline:** The project owner explicitly approved Technical Design and Interface Contracts v1.2 on 19 Oct 2026 ([DUC-34](https://linear.app/ducanh/issue/DUC-34), [DUC-35](https://linear.app/ducanh/issue/DUC-35)). The issue descriptions verify *semantic categories*, not complete original wire signatures. Linear `get_document` returned empty and `list_documents` provided abbreviated previews for the two source documents in this session. Do not substitute this register for the full original text.

## 1. Evidence tiers (avoid counterfeit contract conformity)

| Tier | Evidence | May claim | May not claim |
|---|---|---|---|
| **A — accepted baseline** | Full [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a), reviewed at specific section/table | Exact approved rule and any real wire fields contained in the source | New fields/endpoints/thresholds not present in the baseline |
| **B — accepted-gate summary** | DUC-34/35 (Done) | Create/Register + shared lifecycle, Environment boundary, Desired/Observed, idempotency, conflict, scoped permit, handoff, BLOCKED and Unregister are already approved *semantic categories* | Exact enum, state diagram text, field name, error code, service choice |
| **C — preparation/issues** | DUC-25/27/38/40/43/44/45 and GitHub PR #20 documents | Test hypotheses, owner assignments, proposed negative cases and evidence to collect | G1/G2/G3/G4 approvals, test PASS, implementation-ready contract |

## 2. Requirement → interface owner → expected negative behavior → acceptance / source map

| ID | Requirement/behavior already named in baseline-gate issues | Producer → consumer (planning boundary) | Negative/fail-closed scenario to verify | Test links | Owner / verification evidence | v1.2 exact source & physical mapping |
|---|---|---|---|---|---|---|
| CT-01 | **Create** supported Web + Database Environment, owner and lease | Hoàng Web/API → Đức Anh Blueprint → Đạt state/executor | Unsupported component/parameter or missing owner: no unapproved resource creation | BP-01/02, P3-01 | Đức Anh+Hoàng: DUC-25, DUC-26 | **OPEN — copy exact v1.2 section, field/type/error from original** |
| CT-02 | **Register** compatible Terraform AWS Web+DB workspace with explicit handoff | Hoàng API → Đạt Register/state adapter → Minh preflight | Incompatible config, old writer active, backend unreadable, out-of-scope dependency: reject/BLOCKED | BP-03/04/15, P3-05, P1/P2 | Đạt+Minh: DUC-38, DUC-43 | **OPEN — origin capability, handoff contract, deny state** |
| CT-03 | Environment ownership/resource boundary | Blueprint/Inventory → validator → controller | Shared/out-of-scope resource affected: deny and preserve foreign resources | BP-07/15, P3-05, P4 | Đạt+Minh: DUC-44 | **OPEN — ownership evidence/permit identity** |
| CT-04 | Desired vs Observed state distinct from Terraform state/configuration | Executor/AWS inventory → Minh controller → Hoàng UI | Drift, stale inventory and DB auto-start: no false terminal status | BP-09/13, URL-16, P3-03 | Đạt+Minh: DUC-34, DUC-29 | **OPEN — state/status semantics and reconciliation rule** |
| CT-05 | Lease expiration, extension and lifecycle policy | Hoàng Lease/API → Minh controller | Extend vs Reclaim race, expired lease or unknown policy: no conflicting destructive operation | P4, URL-10, BP-11 | Hoàng+Minh: DUC-26, DUC-44 | **OPEN — lease/authorization/error contract** |
| CT-06 | Sleep data-preserving transition | Minh controller → Đạt executor + Đức Anh Blueprint | Unknown database stop support or unavailable backup: BLOCKED; never imply zero cost | BP-05/13, P3-02/03/04 | Đức Anh+Minh+Hoàng: DUC-25/45 | **OPEN — preflight/sleep capability and DB retention** |
| CT-07 | Wake authorized/idempotent | Web/API → Minh controller → executor → Đức Anh route | Anonymous/duplicate/replayed Wake: no unauthorized AWS operation; unhealthy origin not exposed | URL-03/04/05/13/15, P5-02/03 | Hoàng+Minh+Đức Anh: DUC-27 | **OPEN — role/status/idempotency/denial mapping** |
| CT-08 | Exclusive Terraform state writer and lock | Đạt Register/backend → executor → operation guard | Old writer/concurrent operation/state mismatch: reject/serialize, do not apply stale plan | BP-11, P3-06, P1/P2 | Đạt+Minh: DUC-43 | **OPEN — backend strategy and lock semantics** |
| CT-09 | Validator + scoped permit prior to changing cloud | Đạt validator + Minh policy/controller → executor | Changed plan, missing backup, wrong scope or unknown state: fail closed | BP-07/08, P3-04/07, P4 | Đạt+Minh: DUC-44 | **OPEN — permit scope/binding/error fields** |
| CT-10 | Reclaim with backup and postcondition **Verify** | Minh controller → executor/AWS inventory → API | Partial delete / missing proof: do not mark Reclaimed; preserve evidence and escalate | BP-10/16, URL-11, P3-07 | Minh+Đạt: DUC-31/44 | **OPEN — terminal-state and verification rule** |
| CT-11 | Stable URL/sleeping page/health-gated route | Đức Anh DNS/entry ↔ Hoàng status UI ↔ Minh controller | All ALB targets unhealthy/fail-open, stale DNS or missing TLS/domain authority: route safely or BLOCKED | BP-14, URL-01/02/06/07/13/14, P5-01/03/04/05 | Đức Anh+Hoàng: DUC-27, DUC-45 | **OPEN — route authority/status/cutover mapping** |
| CT-12 | Cost/usage/retained expenses while asleep | Đức Anh component inventory → Hoàng cost service/UI | Missing price/cost measurement must display estimate/unknown, not verified savings | BP-12, URL-12, P3-08/P5-08 | Hoàng+Đức Anh: DUC-32/45 | **OPEN — billing class/cost provenance** |
| CT-13 | **Unregister** as separate safe handback path (named explicitly in DUC-34/35) | Hoàng API → Đạt backend/ownership → Minh controller | Must not treat Unregister as Reclaim/delete; release controls only according to baseline and confirmed handback | **NEW REVIEW GAP — request contract test IDs and semantics from full v1.2** | Đạt+Minh+Hoàng: DUC-34/35/38 | **OPEN — exact Unregister postcondition and tests** |
| CT-14 | Durable operations, retry/resume, error reporting and audit | Minh controller → persisted operation → Hoàng API | Restart, duplicate dispatch, partial failure: no double execute, no false success | URL-09/10, P4; add missing cases on reviewer approval | Minh+Đạt: DUC-29, DUC-44 | **OPEN — retry/idempotency and conflict/error mapping** |

**Known gap:** CT-13 Unregister and precise CT-14 recovery need explicit approved source and test acceptance in the v1.2 check. They are not silently assigned an invented behavior or new API.

## 3. Exact-section/wire review worksheet — MUST be filled from full approved v1.2

Every CT-01…CT-14 needs one verified mapping row. Reviewer copies literal source section and the smallest schema fragment necessary (do **not** paste secret values):

| Column | Reviewer should record | Current state |
|---|---|---|
| Authority/version | Exact `Technical Design v1.2 §X` or `Interface Contracts v1.2 table Y` | `UNVERIFIED` |
| Producer/consumer | Source component → destination component and responsibility | Planned only |
| Wire contract | Literal approved endpoint/event/table, request/response fields and types **only if present** | `UNVERIFIED` |
| Preconditions | Origin, owner, lease, permit, state/lock, capability and role | Category known, exact rule unknown |
| Success/error semantics | Approved state transitions, denial/conflict/BLOCKED, idempotency | Category known, exact mapping unknown |
| Test & negative evidence | CT ID → BP/URL/P# case, expected vs actual and cleanup | Proposed only / NOT RUN |
| Review | Reviewer identity, date, authoritative excerpt link and approval | `PENDING` |

**Rule:** If v1.2 fixes semantics but defers physical wire mapping to implementation, annotate `BASELINE SEMANTICS CONFIRMED / PHYSICAL WIRE PENDING G3–G4`; do **not** pretend v1.2 contains an API field it deliberately deferred. This prevents pointless re-review of G0.

## 4. Review routing, risk acceptance and DoD

- **Đức Anh:** CT-01/11 + traceability completeness; provide P3/P5 evidence slots.
- **Đạt:** CT-02/03/08/09/13 + backend/state boundaries; verify against full v1.2.
- **Minh:** CT-04/05/06/07/09/10/13/14 + safety/Controller; verify desired/observed and Reclaim/Verify.
- **Hoàng:** CT-01/05/07/11/12/13 + API/Lease/UI/cost; verify guest/private status.
- All four owners review overlapping contracts. An AI review on the repo owner's GitHub account **does not** count as independent peer approval.

### Definition of Done — DUC-40

- [x] 14 semantic categories, cross-team boundaries and associated BP/URL/P tests captured with provenance tiers.
- [x] Major missing Unregister and durability coverage made visible rather than inferred.
- [ ] All required categories reconciled against the **actual full** v1.2 text, with section references and no contradictions.
- [ ] Physical wire items identified as baseline-fixed versus G3/G4 implementation decisions; no fabricated schema.
- [ ] Relevant team reviewers confirm ownership/error/negative paths and evidence in Linear.
- [ ] Draft acceptance matrix approved for G4 planning; no AWS runs or product code attributed to this task.

**Result:** review-ready register, **not fully verified**. [PR #20](https://github.com/24021368-DucAnh/InfraFlow/pull/20) should stay OPEN until baseline and independent review checks pass.
