from mazegen.grid import Grid
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy
from ui.renderer.prueba_renderer_2 import draw_grid


def main():
    # Para esta prueba usamos grid cuadrada
    grid = Grid(altura=10, anchura=10)

    # Estrategia de generación
    strategy = IterativeBacktrackerStrategy()

    # Crear generador
    generador = strategy.generate(
        grid=grid,
        seed=238,
        start_gen=(5, 5)
    )

    # IMPORTANTE:
    # generate() es un Generator.
    # Hay que recorrerlo para que ejecute todo el algoritmo
    # y vaya modificando grid.
    for _ in generador:
        pass

    # Cuando termina, grid contiene el laberinto generado
    draw_grid(grid)


if __name__ == "__main__":
    main()
