"""
    Renderer(contrato):
            Dice que debe de poder hacer cualquier visualizador
"""
from abc import ABC, abstractmethod
from mazegen.grid import Grid, Walls
from mazegen.strategies.base import GenerationStrategy
from enum import Enum

class WallColor(str, Enum):
    CYAN = "\033[36m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"


class Renderer(ABC):
    def __init__(self, grid: Grid, 
                 entry: tuple[int, int],
                 exit_: tuple[int, int]) -> None:
        self.matriz: Grid = grid
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_
        self.wall_color: WallColor = WallColor.CYAN
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    @abstractmethod
    def draw_grid(self,
                  path: list[tuple[int, int]] | None = None,
                  ) -> None:
        """Render the complete current state of the maze.
        Args:
        path: Optional sequence of coordinates representing the solution path.
        If None, no solution path is displayed.
        """
        ...

    @abstractmethod
    def live_animation(self, 
                       generator: GenerationStrategy,
                        path: list[tuple[int, int]] | None = None,
                       delay: float = 0.05) -> None:
        """
        animates step by step the generation of the maze.
           Args:
            generator: yields a new coordinate step by step
            delay: slows the animation of the maze
        """

    def ChangeColor(self) -> str:
        colors: list[WallColor] = [WallColor]
        current = colors.index[self.wall_colors]
        next_color = (current + 1) % len(colors)
        self.wall_colors = colors[next_color]
