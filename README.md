# A-Maze-ing — Plan de Proyecto
**Equipo:** Gorka (backend / core de generación) · Oscar (frontend / visualización y CLI)
**Duración:** 3 semanas · 15 días · 8h/día
**Nota sobre roles:** la división backend/frontend es orientativa, no una frontera rígida. Ambos deben entender el proyecto completo — la división solo define quién *lidera* cada pieza primero.

---

## 1. Estructura del proyecto (árbol de archivos)

```
a-maze-ing/
│
├── a_maze_ing.py                     # Punto de entrada obligatorio (nombre fijo)
├── config.txt                        # Config por defecto (obligatorio en el repo)
│
├── Makefile
├── LICENSE.md
├── README.md
├── .gitignore
├── pyproject.toml                    # Metadatos + build del paquete mazegen
├── mazegen-1.0.0-py3-none-any.whl    # Paquete construido, en la raíz (obligatorio)
│
├── mazegen/                          # ── PAQUETE REUTILIZABLE (Gorka) ──
│   │                                 #    Sin prints, sin input(), sin nada de UI.
│   │                                 #    Debe poder importarse sin ninguna otra
│   │                                 #    dependencia del proyecto.
│   │
│   ├── __init__.py                   # Expone la API pública del paquete:
│   │                                 #   from mazegen import MazeGenerator
│   │                                 #   Aquí se decide qué es "público" y qué es
│   │                                 #   detalle interno (no todo lo de dentro
│   │                                 #   tiene que exportarse aquí).
│   │
│   ├── grid.py                       # Cell, Wall (IntFlag), Grid/Maze
│   │                                 # La estructura de datos base. TODO lo demás
│   │                                 # depende de esto, así que se diseña primero
│   │                                 # y se acuerda entre los dos.
│   │
│   ├── generator.py                  # class MazeGenerator (orquestador principal)
│   │                                 # Es la clase que pide el capítulo VI.
│   │                                 # No genera nada por sí misma: coordina
│   │                                 # strategy + modes + pattern42.
│   │
│   ├── strategies/                   # Strategy Pattern — algoritmos intercambiables
│   │   ├── __init__.py               # Puede exponer un registro/factory de
│   │   │                             # estrategias disponibles (ver nota Factory
│   │   │                             # más abajo)
│   │   ├── base.py                   # GenerationStrategy (ABC o Protocol)
│   │   ├── backtracker.py            # RecursiveBacktrackerStrategy
│   │   └── prim.py                   # RandomizedPrimStrategy
│   │
│   ├── modes/                        # Reglas de "perfecto" vs "jugable"
│   │   ├── __init__.py
│   │   ├── perfect.py                # No hace casi nada extra: el árbol de
│   │   │                             # expansión YA es un laberinto perfecto
│   │   └── playable.py               # Post-procesado: crear loops, abrir
│   │                                 # esquinas/centro, controlar dead-ends
│   │
│   ├── pattern42.py                  # Máscara de celdas reservadas para el "42"
│   │
│   ├── solver.py                     # BFS: camino más corto entre entry y exit
│   │
│   ├── encoder.py                    # Grid <-> hexadecimal (lectura y escritura
│   │                                 # del archivo de salida)
│   │
│   └── exceptions.py                 # Excepciones propias del dominio
│                                     # (InvalidMazeError, UnreachableExitError...)
│
├── ui/                                # ── CAPA DE PRESENTACIÓN (Oscar) ──
│   │                                  #    Consume mazegen como si fuera una
│   │                                  #    librería externa ya instalada.
│   │
│   ├── __init__.py
│   ├── config_loader.py              # Parseo de config.txt (usa pydantic),
│   │                                 # validación, mensajes de error claros
│   ├── cli.py                        # Orquesta todo: lee config -> instancia
│   │                                 # MazeGenerator -> instancia Renderer ->
│   │                                 # conecta ambos -> maneja el menú
│   │
│   └── renderer/
│       ├── __init__.py
│       ├── base.py                   # Renderer (ABC): interfaz abstracta
│       └── ascii_renderer.py         # Implementación concreta en terminal
│
├── tests/                            # No se entrega/califica directamente,
│   │                                 # pero es vuestra red de seguridad
│   ├── test_grid.py
│   ├── test_strategies.py
│   ├── test_modes.py
│   ├── test_pattern42.py
│   ├── test_solver.py
│   ├── test_encoder.py
│   └── test_config_loader.py
│
└── scripts/
    └── maze_analyzer.py               # El que os da la escuela, para validar
                                        # vuestros archivos de salida
```

