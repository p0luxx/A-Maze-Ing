from mazegen.grid import Grid


class MazeEncoder:
    """Maze serializer compliant with the subject specification.

    It encodes the grid's topological state into row-by-row hexadecimal strings
    derived from each cell's bitmasks, translates the solution's coordinate
    sequence into cardinal steps (N, E, S, W), and persists the map in the
    required structured text file format.
    """

    @staticmethod
    def cell_to_hex(cell_value: int) -> str:
        """Convert a cell bitmask to its lowercase hexadecimal digit.

        Args:
            cell_value: Integer value (0 to 15) from the combination of wall
                flags.

        Returns:
            A single hexadecimal character ('0' to 'f').
        """
        return f"{cell_value:x}"

    @classmethod
    def encode_grid(cls, grid: Grid) -> list[str]:
        """Serialize the grid into a list of text rows, one per row.

        Iterates from top to bottom and left to right, extracts the integer
        value from each cell's `lista` property, and formats it as hexadecimal.

        Args:
            grid: Instance of the grid to be encoded.

        Returns:
            A list of text lines where each character represents a cell's wall
            configuration.
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
        """Translate a path into a cardinal-direction string.

        Compares successive pairs `(x1, y1)` and `(x2, y2)` to infer the unit
        movement vector and convert it into 'N', 'E', 'S', or 'W'.

        Args:
            path: A sequential list of `(x, y)` tuples representing the optimal
                path.

        Returns:
            A string of cardinal characters (e.g., "EESSNNW"). Returns an empty
            string if the path contains fewer than two nodes.
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
        """Save the canonical maze representation to disk.

        Writes the file following the project's strict structure:
        1. Hexadecimal rows of the grid.
        2. Mandatory blank line as a separator.
        3. Entry coordinates `x,y`.
        4. Exit coordinates `x,y`.
        5. String of cardinal directions for the solved path, or a newline if
           none exists.

        Args:
            grid: Grid with the final wall configuration.
            filepath: Destination path for the file to be written.
            entry: `(x, y)` coordinates of the starting point.
            end: `(x, y)` coordinates of the ending point.
            solution_path: Optional ordered list containing the solution
                calculated by the solver.
        """
        hex_lines = cls.encode_grid(grid)
        try:
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
        except PermissionError as e:
            print(f"Error detected: {e}")
