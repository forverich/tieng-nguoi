# Tiếng khỉ — Tiếng người

Trắc nghiệm từ vựng đối chiếu hai cách dùng tiếng Việt: từ thường gặp sau 1975 ("tiếng khỉ") và từ tương ứng theo cách dùng cũ ("tiếng người").

Web app viết bằng **Flask**, single-file, không cần database.

## Tính năng

- 175 cặp từ vựng dạng trắc nghiệm 4 lựa chọn
- Đáp án sai được lấy ngẫu nhiên, lọc trùng đồng nghĩa với đáp án đúng
- Mỗi câu hỏi có thể có nhiều đáp án đúng (đều được chấp nhận và hiển thị sau khi trả lời)
- Theo dõi điểm số và tiến độ (không lặp câu cho đến khi hết)
- Phím tắt: `1` – `4` chọn đáp án, `Enter` / `Space` qua câu tiếp
- Giao diện kiểu báo giấy cổ (serif, paper texture, mực đỏ son)

## Cách chạy

Yêu cầu Python 3.9+.

```bash
pip install -r requirements.txt
python app.py
```

Mở trình duyệt tại `http://127.0.0.1:5000`.

## Cấu trúc

```
.
├── app.py            # toàn bộ backend + frontend (template inline)
├── requirements.txt
├── .gitignore
└── README.md
```

Dữ liệu từ vựng (`VOCAB`) nằm trực tiếp trong `app.py`. Mỗi mục là một tuple `(tiếng_khỉ, [danh_sách_đáp_án_tiếng_người_chấp_nhận])`.

## Tuỳ biến

- **Thêm từ vựng:** chỉ cần thêm tuple mới vào list `VOCAB`.
- **Đổi số đáp án:** sửa tham số `n` trong `pick_distractors(...)`.
- **Đổi theme:** chỉnh khối CSS `:root` ở đầu template `PAGE` (các biến `--paper`, `--ink`, `--accent`, ...).

## License

Mã nguồn: MIT.
Danh sách từ vựng được tổng hợp lại từ tài liệu lưu hành tự do trong cộng đồng người Việt; không thuộc bản quyền của repo này.
