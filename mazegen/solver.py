from collections import deque

from mazegen.grid import Grid, Walls


class Solver:
    """Implements pathfinding algorithms for Grid matrices."""

    @staticmethod
    def find_path(
        grid: Grid, entry: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        Finds the path from entry to end using BFS.
        Returns a list of coordinates from the start to the finish,
        or an empty list if no solution exists.
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
        """Rebuilds the path from the end back to the start and reverses it."""
        path: list[tuple[int, int]] = []
        # Continue while the current value is not None (the start cell)
        while current is not None:
            path.append(current)
            current = came_from[current]  # type: ignore[assignment]

        return path[::-1]
