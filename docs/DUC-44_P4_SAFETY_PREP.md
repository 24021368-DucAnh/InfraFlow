# DUC-44 / GitHub #4 — P4 safety PoC preparation

**Phần 1 — phạm vi và ranh giới để review.** Owner dự kiến: Nguyễn Huy Minh; reviewer: Trần Quý Đạt. Đây là tài liệu chuẩn bị thử nghiệm, không phải kết quả PoC hay phê duyệt chạy AWS.

## Nguồn và trạng thái quyết định

- [GitHub #4](https://github.com/24021368-DucAnh/InfraFlow/issues/4), Linear DUC-44 (nội dung issue được cung cấp): W7 yêu cầu ma trận lỗi cho ownership, permit, backup, scope, drift, lock, timeout, race và Verify. DUC-29 (controller) và DUC-31 (Reclaim/Verify) là các đầu mối review liên quan.
- [Kế hoạch tuần](TEAM_WEEKLY_PLAN.md) và các issue trên dẫn Technical Design / Interface Contracts **v1.2** làm baseline ngày 19/10/2026. Hai file v3.0 hiện có **cục bộ nhưng chưa được Git theo dõi** (`docs/InfraFlow_Technical_Design_v3.0.md`, `docs/InfraFlow_Interface_Contracts_v3.0.md`) ghi baseline logic ngày 24/10/2026; chúng không nằm trong commit P4 này. Không coi việc chốt logic là PoC pass hoặc G1/G4 approval. Cần Đạt xác nhận phiên bản dùng để đánh giá từng case và mọi khác biệt có ảnh hưởng đến expected outcome.
- Các quyết định và gate chính thức ghi trên Linear; checkbox GitHub không thay thế phê duyệt. Bản này chưa ghi nhận kết quả test AWS.

## Phạm vi P4

Xét Reclaim/Verify và các bước an toàn liên quan của **Create** và **Adopt** (Register workspace tương thích sau bàn giao). Với Adopt, việc thấy tài nguyên trong Terraform state không chứng minh quyền Reclaim; phải đối chiếu phạm vi và quyền trong handoff. Không áp dụng cho workspace Terraform bất kỳ hoặc tài nguyên production.

Mỗi case ở phần sau phân biệt điều kiện đầu vào, hành động được phép/không được phép, trạng thái operation/Environment kỳ vọng, bằng chứng quan sát, lối phục hồi, cleanup và kết quả thực tế (`NOT RUN`/`UNKNOWN`/`PASS`/`FAIL`). Các kết quả kỳ vọng dưới đây dựa trên v3.0 và cần đối chiếu với baseline của issue; **không phải** kết quả PoC.

## Ranh giới kiến trúc cần kiểm tra

| Bên | Trách nhiệm liên quan P4 | Điều không được suy diễn |
|---|---|---|
| API | Nhận yêu cầu, kiểm quyền người gọi, ghi Desired State và trả `operation_id`. | API đã nhận yêu cầu không có nghĩa hạ tầng đã đổi hoặc được quyền phá hủy. |
| Controller | Tính lại Desired State; kiểm Lease, capability, quyền vào AWS target, khóa và quan sát mới; tối đa một workflow thay đổi mỗi Environment; giữ `BLOCKED` khi không thể tiếp tục an toàn. | Terraform state không phải AWS Actual; `BLOCKED` không đồng nghĩa đã ngủ hay đã thu hồi. |
| Planner / Plan Validator | Lập các bước an toàn; đối chiếu Terraform plan với instance được phép, ownership/handoff, backup và scope; scoped permit gắn với operation và hash plan. | Có plan hoặc có tag không tự động cấp quyền apply/destroy. |
| Executor | Thực thi đúng plan được kiểm; ghi bằng chứng từng bước và trả kết quả, kể cả khi kết quả không rõ. | Không được dùng lại permit cũ hoặc xem timeout là thao tác đã thất bại an toàn. |
| Verify | Sau Reclaim, đối chiếu Terraform state, tài nguyên AWS theo phạm vi Environment, DNS và final backup nếu policy yêu cầu; chỉ sau hậu kiểm đầy đủ mới công bố `RECLAIMED`. | `terraform destroy` trả thành công không đủ chứng minh đã dọn sạch. |

Nguồn tham chiếu cục bộ, chưa thuộc commit P4: Technical Design v3.0, mục 3, 6, 8, 10–11; Interface Contracts v3.0, mục 2–3, 9–10, 14. Xem tên file ở mục “Nguồn và trạng thái quyết định”.

## Gate và cách ghi bằng chứng

1. **Trước G1:** chỉ soạn matrix, review và mô phỏng bằng dữ liệu giả. Không gọi AWS hay thử destructive action; không gắn nhãn `PASS` cho kỳ vọng trên giấy.
2. **Sau khi G1 được xác nhận cho đúng phép thử:** chỉ dùng account/slot, IAM, ngân sách, fake workspace/data, phạm vi tài nguyên, backup và phương án cleanup đã được duyệt. Không phá hủy khi thiếu permit, backup hoặc bằng chứng ownership. Lưu inventory trước/sau và kết quả đã lọc thông tin nhạy cảm.
3. **Khi chưa thử hoặc kết quả không rõ:** ghi `NOT RUN` kèm nguyên nhân hoặc `UNKNOWN` kèm bằng chứng còn thiếu; không suy ra `RECLAIMED`. Kết quả và câu hỏi chưa chốt bàn giao cho DUC-37; implementation plan tại DUC-36 chỉ sau các gate tương ứng.
4. Repo công khai: không đưa secret, raw Terraform state/plan, inventory riêng, dữ liệu khách hoặc log chưa làm sạch vào commit/issue. Xem [SECURITY.md](../SECURITY.md).

**Điểm cần reviewer xác nhận khi review case matrix:** baseline v1.2/v3.0 áp dụng cho DUC-44; ranh giới Controller–Validator khi thiếu ownership/permit; bằng chứng tối thiểu đủ để kết luận Verify, đặc biệt với Adopt.

## Phần 2 — năm case đầu để review

Quy ước: `origin=create/adopt` là nguồn Environment; `BLOCKED` là cờ của Environment và trạng thái operation, không thay thế availability quan sát cuối. Các bước giả định chỉ dùng workspace/inventory giả. **Tất cả case hiện `NOT RUN`**; không có AWS evidence hay reviewer sign-off. Trong mỗi case, “không thay đổi” nghĩa là không thực hiện thêm thao tác hạ tầng sau điểm dừng, không giả định những bước trước đó đã được đảo ngược.

| ID / origin / điểm kiểm | Dữ liệu đầu vào và kích thích | Expected: tác động, trạng thái | Evidence cần ghi (đã lọc thông tin nhạy cảm) | Recovery / cleanup dự kiến | Actual / cách thử |
|---|---|---|---|---|---|
| **P4-01 / adopt / handoff** | Workspace có state chứa database, nhưng biên bản bàn giao chưa xác nhận quyền `RECLAIM` hoặc writer cũ chưa ngừng. Yêu cầu Activate rồi Reclaim. | Handoff ở `AWAITING_HANDOFF`, `HANDOFF_INCOMPLETE`; chưa bật capability, chưa ghi state, chưa destroy. **Không** dùng riêng Terraform state làm bằng chứng ownership. | Hạng mục handoff còn thiếu, kết quả kiểm writer/khóa, trạng thái target và operation; inventory trước/sau để xác nhận không có thay đổi do phép thử. | Chủ workspace hoàn tất bàn giao và kiểm lại điều kiện; nếu không đạt thì giữ workspace ngoài quản lý, không thử destroy để “kiểm tra”. | `NOT RUN` — mô phỏng bằng handoff giả; AWS chỉ sau G1 và phê duyệt riêng. |
| **P4-02 / create + adopt / trước apply** | Operation định Reclaim; file plan đã kiểm và scoped permit thiếu, hết hiệu lực, hoặc hash plan hiện tại khác `plan_sha256` của permit. | Executor **không apply/destroy** file plan không được permit bao phủ; không `RECLAIMED`. Với plan đổi giữa lúc kiểm và apply, tạo plan mới và kiểm lại từ đầu. Mã/trạng thái của nhánh “permit thiếu/hết hạn” cần Đạt xác nhận; không tự gán `PLAN_UNSAFE` khi chưa có kết quả Validator. | `operation_id`, danh sách instance được phép, hash plan/permit, thời hạn, lỗi từ Validator/executor, inventory trước/sau. Không đưa plan thô lên repo. | Xác định vì sao permit sai; lấy quan sát mới, lập/kiểm plan mới nếu còn được phép; không tái dùng permit cũ. | `NOT RUN` — mô phỏng permit/hash giả; AWS chỉ sau G1 và phê duyệt riêng. |
| **P4-03 / create + adopt / trước xóa dữ liệu** | Policy yêu cầu giữ final backup; snapshot không thuộc operation hiện tại hoặc chưa `available`, trong khi plan sẽ xóa RDS. | Không xóa RDS. Snapshot lỗi hoặc không đạt `available` → `BLOCKED BACKUP_FAILED`; nếu Validator gặp plan xóa dữ liệu thiếu snapshot hợp lệ → `BLOCKED PLAN_UNSAFE` (V3). Không `RECLAIMED`. | Policy đã xác nhận, `operation_id`, snapshot ID/trạng thái/thời điểm, kết quả V3, trạng thái RDS và inventory trước/sau. Không công khai ID thực hoặc dữ liệu snapshot. | Admin xử lý nguyên nhân, quan sát lại snapshot rồi quyết định retry; giữ tài nguyên dữ liệu, chỉ cleanup tài nguyên test khi đã có quyền và bằng chứng backup phù hợp. | `NOT RUN` — mô phỏng trạng thái snapshot giả; AWS chỉ sau G1 và phê duyệt riêng. |
| **P4-04 / create + adopt / preflight** | Terraform state ghi RDS `STOPPED` nhưng quan sát AWS đọc trong operation ghi `RUNNING`, hoặc quan sát đã cũ; yêu cầu Reclaim. | Dừng trước plan phá hủy; `BLOCKED STALE_OR_CONFLICTING_EVIDENCE` đối với Environment đã Activate; không suy trạng thái AWS từ state và không `RECLAIMED`. Adopt ở pha Validate chỉ bị từ chối đọc, không tạo capability. | Serial/thời điểm state, nguồn và thời điểm AWS observation, các giá trị mâu thuẫn, operation/availability cuối, inventory trước/sau. | Điều tra drift hoặc writer khác; đọc lại state và AWS trong operation mới sau khi nguyên nhân đã xử lý; không tự sửa drift bằng destroy. | `NOT RUN` — mô phỏng hai observation giả; AWS chỉ sau G1 và phê duyệt riêng. |
| **P4-05 / create + adopt / Verify sau destroy** | Lệnh destroy đã trả thành công nhưng lượt Verify cuối vẫn thấy tài nguyên tag `infraflow:env_id`, hoặc state chưa rỗng, còn DNS riêng, hay không xác minh được final backup theo policy. | Không công bố `RECLAIMED`. Sau các lượt Verify có giãn cách, nếu vẫn thiếu điều kiện → `BLOCKED VERIFY_INCOMPLETE`, giữ danh sách mục còn sót; bản lưu cuối hợp lệ (`purpose=final-backup`) không tính là tài nguyên sót. | Kết quả từng lượt quét có thời điểm, danh sách tài nguyên thuộc phạm vi, state list, bản ghi DNS, tình trạng final backup, operation/availability và inventory trước/sau. | Admin đối chiếu tài nguyên thực và bằng chứng, xử lý từng phần còn sót rồi Verify lại; không tự lặp bước destroy khi outcome không rõ. Cleanup test chỉ sau khi có quyền và kiểm phạm vi. | `NOT RUN` — mô phỏng các nguồn Verify giả; AWS chỉ sau G1 và phê duyệt riêng. |

Nguồn expected cục bộ, chưa thuộc commit P4: Technical Design v3.0, mục 7.4, 8, 11; Interface Contracts v3.0, mục 9–10, 14, 16. Các ngưỡng thời gian Verify đánh dấu (\*) còn phụ thuộc PoC, không dùng làm bằng chứng case đã pass. Đạt cần review đặc biệt **P4-02** (lỗi và chủ thể dừng khi permit không hợp lệ) và điều kiện Verify đối với resource thiếu tag/ngoài state ở **P4-05**.

## Phần 3 — failure cases bổ sung

Cùng quy ước của phần 2: **expected chỉ là giả thuyết cần review; actual của mọi hàng là `NOT RUN`**. Nếu một bước đã thay đổi hạ tầng, “dừng” không hàm ý rollback thành công. Không tạo tài nguyên AWS hay chạy destroy để kiểm thử các nhánh từ chối.

| ID / origin / điểm kiểm | Dữ liệu đầu vào và kích thích | Expected: tác động, trạng thái | Evidence cần ghi (đã lọc thông tin nhạy cảm) | Recovery / cleanup dự kiến | Actual / cách thử |
|---|---|---|---|---|---|
| **P4-06 / create + adopt / plan scope** | Plan định xóa resource có `env_id` thuộc Environment khác hoặc resource dùng chung không nằm trong phạm vi bàn giao/instance được phép. | Validator từ chối trước apply: `BLOCKED PLAN_UNSAFE` (V1/V2/V6; Adopt còn V11); không destroy resource đó, không `RECLAIMED`. | Danh sách địa chỉ thay đổi đã lọc, env/instance được phép, phạm vi handoff nếu Adopt, luật vi phạm, inventory của cả Environment bị ảnh hưởng trước/sau. | Điều tra quyền sở hữu và sửa phạm vi/plan qua review; tuyệt đối không nới permit chỉ để pass. Cleanup theo chủ sở hữu từng resource. | `NOT RUN` — plan giả; AWS chỉ sau G1 và scope được duyệt. |
| **P4-07 / create + adopt / plan không đọc được** | `terraform show -json` thất bại hoặc JSON plan không phân tích được nên Validator không kiểm tra đủ V1–V12. | Không cấp permit, không apply/destroy, không `RECLAIMED`. **Mã lỗi và `BLOCKED`/`FAILED` tại điểm này cần Đạt xác nhận**: không gán `PLAN_UNSAFE` nếu Validator chưa thực sự đánh giá plan. | Exit code, lỗi parser đã lọc, hash/artifact ref của plan, có/không permit, operation step, inventory trước/sau. | Tạo plan mới và kiểm lại toàn bộ khi nguyên nhân đã rõ; không chạy apply file plan chưa được kiểm. | `NOT RUN` — artifact giả hỏng; AWS không cần cho phép thử parser. |
| **P4-08 / create + adopt / mất khóa hoặc writer cạnh tranh** | Sau khi operation đã bắt đầu, `active_operation_id`/state lock không còn khớp; với Adopt, writer cũ lại ghi state. | Không khởi chạy bước hạ tầng tiếp theo; không tự chiếm lại lock rồi tiếp tục. Adopt đã Activate có writer khác → `BLOCKED HANDOFF_VIOLATION`; nếu execution đã kết thúc mà khóa chưa nhả hoặc không biết outcome → `BLOCKED UNKNOWN_OUTCOME`. Không `RECLAIMED`. | Operation/lock holder, state serial trước/sau, thời điểm writer ghi, Step Functions execution status, bước cuối đã xác nhận, inventory trước/sau. | Admin đối chiếu state và AWS, dừng writer xung đột, xác minh quyền rồi mới quyết định mở BLOCKED; cleanup chỉ sau khi xác định bước nào đã chạy. | `NOT RUN` — mô phỏng lock/serial giả; AWS chỉ sau G1 và kiểm soát writer. |
| **P4-09 / create + adopt / retry Reclaim** | AWS API trả lỗi tạm thời, hoặc Terraform báo lỗi trong bước destroy sau khi có thể đã tác động một phần. | Lỗi API tạm thời: retry giới hạn theo thiết kế; không coi một lần gọi lỗi là chứng cứ chưa thay đổi. Terraform lỗi Reclaim: `BLOCKED` ngay, **không tự retry bước phá hủy** khi kết quả không rõ; không `RECLAIMED`. | Số lần gọi, mã lỗi, thời điểm, step, kết quả quan sát tài nguyên sau mỗi lần, state serial và inventory trước/sau. | Xác minh tài nguyên và state trước khi admin quyết định retry; không lặp destroy bằng request mới chỉ vì client timeout. | `NOT RUN` — mô phỏng lỗi ở hai ranh giới riêng; AWS chỉ sau G1. |
| **P4-10 / create + adopt / operation đồng thời** | Reclaim đang `RUNNING`; nhận lại yêu cầu cùng mục tiêu, hoặc nhận Sleep/Wake tay trái mục tiêu. | Yêu cầu cùng mục tiêu trả `operation_id` đang chạy; thao tác tay ngược chiều bị từ chối `CONCURRENT_OPERATION`, không xếp hàng ngầm. Tối đa một workflow thay đổi mỗi Environment; Reclaim đang chạy không bị hủy. | Request key/payload đã lọc, `active_operation_id`, response và audit cho từng request, số execution thực tế, inventory trước/sau. | Chờ workflow hiện tại kết thúc rồi đối soát; không gỡ khóa để chạy yêu cầu thứ hai. | `NOT RUN` — mô phỏng hai request đồng thời; AWS không cần cho logic từ chối. |
| **P4-11 / create + adopt / Extend ↔ Reclaim race** | Lease đang hết hạn; Reclaim đã nhận và giữ khóa, đồng thời người quản lý gửi Extend. | Không hủy Reclaim giữa chừng và không chạy workflow trái chiều song song. Extend phải khớp `version`, hạn mới lớn hơn hạn cũ và hiện tại; Lease đã `RECLAIMED` thì từ chối. **Contract chưa nói rõ có nhận Extend khi `RECLAIMING` hay không** — cần Hoàng/Đạt xác nhận. Nếu được nhận, controller xét hạn mới ở lượt đối soát kế tiếp; không hứa cứu được môi trường đã xóa. | Thời điểm/version của Lease, kết quả API Extend hoặc lỗi, operation step/lock, Desired State tính lại sau workflow, AWS/state observation và inventory trước/sau. | Nếu Extend bị từ chối, thông báo trạng thái thực; nếu được nhận, chỉ đối soát sau khi outcome Reclaim rõ; không tự phục hồi từ backup khi chưa có kế hoạch được duyệt. | `NOT RUN` — mô phỏng thứ tự sự kiện giả; AWS không cần cho race logic. |
| **P4-12 / create + adopt / executor timeout** | Step Functions/CodeBuild quá timeout khi đang Reclaim; controller không biết destroy đã hoàn tất hay chưa. | `BLOCKED TIMEOUT` hoặc `UNKNOWN_OUTCOME` theo điểm phát hiện, không suy thành `FAILED` an toàn; dù khóa được nhả ở nhánh lỗi, cờ `BLOCKED` vẫn ngăn khởi chạy destroy lần hai. Không `RECLAIMED`. Reviewer xác nhận cách phân biệt hai mã trong tình huống execution còn chạy/đã mất dấu. | Execution ID, bước cuối, timeout, CodeBuild/Validator artifact refs, state serial và AWS observation mới, inventory trước/sau. | Admin điều tra execution và tài nguyên thực, chặn writer mới; quyết định retry/cleanup sau khi outcome rõ, không dùng log timeout thay hậu kiểm. | `NOT RUN` — mô phỏng timeout; AWS chỉ sau G1. |
| **P4-13 / create + adopt / Verify thiếu bằng chứng** | Destroy trả thành công, nhưng một lượt Tagging API hoặc truy vấn DNS/state lỗi; các lượt Verify có giãn cách vẫn không thu đủ bằng chứng, dù chưa thấy tài nguyên sót. | Không coi “không nhìn thấy” là “không còn”; không `RECLAIMED`. Nếu sau lượt cuối vẫn không chứng minh đủ điều kiện Verify thì `BLOCKED VERIFY_INCOMPLETE` theo ý nghĩa fail-closed; **cần Đạt xác nhận mã lỗi chi tiết khi scan lỗi thay vì trả danh sách còn sót**. | Kết quả/exception và thời điểm từng lượt, nguồn nào thiếu, state list, DNS, final backup nếu cần, inventory trước/sau. | Sửa khả năng quan sát, quét lại toàn bộ phạm vi trước khi admin mở BLOCKED; không tự destroy thêm chỉ vì scan lỗi. | `NOT RUN` — mô phỏng nguồn Verify lỗi; AWS chỉ sau G1. |

Nguồn expected cục bộ, chưa thuộc commit P4: Technical Design v3.0, mục 7.4, 10–11; Interface Contracts v3.0, mục 9–10, 14, 16. Lỗi AWS API có retry giới hạn, nhưng Reclaim lỗi Terraform hoặc outcome phá hủy không rõ phải fail closed. Những nhánh chưa có mã lỗi/chính sách Extend cụ thể được ghi là câu hỏi review, không phải hợp đồng đã chốt.

## Phần 4 — bàn giao review và điều kiện chạy PoC

### Gửi Đạt review trước khi thử

Gửi liên kết tài liệu này trong DUC-44 và GitHub #4; đề nghị Trần Quý Đạt ghi nhận **đồng ý / cần sửa / chưa quyết định** cho từng nhóm sau, kèm lý do và phiên bản contract được dùng:

1. **Writer/state safety:** P4-01, P4-04, P4-08 — xác nhận ownership/handoff, nguồn AWS Actual, state serial và bằng chứng lock; phân biệt từ chối Adopt Validate với `BLOCKED` sau Activate.
2. **Permit/validator:** P4-02, P4-03, P4-06, P4-07 — điểm dừng trước apply, V1/V2/V3/V6/V11, hash của plan và phân loại lỗi khi plan/permit không kiểm được.
3. **Controller và lỗi không rõ:** P4-09–P4-12 — khóa, idempotency, retry, timeout, `FAILED` so với `BLOCKED`; hỏi thêm Hoàng về Extend khi `RECLAIMING`.
4. **Verify và cleanup:** P4-05, P4-13 — phạm vi scan, resource thiếu tag/ngoài state, bằng chứng final backup, cách xử lý scan lỗi và điều kiện mở `BLOCKED`. Không xác nhận `RECLAIMED` khi một nguồn kiểm chứng bắt buộc còn thiếu.

Các câu hỏi v1.2 ↔ v3.0 và câu trả lời review là **đầu vào cho DUC-37**, không tự sửa contract từ kết quả giả lập. Reviewer chưa phản hồi thì giữ trạng thái “chờ review”; không đánh dấu issue hoàn tất thay reviewer.

### Điều kiện đề nghị G1 và phân luồng phép thử

**Chưa có xác nhận G1 trong tài liệu này; toàn bộ hàng đang `NOT RUN`.** Trước một AWS probe, gửi chủ tài khoản/người duyệt G1 đề nghị có ghi rõ: ID case và bước được phép; account/region/slot riêng; IAM và quyền destroy tối thiểu; giới hạn chi phí/thời gian; fake workspace, fake data và resource inventory; chủ sở hữu state/DNS; chính sách retention/backup; đường dừng khẩn, người chịu trách nhiệm cleanup và đối chiếu inventory sau thử. Với Adopt, phải có bàn giao hợp lệ, độc quyền writer và quyền Reclaim **riêng cho workspace test**. G1 chỉ cho phép đúng phạm vi đã duyệt, không mặc nhiên cho phép mọi case hoặc mọi destructive action.

| Nhánh | Khi nào được chạy | Cách ghi kết quả |
|---|---|---|
| **Mô phỏng/dry-run không AWS** | Ngay sau khi thống nhất expected; dùng request, plan JSON, snapshot status, observation và inventory **giả**. Trường hợp parser lỗi P4-07 và xung đột request P4-10/11 phù hợp nhánh này. | Ghi `SIMULATED`, input giả, actual quan sát được và sai khác so với expected; không gọi đó là AWS PoC `PASS`. |
| **AWS read-only** | Chỉ khi G1 ghi rõ quyền/slot/account và dữ liệu test; chỉ đọc state/AWS/lock/backup, đối chiếu before/after. Không lấy thông tin thật của khách để thử. | Ghi `AWS READ-ONLY`, điều kiện G1, nguồn/thời điểm quan sát và inventory đã lọc; không kết luận đã chứng minh guardrail phá hủy. |
| **AWS có thay đổi hạ tầng** | Chỉ khi G1 **cho phép chính xác case đó**, Đạt đã review, fake workspace/data được cô lập, quyền/ownership, permit, backup và cleanup đã xác minh. Không chạy destructive action để thử nhánh *thiếu* các điều kiện này; nhánh từ chối dùng mô phỏng. | Ghi `AWS APPROVED`, approval ref, phạm vi, expected/actual, inventory trước/sau, chi phí/thời gian và cleanup xác nhận. Nếu outcome không rõ: `UNKNOWN`/`BLOCKED`, dừng và báo người duyệt. |

**Stop rule:** mất quyền, mất lock/writer độc quyền, lệch state–AWS, plan ngoài scope, backup không `available` khi policy yêu cầu giữ dữ liệu, permit không hợp lệ, timeout hoặc Verify không đầy đủ → dừng mọi bước thay đổi tiếp theo; không tự retry destroy; ghi bằng chứng đã lọc và chuyển người có thẩm quyền xử lý. Không coi dọn tài nguyên thử nghiệm là ngoại lệ cho ownership/backup/permit.

### Mẫu một bản ghi kết quả (dùng riêng cho từng case và origin)

```text
Case ID / origin / mode:                 P4-xx / create|adopt / SIMULATED|AWS READ-ONLY|AWS APPROVED
Approval G1 ref + scope (nếu AWS):       NOT APPLICABLE hoặc liên kết quyết định, không chứa secret
Input + điểm tiêm lỗi (đã làm sạch):     ...
Expected / actual / sai khác:            ... / NOT RUN / ...
Status + lý do:                          NOT RUN | UNKNOWN | PASS | FAIL
Operation/availability/blocked:          ... / ... / ...
AWS observation + thời điểm; state serial: ... / ...
Permit/plan hash + snapshot status:      ... / ...
Inventory trước/sau; Verify từng nguồn:  ... / ...
Cleanup trước/sau + người xác nhận:      ...
Evidence ref an toàn để công khai:       ...
Reviewer + vấn đề chưa giải quyết:       ...
```

Mẫu trên **chưa phải kết quả**: chỉ điền actual sau khi thực sự chạy theo mode tương ứng. Nếu không đủ bằng chứng, ghi `UNKNOWN` hoặc `NOT RUN` cùng lý do, không gắn `PASS`.

### Chuyển kết quả sang DUC-37 và DUC-36

- DUC-44 / #4: đính kèm tài liệu/PR, phản hồi reviewer, trạng thái từng case và blocker G1; không tick case “đã thử” chỉ vì đã viết expected.
- DUC-37 (G2/G3): chuyển safety gates và taxonomy lỗi đã review, bảng expected–actual theo **từng origin/mode**, bằng chứng đã làm sạch, inventory/cleanup và câu hỏi chưa quyết định. Không diễn giải baseline đã chốt thành PoC đạt.
- DUC-36 (G4): chỉ đưa **quyết định đã review** và case chưa đạt/`UNKNOWN` làm dependency cho implementation plan; trước G4 không bắt đầu product code, Terraform IaC hoặc deployment.
