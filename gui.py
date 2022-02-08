from tkinter import *
import random_grids
import astar


columns = 0
rows = 0
verticies = []


def initPath(fileName):
    global columns
    global rows

    f = open(fileName, "r")
    file = f.read()
    fNums = file.split()
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
    f.close()

    goal = (gx, gy)
    start = (sx, sy)

    # to access a vertex: verticies[columns * x + y]
    for j in range(rows + 1):
        for i in range(columns+1):
            singleVertetx = astar.point(i+1, j+1, False, float('inf'), astar.H(goal, (i+1, j+1)), None)
            verticies.append(singleVertetx)

    # to access a point: verticies[(columns+1) * (y-1) + (x-1)]
    for i in range(columns):
        for j in range(rows):
            blockX = int(fNums[fIndex])
            fIndex += 1
            blockY = int(fNums[fIndex])
            fIndex += 1
            on = int(fNums[fIndex])
            fIndex += 1
            verticies[(columns+1) * (blockY-1)+ (blockX-1)].b = on == 1

    shortestPath = astar.search(verticies, verticies[(columns+1) * (goal[1]-1) + (goal[0]-1)], verticies[(columns+1) * (start[1]-1) + (start[0]-1)], columns, rows)

    return (goal, start), shortestPath


def displayPath(shortestPath, gs):
    s = gs[1]
    g = gs[0]

    # creating the window
    window = Tk()
    window.title("Grid visualizer")

    daCanvas = Canvas(window, width=1020, height=520, bg="white")

    for i in range(1, columns + 2):
        daCanvas.create_line(i*10, 10, i*10, 510, fill="black")
        for j in range(1, rows + 2):
            if i == 1:
                daCanvas.create_line(10, j*10, 1010, j*10, fill="black")
            if verticies[(columns+1) * (j-1) + (i-1)].b:
                daCanvas.create_rectangle(i*10, j*10, (i*10)+10, (j*10)+10, fill="grey")

    daCanvas.create_oval((10*s[0])-3, (10*s[1])-3, (10*s[0])+3, (10*s[1])+3, fill="green")
    daCanvas.create_oval((10*g[0])-3, (10*g[1])-3, (10*g[0])+3, (10*g[1])+3, fill="red")

    for i in range(1, len(shortestPath)):
        v1 = shortestPath[i-1]
        v2 = shortestPath[i]
        daCanvas.create_line(v1.x*10, v1.y*10, v2.x*10, v2.y*10, fill="red")

    daCanvas.grid(row=0, columnspan=3)

    infoX = Entry(window)
    infoY = Entry(window)
    infoX.insert(0, "x value")
    infoY.insert(0, "y value")
    infoX.grid(row=1, column=0)
    infoY.grid(row=1, column=1)

    def getInfo():
        nothing = Label(window, text="")
        nothing.grid(row=2, column=1)
        nothing.grid(row=3, column=1)
        nothing.grid(row=4, column=1)
        nothing.grid(row=5, column=1)
        ix = int(infoX.get())
        iy = int(infoY.get())
        vid = "Vertex ({}, {})"
        vg = "g = {}"
        vh = "h = {}"
        vf = "f = {}"
        infoLabel = Label(window, text=vid.format(ix, iy))
        ourVertex = verticies[(columns+1) * (iy-1) + (ix-1)]
        gLabel = Label(window, text=vg.format(ourVertex.g))
        hLabel = Label(window, text=vh.format(ourVertex.h))
        fLabel = Label(window, text=vf.format(ourVertex.g + ourVertex.h))
        infoLabel.grid(row=2, column=1)
        gLabel.grid(row=3, column=1)
        hLabel.grid(row=4, column=1)
        fLabel.grid(row=5, column=1)

    infoButton = Button(window, text="Get Info", command=getInfo)
    infoButton.grid(row=1, column=2)

    window.mainloop()


def run(file):
    # random_grids.makeRandomGrids(100, 50, 50)
    # gsp = goal, start, path
    gsp = initPath(file)
    displayPath(gsp[1], gsp[0])
