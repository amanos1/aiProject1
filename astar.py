import heapq
import math


fringe = []
closed = set()


# Object that represents a single vertex
class point:
    def __init__(self, x, y, b, g, h, p):
        self.x = x
        self.y = y
        self.b = b
        self.g = g
        self.h = h
        self.p = p

    def setP(self, p):
        self.p = p

    def setG(self, g):
        self.g = g

    def setH(self, h):
        self.h = h

    def __lt__(self, other):
        return self.getF() < other.getF()

    def __int__(self):
        return self.g + self.h

    def getF(self):
        return self.g + self.h

    def __str__(self):
        return "c: " + str(self.x) + " " + str(self.y) + " " + str(self.b)

    def equals(self, p):
        return self.x == p.x and self.y == p.y


# calculates the h value of a vertex, takes 2 tuples
def H(g, p):
    xdiff = math.fabs(p[0] - g[0])
    ydiff = math.fabs(p[1] - g[1])
    dist = math.sqrt(2) * min(xdiff, ydiff) + max(xdiff, ydiff) - min(xdiff, ydiff)
    return dist


# calculates the straight-line distance between two points
def C(s1, s2):
    xdiff = math.fabs(s1.x - s2.x)
    ydiff = math.fabs(s1.y - s2.y)
    return math.sqrt(math.pow(xdiff, 2) + math.pow(ydiff, 2))


# returns whether or not a given cell is blocked
def isBlocked(verts, i, cols):
    if i < 0: return True
    if i > len(verts)-cols: return True  # it's on the last row
    return verts[i].b


# returns a list of the points surrounding p that can be travelled to
def succ(verts, p, cols, row):
    s = set()
    i = (p.x-1) + (cols+1) * (p.y-1)
    u = False
    l = False
    r = False
    d = False

    # horizontal/vertical points
    if p.x > 1:
        if not (isBlocked(verts, i-1, cols) and isBlocked(verts, i-cols-2, cols)):
            s.add(verts[i-1])
            l = True
    if p.x <= cols:
        if not (isBlocked(verts, i, cols) and isBlocked(verts, i-cols-1, cols)):
            s.add(verts[i+1])
            r = True
    if p.y > 1:
        if not (isBlocked(verts, i-cols-1, cols) and isBlocked(verts, i-cols-2, cols)):
            s.add(verts[i-cols-1])
            u = True
    if p.y <= row:
        if not (isBlocked(verts, i, cols) and isBlocked(verts, i-1, cols)):
            s.add(verts[i+cols+1])
            d = True

    # diagonal points
    if u and l:
        if not isBlocked(verts, i-cols-2, cols):
            s.add(verts[i-cols-2])  # up left
    if l and d:
        if not isBlocked(verts, i-1, cols):
            s.add(verts[i+cols])  # down left
    if u and r:
        if not isBlocked(verts, i-cols-1, cols):
            s.add(verts[i-cols])  # up right
    if d and r:
        if not isBlocked(verts, i, cols):
            s.add(verts[i+cols+2])  # down right
    return s


# executes the astar search
def Astar(verts, goal, start):
    start.setG(0)
    start.setP(start)
    heapq.heappush(fringe, start)
    while fringe:
        s = heapq.heappop(fringe)
        if s.equals(goal):
            return True
        closed.add(s)
        for sstar in succ(verts, s, columns, rows):
            if not (sstar in closed):
                UpdateVertex(s, sstar)
    return False


def UpdateVertex(s, sstar):
    if (s.g + C(s, sstar)) < sstar.g:
        sstar.setG(s.g + C(s, sstar))
        sstar.setP(s)
        if sstar in fringe:
            heapq.heapify(fringe)
        else:
            heapq.heappush(fringe, sstar)


def search(verts, goal, start, col, row):
    global columns
    global rows
    columns = col
    rows = row
    nice = []
    if not Astar(verts, goal, start):
        return nice
    node = goal
    while not node.equals(start):
        nice.append(node)
        node = node.p
    nice.append(node)
    return nice


def checkPath(verts, goal, start, col, row):
    global columns
    global rows
    columns = col
    rows = row
    return Astar(verts, goal, start)
