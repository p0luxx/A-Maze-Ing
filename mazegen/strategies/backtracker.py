from .base import GenerationStrategy


class RecursiveBacktrackerStrategy(GenerationStrategy):
    def generate(self, grid: Grid, seed: int, start_gen: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
        #all_coordinates:list[tuple[int, int]] = [[x, y for y in self.grid.altura]]
        pass
