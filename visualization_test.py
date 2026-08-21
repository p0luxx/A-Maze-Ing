import os
import time
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy
from mazegen.grid import Grid, Walls


class ConsoleUI:
    def __init__(self, grid: Grid):
        self.grid = grid

    def clear_screen(self):
        """Limpia la consola (compatible con Windows y Unix/Linux/Mac)"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, current_pos: tuple[int, int] | None = None):
        """Dibuja el laberinto en su estado actual."""
        lineas = []        
        for y in range(self.grid.altura):
            top_line = ""
            mid_line = ""
            for x in range(self.grid.anchura):
                celda = self.grid.grid[x][y]
                if celda.lista & Walls.norte:
                    top_line += "+---"
                else:
                    top_line += "+   "
                if celda.lista & Walls.oeste:
                    mid_line += "| "
                else:
                    mid_line += "  "
                if current_pos and current_pos == (x, y):
                    mid_line += "* "
                else:
                    mid_line += "  "
            top_line += "+"
            if self.grid.grid[self.grid.anchura - 1][y].lista & Walls.este:
                mid_line += "|"
            else:
                mid_line += " "
            lineas.append(top_line)
            lineas.append(mid_line)
        bottom_line = ""
        for x in range(self.grid.anchura):
            celda = self.grid.grid[x][self.grid.altura - 1]
            if celda.lista & Walls.sur:
                bottom_line += "+---"
            else:
                bottom_line += "+   "
        bottom_line += "+"
        lineas.append(bottom_line)
        print("\n".join(lineas))

    def animate_generation(self, generator, delay: float = 0.05):
        """Consume el generador y dibuja frame a frame."""
        for step in generator:
            self.clear_screen()
            self.render(current_pos=step)
            time.sleep(delay)
        self.clear_screen()
        self.render()
        print("\n¡Laberinto generado con éxito!")



def main():
    # 1. Crear una cuadrícula (ej. 15 de ancho x 10 de alto)
    grid = Grid(altura=5, anchura=10)
    # 2. Instanciar la interfaz y la estrategia
    ui = ConsoleUI(grid)
    strategy = IterativeBacktrackerStrategy()
    # 3. Iniciar el generador
    generador = strategy.generate(grid, seed=42, start_gen=(0, 0))
    # 4. Animar la generación (ajusta el delay para que vaya más rápido o más lento)
    ui.animate_generation(generador, delay=0.03)


if __name__ == "__main__":
    main()
