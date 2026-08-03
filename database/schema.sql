CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    signup_date TEXT,
    preferred_genre TEXT,
    is_premium INTEGER
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    session_date TEXT,
    genre TEXT,
    episode_completion_rate REAL,
    session_duration_mins REAL,
    episodes_played INTEGER
);

CREATE TABLE IF NOT EXISTS notifications (
    user_id INTEGER,
    ab_group TEXT,
    sent_date TEXT,
    re_engaged INTEGER
);
