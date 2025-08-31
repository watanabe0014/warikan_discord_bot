import sqlite3

DB_NAME = "payments.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            amount INTEGER,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_payment(user_id, amount, reason=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO payments (user_id, amount, reason) VALUES (?, ?, ?)",
              (user_id, amount, reason))
    conn.commit()
    conn.close()

def get_payments(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT amount FROM payments WHERE user_id=?", (user_id,))
    results = c.fetchall()
    conn.close()
    return results

def clear_payments(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM payments WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()