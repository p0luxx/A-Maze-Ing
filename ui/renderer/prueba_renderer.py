from mazegen.grid import Grid, Walls, Cell
from mazegen.strategies.backtracker import IterativeBacktrackerStrategy


def draw_grid(matriz: Grid) -> None:
    largo = matriz.altura
    ancho = matriz.anchura
    for x in range(largo):
        print("*", end="") #aqui pintamos las esquinas del norte.
        for y in range(ancho): #bucle para el muro del norte
            celda = matriz.grid[x][y] #Marco la celda.
            if x == 0:
                print("---", end="")  #aqui controlamos que siempre se construya el muro exterior por el norte
            else:
                if celda.lista & Walls.norte:
                    print("---", end="")
                else:
                    print("   ", end="")
            print("*", end="") #el asterisco se imprime por separado
        print() #este print senyala el comienzo del medio (este y oeste)
        print("|", end="") #despues del bucle se imprime la primera pared
        for y in range(ancho): #bucle para los muros este-oeste
            celda = matriz.grid[x][y]
            print("   ", end="")
            if y == ancho - 1:
                print("|", end="") #para que siempre se pinte el final del muro este.
            else:
                if celda.lista & Walls.este: #Se supone que si en mi celda actual hay este en la sig hay oeste.
                    print("|", end="")
                else:
                    print(" ", end="")
        print()
        if x == largo - 1: #es decir si ha llegado al final, ponemos una de mas, la parte inferior.
            print("*", end="")
            for _ in range(ancho):
                print("---*", end="")
