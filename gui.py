from tkinter import *
import random_grids
import astar


columns = 0
rows = 0
verticies = []


def initPath(fileName):
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
    for i in range(columns+1):
        for j in range(rows+1):
            singleVertetx = astar.point(i, j, False, float('inf'), astar.H(goal, (i, j)), None)
            verticies.append(singleVertetx)

    for i in range(columns):
        for j in range(rows):
            blockY = int(fNums[fIndex])
            fIndex += 1
            blockX = int(fNums[fIndex])
            fIndex += 1
            on = int(fNums[fIndex])
            fIndex += 1
            verticies[rows * i + j].b = on == 1

    shortestPath = astar.search(verticies, verticies[rows * goal[0] + goal[1]], verticies[rows * start[0] + start[1]])

    return (goal, start), shortestPath


def displayPath(shortestPath, gs):
    s = gs[0]
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
            if verticies[rows * i + j].b:
                daCanvas.create_rectangle(j*10, i*10, (j*10)+10, (i*10)+10, fill="grey")

    daCanvas.create_oval((10*s[0])-3, (10*s[1])-3, (10*s[0])+3, (10*s[1])+3, fill="green")
    # daCanvas.create_text((10*sx)+20, (10*sy)+15, text="start", fill="black")
    daCanvas.create_oval((10*g[0])-3, (10*g[1])-3, (10*g[0])+3, (10*g[1])+3, fill="red")
    # daCanvas.create_text((10*gx)+20, (10*gy)+15, text="goal", fill="black")

    for i in range(1, len(shortestPath)):
        v1 = shortestPath[i-1]
        v2 = shortestPath[i]
        daCanvas.create_line((v1.x+1)*10, (v1.y+1)*10, (v2.x+1)*10, (v2.y+1)*10, fill="red")

    daCanvas.grid(row=0, columnspan=3)

    infoX = Entry(window)
    infoY = Entry(window)
    infoX.grid(row=1, column=0)
    infoY.grid(row=1, column=1)

    def getInfo():
        ix = int(infoX.get())
        iy = int(infoY.get())
        # print(ix, ", ", iy)
        vid = "Vertex ({}, {})"
        vg = "g = {}"
        vh = "h = {}"
        vf = "f = {}"
        infoLabel = Label(window, text=vid.format(ix, iy))
        ourVertex = verticies[rows * ix + iy]
        gLabel = Label(window, text=vg.format(ourVertex.g))
        hLabel = Label(window, text=vh.format(ourVertex.h))
        fLabel = Label(window, text=vf.format(int(ourVertex)))
        infoLabel.grid(row=2, column=1)
        gLabel.grid(row=3, column=1)
        hLabel.grid(row=4, column=1)
        fLabel.grid(row=5, column=1)

    infoButton = Button(window, text="Get Info", command=getInfo)
    infoButton.grid(row=1, column=2)

    window.mainloop()


def run(file):
    random_grids.makeRandomGrids(100, 50, 50)
    # gsp = goal, start, path
    gsp = initPath(file)
    displayPath(gsp[1], gsp[0])
