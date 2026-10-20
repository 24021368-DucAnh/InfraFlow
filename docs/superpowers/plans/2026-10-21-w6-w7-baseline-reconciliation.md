# W6–W7 Baseline Reconciliation and Review Evidence Plan

> **For agentic workers:** use the Superpowers verification, receiving-review, execution and final-review gates. This plan records the documentation task already authorized by the owner; it does not authorize AWS or product implementation.

**Goal:** reconcile PR #20 with the full approved v1.2 baselines and the original versus rebased W6/W7 plans, correct contradictions, and leave reproducible review evidence.

**Architecture:** retain the six PR documents as design and test planning artifacts. Add exact section-level semantic references from the Linear baseline, while labeling AWS choices and measured thresholds as pending G2/G3 and physical wire formats as input to the G4 approval plan. Record tests and findings in this plan.

**Tech stack:** Markdown, local Python/PowerShell checks, Git diff, GitHub and Linear review state.

**Spec:** Technical Design v1.2 and Interface Contracts v1.2 (Linear, approved 19/10/2026); original `progress_1.pdf` Action Plan table 3.1; rebased W6–W10 tracker supplied by the owner.

## Global constraints

- Baseline semantics remain unchanged; no invented HTTP endpoint, Terraform field, IAM policy or numeric AWS threshold.
- No AWS PoC before explicit G1 account-owner approval; no product code, Terraform or IaC before G4.
- Do not mark any BP/URL/P probe PASS without actual execution evidence.
- PR #20 stays open until independent domain reviewers and owner decide; do not self-approve or merge.

## Review focus

1. URL visitor Wake permission must match Technical Design §1 and Interface Contracts §§3, 6, 8.
2. Register without DNS control must remain non-activated under Technical Design §4 and Interface Contracts §§3, 8.
3. RDS seven-day restart and all-unhealthy ALB fail-open must be explicit test risks, not claimed as solved.
4. Unregister handback and uncertain operation recovery must have test ownership and no false terminal success.
5. Original Action Plan W6/W7 implementation work must not be reported as completed by rebased planning artifacts.

### Task 1: Source and review reconciliation

**Files:** six PR documents and this plan.

- [x] Read original Action Plan table 3.1 and supplied rebased tracker.
- [x] Read full Technical Design and Interface Contracts v1.2 through Linear.
- [x] Read PR #20 diff, issue #2 and all review threads before editing.
- [x] Correct source provenance and original-versus-rebased completion language.

### Task 2: Contract and safety correction

**Files:** DUC-25, DUC-27, DUC-40, P3/P5 and G1 documents.

- [x] Map CT-01..14 and the original MAP-01..12 to exact v1.2 sections and logical fields/errors; label physical wire pending for the G4 plan.
- [x] Correct URL-user Wake, Register DNS, Unregister, retry, operation conflicts and fail-closed test expectations.
- [x] Correct AWS service facts against current primary documentation.

### Task 3: Verification and delivery

- [x] Run Markdown lint, links/cross-reference checks and one-to-one BP/URL coverage checks.
- [x] Run secret scan and inspect entire PR diff for out-of-scope files.
- [x] Run Codex Security diff review and resolve actionable findings.
- [ ] Commit and push verified documentation, update PR/review threads and Linear/GitHub issue state with actual evidence.
- [x] Perform independent final diff review and retain gate blockers.

## Execution record

The following outcomes were observed on 21/10/2026 in the local PR branch checkout. These are document checks and a security review of a documentation diff; none executes the planned AWS PoCs or proves runtime security.

| Check | Command or source | Observed result |
|---|---|---|
| Markdown lint | `uvx --from pymarkdownlnt pymarkdown -d MD013 scan` on the seven package Markdown files | Exit 0. MD013 (line length) is disabled for existing long tables and links; all other enabled rules passed. |
| Document structure, links and coverage | `python scripts/check_review_docs.py` | Exit 0: seven Markdown files, 16 local relative links resolved, 47 external references counted, 16 BP IDs, 16 URL IDs, 14 CT IDs, 12 original MAP IDs, 16 P3/P5 recipes and 32 unique primary BP/URL mappings. External references are counted, not all live-checked. |
| Patch hygiene | `git diff --check` | Exit 0; no whitespace errors. |
| Secret scan | `uvx --from detect-secrets detect-secrets scan --all-files --no-verify docs/design docs/planning docs/superpowers/plans scripts/check_review_docs.py` | Exit 0; 27 detectors, zero findings in the scanned paths. |
| Codex Security diff review | `security-diff-scan` on PR's original six-document base-to-head diff | Six documentation surfaces manually inspected, zero reportable code vulnerabilities. Scope does not establish AWS or application security. |
| Independent final AI review | Superpowers review against full v1.2 and current local diff | Two P2 documentation defects found: conflicting goals had been allowed to serialize, and physical mapping was placed after G4 approval. Both corrected before delivery. This is not independent human approval. |

Source checks: full [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66), [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a), original [DUC-40 MAP draft](https://linear.app/ducanh/document/infraflow-requirementcomponenttest-traceability-v01-draft-2613bddb7173), original Action Plan `progress_1.pdf` §3.1 and owner-supplied W6–W10 tracker. The original Action Plan required Blueprint/Terraform and stable URL work in W6/W7; the rebased tracker records W6 G0 and W7 planning gates. This package satisfies documentation preparation, not the original implementation outcomes.

**Remaining gates:** G1 owner approval and AWS evidence; G2/G3 choices and ADRs; physical mapping in a reviewed G4 plan; G4 authorization before product code/IaC; independent domain reviewers and owner decision before PR merge or issue closure.
