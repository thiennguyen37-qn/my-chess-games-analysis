import re
import io
import numpy as np
import pandas as pd
import chess
import chess.pgn

from config import USERNAME

RESULT_MAP = {
    "win":                "Win",
    "agreed":             "Draw",
    "repetition":         "Draw",
    "stalemate":          "Draw",
    "insufficient":       "Draw",
    "50move":             "Draw",
    "timevsinsufficient": "Draw",
    "resigned":           "Loss",
    "checkmated":         "Loss",
    "timeout":            "Loss",
    "abandoned":          "Loss",
}

METHOD_MAP = {
    "resigned":           "Resign",
    "checkmated":         "Checkmate",
    "timeout":            "Timeout",
    "abandoned":          "Abandon",
    "agreed":             "Agreement",
    "repetition":         "Repetition",
    "stalemate":          "Stalemate",
    "insufficient":       "Insufficient Material",
    "50move":             "50-Move Rule",
    "timevsinsufficient": "Time vs Insufficient",
}


def process_end_time(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["end_time"] = pd.to_datetime(df["end_time"], unit="s")
    df = df.sort_values("end_time").reset_index(drop=True)
    return df


def extract_eco_code(pgn: str) -> str | None:
    m = re.search(r'\[ECO "([^"]+)"\]', str(pgn))
    return m.group(1) if m else None


def extract_opening_name(pgn: str) -> str | None:
    m = re.search(r'\[ECOUrl "https://www\.chess\.com/openings/([^"]+)"\]', str(pgn))
    return m.group(1).replace("-", " ") if m else None


def extract_opening_family(opening: str | None) -> str | None:
    if not opening:
        return None
    opening = re.split(r'\d+\.', opening)[0].strip()
    m = re.search(r'^(.*?\b(?:Opening|Defense|Defence|Game|Gambit|Attack|System))\b', opening)
    return m.group(1).strip() if m else opening


def count_moves(pgn: str) -> int | float:
    try:
        game = chess.pgn.read_game(io.StringIO(pgn))
        return game.end().ply()
    except Exception:
        return np.nan


def avg_time_per_move(pgn: str) -> float:
    clocks = re.findall(r'\[%clk (\d+):(\d+):(\d+\.?\d*)\]', pgn)
    times = [int(h) * 3600 + int(m) * 60 + float(s) for h, m, s in clocks]
    diffs = [times[i] - times[i + 2] for i in range(0, len(times) - 2, 2)]
    return np.mean(diffs) if diffs else np.nan


def add_rating_change(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rating_change"] = df["player_rating"].diff().fillna(0).astype(int)
    return df


def build_player_features(df: pd.DataFrame, player: str = USERNAME) -> pd.DataFrame:
    df = df.copy()
    is_white = df["white_username"] == player

    df["player_color"]    = np.where(is_white, "white", "black")
    df["player_rating"]   = np.where(is_white, df["white_rating"], df["black_rating"])
    df["opponent_rating"] = np.where(is_white, df["black_rating"], df["white_rating"])

    player_raw   = pd.Series(np.where(is_white, df["white_result"], df["black_result"]), index=df.index)
    opponent_raw = pd.Series(np.where(is_white, df["black_result"], df["white_result"]), index=df.index)

    df["player_result"]  = player_raw.map(RESULT_MAP).fillna("Loss")

    method_source        = pd.Series(np.where(player_raw == "win", opponent_raw, player_raw), index=df.index)
    df["result_method"]  = method_source.map(METHOD_MAP).fillna(method_source)

    return df

def remove_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    columns_with_nan          = df.columns[df.isnull().any()].tolist()
    single_unique_value_cols  = [c for c in df.columns if df[c].nunique() == 1]
    white_black_cols          = [c for c in df.columns if "white" in c or "black" in c]
    explicit_drop             = ['url', 'uuid', 'eco', 'fen', 'pgn', 'tcn',
                                 'white_uuid', 'white_id', 'black_uuid', 'black_id']

    to_drop = set(columns_with_nan + single_unique_value_cols + white_black_cols + explicit_drop)
    df = df.drop(columns=[c for c in to_drop if c in df.columns])

    return df

