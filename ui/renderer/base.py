import os
from abc import ABC, abstractmethod
from collections.abc import Generator
from enum import Enum

from mazegen.grid import Grid


class WallColor(str, Enum):
    """Palette of ANSI escape codes for coloring walls in the terminal."""

    CYAN = "\033[36m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"


class Renderer(ABC):
    """Abstract base interface for maze rendering engines.

    Defines the required contract for drawing the board and animating
    algorithms step by step, while centralizing wall-color control and
    console cleanup.

    Attributes:
        matriz: Grid with the current cells and walls.
        entry: Coordinates `(x, y)` of the starting point.
        exit: Coordinates `(x, y)` of the exit point.
        wall_color: Active ANSI color for the walls.
    """

    def __init__(
        self,
        grid: Grid,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Initialize the renderer with the base grid and endpoints.

        Args:
            grid: Board with the cells and walls to represent.
            entry: Tuple `(x, y)` for the origin.
            exit: Tuple `(x, y)` for the destination.
        """
        self.matriz: Grid = grid
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.wall_color: WallColor = WallColor.CYAN

    def clear_screen(self) -> None:
        """Clears the visible terminal buffer according to the platform."""
        os.system("cls" if os.name == "nt" else "clear")

    @abstractmethod
    def draw_grid(self, path: list[tuple[int, int]] | None = None) -> None:
        """Render a static view of the maze in its current state.

        Args:
            path: Optional sequential list of coordinates to highlight as a
                solution.
        """
        ...

    @abstractmethod
    def live_animation(
        self,
        generator: Generator[tuple[int, int], None, None],
        path: list[tuple[int, int]] | None = None,
        delay: float = 0.05,
    ) -> None:
        """Consume a generator to draw and refresh each step on screen.

        Args:
            generator: Iterator producing the coordinates processed by the
                algorithm.
            path: Optional route to overlay during the animation.
            delay: Pause interval in seconds between each frame.
        """
        ...

    def ChangeColor(self) -> None:
        """Cycle to the next color palette defined in `WallColor`."""
        colors: list[WallColor] = list(WallColor)
        current = colors.index(self.wall_color)
        next_color = (current + 1) % len(colors)
        self.wall_color = colors[next_color]
