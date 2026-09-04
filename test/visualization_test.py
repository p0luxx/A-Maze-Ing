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
        lines = []

        for y in range(self.grid.altura):
            top_line = ""
            middle_line = ""

            for x in range(self.grid.anchura):
                cell = self.grid.grid[y][x]

                top_line += "+"

                if cell.lista & Walls.norte:
                    top_line += "---"
                else:
                    top_line += "   "

                if x == 0:
                    if cell.lista & Walls.oeste:
                        middle_line += "|"
                    else:
                        middle_line += " "

                middle_line += "   "

                if cell.lista & Walls.este:
                    middle_line += "|"
                else:
                    middle_line += " "

            top_line += "+"
            lines.append(top_line)
            lines.append(middle_line)

        bottom_line = ""

        for x in range(self.grid.anchura):
            cell = self.grid.grid[self.grid.altura - 1][x]

            bottom_line += "+"

            if cell.lista & Walls.sur:
                bottom_line += "---"
            else:
                bottom_line += "   "

        bottom_line += "+"
        lines.append(bottom_line)

        print("\n".join(lines))

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

    generator = strategy.generate(
        grid=grid,
        seed=238,
        start_gen=(5, 5)
    )

    ui = ConsoleUI(grid)

    ui.animate_generation(
        generator,
        delay=0.15
    )


if __name__ == "__main__":
    main()
