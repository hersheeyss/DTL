import sqlite3

DB_NAME = "election.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
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

    # VOTES TABLE (anonymous voter_hash)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS votes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_hash TEXT UNIQUE,
        candidate_id INTEGER
    );
    """)

    conn.commit()
    conn.close()


# ⬇️ New function: get total votes per candidate
def get_vote_counts():
    conn = get_db()

    rows = conn.execute("""
        SELECT candidate_id, COUNT(*) AS votes
        FROM votes
        GROUP BY candidate_id
    """).fetchall()

    # Return as dictionary {candidate_id: count}
    return {row["candidate_id"]: row["votes"] for row in rows}


