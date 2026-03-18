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


@app.command()
def gui():
    """Abrir interfaz gráfica con GTK + libadwaita"""
    try:
        from cashflow.interfaces.gui.app import run_gui
        # Salir del programa CLI y ejecutar la GUI
        raise SystemExit(run_gui())
    except ImportError as e:
        console.print("[red]❌ GUI no disponible[/red]")
        console.print(f"\n[bold]Error:[/bold] {e}")
        console.print("\n[yellow]Solución:[/yellow]")
        console.print("1. Instala las dependencias opcionales:")
        console.print("   hatch run pip install '.[gui]'")
        console.print("\n2. Asegúrate de tener GTK 4 y libadwaita en tu sistema:")
        console.print("   - Fedora: sudo dnf install gtk4 libadwaita")
        console.print("   - Ubuntu: sudo apt install libgtk-4-dev libadwaita-1-dev")
        console.print("   - Arch: sudo pacman -S gtk4 libadwaita")


if __name__ == "__main__":
    app()
