# Chess Game Result Prediction

Dự đoán kết quả ván cờ Rapid (Win / Draw / Loss) của người chơi thien3703 trên
[chess.com](https://www.chess.com), dựa trên dữ liệu ván đấu lấy qua Public API.

## Cấu trúc thư mục

```
chess data/
├── config.py                  # Cấu hình: USERNAME, headers, đường dẫn dữ liệu
├── get_rapid_games.py         # ① Cào toàn bộ game Rapid từ chess.com API -> data/raw
├── preprocess.py              # ② Các hàm tiền xử lý (tái sử dụng được)
├── 01_preprocessing.ipynb     # ③ Notebook: raw -> áp preprocess.py -> data/processed
├── 02_eda_and_features.ipynb  # ④ Notebook: EDA + Feature Engineering
├── requirements.txt
└── data/
    ├── raw/                   # Dữ liệu thô từ API
    └── processed/             # Dữ liệu đã tiền xử lý
```

## Pipeline

1. **Cào dữ liệu** — `get_rapid_games.py` gọi chess.com Public API (không cần API key),
   lọc các ván `time_class == "rapid"` và lưu ra `data/raw/<username>_rapid_games.csv`.
2. **Tiền xử lý** — `01_preprocessing.ipynb` dùng các hàm trong `preprocess.py` để
   parse thời gian, trích đặc trưng khai cuộc/nước đi từ PGN, gom đặc trưng theo góc nhìn
   người chơi, rồi lưu ra `data/processed/<username>_rapid_games_processed_1.csv`.
3. **EDA + Feature Engineering** — `02_eda_and_features.ipynb` khám phá dữ liệu và tạo
   thêm đặc trưng (thời lượng ván, nhóm ECO, khung giờ, chênh lệch rating, lịch sử thi đấu...).

## Cách chạy

```bash
# 1. Cài môi trường
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 2. Cấu hình: đổi USERNAME trong config.py sang tài khoản cần phân tích

# 3. Cào dữ liệu
python get_rapid_games.py

# 4. Mở lần lượt các notebook (chạy từ thư mục gốc của project)
#    01_preprocessing.ipynb  ->  02_eda_and_features.ipynb
```

> Lưu ý: chạy notebook với thư mục làm việc là gốc project để `from config import ...`
> và các đường dẫn `data/...` hoạt động đúng.

## Cấu hình (`config.py`)

| Biến                  | Ý nghĩa                                     |
| --------------------- | ------------------------------------------- |
| `USERNAME`            | Tài khoản chess.com cần phân tích           |
| `HEADERS`             | HTTP headers khi gọi API                    |
| `BASE_URL`            | Endpoint Public API của chess.com           |
| `RAW_DATA_PATH`       | Đường dẫn file dữ liệu thô                   |
| `PROCESSED_DATA_PATH` | Đường dẫn file dữ liệu đã tiền xử lý         |
