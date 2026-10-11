# Phân công 32 task trong 8 tuần

Trạng thái thực tế ghi trong `tasks.csv`. Các paths tính từ gốc repo. Owner/reviewer sẽ được thay bằng tên trong `team.md`.

## Tuần 1 — 12–18/10/2026

Mục tiêu: Dữ liệu và mô hình chạy đúng.

### 1A — CAM và môi trường

**Người 1** · Review: Người 2 · Hạn: 15/10/2026

- **Mục tiêu:** Có CAM đúng lớp để mọi thí nghiệm dùng chung.
- **Cần trước:** Chốt GPU và nơi lưu dự án.
- **Bước làm:** 1. Tạo môi trường, pin code ExCEL/SAM và trọng số CLIP. 2. Viết cam_provider.py chạy SVC. 3. Xuất CAM cho 10–20 ảnh và vẽ overlay.
- **Nơi lưu:** src/cam_provider.py; configs/cam.yaml; results/pilot/cam/; docs/environment.txt.
- **Đầu ra phải có:** NPZ gồm CAM float, tên/mã lớp, image_id và size gốc; log phiên bản, checkpoint hash.
- **Nghiệm thu/lưu ý:** Người 2 kiểm CAM cow đúng kênh, không NaN và overlay đúng ảnh; sửa lệch lớp trước khi tiếp tục.

### 1B — SAM và pilot

**Người 1** · Review: Người 2 · Hạn: 18/10/2026

- **Mục tiêu:** SAM nhận prompt đúng tọa độ và có ước lượng chi phí.
- **Cần trước:** CAM mẫu và class map từ 1A/1C.
- **Bước làm:** 1. Viết SAM wrapper frozen. 2. Vẽ điểm xy lên ảnh, gọi SAM theo từng bộ prompt. 3. Lưu candidates/score; đo thời gian sau warm-up.
- **Nơi lưu:** src/sam_wrapper.py; results/pilot/sam/; results/pilot/cost.csv.
- **Đầu ra phải có:** Binary masks đúng size gốc; prompt_xy, point_labels, qSAM và candidate index; log GPU/VRAM.
- **Nghiệm thu/lưu ý:** Người 2 kiểm 10 ảnh, không đảo xy; mỗi ảnh tái dùng embedding, không cập nhật trọng số.

### 1C — Dữ liệu và nhãn ảnh

**Người 2** · Review: Người 1 · Hạn: 15/10/2026

- **Mục tiêu:** Dữ liệu đọc đúng và mỗi kênh CAM ánh xạ được sang lớp.
- **Cần trước:** Nguồn VOC2012/SBD và danh sách train_aug.
- **Bước làm:** 1. Kiểm file ảnh/mask, size và ID. 2. Tạo nhãn mức ảnh từ XML hoặc nguồn tag đã xác minh. 3. Lập class_map.json và test cow.
- **Nơi lưu:** data/raw/; data/metadata/inventory.csv, image_tags.json, class_map.json.
- **Đầu ra phải có:** Inventory ghi nguồn, số ảnh, file lỗi; tag đa nhãn theo image_id; map nền 0, đối tượng 1–20, ignore 255.
- **Nghiệm thu/lưu ý:** Người 1 đọc lại PNG và kiểm cow CAM 9 → ID 10; không dùng vị trí/box GT làm prompt.

### 1D — Split và evaluator

**Người 2** · Review: Người 1 · Hạn: 18/10/2026

- **Mục tiêu:** Tách dữ liệu công bằng và có metric tính đúng.
- **Cần trước:** Inventory và tag từ 1C.
- **Bước làm:** 1. Giữ dev khoảng 300–500 ảnh từ train_aug đã xác minh. 2. Train-fit loại dev, val giữ riêng. 3. Hash list và test IoU trên mask tính tay.
- **Nơi lưu:** data/lists/train_fit.txt, dev.txt, val.txt; src/metrics.py; tests/test_metrics.py.
- **Đầu ra phải có:** List có seed/hash và không trùng ID; test gồm đúng, sai, GT void; ghi cách dùng GT dev.
- **Nghiệm thu/lưu ý:** Người 1 kiểm giao tập và mẫu IoU; nếu chỉ VOC train gốc, giảm dev và ghi lý do.

## Tuần 2 — 19–25/10/2026

Mục tiêu: Có baseline và ngân sách đáng tin.

### 2A — B0 và B1

**Người 1** · Review: Người 2 · Hạn: 22/10/2026

- **Mục tiêu:** Có mốc CAM-only và CAM cộng SAM một điểm.
- **Cần trước:** 1A–1D chạy đúng.
- **Bước làm:** 1. Chốt chuyển CAM thành B0 có background/ignore. 2. B1 lấy một cực đại/lớp, chọn mask qSAM cao nhất. 3. Chạy cùng dev và lưu PNG chỉ số.
- **Nơi lưu:** configs/B0.yaml, B1.yaml; src/fusion.py; results/<run_id>/pseudo/.
- **Đầu ra phải có:** Một mask/ảnh; config ghi ngưỡng, NMS, xử lý tranh chấp; manifest đủ ảnh và lỗi.
- **Nghiệm thu/lưu ý:** Người 2 kiểm mask ID, ảnh không mask và lớp chồng lấn; không đổi fusion riêng cho B1.

### 2B — B2 và smoke train

**Người 1** · Review: Người 2 · Hạn: 25/10/2026

- **Mục tiêu:** Có baseline mạnh B2 và biết segmenter chạy được.
- **Cần trước:** B1, evaluator và ngân sách pilot.
- **Bước làm:** 1. Chọn top-K local maxima có NMS. 2. Mỗi điểm là một bộ prompt riêng, lưu candidates. 3. Smoke train B0 với SegFormer-B0.
- **Nơi lưu:** src/prompts.py; configs/B2.yaml, train.yaml; cache/<cache_id>/; results/smoke/.
- **Đầu ra phải có:** Cache đủ metadata; logs loss/VRAM; config encoder ImageNet, head mới, batch và số bước.
- **Nghiệm thu/lưu ý:** Người 2 kiểm điểm không trùng và loss hữu hạn; không dùng checkpoint segmenter đã train GT VOC.

### 2C — Metric nhãn giả

**Người 2** · Review: Người 1 · Hạn: 22/10/2026

- **Mục tiêu:** Metric không tăng giả do bỏ qua nhiều pixel khó.
- **Cần trước:** Metric nền từ 1D và B0/B1 mẫu.
- **Bước làm:** 1. Tính full mIoU trên GT hợp lệ. 2. Tách assigned precision, coverage, ignore ratio. 3. Test prediction toàn ignore, phủ nửa và sai lớp.
- **Nơi lưu:** src/metrics.py; tests/test_pseudo_metrics.py; results/metric_checks/.
- **Đầu ra phải có:** Định nghĩa mẫu số từng metric; bảng tính tay và kết quả code khớp, quy định lớp vắng.
- **Nghiệm thu/lưu ý:** Người 1 kiểm abstain tạo FN lớp thật; chỉ GT void bị loại, không loại pseudo ignore khỏi full metric.

### 2D — Chẩn đoán baseline

**Người 2** · Review: Người 1 · Hạn: 25/10/2026

- **Mục tiêu:** Biết baseline sai ở đâu trước khi cải tiến.
- **Cần trước:** B0/B1/B2 và evaluator đã pass.
- **Bước làm:** 1. Chấm cùng dev. 2. Chọn gallery cố định 30–50 ảnh. 3. Ghi lỗi CAM, prompt, candidate, selection và fusion; tổng hợp cost.
- **Nơi lưu:** data/lists/qa_ids.txt; results/baselines/summary.csv; docs/baseline_diagnosis.md.
- **Đầu ra phải có:** Bảng metric/cost có run_id; gallery ảnh, CAM, điểm, mask và GT; ví dụ nhiều đối tượng/nhỏ/lấn nền.
- **Nghiệm thu/lưu ý:** Người 1 đối chiếu 5 ca; GT chỉ dùng phân tích, không đưa ngược vào generator.

## Tuần 3 — 26/10–01/11/2026

Mục tiêu: P và S hoạt động độc lập.

### 3A — Prompt theo vùng P

**Người 1** · Review: Người 2 · Hạn: 29/10/2026

