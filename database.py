import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "resumes_final.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            score REAL,
            result TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_resume(filename, score, result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO resume_history (filename, score, result, created_at) VALUES (?, ?, ?, ?)",
        (filename, score, result, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resume_history ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resume_history")
    conn.commit()
    conn.close()