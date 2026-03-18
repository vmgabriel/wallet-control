"""
Entry point de la aplicación GUI con libadwaita.
"""
import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio

from cashflow.infrastructure.repositories import SQLiteExpenseRepository
from cashflow.application.services import ExpenseService
from cashflow.interfaces.gui.main_window import CashFlowMainWindow


class CashFlowApp(Adw.Application):
    """Aplicación principal con libadwaita"""

    def __init__(self):
        # Sin flags para máxima compatibilidad
        super().__init__(application_id="com.github.vmgabriel.cashflow")
        self.repo = SQLiteExpenseRepository()
        self.service = ExpenseService(self.repo)
        self.main_window = None

    def do_activate(self):
        if not self.main_window:
            self.main_window = CashFlowMainWindow(self, self.service)
        self.main_window.present()

    def do_startup(self):
        Adw.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", lambda *_: self.quit())
        self.add_action(action)

    def on_about(self, _action, _param):
        about = Adw.AboutDialog(
            application_name="CashFlow",
            version="0.1.0",
            developer_name="Gabriel",
            license_type=Gtk.License.MIT_X11,
            website="https://github.com/vmgabriel/wallet-control",
            issue_url="https://github.com/vmgabriel/wallet-control/issues",
            developers=["Gabriel"],
            copyright="© 2026 Gabriel"
        )
        about.present(self.main_window)


def run_gui():
    """Función de entrada para ejecutar la GUI"""
    app = CashFlowApp()
    return app.run(sys.argv)