- **Mục tiêu:** Phân bổ prompt đến nhiều vùng kích hoạt khác nhau.
- **Cần trước:** B2 và CAM cố định.
- **Bước làm:** 1. Threshold từng CAM, tìm vùng liên thông. 2. Xếp hạng, chọn tối đa R vùng theo budget. 3. Lấy một điểm dương/vùng và vẽ overlay.
- **Nơi lưu:** src/region_prompts.py; configs/P.yaml; results/P_dev/prompts/.
- **Đầu ra phải có:** Mỗi điểm có class_id, region_id, xy; config ghi threshold/R/budget và cách xử lý vùng rỗng.
- **Nghiệm thu/lưu ý:** Người 2 kiểm điểm trong vùng; vùng CAM không đồng nghĩa instance thật, chưa gom điểm nhiều vùng vào một prompt.

### 3B — P và đối chứng B2

**Người 1** · Review: Người 2 · Hạn: 01/11/2026

- **Mục tiêu:** So P với B2 công bằng và bàn giao cache cho S.
- **Cần trước:** P hoạt động và schema cache chốt.
- **Bước làm:** 1. Chạy cùng ảnh/cùng budget tối đa. 2. Ghi số điểm, bộ prompt và calls thực tế. 3. Lưu tất cả candidates, không chỉ mask đã chọn.
- **Nơi lưu:** cache/<cache_id>/B2/, P/; results/<run_id>/cost.csv, manifest.json.
- **Đầu ra phải có:** Mask/score khớp index; source/config hash và số ảnh; bảng budget từng ảnh, thời gian encoding/decoding.
- **Nghiệm thu/lưu ý:** Người 2 thử đọc cache mà không chạy SAM; nếu số calls lệch, báo rõ hoặc bổ sung đối chứng matched.

### 3C — Selector S

**Người 2** · Review: Người 1 · Hạn: 29/10/2026

- **Mục tiêu:** Chọn mask phù hợp lớp hơn chỉ nhìn qSAM.
- **Cần trước:** Cache B2 và CAM từ Người 1.
- **Bước làm:** 1. Tính seed coverage trong vùng tạo prompt. 2. Tính phần lấn seed mạnh lớp cạnh tranh. 3. Kết hợp score và điều kiện từ chối mask.
- **Nơi lưu:** src/mask_selector.py; configs/S.yaml; tests/test_selector.py.
- **Đầu ra phải có:** Mỗi candidate ghi qSAM/coverage/leakage/score; selected_index hoặc rejected; tham số không âm.
- **Nghiệm thu/lưu ý:** Người 1 kiểm code không đọc GT; miền hợp lệ từ ảnh/padding, quy định khi seed rỗng.

### 3D — Ablation S

**Người 2** · Review: Người 1 · Hạn: 01/11/2026

- **Mục tiêu:** Đo riêng hiệu quả từng thành phần của S.
- **Cần trước:** 3C và một cache B2 cố định.
- **Bước làm:** 1. Chạy S0=qSAM, S1 thêm coverage, S2 thêm leakage. 2. Chấm cùng dev. 3. Xem mask phình, lấn nền và trường hợp reject.
- **Nơi lưu:** results/S_ablation/summary.csv, selections.csv, figures/.
- **Đầu ra phải có:** Cùng candidates/fusion; bảng metric và tỷ lệ reject; ảnh ca selector thắng và thua.
- **Nghiệm thu/lưu ý:** Người 1 đối chiếu selected_index với ảnh; seed coverage cao không bảo đảm mask đúng toàn bộ đối tượng.

## Tuần 4 — 02–08/11/2026

Mục tiêu: Chọn cấu hình và khóa phương pháp.

### 4A — Tích hợp P và S

**Người 1** · Review: Người 2 · Hạn: 05/11/2026

- **Mục tiêu:** P và S phối hợp, tạo semantic mask hợp lệ.
- **Cần trước:** P, S và fusion đã chốt.
- **Bước làm:** 1. Nối P → SAM → S → fusion. 2. Test mask cùng lớp/hai lớp tranh chấp/vùng rỗng. 3. Đọc lại PNG và kiểm size/ID.
- **Nơi lưu:** src/generate_pseudo.py; configs/PS.yaml; tests/test_fusion.py.
- **Đầu ra phải có:** PNG uint8 một kênh; chỉ 0–20/255; logs mask nhận/reject và lý do; ảnh gốc giữ đúng tọa độ.
- **Nghiệm thu/lưu ý:** Người 2 kiểm không mất ảnh; không vừa đổi selector vừa thêm score fusion mới trong cùng ablation.

