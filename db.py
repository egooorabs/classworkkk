import aiosqlite
import sqlite3
import datetime

class Database:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY,
                                username TEXT,
                                registration_date TEXT,
                                active INTEGER DEFAULT 1
                              )''')
        self.connection.commit()

    async def user_exists(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return bool(result)

    async def add_user(self, user_id, username=None):
        registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO users (user_id, username, registration_date) VALUES (?, ?, ?)", (user_id, username, registration_date))
        self.connection.commit()

    async def set_active(self, user_id, active):
        self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id))
        self.connection.commit()

    async def get_users(self):
        self.cursor.execute("SELECT user_id, active FROM users")
        return self.cursor.fetchall()