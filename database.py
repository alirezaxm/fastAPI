import sqlite3

DATABASE_NAME = "database.db"


def get_connection():
    """ایجاد اتصال به دیتابیس"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # امکان دسترسی به ستون‌ها با نام
    return conn


def init_db():
    """ایجاد جدول users در صورت عدم وجود"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "main":
    init_db()
    print("Database initialized successfully.")