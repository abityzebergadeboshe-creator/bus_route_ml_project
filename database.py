import sqlite3


DATABASE = "guzoai.db"


def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # ==============================
    # DRIVER TABLE
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            driver_id TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    # ==============================
    # DRIVER SCHEDULE TABLE
    # ==============================

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

    # ==============================
    # PASSENGER BOOKINGS TABLE
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passenger_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            destination TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("GuzoAI database created successfully.")
