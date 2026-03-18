.PHONY: install test test-cov lint fmt run shell db-init clean

install:
	hatch env create
	hatch run pip install -e .

test:
	hatch run test

test-cov:
	hatch run test-cov

lint:
	hatch run lint

fmt:
	hatch run fmt

run:
	hatch run cashflow --help

shell:
	hatch shell

db-init:
	hatch run python -c "from cashflow.infrastructure.database import init_db; init_db()"

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	rm -rf cashflow.db


# === Comandos GUI ===

# Instalar dependencias GUI (requiere sistema con GTK 4 + libadwaita)
install-gui:
	hatch run pip install '.[gui]'

# Ejecutar interfaz gráfica
gui:
	hatch run cashflow gui

# Ejecutar GUI con variables de entorno para depuración
gui-debug:
	GTK_DEBUG=interactive hatch run cashflow gui

# Verificar dependencias del sistema para GUI
check-gui-deps:
	@python -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1'); print('✅ GTK 4 + libadwaita disponibles')" 2>/dev/null || echo "❌ GTK 4 o libadwaita no encontrados"