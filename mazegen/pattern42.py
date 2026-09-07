from mazegen.grid import Grid


def apply_pattern42(grid: Grid) -> None:
    # Definimos el "42" como cadenas de texto para evitar que el formateador lo corrompa.
    # '1' representa celda bloqueada (muro de piedra inamovible)
    # '0' representa espacio transitable
    pattern_str = [
        "101001111",  # Fila 0
        "101000001",  # Fila 1
        "111101111",  # Fila 2
        "001001000",  # Fila 3
        "001001111"   # Fila 4
    ]
    
    # Convertimos las cadenas de texto a la matriz numérica real
    pattern = [[int(char) for char in row] for row in pattern_str]
    
    p_width = 9
    p_height = 5
    
    # Validar que el laberinto tenga tamaño suficiente para albergar la máscara
    min_width = p_width + 2
    min_height = p_height + 2
    
    if grid.anchura < min_width or grid.altura < min_height:
        raise ValueError(
            f"Dimensiones insuficientes ({grid.anchura}x{grid.altura}) para el patrón 42. "
            f"Se requiere un tamaño mínimo de {min_width}x{min_height}."
        )
    
    # FÓRMULA DE CENTRADO DINÁMICO:
    # Restamos las dimensiones del patrón a las del laberinto y dividimos por 2
    start_x = (grid.anchura - p_width) // 2
    start_y = (grid.altura - p_height) // 2
    
    # Marcar las celdas correspondientes en tu cuadrícula cartesiana [x, y]
    for dy in range(p_height):
        for dx in range(p_width):
            if pattern[dy][dx] == 1:
                # Usamos la sintaxis limpia [x, y] que creamos
                grid[start_x + dx, start_y + dy].blocked = True
