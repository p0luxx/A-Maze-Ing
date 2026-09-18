import random
from collections.abc import Generator

from mazegen.grid import Grid, Walls

from .base import GenerationStrategy


class IterativeBacktrackerStrategy(GenerationStrategy):
    """Generate a maze using the iterative backtracking algorithm.

    Traverse the grid with an explicit stack, visiting unblocked cells
    and removing walls between connected neighbours. Use a seed to make
    the random generation reproducible.
    """
    def generate(
        self, grid: Grid, seed: int, start_gen: tuple[int, int]
    ) -> Generator[tuple[int, int], None, None]:
        """Generate maze passages with iterative depth-first backtracking.

        Start from the given cell, randomly choose unvisited and unblocked
        neighbours, remove the shared walls, and use a stack to backtrack
        when no valid neighbour remains. Yield positions as generation
        progresses.

        Args:
            grid: Grid instance modified in-place during maze generation.
            seed: Seed used to reproduce the random neighbour selection.
            start_gen: Coordinates of the cell where generation starts.

        Yields:
            Coordinates of the current cell as the algorithm advances or
            backtracks through the grid.
        """
        random.seed(seed)
        stack: list[tuple[int, int]] = [start_gen]
        visited: set[tuple[int, int]] = {start_gen}
        yield start_gen
        while stack:
            current = stack[-1]
            cx, cy = current
            unvisited_neighbours = [
                n for n in grid.neighbours(current)
                if n not in visited and not grid[n].blocked
            ]

            if unvisited_neighbours:
                nx, ny = random.choice(unvisited_neighbours)
                if ny < cy:
                    grid[cx, cy].lista &= ~Walls.norte
                    grid[nx, ny].lista &= ~Walls.sur
                elif ny > cy:
                    grid[cx, cy].lista &= ~Walls.sur
                    grid[nx, ny].lista &= ~Walls.norte
                elif nx > cx:
                    grid[cx, cy].lista &= ~Walls.este
                    grid[nx, ny].lista &= ~Walls.oeste
                elif nx < cx:
                    grid[cx, cy].lista &= ~Walls.oeste
                    grid[nx, ny].lista &= ~Walls.este
                visited.add((nx, ny))
                stack.append((nx, ny))
                yield (nx, ny)
            else:
                stack.pop()
                if stack:
                    yield stack[-1]


class RandomIterativeBacktrackerStrategy(GenerationStrategy):
    """Generate a maze using randomized iterative backtracking.

    Traverse the grid by selecting a random active cell from the stack,
    visiting unblocked neighbours and removing the shared walls between
    connected cells. Use a seed to make the random choices reproducible.
    """
    def generate(
        self, grid: Grid, seed: int, start_gen: tuple[int, int]
    ) -> Generator[tuple[int, int], None, None]:
        """Generate maze passages using randomized iterative backtracking.

        Start from the given cell and repeatedly select a random active cell
        from the stack. Connect it to a random unvisited neighbour when
        possible, or remove it from the stack when no valid move remains.

        Args:
            grid: Grid instance modified in-place during maze generation.
            seed: Seed used to reproduce the random cell and neighbour choices.
            start_gen: Coordinates of the cell where generation starts.

        Yields:
            Coordinates of cells visited or selected while generation
            progresses through the grid.
        """
        random.seed(seed)

        stack: list[tuple[int, int]] = [start_gen]
        visited: set[tuple[int, int]] = {start_gen}

        yield start_gen

        while stack:
            current = random.choice(stack)
            cx, cy = current

            unvisited_neighbours = [
                n for n in grid.neighbours(current)
                if n not in visited and not grid[n].blocked
            ]

            if unvisited_neighbours:
                nx, ny = random.choice(unvisited_neighbours)

                if ny < cy:
                    grid[cx, cy].lista &= ~Walls.norte
                    grid[nx, ny].lista &= ~Walls.sur

                elif ny > cy:
                    grid[cx, cy].lista &= ~Walls.sur
                    grid[nx, ny].lista &= ~Walls.norte

                elif nx > cx:
                    grid[cx, cy].lista &= ~Walls.este
                    grid[nx, ny].lista &= ~Walls.oeste

                elif nx < cx:
                    grid[cx, cy].lista &= ~Walls.oeste
                    grid[nx, ny].lista &= ~Walls.este

                visited.add((nx, ny))
                stack.append((nx, ny))

                yield (nx, ny)

            else:
                stack.remove(current)

                if stack:
                    yield random.choice(stack)


class Prim(GenerationStrategy):
    """Generate a maze using a randomized Prim-style strategy.

    Expand the maze from already visited cells by maintaining candidate
    cells on the frontier. Randomly select candidates, connect them to
    the existing maze, and use a seed to make generation reproducible.
    """
    def generate(
        self, grid: Grid, seed: int, start_gen: tuple[int, int]
    ) -> Generator[tuple[int, int], None, None]:
        """Generate maze passages using a randomized Prim-style process.

        Maintain visited cells and frontier candidates, randomly select an
        available unvisited cell, connect it to an already visited neighbour,
        and continue expanding until no active candidates remain.

        Args:
            grid: Grid instance modified in-place during maze generation.
            seed: Seed used to reproduce the random candidate selections.
            start_gen: Coordinates of the cell where generation starts.

        Yields:
            Coordinates of cells added to the generated maze as the
            algorithm progresses.
        """
        random.seed(seed)
        visited: set[tuple[int, int]] = {start_gen}
        active_candidates: list[tuple[int, int]] = [start_gen]
        available_neighbours: list[tuple[int, int]] = []
        yield start_gen
        while active_candidates:
            available_neighbours.extend(
                n for n in grid.neighbours(active_candidates[-1])
            )

            available_neighbours[:] = [
                n for n in available_neighbours
                if n not in visited and not grid[n].blocked
            ]

            if available_neighbours:
                current: tuple[int, int] = random.choice(available_neighbours)
                x, y = current

                valid_directions = self.get_valid_directions(current, visited)
                direction = random.choice(valid_directions)

                if direction == "a":
                    grid[x, y - 1].lista &= ~Walls.sur
                    grid[x, y].lista &= ~Walls.norte
                elif direction == "b":
                    grid[x, y].lista &= ~Walls.sur
                    grid[x, y + 1].lista &= ~Walls.norte
                elif direction == "c":
                    grid[x - 1, y].lista &= ~Walls.este
                    grid[x, y].lista &= ~Walls.oeste
                elif direction == "d":
                    grid[x, y].lista &= ~Walls.este
                    grid[x + 1, y].lista &= ~Walls.oeste

                available_neighbours.remove(current)
                visited.add(current)
                active_candidates.append(current)
                yield current
            else:
                active_candidates.pop()

    def get_valid_directions(
        self,
        current: tuple[int, int],
        visited: set[tuple[int, int]],
    ) -> list[str]:
        """Return directions that connect the current cell to visited cells.

        Check the four cardinal neighbours of the current position and
        collect the direction identifiers for those already present in the
        visited set.

        Args:
            current: Coordinates of the cell being evaluated.
            visited: Set containing coordinates of previously visited cells.

        Returns:
            A list of direction identifiers leading to visited neighbours.
        """
        directions: list[str] = []

        x, y = current

        if (x, y - 1) in visited:
            directions.append("a")

        if (x, y + 1) in visited:
            directions.append("b")

        if (x - 1, y) in visited:
            directions.append("c")

        if (x + 1, y) in visited:
            directions.append("d")

        return directions
