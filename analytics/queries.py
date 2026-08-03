import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

DB = Path(__file__).resolve().parent.parent / "analytics.db"

def _conn():
    return sqlite3.connect(DB)

def get_dau():
    df = pd.read_sql("SELECT session_date, COUNT(DISTINCT user_id) AS dau FROM sessions GROUP BY session_date ORDER BY session_date", _conn())
    return df.to_dict("records")

def get_mau():
    df = pd.read_sql("SELECT COUNT(DISTINCT user_id) AS mau FROM sessions", _conn())
    return {"mau": int(df["mau"].iloc[0])}

def get_genre():
    df = pd.read_sql("""
        SELECT genre, ROUND(AVG(episode_completion_rate)*100, 1) AS avg_completion,
               COUNT(*) AS sessions FROM sessions GROUP BY genre ORDER BY avg_completion DESC
    """, _conn())
    return df.to_dict("records")

def get_churn():
    df = pd.read_sql("""
        SELECT genre,
               ROUND(100.0*SUM(CASE WHEN episode_completion_rate < 0.25 THEN 1 ELSE 0 END)/COUNT(*), 1) AS churn_pct
        FROM sessions GROUP BY genre ORDER BY churn_pct DESC
    """, _conn())
    return df.to_dict("records")

def get_abtest():
    df = pd.read_sql("""
        SELECT ab_group, COUNT(*) AS sent,
               SUM(re_engaged) AS re_engaged,
               ROUND(100.0*SUM(re_engaged)/COUNT(*), 2) AS rate
        FROM notifications GROUP BY ab_group ORDER BY ab_group
    """, _conn())
    raw = pd.read_sql("SELECT ab_group, re_engaged FROM notifications", _conn())
    ct = pd.crosstab(raw["ab_group"], raw["re_engaged"])
    chi2, p, _, _ = chi2_contingency(ct)
    return {"groups": df.to_dict("records"), "chi2": round(float(chi2), 3), "p_value": round(float(p), 4),
            "significant": bool(p < 0.05)}

def get_retention():
    df = pd.read_sql("""
        SELECT u.user_id, u.signup_date, s.session_date
        FROM users u JOIN sessions s ON u.user_id = s.user_id
    """, _conn())
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["session_date"] = pd.to_datetime(df["session_date"])
    df["week"] = ((df["session_date"] - df["signup_date"]).dt.days // 7).clip(0, 12)
    cohort = df.groupby(["signup_date", "week"])["user_id"].nunique().reset_index()
    sizes = df.groupby("signup_date")["user_id"].nunique()
    cohort["retention"] = cohort.apply(lambda r: round(100 * r["user_id"] / sizes[r["signup_date"]], 1), axis=1)
    return cohort.to_dict("records")

def get_mau_trend():
    df = pd.read_sql("SELECT session_date, user_id FROM sessions", _conn())
    df["session_date"] = pd.to_datetime(df["session_date"])
    df["month"] = df["session_date"].dt.to_period("M")
    trend = df.groupby("month")["user_id"].nunique().reset_index()
    trend["month"] = trend["month"].astype(str)
    trend.columns = ["month", "mau"]
    return trend.to_dict("records")

def get_cohort_heatmap():
    df = pd.read_sql("""
        SELECT u.signup_date, s.session_date, s.user_id
        FROM users u JOIN sessions s ON u.user_id = s.user_id
    """, _conn())
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["session_date"] = pd.to_datetime(df["session_date"])
    df["cohort_week"] = df["signup_date"].dt.to_period("W").astype(str)
    df["week_n"] = ((df["session_date"] - df["signup_date"]).dt.days // 7).clip(0, 8)
    active = df.groupby(["cohort_week", "week_n"])["user_id"].nunique().reset_index()
    sizes = df.groupby("cohort_week")["user_id"].nunique().rename("size")
    active = active.merge(sizes, on="cohort_week")
    active["retention_pct"] = (100 * active["user_id"] / active["size"]).round(1)
    pivot = active.pivot(index="cohort_week", columns="week_n", values="retention_pct").fillna(0)
    for w in pivot.columns:
        if w == 0:
            pivot[w] = 100.0
    return {"cohorts": pivot.index.tolist(), "weeks": [int(c) for c in pivot.columns],
            "values": pivot.values.tolist()}

def get_genre_funnel():
    df = pd.read_sql("SELECT genre, episode_completion_rate FROM sessions", _conn())
    stages = [("Total Plays", 0), ("25%", 0.25), ("50%", 0.5), ("75%", 0.75), ("Completed", 1.0)]
    result = {}
    for genre in df["genre"].unique():
        g = df[df["genre"] == genre]
        total = len(g)
        result[genre] = [total] + [int((g["episode_completion_rate"] >= t).sum()) for _, t in stages[1:]]
    return result

def get_premium_vs_free():
    df = pd.read_sql("""
        SELECT u.is_premium,
               ROUND(AVG(s.episode_completion_rate)*100, 1) AS avg_completion,
               ROUND(AVG(s.session_duration_mins), 1) AS avg_duration,
               ROUND(AVG(s.episodes_played), 1) AS avg_episodes
        FROM sessions s JOIN users u ON s.user_id = u.user_id
        GROUP BY u.is_premium
    """, _conn())
    df["label"] = df["is_premium"].map({0: "Free", 1: "Premium"})
    return df.to_dict("records")

def get_kpis():
    df = pd.read_sql("""
        SELECT COUNT(*) AS total_sessions,
               ROUND(AVG(episode_completion_rate)*100, 1) AS avg_completion,
               ROUND(100.0*SUM(CASE WHEN episode_completion_rate < 0.25 THEN 1 ELSE 0 END)/COUNT(*), 1) AS churn_pct
        FROM sessions
    """, _conn())
    dau = pd.read_sql("SELECT AVG(dau) AS avg_dau FROM (SELECT COUNT(DISTINCT user_id) AS dau FROM sessions GROUP BY session_date)", _conn())
    k = df.iloc[0].to_dict()
    k["avg_dau"] = int(dau["avg_dau"].iloc[0])
    return k
