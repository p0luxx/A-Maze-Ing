import os
from abc import ABC, abstractmethod
from collections.abc import Generator
from enum import Enum

from mazegen.grid import Grid


class WallColor(str, Enum):
    """Paleta de códigos de escape ANSI para colorear muros en terminal."""

    CYAN = "\033[36m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"


class Renderer(ABC):
    """Interfaz base abstracta para los motores de renderizado del laberinto.

    Define el contrato obligatorio para dibujar el tablero y animar algoritmos
    paso a paso, además de centralizar el control de color de las paredes y la
    limpieza de la consola.

    Attributes:
        matriz: Cuadrícula (`Grid`) con las celdas y muros actuales.
        entry: Coordenadas `(x, y)` del punto de inicio.
        exit: Coordenadas `(x, y)` del punto de salida.
        wall_color: Color ANSI activo para las paredes.
    """

    def __init__(self, grid: Grid, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        """Inicializa el renderizador con la cuadrícula base y los extremos.

        Args:
            grid: Tablero con las celdas y paredes a representar.
            entry: Tupla `(x, y)` con el origen.
            exit: Tupla `(x, y)` con el destino.
        """
        self.matriz: Grid = grid
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.wall_color: WallColor = WallColor.CYAN

    def clear_screen(self) -> None:
        """Limpia el búfer visible de la terminal según la plataforma."""
        os.system("cls" if os.name == "nt" else "clear")

    @abstractmethod
    def draw_grid(self, path: list[tuple[int, int]] | None = None) -> None:
        """Renderiza una vista estática del laberinto en su estado vigente.

        Args:
            path: Lista secuencial opcional de coordenadas a resaltar como solución.
        """
        ...

    @abstractmethod
    def live_animation(
        self,
        generator: Generator[tuple[int, int], None, None],
        path: list[tuple[int, int]] | None = None,
        delay: float = 0.05,
    ) -> None:
        """Consume un generador para dibujar y refrescar cada paso en pantalla.

        Args:
            generator: Iterador que produce las coordenadas procesadas por el algoritmo.
            path: Ruta opcional a superponer durante la animación.
            delay: Intervalo de pausa en segundos entre cada fotograma.
        """
        ...

    def ChangeColor(self) -> None:
        """Avanza cíclicamente a la siguiente paleta de color definida en `WallColor`."""
        colors: list[WallColor] = list(WallColor)
        current = colors.index(self.wall_color)
        next_color = (current + 1) % len(colors)
        self.wall_color = colors[next_color]