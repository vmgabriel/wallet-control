import pytest
from abc import ABC

from cashflow.domain.repositories import ExpenseRepository


class TestExpenseRepositoryContract:
    """Verifica que el repositorio cumpla el contrato del dominio"""

    def test_repository_is_abstract(self):
        """El repositorio base debe ser abstracto"""
        assert issubclass(ExpenseRepository, ABC)

    def test_repository_has_required_methods(self):
        """El repositorio debe definir los métodos requeridos"""
        required_methods = ['add', 'get_all', 'get_balance']

        for method in required_methods:
            assert hasattr(ExpenseRepository, method), \
                f"ExpenseRepository debe implementar '{method}'"