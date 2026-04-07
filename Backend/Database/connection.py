import sqlite3
import sqlite_vec


def get_db_connection(db_path="lol_data.db"):
    """Return a database connection with vector module."""
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn
