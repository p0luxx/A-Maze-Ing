*This project has been created as part of the 42 curriculum by gorkgall, osuarez-.*

---

# 🌐 A-Maze-Ing — Generator, Solver & Visualizer

[Español](#-versión-en-español) | [English](#-english-version)

---

## 🇪🇸 Versión en Español

### 📋 Descripción
**A-Maze-Ing** es una suite completa en Python 3 para la generación procedimental, resolución, codificación hexadecimal y visualización interactiva de laberintos 2D. Diseñado bajo los estándares rigurosos del currículo de 42, el proyecto destaca por una separación arquitectónica estricta entre el motor principal reutilizable (`mazegen`) y la interfaz gráfica interactiva por terminal (`ui`).

Soporta dos modos de generación:
- **Modo Perfecto (`PERFECT=True`)**: Genera un laberinto en árbol de expansión (*spanning tree*) con exactamente **un único camino** entre entrada y salida (sin bucles).
- **Modo Jugable / Pac-Man (`PERFECT=False`)**: Genera un laberinto totalmente conectado y "trenzado" (*braided*) con **múltiples rutas independientes (bucles)**, esquinas y centro abiertos, y 0 calles sin salida reales, optimizado para dinámicas estilo arcade.

El generador integra la máscara del **patrón "42"** en el centro mediante bloques cerrados, garantizando la conectividad total y la validez de los caminos alrededor de la figura.

---

### 📂 Estructura del Proyecto (`tree`)

```text
amazing/
├── a_maze_ing.py               # Punto de entrada principal (CLI runner exigido por el subject)
├── cli.py                      # Orquestador del menú interactivo y bucle de control
├── config.txt                  # Archivo de configuración por defecto
├── __init__.py                 # Marcador de módulo raíz
├── LICENSE.md                  # Licencia del proyecto
├── Makefile                    # Automatización de tareas (install, run, debug, clean, lint)
├── pyproject.toml              # Configuración de empaquetado reutilizable (PEP 517/518)
├── README.md                   # Documentación oficial del proyecto
├── requirements.txt            # Dependencias del proyecto (pydantic, flake8, mypy, build)
├── mazegen/                    # 📦 LIBRERÍA CORE REUTILIZABLE (Backend)
│   ├── __init__.py             # Exporta la API pública: MazeGenerator
│   ├── encoder.py              # Exportación y serialización hexadecimal (Sección IV.5)
│   ├── generator.py            # Orquestador central de generación
│   ├── grid.py                 # Estructuras de datos: Grid, Cell y Walls (IntFlag)
│   ├── pattern42.py            # Máscara y validación del patrón "42"
│   ├── solver.py               # Algoritmo BFS para encontrar el camino más corto
│   └── strategies/             # Patrón Estrategia para algoritmos
│       ├── __init__.py
│       ├── algorithms.py       # IterativeBacktracker, RandomIterativeBacktracker y Prim
│       └── base.py             # Clase base abstracta GenerationStrategy
└── ui/                         # 🖥️ CAPA DE PRESENTACIÓN E INTERFAZ (Frontend)
    ├── __init__.py
    ├── config_loader.py        # Validación estricta con Pydantic v2
    └── renderer/               # Renderizado visual ANSI
        ├── __init__.py
        ├── ascii_renderer.py   # Renderizador ASCII interactivo con código ANSI
        └── base.py             # Clase base abstracta Renderer
```

---

### 🚀 Instrucciones de Uso

#### Requisitos Previos
- **Python 3.10+**
- **pip**

#### 1. Instalación
Instala las dependencias del proyecto (`pydantic`, `flake8`, `mypy`, `build`):
```bash
make install
```

#### 2. Ejecución
Para iniciar la aplicación interactiva:
```bash
make run
```
*O directamente con Python:*
```bash
python3 a_maze_ing.py config.txt
```

#### 3. Depuración y Calidad de Código
- **Depurador (`pdb`)**: `make debug`
- **Verificación de tipos y linter**: `make lint`
- **Verificación estricta (`mypy --strict`)**: `make lint-strict`
- **Limpieza de caché**: `make clean`

#### 4. Empaquetado y Reutilización de `mazegen`
Para compilar el paquete distribuible (`.whl` y `.tar.gz`):
```bash
python3 -m build
```
Para instalar el paquete empaquetado en cualquier proyecto:
```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

---

### ⚙️ Archivo de Configuración (`config.txt`)

Formato clave-valor (`KEY=VALUE`). Las líneas vacías o iniciadas por `#` se ignoran.

```ini
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
ALGORITHM=backtracker
```

---

### 🧠 Algoritmos de Generación

1. **Iterative Backtracker (DFS Clásico)**: Explora pasillos largos y serpenteantes usando una pila explícita. Ideal para `PERFECT=True`.
2. **Random Iterative Backtracker (DFS Aleatorio / Growing Tree)**: Selecciona elementos al azar de la pila activa, creando un laberinto más ramificado.
3. **Randomized Prim (Prim Aleatorizado)**: Crece de forma radial construyendo un árbol de expansión con ramificaciones cortas, ideal para trenzar en `PERFECT=False`.

---

### 👥 Equipo y Gestión del Proyecto

#### Roles y Responsabilidades
- **Gorka (`gorkgall`) — Tech Lead & Arquitecto de Software (Backend Lead)**:
  - Diseño de la arquitectura general del sistema y patrón de diseño decoupled.
  - Creación de las estructuras de datos fundamentales (`Grid`, `Cell`, `Walls` bitwise).
  - Implementación del algoritmo `IterativeBacktrackerStrategy` (DFS Clásico), el resolvedor `Solver` (BFS), `encoder.py` (serialización hexadecimal) y la lógica de enmascarado `pattern42`.
- **Oscar (`osuarez-`) — Frontend Lead & Responsable de Empaquetado**:
  - Diseño y desarrollo de la interfaz `ascii_renderer.py` y controles ANSI.
  - Implementación del cargador de configuración con `pydantic` (`config_loader.py`).
  - Configuración del sistema de empaquetado distribuible `pyproject.toml` y generación del `.whl`.
  - Desarrollo de los algoritmos **`RandomizedPrimStrategy` (Prim)** y **`RandomIterativeBacktrackerStrategy` (DFS Aleatorio)**.

#### Declaración de Uso de IA (Capítulo II)
Se utilizó Inteligencia Artificial de forma supervisada para la generación de docstrings (PEP 257), consulta de secuencias ANSI y asistencia en refactorizaciones de tipado estricto. Todo el código fue auditado y validado en equipo.

---
---

## 🇬🇧 English Version

### 📋 Description
**A-Maze-Ing** is a Python 3 suite for 2D maze generation, solving, encoding, and live terminal visualization. Built according to 42 curriculum standards, it features strict decoupling between the core engine (`mazegen`) and the terminal interface (`ui`).

Generates both **Perfect Mazes** (`PERFECT=True`, single path) and **Playable/Pac-Man Mazes** (`PERFECT=False`, multi-path braided loops with 0 dead-ends), including an embedded **"42" pattern** mask.

---

### 👥 Team & Management

#### Roles & Responsibilities
- **Gorka (`gorkgall`) — Tech Lead & Software Architect (Backend Lead)**:
  - System architecture design and decoupled component integration.
  - Core data structures (`Grid`, `Cell`, bitwise `Walls`).
  - `IterativeBacktrackerStrategy` (Classic DFS), `Solver` (BFS pathfinding), `encoder.py` (hexadecimal output format), and `pattern42` mask logic.
- **Oscar (`osuarez-`) — Frontend Lead & Packaging Manager**:
  - Terminal presentation layer (`ascii_renderer.py`) and interactive ANSI controls.
  - Configuration parsing and strict validation with Pydantic (`config_loader.py`).
  - Distribution setup via `pyproject.toml` and wheel generation.
  - Implementation of **`RandomizedPrimStrategy` (Prim)** and **`RandomIterativeBacktrackerStrategy` (Randomized DFS)** algorithms.

---

### 🚀 Quick Start
```bash
make install
make run
```
Build package:
```bash
python3 -m build
```
