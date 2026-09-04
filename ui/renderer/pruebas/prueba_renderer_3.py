from mazegen.grid import Grid, Walls, Cell
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy

"""
El objetivo de esta prueba es realizar el laberinto sin garantizar la existencia de los muros exteriores
- Ahora vamos a meterle el entry y el exit.
"""
def draw_grid(
    matriz: Grid,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[tuple[int, int]] | None = None,
) -> None:
    for y in range(matriz.altura):
        print("*", end="")
        for x in range(matriz.anchura):
            celda = matriz.grid[y][x]
            if celda.lista & Walls.norte:
                print("---", end="")
            else:
                print("   ", end="")
            print("*", end="")
        print()

        if matriz.grid[y][0].lista & Walls.oeste:
            print("|", end="")
        else:
            print(" ", end="")
        for x in range(matriz.anchura):
            celda = matriz.grid[y][x]
            path_set = set(path) if path is not None else set()
            if (x, y) == entry:
                print("EEE", end="")
            elif (x, y)== exit_:
                print("SSS", end="")
            elif (x, y) in path_set:
                print(" O ", end="")
            else:
                print("   ", end="")

            if celda.lista & Walls.este:
                print("|", end="")
            else:
                print(" ", end="")
        print()

        if y == matriz.altura - 1:
            print("*", end="")
            for x in range(matriz.anchura):
                if matriz.grid[y][x].lista & Walls.sur:
                    print("---", end="")
                else:
                    print("   ", end="")
                print("*", end="")
            print()