### Sobre los `__init__.py`: qué va en cada uno

Un `__init__.py` en Python tiene un propósito muy concreto: define **qué es visible desde fuera** cuando alguien hace `import` de esa carpeta. No debe contener lógica de negocio, solo "reexportar" lo que quieres que sea la fachada pública.

- **`mazegen/__init__.py`**: debe contener básicamente `from .generator import MazeGenerator` (y quizás las excepciones públicas). Así, quien instale vuestro paquete pip solo necesita escribir `from mazegen import MazeGenerator`, sin saber que por dentro existe `generator.py`, `grid.py`, etc. Esto es literalmente lo que hace que sea "una librería" y no "una carpeta de scripts sueltos".
- **`mazegen/strategies/__init__.py`**: aquí es donde podéis investigar si os interesa montar un pequeño **Factory** (mencionaste que ya conoces el patrón): un diccionario o función que, dado un nombre de string (`"backtracker"`, `"prim"`), devuelva la clase/instancia correcta. Esto es opcional pero conecta muy bien con lo que pide el config (`ALGORITHM=prim`, por ejemplo, como clave adicional que sugiere el propio enunciado).
- **`ui/__init__.py`** y **`ui/renderer/__init__.py`**: mucho más simples, casi vacíos o con un `from .ascii_renderer import AsciiRenderer` de conveniencia.
- **`tests/`**: normalmente no necesita `__init__.py` si usáis pytest con configuración moderna (pytest descubre los tests solo), pero investigadlo al montar el proyecto — depende de cómo configuréis las rutas de importación.

### Regla de dependencia (la más importante de todo el árbol)

**`mazegen/` no debe importar nunca nada de `ui/`.** La flecha de dependencia va en un solo sentido: `ui/` → `mazegen/`. Si en algún momento sentís la tentación de que el generador "sepa" algo sobre cómo se muestra (por ejemplo, para imprimir un mensaje), es una señal de que ese código está en la carpeta equivocada. Esta regla es la que os permite construir el `.whl` sin arrastrar nada de la interfaz, y es lo que vais a poder demostrar en la defensa.

---

## 2. Tablero de tareas

Formato sugerido para cada ticket cuando lo paséis a GitHub Projects/Issues: **Título / Descripción corta / Criterio de "Hecho" / Depende de**.

### 🟦 GORKA — Backend / mazegen

#### Semana 1

**[G1] Diseñar `Grid`, `Cell` y el sistema de muros — 🤝 CONJUNTO con Oscar**
- 📄 Archivo(s): `mazegen/grid.py`
- Qué investigar: `enum.IntFlag`, `dataclasses`, cómo modelar una cuadrícula 2D (lista de listas vs. dict con tuplas como clave).
- Cómo afrontarlo: antes de escribir código, dibujad en papel una cuadrícula pequeña (3x3) y decidid a mano cómo representaríais cada celda y cada muro compartido. Si no podéis explicarlo en papel, tampoco lo vais a poder programar bien.
- Criterio de hecho: tenéis una clase `Cell` que puede responder "¿tengo muro al norte?" y una `Grid` que puede acceder a `grid[x, y]`.
- Conecta con: literalmente todo lo demás depende de esto. Es el ticket más importante del proyecto.

**[G2] Diseñar la interfaz `GenerationStrategy` — 🤝 CONJUNTO con Oscar**
- 📄 Archivo(s): `mazegen/strategies/base.py`
- Qué investigar: `abc.ABC` / `Protocol`, generadores y `yield` (crítico: la estrategia debe poder "ceder" estados intermedios paso a paso, no solo devolver el resultado final — esto es lo que luego permite la animación sin duplicar código).
- Cómo afrontarlo: escribid primero la *firma* del método (qué recibe, qué produce en cada `yield`) antes de implementar ningún algoritmo real. Es un contrato, como una API.
- Criterio de hecho: existe `strategies/base.py` con la clase abstracta y está documentada con docstrings de qué se espera de cualquier implementación futura.
- Conecta con: Oscar necesita saber esta interfaz para poder programar el modo animado sin esperar a que el algoritmo esté terminado.

