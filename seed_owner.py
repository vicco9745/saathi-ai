import os, secrets, sqlite3
from dotenv import load_dotenv

load_dotenv()
db = os.getenv("DATABASE_PATH", "ichat.db")
key = os.getenv("OWNER_API_KEY") or "ichat_owner_" + secrets.token_urlsafe(32)

conn = sqlite3.connect(db)
conn.execute("""
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    key TEXT UNIQUE NOT NULL,
    owner INTEGER DEFAULT 0,
    active INTEGER DEFAULT 1,
    plan TEXT DEFAULT 'free',
    request_count INTEGER DEFAULT 0
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS usage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_key_id INTEGER,
    service TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")
conn.execute(
    "INSERT OR IGNORE INTO api_keys(name,key,owner,active,plan) VALUES(?,?,?,?,?)",
    ("Owner", key, 1, 1, "owner")
)
conn.commit()
conn.close()

print("Owner API key:", key)
print("Keep this key private.")
