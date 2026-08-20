"""
    Renderer(contrato):
            Dice que debe de poder hacer cualquier visualizador
"""
from abc import ABC, abstractmethod
from mazegen.strategies import #...


class Renderer(ABC):
    @abstractmethod
    def draw_grid(self, grid: Grid,
             entry: tuple[int, int],
             exit_: tuple[int, int],
             path: list[tuple[int, int]] | None = None
             ) -> None:
        """Render the complete current state of the maze.
        Args:
        grid: The maze grid to render.
        entry: Coordinates of the maze entrance.
        exit_: Coordinates of the maze exit.
        path: Optional sequence of coordinates representing the solution path.
        If None, no solution path is displayed.
        """

    @abstractmethod
    def draw_cell(self, tuple[int, int]) -> None:
        ...

    @abstractmethod
    def change_walls_colors("""Debe de recibir la grid"""):
        ...

    @abstractmethod
    def change_42_colors("""Debe de recibir las coordenadas del patron 42"""):
        ...
