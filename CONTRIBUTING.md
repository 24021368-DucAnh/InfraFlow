# Contributing to InfraFlow

InfraFlow is a **public** repository for a Cloud Computing course project. Work is tracked in [Linear](https://linear.app/ducanh/project/infraflow-31b8c3b2d1ad); the public Git history documents reviewed deliverables, not approval to operate AWS.

## Source of truth and approval gates

- G0: Technical Design v1.2 and Interface Contracts v1.2 were accepted on 19 October 2026. Treat contract semantics as fixed unless changed through an explicit review/ADR.
- G1: no AWS technical PoC until the account owner approves the sandbox, IAM, region, budget, resource scope, safeguards and cleanup.
- G2: capture expected versus actual PoC results, failure paths and sanitized evidence.
- G3: document and review PoC-driven architecture/implementation decisions.
- G4: **no product code, Terraform IaC, deployment or destructive automation** until the implementation plan is approved.
- Work permitted before G4 includes documentation, requirements-to-tests mapping, written PoC plans and collaboration setup.

## Development workflow

1. Select one [Linear issue](https://linear.app/ducanh/project/infraflow-31b8c3b2d1ad) with owner, dependencies and acceptance criteria. Do not start a blocked issue.
2. Branch from the latest `main`; name the branch using the issue ID (example: `docs/DUC-39-onboarding`; after G4: `feat/DUC-XX-short-name`).
3. Make focused changes supported by the approved baseline. If the change alters lifecycle semantics, data ownership, safety checks or interfaces, stop and request a design decision rather than silently changing behavior.
4. Verify the change and record the **commands run and actual results**. For documentation, check links, language, formatting and public-safe content; do not claim automated tests were run when they were not.
5. Open a pull request to `main`, reference the Linear issue and complete the [PR template](.github/PULL_REQUEST_TEMPLATE.md).
6. Request independent peer review where feasible. Do not merge a PR requiring owner/architectural approval without that approval. Actual GitHub branch protection must be verified; documentation alone does not enable it.
7. After merge, link the PR/commit and sanitized evidence to the Linear issue, then update the issue state against its acceptance criteria.

## Expected PR quality

- One logical scope per PR, with requirements/contract references.
- Reproducible checks, expected and actual behavior, limitations and rollback/cleanup requirements when relevant.
- Fail-closed handling of unsafe/ambiguous cloud state, conflicting writers and missing permissions.
- No raw secrets, Terraform state/plan, private environment inventories, personal data or production credentials in code, PRs, screenshots or logs.
- For **future approved** IaC changes: reviewed provider lockfile (`.terraform.lock.hcl`) should be versioned, whereas `.terraform/`, `*.tfstate`, local `*.tfvars` and saved plans must remain out of Git.
- No pull-request workflow should automatically execute `terraform apply` or `terraform destroy` against a live cloud account.

## Planned ownership (not a final personnel assignment)

The project has separate planning tasks for state/backend, safety/controller, blueprint/DNS and product/API/cost. Component ownership and reviewers must be confirmed on the relevant Linear issue before implementation. Do not infer GitHub identities from contributor names.

## Reporting incidents

See [SECURITY.md](SECURITY.md). If you discover exposed credentials or a potentially destructive workflow, stop and notify the maintainer privately; do not disclose secrets in a public issue.
