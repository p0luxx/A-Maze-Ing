from abc import ABC, abstractmethod
from collections.abc import Generator

from mazegen.grid import Grid


class GenerationStrategy(ABC):
    @abstractmethod
    def generate(
        self, grid: Grid, seed: int, start_gen: tuple[int, int]
    ) -> Generator[tuple[int, int], None, None]:
        """Abstract generation method that yields cells step by step."""
        ...
