import os, sqlite3
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DATABASE_PATH", "ichat.db")

def connect():
    return sqlite3.connect(DB)

def init_db():
    conn = connect()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        key TEXT UNIQUE NOT NULL,
        owner INTEGER DEFAULT 0,
        active INTEGER DEFAULT 1,
        plan TEXT DEFAULT 'free',
        request_count INTEGER DEFAULT 0
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS usage_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key_id INTEGER,
        service TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

def get_key_record(api_key):
    conn = connect()
    row = conn.execute(
        "SELECT id,name,key,owner,active,plan,request_count FROM api_keys WHERE key=?",
        (api_key,)
    ).fetchone()
    conn.close()
    return row

def log_usage(key_id, service):
    conn = connect()
    conn.execute("UPDATE api_keys SET request_count=request_count+1 WHERE id=?", (key_id,))
    conn.execute("INSERT INTO usage_logs(api_key_id,service) VALUES(?,?)", (key_id, service))
    conn.commit()
    conn.close()
