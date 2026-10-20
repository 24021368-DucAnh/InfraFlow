# DUC-40 — Baseline v1.2 → Contract → Acceptance Traceability Register v0.3

**Maintainer:** Ngô Bùi Đức Anh · **Date:** 2026-10-21 · **State:** baseline logic mapped; peer review and physical wire **PENDING**; not G4 approval

> **Authority discipline:** The project owner approved [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) on 19/10/2026. Both full document bodies were retrieved and read on 21/10/2026. Contracts §2.1 specifies **logical** fields and invariants; §10 explicitly defers HTTP/JSON wire mapping, service choices and measured thresholds. This register cites approved sections without inventing those physical details. It is still subject to independent reviewer confirmation.

## 1. Evidence tiers (avoid counterfeit contract conformity)

| Tier | Evidence | May claim | May not claim |
|---|---|---|---|
| **A — accepted baseline** | Full [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a), reviewed at specific section/table | Exact approved rule and any real wire fields contained in the source | New fields/endpoints/thresholds not present in the baseline |
| **B — accepted-gate summary** | DUC-34/35 (Done) | Confirms the owner accepted both v1.2 baselines | Replaces reading the baseline, or proves a physical wire/PoC result |
| **C — preparation/issues** | DUC-25/27/38/40/43/44/45 and GitHub PR #20 documents | Test hypotheses, owner assignments, proposed negative cases and evidence to collect | G1/G2/G3/G4 approvals, test PASS, implementation-ready contract |

## 2. Requirement → interface owner → expected negative behavior → acceptance / source map

