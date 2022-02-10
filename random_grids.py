import random
from math import ceil
import astar

verticies = []


# returns true if a path exists and false if it doesn't
def checkPath(fileName):
    global columns
    global rows

    # opens the file and puts its information on a string
    f = open(fileName, "r")
    file = f.read()
    fNums = file.split()
    f.close()

    # read the start, goal, and total columns and rows from the file
    fIndex = 0
    sx = int(fNums[fIndex])
    fIndex += 1
    sy = int(fNums[fIndex])
    fIndex += 1
    gx = int(fNums[fIndex])
    fIndex += 1
    gy = int(fNums[fIndex])
    fIndex += 1
    columns = int(fNums[fIndex])
    fIndex += 1
    rows = int(fNums[fIndex])
    fIndex += 1

    goal = (gx, gy)
    start = (sx, sy)

    # creates each of the vertices in the grid
    # to access a point: verticies[(columns+1) * (y-1) + (x-1)]
    for j in range(rows + 1):
        for i in range(columns+1):
            singleVertetx = astar.point(i+1, j+1, False, float('inf'), astar.H(goal, (i+1, j+1)), None)
            verticies.append(singleVertetx)

    # determines weather each cell is blocked, based on the file
    for i in range(columns):
        for j in range(rows):
            blockX = int(fNums[fIndex])
            fIndex += 1
            blockY = int(fNums[fIndex])
            fIndex += 1
            on = int(fNums[fIndex])
            fIndex += 1
            verticies[(columns+1) * (blockY-1)+ (blockX-1)].b = on == 1

    # runs either a* or theta* to find the shortest path between the start vertex and the goal vertex
    return astar.checkPath(verticies, verticies[(columns+1) * (goal[1]-1) + (goal[0]-1)], verticies[(columns+1) * (start[1]-1) + (start[0]-1)], columns, rows)


def makeRandomGrids(columns, rows, amount):
    for i in range(1, amount+1):
        fileName = "grids/grid{}.txt"
        f = open(fileName.format(i), 'w')
        firstThree = "{} {}\n"
        sx = random.randrange(1, columns+1)
        sy = random.randrange(1, rows+1)
        gx = sx
        gy = sy
        while gx == sx and gy == sy:
            gx = random.randrange(1, columns+1)
            gy = random.randrange(1, rows+1)
        f.write(firstThree.format(sx, sy))
        f.write(firstThree.format(gx, gy))
        f.write(firstThree.format(columns, rows))
        restOfTheLines = "{} {} {}{}"
        blockedNum = ceil((rows * columns) / 10)
        blockedCells = set()
        while len(blockedCells) < blockedNum:
            blockedCells.add(random.randrange(1, (rows * columns)+1))
        for j in range(1, columns+1):
            for k in range(1, rows+1):
                blocked = (rows * (j-1) + k) in blockedCells
                f.write(restOfTheLines.format(j, k, int(blocked), "\n"))
        f.close()
        if not checkPath(fileName.format(i)):
            i -= 1
