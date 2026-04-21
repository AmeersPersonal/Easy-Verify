import os
import sqlite3


class Database:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), "easyverify.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("PRAGMA foreign_keys = ON")

        # company demo table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companyx (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                pw TEXT NOT NULL,
                verified INTEGER DEFAULT NULL
            );

        """)
        self.conn.commit()
        # users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                pw TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                is_persistent INTEGER NOT NULL DEFAULT 0,
                last_login TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

        """)
        self.conn.commit()
        # verfication table only will be used to send if user is verified or not and then deleted unless they have the save feature enabled
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS verifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                result INTEGER NOT NULL,
                method TEXT DEFAULT NULL,
                policy TEXT DEFAULT NULL,
                confidence INTEGER DEFAULT NULL,
                error_code TEXT DEFAULT NULL,
                token TEXT NOT NULL,
                expires_at TEXT DEFAULT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        """)
        self.conn.commit()

    def create_user(self, username, email, pw, is_persistent):
        self.cursor.execute(
            """
            INSERT INTO users (username, email, pw, is_persistent) VALUES (?, ?, ?, ?)
        """,
            (username, email, pw, is_persistent),
        )
        self.conn.commit()

        self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = self.cursor.fetchone()
        return user[0] if user else None

    def validate_email(self, email) -> bool:
        self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone() is not None

    # from company_table
    def is_verified_company(self, email):
        self.cursor.execute(
            """ SELECT verified FROM companyx WHERE email = ? """, (email,)
        )
        result = self.cursor.fetchone()
        return result[0] == 1 if result else False

    # def is_verified_user(self, email):

    # company  table
    def update_verification(self, email: str, verified: int):
        self.cursor.execute(
            """ UPDATE companyx SET verified = ? WHERE email = ? """, (verified, email)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
