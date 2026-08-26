from mazegen.grid import Grid, Walls, Cell
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy

"""
El objetivo de esta prueba es realizar el laberinto sin garantizar la existencia de los muros exteriores
"""

def draw_grid(matriz: Grid) -> None:
    for y in range(matriz.altura):
        print("*", end="") #aqui pintamos las esquinas del norte.
        for x in range(matriz.anchura): #bucle para el muro del norte
            celda = matriz.grid[y][x] #Marco la celda.
            if celda.lista & Walls.norte:
                print("---", end="")
            else:
                print("   ", end="")
            print("*", end="") #el asterisco se imprime por separado
        print() #este print senyala el comienzo del medio (este y oeste)
        if matriz.grid[y][0].lista & Walls.oeste:
            print("|", end="")
        else:
            print(" ", end="")
        for x in range(matriz.anchura):
            celda = matriz.grid[y][x]
            print("   ", end="")
            if celda.lista & Walls.este: #Se supone que si en mi celda actual hay este en la sig hay oeste.
                print("|", end="")
            else:
                print(" ", end="")
        print()
        if y == matriz.altura - 1: #es decir si ha llegado al final, ponemos una de mas, la parte inferior.
            print("*", end="")
            for x in range(matriz.anchura):
                if matriz.grid[y][x].lista & Walls.sur:
                    print("---", end="")
                else:
                    print("   ", end="")
                print("*", end="") #el asterisco se imprime por separado
            print()
