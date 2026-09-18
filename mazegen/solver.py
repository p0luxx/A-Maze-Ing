from collections import deque

from mazegen.grid import Grid, Walls


class Solver:
    """Find paths between cells in a maze grid.

    Provide pathfinding operations over a Grid while respecting the
    walls that define which neighbouring cells can be reached.
    """

    @staticmethod
    def find_path(
        grid: Grid, entry: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Find a path between two grid positions using breadth-first search.

        Traverse accessible neighbouring cells while respecting the walls
        of each cell. Track the origin of every visited position so the
        path can be reconstructed once the destination is reached.

        Args:
            grid: Grid containing the maze structure to traverse.
            entry: Coordinates of the starting cell as an (x, y) tuple.
            end: Coordinates of the destination cell as an (x, y) tuple.

        Returns:
            A list of coordinates from entry to end, or an empty list if
            no valid path exists.
        """
        # deque is more efficient O(1) than list O(n)
        # for front pops.
        queue: deque[tuple[int, int]] = deque([entry])

        # Dictionary tracking which cell we came from.
        # Saves memory.
        came_from: dict[
            tuple[int, int],
            tuple[int, int] | None,
        ] = {entry: None}

        while queue:
            current = queue.popleft()

            if current == end:
                return Solver._reconstruct_path(came_from, current)

            cx, cy = current
            # Equivalent to '.walls' if renamed.
            walls = grid[cx, cy].lista

            # Evaluate accessible neighbors: (walls & Wall) == 0 means open.
            valid_moves: list[tuple[int, int]] = []
            if not (walls & Walls.norte):
                valid_moves.append((cx, cy - 1))
            if not (walls & Walls.sur):
                valid_moves.append((cx, cy + 1))
            if not (walls & Walls.este):
                valid_moves.append((cx + 1, cy))
            if not (walls & Walls.oeste):
                valid_moves.append((cx - 1, cy))

            for next_cell in valid_moves:
                if next_cell not in came_from:
                    came_from[next_cell] = current
                    queue.append(next_cell)

        return []

    @staticmethod
    def _reconstruct_path(
        came_from: dict[tuple[int, int], tuple[int, int] | None],
        current: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Reconstruct a path from the destination back to the start.

        Follow the recorded previous position for each visited cell until
        reaching the starting cell, then reverse the collected coordinates
        so the path is returned in traversal order.

        Args:
            came_from: Mapping of each visited cell to the cell it came from.
            current: Coordinates of the destination cell.

        Returns:
            A list of coordinates ordered from the start cell to the
            destination cell.
        """
        path: list[tuple[int, int]] = []
        # Continue while the current value is not None (the start cell)
        while current is not None:
            path.append(current)
            current = came_from[current]  # type: ignore[assignment]

        return path[::-1]