### 4B — Chốt generator

**Người 1** · Review: Người 2 · Hạn: 08/11/2026

- **Mục tiêu:** Generator khóa được để train và tái lập.
- **Cần trước:** Kết quả dev và quyết định 4D.
- **Bước làm:** 1. Sửa lỗi kỹ thuật đã xác nhận. 2. Đóng băng code, model và ngưỡng. 3. Ghi lệnh chạy, chạy lại một batch và so output.
- **Nơi lưu:** configs/final.yaml; docs/generator_freeze.md; results/freeze_check/.
- **Đầu ra phải có:** Commit/hash, class map, split hash; lệnh chạy đầy đủ; manifest xác nhận batch lặp lại.
- **Nghiệm thu/lưu ý:** Người 2 ký review; sau freeze không chỉnh theo val và không thêm zoom/loss mới vào lõi.

### 4C — Ablation P và S

**Người 2** · Review: Người 1 · Hạn: 05/11/2026

- **Mục tiêu:** Có bằng chứng đóng góp P, S và tương tác.
- **Cần trước:** Tất cả pseudo dev và metric đúng.
- **Bước làm:** 1. Tổng hợp B0/B1/B2/P/S/P+S. 2. Thử vài threshold P và trọng số S trên dev. 3. Xuất bảng metric/cost từ file gốc.
- **Nơi lưu:** results/ablation/summary.csv; results/sensitivity/; docs/experiments.csv.
- **Đầu ra phải có:** Mỗi dòng có run/config, mIoU, precision, coverage, ignore và cost; không thiếu ca chạy lỗi.
- **Nghiệm thu/lưu ý:** Người 1 kiểm budget và config; tránh thử mọi tổ hợp để săn số đẹp.

### 4D — Chọn trên dev

**Người 2** · Review: Người 1 · Hạn: 08/11/2026

- **Mục tiêu:** Chọn phương pháp cuối dựa trên dev, không dựa val.
- **Cần trước:** 4C và giới hạn GPU.
- **Bước làm:** 1. So gain với B2, độ phủ và chi phí. 2. Xem ca thất bại. 3. Chọn method, ghi lý do và danh sách run train.
- **Nơi lưu:** docs/decisions.md; configs/final.yaml; docs/training_budget.csv.
- **Đầu ra phải có:** Tên cấu hình cụ thể; số liệu dev hỗ trợ; kế hoạch B0/B2/method và seed; hai người xác nhận.
- **Nghiệm thu/lưu ý:** Người 1 kiểm lựa chọn nhất quán; được chọn P hoặc S nếu tốt hơn P+S, không ép kết quả.

## Tuần 5 — 09–15/11/2026

Mục tiêu: Sinh nhãn giả và train mô hình cuối.

### 5A — Full pseudo

**Người 1** · Review: Người 2 · Hạn: 11/11/2026

- **Mục tiêu:** Có target nhãn giả đầy đủ cho train-fit.
- **Cần trước:** Frozen generator và train-fit list.
- **Bước làm:** 1. Sinh B0/B2/method. 2. Lưu PNG raw và manifest từng ảnh. 3. Thử đọc bằng training loader, bàn giao QA.
- **Nơi lưu:** artifacts/pseudo/<method>/<config_hash>/train_fit/; results/<run_id>/manifest.csv.
- **Đầu ra phải có:** Một PNG chỉ số/ảnh, size gốc; config/checkpoint/split hashes; failure_count và ignore ratio.
- **Nghiệm thu/lưu ý:** Người 2 kiểm đủ ID; không dùng overlay màu làm nhãn và không tự loại ảnh lỗi khỏi list.

### 5B — Training seed 0

**Người 1** · Review: Người 2 · Hạn: 15/11/2026

- **Mục tiêu:** So chất lượng segmenter khi chỉ thay nguồn pseudo.
- **Cần trước:** 5A được Người 2 nghiệm thu.
- **Bước làm:** 1. Khóa train config chung. 2. Train seed 0 B0/B2/method. 3. Lưu logs/resume và checkpoint cuối theo quy tắc đã chốt.
- **Nơi lưu:** configs/train.yaml; results/train_<method>_s0/; checkpoints/<run_id>/.
- **Đầu ra phải có:** Loss curve, LR, steps, seed, dataset hash; best/last có tiêu chí chọn; checkpoint tải lại được.
- **Nghiệm thu/lưu ý:** Người 2 kiểm cùng pretrained/steps/augmentation; mask resize nearest, flip/crop đồng bộ, ignore 255 bỏ loss.

