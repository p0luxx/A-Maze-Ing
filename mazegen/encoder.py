from mazegen.grid import Grid


class MazeEncoder:
    """Serializador de laberintos conforme a la especificación del subject.

    Codifica el estado topológico de la cuadrícula en cadenas hexadecimales por
    fila a partir de las máscaras de bits de cada celda, traduce la secuencia de
    coordenadas de la solución a pasos cardinales (N, E, S, W) y persiste el mapa
    en el formato de archivo de texto estructurado requerido.
    """

    @staticmethod
    def cell_to_hex(cell_value: int) -> str:
        """Convierte la máscara de bits entera de una celda en su dígito hexadecimal en minúscula.

        Args:
            cell_value: Valor entero (0 a 15) resultante de la combinación de banderas de muros.

        Returns:
            Carácter hexadecimal individual ('0' a 'f').
        """
        return f"{cell_value:x}"

    @classmethod
    def encode_grid(cls, grid: Grid) -> list[str]:
        """Serializa la matriz de celdas en una lista de cadenas de texto, una por fila.

        Recorre el tablero de arriba a abajo e izquierda a derecha extrayendo el
        valor entero de la propiedad `lista` de cada celda para formatearlo en hexadecimal.

        Args:
            grid: Instancia de la cuadrícula a codificar.

        Returns:
            Lista de líneas de texto donde cada carácter representa la configuración
            de muros de una celda.
        """
        lines = []
        for y in range(grid.altura):
            row_str = ""
            for x in range(grid.anchura):
                cell = grid[x, y]
                row_str += cls.cell_to_hex(cell.lista.value)
            lines.append(row_str)
        return lines

    @staticmethod
    def path_to_directions(path: list[tuple[int, int]]) -> str:
        """Traduce una lista ordenada de coordenadas contiguas a una cadena de pasos cardinales.

        Compara pares sucesivos `(x1, y1)` y `(x2, y2)` para inferir el vector
        de movimiento unitario y convertirlo a caracteres 'N', 'E', 'S' o 'W'.

        Args:
            path: Lista secuencial de tuplas `(x, y)` que representan la ruta óptima.

        Returns:
            Cadena de caracteres cardinales (e.g., "EESSNNW"). Devuelve una cadena
            vacía si la ruta tiene menos de dos nodos.
        """
        directions = []
        for i in range(len(path) - 1):
            cx, cy = path[i]
            nx, ny = path[i + 1]
            if ny < cy:
                directions.append("N")
            elif nx > cx:
                directions.append("E")
            elif ny > cy:
                directions.append("S")
            elif nx < cx:
                directions.append("W")
        return "".join(directions)

    @classmethod
    def save_to_file(
        cls,
        grid: Grid,
        filepath: str,
        entry: tuple[int, int],
        end: tuple[int, int],
        solution_path: list[tuple[int, int]] | None = None,
    ) -> None:
        """Guarda la representación canónica del laberinto en el sistema de archivos.

        Escribe el fichero siguiendo la estructura estricta del proyecto:
        1. Filas hexadecimales del tablero.
        2. Línea en blanco obligatoria como separador.
        3. Coordenadas de entrada `x,y`.
        4. Coordenadas de salida `x,y`.
        5. Cadena de direcciones cardinales de la ruta resuelta (o salto de línea si no existe).

        Args:
            grid: Tablero con la configuración de muros definitiva.
            filepath: Ruta de destino del archivo a escribir.
            entry: Coordenadas `(x, y)` del punto de partida.
            end: Coordenadas `(x, y)` del punto de llegada.
            solution_path: Lista ordenada opcional con la solución calculada por el solver.
        """
        hex_lines = cls.encode_grid(grid)
        with open(filepath, "w", encoding="utf-8") as f:
            for line in hex_lines:
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{end[0]},{end[1]}\n")

            if solution_path:
                dirs = cls.path_to_directions(solution_path)
                f.write(dirs + "\n")
            else:
                f.write("\n")