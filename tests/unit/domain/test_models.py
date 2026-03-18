import pytest
from datetime import date
from uuid import UUID

from cashflow.domain.models import Expense


class TestExpenseModel:
    """Tests para la entidad Expense"""

    def test_create_expense(self):
        """Debe crear un expense con ID automático"""
        expense = Expense.create(
            amount=100.00,
            description="Test expense",
            category="General"
        )

        assert isinstance(expense.id, UUID)
        assert expense.amount == 100.00
        assert expense.description == "Test expense"
        assert expense.category == "General"
        assert expense.date == date.today()

    def test_create_expense_with_custom_date(self):
        """Debe permitir especificar una fecha personalizada"""
        custom_date = date(2024, 1, 15)
        expense = Expense.create(
            amount=50.00,
            description="Test",
            category="Test",
            date=custom_date
        )

        assert expense.date == custom_date

    def test_expense_amount_validation(self):
        """Debe aceptar montos decimales"""
        expense = Expense.create(
            amount=99.99,
            description="Test",
            category="Test"
        )

        assert expense.amount == 99.99

    def test_expense_id_is_unique(self):
        """Cada expense debe tener un ID único"""
        expense1 = Expense.create(100, "Test 1", "Cat1")
        expense2 = Expense.create(100, "Test 2", "Cat1")

        assert expense1.id != expense2.id
