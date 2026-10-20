## Linear issue and scope

Linear: DUC-…

- **Goal / change summary:**
- **Scope and acceptance criteria:**
- **Out of scope:**
- **Baseline reference:** Technical Design / Interface Contracts v1.2 section (if applicable)

## Verification

- [ ] I recorded actual checks and outcomes below (or clearly stated *not run*).
- [ ] Required acceptance scenarios and failure paths are addressed or explicitly deferred.
- [ ] Reviewer can reproduce the checks using non-secret instructions.

**Commands / checks run and actual results (do not invent):**

**Sanitized test evidence / known limitations:**

## Public repository and operational safety

- [ ] No secrets, keys, credentials, private cloud inventories, personal data, raw Terraform state or saved plans are included (including screenshots and log excerpts).
- [ ] No unreviewed changes to lifecycle ownership, state writer-lock, authorization, data preservation, fail-closed or verification semantics.
- [ ] If this PR contains product code/IaC, the approved **G4** implementation plan/task is linked. Otherwise it is a docs/planning-only PR.
- [ ] If real AWS actions occurred, **G1** authorization, resource scope, IAM/budget, teardown and PoC evidence are linked.
- [ ] This PR does **not** trigger unattended `terraform apply` or `terraform destroy`.

## Review and follow-up

- **Reviewer(s):**
- **Risks, rollback/cleanup (if relevant):**
- **Related Linear issues / approvals:**
