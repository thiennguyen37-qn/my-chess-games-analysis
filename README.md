# Chess Game Result Prediction

Dự đoán kết quả ván cờ Rapid (**Win / Not-Win**) của người chơi thien3703 trên
[chess.com](https://www.chess.com), dựa trên dữ liệu ván đấu lấy qua Public API.

> Bài toán phân loại nhị phân: `Win = 1`, `Not-Win (Draw + Loss) = 0`.

## Cấu trúc thư mục

```
chess data/
├── config.py                       # Cấu hình: USERNAME, headers, đường dẫn dữ liệu
├── get_rapid_games.py              # ① Cào game Rapid từ chess.com API -> data/raw
├── preprocess.py                   # ② Các hàm tiền xử lý (tái sử dụng được)
├── 01_preprocessing_raw_data.ipynb # ③ raw -> áp preprocess.py -> data/processed
├── 02_feature_engineering.ipynb    # ④ Tạo đặc trưng -> data/processed
├── 03_EDA.ipynb                    # ⑤ EDA + kiểm định giả thuyết + chọn feature
├── 04_model_training.ipynb         # ⑥ So sánh model + train + SHAP
├── requirements.txt
└── data/
    ├── raw/                        # Dữ liệu thô từ API
    └── processed/                  # Dữ liệu đã tiền xử lý / sẵn sàng train
```

## Pipeline

1. **Cào dữ liệu** — `get_rapid_games.py` gọi chess.com Public API (không cần API key),
   lọc các ván `time_class == "rapid"` và lưu ra `data/raw/<username>_rapid_games.csv`.
2. **Tiền xử lý** — `01_preprocessing_raw_data.ipynb` dùng các hàm trong `preprocess.py`
   để parse thời gian, trích đặc trưng khai cuộc/nước đi từ PGN, gom đặc trưng theo góc
   nhìn người chơi, rồi lưu ra `data/processed/<username>_rapid_games_processed_1.csv`.
3. **Feature Engineering** — `02_feature_engineering.ipynb` tạo thêm đặc trưng (thời lượng
   ván, nhóm ECO, khung giờ, chênh lệch rating, lịch sử thi đấu...) và lưu
   `data/processed/<username>_rapid_games_features.csv`.
4. **EDA + Feature Selection** — `03_EDA.ipynb` khám phá dữ liệu, kiểm định giả thuyết
   (Kruskal-Wallis / Chi-square) để chọn 6 feature có ý nghĩa thống kê, lưu
   `data/processed/<username>_train_ready.csv`.
5. **Huấn luyện & Đánh giá** — `04_model_training.ipynb` so sánh nhiều model
   (Logistic Regression, KNN, SVM, Random Forest, XGBoost, LightGBM) bằng cross-validation,
   vẽ confusion matrix, feature importance và SHAP summary cho model tốt nhất.

## Cách chạy

```bash
# 1. Cài môi trường
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 2. Cấu hình: đổi USERNAME trong config.py sang tài khoản cần phân tích

# 3. Cào dữ liệu
python get_rapid_games.py

# 4. Chạy lần lượt các notebook (từ thư mục gốc project)
#    01_preprocessing_raw_data -> 02_feature_engineering -> 03_EDA -> 04_model_training
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
| `FEATURE_DATA_PATH`   | Đường dẫn file dữ liệu sau feature engineering |
| `TRAIN_DATA_PATH`     | Đường dẫn file 6 feature đã chọn, sẵn sàng train |
