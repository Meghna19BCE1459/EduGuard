import sqlite3, json
from pathlib import Path

DB_PATH = Path("data/audits.db")

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY,
            platform TEXT,
            url TEXT,
            c1 INTEGER, c2 INTEGER, c3 INTEGER, c4 INTEGER, c5 INTEGER,
            total INTEGER,
            flags TEXT,
            audited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.commit()
    con.close()

def save_result(platform, url, scores):
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        INSERT INTO audits (platform, url, c1, c2, c3, c4, c5, total, flags)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (platform, url, scores["C1"], scores["C2"], scores["C3"],
          scores["C4"], scores["C5"], scores["total"], scores.get("flags","")))
    con.commit()
    con.close()

def get_all():
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("SELECT platform, url, c1, c2, c3, c4, c5, total, flags, audited_at FROM audits ORDER BY total DESC").fetchall()
    con.close()
    return rows