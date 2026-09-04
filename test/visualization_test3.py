import os
import time

from mazegen.grid import Grid, Walls
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy


class ConsoleUI:
    def __init__(self, grid: Grid):
        self.grid = grid

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def render(self) -> None:
        largo = self.grid.altura
        ancho = self.grid.anchura

        for y in range(largo):
            print("*", end="")

            for x in range(ancho):
                celda = self.grid.grid[y][x]

                if y == 0:
                    print("---", end="")
                elif celda.lista & Walls.norte:
                    print("---", end="")
                else:
                    print("   ", end="")

                print("*", end="")

            print()

            print("|", end="")

            for x in range(ancho):
                celda = self.grid.grid[y][x]

                print("   ", end="")

                if x == ancho - 1:
                    print("|", end="")
                elif celda.lista & Walls.este:
                    print("|", end="")
                else:
                    print(" ", end="")

            print()

            if y == largo - 1:
                print("*", end="")

                for _ in range(ancho):
                    print("---*", end="")

                print()

    def animate_generation(
        self,
        generator,
        delay: float = 0.05
    ) -> None:
        for _ in generator:
            self.clear_screen()
            self.render()
            time.sleep(delay)

        self.clear_screen()
        self.render()

        print("\nLaberinto generado")


def main() -> None:
    grid = Grid(
        altura=10,
        anchura=10
    )

    strategy = IterativeBacktrackerStrategy()

    generador = strategy.generate(
        grid=grid,
        seed=238,
        start_gen=(5, 5)
    )

    ui = ConsoleUI(grid)

    ui.animate_generation(
        generador,
        delay=0.03
    )


if __name__ == "__main__":
    main()
