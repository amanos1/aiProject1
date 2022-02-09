# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
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

fringe = []
closed = set()
def H(g, p):
    xdiff = math.fabs(p[0] - g[0])
    ydiff = math.fabs(p[1] - g[1])
    dist = math.sqrt(2)*min(xdiff, ydiff) + max(xdiff, ydiff) - min(xdiff, ydiff)
    return dist
def succ(verts, p):
    s = set()
    i = (p.x-1)+columns*(p.y-1)
    if p.x>1:
        if not verts[i-1].b:
            s.add(verts[i-1])
        l = True
    else:
        l = False
    if p.x<columns:
        if not verts[i].b:
            s.add(verts[i+1])
        r = True
    else:
        r = False
    if p.y>1:
        if not verts[i-columns].b:
            s.add(verts[i-columns])
        u = True
    else:
        u = False
    if p.y<rows:
        if not verts[i].b:
            s.add(verts[i+columns])
        d = True
    else:
        d = False

    if u and l:
        if not verts[i-(columns+1)].b:
            s.add(verts[i-(columns+1)])#up left
            s.add(verts[i-columns])#up
            s.add(verts[i-1])#left
    if l and d:
        if not verts[i-1].b:
            s.add(verts[i+4])#down left
            s.add(verts[i-1])#left
            s.add(verts[i+5])#down
    if u and r:
        if not verts[i-columns].b:
            s.add(verts[i-(columns-1)])#up right
            s.add(verts[i-columns])#up
            s.add(verts[i+1])#right
    if d and r:
        if not verts[i].b:
            s.add(verts[i+1])#right
            s.add(verts[i+(columns+1)])#down right
            s.add(verts[i+columns])#down
    return s
def Astar(verts,goal,start):
    g = goal
    start.setG(0)
    start.setP(start)
    heapq.heapify(fringe)
    heapq.heappush(fringe, start)
    while fringe:
        s = heapq.heappop(fringe)
        if s.x == g.x and s.y == g.y:
            return "path found"
        closed.add(s)
        for sstar in succ(verts,s):
            if sstar not in closed:
                if sstar not in fringe:
                    sstar.setG(float('inf'))
                    sstar.setP(None)
                UpdateVertex(verts,s,sstar)
    return "no path found"
def UpdateVertex(verts,s,sstar):
    if LineOfSight(verts,s.p, sstar):
        if (sstar.g+math.dist([s.p.x,s.p.y],[sstar.x,sstar.y]))<sstar.g:
            sstar.g = s.p.g + math.dist([s.p.x,s.p.y],[sstar.x,sstar.y])
            sstar.p = s.p
            if sstar in fringe:
                fringe.remove(sstar)
            heapq.heapify(fringe)
            heapq.heappush(fringe,sstar)
    else:
        if s.g + math.dist([s.x, s.y], [sstar.x, sstar.y]) < sstar.g:
            sstar.g = s.g + math.dist([s.x,s.y],[sstar.x,sstar.y])
            sstar.p = s
            if sstar in fringe:
                fringe.remove(sstar)
            heapq.heappush(fringe,sstar)
            heapq.heapify(fringe)
def grid(x,y,verts):
    return verts[(x - 1) + columns * (y - 1)].b
def LineOfSight(verts,s,sstar):
    x0 = int(s.x)
    y0 = int(s.y)
    x1 = int(sstar.x)
    y1 = int(sstar.y)
    f = 0
    dy = int(y1-y0)
    dx = int(x1-x0)
    if dy<0:
        dy = -1*dy
        s.y = -1
    else:
        s.y = 1
    if dx<0:
        dx = -1*dx
        s.x = -1
    else:
        s.x = 1
    if dx>=dy:
        while x0!=x1:
            f = f+dy
            if f<dx:
                if grid(int(x0+((s.x-1)/2)), int(y0+((s.y-1)/2)),verts):
                    return False
            y0 = y0+s.y
            f = f-dx
            if f!=0 and grid(int(x0+((s.x-1)/2)), int(y0+((s.y-1)/2)),verts):
                return False
            if dy==0 and grid(int(x0+((s.x-1)/2)), int(y0),verts) and grid(int(x0+((s.x-1)/2)), int(y0-1),verts):
                return False
            x0 = x0+s.x
    else:
        while y0!=y1:
            f = f+dx
            if f>=dy:
                if grid(int(x0+((s.x-1)/2)), int(y0+((s.y-1)/2)),verts):
                    return False
                x0 = x0 + s.x
                f = f-dy
            if f!=0 and grid(int(x0+((s.x-1)/2)), int(y0+((s.y-1)/2)),verts) and grid(int(x0-1), int(y0+((s.y-1)/2)),verts):
                return False
            y0 = y0+s.y
    return True
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    s = (4, 1)
    gl = (1, 3)
    verts = []
    for j in range(1,4):
        for i in range(1, 6):
            verts.append(point(i, j, False, float('inf'), H(gl,(i,j)), None))
    #trial blocks
    verts[1].b = True
    verts[7].b = True

    for i in range(10,15):
        verts[i].b = True
    # start = verts[3] goal = verts[10]
    print(Astar(verts, verts[10], verts[3]))