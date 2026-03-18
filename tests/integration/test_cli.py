"""
Tests de integración para la interfaz CLI.
"""
import pytest
from typer.testing import CliRunner

from cashflow.interfaces.cli import app
from cashflow.infrastructure.database import init_db, get_connection, DB_PATH


runner = CliRunner()


class TestCLI:
    """Tests para la interfaz de línea de comandos"""

    def test_cli_help(self):
        """El comando --help debe funcionar"""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Registrar un nuevo gasto" in result.stdout
        assert "Ver resumen de flujo de caja" in result.stdout

    def test_cli_add_expense(self, test_db, monkeypatch):
        """El comando add debe registrar un gasto"""
        # Override temporal del DB_PATH
        import cashflow.infrastructure.database as db_module
        original_path = db_module.DB_PATH
        db_module.DB_PATH = test_db

        try:
            init_db()
            result = runner.invoke(app, [
                "add", "50.00", "Test expense", "--category", "Test"
            ])

            assert result.exit_code == 0
            assert "Gasto registrado" in result.stdout
        finally:
            db_module.DB_PATH = original_path

    def test_cli_summary(self, test_db, monkeypatch):
        """El comando summary debe mostrar el resumen"""
        import cashflow.infrastructure.database as db_module
        original_path = db_module.DB_PATH
        db_module.DB_PATH = test_db

        try:
            init_db()
            # Agregar un gasto primero
            runner.invoke(app, ["add", "100.00", "Test", "--category", "Test"])

            result = runner.invoke(app, ["summary"])

            assert result.exit_code == 0
            assert "Balance Total" in result.stdout
        finally:
            db_module.DB_PATH = original_path