### 5C — QA pseudo toàn tập

**Người 2** · Review: Người 1 · Hạn: 11/11/2026

- **Mục tiêu:** Ngăn lỗi nhãn giả làm hỏng training.
- **Cần trước:** Pseudo từ 5A.
- **Bước làm:** 1. Quét file tồn tại/size/ID và failure. 2. Tổng hợp coverage/ignore theo ảnh/lớp. 3. Kiểm gallery và mẫu loader.
- **Nơi lưu:** results/pseudo_qa/<method>/qa.csv, report.md; docs/issues.md.
- **Đầu ra phải có:** Số ảnh khớp train-fit; danh sách lỗi và người sửa; mẫu overlay/target đọc lại; kết luận pass/fail.
- **Nghiệm thu/lưu ý:** Người 1 sửa lỗi rồi Người 2 recheck; không bỏ ảnh khó để làm số đẹp.

### 5D — Chuẩn bị đánh giá cuối

**Người 2** · Review: Người 1 · Hạn: 15/11/2026

- **Mục tiêu:** Evaluator cuối sẵn sàng trước khi mở val.
- **Cần trước:** Metric đã test và config đã freeze.
- **Bước làm:** 1. Kiểm inference chỉ nhận ảnh. 2. Test batch cuối, resize và PNG. 3. Khóa val list, metric và mẫu bảng kết quả.
- **Nơi lưu:** src/evaluate_final.py; configs/eval.yaml; results/final_eval_checks/.
- **Đầu ra phải có:** Script trả confusion/per-class/mIoU; đủ ảnh; tên checkpoint, metric version và class map.
- **Nghiệm thu/lưu ý:** Người 1 kiểm không dùng GT tag lọc lớp hoặc chọn checkpoint theo val liên tục.

## Tuần 6 — 16–22/11/2026

Mục tiêu: Có kết quả cuối và chi phí.

### 6A — Seed và inference

**Người 1** · Review: Người 2 · Hạn: 20/11/2026

- **Mục tiêu:** Có dự đoán cuối và kiểm độ biến thiên nếu đủ GPU.
- **Cần trước:** Train seed 0 xong, eval đã khóa.
- **Bước làm:** 1. Infer B0/B2/method. 2. Nếu đủ budget, train thêm seed 1/2 cho B2 và method. 3. Lưu raw predictions và manifests.
- **Nơi lưu:** artifacts/predictions/<run_id>/val/; checkpoints/<run_id>/; results/<run_id>/.
- **Đầu ra phải có:** Đủ 1449 ảnh hoặc giải trình lỗi; mask size gốc 0–20; log seed/checkpoint/time, không hậu xử lý GT.
- **Nghiệm thu/lưu ý:** Người 2 kiểm resize logits rồi argmax; không báo 3-seed nếu còn run chưa hoàn thành.

### 6B — Cost và demo

**Người 1** · Review: Người 2 · Hạn: 22/11/2026

- **Mục tiêu:** Đo chi phí thật và demo được ảnh mới.
- **Cần trước:** Các checkpoint cuối và pipeline frozen.
- **Bước làm:** 1. Profile CAM/encoding/decoding/selection/fusion. 2. Demo segmenter chỉ nhận ảnh. 3. Backup trọng số, quay video.
- **Nơi lưu:** results/profiling/profile.csv; demo/; artifacts/demo/video.mp4; docs/artifacts.csv.
- **Đầu ra phải có:** Hardware, warm-up, calls, time, peak VRAM; ảnh demo và prediction; link/hash checkpoint bền vững.
- **Nghiệm thu/lưu ý:** Người 2 chạy demo; khi đo GPU có sync, tách cache-hit/miss và thời gian segmenter khỏi pseudo pipeline.

### 6C — Chấm kết quả cuối

**Người 2** · Review: Người 1 · Hạn: 20/11/2026

