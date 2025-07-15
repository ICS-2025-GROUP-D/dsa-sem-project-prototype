import sqlite3

# =============== Class to handle connections with SQLite database ===============

class DatabaseManager:
    def __init__(self):
        self.db_name = "entries.db"
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                content TEXT,
                mood TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_entry(self, date, content, mood):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (date, content, mood) VALUES (?, ?, ?)", (date, content, mood))
        conn.commit()
        conn.close()

    def update_entry(self, entry_id, content, mood):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE entries SET content = ?, mood = ? WHERE id = ?", (content, mood, entry_id))
        conn.commit()
        conn.close()

    def delete_entry(self, entry_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()

    def fetch_entry(self, entry_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT content, mood FROM entries WHERE id = ?", (entry_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def fetch_entry_info(self, entry_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT date, mood FROM entries WHERE id = ?", (entry_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def fetch_entry_id(self, date, content):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM entries WHERE date = ? AND content = ?", (date, content,))
        result = cursor.fetchone()
        conn.close()
        return result

    def fetch_all_entries(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, mood FROM entries ORDER BY date DESC")
        result = cursor.fetchall()
        conn.close()
        return result

    def fetch_all_entries_bst(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, mood FROM entries")
        result = cursor.fetchall()
        conn.close()
        return result

    def search_entries_by_date(self, date_prefix):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, mood FROM entries WHERE date LIKE ?", (date_prefix + '%',))
        result = cursor.fetchall()
        conn.close()
        return result