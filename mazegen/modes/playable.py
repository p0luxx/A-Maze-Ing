import random

from mazegen.grid import Grid, Walls


class PlayableMode:
    """Transforma un laberinto perfecto en uno imperfecto (braided).

    Elimina callejones sin salida (dead-ends) derribando muros al azar hacia
    vecinos transitables, generando ciclos alternativos que facilitan la
    jugabilidad y evitan frustración al explorar.
    """

    OPPOSITE_WALL = {
        Walls.norte: Walls.sur,
        Walls.sur: Walls.norte,
        Walls.este: Walls.oeste,
        Walls.oeste: Walls.este,
    }

    DIRECTION_OFFSETS = {
        Walls.norte: (0, -1),
        Walls.sur: (0, 1),
        Walls.este: (1, 0),
        Walls.oeste: (-1, 0),
    }

    @staticmethod
    def apply(grid: Grid, seed: int | None = None) -> None:
        """Detecta celdas sin salida y derriba una pared para crear bucles.

        Recorre la cuadrícula identificando celdas con exactamente tres paredes
        activas (callejones sin salida). Para cada una, selecciona al azar un
        muro colindante con una celda navegable dentro de los límites y actualiza
        las bitmasks de ambas celdas para abrir el paso.

        Args:
            grid: Instancia de la cuadrícula a modificar in-place.
            seed: Semilla opcional para reproducir la selección de muros derribados.
        """
        if seed is not None:
            random.seed(seed)

        for y in range(grid.altura):
            for x in range(grid.anchura):
                celda = grid[x, y]
                if celda.blocked:
                    continue

                # Recopila paredes cerradas que dan a celdas transitables dentro del mapa
                muros_cerrados = []
                for wall_flag, (dx, dy) in PlayableMode.DIRECTION_OFFSETS.items():
                    nx, ny = x + dx, y + dy
                    if (celda.lista & wall_flag) and (0 <= nx < grid.anchura and 0 <= ny < grid.altura):
                        if not grid[nx, ny].blocked:
                            muros_cerrados.append((wall_flag, nx, ny))

                # Un dead-end tiene exactamente 3 muros activos (1 sola salida)
                total_muros_activos = sum(
                    1 for w in (Walls.norte, Walls.sur, Walls.este, Walls.oeste)
                    if celda.lista & w
                )

                if total_muros_activos == 3 and muros_cerrados:
                    wall_to_remove, nx, ny = random.choice(muros_cerrados)

                    # Apertura bidireccional mediante operaciones a nivel de bits
                    celda.lista &= ~wall_to_remove
                    grid[nx, ny].lista &= ~PlayableMode.OPPOSITE_WALL[wall_to_remove]