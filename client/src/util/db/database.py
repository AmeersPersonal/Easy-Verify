import os
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._create_tables()
        DB_PATH = os.path.join(os.path.dirname(__file__), "easyverify.db")

    def _create_tables(self):
        # company demo table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `companyx` (
            `id` int(11) NOT NULL,
            `user_id` int(11) NOT NULL,
            `name` varchar(100) NOT NULL,
            `email` varchar(255) NOT NULL,
            `pw` char(100) NOT NULL,
            `verified` tinyint(1) DEFAULT NULL
            );

        """)
        self.conn.commit()
        # users table
        self.cursor.execute("""
            CREATE TABLE  IF NOT EXISTS `users` (
            `id` int(11) NOT NULL,
            `username` varchar(100) NOT NULL,
            `email` varchar(255) NOT NULL,
            `pw` char(60) NOT NULL,
            `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
            `is_persistent` tinyint(1) NOT NULL,
            `last_login` timestamp NOT NULL DEFAULT current_timestamp()
            );

        """)
        self.conn.commit()
        # verfication table only will be used to send if user is verified or not and then deleted unless they have the save feature enabled
        self.cursor.execute("""
            CREATE TABLE  IF NOT EXISTS `verifications` (
            `id` int(11) NOT NULL,
            `user_id` int(11) NOT NULL,
            `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
            `result` tinyint(1) NOT NULL,
            `method` text DEFAULT NULL,
            `policy` text DEFAULT NULL,
            `confidence` int(11) DEFAULT NULL,
            `error_code` text DEFAULT NULL,
            `token` text NOT NULL,
            `expires_at` timestamp NULL DEFAULT NULL
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

        self.cursor.execute("SELECT id FROM users WHERE email = ?", (email))
        return self.cursor.fetchone()[0]

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
