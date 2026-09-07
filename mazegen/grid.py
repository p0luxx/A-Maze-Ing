from enum import IntFlag


class Walls(IntFlag):
    norte = 1
    este = 2
    sur = 4
    oeste = 8


class Cell():
    def __init__(self):
        self.lista = Walls(15)
        self.blocked = False


class Grid():
    def __init__(self, altura: int, anchura: int):
        self.altura = altura
        self.anchura = anchura
        self._grid = [[Cell() for _ in range(altura)] for _ in range(anchura)]

    def __getitem__(self, position: tuple[int, int]) -> Cell:
        x, y = position
        if not (0 <= x < self.anchura and 0 <= y < self.altura):
            raise IndexError ("Grid dimensions are incorrect")
        return self._grid[x][y]

    def neighbours(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        conections: list[tuple[int, int]] = []
        if y > 0:
            conections.append((x, y - 1))
        if y < self.altura - 1:
            conections.append((x, y + 1))
        if x < self.anchura - 1:
            conections.append((x + 1, y))
        if x > 0:
            conections.append((x - 1, y))
        return conections
"""
if __name__ == "__main__":
    celda = Cell()
    print(celda.lista)
    print("Norte -> ", Walls.norte in celda.lista)
    print("Este -> ", Walls.este in celda.lista)
    print("Sur -> ", Walls.sur in celda.lista)
    print("Oeste -> ", Walls.oeste in celda.lista)
    print("\n\n")
    Matriz = Grid(2,2)
    print(Matriz)
    print("\n\n")
    for fila in Matriz.grid:
        for cell in fila:
            print(cell.lista)
"""
