import os
import time

from mazegen.grid import Grid, Walls
from mazegen.strategies.base import GenerationStrategy

from .base import Renderer

RESET = "\033[0m"
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
        # El borde oeste (izquierdo) de la primera columna
        if matriz[0, y].lista & Walls.oeste:
            print(self._paint("┃", self.wall_color), end="")
        else:
            print(" ", end="")

        for x in range(matriz.anchura):
            celda = matriz[x, y]

            self._draw_cell_content(
                x,
                y,
                entry,
                exit_,
                path_set,
            )

            if celda.lista & Walls.este:
                print(self._paint("┃", self.wall_color), end="")
            else:
                print(" ", end="")

        print()

    def _draw_horizontal_wall(self, matriz: Grid, y: int) -> None:
        # y es siempre 0 (muro superior externo)
        for x in range(matriz.anchura):
            joint = self._get_joint_at(matriz, x, 0)
            print(self._paint(joint, self.wall_color), end="")
            
            celda = matriz[x, 0]
            if celda.lista & Walls.norte:
                print(self._paint("━━━", self.wall_color), end="")
            else:
                print("   ", end="")
                
        last_joint = self._get_joint_at(matriz, matriz.anchura, 0)
        print(self._paint(last_joint, self.wall_color))

    def _draw_middle_wall(self, matriz: Grid, y: int) -> None:
        if y >= matriz.altura - 1:
            return
            
        for x in range(matriz.anchura):
            joint = self._get_joint_at(matriz, x, y + 1)
            print(self._paint(joint, self.wall_color), end="")
            
            celda = matriz[x, y]
            if celda.lista & Walls.sur:
                print(self._paint("━━━", self.wall_color), end="")
            else:
                print("   ", end="")
                
        last_joint = self._get_joint_at(matriz, matriz.anchura, y + 1)
        print(self._paint(last_joint, self.wall_color))

    def _draw_bottom_wall(self, matriz: Grid) -> None:
        y_last = matriz.altura
        for x in range(matriz.anchura):
            joint = self._get_joint_at(matriz, x, y_last)
            print(self._paint(joint, self.wall_color), end="")
            
            celda = matriz[x, matriz.altura - 1]
            if celda.lista & Walls.sur:
                print(self._paint("━━━", self.wall_color), end="")
            else:
                print("   ", end="")
                
        last_joint = self._get_joint_at(matriz, matriz.anchura, y_last)
        print(self._paint(last_joint, self.wall_color))

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

    def _get_joint_at(self, grid: Grid, jx: int, jy: int) -> str:
        """
        Determina dinámicamente qué junta Unicode (esquina o intersección)
        se debe pintar en el punto de grilla (jx, jy) basándose en qué
        muros reales (norte, sur, este, oeste) se conectan a él.
        """
        def has_wall(x: int, y: int, direction: Walls) -> bool:
            if 0 <= x < grid.anchura and 0 <= y < grid.altura:
                return bool(grid[x, y].lista & direction)
            return False

        def has_vertical_wall(col: int, r: int) -> bool:
            if r < 0 or r >= grid.altura:
                return False
            if col == 0:
                return has_wall(0, r, Walls.oeste)
            if col == grid.anchura:
                return has_wall(grid.anchura - 1, r, Walls.este)
            return has_wall(col - 1, r, Walls.este) or has_wall(col, r, Walls.oeste)

        def has_horizontal_wall(c: int, row: int) -> bool:
            if c < 0 or c >= grid.anchura:
                return False
            if row == 0:
                return has_wall(c, 0, Walls.norte)
            if row == grid.altura:
                return has_wall(c, grid.altura - 1, Walls.sur)
            return has_wall(c, row - 1, Walls.sur) or has_wall(c, row, Walls.norte)

        # Evaluar conexiones en las 4 direcciones para la junta (jx, jy)
        north = has_vertical_wall(jx, jy - 1)
        south = has_vertical_wall(jx, jy)
        west = has_horizontal_wall(jx - 1, jy)
        east = has_horizontal_wall(jx, jy)

        return self._get_joint(north, east, south, west)

    def _get_joint(self,
                   north: bool,
                   east: bool,
                   south: bool,
                   west: bool,
                   ) -> str:
        connections = (north, east, south, west)

        joints = {
            # Esquinas externas o internas
            (False, True, True, False): "┏",
            (False, False, True, True): "┓",
            (True, True, False, False): "┗",
            (True, False, False, True): "┛",

            # Intersecciones de 3 direcciones (T-joints)
            (True, True, True, False): "┣",
            (True, False, True, True): "┫",
            (False, True, True, True): "┳",
            (True, True, False, True): "┻",

            # Cruces completos (4 direcciones)
            (True, True, True, True): "╋",

            # Líneas continuas (2 direcciones opuestas)
            (True, False, True, False): "┃",
            (False, True, False, True): "━",
            
            # Conexiones simples (para finales de línea o celdas especiales)
            (True, False, False, False): "┃",
            (False, False, True, False): "┃",
            (False, True, False, False): "━",
            (False, False, False, True): "━",
        }

        return joints.get(connections, " ")

    def _paint(self, text: str, color: str) -> str:
        return f"{color}{text}{RESET}"
