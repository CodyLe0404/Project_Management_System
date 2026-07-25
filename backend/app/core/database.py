from collections.abc import Iterator
from contextlib import contextmanager
import pyodbc

from app.config import get_database_config


@contextmanager
def get_db_connection() -> Iterator[pyodbc.Connection]:
    config = get_database_config()
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['username']};"
        f"PWD={config['password']};"
        f"Encrypt=no;"
        f"TrustServerCertificate=yes;"
    )

    conn = pyodbc.connect(conn_str)
    try:
        yield conn
    finally:
        conn.close()
