    @abstractmethod
    def draw_cell(self, position: tuple[int, int]) -> None:
        """Render or update a single maze cell.
            Args:
                position: Coordinates of the cell to render.
        """
        ... """ para manyana cambiar el draw cell por el animate_generation"""

    """
    @abstractmethod
    def change_walls_colors("""Debe de recibir la grid"""):
        ...

    @abstractmethod
    def change_42_colors("""Debe de recibir las coordenadas del patron 42"""):
        ...
    """
    """
    @abstractmethod
    def draw_grid(self, entry: tuple[int, int],
                  exit_: tuple[int, int],
                  path: list[tuple[int, int]] | None = None
                  ) -> None:
        """Render the complete current state of the maze.
        Args:
        entry: Coordinates of the maze entrance.
        exit_: Coordinates of the maze exit.
        path: Optional sequence of coordinates representing the solution path.
        If None, no solution path is displayed.
        """
        ...
    """