**[G3] Implementar `RecursiveBacktrackerStrategy`**
- 📄 Archivo(s): `mazegen/strategies/backtracker.py` (implementa la interfaz de `base.py`)
- Qué investigar: el algoritmo recursive backtracker (concepto, no pseudocódigo copiado — mirad varias fuentes y quedaos con el entendimiento, no con una implementación concreta).
- Cómo afrontarlo: primero hacedlo funcionar generando un laberinto perfecto sin preocuparos de reproducibilidad ni seed. Una vez funciona, añadid el `random.seed()`.
- Criterio de hecho: genera laberintos perfectos válidos (sin ciclos, todo conectado) para varios tamaños, y con la misma seed siempre da el mismo resultado.
- Conecta con: es el primer algoritmo real que Oscar puede usar para probar su renderer.

**[G4] Implementar `encoder.py`**
- 📄 Archivo(s): `mazegen/encoder.py`
- Qué investigar: operaciones a nivel de bit (`&`, `|`, formato hexadecimal en Python con `hex()` / f-strings `{:x}`).
- Cómo afrontarlo: escribid primero los tests con casos conocidos a mano (una celda con muros N y E cerrados debería dar tal dígito) antes de implementar — así sabéis exactamente qué tiene que devolver.
- Criterio de hecho: pasa el `maze_analyzer.py` sin errores de coherencia.
- Conecta con: Oscar lo necesita indirectamente porque `cli.py` debe llamarlo para escribir el archivo de salida.

**[G5] Implementar `solver.py` (BFS)**
- 📄 Archivo(s): `mazegen/solver.py`
- Qué investigar: BFS con una cola (`collections.deque`), cómo reconstruir el camino desde el resultado del BFS.
- Cómo afrontarlo: es un algoritmo bastante estándar — buscad el concepto general de "BFS shortest path en grid con obstáculos" (los muros son vuestros obstáculos), no una solución específica de laberintos.
- Criterio de hecho: devuelve la secuencia correcta de letras N/E/S/W para varios laberintos de prueba.
- Conecta con: `encoder.py` (necesita el camino para escribirlo en el archivo) y con Oscar (necesita el camino para dibujar la ruta resaltada).

#### Semana 2

**[G6] Implementar `pattern42.py`**
- 📄 Archivo(s): `mazegen/pattern42.py` (se invoca desde `mazegen/generator.py`)
- Qué investigar: cómo definir una máscara de coordenadas fijas (una matriz booleana o un `set` de tuplas `(x,y)`) que representen el dibujo del "42", y cómo hacer que la generación respete esas celdas como "completamente cerradas".
- Cómo afrontarlo: primero diseñad el patrón como una matriz simple en papel/spreadsheet para un tamaño de referencia (ej. 20x15), luego programad cómo escalarlo o centrarlo según el tamaño real del laberinto pedido en config.
- Criterio de hecho: el patrón se ve reconocible en la salida ASCII para varios tamaños razonables, y el programa muestra el mensaje de error correcto cuando el tamaño es demasiado pequeño.
- Conecta con: debe aplicarse *antes* de correr la estrategia de generación (como restricción), así que toca `generator.py`.

**[G7] Implementar `modes/playable.py`**
- 📄 Archivo(s): `mazegen/modes/playable.py` (y probablemente `mazegen/modes/perfect.py` en paralelo, para dejar simétrico el otro modo)
- Qué investigar: técnicas de "braiding" (romper muros de un árbol de expansión para crear loops controlados), cómo detectar dead-ends en una grid, cómo verificar conectividad (podéis reutilizar ideas de BFS/DFS que ya usasteis en el solver).
- Cómo afrontarlo — el más delicado del proyecto: dividid el problema en sub-requisitos y resolvedlos uno a uno, verificando cada uno con tests antes de pasar al siguiente: (1) esquinas y centro abiertos, (2) al menos 2 rutas independientes, (3) sin áreas 3x3 abiertas, (4) control de dead-ends. No intentéis resolver los cuatro a la vez.
- Criterio de hecho: pasa `maze_analyzer.py` en modo "playable" de forma consistente en varios tamaños y seeds.
- Conecta con: Oscar puede empezar a probar su interfaz "regenerar" con este modo en cuanto esté listo.