- **Mục tiêu:** Bảng kết quả cuối có thể kiểm chứng.
- **Cần trước:** Raw predictions từ 6A.
- **Bước làm:** 1. Chấm full val bằng evaluator khóa. 2. Xuất mIoU/per-class. 3. Tính mean/std trên seed hoàn thành nếu có.
- **Nơi lưu:** results/final/metrics.csv, per_class.csv, seed_summary.csv.
- **Đầu ra phải có:** Từng dòng có run/seed/checkpoint/split hash; số seed thực tế; metric giữ đủ precision trước làm tròn.
- **Nghiệm thu/lưu ý:** Người 1 đối chiếu CSV và confusion; một seed chỉ báo kết quả một lần, không kết luận ổn định.

### 6D — Phân tích kết quả

**Người 2** · Review: Người 1 · Hạn: 22/11/2026

- **Mục tiêu:** Giải thích method cải thiện hoặc thất bại ở đâu.
- **Cần trước:** Bảng cuối, gallery và instance GT nếu có.
- **Bước làm:** 1. So ca thắng/thua trên danh sách cố định. 2. Đo coverage đúng lớp theo instance. 3. Viết hạn chế, cost và kết quả âm.
- **Nơi lưu:** results/analysis/figures/, instance_coverage.csv; docs/discussion.md.
- **Đầu ra phải có:** Ảnh kèm ID/config; ca bỏ sót/lấn nền/nhiều đối tượng; ghi định nghĩa nhóm size và subset có instance GT.
- **Nghiệm thu/lưu ý:** Người 1 kiểm kết luận có evidence; không coi coverage là instance AP hoặc tạo instance GT từ semantic components.

## Tuần 7 — 23–29/11/2026

Mục tiêu: Báo cáo nháp và demo hoàn chỉnh.

### 7A — Viết phương pháp

**Người 1** · Review: Người 2 · Hạn: 26/11/2026

- **Mục tiêu:** Người đọc hiểu và triển khai lại phương pháp.
- **Cần trước:** Code freeze và configs thực tế.
- **Bước làm:** 1. Vẽ hai giai đoạn pipeline. 2. Mô tả P, S, fusion/background/ignore. 3. Ghi pretrained, tham số và training.
- **Nơi lưu:** docs/report/method.docx; docs/figures/pipeline.svg; docs/report/implementation.md.
- **Đầu ra phải có:** Mô tả khớp code; input/output rõ; công thức S có định nghĩa miền và seed cục bộ.
- **Nghiệm thu/lưu ý:** Người 2 đọc đối chiếu config; không gọi CAM chuẩn hóa là xác suất pixel hoặc SAM tự phân loại.

### 7B — README và demo

**Người 1** · Review: Người 2 · Hạn: 29/11/2026

- **Mục tiêu:** Người khác chạy được và có minh họa thuyết trình.
- **Cần trước:** Checkpoint và artifact đã backup.
- **Bước làm:** 1. Viết lệnh setup/cache/generate/train/eval/demo. 2. Ghi paths và yêu cầu tài nguyên. 3. Làm slide phương pháp/video dự phòng.
- **Nơi lưu:** README.md; demo/; docs/slides/method.pptx; docs/artifacts.csv.
- **Đầu ra phải có:** Lệnh thật, ví dụ config, dependencies; links/hash; ảnh mới inference chỉ cần RGB; demo chạy được.
- **Nghiệm thu/lưu ý:** Người 2 chạy README trong phiên sạch; không hardcode đường dẫn cá nhân hoặc yêu cầu click prompt tay.

### 7C — Viết setup và results

**Người 2** · Review: Người 1 · Hạn: 26/11/2026

- **Mục tiêu:** Báo cáo số liệu đúng giao thức và dễ đọc.
- **Cần trước:** CSV gốc và logs đã đối chiếu.
- **Bước làm:** 1. Viết setup/split/pretrained/metric. 2. Sinh bảng/hình từ CSV. 3. Viết kết quả ablation, cuối và chi phí.
- **Nơi lưu:** docs/report/setup_results.docx; docs/figures/; results/final/.
- **Đầu ra phải có:** Caption có run/giao thức; nêu GT dev; bảng không bịa ô trống; ghi số seed và các giới hạn.
- **Nghiệm thu/lưu ý:** Người 1 kiểm ít nhất 10 số; không so SOTA khác split/backbone/pretrained mà không giải thích.

### 7D — Ghép báo cáo

**Người 2** · Review: Người 1 · Hạn: 29/11/2026