| ID | Approved requirement/behavior | Producer → consumer (planning boundary) | Negative/fail-closed scenario to verify | Planned test links | Owner / verification evidence | Exact v1.2 logical source; physical mapping |
|---|---|---|---|---|---|---|
| CT-01 | **Create** supported Web + Database Environment, owner and Lease | Hoàng Web/API → Đức Anh Blueprint → Đạt executor | Invalid Blueprint/Lease/policy: reject before AWS action; Create may end `ACTIVE/PREPARED` | BP-01/02, P3-01 | Đức Anh+Hoàng: DUC-25/26 | Technical Design §§1, 3–4; Contracts §§2.1–2.2, 3, 7 (`Lease`, `Environment`, `Operation`); physical endpoint/types **PENDING G4** |
| CT-02 | **Register** compatible Terraform AWS Web+DB with complete handoff | Hoàng API → Đạt Register/state → Minh preflight | Incompatible config, old writer, no DNS authority or incomplete rights: read-only reject/no Activate | BP-03/04/15, P3-05, P1/P2 | Đạt+Minh: DUC-38/43 | Technical Design §§1, 3–4; Contracts §§2.1–2.2, 3, 5, 8 (`HandoffRecord`, `HANDOFF_INCOMPLETE`, `DNS_CONTROL_MISSING`); backend choice **PENDING G2/G3** |
| CT-03 | Environment ownership/resource boundary | Blueprint/inventory → validator → controller | Shared/retained/out-of-scope resource in plan or direct AWS action: `BLOCKED` | BP-07/15, P3-05, P4 | Đạt+Minh: DUC-44 | Technical Design §§2–3, 5; Contracts §§2.1, 5, 8 (`resourceOwnershipClass`, `ScopedPermit`, `SHARED_RESOURCE_IN_PLAN`); physical inventory **PENDING G4** |
| CT-04 | Desired, Terraform state, AWS actual and observed availability stay distinct | Executor/AWS observation → Minh controller → Hoàng UI | Stale/conflicting evidence or DB auto-start cannot yield false `SLEEPING`/success | BP-09/13, URL-16, P3-03 | Đạt+Minh: DUC-29 | Technical Design §§2, 5, 7; Contracts §§2–2.1, 4, 8 (`Observation`, three status axes, `STALE_OR_CONFLICTING_EVIDENCE`); freshness **PENDING G2/G3** |
| CT-05 | Lease expiry, extension and reclaim policy | Hoàng Lease/API → Minh controller | Expired Wake denied; Lease version change invalidates destructive permit | BP-11, URL-10, P4 | Hoàng+Minh: DUC-26/44 | Technical Design §§1, 5; Contracts §§2.1, 3–4, 8 (`Lease.version`, `LEASE_EXPIRED`, `LEASE_VERSION_CHANGED`); physical types **PENDING G4** |
| CT-06 | Sleep preserves required data and safe URL | Minh controller → Đạt executor + Đức Anh Blueprint | Unsupported DB topology or unverified cutover: no false Sleep; stop/backup policy observed | BP-05/13, P3-02/03/04 | Đức Anh+Minh+Hoàng: DUC-25/45 | Technical Design §§3–5, 8; Contracts §§2.2, 4–5, 8 (`LIFECYCLE_UNSUPPORTED`, `CUTOVER_UNVERIFIED`); AWS variant **PENDING G2/G3** |
| CT-07 | URL visitor may request bounded **Wake** without AWS account | Web/status API → Minh controller → executor → Đức Anh route | Invalid/expired/capability-less or abusive request denied; valid URL request idempotent; unhealthy app never announced Awake | URL-03/04/05/13/15, P5-02/03 | Hoàng+Minh+Đức Anh: DUC-27 | Technical Design §§1, 5–7; Contracts §§2–4, 6, 8 (`requestKey`, `operationId`, `LEASE_EXPIRED`, `HEALTH_GATE_FAILED`); auth mechanism/limits **PENDING G2/G3/G4** |
| CT-08 | Exclusive Terraform state writer and per-Environment operation lock | Đạt Register/backend → executor → operation guard | Old writer, lock loss or conflicting goal: no stale apply/no queue | BP-11, P3-06, P1/P2 | Đạt+Minh: DUC-43 | Technical Design §§2, 4–5; Contracts §§2–2.1, 4–5, 8 (`CONCURRENT_OPERATION`, `HandoffRecord`); backend/lock choice **PENDING G2/G3** |
| CT-09 | Validator issues scoped permit before cloud change | Đạt validator + Minh controller → executor | Changed plan/actual/ownership or missing backup: invalidate permit and `BLOCKED` | BP-07/08, P3-04/07, P4 | Đạt+Minh: DUC-44 | Technical Design §§3, 5–6; Contracts §§2.1, 5, 8 (`ScopedPermit`, `BACKUP_OR_PLAN_UNSAFE`); encoding **PENDING G4** |
| CT-10 | Reclaim requires backup, scoped action and postcondition **Verify** | Minh controller → executor/AWS inventory → API | Partial delete or absent proof: no `RECLAIMED`; retained backups follow Lease policy | BP-10/16, URL-11, P3-07 | Minh+Đạt: DUC-31/44 | Technical Design §§4–5, 7; Contracts §§2.1, 3, 5, 8 (`VERIFY_INCOMPLETE`, `RECLAIMED`); physical evidence store **PENDING G4** |
| CT-11 | Stable URL, sleeping page and health-gated route | Đức Anh DNS/entry ↔ Hoàng status ↔ Minh controller | ALB fail-open, stale DNS or missing DNS rights cannot count as safe cutover | BP-14, URL-01/02/06/07/13/14, P5-01/03/04/05 | Đức Anh+Hoàng: DUC-27/45 | Technical Design §§3–5, 7–8; Contracts §§2.2, 3, 6, 8 (`DNS_CONTROL_MISSING`, `CUTOVER_UNVERIFIED`); topology **PENDING G2/G3** |
| CT-12 | Cost comparison includes retained Sleep costs and source | Đức Anh inventory → Hoàng cost/UI | Unknown price or missing measurement cannot be called verified savings | BP-12, URL-12, P3-08/P5-08 | Hoàng+Đức Anh: DUC-32/45 | Technical Design §§3, 7–8; Contracts §§3, 9 status/provenance; price and billing window **PENDING P6/G3** |
| CT-13 | **Unregister** hands Register workspace back without destroy | Hoàng API → Đạt state/DNS handback → Minh controller | Active workflow or incomplete reverse handoff: `BLOCKED`; keep control until safe Verify, no destroy | CT-13-U handback case in G1 P2A/P2B; P4 negative | Đạt+Minh+Hoàng: DUC-38 | Technical Design §§4–5; Contracts §§2.1–2.2, 3, 7, 9 (`HandoffRecord`, `UNREGISTERED`); physical handback **PENDING G2/G3/G4** |
| CT-14 | Durable operation identity, bounded retry and honest outcome | Minh controller → operation record → Hoàng API | Same key/different payload denied; uncertain infrastructure outcome `BLOCKED`, no blind Reclaim retry or false success | CT-14-R recovery case in G1 P4; URL-09/10 | Minh+Đạt: DUC-29/44 | Technical Design §§3, 5–6; Contracts §§2, 2.1, 4–5, 7–8 (`REQUEST_KEY_REUSED`, `FAILED_RECOVERABLE`, `BLOCKED`); persistence transport **PENDING G4** |