**[G8] Implementar `RandomizedPrimStrategy`**
- 📄 Archivo(s): `mazegen/strategies/prim.py` + actualizar `mazegen/strategies/__init__.py` (registro/factory)
- Qué investigar: el algoritmo de Prim aleatorizado para laberintos (concepto).
- Cómo afrontarlo: dado que ya existe `base.py` y `backtracker.py` como referencia de "cómo se implementa una strategy en este proyecto", usad ese patrón ya establecido — este ticket es buen candidato para que Oscar lo intente con tu apoyo cercano (ver sección de Oscar).
- Criterio de hecho: mismo criterio que G3, pero con este algoritmo.
- Conecta con: `strategies/__init__.py` (registro/factory de estrategias) y con la CLI de Oscar (selector de algoritmo).

#### Semana 3

**[G9] Excepciones propias y manejo de errores del dominio**
- 📄 Archivo(s): `mazegen/exceptions.py` (y revisar/tocar `mazegen/generator.py`, `mazegen/grid.py`, etc. para que las lancen donde corresponda)
- Qué investigar: buenas prácticas de excepciones custom en Python (heredar de `Exception`, jerarquías de excepciones).
- Criterio de hecho: `mazegen/` nunca deja escapar una excepción "cruda" de Python sin contexto — todo pasa por excepciones propias que la capa `ui/` puede capturar y mostrar con un mensaje claro.

**[G10] Tests completos + cobertura de casos límite**
- 📄 Archivo(s): `tests/test_grid.py`, `tests/test_strategies.py`, `tests/test_modes.py`, `tests/test_pattern42.py`, `tests/test_solver.py`, `tests/test_encoder.py`
- Qué investigar: qué son los "edge cases" típicos aquí (laberinto 1x1, entry=exit, coordenadas fuera de rango, tamaño insuficiente para el 42).
- Criterio de hecho: `pytest` corre en verde para todos los módulos de `mazegen/`.

**[G11] Empaquetado pip del módulo `mazegen`**
- 📄 Archivo(s): `pyproject.toml` (raíz del repo) → genera `mazegen-1.0.0-py3-none-any.whl` (raíz del repo)
- Qué investigar: `pyproject.toml`, `python -m build`, diferencia `.whl`/`.tar.gz`, cómo probar la instalación en un venv limpio.
- Criterio de hecho: podéis hacer `pip install mazegen-1.0.0-py3-none-any.whl` en un entorno virtual nuevo y ejecutar `from mazegen import MazeGenerator` sin errores.

---

### 🟩 OSCAR — Frontend / ui

#### Semana 1

**[O1] Investigación de fundamentos + acompañar diseño conjunto (G1, G2)**
- 📄 Archivo(s): ninguno propio todavía — participas en `mazegen/grid.py` y `mazegen/strategies/base.py` como revisor/co-diseñador
- Qué investigar en paralelo mientras Gorka avanza en profundidad en teoría de grafos: type hints, dataclasses, clases abstractas (`abc.ABC`), y específicamente para tu parte: **códigos de escape ANSI** para colores en terminal, y técnicas de limpiar pantalla (`os.system`, o investigar `curses` como alternativa más potente si os apetece explorarlo).
- Cómo afrontarlo para no perder tiempo: no intentes entender el algoritmo de generación a fondo todavía — de momento solo necesitas entender *la forma* de los datos que vas a recibir (una grid con celdas que tienen muros), no cómo se generan.
- Conecta con: participas activamente en G1/G2 porque tú vas a *consumir* esa interfaz constantemente — tu input en el diseño es valioso precisamente porque ves el problema desde el lado de "qué necesito para dibujar esto fácilmente".

**[O2] Diseñar la interfaz `Renderer` (abstracta)**
- 📄 Archivo(s): `ui/renderer/base.py`
- Qué investigar: cómo se define una interfaz mínima en Python con `abc.ABC` (mismo concepto que G2, así que es buen momento para consolidarlo).
- Cómo afrontarlo: pensad en los verbos que necesitáis: `setup()`, `draw(grid, entry, exit, path=None)`, algo para manejar eventos de menú. No diseñéis de más — solo lo que el capítulo V pide explícitamente (regenerar, mostrar/ocultar camino, cambiar colores).
- Criterio de hecho: `ui/renderer/base.py` existe con la interfaz documentada.
- Conecta con: define el contrato que `ascii_renderer.py` va a implementar después.

