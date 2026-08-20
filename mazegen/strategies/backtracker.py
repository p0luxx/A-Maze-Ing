import random
from collections.abc import Generator
from .base import GenerationStrategy
from mazegen.grid import Grid, Walls 


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
                n for n in grid.neighbours(current) if n not in visited
            ]

            if unvisited_neighbours:
                nx, ny = random.choice(unvisited_neighbours)
                if ny < cy:    
                    grid.grid[cx][cy].lista &= ~Walls.norte
                    grid.grid[nx][ny].lista &= ~Walls.sur
                elif ny > cy:  
                    grid.grid[cx][cy].lista &= ~Walls.sur
                    grid.grid[nx][ny].lista &= ~Walls.norte
                elif nx > cx:  
                    grid.grid[cx][cy].lista &= ~Walls.este
                    grid.grid[nx][ny].lista &= ~Walls.oeste
                elif nx < cx:  
                    grid.grid[cx][cy].lista &= ~Walls.oeste
                    grid.grid[nx][ny].lista &= ~Walls.este
                visited.add((nx, ny))
                stack.append((nx, ny))
                yield (nx, ny)
            else:
                stack.pop()
                if stack:
                    yield stack[-1]
