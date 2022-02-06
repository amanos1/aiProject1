from tkinter import *
from math import sqrt
import random_grids


class Vertex:
    def __init__(this, x, y):
        this.x = x
        this.y = y
        this.g = 0
        this.h = 0
        this.f = 0


def initPath(fileName):
    f = open(fileName, "r")
    startx = int(f.read(2))
    starty = int(f.read(2))
    goalx = int(f.read(2))
    goaly = int(f.read(2))
    columns = int(f.read(2))
    rows = int(f.read(2))
    f.close()

    print("columns: ", columns, "rows: ", rows)

    # to access a vertex: verticies[columns * x + y]
    for i in range(columns+1):
        for j in range(rows+1):
            print(columns * i + j)
            singleVertetx = Vertex(i, j)
            verticies.append(singleVertetx)

    for i in range(columns+1):
        for j in range(rows+1):
            # print(columns * i + j)
            """ verticies[columns * i + j].neighbors = []
            if i > 0:
                verticies[columns * i + j].neighbors.append(verticies[columns * (i - 1) + j])
                if j > 0:
                    verticies[columns * i + j].neighbors.append(verticies[columns * (i - 1) + (j - 1)])
                if j < rows:
                    verticies[columns * i + j].neighbors.append(verticies[columns * (i - 1) + (j + 1)])
            if i < columns:
                verticies[columns * i + j].neighbors.append(verticies[columns * (i + 1) + j])
                if j > 0:
                    verticies[columns * i + j].neighbors.append(verticies[columns * (i + 1) + (j - 1)])
                if j < rows:
                    verticies[columns * i + j].neighbors.append(verticies[columns * (i + 1) + (j + 1)])
            if j > 0:
                verticies[columns * i + j].neighbors.append(verticies[columns * i + (j - 1)])
            if j < rows:
                verticies[columns * i + j].neighbors.append(verticies[columns * i + (j + 1)]) """

    print(columns*2+2)
    path = [verticies[columns*1+3], verticies[columns*2+2], verticies[columns*2+1], verticies[columns*1+0]]
    return path


def displayPath(fileName, shortestPath):
    f = open(fileName, "r")
    sx = int(f.read(2))
    sy = int(f.read(2))
    gx = int(f.read(2))
    gy = int(f.read(2))
    columns = int(f.read(2))
    rows = int(f.read(2))

    def h(v):
        m1 = min(abs(v.x-gx), abs(v.y-gy))
        m2 = max(abs(v.x-gx), abs(v.y-gy))
        return sqrt(2) * m1 + m2 - m1

    for i in verticies:
        i.h = h(i)
        i.f = i.g + i.f

    # creating the window
    window = Tk()
    window.title("Grid visualizer")
    # window.geometry("500x500")

    daCanvas = Canvas(window, width=1020, height=520, bg="white")

    # daCanvas.create_line(x1, y1, x2, y2, fill="color")
    # daCanvas.create_rectangle(x1, y1, x2, y2, fill="color")
    # daCanvas.create_text()


    for i in range(1, columns + 2):
        daCanvas.create_line(i*10, 10, i*10, 500, fill="black")

    for i in range(1, rows + 2):
        daCanvas.create_line(10, i*10, 1000, i*10, fill="black")

    for i in range(rows * columns):
        blockY = int(f.read(2))
        blockX = int(f.read(2))
        on = int(f.read(2))
        if on == 1:
            daCanvas.create_rectangle(blockY*10, blockX*10, (blockY*10)+10, (blockX*10)+10, fill="grey")

    f.close()

    daCanvas.create_oval((10*sx)-5, (10*sy)-5, (10*sx)+5, (10*sy)+5, fill="black")
    daCanvas.create_text((10*sx)+20, (10*sy)+15, text="start", fill="black")
    daCanvas.create_oval((10*gx)-5, (10*gy)-5, (10*gx)+5, (10*gy)+5, fill="black")
    daCanvas.create_text((10*gx)+20, (10*gy)+15, text="goal", fill="black")

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
        print(ix, ", ", iy)
        vid = "Vertex ({}, {})"
        vg = "g = {}"
        vh = "h = {}"
        vf = "f = {}"
        infoLabel = Label(window, text=vid.format(ix, iy))
        ourVertex = verticies[columns * ix + iy]
        ourH = h(ourVertex)
        gLabel = Label(window, text=vg.format(ourVertex.g))
        hLabel = Label(window, text=vh.format(ourH))
        fLabel = Label(window, text=vf.format(ourVertex.g+ourH))
        infoLabel.grid(row=2, column=1)
        gLabel.grid(row=3, column=1)
        hLabel.grid(row=4, column=1)
        fLabel.grid(row=5, column=1)

    infoButton = Button(window, text="Get Info", command=getInfo)
    infoButton.grid(row=1, column=2)

    myLabel = Label(window, text="Geronimooo!")
    #myLabel.pack()

    window.mainloop()


verticies = []
random_grids.makeRandomGrids(100, 50, 12)
path = initPath("grid2.txt")
displayPath("grid2.txt", path)