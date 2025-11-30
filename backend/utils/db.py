import sqlite3

DB_NAME = "election.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # so we can access columns by name
    return conn

def init_db():
    conn = get_db()

    # USERS TABLE
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name   TEXT,
        student_id  TEXT UNIQUE,
        email       TEXT,
        password    TEXT,
        eth_address TEXT
    );
    """)

    # VOTES TABLE
    conn.execute("""
    CREATE TABLE IF NOT EXISTS votes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id  TEXT UNIQUE,
        candidate_id INTEGER
    );
    """)

    conn.commit()
    conn.close()

