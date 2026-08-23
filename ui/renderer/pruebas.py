

def ft_printeando():
    print("+---+")
    print("|   |")
    print("+---+")

for i in range(3):
    print("*", end="")
    c = 0
    while (c <= 2):
        if c == 1:
            print("    ", end="")
        else:
            print("----", end="")
        print("*", end="")
        c += 1
    print()
    print("|", end="")
    for _ in range(3):
        print("    |", end="")
    print()
    if i == 2: #es decir si ha llegado al final, ponemos una de mas
        print("*", end="")
        for _ in range(3):
            print("----*", end="")
        
