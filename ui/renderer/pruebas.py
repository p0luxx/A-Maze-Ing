from mazegen.grid import Grid, Walls

def ft_printeando():
    print("+---+")
    print("|   |")
    print("+---+")


Matriz = Grid(2,2)
print(Matriz)
for fila in Matriz.grid:
    for cell in fila:
        if cell.lista == 15:
            ft_printeando()

