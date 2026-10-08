import sqlite3


def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            image_password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


def add_user(username, email, password, image_password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users
            (username, email, password, image_password)
            VALUES (?, ?, ?, ?)
        """, (username, email, password, image_password))

        conn.commit()
        print("User added successfully!")

    except sqlite3.IntegrityError:
        print("Username already exists!")

    conn.close()


def get_user(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, email, password, image_password
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user