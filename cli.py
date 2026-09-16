import time

from mazegen import MazeGenerator
from ui.config_loader import process_config
from ui.renderer.ascii_renderer import ascii_renderer


def main() -> None:
    """Punto de entrada interactivo para la generación y renderizado del laberinto.

    Carga los parámetros desde configuración/CLI, instancia el orquestador
    (`MazeGenerator`) y ejecuta un bucle interactivo de consola para regenerar
    tableros con semillas secuenciales, alternar la visualización del camino
    más corto, rotar las paletas de color y persistir la salida en disco.
    """
    config = process_config()
    if config is None:
        return

    # Semilla por defecto si no se definió por CLI o archivo
    current_seed = config.seed if config.seed is not None else 42

    maze_gen = MazeGenerator(
        width=config.width,
        height=config.height,
        seed=current_seed,
        entry=config.entry,
        end=config.exit,
        output_file=config.output_file,
        algorithm=config.algorithm,
        perfect=config.perfect,
    )

    renderer = ascii_renderer(
        grid=maze_gen.grid,
        entry=config.entry,
        exit=config.exit,
    )

    renderer.clear_screen()
    print("Iniciando generación animada...")
    time.sleep(0.5)
    renderer.live_animation(maze_gen.generate(), path=None, delay=0.05)
    print("\n¡Laberinto generado con éxito!")

    path = maze_gen.solve_and_export()
    print(f"Archivo exportado correctamente a: {config.output_file}")
    show_path = False

    while True:
        print(
            "\n=== A-Maze-ing ===\n"
            "1. Re-generate a new maze\n"
            "2. Show / Hide the shortest path\n"
            "3. Rotate the wall colours\n"
            "4. Quit"
        )
        option = input("Choice? (1-4): ").strip()

        match option:
            case "1":
                renderer.clear_screen()
                current_seed += 1

                # Reinstanciación completa para limpiar cuadrícula y estado interno
                maze_gen = MazeGenerator(
                    width=config.width,
                    height=config.height,
                    seed=current_seed,
                    entry=config.entry,
                    end=config.exit,
                    output_file=config.output_file,
                    algorithm=config.algorithm,
                    perfect=config.perfect,
                )
                renderer.matriz = maze_gen.grid
                renderer.live_animation(maze_gen.generate(), path=None, delay=0.05)

                path = maze_gen.solve_and_export()
                show_path = False

            case "2":
                renderer.clear_screen()
                show_path = not show_path
                route = path if show_path else None
                renderer.draw_grid(path=route)

            case "3":
                renderer.clear_screen()
                renderer.ChangeColor()
                route = path if show_path else None
                renderer.draw_grid(path=route)

            case "4":
                renderer.clear_screen()
                print("¡Hasta pronto!")
                break

            case _:
                renderer.clear_screen()
                print("Opción no válida. Por favor introduce un número del 1 al 4.")


if __name__ == "__main__":
    main()
