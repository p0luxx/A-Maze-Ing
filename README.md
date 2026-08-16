# A-Maze-ing — Plan de Proyecto
**Equipo:** Gorka (backend / core de generación) · Oscar (frontend / visualización y CLI)
**Duración:** 3 semanas · 15 días · 8h/día

Dividimos el proyecto en backend y frontend, pero lo definimos de forma flexible: al final los dos vamos a tocar todo el proyecto. La división solo marca quién lidera cada pieza primero, no una frontera cerrada.

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
├── mazegen/                          # ── PAQUETE REUTILIZABLE (lidero yo, Gorka) ──
│   │                                 #    Sin prints, sin input(), sin nada de UI.
│   │                                 #    Tiene que poder importarse sin ninguna otra
│   │                                 #    dependencia del proyecto.
│   │
│   ├── __init__.py                   # Expone la API pública del paquete:
│   │                                 #   from mazegen import MazeGenerator
│   │                                 #   Aquí decidimos qué es "público" y qué es
│   │                                 #   detalle interno (no todo lo de dentro
│   │                                 #   tiene que exportarse aquí).
│   │
│   ├── grid.py                       # Cell, Wall (IntFlag), Grid/Maze
│   │                                 # La estructura de datos base. Todo lo demás
│   │                                 # depende de esto, así que la diseñamos primero
│   │                                 # y la acordamos entre los dos.
│   │
│   ├── generator.py                  # class MazeGenerator (orquestador principal)
│   │                                 # Es la clase que pide el capítulo VI.
│   │                                 # No genera nada por sí misma: coordina
│   │                                 # strategy + modes + pattern42.
│   │
│   ├── strategies/                   # Strategy Pattern — algoritmos intercambiables
│   │   ├── __init__.py               # Puede exponer un registro/factory de
│   │   │                             # estrategias disponibles
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
├── ui/                                # ── CAPA DE PRESENTACIÓN (lidera Oscar) ──
│   │                                  #    Consume mazegen como si fuera una
│   │                                  #    librería externa ya instalada.
│   │
│   ├── __init__.py
│   ├── config_loader.py              # Parseo de config.txt (con pydantic),
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
│   │                                 # pero es nuestra red de seguridad
│   ├── test_grid.py
│   ├── test_strategies.py
│   ├── test_modes.py
│   ├── test_pattern42.py
│   ├── test_solver.py
│   ├── test_encoder.py
│   └── test_config_loader.py
│
└── scripts/
    └── maze_analyzer.py               # El que nos da la escuela, para validar
                                        # nuestros archivos de salida
