import sqlite3
import os
from contextlib import contextmanager

DB_FILE = "xenons.db"

class DatabaseManager:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self.get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS findings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    module TEXT NOT NULL,
                    target TEXT,
                    details TEXT,
                    severity TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def log_finding(self, module, target, details, severity="INFO"):
        with self.get_conn() as conn:
            conn.execute("INSERT INTO findings (module, target, details, severity) VALUES (?,?,?,?)",
                         (module, target, details, severity))
            conn.commit()

db = DatabaseManager()
