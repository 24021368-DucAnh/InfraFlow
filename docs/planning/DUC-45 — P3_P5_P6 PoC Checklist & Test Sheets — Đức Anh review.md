# **DUC-45 — P3/P5/P6 PoC Checklist & Test Sheets**

**Date:** 2026-10-31  
**Status:** TEST PLAN ONLY / NOT RUN (G0)  
**Author:** Hà Hải Hoàng (AI-assisted draft — confirm before commit)  
Reviewers proposed: Đức Anh (DUC-45 reviewer; owner of P3-08/P5-08), Minh (Reclaim/backup retention), Đạt (state/ownership).

**Tracking:** GitHub issue \#5 \| Linear DUC-45 (child of DUC-24) \| evidence gate DUC-37.  
G0 accepted 19/10/2026.

# **0\. Gate and public-safety rules**

* **No AWS action before G1.** Everything in this sheet is documentation or arithmetic on stated assumptions until the AWS account owner signs G1.  
* **No cost claim is PASS on an estimate alone.** Savings are never reported as "achieved" until measured.  
* **Public repo.** Do not commit AWS account IDs, billing screenshots, Cost Explorer exports, budget amounts, credit balances, invoices or raw logs. Keep private evidence in owner-approved restricted storage.

# **1\. DUC-45 — P6 Cost Model Evidence/Test Sheet**

## **Assumption Register**

* A-01: AWS region `ap-southeast-1` (ASSUMED)  
* A-02: Currency `USD` (ASSUMED)  
* A-05: Measurement window `[2026-11-01T00:00, 2027-01-01T00:00) in Asia/Ho_Chi_Minh` (ASSUMED)  
* A-06: Scale `3 Environments (dev, qa, uat)` in one Lease (ASSUMED)  
* A-07: Schedule Mon–Fri 08:00–19:00 local (ASSUMED)  
* A-08: Size "Small" \- App: `t3.small`; DB: `db.t4g.micro`; DB storage `20 GB gp3` (ASSUMED)  
* A-09: Sleep level `Deep Sleep only` (ASSUMED)  
* A-14: Register-origin resources (Cost scope \= exclusive resources only)

## **Rates recorded 2026-10-31 (regional source/configuration verification pending)**

* **EC2 t3.small (Linux):** \$0.0264/hour  
* **RDS db.t4g.micro (PostgreSQL):** \$0.0160/hour  
* **NAT Gateway:** \$0.059/hour (duy trì) \+ \$0.045/GB (xử lý dữ liệu)  
* **Public IPv4:** \$0.005/hour  
* **EBS gp3:** \~\$0.08/GB-month  
* Rate note: These are recorded figures, not yet substantiated as verified regional rates. Add an AWS official source or Pricing Calculator estimate and its date, ap-southeast-1 Region and service configuration before using them as verified. Include applicable data transfer, snapshots/backups, public IPv4, ALB/front door and DNS. Estimates are not actual bills.

## **P6 Cases (NOT RUN)**

* **P6-01:** Price register \-\> BP-12, URL-12  
* **P6-02:** Three-scenario model \-\> BP-12  
* **P6-03:** Residual cost while asleep and after Reclaim  
* **P6-04:** Billing granularity and minimums  
* **P6-05:** Estimate vs actual (Sau G1)  
* **P6-06:** Sensitivity (Front-door, DB topology, wake/sleep time)

# **2\. DUC-45 — P3 Test Sheet Draft (Dependency & Health)**

*Mục tiêu: Đảm bảo tính toàn vẹn dữ liệu, thứ tự khởi động và cơ chế Health Check (Không giả định RDS Hibernate).*

