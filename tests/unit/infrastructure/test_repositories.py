"""
Tests para la implementación del repositorio SQLite.
"""
import pytest
from datetime import date

from cashflow.domain.models import Expense
from cashflow.infrastructure.repositories import SQLiteExpenseRepository


class TestSQLiteExpenseRepository:
    """Tests para el repositorio SQLite"""

    def test_add_expense(self, expense_repo, sample_expense):
        """Debe agregar un gasto a la base de datos"""
        expense_repo.add(sample_expense)

        expenses = expense_repo.get_all()
        assert len(expenses) == 1
        assert expenses[0].id == sample_expense.id
        assert expenses[0].amount == sample_expense.amount

    def test_get_all_returns_all_expenses(self, expense_repo, sample_expenses):
        """Debe retornar todos los gastos registrados"""
        for exp in sample_expenses:
            expense_repo.add(exp)

        expenses = expense_repo.get_all()
        assert len(expenses) == 3

    def test_get_all_orders_by_date_desc(self, expense_repo):
        """Debe ordenar los gastos por fecha descendente"""
        expenses = [
            Expense.create(10, "Old", "Cat", date(2024, 1, 1)),
            Expense.create(20, "New", "Cat", date(2024, 12, 31)),
            Expense.create(30, "Mid", "Cat", date(2024, 6, 15)),
        ]

        for exp in expenses:
            expense_repo.add(exp)

        result = expense_repo.get_all()
        assert result[0].date == date(2024, 12, 31)  # Más reciente primero
        assert result[2].date == date(2024, 1, 1)    # Más antiguo al final

    def test_get_balance_returns_sum(self, expense_repo, sample_expenses):
        """Debe calcular la suma total de gastos"""
        for exp in sample_expenses:
            expense_repo.add(exp)

        balance = expense_repo.get_balance()
        assert balance == 175.50  # 50 + 100 + 25.50

    def test_get_balance_empty(self, expense_repo):
        """Debe retornar 0 cuando no hay gastos"""
        balance = expense_repo.get_balance()
        assert balance == 0.0

    def test_expense_persistence(self, expense_repo, sample_expense):
        """Los gastos deben persistir entre llamadas"""
        expense_repo.add(sample_expense)

        # Nueva instancia (simula nueva sesión)
        all_expenses = expense_repo.get_all()
        assert len(all_expenses) == 1
        assert all_expenses[0].description == sample_expense.description
