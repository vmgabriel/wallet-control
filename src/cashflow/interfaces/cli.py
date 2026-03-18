import typer
from rich.console import Console
from rich.table import Table
from cashflow.infrastructure.repositories import SQLiteExpenseRepository
from cashflow.application.services import ExpenseService
from cashflow.infrastructure.database import init_db

app = typer.Typer()
console = Console()

# Inyección de dependencias simple para la CLI
def get_service() -> ExpenseService:
    init_db() # Asegurar DB existe
    repo = SQLiteExpenseRepository()
    return ExpenseService(repo)

@app.command()
def add(amount: float, description: str, category: str = "General"):
    """Registrar un nuevo gasto."""
    service = get_service()
    expense = service.record_expense(amount, description, category)
    console.print(f"[green]✓ Gasto registrado:[/green] {expense.description} (${expense.amount})")

@app.command()
def summary():
    """Ver resumen de flujo de caja."""
    service = get_service()
    data = service.get_summary()

    console.print(f"\n[bold]Balance Total:[/bold] ${data['total_expenses']:.2f}")
    console.print(f"[bold]Movimientos:[/bold] {data['count']}\n")

    table = Table(title="Últimos Movimientos")
    table.add_column("Fecha", style="cyan")
    table.add_column("Categoría", style="magenta")
    table.add_column("Descripción", style="white")
    table.add_column("Monto", style="red")

    for exp in data['last_movements']:
        table.add_row(
            exp.date.isoformat(),
            exp.category,
            exp.description,
            f"${exp.amount:.2f}"
        )
    console.print(table)

if __name__ == "__main__":
    app()