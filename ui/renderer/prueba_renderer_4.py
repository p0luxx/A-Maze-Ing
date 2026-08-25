from mazegen.grid import Grid, Walls, Cell
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy

"""
El objetivo de esta prueba es realizar el laberinto sin garantizar la existencia de los muros exteriores
- Ahora bonito
"""



RESET = "\033[0m"

WALL_COLOR = "\033[36m"
ENTRY_COLOR = "\033[32m"
EXIT_COLOR = "\033[31m"
PATH_COLOR = "\033[33m"


def paint(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def get_joint(
    north: bool,
    east: bool,
    south: bool,
    west: bool,
) -> str:
    connections = (north, east, south, west)

    joints = {
        (False, True, True, False): "┏",
        (False, False, True, True): "┓",
        (True, True, False, False): "┗",
        (True, False, False, True): "┛",

        (True, True, True, False): "┣",
        (True, False, True, True): "┫",
        (False, True, True, True): "┳",
        (True, True, False, True): "┻",

        (True, True, True, True): "╋",

        (True, False, True, False): "┃",
        (False, True, False, True): "━",
    }

    return joints.get(connections, " ")


def draw_cell_content(
    x: int,
    y: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path_set: set[tuple[int, int]],
) -> None:
    if (x, y) == entry:
        print(paint(" ▶ ", ENTRY_COLOR), end="")
    elif (x, y) == exit_:
        print(paint(" ◆ ", EXIT_COLOR), end="")
    elif (x, y) in path_set:
        print(paint(" • ", PATH_COLOR), end="")
    else:
        print("   ", end="")


def draw_horizontal_wall(
    matriz: Grid,
    y: int,
) -> None:
    for x in range(matriz.anchura):
        celda = matriz.grid[y][x]

        if x == 0:
            print(paint("┏", WALL_COLOR), end="")

        if celda.lista & Walls.norte:
            print(paint("━━━", WALL_COLOR), end="")
        else:
            print("   ", end="")

        if x == matriz.anchura - 1:
            print(paint("┓", WALL_COLOR), end="")
        else:
            print(paint("┳", WALL_COLOR), end="")

    print()


def draw_middle_wall(
    matriz: Grid,
    y: int,
) -> None:
    if y >= matriz.altura - 1:
        return

    print(paint("┣", WALL_COLOR), end="")

    for x in range(matriz.anchura):
        celda = matriz.grid[y][x]

        if celda.lista & Walls.sur:
            print(paint("━━━", WALL_COLOR), end="")
        else:
            print("   ", end="")

        if x == matriz.anchura - 1:
            print(paint("┫", WALL_COLOR), end="")
        else:
            print(paint("╋", WALL_COLOR), end="")

    print()


def draw_bottom_wall(matriz: Grid) -> None:
    y = matriz.altura - 1

    print(paint("┗", WALL_COLOR), end="")

    for x in range(matriz.anchura):
        celda = matriz.grid[y][x]

        if celda.lista & Walls.sur:
            print(paint("━━━", WALL_COLOR), end="")
        else:
            print("   ", end="")

        if x == matriz.anchura - 1:
            print(paint("┛", WALL_COLOR), end="")
        else:
            print(paint("┻", WALL_COLOR), end="")

    print()


def draw_row(
    matriz: Grid,
    y: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path_set: set[tuple[int, int]],
) -> None:
    if matriz.grid[y][0].lista & Walls.oeste:
        print(paint("┃", WALL_COLOR), end="")
    else:
        print(" ", end="")

    for x in range(matriz.anchura):
        celda = matriz.grid[y][x]

        draw_cell_content(
            x,
            y,
            entry,
            exit_,
            path_set,
        )

        if celda.lista & Walls.este:
            print(paint("┃", WALL_COLOR), end="")
        else:
            print(" ", end="")

    print()


def draw_grid(
    matriz: Grid,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[tuple[int, int]] | None = None,
) -> None:
    path_set = set(path) if path is not None else set()

    draw_horizontal_wall(matriz, 0)

    for y in range(matriz.altura):
        draw_row(
            matriz,
            y,
            entry,
            exit_,
            path_set,
        )

        if y < matriz.altura - 1:
            draw_middle_wall(matriz, y)

    draw_bottom_wall(matriz)
