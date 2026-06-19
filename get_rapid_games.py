"""
Lấy toàn bộ game Rapid của một user trên chess.com qua Public API (PubAPI).
Không cần API key, không cần đăng nhập.

Cách dùng:
    pip install requests
    python get_rapid_games.py

Kết quả: tạo file <username>_rapid_games.csv chứa toàn bộ game Rapid của user.
"""

import requests
import csv
import time

from config import USERNAME, HEADERS, BASE_URL, RAW_DATA_PATH


def get_archive_urls(username: str) -> list[str]:
    """Lấy danh sách URL các tháng có lưu game."""
    url = f"{BASE_URL}/{username}/games/archives"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()["archives"]


def get_games_from_archive(archive_url: str) -> list[dict]:
    """Lấy toàn bộ game trong 1 tháng."""
    resp = requests.get(archive_url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json().get("games", [])


def main():
    print(f"Đang lấy danh sách archive cho user '{USERNAME}'...")
    archive_urls = get_archive_urls(USERNAME)
    print(f"Tìm thấy {len(archive_urls)} tháng có dữ liệu.")

    rapid_games = []

    for i, archive_url in enumerate(archive_urls, start=1):
        print(f"  [{i}/{len(archive_urls)}] Đang tải {archive_url} ...")
        games = get_games_from_archive(archive_url)

        for g in games:
            # time_class có thể là: daily, rapid, blitz, bullet
            if g.get("time_class") == "rapid":
                white = g.get("white", {})
                black = g.get("black", {})
                accuracies = g.get("accuracies", {}) or {}

                rapid_games.append({
                    # --- Thông tin chung về game ---
                    "url": g.get("url"),
                    "uuid": g.get("uuid"),                    # ID duy nhất của trận
                    "start_time": g.get("start_time"),         # thường None với game live (rapid/blitz/bullet)
                    "end_time": g.get("end_time"),
                    "time_control": g.get("time_control"),
                    "time_class": g.get("time_class"),
                    "rated": g.get("rated"),
                    "rules": g.get("rules"),
                    "initial_setup": g.get("initial_setup"),
                    "eco": g.get("eco"),
                    "match": g.get("match"),                   # link team match (nếu có)
                    "tournament": g.get("tournament"),         # link tournament (nếu có)
                    "fen": g.get("fen"),                       # vị trí cuối game
                    "tcn": g.get("tcn"),                       # nước đi dạng nén TCN
                    "pgn": g.get("pgn"),                       # nước đi đầy đủ dạng PGN

                    # --- Độ chính xác (nếu đã được engine phân tích) ---
                    "white_accuracy": accuracies.get("white"),
                    "black_accuracy": accuracies.get("black"),

                    # --- Người chơi quân Trắng ---
                    "white_username": white.get("username"),
                    "white_rating": white.get("rating"),
                    "white_result": white.get("result"),
                    "white_uuid": white.get("uuid"),           # ID người chơi
                    "white_id": white.get("@id"),               # link profile

                    # --- Người chơi quân Đen ---
                    "black_username": black.get("username"),
                    "black_rating": black.get("rating"),
                    "black_result": black.get("result"),
                    "black_uuid": black.get("uuid"),
                    "black_id": black.get("@id"),
                })

        # Nghỉ nhẹ giữa các request để tránh bị rate limit
        time.sleep(0.3)

    print(f"\nTổng số game Rapid tìm được: {len(rapid_games)}")

    if rapid_games:
        out_file = RAW_DATA_PATH
        fieldnames = list(rapid_games[0].keys())
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rapid_games)
        print(f"Đã lưu kết quả vào: {out_file}")
    else:
        print("Không tìm thấy game Rapid nào cho user này.")


if __name__ == "__main__":
    main()
