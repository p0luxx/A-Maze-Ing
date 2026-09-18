from enum import IntFlag


class Walls(IntFlag):
    """Represent the four possible walls of a maze cell.

        Use bit flags so multiple walls can be combined in a single value
        and checked individually with bitwise operations.

    Attributes:
        norte: North wall flag.
        este: East wall flag.
        sur: South wall flag.
        oeste: West wall flag.
    """
    norte = 1
    este = 2
    sur = 4
    oeste = 8


class Cell():
    """Represent a single cell in the maze grid.

        Store the current wall configuration of the cell and whether the
        cell is blocked from normal maze generation or traversal.

        Attributes:
            lista: Bitmask containing the active walls of the cell.
            blocked: Indicates whether the cell is blocked.
    """
    def __init__(self) -> None:
        """Initialize a cell with all walls closed and unblocked."""
        self.lista = Walls(15)
        self.blocked = False


class Grid():
    """Initialize a grid with the given dimensions.

        Create a Cell instance for every coordinate in the grid.

        Args:
            altura: Number of rows in the grid.
            anchura: Number of columns in the grid.
        """
    def __init__(self, altura: int, anchura: int):
        self.altura = altura
        self.anchura = anchura
        self._grid = [[Cell() for _ in range(altura)] for _ in range(anchura)]

    def __getitem__(self, position: tuple[int, int]) -> Cell:
        """Return the cell stored at the given grid position.

        Validate that the coordinates are inside the grid bounds before
        accessing the internal cell structure.

        Args:
            position: Coordinates of the requested cell as an (x, y) tuple.

        Returns:
            The Cell instance stored at the given position.

        Raises:
            IndexError: If the coordinates are outside the grid bounds.
        """
        x, y = position
        if not (0 <= x < self.anchura and 0 <= y < self.altura):
            raise IndexError("Grid dimensions are incorrect")
        return self._grid[x][y]

    def neighbours(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """Return the valid neighbouring coordinates of a grid position.

        Check the four cardinal directions and include only coordinates
        that remain inside the grid boundaries.

        Args:
            position: Coordinates of the reference cell as an (x, y) tuple.

        Returns:
            A list containing the valid neighbouring coordinates.
    """
        x, y = position
        conections: list[tuple[int, int]] = []
        if y > 0:
            conections.append((x, y - 1))
        if y < self.altura - 1:
            conections.append((x, y + 1))
        if x < self.anchura - 1:
            conections.append((x + 1, y))
        if x > 0:
            conections.append((x - 1, y))
        return conections
