# DUC-41 — CI/PR workflow and G4 readiness

**Status:** TEAM ALIGNMENT REPORTED · Planning artifact merged 2 November 2026

**Tracking:** [DUC-41](https://linear.app/ducanh/issue/DUC-41), [DUC-36](https://linear.app/ducanh/issue/DUC-36)
**Scope:** Planning only. This document proposes a reviewable collaboration and verification workflow; it does not configure CI, change branch protection, authorize AWS access, or approve implementation.

## 1. Current gate state

- **G0:** Technical Design and Interface Contracts v1.2 are the accepted logical baseline.
- **G1:** No AWS PoC permission is recorded. Do not use AWS credentials or run cloud probes.
- **G2/G3:** P1–P6 evidence and evidence-based implementation decisions remain pending. P3/P5 are NOT RUN.
- **G4:** No approved implementation plan is recorded. Product code, Terraform/IaC, deployment, and destructive automation remain out of scope.

The project README, `SECURITY.md`, and `CONTRIBUTING.md` remain authoritative for these gates. A checklist, draft, green documentation check, or merged planning PR does not satisfy a gate.

## 2. Proposed issue-to-PR workflow

1. Select one unblocked Linear issue. Confirm its owner, dependencies, acceptance criteria, baseline section, and permitted scope before editing.
2. Create an issue-linked branch from the latest `main` branch. Use `docs/DUC-XX-short-name` for planning work and the project-approved feature naming convention only after G4.
3. Keep one logical change per PR. Link the Linear issue and include scope, out-of-scope items, contract references, checks actually run, results, limitations, and rollback/cleanup notes where relevant.
4. Run only checks appropriate to the change. Record commands and real results; mark cloud or integration scenarios NOT RUN/BLOCKED when their gates or fixtures are absent.
5. Obtain review from someone other than the author. Route contract, state/lock, safety, and URL/API questions to the relevant domain reviewers identified in the issue. AI comments and author replies do not count as independent approval.
6. Merge only after required review and owner decisions are recorded. No PR should auto-merge or run `terraform apply`/`terraform destroy` against a live account.
7. After an owner-authorized merge, record the PR/commit and sanitized evidence in Linear and update status against acceptance criteria. Do not mark an issue Done merely because its PR merged.

## 3. Non-destructive CI proposal

The CI provider and exact workflow configuration are intentionally **not selected** in this planning document. After G4 approval, the implementation plan may select appropriate checks such as:

- documentation structure/link checks and Markdown lint for documentation changes;
- unit and contract tests using local fixtures or mocks for approved implementation changes;
- static analysis and secret scanning on proposed changes;
- repository hygiene checks that do not access cloud accounts or private state.

Any future PR checks must be non-destructive. They must not receive AWS credentials, read Terraform state or saved plans, or run AWS operations. They must never execute `terraform apply` or `terraform destroy`. AWS end-to-end tests require both an approved G1 scope and G4-authorized implementation, plus isolated resources, a budget/stop condition, and documented cleanup. If authorized, they belong in a separately controlled test lane, never as an automatic PR check. If these conditions are not met, keep the test NOT RUN or use an approved local mock.

This is a proposal for team review, not a claim that CI or branch protection is currently configured or enforced.

## 4. Planned review boundaries

Use the ownership areas below as routing suggestions only; confirm the actual owner/reviewer on each Linear issue. Do not infer GitHub usernames from names.

| Area | Review focus |
|---|---|
| Đạt — platform/state | Backend, state ownership, lock/writer exclusivity, validator boundary |
| Đức Anh — Blueprint/DNS | Create inputs, component dependencies, URL ownership and DNS handoff |
| Minh — controller/safety | Permit, BLOCKED behavior, retries, cutover failure, Reclaim/Verify |
| Hoàng — API/UI | Public status, Wake capability, user-visible progress, cost presentation |

Cross-boundary changes need reviewers from each affected area. Only the project/architecture owner can accept an architecture decision or approve G4; only the AWS account owner can grant G1.

## 5. G4 implementation-plan readiness checklist

The G4 plan must be based on reviewed G2 evidence and G3 decisions. For each authorized task it should identify:

- the Linear issue, owner, dependencies, acceptance criteria, and exact approved contract sections;
- the files/components and producer/consumer interfaces to change, without inventing unreviewed wire fields;
- a small test-first sequence: a named test that fails for the missing behavior, the minimal implementation, then the passing test and relevant regression suite;
- normal, denial, failure, retry, concurrency, and recovery cases that apply to the task;
- reviewer, effort estimate, risk, rollback, cleanup, and evidence required;
- explicit G1 conditions for any AWS test and the gate that blocks implementation until G4 approval.

Exact file paths, physical API payloads, CI service, AWS services, thresholds, and estimates remain open until their dependencies are reviewed. The plan must preserve Create and Register as separate origins and retain fail-closed behavior when ownership, state/lock, permission, backup, DNS control, or observed state is uncertain.

## 6. Evidence to attach to DUC-41 / DUC-36

For team review, record:

- reviewer names and the specific sections they accepted or requested changes to;
- any owner decision on merge policy, reviewer requirements, and branch rules;
- the actual capability and evidence for branch protection, if enabled; otherwise record that it is a checklist rather than enforced policy;
- links to this reviewed workflow and the G4 plan, once that plan is authorized.

## 7. Open decisions and non-goals

- Confirm exact GitHub handles and collaborator permissions through DUC-42; do not guess identities.
- Verify actual repository rulesets/branch protection before claiming they are active.
- Select CI provider and workflow permissions only in the approved G4 plan.
- This document does not implement CI, modify repository settings, invite collaborators, run AWS tests, or authorize product code/IaC.

## Review state

**Owner review:** Đức Anh approved this planning draft in the Codex conversation on 1 November 2026.

**Review disposition (2 November 2026):** Owner Đức Anh reported that the team has aligned on this planning artifact. The source conversation did not identify individual reviewers or section-by-section decisions, so none are attributed here. PR #24 merged this document to `main`; DUC-41 is Done for the planning artifact only. This does not represent G1 AWS authorization, G2 evidence, G3 decisions, or G4 implementation approval.

### Independent draft review

- Important: separate authorized AWS end-to-end testing from automatic PR checks — clarified above.
- Important: require completed group review, recorded reviewer decisions, and the DUC-36 link before Done — clarified above.
- Final review follow-up: use “latest `main`” and “After G4 approval” to match `CONTRIBUTING.md` and clarify the gate wording; both edits are now applied above.

