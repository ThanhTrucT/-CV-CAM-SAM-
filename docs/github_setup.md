# Đưa repo lên GitHub

Bộ khung local đã sẵn sàng; không đồng nghĩa repo GitHub đã được tạo.

1. Đăng nhập tài khoản chủ repo, tạo repo `cam-sam-wsss` (mặc định đề xuất Private). Không thêm README/license/.gitignore online vì local đã có.
2. Sau khi repo online tồn tại, mở terminal trong thư mục local và chạy, thay OWNER bằng username thật:

```powershell
git remote add origin https://github.com/OWNER/cam-sam-wsss.git
git push -u origin main
```

Nếu origin đã có, kiểm `git remote -v` trước; không ghi đè remote không đúng. Nếu yêu cầu đăng nhập, dùng browser/Git Credential Manager; không dán token vào chat hay repo.

3. Settings → Collaborators: chủ repo mời đúng username người thứ hai. Người đó chấp nhận, clone repo và điền `docs/team.md` qua PR.
4. Thiết lập bảo vệ main nếu gói GitHub cho phép; yêu cầu PR, 1 review và scaffold checks. Các thao tác quyền truy cập cần xác nhận đúng người nhận.
5. Chọn task trong `docs/task_plan.md`; tạo Issue từ mẫu, branch theo task và review chéo.

Initial commit do bộ khung tự động tạo với tác giả kỹ thuật `Project scaffold`; mỗi thành viên cấu hình tên/email Git của mình cho các commit tiếp theo.
