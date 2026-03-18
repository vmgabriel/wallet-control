import pytest
from datetime import date

from cashflow.application.services import ExpenseService
from cashflow.domain.models import Expense


class TestExpenseService:
    """Tests para el servicio de gastos"""

    def test_record_expense(self, expense_repo, sample_expense):
        """Debe registrar un gasto correctamente"""
        service = ExpenseService(expense_repo)

        result = service.record_expense(
            amount=sample_expense.amount,
            description=sample_expense.description,
            category=sample_expense.category
        )

        assert isinstance(result, Expense)
        assert result.amount == sample_expense.amount
        assert result.description == sample_expense.description

    def test_get_summary_empty(self, expense_repo):
        """Debe retornar resumen vacío cuando no hay gastos"""
        service = ExpenseService(expense_repo)
        summary = service.get_summary()

        assert summary['total_expenses'] == 0.0
        assert summary['count'] == 0
        assert summary['last_movements'] == []

    def test_get_summary_with_expenses(self, expense_repo, sample_expenses):
        """Debe calcular correctamente el resumen con gastos"""
        service = ExpenseService(expense_repo)

        # Registrar gastos
        for exp in sample_expenses:
            expense_repo.add(exp)

        summary = service.get_summary()

        assert summary['count'] == 3
        assert summary['total_expenses'] == 175.50  # 50 + 100 + 25.50
        assert len(summary['last_movements']) == 3

    def test_get_summary_limits_last_movements(self, expense_repo, sample_expenses):
        """Debe limitar los últimos movimientos a 5"""
        service = ExpenseService(expense_repo)

        # Agregar más de 5 gastos
        for i in range(10):
            expense_repo.add(Expense.create(10, f"Gasto {i}", "Test"))

        summary = service.get_summary()

        assert len(summary['last_movements']) == 5