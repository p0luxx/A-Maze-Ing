import random

from mazegen.grid import Grid, Walls


class PlayableMode:
    """Transforms a perfect maze into an imperfect (braided) one.

    Eliminates dead ends by randomly removing walls into traversable
    neighboring cells, creating alternative loops that improve gameplay and
    prevent frustration during exploration.
    """

    OPPOSITE_WALL = {
        Walls.norte: Walls.sur,
        Walls.sur: Walls.norte,
        Walls.este: Walls.oeste,
        Walls.oeste: Walls.este,
    }

    DIRECTION_OFFSETS = {
        Walls.norte: (0, -1),
        Walls.sur: (0, 1),
        Walls.este: (1, 0),
        Walls.oeste: (-1, 0),
    }

    @staticmethod
    def apply(grid: Grid, seed: int | None = None) -> None:
        """Detect dead-end cells and knock down a wall to create loops.

        Traverse the grid, identifying cells with exactly three active walls
        (dead ends). For each one, randomly select a wall adjacent to an
        in-bounds, navigable cell and update the bitmasks for both cells
        to open the passage.

        Args:
            grid: Instance of the grid to be modified in-place.
            seed: Optional seed to reproduce the selection of demolished walls.
        """
        if seed is not None:
            random.seed(seed)

        for y in range(grid.altura):
            for x in range(grid.anchura):
                celda = grid[x, y]
                if celda.blocked:
                    continue

                # Collects closed walls facing traversable cells in the map.
                muros_cerrados = []
                for wall_flag, (dx, dy) in (
                    PlayableMode.DIRECTION_OFFSETS.items()
                ):
                    nx, ny = x + dx, y + dy
                    in_bounds = (
                        0 <= nx < grid.anchura and 0 <= ny < grid.altura
                    )
                    if (celda.lista & wall_flag) and in_bounds:
                        if not grid[nx, ny].blocked:
                            muros_cerrados.append((wall_flag, nx, ny))

                # A dead-end has exactly 3 active walls (a single exit).
                total_muros_activos = sum(
                    1
                    for w in (Walls.norte, Walls.sur, Walls.este, Walls.oeste)
                    if celda.lista & w
                )

                if (
                    total_muros_activos == 3
                    and muros_cerrados
                ):
                    wall_to_remove, nx, ny = random.choice(muros_cerrados)

                    # Bidirectional opening using bitwise operations
                    celda.lista &= ~wall_to_remove
                    grid[nx, ny].lista &= ~PlayableMode.OPPOSITE_WALL[
                        wall_to_remove
                    ]
