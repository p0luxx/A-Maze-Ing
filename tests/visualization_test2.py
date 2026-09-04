import os
import time

from mazegen.grid import Grid, Walls
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy


class ConsoleUI:
    def __init__(self, grid: Grid):
        self.grid = grid

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def render(self, current_pos: tuple[int, int] | None = None):
        lineas = []

        for y in range(self.grid.altura):
            top_line = ""
            mid_line = ""

            for x in range(self.grid.anchura):
                celda = self.grid.grid[y][x]

                if celda.lista & Walls.norte:
                    top_line += "+---"
                else:
                    top_line += "+   "

                if celda.lista & Walls.oeste:
                    mid_line += "| "
                else:
                    mid_line += "  "

                if current_pos == (x, y):
                    mid_line += "* "
                else:
                    mid_line += "  "

            top_line += "+"

            ultima_celda = self.grid.grid[y][self.grid.anchura - 1]

            if ultima_celda.lista & Walls.este:
                mid_line += "|"
            else:
                mid_line += " "

            lineas.append(top_line)
            lineas.append(mid_line)

        bottom_line = ""

        for x in range(self.grid.anchura):
            celda = self.grid.grid[self.grid.altura - 1][x]

            if celda.lista & Walls.sur:
                bottom_line += "+---"
            else:
                bottom_line += "+   "

        bottom_line += "+"
        lineas.append(bottom_line)

        print("\n".join(lineas))

    def animate_generation(self, generator, delay: float = 0.05):
        for step in generator:
            self.clear_screen()
            self.render(current_pos=step)
            time.sleep(delay)

        self.clear_screen()
        self.render()

        print("\nLaberinto generado")


def main():
    grid = Grid(
        altura=10,
        anchura=10
    )

    ui = ConsoleUI(grid)

    strategy = IterativeBacktrackerStrategy()

    generador = strategy.generate(
        grid=grid,
        seed=238,
        start_gen=(5, 5)
    )

    ui.animate_generation(
        generador,
        delay=0.03
    )


if __name__ == "__main__":
    main()
