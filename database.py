import sqlite3

def create_database():
    conn = sqlite3.connect("guzoai.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            route TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            passengers INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_database()