import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "analytics.db"
DATA = ROOT / "data"

def load():
    import sys
    sys.path.insert(0, str(ROOT))
    from data.generate_data import generate
    if not (DATA / "users.csv").exists():
        generate()

    conn = sqlite3.connect(DB)
    conn.executescript((Path(__file__).parent / "schema.sql").read_text())
    for table in ("users", "sessions", "notifications"):
        df = pd.read_csv(DATA / f"{table}.csv")
        df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Database loaded at {DB}")

if __name__ == "__main__":
    load()
