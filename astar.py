# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import heapq
import math
import bin_heap
from typing import List, Any


fringe = []
closed = set()


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


def H(g, p): #takes 2 tuples
    xdiff = math.fabs(p[0] - g[0])
    ydiff = math.fabs(p[1] - g[1])
    dist = math.sqrt(2) * min(xdiff, ydiff) + max(xdiff, ydiff) - min(xdiff, ydiff)
    return dist


def C(s1, s2):
    xdiff = math.fabs(s1.x - s2.x)
    ydiff = math.fabs(s1.y - s2.y)
    return math.sqrt(math.pow(xdiff, 2) + math.pow(ydiff, 2))


def isBlocked(verts, i, cols):
    if i < 0: return True
    if i > len(verts)-cols: return True  # it's on the last row
    return verts[i].b


def succ(verts, p, cols, row):
    s = set()
    i = (p.x-1) + (cols+1) * (p.y-1)
    u = False
    l = False
    r = False
    d = False
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


def Astar(verts, goal, start):
    start.setG(0)
    start.setP(start)
    heapq.heappush(fringe, start)
    while len(fringe) != 0:
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
            fringe.remove(sstar)
            heapq.heapify(fringe)
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
