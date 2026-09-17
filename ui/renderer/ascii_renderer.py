import os
import time
from collections.abc import Generator

from mazegen.grid import Walls
from ui.renderer.base import Renderer, WallColor

RESET = "\033[0m"
ENTRY_COLOR = "\033[32m"
EXIT_COLOR = "\033[31m"
PATH_COLOR = "\033[33m"

# Color mapping to contrast the central logo against the wall color
COMPLEMENTARY_COLORS = {
    WallColor.CYAN: WallColor.RED,
    WallColor.RED: WallColor.CYAN,
    WallColor.GREEN: WallColor.MAGENTA,
    WallColor.YELLOW: WallColor.BLUE,
    WallColor.MAGENTA: WallColor.GREEN,
    WallColor.BLUE: WallColor.YELLOW,
}


class ascii_renderer(Renderer):
    """Terminal renderer with strict border resolution and box-drawing.

    Draws the grid while keeping the perimeter boundaries always closed.
    Handles the boundaries between walkable corridors and the central logo as
    standard structural walls, filling only the pure interior of blocked cells
    with continuous blocks.
    """

    def clear_screen(self) -> None:
        """Clears the visible console buffer according to the platform."""
        os.system("cls" if os.name == "nt" else "clear")

    def is_blocked(self, x: int, y: int) -> bool:
        """Checks whether a cell is blocked while respecting matrix boundaries.

        Args:
            x: Horizontal coordinate (column).
            y: Vertical coordinate (row).

        Returns:
            `True` if the cell exists and has the `blocked` property,
            otherwise `False`.
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
        """Consume a generator to refresh the display in real time.

        Args:
            generator: Iterator yielding coordinate tuples during the
                algorithm.
            path: Optional list of coordinates to overlay as the solution.
            delay: Pause in seconds between frames to regulate speed.
        """
        for _ in generator:
            self.clear_screen()
            self.draw_grid(path)
            time.sleep(delay)
        self.clear_screen()
        self.draw_grid(path)

    def draw_grid(self, path: list[tuple[int, int]] | None = None) -> None:
        """Render the complete maze to stdout with its borders and cells.

        Args:
            path: Solved path to highlight on the drawing.
        """
        path_set = set(path) if path is not None else set()

        self._draw_horizontal_wall(0)
        for y in range(self.matriz.altura):
            self._draw_row(y, path_set)
            if y < self.matriz.altura - 1:
                self._draw_middle_wall(y)
        self._draw_bottom_wall()

    def _draw_horizontal_wall(self, y: int) -> None:
        """Draws the continuous horizontal top border of the board."""
        for x in range(self.matriz.anchura):
            joint = self._get_joint_at(x, 0)
            print(joint, end="")
            print(self._paint("━━━", self.wall_color.value), end="")
        last_joint = self._get_joint_at(self.matriz.anchura, 0)
        print(last_joint)

    def _draw_bottom_wall(self) -> None:
        """Draws the continuous horizontal closing wall at the board base."""
        y_last = self.matriz.altura
        for x in range(self.matriz.anchura):
            joint = self._get_joint_at(x, y_last)
            print(joint, end="")
            print(self._paint("━━━", self.wall_color.value), end="")
        last_joint = self._get_joint_at(self.matriz.anchura, y_last)
        print(last_joint)

    def _draw_row(self, y: int, path_set: set[tuple[int, int]]) -> None:
        """Renders one horizontal row of cells and manages east-west dividers.

        Distinguishes three cases between adjacent columns:
        - Both blocked: solid continuous fill block (`█`).
        - Corridor/block transition: regular divider wall (`┃`).
        - Open corridors: checks the active wall in the cell.

        Args:
            y: Index of the row to draw.
            path_set: Set of coordinates belonging to the optimal path.
        """
        pattern_color = (
            COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value
        )

        # The left outer perimeter is an invariant structural wall.
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
        """Draw the horizontal divisions between rows `y` and `y + 1`.

        Visually resolves north-south transitions between blocked and
        traversable cells.
        """
        pattern_color = (
            COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value
        )

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

    def _draw_cell_content(
        self,
        x: int,
        y: int,
        path_set: set[tuple[int, int]],
    ) -> None:
        """Print the central 3-character fill for a cell based on state."""
        pattern_color = (
            COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value
        )
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
        """Determine the orthogonal section for junction `(jx, jy)`.

        Only draws a solid fill `█` when the node is completely inside the
        strict blocked pattern area (all 4 incident corners blocked and not
        touching the map edges). Otherwise, it checks connectivity in the four
        cardinal directions to resolve the appropriate box-drawing glyph.

        Args:
            jx: Horizontal coordinate of the node (0 to width).
            jy: Vertical coordinate of the node (0 to height).

        Returns:
            A colored string with the computed glyph.
        """
        pattern_color = (
            COMPLEMENTARY_COLORS.get(self.wall_color, WallColor.RED).value
        )

        top_left = (
            self.is_blocked(jx - 1, jy - 1) if (jx > 0 and jy > 0) else False
        )
        top_right = (
            self.is_blocked(jx, jy - 1)
            if (jx < self.matriz.anchura and jy > 0)
            else False
        )
        bottom_left = (
            self.is_blocked(jx - 1, jy)
            if (jx > 0 and jy < self.matriz.altura)
            else False
        )
        bottom_right = (
            self.is_blocked(jx, jy)
            if (jx < self.matriz.anchura and jy < self.matriz.altura)
            else False
        )

        # Solid block drawn only when the junction is completely inside
        # the mask.
        if (
            0 < jx < self.matriz.anchura
            and 0 < jy < self.matriz.altura
        ):
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
            return has_wall(jx - 1, jy - 1, Walls.este) or has_wall(
                jx, jy - 1, Walls.oeste
            )

        def has_vertical_south() -> bool:
            if jy == self.matriz.altura:
                return False
            if jx == 0 or jx == self.matriz.anchura:
                return True
            bl = self.is_blocked(jx - 1, jy)
            br = self.is_blocked(jx, jy)
            if bl != br:
                return True
            return has_wall(jx - 1, jy, Walls.este) or has_wall(
                jx, jy, Walls.oeste
            )

        def has_horizontal_west() -> bool:
            if jx == 0:
                return False
            if jy == 0 or jy == self.matriz.altura:
                return True
            tl = self.is_blocked(jx - 1, jy - 1)
            bl = self.is_blocked(jx - 1, jy)
            if tl != bl:
                return True
            return has_wall(jx - 1, jy - 1, Walls.sur) or has_wall(
                jx - 1, jy, Walls.norte
            )

        def has_horizontal_east() -> bool:
            if jx == self.matriz.anchura:
                return False
            if jy == 0 or jy == self.matriz.altura:
                return True
            tr = self.is_blocked(jx, jy - 1)
            br = self.is_blocked(jx, jy)
            if tr != br:
                return True
            return has_wall(jx, jy - 1, Walls.sur) or has_wall(
                jx, jy, Walls.norte
            )

        north = has_vertical_north()
        south = has_vertical_south()
        west = has_horizontal_west()
        east = has_horizontal_east()

        joint_char = self._get_joint(north, east, south, west)
        return self._paint(joint_char, self.wall_color.value)

    def _get_joint(
        self,
        north: bool,
        east: bool,
        south: bool,
        west: bool,
    ) -> str:
        """Map connected walls in the four directions to one glyph."""
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
        """Apply the ANSI color sequence and reset formatting at the end."""
        return f"{color}{text}{RESET}"
