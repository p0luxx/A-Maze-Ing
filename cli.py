import time

from mazegen import MazeGenerator
from ui.config_loader import process_config
from ui.renderer.ascii_renderer import ascii_renderer


def main() -> None:
    """Interactive entry point for maze generation and rendering.

    Loads the parameters from configuration/CLI, instantiates the orchestrator
    (`MazeGenerator`), and runs a console loop to regenerate boards with
    sequential seeds, toggle the shortest-path display, rotate color palettes,
    and persist the output to disk.
    """
    config = process_config()
    if config is None:
        return

    # Default seed if it was not defined by CLI or config file
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
    print("Starting animated generation...")
    time.sleep(0.5)
    renderer.live_animation(maze_gen.generate(), path=None, delay=0.05)
    print("\nMaze generated successfully!")

    path = maze_gen.solve_and_export()
    print(f"File exported successfully to: {config.output_file}")
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

                # Full re-instantiation to clear the grid and internal state
                config = process_config()
                if config is None:
                    return
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
                renderer.live_animation(
                    maze_gen.generate(),
                    path=None,
                    delay=0.05,
                )

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
                print("Goodbye!")
                break

            case _:
                renderer.clear_screen()
                print("Invalid option. Please enter a number from 1 to 4.")
