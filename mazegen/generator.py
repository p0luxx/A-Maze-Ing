from typing import Generator

from mazegen.encoder import MazeEncoder
from mazegen.grid import Grid
from mazegen.modes.playable import PlayableMode
from mazegen.pattern42 import apply_pattern42
from mazegen.strategies.algorithms import (
    IterativeBacktrackerStrategy,
    Prim,
    RandomIterativeBacktrackerStrategy,
)
from mazegen.strategies.base import GenerationStrategy

from .solver import Solver


class MazeGenerator:
    """Main orchestrator for maze generation and resolution."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
        entry: tuple[int, int],
        end: tuple[int, int],
        output_file: str,
        perfect: bool = False,
        algorithm: str = "backtracker",
    ):
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.end = end
        self.output_file = output_file
        self.perfect = perfect
        self.algorithm = algorithm.lower()

        self.grid = Grid(altura=self.height, anchura=self.width)
        self.check_parameters()

    def check_parameters(self) -> None:
        """Validates the initial configuration parameters."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be greater than zero.")

        ex, ey = self.entry
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError("The entry is outside the grid bounds.")

        ox, oy = self.end
        if not (0 <= ox < self.width and 0 <= oy < self.height):
            raise ValueError("The exit is outside the grid bounds.")

        if self.entry == self.end:
            raise ValueError("The entry and exit cannot be the same cell.")

    def _select_strategy(self) -> GenerationStrategy:
        """Selects the generation strategy based on the requested algorithm."""
        algo = self.algorithm
        if algo == "backtracker":
            return IterativeBacktrackerStrategy()
        elif algo == "prim":
            return Prim()
        elif algo == "rdfs":
            return RandomIterativeBacktrackerStrategy()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def generate(self) -> Generator[tuple[int, int], None, None]:
        """
        Orchestrates the generation process by yielding intermediate steps.

        This allows the UI to consume the generator for animations.
        """
        # 1. Apply the mask when applicable (e.g. Pattern 42)
        apply_pattern42(self.grid)

        # 2. Run the generation strategy
        strategy = self._select_strategy()
        for step in strategy.generate(
            self.grid,
            seed=self.seed,
            start_gen=self.entry,
        ):
            yield step

        # 3. Apply post-processing depending on the mode (perfect vs playable)
        if not self.perfect:
            PlayableMode.apply(self.grid, seed=self.seed)

    def solve_and_export(self) -> list[tuple[int, int]]:
        """Solves the maze and saves the result to the specified file."""
        # 1. Obtain the solution by calling the solver
        path = Solver.find_path(self.grid, self.entry, self.end)
        # 2. Save by calling the encoder with explicit arguments
        MazeEncoder.save_to_file(
            grid=self.grid,
            filepath=self.output_file,
            entry=self.entry,
            end=self.end,
            solution_path=path,
        )
        return path
