# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import heapq
import math
from typing import List, Any
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
def H(g, p):#takes 2 tuples
    xdiff = math.fabs(p[0] - g[0])
    ydiff = math.fabs(p[1] - g[1])
    dist = math.sqrt(2)*min(xdiff, ydiff) + max(xdiff, ydiff) - min(xdiff, ydiff)
    return dist
def succ(verts, p, gx, gy):
    s = set()
    i = (p.x-1)+gx*(p.y-1)
    if p.x>1:
        if not verts[i-1].b:
            s.add(verts[i-1])
        l = True
    else:
        l = False
    if p.x<gx:
        if not verts[i].b:
            s.add(verts[i+1])
        r = True
    else:
        r = False
    if p.y>1:
        if not verts[i-gx].b:
            s.add(verts[i-gx])
        u = True
    else:
        u = False
    if p.y<gy:
        if not verts[i].b:
            s.add(verts[i+gx])
        d = True
    else:
        d = False

    if u and l:
        if not verts[i-(gx+1)].b:
            s.add(verts[i-(gx+1)])#up left
            s.add(verts[i-gx])#up
            s.add(verts[i-1])#left
    if l and d:
        if not verts[i-1].b:
            s.add(verts[i+(gx-1)])#down left
            s.add(verts[i-1])#left
            s.add(verts[i+gx])#down
    if u and r:
        if not verts[i-5].b:
            s.add(verts[i-(gx-1)])#up right
            s.add(verts[i-gx])#up
            s.add(verts[i+1])#right
    if d and r:
        if not verts[i].b:
            s.add(verts[i+1])#right
            s.add(verts[i+(gx+1)])#down right
            s.add(verts[i+gx])#down
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
                UpdateVertex(s,sstar)
    return "no path found"
def UpdateVertex(s,sstar):
    if ( s.g + H((s.x,s.y),(sstar.x,sstar.y)) ) < sstar.g:
        sstar.setG(s.g + H((s.x,s.y),(sstar.x,sstar.y)))
        sstar.setP(s)
        if sstar in fringe:
            fringe.remove(sstar)
        heapq.heappush(fringe, sstar)
        heapq.heapify(fringe)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    s = (4, 1)
    g = (1, 3)
    verts = []
    for j in range(1,4):
        for i in range(1, 6):
            verts.append(point(i, j, False, float('inf'), H(g,(i,j)), None))
    #trial blocks
    verts[1].b = True
    verts[7].b = True

    for i in range(10,15):
        verts[i].b = True
    # start = verts[3] goal = verts[10]
    print(Astar(verts, verts[10], verts[3]))
    nice = []
    node = verts[10]
    while (node.x, node.y) != s:
        nice.append(node)
        node = node.p
    nice.append(node)
    for i in nice:
        print(i)

