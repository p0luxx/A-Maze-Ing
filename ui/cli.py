from ui.config_loader import process_config
from mazegen.grid import Grid # despues habira que quitar todos los imports y poner la clase mazegenerator pero por ahora para probar. 
from mazegen.pattern42 import apply_pattern42
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy
from ui.renderer.ascii_renderer import ascii_renderer
from mazegen.solver import Solver
import time

def cli() -> None:
   config =  process_config()
   grid = Grid(altura=config.height, anchura=config.width)
   apply_pattern42(grid)
   strategy = IterativeBacktrackerStrategy()
   generador = strategy.generate(grid=grid, seed=config.seed, start_gen=config.entry)
   renderer = ascii_renderer(grid=grid, entry=config.entry, exit=config.exit)
   print("Iniciando generación animada del patrón 42...")
   time.sleep(1)
   renderer.live_animation(generador, path=None, delay=0.1)
   print("\n¡Laberinto con el patrón 42 generado con éxito!")
   print("Calculando la ruta de resolución...")
   path = Solver.find_path(grid=grid, entry=config.entry, end=config.exit)
   renderer.clear_screen()
   print("--- ANIMACIÓN DE RESOLUCIÓN ---")
   renderer.live_animation(generador, path=path, delay=0.3)
   print(f"\n¡Camino encontrado! Longitud: {len(path)} celdas.")


if __name__ == "__main__":
    main()
