# Quy trình làm việc của hai người

## Mỗi task một branch và một PR

1. Nhận task trong `docs/tasks.csv`, tạo GitHub Issue bằng mẫu **Task**. Điền ID, người làm, reviewer, mục tiêu và đầu ra. Issue giao cho người làm khi đã được mời vào repo.
2. Lấy code mới trước khi bắt đầu:

```powershell
git switch main
git pull --ff-only
git switch -c feat/3a-region-prompts
```

3. Code, chạy kiểm tra liên quan, lưu run lớn bên ngoài Git. Commit theo mốc nhỏ:

```powershell
git add src configs tests docs
git commit -m "feat: add region-aware prompt generator for task 3A"
git push -u origin feat/3a-region-prompts
```

4. Mở Pull Request vào `main`, điền mẫu, liên kết `Closes #<issue>`, config/run và ảnh QA. Yêu cầu người còn lại review. Không tạo task Xong khi mới chạy xong log.
5. Reviewer kiểm code, class/geometry, command và artifact; chạy mẫu nếu cần. Sửa các lỗi quan trọng, chờ CI pass, rồi squash merge. Đóng task và ghi artifact/review vào CSV.

## Phân chia file để tránh conflict

- Người 1: CAM/SAM/prompts/fusion/segmenter, training/demo.
- Người 2: data/metadata/lists, metric, selector S, analysis/report.
- Selector interface, class map, fusion và configs chung: thỏa thuận trước qua Issue, không sửa song song tùy ý.
- Nếu cùng sửa CSV hoặc Word: thống nhất một owner ghép cuối, người kia review. Markdown/code dễ merge hơn file Word.
- Branch ngắn theo task; không push thẳng vào main sau khi nhóm bắt đầu cộng tác. Không force-push branch của người khác.

## Mốc tuần

Đầu tuần nhận task và GPU quota; giữa tuần giao data/cache; cuối tuần review khoảng 30 phút. Blocked phải có lý do, người hỗ trợ và hạn mới. `docs/task_plan.md` là mô tả chi tiết, `docs/tasks.csv` là trạng thái thực tế.

## Khi có conflict

Pull main vào branch, mở từng file, hiểu thay đổi hai bên và giữ đúng interface; chạy lại checks. Không chọn toàn bộ ours/theirs chỉ để bỏ conflict. Thông báo người đang sửa file liên quan.

## GitHub settings đề xuất

Chủ repo mời đúng username người còn lại. Nếu gói GitHub hỗ trợ, đặt rule cho main: PR trước merge, 1 approval của người còn lại và CI `scaffold` pass. Các rule chưa được thiết lập tự động trong bộ khung này.
