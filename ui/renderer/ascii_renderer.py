from .base import Renderer


class ascii_renderer(Renderer):
    def draw_grid(self, entry: tuple[int, int],
                  exit_: tuple[int, int],
                  path: list[tuple[int, int]] | None = None
                  ) -> None:
        ...

    def draw_cell(self, position: tuple[int, int]) -> None:
        ...
