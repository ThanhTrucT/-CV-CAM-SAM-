# Giao thức thí nghiệm

| ID | Prompt | Chọn mask | Mục đích |
|---|---|---|---|
| B0 | Không SAM | CAM-only | Mốc nguồn CAM |
| B1 | Một cực đại mỗi lớp | qSAM | Tác động thêm SAM |
| B2 | Top-K local maxima và NMS | qSAM | Baseline chính |
| P | Vùng CAM, bộ prompt riêng | qSAM | So B2 cùng budget |
| S | Giữ prompt/candidates B2 | qSAM + seed − leakage | Đo selector |
| PS | Prompt vùng | Selector S | Đo kết hợp |

S0=qSAM; S1 thêm seed coverage cục bộ; S2 thêm phạt seed mạnh lớp cạnh tranh. Một điểm dương/vùng ở bản đầu. Các vùng khác nhau không tự gom thành một bộ prompt. SAM không tự phân loại; class lấy từ CAM tạo prompt.

Giữ CAM/SAM checkpoint, fusion/background/ignore và tập ảnh giữa run. Ghi số điểm, bộ prompt và calls thực tế. P/B2 cùng ngân sách; S dùng cùng candidates. qSAM/CAM không mặc định là xác suất đúng lớp.

Đánh giá mọi cấu hình pseudo trên dev: full mIoU, assigned precision, coverage, ignore, cost; gallery cố định. Coverage instance chỉ khi có instance GT thật. Train seed 0 B0/B2/method chọn trên dev; nếu đủ GPU, seed 1/2 B2 và method. Chỉ ghi kết quả có thật.

Chọn config/checkpoint theo giao thức trước khi chấm final val. Seed mean/std chỉ cho seed hoàn thành; encoder SegFormer-B0 ImageNet và head mới, cùng train schedule/augmentation. Crop mask nearest; inference resize logits rồi argmax.

Trong mỗi run lưu config/command/manifest/log/metric/cost và đường dẫn file lớn. `configs/*.json` hiện là khung chưa khóa; null yêu cầu chủ task chốt trên dev/pilot. Không thể chạy ML từ config này trước khi implement.
