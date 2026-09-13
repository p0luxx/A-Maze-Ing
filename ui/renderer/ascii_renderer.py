import os
import time
from collections.abc import Generator

from mazegen.grid import Grid, Walls
from ui.renderer.base import Renderer, WallColor

RESET = "\033[0m"
ENTRY_COLOR = "\033[32m"
EXIT_COLOR = "\033[31m"
PATH_COLOR = "\033[33m"

# Mapeo cromático para contrastar el logotipo central frente al color de los muros
COMPLEMENTARY_COLORS = {
    WallColor.CYAN: WallColor.RED,
    WallColor.RED: WallColor.CYAN,
    WallColor.GREEN: WallColor.MAGENTA,
    WallColor.YELLOW: WallColor.BLUE,
    WallColor.MAGENTA: WallColor.GREEN,
    WallColor.BLUE: WallColor.YELLOW,
}


class ascii_renderer(Renderer):
    """Renderizador por terminal con resolución estricta de bordes y caracteres box-drawing.

    Dibuja la cuadrícula asegurando que los límites perimetrales queden siempre
    cerrados. Maneja las fronteras entre pasillos transitables y el logotipo
    central como muros estructurales estándar, rellenando con bloques continuos
    únicamente el interior puro de las celdas bloqueadas.
    """

    def clear_screen(self) -> None:
        """Limpia el búfer visible de la consola según la plataforma."""
        os.system("cls" if os.name == "nt" else "clear")

    def is_blocked(self, x: int, y: int) -> bool:
        """Comprueba si una celda está bloqueada respetando los límites de la matriz.

        Args:
            x: Coordenada horizontal (columna).
            y: Coordenada vertical (fila).

        Returns:
            `True` si la celda existe y tiene la propiedad `blocked`, `False` en caso contrario.
        """
        if 0 <= x < self.matriz.anchura and 0 <= y < self.matriz.altura:
            return self.matriz[x, y].blocked
        return False

    def live_animation(
        self,
        generator: Generator[tuple[int, int], None, None],
        path: list[tuple[int, int]] | None = None,
        delay: float = 0.05,
    ) -> None:
        """Consume un generador paso a paso para refrescar la visualización en tiempo real.

        Args:
            generator: Iterador que emite tuplas de coordenadas durante el algoritmo.
            path: Lista opcional de coordenadas a sobreimprimir como solución.
            delay: Pausa en segundos entre fotogramas para regular la velocidad.
        """
        for _ in generator:
            self.clear_screen()
            self.draw_grid(path)
            time.sleep(delay)
        self.clear_screen()
        self.draw_grid(path)

    def draw_grid(self, path: list[tuple[int, int]] | None = None) -> None:
        """Renderiza en stdout el laberinto completo con sus bordes, divisiones y celdas.

        Args:
            path: Camino resuelto a resaltar sobre el trazado.
        """
        path_set = set(path) if path is not None else set()

        self._draw_horizontal_wall(0)
        for y in range(self.matriz.altura):
            self._draw_row(y, path_set)
            if y < self.matriz.altura - 1:
                self._draw_middle_wall(y)
        self._draw_bottom_wall()

    def _draw_horizontal_wall(self, y: int) -> None:
        """Dibuja el borde horizontal continuo de la parte superior del tablero."""
        for x in range(self.matriz.anchura):
            joint = self._get_joint_at(x, 0)
            print(joint, end="")
            print(self._paint("━━━", self.wall_color.value), end="")
        last_joint = self._get_joint_at(self.matriz.anchura, 0)
        print(last_joint)

    def _draw_bottom_wall(self) -> None:
        """Dibuja el cierre horizontal continuo de la base del tablero."""
        y_last = self.matriz.altura
        for x in range(self.matriz.anchura):
            joint = self._get_joint_at(x, y_last)
            print(joint, end="")
            print(self._paint("━━━", self.wall_color.value), end="")
        last_joint = self._get_joint_at(self.matriz.anchura, y_last)
        print(last_joint)

    def _draw_row(self, y: int, path_set: set[tuple[int, int]]) -> None:
        """Renderiza una fila horizontal de celdas y gestiona sus divisiones verticales este-oeste.

        Diferencia tres casos entre columnas adyacentes:
        - Ambas bloqueadas: bloque sólido de relleno continuo (`█`).
        - Transición pasillo/bloqueo: muro regular divisorio (`┃`).
        - Pasillos abiertos: consulta de pared activa en la celda.

        Args:
            y: Índice de la fila a dibujar.
            path_set: Conjunto de coordenadas pertenecientes a la ruta óptima.
        """
        pattern_color = COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value

        # El perímetro exterior izquierdo es un muro estructural invariable
        print(self._paint("┃", self.wall_color.value), end="")

        for x in range(self.matriz.anchura):
            self._draw_cell_content(x, y, path_set)

            if x == self.matriz.anchura - 1:
                print(self._paint("┃", self.wall_color.value), end="")
            else:
                b1 = self.is_blocked(x, y)
                b2 = self.is_blocked(x + 1, y)

                if b1 and b2:
                    print(self._paint("█", pattern_color), end="")
                elif b1 != b2:
                    print(self._paint("┃", self.wall_color.value), end="")
                else:
                    celda = self.matriz[x, y]
                    if celda.lista & Walls.este:
                        print(self._paint("┃", self.wall_color.value), end="")
                    else:
                        print(" ", end="")
        print()

    def _draw_middle_wall(self, y: int) -> None:
        """Dibuja las divisiones horizontales entre la fila `y` e `y + 1`.

        Resuelve visualmente las transiciones norte-sur entre celdas bloqueadas y transitables.
        """
        pattern_color = COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value

        for x in range(self.matriz.anchura):
            joint = self._get_joint_at(x, y + 1)
            print(joint, end="")

            b_top = self.is_blocked(x, y)
            b_bot = self.is_blocked(x, y + 1)

            if b_top and b_bot:
                print(self._paint("███", pattern_color), end="")
            elif b_top != b_bot:
                print(self._paint("━━━", self.wall_color.value), end="")
            else:
                celda_arriba = self.matriz[x, y]
                if celda_arriba.lista & Walls.sur:
                    print(self._paint("━━━", self.wall_color.value), end="")
                else:
                    print("   ", end="")
        last_joint = self._get_joint_at(self.matriz.anchura, y + 1)
        print(last_joint)

    def _draw_cell_content(self, x: int, y: int, path_set: set[tuple[int, int]]) -> None:
        """Imprime el relleno central de 3 caracteres de la celda según prioridades de estado."""
        pattern_color = COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value
        celda = self.matriz[x, y]

        if celda.blocked:
            print(self._paint("███", pattern_color), end="")
        elif (x, y) == self.entry:
            print(self._paint(" ▶ ", ENTRY_COLOR), end="")
        elif (x, y) == self.exit:
            print(self._paint(" ◆ ", EXIT_COLOR), end="")
        elif (x, y) in path_set:
            print(self._paint(" • ", PATH_COLOR), end="")
        else:
            print("   ", end="")

    def _get_joint_at(self, jx: int, jy: int) -> str:
        """Determina la pieza ortogonal (`+`, `T`, esquinas o relleno) para el cruce `(jx, jy)`.

        Solo dibuja relleno sólido `█` si el nodo está completamente contenido en el interior
        estricto del patrón bloqueado (las 4 esquinas incidentes bloqueadas y sin tocar los bordes
        del mapa). En caso contrario, comprueba la conectividad en las cuatro direcciones
        cardinales para resolver el glifo box-drawing apropiado.

        Args:
            jx: Coordenada horizontal del nodo (0 a anchura).
            jy: Coordenada vertical del nodo (0 a altura).

        Returns:
            Cadena coloreada con el glifo calculado.
        """
        pattern_color = COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value

        top_left = self.is_blocked(jx - 1, jy - 1) if (jx > 0 and jy > 0) else False
        top_right = self.is_blocked(jx, jy - 1) if (jx < self.matriz.anchura and jy > 0) else False
        bottom_left = self.is_blocked(jx - 1, jy) if (jx > 0 and jy < self.matriz.altura) else False
        bottom_right = self.is_blocked(jx, jy) if (jx < self.matriz.anchura and jy < self.matriz.altura) else False

        # El bloque macizo solo se dibuja si el cruce es 100% interno a la máscara
        if 0 < jx < self.matriz.anchura and 0 < jy < self.matriz.altura:
            if top_left and top_right and bottom_left and bottom_right:
                return self._paint("█", pattern_color)

        def has_wall(x: int, y: int, direction: Walls) -> bool:
            if 0 <= x < self.matriz.anchura and 0 <= y < self.matriz.altura:
                return bool(self.matriz[x, y].lista & direction)
            return False

        def has_vertical_north() -> bool:
            if jy == 0:
                return False
            if jx == 0 or jx == self.matriz.anchura:
                return True
            tl = self.is_blocked(jx - 1, jy - 1)
            tr = self.is_blocked(jx, jy - 1)
            if tl != tr:
                return True
            return has_wall(jx - 1, jy - 1, Walls.este) or has_wall(jx, jy - 1, Walls.oeste)

        def has_vertical_south() -> bool:
            if jy == self.matriz.altura:
                return False
            if jx == 0 or jx == self.matriz.anchura:
                return True
            bl = self.is_blocked(jx - 1, jy)
            br = self.is_blocked(jx, jy)
            if bl != br:
                return True
            return has_wall(jx - 1, jy, Walls.este) or has_wall(jx, jy, Walls.oeste)

        def has_horizontal_west() -> bool:
            if jx == 0:
                return False
            if jy == 0 or jy == self.matriz.altura:
                return True
            tl = self.is_blocked(jx - 1, jy - 1)
            bl = self.is_blocked(jx - 1, jy)
            if tl != bl:
                return True
            return has_wall(jx - 1, jy - 1, Walls.sur) or has_wall(jx - 1, jy, Walls.norte)

        def has_horizontal_east() -> bool:
            if jx == self.matriz.anchura:
                return False
            if jy == 0 or jy == self.matriz.altura:
                return True
            tr = self.is_blocked(jx, jy - 1)
            br = self.is_blocked(jx, jy)
            if tr != br:
                return True
            return has_wall(jx, jy - 1, Walls.sur) or has_wall(jx, jy, Walls.norte)

        north = has_vertical_north()
        south = has_vertical_south()
        west = has_horizontal_west()
        east = has_horizontal_east()

        joint_char = self._get_joint(north, east, south, west)
        return self._paint(joint_char, self.wall_color.value)

    def _get_joint(self, north: bool, east: bool, south: bool, west: bool) -> str:
        """Mapea la presencia de muros conectados en las cuatro direcciones a un glifo Unicode."""
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
            (True, False, False, False): "┃",
            (False, False, True, False): "┃",
            (False, True, False, False): "━",
            (False, False, False, True): "━",
        }
        return joints.get(connections, " ")

    def _paint(self, text: str, color: str) -> str:
        """Aplica la secuencia ANSI del color especificado y resetea el formato al final."""
        return f"{color}{text}{RESET}"