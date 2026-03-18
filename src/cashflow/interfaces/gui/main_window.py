"""
Ventana principal con compatibilidad libadwaita 1.0+.
Evita widgets introducidos en versiones recientes.
"""
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from cashflow.interfaces.gui.add_expense_dialog import AddExpenseDialog


class ExpenseRow(Gtk.ListBoxRow):
    """Widget para mostrar un gasto en la lista"""

    def __init__(self, expense):
        super().__init__()
        self.expense = expense

        box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            margin_start=12, margin_end=12, margin_top=6, margin_bottom=6
        )

        # Fecha
        date_label = Gtk.Label(
            label=expense.date.strftime("%d/%m"),
            halign=Gtk.Align.START,
            css_classes=["caption", "dim-label"]
        )
        date_label.set_size_request(40, -1)

        # Descripción y categoría
        details_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2, hexpand=True)
        desc_label = Gtk.Label(
            label=expense.description,
            halign=Gtk.Align.START,
            ellipsize=3
        )
        cat_label = Gtk.Label(
            label=expense.category,
            halign=Gtk.Align.START,
            css_classes=["caption", "dim-label"]
        )
        details_box.append(desc_label)
        details_box.append(cat_label)

        # Monto
        amount_label = Gtk.Label(
            label=f"${expense.amount:.2f}",
            halign=Gtk.Align.END,
            css_classes=["heading"]
        )
        amount_label.set_size_request(80, -1)

        box.append(date_label)
        box.append(details_box)
        box.append(amount_label)
        self.set_child(box)


class CashFlowMainWindow(Adw.ApplicationWindow):
    """Ventana principal compatible con libadwaita 1.0+"""

    def __init__(self, app, service=None):
        super().__init__(
            application=app,
            title="CashFlow",
            default_width=400,
            default_height=600
        )

        self.service = service

        # ✅ ToolbarView (patrón correcto de libadwaita)
        toolbar_view = Adw.ToolbarView()

        # Header bar
        header = Adw.HeaderBar()
        self.add_btn = Gtk.Button(
            icon_name="list-add-symbolic",
            tooltip_text="Agregar gasto",
            css_classes=["suggested-action"]
        )
        self.add_btn.connect("clicked", self.on_add_expense)
        header.pack_end(self.add_btn)
        toolbar_view.add_top_bar(header)

        # Contenido principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # ✅ Tarjeta de balance (compatible: Gtk.Box + css_classes=["card"])
        balance_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            margin_start=16, margin_end=16, margin_top=12, margin_bottom=12,
            spacing=12,
            css_classes=["card"]  # ← Estilo de tarjeta sin Adw.Card
        )

        icon_label = Gtk.Label(label="💰", css_classes=["title-1"])
        icon_label.set_size_request(40, 40)
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, hexpand=True)

        self.balance_label = Gtk.Label(
            label="$0.00",
            halign=Gtk.Align.START,
            css_classes=["title-1", "accent"]
        )
        subtitle_label = Gtk.Label(
            label="Balance total",
            halign=Gtk.Align.START,
            css_classes=["body", "dim-label"]
        )

        text_box.append(self.balance_label)
        text_box.append(subtitle_label)
        balance_box.append(icon_label)
        balance_box.append(text_box)

        # Lista de gastos
        list_header = Gtk.Label(
            label="Últimos movimientos",
            halign=Gtk.Align.START,
            margin_start=16, margin_top=8, margin_bottom=4,
            css_classes=["heading"]
        )

        self.expense_list = Gtk.ListBox(
            css_classes=["boxed-list"],
            margin_start=12, margin_end=12, margin_bottom=12
        )
        self.expense_list.set_selection_mode(Gtk.SelectionMode.NONE)

        # Placeholder
        self.placeholder = Gtk.Label(
            label="No hay gastos registrados\n¡Agrega tu primer gasto!",
            margin_top=40,
            css_classes=["dim-label"]
        )

        # Stack
        self.stack = Gtk.Stack()
        self.stack.add_named(self.placeholder, "empty")
        self.stack.add_named(self.expense_list, "list")

        # Layout
        main_box.append(balance_box)  # ← Sin Card wrapper
        main_box.append(list_header)
        main_box.append(self.stack)

        scrolled = Gtk.ScrolledWindow(
            hscrollbar_policy=Gtk.PolicyType.NEVER,
            vscrollbar_policy=Gtk.PolicyType.AUTOMATIC,
            hexpand=True, vexpand=True
        )
        scrolled.set_child(main_box)

        toolbar_view.set_content(scrolled)
        self.set_content(toolbar_view)

        if self.service:
            self.refresh_summary()

    def refresh_summary(self):
        """Actualizar UI con datos del servicio"""
        if not self.service:
            return
        summary = self.service.get_summary()
        self.balance_label.set_label(f"${summary['total_expenses']:.2f}")

        # Limpiar lista
        child = self.expense_list.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.expense_list.remove(child)
            child = next_child

        # Agregar items
        if summary['last_movements']:
            self.stack.set_visible_child_name("list")
            for expense in summary['last_movements']:
                row = ExpenseRow(expense)
                self.expense_list.append(row)
        else:
            self.stack.set_visible_child_name("empty")

    def on_add_expense(self, _button):
        if self.service:
            dialog = AddExpenseDialog(self.service)
            dialog.connect("closed", self.on_add_response)
            dialog.present()

    def on_add_response(self, dialog):
        """Callback cuando el diálogo se cierra (señal 'closed')"""
        if self.service:
            self.refresh_summary()
