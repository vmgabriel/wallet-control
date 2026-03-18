from typing import List
from datetime import date as date_type  # ← Importar tipo date
from cashflow.domain.models import Expense
from cashflow.domain.repositories import ExpenseRepository
from cashflow.infrastructure.database import get_connection
import uuid

class SQLiteExpenseRepository(ExpenseRepository):
    def add(self, expense: Expense) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO expenses (id, amount, description, category, date) VALUES (?, ?, ?, ?, ?)",
                (str(expense.id), expense.amount, expense.description, expense.category, expense.date.isoformat())
            )
            conn.commit()

    def get_all(self) -> List[Expense]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
            return [
                Expense(
                    id=uuid.UUID(row["id"]),
                    amount=row["amount"],
                    description=row["description"],
                    category=row["category"],
                    date=date_type.fromisoformat(row["date"])
                )
                for row in rows
            ]

    def get_balance(self) -> float:
        with get_connection() as conn:
            res = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()
            return res[0] or 0.0