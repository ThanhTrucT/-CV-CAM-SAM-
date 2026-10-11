# CAM + SAM cho phân đoạn ngữ nghĩa giám sát yếu

Repo làm việc chung cho 2 người trong 8 tuần. Đây là bộ khung tổ chức dự án; **pipeline ML chưa được triển khai và chưa có kết quả thực nghiệm**.

Hướng chốt: ExCEL training-free/SVC → prompt theo vùng P → SAM ViT-B frozen → chọn mask S → fusion → nhãn giả offline → SegFormer-B0. Suy luận ảnh mới chỉ chạy segmenter. VOC2012/SBD là dữ liệu chính; COCO và crop/zoom là mở rộng.

## Bắt đầu

1. Cả hai clone repo và đọc [quy trình cộng tác](CONTRIBUTING.md).
2. Điền tên/GitHub username trong [phân công](docs/team.md).
3. Mở [32 task](docs/task_plan.md), nhận task qua Issue template và tạo branch.
4. Chạy kiểm tra cấu trúc bằng Python 3.10 trở lên:

```powershell
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

5. Người 1 thiết lập môi trường Torch/CUDA theo GPU ở tuần 1; ghi version thực tế vào `docs/environment.md` và tạo file dependency lock. Các kiểm tra scaffold hiện chỉ cần thư viện chuẩn Python, không cần GPU.
6. Người 2 chuẩn bị data/split/tag và giữ val để đánh giá cuối. Đọc [quy tắc dữ liệu](docs/data_protocol.md).

## Cấu trúc

```text
src/          cam/ prompts/ sam/ selection/ fusion/ segmentation/
configs/      cấu hình JSON theo phương pháp, train và eval
tests/        kiểm tra có ý nghĩa theo từng module
scripts/      tạo run và kiểm tra hợp đồng repo
data/raw/     ảnh/annotation gốc, không commit
data/lists/   train-fit/dev/val/QA ID, chỉ commit sau xác minh
data/metadata/ class map, image tags, inventory
cache/        CAM/candidates, không commit
results/      từng run độc lập, không commit
artifacts/    pseudo/prediction/demo lớn, không commit
checkpoints/  trọng số lớn, không commit
docs/         task, experiment, quyết định, báo cáo và review
demo/         code inference ảnh mới
deliverables/ gói nộp cuối, không commit
```

Git giữ code, config, list/hash, metadata nhỏ, docs và bảng tóm tắt. Dữ liệu/model/cache lớn đặt ở ổ dùng chung hoặc Drive nhóm; lưu link và SHA-256 trong `docs/artifacts.csv`. Không đưa ảnh cá nhân, mật khẩu, token hoặc file `.env` lên Git.

## Tạo một run

```powershell
python scripts/new_run.py E001_B2_dev_s0 --method B2 --owner "Nguoi 1" --split dev --seed 0
```

Lệnh này chỉ tạo `results/E001_B2_dev_s0/` với config copy, manifest và các mẫu log/metric. **Không chạy CAM/SAM hay train.** Điền các trường provenance còn thiếu trước khi chạy. Không ghi đè run cũ.

## Thí nghiệm

B0 CAM-only; B1 một cực đại/lớp; B2 top-K local maxima; P prompt vùng; S selector có xét lớp; PS kết hợp. P so với B2 cùng budget; S so cùng cache candidates. Train B0/B2/cấu hình chọn trên dev, không mặc định PS luôn thắng. Chi tiết: [experiment protocol](docs/experiment_protocol.md).

## Nguồn upstream

- ExCEL: https://github.com/zwyang6/ExCEL
- SAM: https://github.com/facebookresearch/segment-anything

Không chép upstream code/weights vào repo này trước khi kiểm tra giấy phép và pin commit. Nhóm chưa chọn giấy phép phát hành; quyền truy cập repo do chủ repo quản lý.
