from mazegen.grid import Grid


class MazeEncoder:
    """Clase encargada de serializar y guardar estructuras Grid en archivos."""

    @staticmethod
    def cell_to_hex(cell_value: int) -> str:
        """Convierte el valor entero de los muros de una celda a su dígito hexadecimal."""
        return f"{cell_value:x}"

    @classmethod
    def encode_grid(cls, grid: Grid) -> list[str]:
        """
        Serializa la cuadrícula en una lista de cadenas hexadecimales por fila.
        
        Nota: Se recorre fila a fila (y) y columna a columna (x) según la disposición.
        """
        lines = []
        for y in range(grid.altura):
            row_str = ""
            for x in range(grid.anchura):
                cell = grid.grid[x][y]
                # cell.lista contiene el IntFlag de Walls (valor de 0 a 15)
                row_str += cls.cell_to_hex(cell.lista.value)
            lines.append(row_str)
        return lines

    @classmethod
    def save_to_file(
        cls,
        grid: Grid,
        filepath: str,
        entry: tuple[int, int] | None = None,
        end: tuple[int, int] | None = None,
        solution_path: str | None = None,
    ) -> None:
        """
        Escribe la representación serializada del laberinto en el archivo especificado.
        """
        hex_lines = cls.encode_grid(grid)

        with open(filepath, "w", encoding="utf-8") as f:
            # Si el formato requiere cabeceras con metadata:
            f.write(f"# Dimensions: {grid.anchura}x{grid.altura}\n")
            if entry and end:
                f.write(f"# Entry: {entry[0]},{entry[1]} | Exit: {end[0]},{end[1]}\n")
            if solution_path:
                f.write(f"# Solution: {solution_path}\n")
            
            # Escribir la matriz de celdas
            for line in hex_lines:
                f.write(line + "\n")
