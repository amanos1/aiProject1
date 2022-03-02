import heapq
import math
from typing import List, Any
rows = 3
columns = 5


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

fringe = []
closed = set()


# calculates the straight-line distance between two points
def H(g, p):
    xdiff = math.fabs(p[0] - g[0])
    ydiff = math.fabs(p[1] - g[1])
    return math.sqrt(math.pow(xdiff, 2) + math.pow(ydiff, 2))


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


def succ(verts, p):
    s = set()
    i = (p.x-1) + (columns+1) * (p.y-1)
    u = False
    l = False
    r = False
    d = False

    # horizontal/vertical points
    if p.x > 1:
        if not (isBlocked(verts, i-1, columns) and isBlocked(verts, i-columns-2, columns)):
            s.add(verts[i-1])
            l = True
    if p.x <= columns:
        if not (isBlocked(verts, i, columns) and isBlocked(verts, i-columns-1, columns)):
            s.add(verts[i+1])
            r = True
    if p.y > 1:
        if not (isBlocked(verts, i-columns-1, columns) and isBlocked(verts, i-columns-2, columns)):
            s.add(verts[i-columns-1])
            u = True
    if p.y <= rows:
        if not (isBlocked(verts, i, columns) and isBlocked(verts, i-1, columns)):
            s.add(verts[i+columns+1])
            d = True

    # diagonal points
    if u and l:
        if not isBlocked(verts, i-columns-2, columns):
            s.add(verts[i-columns-2])  # up left
    if l and d:
        if not isBlocked(verts, i-1, columns):
            s.add(verts[i+columns])  # down left
    if u and r:
        if not isBlocked(verts, i-columns-1, columns):
            s.add(verts[i-columns])  # up right
    if d and r:
        if not isBlocked(verts, i, columns):
            s.add(verts[i+columns+2])  # down right
    return s


def thetaStar(goal, start, verts):
    g = goal
    start.setG(0)
    start.setP(start)
    heapq.heapify(fringe)
    heapq.heappush(fringe, start)
    while fringe:
        s = heapq.heappop(fringe)
        if s.x == g.x and s.y == g.y:
            return True
        closed.add(s)
        for sstar in succ(verts, s):
            if sstar not in closed:
                UpdateVertex(s, sstar, verts)
    return False


def UpdateVertex(s, sstar, verts):
    if LineOfSight(s.p, sstar, verts):
        if (s.p.g+C(s.p, sstar)) < sstar.g:
            sstar.g = s.p.g + C(s.p, sstar)
            sstar.p = s.p
            if sstar in fringe:
                heapq.heapify(fringe)
            else:
                heapq.heappush(fringe, sstar)
    else:
        if s.g + C(s, sstar) < sstar.g:
            sstar.g = s.g + C(s, sstar)
            sstar.p = s
            if sstar in fringe:
                heapq.heapify(fringe)
            else:
                heapq.heappush(fringe, sstar)


def grid(x, y, verts):
    return verts[(x-1) + (columns+1) * (y-1)].b


def LineOfSight(s, sstar, verts):
    x0 = int(s.x)
    y0 = int(s.y)
    x1 = int(sstar.x)
    y1 = int(sstar.y)
    f = int(0)
    dy = int(y1-y0)
    dx = int(x1-x0)
    sy = int(0)
    sx = int(0)
    if dy < 0:
        dy = -1*dy
        sy = -1
    else:
        sy = 1
    if dx < 0:
        dx = -1*dx
        sx = -1
    else:
        sx = 1
    if dx >= dy:
        while x0 != x1:
            f = f + dy
            if f >= dx:
                if grid(int(x0+((sx-1)/2)), int(y0+((sy-1)/2)), verts):
                    return False
                y0 = y0 + sy
                f = f - dx
            if f != 0 and grid(int(x0+((sx-1)/2)), int(y0+((sy-1)/2)), verts):
                return False
            if dy == 0 and grid(int(x0+((sx-1)/2)), int(y0),verts) and grid(int(x0+((sx-1)/2)), int(y0-1), verts):
                return False
            x0 = x0 + sx
    else:
        while y0 != y1:
            f = f + dx
            if f >= dy:
                if grid(int(x0+((sx-1)/2)), int(y0+((sy-1)/2)), verts):
                    return False
                x0 = x0 + sx
                f = f - dy
            if f != 0 and grid(int(x0+((sx-1)/2)), int(y0+((sy-1)/2)),verts):
                return False
            if dx == 0 and grid(int(x0), int(y0+((sy-1)/2)), verts) and grid(int(x0-1), int(y0+((sy-1)/2)), verts):
                return False
            y0 = y0 + sy
    return True


def search(verts, goal, start, col, row):
    global columns
    global rows
    columns = col
    rows = row
    nice = []
    if not thetaStar(goal, start, verts):
        return nice
    node = goal
    while not node.equals(start):
        nice.append(node)
        node = node.p
    nice.append(node)
    return nice
