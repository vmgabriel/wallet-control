import pytest
from uuid import uuid4
from datetime import date

from cashflow.domain.models import Expense
from cashflow.infrastructure.database import get_connection, DB_PATH
from cashflow.infrastructure.repositories import SQLiteExpenseRepository


@pytest.fixture
def test_db_path(tmp_path):
    """Crea una ruta temporal para la base de datos de tests"""
    return tmp_path / "test_cashflow.db"


@pytest.fixture
def test_db(test_db_path):
    """
    Fixture que crea una DB SQLite en memoria temporal.
    Se limpia automáticamente después de cada test.
    """
    # Override temporal del DB_PATH
    original_path = DB_PATH
    import cashflow.infrastructure.database as db_module
    db_module.DB_PATH = test_db_path

    # Crear tabla
    with get_connection() as conn:
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

    yield test_db_path

    # Cleanup: restaurar path original
    db_module.DB_PATH = original_path
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.fixture
def expense_repo(test_db):
    return SQLiteExpenseRepository()


@pytest.fixture
def sample_expense():
    return Expense(
        id=uuid4(),
        amount=50.00,
        description="Almuerzo de prueba",
        category="Comida",
        date=date.today()
    )


@pytest.fixture
def sample_expenses():
    return [
        Expense(
            id=uuid4(),
            amount=50.00,
            description="Almuerzo",
            category="Comida",
            date=date.today()
        ),
        Expense(
            id=uuid4(),
            amount=100.00,
            description="Transporte",
            category="Movilidad",
            date=date.today()
        ),
        Expense(
            id=uuid4(),
            amount=25.50,
            description="Café",
            category="Comida",
            date=date.today()
        ),
    ]