```

### Sobre los `__init__.py`: qué va en cada uno

Un `__init__.py` define qué es visible desde fuera cuando alguien hace `import` de esa carpeta. No debe contener lógica de negocio, solo "reexportar" lo que queremos que sea la fachada pública.

- **`mazegen/__init__.py`**: va a contener básicamente `from .generator import MazeGenerator` (y quizás las excepciones públicas). Así, quien instale nuestro paquete pip solo necesita escribir `from mazegen import MazeGenerator`, sin saber que por dentro existe `generator.py`, `grid.py`, etc. Esto es lo que hace que sea "una librería" y no "una carpeta de scripts sueltos".
- **`mazegen/strategies/__init__.py`**: aquí es donde vamos a valorar si montamos un pequeño Factory: un diccionario o función que, dado un nombre de string (`"backtracker"`, `"prim"`), devuelva la clase/instancia correcta. Es opcional pero conecta bien con lo que pide el config (`ALGORITHM=prim`, por ejemplo, como clave adicional que sugiere el propio enunciado).
- **`ui/__init__.py`** y **`ui/renderer/__init__.py`**: mucho más simples, casi vacíos o con un `from .ascii_renderer import AsciiRenderer` de conveniencia.
- **`tests/`**: normalmente no necesita `__init__.py` si usamos pytest con configuración moderna (pytest descubre los tests solo), pero lo comprobaremos al montar el proyecto — depende de cómo configuremos las rutas de importación.

### Regla de dependencia (la más importante de todo el árbol)

`mazegen/` no puede importar nunca nada de `ui/`. La flecha de dependencia va en un solo sentido: `ui/` → `mazegen/`. Si en algún momento sentimos la tentación de que el generador "sepa" algo sobre cómo se muestra (por ejemplo, para imprimir un mensaje), es una señal de que ese código está en la carpeta equivocada. Esta regla es la que nos permite construir el `.whl` sin arrastrar nada de la interfaz, y lo que vamos a poder demostrar en la defensa.

---

## 2. Tablero de tareas

Formato para cada ticket en GitHub Projects/Issues:

### 🟦 GORKA — Backend / mazegen

#### Semana 1

**[G1] Diseñar `Grid`, `Cell` y el sistema de muros — 🤝 CONJUNTO con Oscar**
- 📄 Archivo(s): `mazegen/grid.py`
- Qué investigar: `enum.IntFlag`, `dataclasses`, cómo modelar una cuadrícula 2D (lista de listas vs. dict con tuplas como clave).
- Cómo lo vamos a afrontar: antes de escribir código, vamos a dibujar en papel una cuadrícula pequeña (3x3) y decidir a mano cómo representamos cada celda y cada muro compartido. Si no lo podemos explicar en papel, tampoco lo vamos a poder programar bien.
- Criterio de hecho: tenemos una clase `Cell` que puede responder "¿tengo muro al norte?" y una `Grid` que puede acceder a `grid[x, y]`.
- Conecta con: literalmente todo lo demás depende de esto. Es el ticket más importante del proyecto.

**[G2] Diseñar la interfaz `GenerationStrategy` — 🤝 CONJUNTO con Oscar**
- 📄 Archivo(s): `mazegen/strategies/base.py`
- Qué investigar: `abc.ABC` / `Protocol`, generadores y `yield` (crítico: la estrategia tiene que poder "ceder" estados intermedios paso a paso, no solo devolver el resultado final — esto es lo que luego nos permite la animación sin duplicar código).
- Cómo lo vamos a afrontar: vamos a escribir primero la firma del método (qué recibe, qué produce en cada `yield`) antes de implementar ningún algoritmo real. Es un contrato, como una API.
- Criterio de hecho: existe `strategies/base.py` con la clase abstracta y está documentada con docstrings de qué se espera de cualquier implementación futura.
- Conecta con: Oscar necesita saber esta interfaz para poder programar el modo animado sin esperar a que el algoritmo esté terminado.

**[G3] Implementar `RecursiveBacktrackerStrategy`**
- 📄 Archivo(s): `mazegen/strategies/backtracker.py` (implementa la interfaz de `base.py`)
- Qué investigar: el algoritmo recursive backtracker (el concepto, no pseudocódigo copiado — voy a mirar varias fuentes y quedarme con el entendimiento, no con una implementación concreta).
- Cómo lo voy a afrontar: primero lo voy a hacer funcionar generando un laberinto perfecto sin preocuparme de reproducibilidad ni seed. Una vez funcione, añado el `random.seed()`.
- Criterio de hecho: genera laberintos perfectos válidos (sin ciclos, todo conectado) para varios tamaños, y con la misma seed siempre da el mismo resultado.
- Conecta con: es el primer algoritmo real que Oscar puede usar para probar su renderer.

**[G4] Implementar `encoder.py`**
- 📄 Archivo(s): `mazegen/encoder.py`
- Qué investigar: operaciones a nivel de bit (`&`, `|`, formato hexadecimal en Python con `hex()` / f-strings `{:x}`).
- Cómo lo voy a afrontar: voy a escribir primero los tests con casos conocidos a mano (una celda con muros N y E cerrados debería dar tal dígito) antes de implementar — así sé exactamente qué tiene que devolver.
- Criterio de hecho: pasa el `maze_analyzer.py` sin errores de coherencia.
- Conecta con: Oscar lo necesita indirectamente porque `cli.py` debe llamarlo para escribir el archivo de salida.

**[G5] Implementar `solver.py` (BFS)**
- 📄 Archivo(s): `mazegen/solver.py`
- Qué investigar: BFS con una cola (`collections.deque`), cómo reconstruir el camino desde el resultado del BFS.
- Cómo lo voy a afrontar: es un algoritmo bastante estándar — voy a buscar el concepto general de "BFS shortest path en grid con obstáculos" (los muros son mis obstáculos), no una solución específica de laberintos.
- Criterio de hecho: devuelve la secuencia correcta de letras N/E/S/W para varios laberintos de prueba.
- Conecta con: `encoder.py` (necesita el camino para escribirlo en el archivo) y con Oscar (necesita el camino para dibujar la ruta resaltada).

#### Semana 2

**[G6] Implementar `pattern42.py`**
- 📄 Archivo(s): `mazegen/pattern42.py` (se invoca desde `mazegen/generator.py`)
- Qué investigar: cómo definir una máscara de coordenadas fijas (una matriz booleana o un `set` de tuplas `(x,y)`) que representen el dibujo del "42", y cómo hacer que la generación respete esas celdas como "completamente cerradas".
- Cómo lo voy a afrontar: primero voy a diseñar el patrón como una matriz simple en papel/spreadsheet para un tamaño de referencia (por ejemplo 20x15), y luego programaré cómo escalarlo o centrarlo según el tamaño real del laberinto pedido en config.
- Criterio de hecho: el patrón se ve reconocible en la salida ASCII para varios tamaños razonables, y el programa muestra el mensaje de error correcto cuando el tamaño es demasiado pequeño.
- Conecta con: tiene que aplicarse antes de correr la estrategia de generación (como restricción), así que toca `generator.py`.

**[G7] Implementar `modes/playable.py`**
- 📄 Archivo(s): `mazegen/modes/playable.py` (y probablemente `mazegen/modes/perfect.py` en paralelo, para dejar simétrico el otro modo)
- Qué investigar: técnicas de "braiding" (romper muros de un árbol de expansión para crear loops controlados), cómo detectar dead-ends en una grid, cómo verificar conectividad (puedo reutilizar ideas de BFS/DFS que ya usé en el solver).
- Cómo lo voy a afrontar — es el ticket más delicado del proyecto: voy a dividir el problema en sub-requisitos y resolverlos uno a uno, verificando cada uno con tests antes de pasar al siguiente: (1) esquinas y centro abiertos, (2) al menos 2 rutas independientes, (3) sin áreas 3x3 abiertas, (4) control de dead-ends. No voy a intentar resolver los cuatro a la vez.
- Criterio de hecho: pasa `maze_analyzer.py` en modo "playable" de forma consistente en varios tamaños y seeds.
- Conecta con: Oscar puede empezar a probar su interfaz "regenerar" con este modo en cuanto esté listo.

**[G8] Implementar `RandomizedPrimStrategy`**
- 📄 Archivo(s): `mazegen/strategies/prim.py` + actualizar `mazegen/strategies/__init__.py` (registro/factory)
- Qué investigar: el algoritmo de Prim aleatorizado para laberintos (concepto).
- Cómo lo vamos a afrontar: como ya existe `base.py` y `backtracker.py` como referencia de "cómo se implementa una strategy en este proyecto", vamos a usar ese patrón ya establecido — este ticket es buena oportunidad para que Oscar lo intente con mi apoyo cercano.
- Criterio de hecho: mismo criterio que G3, pero con este algoritmo.
- Conecta con: `strategies/__init__.py` (registro/factory de estrategias) y con la CLI de Oscar (selector de algoritmo).

#### Semana 3

**[G9] Excepciones propias y manejo de errores del dominio**
- 📄 Archivo(s): `mazegen/exceptions.py` (y voy a revisar/tocar `mazegen/generator.py`, `mazegen/grid.py`, etc. para que las lancen donde corresponda)
- Qué investigar: buenas prácticas de excepciones custom en Python (heredar de `Exception`, jerarquías de excepciones).
- Criterio de hecho: `mazegen/` nunca deja escapar una excepción "cruda" de Python sin contexto — todo pasa por excepciones propias que la capa `ui/` puede capturar y mostrar con un mensaje claro.

**[G10] Tests completos + cobertura de casos límite**
- 📄 Archivo(s): `tests/test_grid.py`, `tests/test_strategies.py`, `tests/test_modes.py`, `tests/test_pattern42.py`, `tests/test_solver.py`, `tests/test_encoder.py`
- Qué investigar: qué son los "edge cases" típicos aquí (laberinto 1x1, entry=exit, coordenadas fuera de rango, tamaño insuficiente para el 42).
- Criterio de hecho: `pytest` corre en verde para todos los módulos de `mazegen/`.

**[G11] Empaquetado pip del módulo `mazegen`**
- 📄 Archivo(s): `pyproject.toml` (raíz del repo) → genera `mazegen-1.0.0-py3-none-any.whl` (raíz del repo)
- Qué investigar: `pyproject.toml`, `python -m build`, diferencia `.whl`/`.tar.gz`, cómo probar la instalación en un venv limpio.
- Criterio de hecho: puedo hacer `pip install mazegen-1.0.0-py3-none-any.whl` en un entorno virtual nuevo y ejecutar `from mazegen import MazeGenerator` sin errores.

---

### 🟩 OSCAR — Frontend / ui

#### Semana 1

**[O1] Investigación de fundamentos + acompañar diseño conjunto (G1, G2)**
- 📄 Archivo(s): ninguno propio todavía — participo en `mazegen/grid.py` y `mazegen/strategies/base.py` como revisor/co-diseñador
- Qué investigar en paralelo mientras Gorka avanza en profundidad en teoría de grafos: type hints, dataclasses, clases abstractas (`abc.ABC`), y específicamente para mi parte: códigos de escape ANSI para colores en terminal, y técnicas de limpiar pantalla (`os.system`, o investigar `curses` como alternativa más potente si me apetece explorarlo).
- Cómo lo voy a afrontar para no perder tiempo: no voy a intentar entender el algoritmo de generación a fondo todavía — de momento solo necesito entender la forma de los datos que voy a recibir (una grid con celdas que tienen muros), no cómo se generan.
- Conecta con: participo activamente en G1/G2 porque voy a consumir esa interfaz constantemente — mi input en el diseño es valioso precisamente porque veo el problema desde el lado de "qué necesito para dibujar esto fácilmente".

**[O2] Diseñar la interfaz `Renderer` (abstracta)**
- 📄 Archivo(s): `ui/renderer/base.py`
- Qué investigar: cómo se define una interfaz mínima en Python con `abc.ABC` (mismo concepto que G2, así que es buen momento para consolidarlo).
- Cómo lo voy a afrontar: voy a pensar en los verbos que necesito: `setup()`, `draw(grid, entry, exit, path=None)`, algo para manejar eventos de menú. No voy a diseñar de más — solo lo que el capítulo V pide explícitamente (regenerar, mostrar/ocultar camino, cambiar colores).
- Criterio de hecho: `ui/renderer/base.py` existe con la interfaz documentada.
- Conecta con: define el contrato que `ascii_renderer.py` va a implementar después.

**[O3] Primer renderer ASCII mínimo (sin interacción todavía)**
- 📄 Archivo(s): `ui/renderer/ascii_renderer.py` (implementa `ui/renderer/base.py`)
- Qué investigar: cómo combinar caracteres (`-`, `|`, `+`, o los de línea Unicode `─│┌┐└┘`) para representar una cuadrícula con muros según los datos de cada celda.
- Cómo lo voy a afrontar: no voy a esperar a que el backend esté terminado. En cuanto Gorka tenga aunque sea una `Grid` construida "a mano" (sin generación real, solo para probar), puedo empezar a dibujarla — desacoplo mi trabajo de si el algoritmo real ya funciona o no.
- Criterio de hecho: puedo pasar una `Grid` cualquiera y se ve una representación ASCII reconocible en terminal.
- Conecta con: en cuanto G3 (backtracker) esté listo, sustituyo la grid "hecha a mano" por una real generada.

#### Semana 2

**[O4] `config_loader.py` con pydantic**
- 📄 Archivo(s): `ui/config_loader.py`
- Qué investigar: modelos básicos de pydantic (`BaseModel`, validadores, tipos con restricciones), y cómo parsear un archivo de texto simple `CLAVE=VALOR` a un diccionario antes de pasarlo al modelo.
- Cómo lo voy a afrontar: voy a separar el problema en dos pasos claros: (1) leer el archivo y convertirlo en un diccionario simple ignorando comentarios, (2) validar ese diccionario con un modelo pydantic que dé errores claros si falta una clave obligatoria o el tipo no es correcto.
- Criterio de hecho: mensajes de error entendibles para casos como archivo inexistente, clave faltante, coordenadas fuera de rango, valores no numéricos donde se esperan números.
- Conecta con: `cli.py` lo usa como primer paso de todo el flujo del programa.

**[O5] Interacciones del renderer: mostrar/ocultar camino, cambiar colores**
- 📄 Archivo(s): `ui/renderer/ascii_renderer.py` (y probablemente `ui/cli.py` para el bucle de menú)
- Qué investigar: cómo mantener un pequeño "estado" del programa (¿está visible el camino o no?, ¿qué color toca ahora?) entre iteraciones del menú.
- Cómo lo voy a afrontar: voy a empezar con un menú basado en `input()` simple con opciones numeradas — no necesito nada más sofisticado, el enunciado no pide tiempo real, solo que las funciones existan.
- Criterio de hecho: se cumplen las 3 interacciones mínimas del capítulo V.
- Conecta con: usa `solver.py` de Gorka (G5) para el camino, y los datos de `Grid` para el resto.

**[O6] Segunda strategy (Prim) — con apoyo cercano de Gorka**
- 📄 Archivo(s): `mazegen/strategies/prim.py` (mismo archivo que G8 — es el mismo ticket, lo hacemos en conjunto)
- Como hablamos, es una buena oportunidad para que toque directamente el core del backend con guía, replicando el patrón ya establecido por `backtracker.py`. Ver ticket G8 — lo hacemos en sesión conjunta o con check-ins más frecuentes ese día concreto.

#### Semana 3

**[O7] `cli.py` — integración completa del flujo**
- 📄 Archivo(s): `ui/cli.py` + `a_maze_ing.py` (punto de entrada raíz, que probablemente solo llama a `ui/cli.py`)
- Qué investigar: nada nuevo técnicamente, es sobre todo orquestación de piezas ya existentes.
- Cómo lo voy a afrontar: voy a dibujar primero el flujo como un diagrama simple (leer config → construir generator → generar → escribir archivo → mostrar → menú interactivo) antes de escribir el código, para no perder piezas.
- Criterio de hecho: `python3 a_maze_ing.py config.txt` funciona de punta a punta.
- Conecta con: es el punto donde backend y frontend se encuentran de verdad — buen ticket para hacer en pair programming los dos juntos.

**[O8] Animación de generación en vivo (bonus)**
- 📄 Archivo(s): `ui/renderer/ascii_renderer.py` (nuevo método tipo `draw_step`) + `ui/cli.py` (para invocarlo iterando la strategy)
- Qué investigar: cómo consumir un generador Python (`for state in strategy.generate(...): renderer.draw(state)`) con una pequeña pausa (`time.sleep()`) entre pasos.
- Cómo lo voy a afrontar: esto debería ser relativamente directo si la interfaz `GenerationStrategy` (G2) se diseñó bien desde el principio con `yield` — si nos cuesta mucho implementarlo, es una señal de que hay que revisar esa interfaz, no forzar el renderer.
- Criterio de hecho: se ve el laberinto "construirse" celda a celda en terminal.

**[O9] Tests de `config_loader.py` y del renderer**
- 📄 Archivo(s): `tests/test_config_loader.py` (y podemos añadir un `tests/test_renderer.py` si nos interesa, no estaba en el árbol original pero encaja)
- Igual que G10 pero para mi parte — no vamos a dejar los tests solo para el backend.

**[O10] Makefile, `.gitignore`, LICENSE.md**
- 📄 Archivo(s): `Makefile`, `.gitignore`, `LICENSE.md` (todos en la raíz del repo)
- Qué investigar: sintaxis básica de Makefile (targets, dependencias entre ellos), diferencia entre licencias permisivas (MIT) y copyleft (GPL) para elegir con criterio.
- Criterio de hecho: los 6 comandos del capítulo III.2 funcionan.

---

### 🟨 TICKETS CONJUNTOS (ambos, cualquier semana según avance)

- **[C1] README.md** — 📄 Archivo(s): `README.md` (raíz). Lo vamos a ir rellenando progresivamente, no todo al final. Cada uno documenta su propia parte a medida que la termina.
- **[C2] Sesiones de peer learning / live coding** — 📄 Archivo(s): ninguno propio, trabajamos sobre cualquier archivo ya existente del repo, rotando. Cadencia: check-ins cortos 2-3x/semana + sesión larga semanal.
- **[C3] Integración final y pulido de mypy/flake8** — 📄 Archivo(s): todo el repo (barrido general, sin archivo fijo). Pasada final ya con todas las piezas encajadas.
- **[C4] Preparación de la defensa** — 📄 Archivo(s): ninguno (es repaso oral/conceptual sobre todo el repo). Repasamos juntos cómo explicaríamos cualquier parte del proyecto, incluida la del otro, para estar cubiertos ante el capítulo IX.

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

Todo converge en: O7 (cli.py) — el punto de integración real del proyecto
```

