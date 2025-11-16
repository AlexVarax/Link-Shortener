import sqlite3
import os.path
import sys


class DB_Connect:
    def __init__(self, db_path=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'link-short.db')):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER,
                    original_url TEXT NOT NULL,
                    short_key TEXT NOT NULL UNIQUE,
                    FOREIGN KEY (id) REFERENCES users(id)
                )
            """)

    def anti_sql_injection(self, param: str) -> bool:
        return True

    def get_full_url(self, short_key: str):
        if not self.anti_sql_injection(short_key):
            return None

        self.cur.execute('SELECT original_url FROM urls WHERE short_key = ?', (short_key,))
        result = self.cur.fetchone()

        print(result)

        return result[0] if result else None

    def add_short_url(self, user_id: int, original_url: str, short_key: str):
        if not self.anti_sql_injection(original_url) or not self.anti_sql_injection(short_key):
            return False

        try:
            with self.connection:
                self.cur.execute('SELECT short_key FROM urls WHERE short_key = ?', (short_key,))
                count_short_key = self.cur.fetchone()

                if count_short_key == 0 or count_short_key == None:
                    self.cur.execute(
                        'INSERT INTO urls (id, original_url, short_key) VALUES (?, ?, ?)',
                        (user_id, original_url, short_key)
                    )
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_name(self, user_id: int):
        self.cur.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        result = self.cur.fetchone()

        return result[0] if result else None

    def add_user(self, user_id: int, name: str):
        if not self.anti_sql_injection(name):
            return False

        try:
            with self.connection:
                self.cur.execute('SELECT id FROM users WHERE id = ?', (user_id,))
                count_id = self.cur.fetchone()
                if count_id == None or count_id == 0:
                    self.cur.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, name))
            return True
        except sqlite3.IntegrityError:
            return False

    def close(self):
        self.connection.close()
