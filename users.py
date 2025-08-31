import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paypay_id TEXT,
        user_name TEXT,
        mail_address TEXT,
        tell_num INTEGER,
        payments_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_user(paypay_id, user_name, mail_address, tell_num, payments_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (paypay_id, user_name, mail_address, tell_num) VALUES (?, ?, ?, ?)",
              (paypay_id, user_name, mail_address, tell_num))
    conn.commit()
    conn.close()

def get_users(guild_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, amount FROM users WHERE guild_id=?", (guild_id,))
    results = c.fetchall()
    conn.close()
    return results

def clear_users(guild_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE guild_id=?", (guild_id,))
    conn.commit()
    conn.close()
