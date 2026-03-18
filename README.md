# 💰 CashFlow

> Sistema de gestión de gastos personales con arquitectura limpia, CLI moderna y persistencia en SQLite.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Ruff-black)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/Tests-pytest-yellow.svg)](https://pytest.org)

---

## 📋 Tabla de Contenidos

- [✨ Características](#-características)
- [🛠️ Stack Tecnológico](#️-stack-tecnológico)
- [🏗️ Arquitectura](#️-arquitectura)
- [🚀 Instalación](#-instalación)
- [🎯 Uso](#-uso)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🧪 Testing](#-testing)
- [🔧 Desarrollo](#-desarrollo)
- [🤝 Contribuir](#-contribuir)
- [📄 Licencia](#-licencia)

---

## ✨ Características

- ✅ **Registro rápido de gastos**: CLI intuitiva con validación de datos
- ✅ **Categorización**: Organiza tus gastos por categorías personalizadas
- ✅ **Balance en tiempo real**: Visualiza tu flujo de caja al instante
- ✅ **Persistencia ligera**: SQLite, cero configuración, archivo único
- ✅ **Arquitectura escalable**: Clean Architecture + DDD listo para crecer
- ✅ **Tests automatizados**: Cobertura >90% con pytest
- ✅ **Entorno reproducible**: Hatch + Makefile para desarrollo consistente

---

## 🛠️ Stack Tecnológico

| Categoría | Herramienta | Propósito |
|-----------|-------------|-----------|
| **Lenguaje** | Python 3.10+ | Lógica de negocio y scripting |
| **Gestión de Proyecto** | [Hatch](https://hatch.pypa.io/) | Entornos virtuales, build, publishing |
| **CLI** | [Typer](https://typer.tiangolo.com/) | Interfaz de línea de comandos moderna |
| **UI Terminal** | [Rich](https://rich.readthedocs.io/) | Tablas, colores y formato en consola |
| **Validación** | [Pydantic](https://docs.pydantic.dev/) | Tipos, validación y settings |
| **Base de Datos** | SQLite (stdlib) | Persistencia ligera y portable |
| **Testing** | pytest + pytest-cov | Tests unitarios, integración y cobertura |
| **Linting/Format** | [Ruff](https://docs.astral.sh/ruff/) | Linter y formateador ultrarrápido |
| **Automatización** | Makefile | Comandos repetitivos simplificados |

---

## 🏗️ Arquitectura

El proyecto sigue **Clean Architecture** con principios de **Domain-Driven Design (DDD)** y **Screaming Architecture**:

```
src/cashflow/
├── domain/           # 🧠 Reglas de negocio puras (sin dependencias externas)
│   ├── models.py     # Entidades: Expense
│   └── repositories.py # Contratos: ExpenseRepository (ABC)
│
├── application/      # ⚙️ Casos de uso y servicios
│   └── services.py   # ExpenseService: orquesta dominio + infra
│
├── infrastructure/   # 🔌 Implementaciones técnicas
│   ├── database.py   # Conexión SQLite con contextmanager
│   └── repositories.py # SQLiteExpenseRepository: implementación real
│
└── interfaces/       # 🎭 Adaptadores de entrada (CLI, API, etc.)
    └── cli.py        # Typer: comandos 'add', 'summary'
```

### 🔑 Principios Clave

1. **Regla de Dependencia**: Las capas externas dependen de las internas, nunca al revés.
2. **Inversión de Dependencias**: El dominio define interfaces; la infraestructura las implementa.
3. **Entidades Anémicas (pragmático)**: Dataclasses + métodos de fábrica para simplicidad.
4. **Inyección de Dependencias**: Manual en la CLI, fácil de mockear en tests.

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.10 o superior
- [Hatch](https://hatch.pypa.io/latest/install/) instalado:
  ```bash
  pip install --user hatch
  ```

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/cashflow.git
cd cashflow

# 2. Instalar dependencias y entorno
make install

# 3. Inicializar la base de datos
make db-init

# 4. Verificar instalación
hatch run cashflow --help
```

> 💡 **Nota**: `make install` crea un entorno virtual aislado con Hatch y instala el paquete en modo editable (`-e`).

---

## 🎯 Uso

### Comandos Principales

#### ➕ Registrar un Gasto

```bash
hatch run cashflow add <monto> "<descripción>" --category "<categoría>"

# Ejemplos:
hatch run cashflow add 50.00 "Almuerzo" --category "Comida"
hatch run cashflow add 120.50 "Supermercado" --category "Hogar"
hatch run cashflow add 25 "Café"  # Categoría por defecto: "General"
```

#### 📊 Ver Resumen

```bash
hatch run cashflow summary
```

**Salida de ejemplo:**
```
Balance Total: $195.50
Movimientos: 3

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Fecha      ┃ Categoría   ┃ Descripción ┃ Monto  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 2026-03-17 │ Hogar       │ Supermercado│ $120.5 │
│ 2026-03-17 │ Comida      │ Almuerzo    │ $50.0  │
│ 2026-03-17 │ General     │ Café        │ $25.0  │
└────────────┴─────────────┴─────────────┴────────┘
```

#### ❓ Ayuda

```bash
# Ayuda general
hatch run cashflow --help

# Ayuda de un comando
hatch run cashflow add --help
```

### 🎨 Alias Recomendado (Opcional)

Agrega a tu `~/.bashrc` o `~/.zshrc`:

```bash
alias cf='hatch run cashflow'
```

Luego usa:
```bash
cf add 50 "Almuerzo" --category "Comida"
cf summary
```

---

## 📁 Estructura del Proyecto

```
cashflow/
├── src/
│   └── cashflow/               # Código fuente del paquete
│       ├── __init__.py
│       ├── domain/             # 🧠 Dominio puro
│       ├── application/        # ⚙️ Casos de uso
│       ├── infrastructure/     # 🔌 Implementaciones técnicas
│       └── interfaces/         # 🎭 CLI / Adaptadores
├── tests/                      # 🧪 Tests (espejo de src/)
│   ├── conftest.py            # Fixtures compartidos
│   ├── unit/                  # Tests unitarios
│   └── integration/           # Tests de integración
├── scripts/                    # 🛠️ Scripts auxiliares (opcional)
├── pyproject.toml             # 📦 Configuración de Hatch y dependencias
├── Makefile                   # ⚡ Comandos de automatización
├── README.md                  # 📄 Este archivo
└── cashflow.db                # 🗄️ Base de datos SQLite (generado)
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
make test

# Con reporte de cobertura
make test-cov

# Tests específicos
hatch run pytest tests/unit/domain/ -v

# Modo interactivo con pdb en fallos
hatch run pytest --pdb -x
```

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures: test_db, expense_repo, sample_expense
├── unit/
│   ├── domain/              # Tests de entidades y contratos (sin DB)
│   ├── application/         # Tests de servicios (mock de repo)
│   └── infrastructure/      # Tests de DB y repositorios (DB en memoria)
└── integration/
    └── test_cli.py          # Tests end-to-end de la CLI
```

### Cobertura Esperada

```
---------- coverage: platform linux, python 3.14.3-final-0 -----------
Name                                      Stmts   Miss  Cover
-------------------------------------------------------------
src/cashflow/domain/models.py                15      0   100%
src/cashflow/domain/repositories.py           4      0   100%
src/cashflow/application/services.py         12      0   100%
src/cashflow/infrastructure/database.py      18      0   100%
src/cashflow/infrastructure/repositories.py  25      0   100%
src/cashflow/interfaces/cli.py               32      2    94%
-------------------------------------------------------------
TOTAL                                       106      2    98%
```

---

## 🔧 Desarrollo

### Comandos Útiles del Makefile

```bash
make install      # Crear entorno e instalar dependencias
make test         # Ejecutar tests
make test-cov     # Tests con cobertura
make lint         # Verificar estilo con Ruff
make fmt          # Formatear código con Ruff
make run          # Ver ayuda de la CLI
make shell        # Entrar al shell del entorno virtual
make db-init      # Inicializar/actualizar esquema de DB
make clean        # Limpiar archivos temporales y caché
```

### Flujo de Trabajo Recomendado

```bash
# 1. Crear una nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# 2. Escribir tests primero (TDD opcional pero recomendado)
#    Editar: tests/unit/... o tests/integration/...

# 3. Implementar la lógica
#    Editar: src/cashflow/...

# 4. Verificar que todo pasa
make test && make lint

# 5. Formatear y confirmar
make fmt
git add .
git commit -m "feat: descripción del cambio"
```

### Depuración

```bash
# Entrar al entorno virtual interactivo
make shell

# Dentro del shell:
(cashflow) $ python
>>> from cashflow.infrastructure.database import init_db
>>> init_db()
>>> # ... depurar interactivamente
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guidelines

- ✅ Sigue el estilo de código con `make lint` y `make fmt`
- ✅ Añade tests para nuevas funcionalidades
- ✅ Actualiza la documentación si es necesario
- ✅ Usa commits semánticos: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

---

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

```
MIT License

Copyright (c) 2026 Gabriel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Agradecimientos

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Robert C. Martin
- [Domain-Driven Design](https://domainlanguage.com/ddd/) - Eric Evans
- [Hatch](https://hatch.pypa.io/) - Ofek Lev & contribuidores
- [Typer](https://typer.tiangolo.com/) - Sebastián Ramírez
- [Rich](https://rich.readthedocs.io/) - Will McGugan

---

> 💡 **Tip**: Este proyecto está diseñado para ser **tu punto de partida**. ¿Necesitas ingresos además de gastos? ¿Exportación a CSV? ¿API REST? La arquitectura está lista para escalar. ¡Hazlo tuyo! 🚀

---

### 📌 Próximas Funcionalidades (Roadmap)

- [ ] 📈 Gráficos de gastos por categoría (con `rich.plot` o export a matplotlib)
- [ ] 📤 Exportar reportes a CSV/Excel
- [ ] 🔍 Filtros por fecha y categoría en `summary`
- [ ] 🗑️ Comando `delete` para eliminar gastos por ID
- [ ] 🔄 Comando `edit` para modificar gastos existentes
- [ ] 📱 API REST con FastAPI (opcional, misma arquitectura)
