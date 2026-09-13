from mazegen.grid import Grid


def apply_pattern42(grid: Grid) -> None:
    """Superpone el logotipo "42" con silueta semiabierta en el centro del laberinto.

    Alinea una matriz binaria de 9x5 en el centro del tablero y bloquea las
    celdas marcadas (`blocked = True`). Esta versión conserva el contorno
    habitual del número 2 pero abre el cuadrante superior del 4, impidiendo
    que se formen regiones cerradas o cavidades ciegas que puedan atrapar al
    generador por retroceso o bloquear la resolución.

    Requiere un margen perimetral libre de al menos 1 celda en cada borde
    (tablero mínimo de 11x7) para que el trazado pueda rodear la figura.

    Args:
        grid: Instancia de la cuadrícula a modificar in-place.

    Raises:
        ValueError: Si el ancho es inferior a 11 o la altura es inferior a 7 celdas.
    """
    pattern_str = [
        "100001111",  # Fila 0: Palo izq. del 4 | Barra superior del 2
        "100000001",  # Fila 1: Palo izq. del 4 | Trazo derecho del 2
        "111101111",  # Fila 2: Barra transversal del 4 | Barra central del 2
        "001001000",  # Fila 3: Pata del 4 | Trazo izquierdo del 2
        "001001111",  # Fila 4: Pata del 4 | Base del 2
    ]

    pattern = [[int(char) for char in row] for row in pattern_str]
    p_width = 9
    p_height = 5

    # Margen perimetral obligatorio para garantizar paso alrededor de la máscara
    min_width = p_width + 2
    min_height = p_height + 2

    if grid.anchura < min_width or grid.altura < min_height:
        raise ValueError(
            f"Dimensiones insuficientes ({grid.anchura}x{grid.altura}) para el patrón 42. "
            f"Se requiere un tamaño mínimo de {min_width}x{min_height}."
        )

    start_x = (grid.anchura - p_width) // 2
    start_y = (grid.altura - p_height) // 2

    for dy in range(p_height):
        for dx in range(p_width):
            if pattern[dy][dx] == 1:
                grid[start_x + dx, start_y + dy].blocked = True