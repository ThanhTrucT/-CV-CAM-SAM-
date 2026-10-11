# Giao thức dữ liệu

- Giữ raw data nguyên bản và ghi nguồn/phiên bản vào inventory. Kiểm train_aug VOC/SBD, số ảnh, size và ID.
- Nếu train_aug xác minh được, giữ dev khoảng 300–500 ảnh; train-fit loại dev. Nếu chỉ VOC train gốc, chọn dev nhỏ hơn và công bố.
- Val VOC chính thức 1449 ảnh giữ cuối. Hash các list, seed và kiểm không trùng ID. File list chưa tồn tại nghĩa là chưa có split; không tự coi metadata là đã hoàn thành.
- Image tags dùng nhãn mức ảnh từ XML/nguồn đã xác minh; không lấy box/GT vị trí để prompt. Nếu tạo tags từ tập lớp có trong annotation, phải ghi rõ provenance và chỉ dùng thông tin hiện diện lớp.
- CAM channel 0–19 → semantic ID 1–20; background 0, ignore 255. Cow channel 9 → ID 10. Xác minh order thực tế upstream trước mapping.
- GT dev dùng đánh giá/tuning phải công bố. GT mask/point/box/void không vào generator; miền ảnh hợp lệ từ ảnh/padding.
- Full pseudo metric: GT void bỏ qua; pseudo ignore trên GT hợp lệ là abstain/FN lớp thật. Báo assigned precision, coverage và ignore riêng.
- Không loại ảnh khó khỏi evaluator; lỗi dữ liệu ghi rõ và sửa. Không dùng val để đổi ngưỡng.
