from typing import Generator

from mazegen.encoder import MazeEncoder
from mazegen.grid import Grid
from mazegen.pattern42 import apply_pattern42
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy
from mazegen.strategies.base import GenerationStrategy

from .solver import Solver

# from mazegen.exceptions import InvalidMazeError
# from mazegen.strategies.prim import RandomizedPrimStrategy
# from mazegen.modes.playable import PlayableMode

class MazeGenerator:
    """Orquestador principal para la generación y resolución de laberintos."""

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
        self.algorithm = algorithm

        self.grid = Grid(altura=self.height, anchura=self.width)
        self.check_parameters()

    def check_parameters(self) -> None:
        """Valida los parámetros de configuración iniciales."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Las dimensiones deben ser mayores que cero.")

        ex, ey = self.entry
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError("La entrada está fuera de los límites de la cuadrícula.")

        ox, oy = self.end
        if not (0 <= ox < self.width and 0 <= oy < self.height):
            raise ValueError("La salida está fuera de los límites de la cuadrícula.")

        if self.entry == self.end:
            raise ValueError("La entrada y la salida no pueden ser la misma celda.")

    def _select_strategy(self) -> GenerationStrategy:
        """Selecciona la estrategia de generación según el algoritmo indicado."""
        if self.algorithm == "backtracker":
            return IterativeBacktrackerStrategy()
        # elif self.algorithm == "prim":
        #     return RandomizedPrimStrategy()
        else:
            raise ValueError(f"Algoritmo desconocido: {self.algorithm}")

    def generate(self) -> Generator[tuple[int, int], None, None]:
        """
        Orquesta el proceso de generación cediendo (yield) los pasos intermedios.

        Permite a la interfaz de usuario consumir el generador para animaciones.
        """
        # 1. Aplicar máscara si aplica (ej. Pattern 42)
        apply_pattern42(self.grid)

        # 2. Ejecutar la estrategia de generación
        strategy = self._select_strategy()
        for step in strategy.generate(self.grid, seed=self.seed, start_gen=self.entry):
            yield step

        # 3. Aplicar post-procesado según el modo (perfect vs playable)
        if not self.perfect:
            # PlayableMode.apply(self.grid, seed=self.seed)
            pass

    def solve_and_export(self) -> None:
        """Resuelve el laberinto y guarda el resultado en el archivo especificado."""
        # 1. Obtener la solución llamando al solver
        path = Solver.find_path(self.grid, self.entry, self.end)
        # 2. Guardar llamando al encoder con argumentos explícitos
        MazeEncoder.save_to_file(
            grid=self.grid,
            filepath=self.output_file,
            entry=self.entry,
            end=self.end,
            solution_path=path,
        )

