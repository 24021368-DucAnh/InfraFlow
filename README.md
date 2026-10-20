# InfraFlow

**Cloud environment lifecycle management for Terraform-managed AWS Web + Database workloads.**

> **Project status (20 October 2026):** Technical Design and Interface Contracts v1.2 are the agreed G0 baseline. This public repository is currently in collaboration/onboarding setup. **No production-ready platform, implemented MVP, or deployed AWS infrastructure is claimed here.**

## Why InfraFlow?

Terraform can provision infrastructure, but a team also needs to know who owns an environment, how long it should live, when it can be paused or reclaimed, which resources or data must be preserved, and how to recover safely from partial failures. InfraFlow is intended to manage these operational workflows around Terraform, rather than merely providing a UI for Terraform commands.

## MVP boundaries (design baseline)

- **Create:** provision a supported AWS Web + Database environment using an InfraFlow blueprint and Terraform.
- **Register:** adopt an existing **compatible** Terraform-managed AWS Web + Database environment after ownership, state/workspace compatibility and safe handoff checks.
- **Shared lifecycle:** apply approved Sleep, Wake, Reclaim and Verify workflows to both origins.
- **Guardrails:** track desired versus observed state, require authorized operations, prevent conflicting writers, fail closed when preconditions cannot be verified, and surface explicit blocked/error states.
- **Recovery and verification:** persist enough workflow state to resume safely and check real AWS conditions after an operation; preserve required data and validate application health before claiming recovery.

Details and wire mappings must follow the approved design and PoC outcomes; the bullets above are scope statements, **not evidence that features are implemented**.

## Collaboration

Planning and approvals: [InfraFlow on Linear](https://linear.app/ducanh/project/infraflow-31b8c3b2d1ad).

- [Contributing guide](CONTRIBUTING.md): issue → branch → reviewable PR workflow.
- [Security policy](SECURITY.md): handling of public repository content and private cloud information.
- [GitHub collaboration agreement v0.2](https://linear.app/ducanh/document/infraflow-github-collaboration-and-integration-v02-public-pre-g4-8139b78c893a) (team access may be required).
- [Technical Design v1.2](https://linear.app/ducanh/document/infraflow-technical-design-v12-baseline-dja-chot-poc-xac-minh-chi-tiet-4d090c7a3d66) and [Interface Contracts v1.2](https://linear.app/ducanh/document/infraflow-interface-contracts-v12-baseline-logic-dja-chot-wire-mapping-94d3f67d204a) (baseline; team access may be required).

## Stage gates

| Gate | Meaning | Current statement |
|---|---|---|
| G0 | Design/interface baseline accepted | Confirmed on 19 October 2026 |
| G1 | Test AWS account, IAM, budget, region, scope and cleanup explicitly authorized | Must be approved before AWS PoC execution |
| G2 | Technical PoC evidence for open implementation questions | Requires executed and reviewed tests |
| G3 | PoC-driven implementation decisions / ADRs reviewed | Requires G2 evidence |
| G4 | Implementation plan reviewed and authorized | Required before product code, Terraform IaC or deployment |

**Do not run AWS PoC work without G1. Do not begin product implementation/IaC deployment before G4.** Documents and test plans may be prepared beforehand.

## Public repository

The project owner intentionally chose a **public repository**. Never commit credentials, personal data, raw Terraform state, saved plans, unredacted cloud inventories, backups or private test evidence. A `.gitignore` file helps avoid accidental commits but does not prevent a contributor from explicitly adding a file or remove information already published.

License: no open-source license has been selected at this stage; public visibility alone does not grant a general reuse license.
