import sqlite3
from pathlib import Path

DB_PATH = Path("src/database/telemetry.db")

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # events tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        timestamp TEXT,
        session_id TEXT,
        user_email TEXT,
        model TEXT,
        input_tokens INTEGER,
        output_tokens INTEGER,
        cost_usd REAL,
        tool_name TEXT,
        success TEXT,
        duration_ms INTEGER
    )
    """)

    # employees tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        email TEXT PRIMARY KEY,
        practice TEXT,
        level TEXT,
        location TEXT
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database setup completed at {DB_PATH}")


if __name__ == "__main__":
    setup_database()