from .base import Renderer
from mazegen.grid import Grid, Walls
from mazegen.strategies.base import GenerationStrategy
import os
import time


RESET = "\033[0m"

WALL_COLOR = "\033[36m"
ENTRY_COLOR = "\033[32m"
EXIT_COLOR = "\033[31m"
PATH_COLOR = "\033[33m"

class ascii_renderer(Renderer):

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def live_animation(self,
                       generator: GenerationStrategy,
                        path: list[tuple[int, int]] | None = None,
                       delay: float = 0.10) -> None:
        for step in generator:
            self.clear_screen()
            self.draw_grid(path)
            time.sleep(delay)
        self.clear_screen()
        self.draw_grid(path)

    def draw_grid(self,
                  path: list[tuple[int, int]] | None = None
                  ) -> None:
        path_set = set(path) if path is not None else set()

        self._draw_horizontal_wall(self.matriz, 0)

        for y in range(self.matriz.altura):
            self._draw_row(
                self.matriz, y,
                self.entry, self.exit,
                path_set,
                    )

            if y < self.matriz.altura - 1:
                self._draw_middle_wall(self.matriz, y)

        self._draw_bottom_wall(self.matriz)

    def _draw_row(self,
        matriz: Grid,
        y: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        path_set: set[tuple[int, int]],
        ) -> None:
        if matriz.grid[y][0].lista & Walls.oeste:
            print(self._paint("┃", WALL_COLOR), end="")
        else:
            print(" ", end="")

        for x in range(matriz.anchura):
            celda = matriz.grid[y][x]

            self._draw_cell_content(
                x,
                y,
                entry,
                exit_,
                path_set,
                )

            if celda.lista & Walls.este:
                print(self._paint("┃", WALL_COLOR), end="")
            else:
                print(" ", end="")

        print()

    def _draw_bottom_wall(self, matriz: Grid) -> None:
        y = matriz.altura - 1

        print(self._paint("┗", WALL_COLOR), end="")

        for x in range(matriz.anchura):
            celda = matriz.grid[y][x]

            if celda.lista & Walls.sur:
                print(self._paint("━━━", WALL_COLOR), end="")
            else:
                print("   ", end="")

            if x == matriz.anchura - 1:
                print(self._paint("┛", WALL_COLOR), end="")
            else:
                print(self._paint("┻", WALL_COLOR), end="")

        print()

    def _draw_middle_wall(self,
            matriz: Grid,
            y: int,
        ) -> None:
        if y >= matriz.altura - 1:
            return

        print(self._paint("┣", WALL_COLOR), end="")

        for x in range(matriz.anchura):
            celda = matriz.grid[y][x]

            if celda.lista & Walls.sur:
                print(self._paint("━━━", WALL_COLOR), end="")
            else:
                print("   ", end="")

            if x == matriz.anchura - 1:
                print(self._paint("┫", WALL_COLOR), end="")
            else:
                print(self._paint("╋", WALL_COLOR), end="")

        print()

    def _draw_horizontal_wall(self,
        matriz: Grid,
        y: int,
        ) -> None:
        for x in range(matriz.anchura):
            celda = matriz.grid[y][x]

            if x == 0:
                print(self._paint("┏", WALL_COLOR), end="")

            if celda.lista & Walls.norte:
                print(self._paint("━━━", WALL_COLOR), end="")
            else:
                print("   ", end="")

            if x == matriz.anchura - 1:
                print(self._paint("┓", WALL_COLOR), end="")
            else:
                print(self._paint("┳", WALL_COLOR), end="")

        print()

    def _draw_cell_content(self,
            x: int,
            y: int,
            entry: tuple[int, int],
            exit_: tuple[int, int],
            path_set: set[tuple[int, int]],
            ) -> None:
        if (x, y) == entry:
            print(self._paint(" ▶ ", ENTRY_COLOR), end="")
        elif (x, y) == exit_:
            print(self._paint(" ◆ ", EXIT_COLOR), end="")
        elif (x, y) in path_set:
            print(self._paint(" • ", PATH_COLOR), end="")
        else:
            print("   ", end="")

    def _get_joint(self,
        north: bool,
        east: bool,
        south: bool,
        west: bool,
        ) -> str:
        """Para una futura optimizacion del laberinto"""
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

    def _paint(self, text: str, color: str) -> str:
        return f"{color}{text}{RESET}"
