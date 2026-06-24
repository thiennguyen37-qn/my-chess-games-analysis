USERNAME = "thien3703"

HEADERS = {
    "User-Agent": "research-script (contact: example@example.com)"
}

BASE_URL = "https://api.chess.com/pub/player"

RAW_DATA_DIR  = "data/raw"
RAW_DATA_PATH = f"{RAW_DATA_DIR}/{USERNAME}_rapid_games.csv"

PROCESSED_DATA_DIR  = "data/processed"
PROCESSED_DATA_PATH = f"{PROCESSED_DATA_DIR}/{USERNAME}_rapid_games_processed_1.csv"
FEATURE_DATA_PATH   = f"{PROCESSED_DATA_DIR}/{USERNAME}_rapid_games_features.csv"
TRAIN_DATA_PATH     = f"{PROCESSED_DATA_DIR}/{USERNAME}_train_ready.csv"
