from .base import Renderer


class ascii_renderer(Renderer):
    def draw_cell(self, position: tuple[int, int]) -> None:
        """
            Lo que quiero hacer es pintar celda a celda
        """
        y, x = position
        celda = self.matriz.grid[y][x]
        if celda.lista & Walls.norte:
