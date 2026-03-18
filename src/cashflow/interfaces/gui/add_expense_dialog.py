"""
Diálogo modal para agregar gasto.
"""
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GObject

from cashflow.application.services import ExpenseService


class AddExpenseDialog(Adw.Dialog):
    """Diálogo para crear un nuevo gasto"""

    __gtype_name__ = "AddExpenseDialog"

    def __init__(self, service: ExpenseService):
        super().__init__(
            title="Nuevo gasto",
            content_width=350,
            content_height=280
        )

        self.service = service

        # Lista de categorías
        self.categories = [
            "Comida", "Transporte", "Servicios", "Hogar",
            "Salud", "Ocio", "General"
        ]

        # ToolbarView
        toolbar_view = Adw.ToolbarView()

        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(False)
        toolbar_view.add_top_bar(header)

        # Formulario
        form_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_start=16, margin_end=16, margin_top=8, margin_bottom=16,
            spacing=12
        )

        # Campo: Monto
        amount_row = Adw.EntryRow(title="Monto ($)", input_purpose=Gtk.InputPurpose.DIGITS)
        self.amount_entry = amount_row

        # Campo: Descripción
        desc_row = Adw.EntryRow(title="Descripción")
        self.desc_entry = desc_row

        # ✅ Campo: Categoría (usando Gtk.DropDown en vez de Adw.ComboRow)
        cat_label = Gtk.Label(label="Categoría", halign=Gtk.Align.START, css_classes=["caption"])

        # Crear StringList para las categorías
        self.category_model = Gtk.StringList.new(self.categories)

        # DropDown con modelo
        self.category_dropdown = Gtk.DropDown(
            model=self.category_model,
            selected=6  # "General" por defecto (índice 6)
        )
        self.category_dropdown.set_hexpand(True)

        cat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        cat_box.append(cat_label)
        cat_box.append(self.category_dropdown)

        form_box.append(amount_row)
        form_box.append(desc_row)
        form_box.append(cat_box)

        # Botones
        action_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6,
            halign=Gtk.Align.END,
            margin_top=8
        )

        cancel_btn = Gtk.Button(label="Cancelar")
        cancel_btn.connect("clicked", lambda _: self.close())

        add_btn = Gtk.Button(label="Agregar", css_classes=["suggested-action"])
        add_btn.connect("clicked", self.on_add_clicked)

        action_box.append(cancel_btn)
        action_box.append(add_btn)
        form_box.append(action_box)

        toolbar_view.set_content(form_box)
        self.set_child(toolbar_view)

        self.connect("show", lambda _: amount_row.grab_focus())

    def get_selected_category(self):
        """Obtener categoría seleccionada"""
        selected = self.category_dropdown.get_selected()
        if selected is not None:
            return self.categories[selected]
        return "General"

    def on_add_clicked(self, _button):
        """Validar y guardar gasto"""
        amount_text = self.amount_entry.get_text()
        description = self.desc_entry.get_text()
        category = self.get_selected_category()

        errors = []
        try:
            amount = float(amount_text)
            if amount <= 0:
                errors.append("El monto debe ser mayor a cero")
        except ValueError:
            errors.append("Monto inválido (usa números)")

        if not description.strip():
            errors.append("La descripción es requerida")

        if errors:
            error_dialog = Adw.AlertDialog(
                heading="Error de validación",
                body="\n".join(errors)
            )
            error_dialog.add_response("ok", "Entendido")
            error_dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
            error_dialog.present(self)
            return

        self.service.record_expense(amount, description.strip(), category)
        self.close()