**Known execution gap:** CT-13 and CT-14 have approved logical source sections, but their proposed handback/recovery cases have **NOT RUN** and lack independent producer/consumer review. Neither a physical API nor a passing result is implied.

### Original DUC-40 MAP-01…MAP-12 reconciliation

The [original DUC-40 traceability draft](https://linear.app/ducanh/document/infraflow-requirementcomponenttest-traceability-v01-draft-2613bddb7173) defines twelve working MAP IDs. They are planning IDs, not v1.2 requirement IDs. The crosswalk below preserves all twelve and ties each to the approved section citations and planned cases in the CT table above. It does not turn the unrun cases into PASS results.

| MAP ID | CT coverage | Planned acceptance coverage | Remaining evidence |
|---|---|---|---|
| MAP-01 | CT-01, CT-03, CT-04 | BP-01/02/07/09, P3-01/03 | P3 Create and inventory after G1/G4 |
| MAP-02 | CT-02, CT-03, CT-08 | BP-03/04/15, P3-05/06, P1/P2 | Register handoff, DNS rights and lock proof |
| MAP-03 | CT-05, CT-06, CT-07 | BP-05/13, URL-03/05, P3-02/03, P5-02 | Both-origin Sleep/Wake after gates |
| MAP-04 | CT-04, CT-08, CT-14 | BP-09/11/13, URL-09/16, P3-03/06 | Reconcile observed, state and AWS actual |
| MAP-05 | CT-03, CT-09, CT-10 | BP-07/08/10/16, P3-04/07, P4 | Permit, ownership and backup proof |
| MAP-06 | CT-09, CT-10, CT-14 | BP-10/16, URL-11, P3-07, P4 | Reclaim and positive Verify proof |
| MAP-07 | CT-07, CT-11 | BP-14, URL-01/02/03/06/07/13/14/15, P5-01/02/03/04/05 | DNS, guest Wake and healthy cutover |
| MAP-08 | CT-04, CT-06, CT-11 | BP-05/13/14, URL-16, P3-02/03, P5-05 | DB persistence, RDS restart and residual resources |
| MAP-09 | CT-05, CT-07, CT-08, CT-14 | BP-11, URL-09/10, P3-06, P5-07, P4 | Roles, idempotency and conflict responses |
| MAP-10 | CT-02, CT-03, CT-13 | BP-03/04/15, P3-05, CT-13-U | Reverse handoff without destroy |
| MAP-11 | CT-12 | BP-12, URL-12, P3-08, P5-08, P6 | Cost source, assumptions and measurement window |
| MAP-12 | CT-03, CT-09, CT-10, CT-12 | BP-07/08/10/12/16, P3-04/07/08, P4/P6 | Secret/redaction and cleanup evidence across all probes |

**Crosscutting MAP-12 rule:** Contracts v1.2 §3 forbids exposing raw Terraform state/plan, secrets or private resource data to unauthorized status viewers. G1 evidence must redact credentials and sensitive state; inventory and cleanup must be checked across P1–P6 rather than inferred from one CT row. Static document scanning below is preparation evidence, not proof that a future runtime enforces this rule.

**Crosswalk status:** twelve source MAP rows accounted for at section level through CT-01…CT-14. Producer/consumer confirmation, physical wire and test evidence remain pending. The original draft's full closure checklist therefore remains open.

## 3. Source and physical-wire review worksheet

Every CT-01…CT-14 needs one verified mapping row. Reviewer copies literal source section and the smallest schema fragment necessary (do **not** paste secret values):

| Column | Reviewer should record | Current state |
|---|---|---|
| Authority/version | Exact `Technical Design v1.2 §X` or `Interface Contracts v1.2 §Y` | Mapped in CT-01..14; peer confirmation pending |
| Producer/consumer | Source component → destination component and responsibility | Planned only |
| Wire contract | Keep approved logical names in Contracts §2.1; prepare physical endpoint/event/payload mapping after G2/G3 within the implementation plan submitted for G4 approval | `PHYSICAL WIRE PENDING G4 PLAN`; v1.2 does not prescribe HTTP/JSON names |
| Preconditions | Origin, owner, lease, permit, state/lock, capability and role | Mapped by section above; per-boundary reviewer confirmation pending |
| Success/error semantics | Approved state transitions, denial/conflict/BLOCKED, idempotency | Mapped to Contracts §§2–8; physical mapping pending |
| Test & negative evidence | CT ID → BP/URL/P# case, expected vs actual and cleanup | Proposed only / NOT RUN |
| Review | Reviewer identity, date, authoritative excerpt link and approval | `PENDING` |

**Rule:** If v1.2 fixes semantics but defers physical wire mapping to implementation, annotate `BASELINE SEMANTICS CONFIRMED / PHYSICAL WIRE PENDING G4 PLAN`; do **not** pretend v1.2 contains an API field it deliberately deferred. The mapping belongs in the plan reviewed for G4 approval, after G2/G3 decisions and before product code or IaC. This prevents pointless re-review of G0.

## 4. Review routing, risk acceptance and DoD

- **Đức Anh:** CT-01/11 + traceability completeness; provide P3/P5 evidence slots.
- **Đạt:** CT-02/03/08/09/13 + backend/state boundaries; verify against full v1.2.
- **Minh:** CT-04/05/06/07/09/10/13/14 + safety/Controller; verify desired/observed and Reclaim/Verify.
- **Hoàng:** CT-01/05/07/11/12/13 + API/Lease/UI/cost; verify guest/private status.
- All four owners review overlapping contracts. An AI review on the repo owner's GitHub account **does not** count as independent peer approval.

### Definition of Done — DUC-40

- [x] 14 semantic categories, cross-team boundaries and associated BP/URL/P tests captured with provenance tiers.
- [x] Unregister and durability mapped to full approved logical source; planned CT-13-U/CT-14-R cases added, NOT RUN.
- [x] All 14 categories reconciled against the full v1.2 text at section level; URL-user Wake contradiction corrected.
- [x] Original DUC-40 MAP-01..MAP-12 working rows reconciled to CT and planned acceptance cases; no test execution implied.
- [x] Physical wire identified as G4 mapping; no HTTP/JSON endpoint or payload invented.
- [ ] Relevant team reviewers confirm ownership/error/negative paths and evidence in Linear.
- [ ] Draft acceptance matrix approved for G4 planning; no AWS runs or product code attributed to this task.

**Result:** section-level baseline logic mapped by author, **not independently verified**. [PR #20](https://github.com/24021368-DucAnh/InfraFlow/pull/20) stays OPEN until independent review; physical wire and test execution remain pending their gates.
