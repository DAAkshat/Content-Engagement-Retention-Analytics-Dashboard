import numpy as np
import pandas as pd
from pathlib import Path

GENRES = ["Romance", "Thriller", "Fantasy", "Horror", "Comedy"]
DAYS = 90
N_USERS = 10_000
RNG = np.random.default_rng(42)

def generate():
    base = Path(__file__).resolve().parent
    start = pd.Timestamp("2024-01-01")

    users = pd.DataFrame({
        "user_id": range(1, N_USERS + 1),
        "signup_date": (start + pd.to_timedelta(RNG.integers(0, DAYS, N_USERS), unit="D")).strftime("%Y-%m-%d"),
        "preferred_genre": RNG.choice(GENRES, N_USERS),
        "is_premium": RNG.choice([0, 1], N_USERS, p=[0.7, 0.3]),
    })

    sessions, sid = [], 1
    for uid in users["user_id"]:
        n = RNG.integers(1, 15)
        for _ in range(n):
            genre = RNG.choice(GENRES)
            completion = float(np.clip(RNG.beta(2, 2), 0, 1))
            sessions.append({
                "session_id": sid, "user_id": uid,
                "session_date": (start + pd.to_timedelta(RNG.integers(0, DAYS), unit="D")).strftime("%Y-%m-%d"),
                "genre": genre,
                "episode_completion_rate": round(completion, 3),
                "session_duration_mins": round(float(RNG.uniform(5, 60)), 1),
                "episodes_played": int(RNG.integers(1, 6)),
            })
            sid += 1

    notifications = []
    for uid in users["user_id"]:
        group = "A" if uid % 2 == 0 else "B"
        re_engaged = 1 if (group == "B" and RNG.random() < 0.18) or (group == "A" and RNG.random() < 0.12) else 0
        notifications.append({
            "user_id": uid, "ab_group": group,
            "sent_date": (start + pd.to_timedelta(RNG.integers(30, DAYS), unit="D")).strftime("%Y-%m-%d"),
            "re_engaged": re_engaged,
        })

    pd.DataFrame(sessions).to_csv(base / "sessions.csv", index=False)
    users.to_csv(base / "users.csv", index=False)
    pd.DataFrame(notifications).to_csv(base / "notifications.csv", index=False)
    print(f"Generated {len(users)} users, {len(sessions)} sessions, {len(notifications)} notifications")

if __name__ == "__main__":
    generate()
