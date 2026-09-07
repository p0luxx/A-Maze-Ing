import time
from mazegen.grid import Grid
from mazegen.pattern42 import apply_pattern42
from mazegen.solver import Solver
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy
from ui.renderer.ascii_renderer import ascii_renderer


def main():
    # 1. Dimensiones perfectas para lucir el patrón "42"
    # El patrón es de 9x5, así que un laberinto de 15x9 deja un pasillo precioso alrededor
    ancho = 12
    alto = 12
    seed = 42
    
    # 2. Puntos de entrada y salida fuera de la máscara (0,0 es perfecto)
    entry = (0, 0)
    exit_ = (ancho - 1, alto - 1)
    
    # 3. Inicializar la cuadrícula
    grid = Grid(altura=alto, anchura=ancho)
    
    # 4. ¡APLICAR LA MÁSCARA DEL "42"!
    # Bloqueamos las celdas del número antes de que empiece la generación
    apply_pattern42(grid)
    
    # 5. Configurar la estrategia de generación (Recursive Backtracker)
    strategy = IterativeBacktrackerStrategy()
    
    # IMPORTANTE: Empezamos a generar desde la entrada (0, 0), que está libre,
    # NUNCA desde el centro (5, 5) que está bloqueado por el "42"
    generador = strategy.generate(grid=grid, seed=seed, start_gen=entry)
    
    # 6. Instanciar el renderizador optimizado
    renderer = ascii_renderer(grid=grid, entry=entry, exit_=exit_)
    
    print("Iniciando generación animada del patrón 42...")
    time.sleep(1)
    
    # 7. Mostrar la animación de generación en vivo (súper rápida)
    renderer.live_animation(generador, path=None, delay=0.1)
    
    print("\n¡Laberinto con el patrón 42 generado con éxito!")
    print("Calculando la ruta de resolución...")
    time.sleep(1.5)
    
    # 8. Resolver el laberinto usando el solver BFS
    # El solver buscará el camino más corto esquivando el "42" central
    path = Solver.find_path(grid=grid, entry=entry, end=exit_)
    
    # 9. Mostrar la resolución animada paso a paso
    renderer.clear_screen()
    print("--- ANIMACIÓN DE RESOLUCIÓN ---")
    for i in range(1, len(path) + 1):
        renderer.clear_screen()
        print("--- BUSCANDO LA SALIDA ALREDEDOR DEL 42 ---")
        renderer.draw_grid(path=path[:i])
        time.sleep(0.05)
        
    print(f"\n¡Camino encontrado! Longitud: {len(path)} celdas.")

if __name__ == "__main__":
    main()