**Lectura práctica de este mapa:** G1 y G2 son los únicos tickets que de verdad bloquean el trabajo de Oscar si no están listos — por eso van primero y en conjunto. Una vez existen (aunque sea en versión mínima/borrador), Oscar puede avanzar en paralelo casi sin esperarme, incluso simulando datos de prueba a mano mientras el backend real se termina.

---

## 4. Cómo vamos a evitar perder tiempo (resumen de criterios prácticos)

- **No vamos a investigar más de lo necesario antes de programar.** El objetivo de la fase de investigación no es "dominar el tema", es entender lo suficiente para empezar a experimentar y equivocarnos rápido. Si llevamos más de 2-3 horas leyendo sobre un algoritmo sin haber escrito ni una línea, es momento de empezar a probar aunque no lo tengamos 100% claro.
- **Vamos a construir de lo simple a lo complejo dentro de cada ticket.** Ejemplo: primero un laberinto perfecto sin seed, luego con seed; primero el renderer sin colores, luego con colores.
- **No nos vamos a bloquear esperando al otro si no hace falta.** Usaremos datos "de mentira" (una grid construida a mano) para no depender de que la pieza real del compañero esté terminada.
- **Vamos a correr `maze_analyzer.py` constantemente**, no solo al final — es nuestra forma más rápida de saber si algo está mal sin tener que depurarlo nosotros mismos desde cero.
- **Vamos a documentar decisiones en el momento, no al final** (comentario corto en cada ticket cerrado) — nos ahorra reconstruir el README bajo presión en la última semana.
