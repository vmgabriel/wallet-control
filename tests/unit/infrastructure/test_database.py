"""
Tests para la infraestructura de base de datos.
"""
import pytest
import sqlite3
from pathlib import Path

from cashflow.infrastructure.database import get_connection, init_db, DB_PATH


class TestDatabaseConnection:
    """Tests para la conexión a la base de datos"""

    def test_get_connection_returns_connection(self, test_db):
        """Debe retornar una conexión SQLite válida"""
        with get_connection() as conn:
            assert isinstance(conn, sqlite3.Connection)
            assert conn.row_factory == sqlite3.Row

    def test_get_connection_closes_properly(self, test_db):
        """La conexión debe cerrarse después del contexto"""
        with get_connection() as conn:
            cursor = conn.cursor()

        # Después del contexto, la conexión debe estar cerrada
        with pytest.raises(sqlite3.ProgrammingError):
            cursor.execute("SELECT 1")


class TestDatabaseInit:
    """Tests para la inicialización de la base de datos"""

    def test_init_db_creates_table(self, test_db):
        """init_db debe crear la tabla expenses"""
        init_db()

        with get_connection() as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()

        table_names = [t[0] for t in tables]
        assert 'expenses' in table_names

    def test_init_db_is_idempotent(self, test_db):
        """init_db debe poder ejecutarse múltiples veces sin error"""
        init_db()
        init_db()  # Segunda ejecución no debe fallar
        init_db()  # Tercera tampoco

        # Verificar que solo hay una tabla
        with get_connection() as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()

        assert len(tables) == 1

    def test_expenses_table_schema(self, test_db):
        """La tabla expenses debe tener el schema correcto"""
        init_db()

        with get_connection() as conn:
            columns = conn.execute("PRAGMA table_info(expenses)").fetchall()

        column_names = [col[1] for col in columns]
        expected_columns = ['id', 'amount', 'description', 'category', 'date']

        for col in expected_columns:
            assert col in column_names, f"Columna '{col}' falta en el schema"
