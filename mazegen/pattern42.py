from mazegen.grid import Grid


def apply_pattern42(grid: Grid) -> None:
    """Overlays the semi-open "42" logo in the center of the maze.

    Aligns a 9x5 binary matrix at the center of the board and blocks the
    marked cells (`blocked = True`). This version keeps the usual outline of
    the number 2 while opening the upper quadrant of the 4, preventing closed
    regions or blind cavities that could trap the backtracking generator or
    block pathfinding.

    Requires a free perimeter margin of at least 1 cell on each edge
    (minimum board size 11x7) so the path can wrap around the figure.

    Args:
        grid: Grid instance to modify in-place.

    Raises:
        ValueError: If the width is below 11 or the height is below 7 cells.
    """
    pattern_str = [
        "100001111",  # Row 0: left stem of the 4 | top bar of the 2
        "100000001",  # Row 1: left stem of the 4 | right stroke of the 2
        "111101111",  # Row 2: crossbar of the 4 | center bar of the 2
        "001001000",  # Row 3: leg of the 4 | left stroke of the 2
        "001001111",  # Row 4: leg of the 4 | base of the 2
    ]

    pattern = [[int(char) for char in row] for row in pattern_str]
    p_width = 9
    p_height = 5

    # Mandatory perimeter margin to guarantee space around the mask
    min_width = p_width + 2
    min_height = p_height + 2

    if grid.anchura < min_width or grid.altura < min_height:
        raise ValueError(
            "Insufficient dimensions "
            f"({grid.anchura}x{grid.altura}) for pattern 42. "
            f"A minimum size of {min_width}x{min_height} is required."
        )

    start_x = (grid.anchura - p_width) // 2
    start_y = (grid.altura - p_height) // 2

    for dy in range(p_height):
        for dx in range(p_width):
            if pattern[dy][dx] == 1:
                grid[start_x + dx, start_y + dy].blocked = True