**[O3] Primer renderer ASCII mínimo (sin interacción todavía)**
- 📄 Archivo(s): `ui/renderer/ascii_renderer.py` (implementa `ui/renderer/base.py`)
- Qué investigar: cómo combinar caracteres (`-`, `|`, `+`, o los de línea Unicode `─│┌┐└┘`) para representar una cuadrícula con muros según los datos de cada celda.
- Cómo afrontarlo: no esperéis a que el backend esté terminado. En cuanto Gorka tenga aunque sea una `Grid` construida "a mano" (sin generación real, solo para probar), podéis empezar a dibujarla — desacoplad vuestro trabajo de si el algoritmo real ya funciona o no.
- Criterio de hecho: podéis pasar una `Grid` cualquiera y se ve una representación ASCII reconocible en terminal.
- Conecta con: en cuanto G3 (backtracker) esté listo, sustituís la grid "hecha a mano" por una real generada.

#### Semana 2

**[O4] `config_loader.py` con pydantic**
- 📄 Archivo(s): `ui/config_loader.py`
- Qué investigar: modelos básicos de pydantic (`BaseModel`, validadores, tipos con restricciones), y cómo parsear un archivo de texto simple `CLAVE=VALOR` a un diccionario antes de pasarlo al modelo.
- Cómo afrontarlo: separad el problema en dos pasos claros: (1) leer el archivo y convertirlo en un diccionario simple ignorando comentarios, (2) validar ese diccionario con un modelo pydantic que dé errores claros si falta una clave obligatoria o el tipo no es correcto.
- Criterio de hecho: mensajes de error entendibles para casos como archivo inexistente, clave faltante, coordenadas fuera de rango, valores no numéricos donde se esperan números.
- Conecta con: `cli.py` lo usa como primer paso de todo el flujo del programa.

**[O5] Interacciones del renderer: mostrar/ocultar camino, cambiar colores**
- 📄 Archivo(s): `ui/renderer/ascii_renderer.py` (y probablemente `ui/cli.py` para el bucle de menú)
- Qué investigar: cómo mantener un pequeño "estado" del programa (¿está visible el camino o no?, ¿qué color toca ahora?) entre iteraciones del menú.
- Cómo afrontarlo: empezad con un menú basado en `input()` simple con opciones numeradas — no necesitáis nada más sofisticado, el enunciado no pide tiempo real, solo que las funciones existan.
- Criterio de hecho: se cumplen las 3 interacciones mínimas del capítulo V.
- Conecta con: usa `solver.py` de Gorka (G5) para el camino, y los datos de `Grid` para el resto.

**[O6] Segunda strategy (Prim) — con apoyo cercano de Gorka**
- 📄 Archivo(s): `mazegen/strategies/prim.py` (mismo archivo que G8 — es el mismo ticket, ejecutado en conjunto)
- Este ticket, como hablamos, es una buena oportunidad de que Oscar toque directamente el core del backend con guía, replicando el patrón ya establecido por `backtracker.py`. Ver ticket G8 — se recomienda hacerlo en sesión conjunta o con check-ins más frecuentes ese día concreto.

#### Semana 3

**[O7] `cli.py` — integración completa del flujo**
- 📄 Archivo(s): `ui/cli.py` + `a_maze_ing.py` (punto de entrada raíz, que probablemente solo llama a `ui/cli.py`)
- Qué investigar: nada nuevo técnicamente, es sobre todo orquestación de piezas ya existentes.
- Cómo afrontarlo: dibujad primero el flujo como un diagrama simple (leer config → construir generator → generar → escribir archivo → mostrar → menú interactivo) antes de escribir el código, para no perder piezas.
- Criterio de hecho: `python3 a_maze_ing.py config.txt` funciona de punta a punta.
- Conecta con: es el punto donde backend y frontend se encuentran de verdad — buen ticket para hacer en pair programming los dos juntos.

**[O8] Animación de generación en vivo (bonus)**
- 📄 Archivo(s): `ui/renderer/ascii_renderer.py` (nuevo método tipo `draw_step`) + `ui/cli.py` (para invocarlo iterando la strategy)
- Qué investigar: cómo consumir un generador Python (`for state in strategy.generate(...): renderer.draw(state)`) con una pequeña pausa (`time.sleep()`) entre pasos.
- Cómo afrontarlo: esto debería ser relativamente directo *si* la interfaz `GenerationStrategy` (G2) se diseñó bien desde el principio con `yield` — si os cuesta mucho implementarlo, es una señal de que conviene revisar esa interfaz, no forzar el renderer.
- Criterio de hecho: se ve el laberinto "construirse" celda a celda en terminal.

