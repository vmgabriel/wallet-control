import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

DB_PATH = Path("cashflow.db")

@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager para conexiones SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Inicializa la tabla de expenses si no existe"""
    with get_connection() as conn:  # ← Ahora sí funciona correctamente
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id TEXT PRIMARY KEY,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        conn.commit()