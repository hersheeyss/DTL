import sqlite3
import os

DB_NAME = "election.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()

    # USERS TABLE
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id  TEXT UNIQUE NOT NULL,
        password    TEXT NOT NULL,
        eth_address TEXT NOT NULL
    );
    """)

    # VOTES TABLE (anonymous via hash, one vote per student)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_hash  TEXT UNIQUE NOT NULL,
        candidate_id INTEGER NOT NULL
    );
    """)

    conn.commit()
    conn.close()