* **P3-01:** (Stop) Gửi lệnh Stop DB. Kiểm tra trạng thái DB chuyển sang STOPPED. (PASS: DB dừng hoàn toàn, không dùng Hibernate).  
* **P3-02:** (Wake) Gửi lệnh Start. (PASS: DB khởi động trước, EC2 chỉ start khi DB báo AVAILABLE & passed health check).  
* **P3-03:** (Restart 7 ngày) Theo dõi trạng thái DB ở ngày thứ 8 sau khi stop. (PASS: Bắt được event AWS tự start lại RDS và có kịch bản xử lý).  
* **P3-04:** (Data preservation) Ghi data \-\> Stop \-\> Start \-\> Đọc lại data. (PASS: Dữ liệu nguyên vẹn sau khi wake up).  
* **P3-05:** (Reclaim) Kích hoạt kịch bản Reclaim. (PASS: Tạo Final Snapshot/Backup trước khi xóa RDS/EC2).  
* P3-08: (Cost comparison) Estimate 24/7, stop-only and Deep Sleep for the same Web+DB workload and the P6 scenario. Include retained and one-time costs; use A-14 to limit Register-origin scope to exclusive resources. Compare P6-01/02/03/04/06. P6-05 actual-cost evidence only after G1. (NOT RUN; no savings claim)

# **3\. DUC-45 — P5 Test Sheet Draft (DNS & Stable URL)**

*Mục tiêu: Trải nghiệm định tuyến DNS mượt mà, URL không đổi, chứng chỉ bảo mật và Sleeping Page.*

* **P5-01:** (Deep Sleep) Truy cập URL của môi trường. (PASS: Trả về Sleeping Page đúng chuẩn, không lỗi SSL).  
* **P5-02:** (Cutover) Truy cập URL trong quá trình Wake. (PASS: Chặn traffic hoặc hiển thị "Waking up" cho đến khi Web pass Health Check).  
* **P5-03:** (DNS TTL) Trỏ Domain giữa Sleeping Page và ALB/Web đích. (PASS: Thời gian propagate nằm trong ngưỡng cho phép).  
* **P5-04:** (TLS/SSL) Truy cập qua HTTPS vào Stable URL lúc thức và ngủ. (PASS: Certificate hợp lệ, không lỗi ownership ở cả 2 trạng thái).  
* P5-08: (Stable URL cost) Estimate recurring and one-time cost of keeping the public route available during Sleep using P6-01/02/03/04/06 and the same A-01/A-02/A-05–A-09 assumptions. Break out candidate DNS, TLS, edge/ALB, public IPv4 and transfer charges where applicable; do not assume a route architecture. Actual cost only after G1. (NOT RUN)

# **4\. Interface Mapping & UI/API Assumptions vs Contracts v1.2**

* **Create/Register:** Ánh xạ tới `Environment.resourceOwnershipClass` (MAPPED) \- Phân loại rõ resources thuộc scope tính tiền.  
* **Lease (Policy):** Ánh xạ tới `Lease (startsAt, expiresAt, timeZone, schedule)` (MAPPED).  
* **Operation (Wake/Sleep):** OPEN (O-02) \- Thiếu record lưu state-history dành riêng cho việc tính billing tự động.  
* **Cost Dashboard (Manager):** OPEN (O-01) \- Bảng Web API trong Contracts v1.2 §3 chưa có API cho tính năng báo cáo chi phí.  
* P3-08 → P6-01/02/03/04/05/06: Compare 24/7, stop-only and Deep Sleep estimates on the same Web+DB workload and P6 assumptions. Keep retained and one-time costs separate; actual-cost evidence is only after G1. (NOT RUN)  
* P5-08 → P6-01/02/03/04/05/06: Estimate recurring and one-time public-route costs during Sleep on the same assumed window/scale. Break out candidate DNS, TLS, edge/ALB, IPv4 and transfer costs where applicable; the route is not selected. Actual costs only after G1. (NOT RUN)  
* BP-12 → P6-01/02/03/04/05/06: Use A-01, A-02 and A-05–A-09 for the comparison scenario; for Register include only exclusive resources per A-14. Estimate is not achieved savings. (NOT RUN)  
* URL-12 → P6-01/02/03/04/05/06: Use the same assumptions and show public-route costs while asleep separately from application/database costs; front-door amounts remain candidate estimates until G3. (NOT RUN)

# **5\. Open Questions & Responsibilities**