- **Mục tiêu:** Có báo cáo hoàn chỉnh để review tuần cuối.
- **Cần trước:** 7A và 7C bàn giao.
- **Bước làm:** 1. Viết intro/related work và trích dẫn. 2. Ghép method/results/discussion. 3. Làm slide kết quả và liệt kê việc còn thiếu.
- **Nơi lưu:** docs/report/report_v1.docx; docs/references.bib; docs/slides/results.pptx; docs/issues.md.
- **Đầu ra phải có:** Đủ các phần, hình/bảng có nguồn; danh sách issue; phân biệt đóng góp dự kiến và đã chứng minh.
- **Nghiệm thu/lưu ý:** Người 1 review phương pháp; không nhận việc ghép CAM+SAM là hoàn toàn mới.

## Tuần 8 — 30/11–06/12/2026

Mục tiêu: Kiểm tra tái lập và đóng gói nộp.

### 8A — Sửa lỗi và đóng gói code

**Người 1** · Review: Người 2 · Hạn: 03/12/2026

- **Mục tiêu:** Code nộp chạy được, đủ nguồn để tái lập.
- **Cần trước:** Issue tuần 7 và reproduction feedback.
- **Bước làm:** 1. Sửa bug đã xác nhận. 2. Loại cache tạm khỏi zip, giữ config/list/hash. 3. Giải nén và chạy smoke.
- **Nơi lưu:** deliverables/code.zip; docs/release_notes.md; docs/artifacts.csv.
- **Đầu ra phải có:** Code sạch, commit/tag, env và lệnh; checkpoint/pseudo lớn dùng link bền vững có hash.
- **Nghiệm thu/lưu ý:** Người 2 thử zip; không thêm module mới hoặc mất file ignored quan trọng khi đóng gói.

### 8B — Tập demo và review số

**Người 1** · Review: Người 2 · Hạn: 06/12/2026

- **Mục tiêu:** Demo trơn tru và số trong slide khớp báo cáo.
- **Cần trước:** Code package, report draft, kết quả cuối.
- **Bước làm:** 1. Tập trình bày input/output/P/S. 2. Demo và chuẩn bị video khi GPU lỗi. 3. Đối chiếu số bảng với Người 2.
- **Nơi lưu:** deliverables/demo.mp4; deliverables/slides.pptx; docs/review/number_audit.csv.
- **Đầu ra phải có:** Slide cùng version report; demo ảnh mới; audit số có file nguồn, không còn mismatch.
- **Nghiệm thu/lưu ý:** Người 2 kiểm và tập câu hỏi; không dùng ảnh đã tuning rồi gọi là ảnh kiểm thử độc lập.

### 8C — Tái lập và kiểm báo cáo

**Người 2** · Review: Người 1 · Hạn: 03/12/2026

- **Mục tiêu:** Kiểm một người khác thực sự chạy lại được.
- **Cần trước:** README và code zip từ Người 1.
- **Bước làm:** 1. Chạy từ phiên sạch theo README. 2. Log lệnh/lỗi, gửi Người 1 sửa. 3. Kiểm report Word/PDF, hình và trích dẫn.
- **Nơi lưu:** docs/review/reproduction.md; deliverables/report.docx, report.pdf.
- **Đầu ra phải có:** Một smoke run/eval tái lập; report mở được, không placeholder, bảng rõ và tiếng Việt đúng.
- **Nghiệm thu/lưu ý:** Người 1 ký review; không sửa kết quả để khớp claim nếu số thực nghiệm khác.

### 8D — Bộ nộp và thuyết trình

**Người 2** · Review: Người 1 · Hạn: 06/12/2026

- **Mục tiêu:** Gói nộp đầy đủ và hai người trình bày được.
- **Cần trước:** 8A–8C được nghiệm thu.
- **Bước làm:** 1. Gom report/slides/code/results và links. 2. Kiểm zip/file mở được, tập phần Results. 3. Nộp theo lịch môn, tải lại và lưu receipt.
- **Nơi lưu:** deliverables/; deliverables/submission_manifest.csv; docs/review/submission_receipt/.
- **Đầu ra phải có:** Checklist hai người xác nhận; filenames/version/hash; link tải hoạt động; receipt khi đã nộp.
- **Nghiệm thu/lưu ý:** Người 1 kiểm bộ nộp; không ghi đã nộp khi mới tạo zip, không để file duy nhất trên GPU session.