**[O9] Tests de `config_loader.py` y del renderer**
- 📄 Archivo(s): `tests/test_config_loader.py` (y podéis añadir un `tests/test_renderer.py` si os interesa, no estaba en el árbol original pero encaja)
- Igual que G10 pero para vuestra parte — no dejéis los tests solo para el backend.

**[O10] Makefile, `.gitignore`, LICENSE.md**
- 📄 Archivo(s): `Makefile`, `.gitignore`, `LICENSE.md` (todos en la raíz del repo)
- Qué investigar: sintaxis básica de Makefile (targets, dependencias entre ellos), diferencia entre licencias permisivas (MIT) y copyleft (GPL) para elegir con criterio.
- Criterio de hecho: los 6 comandos del capítulo III.2 funcionan.

---

### 🟨 TICKETS CONJUNTOS (ambos, cualquier semana según avance)

- **[C1] README.md** — 📄 Archivo(s): `README.md` (raíz). Id ealmente ir rellenándolo progresivamente, no todo al final. Cada uno documenta su propia parte a medida que la termina.
- **[C2] Sesiones de peer learning / live coding** — 📄 Archivo(s): ninguno propio, se trabaja sobre cualquier archivo ya existente del repo, rotando. Cadencia ya definida (check-ins cortos 2-3x/semana + sesión larga semanal).
- **[C3] Integración final y pulido de mypy/flake8** — 📄 Archivo(s): todo el repo (barrido general, sin archivo fijo). Pasada final ya con todas las piezas encajadas.
- **[C4] Preparación de la defensa** — 📄 Archivo(s): ninguno (es repaso oral/conceptual sobre todo el repo). Repasad juntos cómo explicaríais cualquier parte del proyecto, incluida la del otro, para estar cubiertos ante el capítulo IX.

---

## 3. Mapa de dependencias entre tareas (quién bloquea a quién)

```
G1 (Grid/Cell) ──┬──> G3 (Backtracker) ──> O3 (Renderer ASCII básico)
                 │                     └─> G5 (Solver BFS) ──> O5 (Mostrar/ocultar camino)
                 │
                 └──> G4 (Encoder) ──> O7 (CLI: escribir archivo de salida)

G2 (Strategy interface) ──┬──> G3, G8 (implementaciones concretas)
                          └──> O8 (Animación, usa el mismo yield)

O2 (Renderer interface) ──> O3 (implementación ASCII)

O4 (Config loader) ──> O7 (CLI)

G6 (Pattern42) + G7 (Modo playable) ──> afectan a G1/generator.py,
                                        pero no bloquean a Oscar directamente
                                        (Oscar sigue dibujando lo que reciba)

TODO converge en: O7 (cli.py) — el punto de integración real del proyecto
```

**Lectura práctica de este mapa:** los tickets G1 y G2 son los únicos que de verdad *bloquean* el trabajo de Oscar si no están listos — por eso van primero y en conjunto. Una vez existen (aunque sea en versión mínima/borrador), Oscar puede avanzar en paralelo casi sin esperar a Gorka, incluso simulando datos de prueba a mano mientras el backend real se termina.

---

## 4. Cómo evitar perder tiempo (resumen de criterios prácticos)

- **No investiguéis más de lo necesario antes de programar.** El objetivo de la fase de investigación no es "dominar el tema", es "entender lo suficiente para empezar a experimentar y equivocarse rápido". Si lleváis más de 2-3 horas leyendo sobre un algoritmo sin haber escrito ni una línea, es momento de empezar a probar aunque no lo tengáis 100% claro.
- **Construid de lo simple a lo complejo dentro de cada ticket.** Ejemplo: primero un laberinto perfecto sin seed, luego con seed; primero el renderer sin colores, luego con colores.
- **No os bloqueéis esperando al otro si no hace falta.** Usad datos "de mentira" (una grid construida a mano) para no depender de que la pieza real del compañero esté terminada.
- **Corred `maze_analyzer.py` constantemente**, no solo al final — es vuestra forma más rápida de saber si algo está mal sin tener que depurarlo vosotros mismos desde cero.
- **Documentad decisiones en el momento, no al final** (comentario corto en cada ticket cerrado) — os ahorra reconstruir el README bajo presión en la última semana.
