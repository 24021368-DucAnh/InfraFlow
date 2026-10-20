# Security Policy

InfraFlow is a Cloud Computing course project. Its GitHub repository is intentionally **public**. Repository visibility does not authorize publication of sensitive infrastructure information.

## Never publish

- AWS keys, cloud access tokens, private keys, passwords, session credentials or real connection strings.
- Terraform state and backups (`*.tfstate`), saved Terraform plans, local variable files containing sensitive values, private inventory or unredacted infrastructure logs.
- Personal data, customer/tenant data, private budget/billing details, database snapshots or unapproved test evidence.

Use placeholders and sanitized examples only. `.gitignore` is a prevention aid, not a security boundary. Deleting a leaked secret from a file does not remove it from commit history or external copies.

## Security and vulnerability reports

Do not report working exploits or secrets in public GitHub issues or PRs. Contact the repository owner through an agreed private team channel. If GitHub private vulnerability reporting is enabled, that may be used; do not assume it is configured.

If exposure occurs: **stop using the secret, notify the appropriate owner privately, rotate/revoke it, assess the affected resources, and address commit-history exposure**. Do not paste the exposed value in discussion.

## Cloud operations safety

- Real AWS PoC requires explicit **G1** permission covering account, IAM, region, cost limit, cleanup and resource scope.
- Implementation and Terraform IaC must not begin before approved **G4**.
- Never treat an incomplete, denied, ambiguous or unverified operation as successful. Preserve the project's fail-closed and BLOCKED rules.
- The use of a public source repository must not grant credentials or execution permission to unaudited contributions.

Security contact: use the project owner's private team channel. A public email address or private-vulnerability-reporting endpoint has not been established.
