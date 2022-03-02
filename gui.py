from tkinter import *
import astar
import thetastar


columns = 0
rows = 0
verticies = []


# creates the grid based on an input file
# and finds the shortest path between the start and goal vertices given in the file
def initPath(fileName, a):
    global columns
    global rows

    # opens the file and puts it's information on a string
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
            if a:
                singleVertetx = astar.point(i+1, j+1, False, float('inf'), astar.H(goal, (i+1, j+1)), None)
                verticies.append(singleVertetx)
            else:
                singleVertetx = thetastar.point(i+1, j+1, False, float('inf'), thetastar.H(goal, (i+1, j+1)), None)
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
    shortestPath = []
    if a:
        shortestPath = astar.search(verticies, verticies[(columns+1) * (goal[1]-1) + (goal[0]-1)], verticies[(columns+1) * (start[1]-1) + (start[0]-1)], columns, rows)
    else:
        shortestPath = thetastar.search(verticies, verticies[(columns+1) * (goal[1]-1) + (goal[0]-1)], verticies[(columns+1) * (start[1]-1) + (start[0]-1)], columns, rows)

    return (goal, start), shortestPath


# displays the grid and displays the given shortest path between the given start and goal points
def displayPath(shortestPath, gs):
    s = gs[1]
    g = gs[0]

    # creating the window
    window = Tk()
    window.title("Grid visualizer")
    daCanvas = Canvas(window, width=1020, height=520, bg="white")

    # drawing the grids and the blocked cells
    for i in range(1, columns + 2):
        daCanvas.create_line(i*10, 10, i*10, 510, fill="black")
        for j in range(1, rows + 2):
            if i == 1:
                daCanvas.create_line(10, j*10, 1010, j*10, fill="black")
            if verticies[(columns+1) * (j-1) + (i-1)].b:
                daCanvas.create_rectangle(i*10, j*10, (i*10)+10, (j*10)+10, fill="grey")

    # drawing the start and goal points
    daCanvas.create_oval((10*s[0])-4, (10*s[1])-4, (10*s[0])+4, (10*s[1])+4, fill="green")
    daCanvas.create_oval((10*g[0])-4, (10*g[1])-4, (10*g[0])+4, (10*g[1])+4, fill="red")

    # drawing the path returned by the a* or theta* function
    for i in range(1, len(shortestPath)):
        v1 = shortestPath[i-1]
        v2 = shortestPath[i]
        daCanvas.create_line(v1.x*10, v1.y*10, v2.x*10, v2.y*10, fill="red")

    daCanvas.grid(row=0, columnspan=3)

    # making the input boxes to get information about a single vertex
    infoX = Entry(window)
    infoY = Entry(window)
    infoX.insert(0, "x value")
    infoY.insert(0, "y value")
    infoX.grid(row=1, column=0)
    infoY.grid(row=1, column=1)

    # runs when the "get info" button is pressed. Displays a vertex's information.
    def getInfo():
        # deleting the previous point
        daCanvas.delete("infoPoint")

        # getting the vertex from the input fields
        ix = int(infoX.get())
        iy = int(infoY.get())

        vid = "Vertex ({}, {})"
        vg = "g = {}"
        vh = "h = {}"
        vf = "f = {}"

        if ix > columns or iy > rows or ix < 1 or iy < 1:
            return

        # display the information
        infoLabel = Label(window, text=vid.format(ix, iy))
        ourVertex = verticies[(columns+1) * (iy-1) + (ix-1)]
        gLabel = Label(window, text=vg.format(ourVertex.g))
        hLabel = Label(window, text=vh.format(ourVertex.h))
        fLabel = Label(window, text=vf.format(ourVertex.g + ourVertex.h))
        infoLabel.grid(row=2, column=1)
        gLabel.grid(row=3, column=1)
        hLabel.grid(row=4, column=1)
        fLabel.grid(row=5, column=1)

        point = daCanvas.create_oval((10*ix)-4, (10*iy)-4, (10*ix)+4, (10*iy)+4, fill="black", tags="infoPoint")
        # daCanvas.after(5000, daCanvas.delete("infoPoint"))

    # display the button that initiates the getInfo function
    infoButton = Button(window, text="Get Info", command=getInfo)
    infoButton.grid(row=1, column=2)

    # display the window
    window.mainloop()


def run(file, a):
    # gsp = goal, start, path
    gsp = initPath(file, a)
    displayPath(gsp[1], gsp[0])
