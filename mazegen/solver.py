from collections import deque

from mazegen.grid import Grid, Walls


class Solver:
    """Implementa algoritmos de resolución para matrices Grid."""

    @staticmethod
    def find_path(
        grid: Grid, entry: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        Encuentra el camino desde entry hasta end usando BFS.
        Retorna una lista de coordenadas desde el inicio hasta el final,
        o una lista vacía si no existe solución.
        """
        # deque es mucho más eficiente O(1) que una lista O(n) para extraer del inicio
        queue: deque[tuple[int, int]] = deque([entry])

        # Diccionario para rastrear de qué celda venimos. Ahorra mucha memoria.
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {entry: None}

        while queue:
            current = queue.popleft()

            if current == end:
                return Solver._reconstruct_path(came_from, current)

            cx, cy = current
            walls = grid[cx, cy].lista  # O '.walls' si lo renombraste

            # Evaluar vecinos accesibles: (walls & Muro) == 0 indica paso libre
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
        """Reconstruye el camino desde el final hasta el principio y lo invierte."""
        path: list[tuple[int, int]] = []
        # Mientras el valor actual no sea None (la celda de inicio)
        while current is not None:
            path.append(current)
            current = came_from[current]  # type: ignore[assignment]

        return path[::-1]