* **Q-01: Confirm whether v3.0 (24/10) has an approved replacement decision. The current Linear project record names v1.2 as accepted on 19/10; keep v1.2 as source of truth until an authorized replacement/ADR is recorded. (Đạt / project owner; written confirmation pending)**  
* **Q-02: RESOLVED FOR THIS TEST PLAN — P3-08, P5-08, BP-12 and URL-12 use the P6 scenario assumptions A-01, A-02 and A-05–A-09; see the mapping above. These remain estimates/assumptions, not approved requirements or cost claims. (Đức Anh; peer/account review remains open)**  
* **Q-03:** Does the account owner approve ap-southeast-1 and USD? (Account owner)  
* **Q-04: For this P6 scenario only, A-08 assumes app t3.small, PostgreSQL db.t4g.micro and 20 GB gp3. v1.2 does not mandate these sizes; confirm before using them outside the estimate. (Đức Anh; review pending)**  
* **Hoàng:** P6 author; independent review of P3/P5 sheets.  
* **Đức Anh:** DUC-45 reviewer; owner of P3/P5 sheets and G1 package.

6\. DUC-45 — Illustrative P6 arithmetic (NOT a verified price estimate)  
Purpose and limits  
This appendix demonstrates calculation mechanics only, using the unverified rates listed above. It is not a current AWS quote, regional price verification, bill forecast, savings claim, or approval of the assumed topology. Recalculate with the AWS Pricing Calculator or official regional price pages after service configuration, purchase model, tenancy, storage, traffic, backup, tax and usage are confirmed. Actual charges are only measurable after G1 authorization.

Scenario assumptions  
\- Measurement period A-05 spans 61 calendar days: 1 November 2026 00:00 through 1 January 2027 00:00, Asia/Ho\_Chi\_Minh.  
\- Three environments each use one t3.small Linux app, one db.t4g.micro PostgreSQL DB, and 20 GB gp3 storage as in A-06/A-08. The rates are treated as hourly simply for arithmetic; the source/configuration is unverified.  
\- Schedule A-07 is 11 hours/day, Monday–Friday. The window includes 44 weekdays (484 scheduled hours) and 17 weekend days (408 hours). The model treats stop-only as running only during scheduled hours; Deep Sleep as compute stopped outside those hours; DB storage remains billed all 61 days. This is illustrative and does not assert a supported RDS operation.  
\- Excludes NAT, IPv4, DNS, TLS, ALB/edge, data transfer, snapshots/backups, monitoring, API/control plane, taxes, discounts, startup/stop minimums and all one-time operations. These exclusions mean every total below is a lower-bound subtotal, not a complete environment cost.

Rate-derived subtotals per environment  
\- App hourly rate: \$0.0264; DB hourly rate: \$0.0160; combined running rate: \$0.0424/hour.  
\- Storage subtotal: 20 GB × \$0.08/GB-month × (61/30 days) \= \$3.2533.  
\- 24/7 subtotal: 1,464 hours × \$0.0424 \+ \$3.2533 \= \$65.3269 per environment; ×3 \= \$195.9808 for the Lease.  
\- Stop-only subtotal: 484 hours × \$0.0424 \+ \$3.2533 \= \$23.7749 per environment; ×3 \= \$71.3248 for the Lease.  
\- Deep Sleep illustrative subtotal: the same 484 scheduled hours × \$0.0424 \+ \$3.2533 storage \= \$23.7749 per environment; ×3 \= \$71.3248. This equals stop-only under these assumptions because no distinct route/front-door or Wake-event costs are included; it must not be presented as demonstrated savings.  
\- Reclaimed-after-day-20 illustration: assume compute ran continuously for the first 20 days (480 hours), then stopped; storage remains for all 61 days. Cost is 480 × \$0.0424 \+ \$3.2533 \= \$23.6053 per environment / \$70.8160 for three environments, before snapshot retention, teardown and other residual costs. Reclaim is not assumed to remove retained storage or backups.

Interpretation  
The arithmetic validates only multiplication of supplied assumptions. It does not validate the supplied rates, service support, billing granularity, stop behavior, actual workload, Deep Sleep feasibility, price savings, or a selected public-route architecture. P6-01 regional source verification; P6-03 resource inventory and retention; P6-04 billing minimums; P6-06 route/topology sensitivity; P3-08/P5-08 owner and peer review all remain OPEN. P6-05 estimate-versus-actual and every P3/P5 AWS case remain NOT RUN until G1.  
