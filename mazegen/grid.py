from enum import IntFlag


class Walls(IntFlag):
    norte = 1
    este = 2
    sur = 4
    oeste = 8


class Cell():
    def __init__(self):
        self.lista = Walls(15)


class Grid():
    def __init__(self, altura: int, anchura: int):
        self.grid = [[Cell() for _ in range(altura)] for _ in range(anchura)]


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
