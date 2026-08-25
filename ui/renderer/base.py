"""
    Renderer(contrato):
            Dice que debe de poder hacer cualquier visualizador
"""
from abc import ABC, abstractmethod
from mazegen.strategies import Grid, Walls
import os
import time


class Renderer(ABC):
    def __init__(self, grid: Grid, 
                 entry: tuple[int, int],
                 exit_: tuple[int, int]) -> None:
        self.matriz: Grid = grid
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
        
    """
    @abstractmethod
    def draw_grid(self,
                  path: list[tuple[int, int]] | None = None
                  ) -> None:
        """Render the complete current state of the maze.
        Args:
        path: Optional sequence of coordinates representing the solution path.
        If None, no solution path is displayed.
        """
        ...
    """

    def live_animation(self, 
                       generator: GenerationStrategydelay,
                       delay: float = 0.05) -> None:
        """animates step by step the generation of the maze.
           Args:
            generator: yields a new coordinate step by step
            delay: slows the animation of the maze
        """
        for step in generator:
            self.clear_screen()
            self.draw_grid()
            time.sleep(delay)
        self.clear_screen()
        self.render()
