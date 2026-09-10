from ui.config_loader import process_config
from mazegen.grid import Grid # despues habira que quitar todos los imports y poner la clase mazegenerator pero por ahora para probar. 
from mazegen.pattern42 import apply_pattern42
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy
from ui.renderer.ascii_renderer import ascii_renderer
from mazegen.solver import Solver
import time

def iniciacion() -> None:
    config =  process_config()
    grid = Grid(altura=config.height, anchura=config.width)
    apply_pattern42(grid)
    strategy = IterativeBacktrackerStrategy()
    generador = strategy.generate(grid=grid, seed=config.seed, start_gen=config.entry)
    renderer = ascii_renderer(grid=grid, entry=config.entry, exit=config.exit)
    print("Iniciando generación animada del patrón 42...")
    time.sleep(1)
    renderer.live_animation(generador, path=None, delay=0.01)
    print("\n¡Laberinto con el patrón 42 generado con éxito!")
    print("Calculando la ruta de resolución...")
    path = Solver.find_path(grid=grid, entry=config.entry, end=config.exit)
    
    flag = True
    while 1:
        print(
        "=== A-Maze-ing ===\n"
        "1. Re-generate a new maze\n"
        "2. Show / Hide the shortest path\n"
        "3. Rotate the wall colours\n"
        "4. Quit")
        option = input("Choice? (1-4): ").strip()
        match option:
            case "1":
                renderer.clear_screen()
                new_seed = config.seed + 1
                generador = strategy.generate(grid=grid, seed=new_seed, start_gen=config.entry)
                renderer.live_animation(generador, path=None, delay=0.01)
            case "2":
                renderer.clear_screen()
                flag = not flag
                if flag:
                    route = None
                else:
                    route = path
                renderer.draw_grid(path=route)
            case "3":
                renderer.ChangeColor()
                renderer.live_animation(generador, path=route, delay=0.01)
            case "4":
                renderer.clear_screen()
                break
            case _:
                renderer.clear_screen()
                print("bitch please!\n Porfavor pon del 1 al 4")
                


if __name__ == "__main__":
    iniciacion()
