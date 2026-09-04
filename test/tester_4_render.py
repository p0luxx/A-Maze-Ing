from mazegen.grid import Grid
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy
from ui.renderer.prueba_renderer_4 import draw_grid


def main():
    # Para esta prueba usamos grid cuadrada
    grid = Grid(altura=10, anchura=10)
    
    # Estrategia de generación
    strategy = IterativeBacktrackerStrategy()

    # Crear generador
    generador = strategy.generate(
        grid=grid,
        seed=268,
        start_gen=(5, 5)
    )

    # IMPORTANTE:
    # generate() es un Generator.
    # Hay que recorrerlo para que ejecute todo el algoritmo
    # y vaya modificando grid.
    for _ in generador:
        pass
    
    # Cuando termina, grid contiene el laberinto generado
    lista_tuplas = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
 (6, 3), (6, 4), (6, 5), (6, 6)]
    draw_grid(grid, (0, 2), (6, 7), lista_tuplas)


if __name__ == "__main__":
    main()

