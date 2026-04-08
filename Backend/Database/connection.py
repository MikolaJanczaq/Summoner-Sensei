import os
import sqlite3
import sqlite_vec


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "lol_data.db")

def get_db_connection(db_path=DEFAULT_DB_PATH):
    """Return a database connection with vector module."""
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn
