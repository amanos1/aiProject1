import random
from math import ceil


def makeRandomGrids(columns, rows, amount):
    # for i in range(2, amount):
    fileName = "grid2.txt"
    f = open(fileName, 'w')
    firstThree = "{} {}\n"
    sx = random.randrange(1, rows+1)
    sy = random.randrange(1, columns+1)
    gx = sx
    gy = sy
    while gx == sx and gy == sy:
        gx = random.randrange(1, rows+1)
        gy = random.randrange(1, columns+1)
    f.write(firstThree.format(sx, sy))
    f.write(firstThree.format(gx, gy))
    f.write(firstThree.format(columns, rows))
    restOfTheLines = "{} {} {}{}"
    blockedNum = ceil((rows * columns) / 10)
    blockedCells = {"jope"}
    blockedCells.remove("jope")
    while len(blockedCells) < blockedNum:
        blockedCells.add(random.randrange(1, (rows * columns)+1))
    print(blockedCells)
    for j in range(1, columns+1):
        for k in range(1, rows+1):
            blocked = (rows * (j-1) + k) in blockedCells
            # print(rows * (j-1) + k, ", ", blocked)
            f.write(restOfTheLines.format(j, k, int(blocked), "\n"))
