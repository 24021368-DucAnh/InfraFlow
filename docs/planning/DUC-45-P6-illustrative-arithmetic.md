# DUC-45 — Illustrative P6 arithmetic

**Status:** Planning arithmetic only · **Rates:** copied from the Hoàng draft and not independently verified · **AWS tests:** NOT RUN (G1 not approved)

Source inputs: [Hoàng's DUC-45 test plan](https://docs.google.com/document/d/1UbH1cfdQKijbV51Ro9APtGNbfVDPKgcxRUYMzrm7XOw) and [Đức Anh review copy with the expanded calculation](https://docs.google.com/document/d/1YRb5Z8dDZz53nfGHsEuAPVSzRhAlznRfdP8K87sxnfo). This file exposes calculation mechanics only. It is not a current AWS quote, regional price verification, bill forecast, savings claim, or approval of the assumed topology. Recalculate with the AWS Pricing Calculator or official regional price pages once service configuration, purchase model, tenancy, storage, traffic, backup, tax and usage are confirmed. Actual charges can only be measured after G1 authorization.

## Scenario assumptions

- Measurement period A-05: 1 November 2026 00:00 through 1 January 2027 00:00 Asia/Ho_Chi_Minh = 61 calendar days.
- Three environments each use one t3.small Linux app, one db.t4g.micro PostgreSQL DB and 20 GB gp3 storage, as assumed in A-06/A-08.
- Treat the supplied compute rates as hourly only for arithmetic: app $0.0264/hour; DB $0.0160/hour. Their regional source/configuration is unverified.
- A-07 schedule: 11 hours/day, Monday–Friday. The period has 44 weekdays (484 scheduled hours) and 17 weekend days (408 hours).
- Illustrative stop-only and Deep Sleep cases run compute only in the scheduled hours; DB storage remains billed all 61 days. This does not assert a supported RDS stop/start lifecycle.
- Excluded: NAT, IPv4, DNS, TLS, ALB/edge, data transfer, snapshots/backups, monitoring, API/control plane, tax, discounts, start/stop minimums and one-time operations. Totals are lower-bound subtotals, not complete environment cost.

## Rate-derived subtotals

Storage per environment: 20 GB × $0.08/GB-month × (61/30 days) = **$3.2533**.

| Scenario | Compute hours per environment | Arithmetic per environment | Three-environment Lease |
|---|---:|---:|---:|
| 24/7 | 1,464 | 1,464 × ($0.0264 + $0.0160) + $3.2533 = **$65.3269** | **$195.9807** |
| Stop-only | 484 | 484 × $0.0424 + $3.2533 = **$23.7749** | **$71.3247** |
| Deep Sleep (illustration) | 484 | 484 × $0.0424 + $3.2533 = **$23.7749** | **$71.3247** |
| Reclaimed after day 20 (illustration) | 480 | 480 × $0.0424 + $3.2533 = **$23.6053** | **$70.8159** |

Deep Sleep equals stop-only under these assumptions because no separate route/front-door or Wake-event charges are included; do not call this demonstrated savings. For the Reclaim illustration, compute is assumed to run continuously during the first 20 days, then stop; storage remains for all 61 days. Snapshot retention, teardown and other residual costs are excluded. Reclaim is not assumed to erase retained storage or backups.

## Interpretation and remaining work

The arithmetic checks only multiplication of supplied assumptions. It does not validate rates, AWS service support, billing granularity, stop behavior, workload, Deep Sleep feasibility, savings, or a public-route design.

- **P6-01:** Verify region-specific source/configuration and date.
- **P6-02:** Complete three-scenario estimate with included and excluded resources.
- **P6-03:** Inventory resources and retention after Sleep and Reclaim.
- **P6-04:** Verify billing minimums/granularity and operation charges.
- **P6-05:** Estimate-versus-actual remains NOT RUN until G1.
- **P6-06:** Add route, DB-topology and schedule sensitivity after G3 candidate choices are known.
- **P3-08/P5-08:** Owner and peer review still needed. All P3/P5 AWS cases remain NOT RUN until G1.
