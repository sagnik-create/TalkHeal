import sqlite3
from contextlib import contextmanager

DB_PATH = "talkheal.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    with get_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        db.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
        db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            sender TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )""")

def create_user(username, email):
    with get_db() as db:
        db.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )

def get_user_by_username(username):
    with get_db() as db:
        cur = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        return cur.fetchone()

def get_user_by_email(email):
    with get_db() as db:
        cur = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )
        return cur.fetchone()

def create_chat(user_id, title):
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO chats (user_id, title) VALUES (?, ?)",
            (user_id, title)
        )
        return cur.lastrowid

def add_message(chat_id, sender, message):
    with get_db() as db:
        db.execute(
            "INSERT INTO messages (chat_id, sender, message) VALUES (?, ?, ?)",
            (chat_id, sender, message)
        )

def get_messages(chat_id):
    with get_db() as db:
        cur = db.execute(
            "SELECT * FROM messages WHERE chat_id = ? ORDER BY timestamp ASC",
            (chat_id,)
        )
        return cur.fetchall()