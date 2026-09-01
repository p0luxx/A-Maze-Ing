import os
import time
from mazegen import MazeGenerator
from mazegen.grid import Grid, Walls
from mazegen.solver import Solver


class ConsoleUI:
    def __init__(self, grid: Grid, entry: tuple[int, int], end: tuple[int, int]):
        self.grid = grid
        self.entry = entry
        self.end = end

    def clear_screen(self):
        """Limpia la consola (compatible con Windows y Unix/Linux/Mac)."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, current_pos: tuple[int, int] | None = None, path: set[tuple[int, int]] | None = None):
        """Dibuja el laberinto con colores ANSI, bloques sólidos como trazo y marcas de inicio/fin."""
        path = path or set()
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

                pos = (x, y)
                if current_pos and current_pos == pos:
                    mid_line += "\033[35m* \033[0m"      # Magenta para el cursor actual
                elif pos == self.entry:
                    mid_line += "\033[32m██\033[0m"      # Verde brillante para la celda de salida (entry)
                elif pos == self.end:
                    mid_line += "\033[31m██\033[0m"      # Rojo brillante para la celda final (end)
                elif pos in path:
                    mid_line += "\033[36m██\033[0m"      # Cian en bloque para formar un trazo continuo
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
        """Consume el generador y dibuja frame a frame la creación."""
        for step in generator:
            self.clear_screen()
            self.render(current_pos=step)
            time.sleep(delay)
        self.clear_screen()
        self.render()
        print("\n\033[32m¡Laberinto generado con éxito!\033[0m")

    def animate_solution(self, path_coords: list[tuple[int, int]], delay: float = 0.05):
        """Dibuja el trazo del camino solucionador paso a paso."""
        current_path = set()
        for step in path_coords:
            current_path.add(step)
            self.clear_screen()
            self.render(current_pos=step, path=current_path)
            time.sleep(delay)
        self.clear_screen()
        self.render(path=current_path)
        print("\n\033[36m¡Laberinto resuelto con éxito!\033[0m")


def main():
    entry_pos = (0, 0)
    end_pos = (9, 4)

    # 1. Instanciar el orquestador
    maze = MazeGenerator(
        width=10,
        height=10,
        seed=42,
        entry=entry_pos,
        end=end_pos,
        output_file="maze.txt",
        algorithm="backtracker"
    )

    # 2. Instanciar la interfaz pasando las posiciones clave para los colores
    ui = ConsoleUI(maze.grid, entry=entry_pos, end=end_pos)

    # 3. Animar la generación
    generador = maze.generate()
    ui.animate_generation(generador, delay=0.03)

    time.sleep(0.5)

    # 4. Resolver el laberinto matemáticamente
    ruta_solucion = Solver.find_path(maze.grid, maze.entry, maze.end)

    # 5. Animar la solución visualmente con efecto de trazo
    if ruta_solucion:
        ui.animate_solution(ruta_solucion, delay=0.04)
    else:
        print("\nEl Solver no encontró un camino válido.")

    # 6. Guardar en el archivo de texto
    maze.solve_and_export()


if __name__ == "__main__":
    main()
