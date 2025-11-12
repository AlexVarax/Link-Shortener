import sqlite3


connection = sqlite3.connect('DataLayer/link-short.db')
cur = connection.cursor()

with connection:
    if not (cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{users}'")):
        cur.execute("""
            CREATE TABLE users (
                id INT,
                name TEXT
                )
        """)

        cur.execute("""
            CREATE TABLE urls (
                id INT,
                original_url TEXT,
                short_key TEXT
                )         
        """)

        connection.commit()


connection.close()