import random
from collections.abc import Generator

from mazegen.grid import Grid, Walls

from .base import GenerationStrategy


class IterativeBacktrackerStrategy(GenerationStrategy):
    def generate(
        self, grid: Grid, seed: int, start_gen: tuple[int, int]
    ) -> Generator[tuple[int, int], None, None]:
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
    def generate(
        self, grid: Grid, seed: int, start_gen: tuple[int, int]
    ) -> Generator[tuple[int, int], None, None]:
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
    def generate(
        self, grid: Grid, seed: int, start_gen: tuple[int, int]
    ) -> Generator[tuple[int, int], None, None]:
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
