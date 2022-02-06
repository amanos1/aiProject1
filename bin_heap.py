class binHeap:
    def __init__(self):
        self.size = 0
        self.elements = [None]

    def insert(self, v):
        self.elements.append(v)
        self.swim(self.size-1)
        self.size += 1

    def pop(self):
        if self.isEmpty(): return None
        max = self.elements[1]
        self.ex(1, self.size-1)
        self.elements.pop()
        self.sink(1)
        return max

    def search(self, v):
        return self.search2(v, 1)

    def search2(self, v, k):
        if k >= self.size: return False
        if self.equal(self.elements[k], v): return True
        return self.search2(v, k/2) and self.search2(v, k/2+1)

    def equal(self, v1, v2):
        return v1.x == v2.x and v1.y == v2.y

    def sink(self, k):
        if 2*k >= self.size-1: return
        j = 2*k
        if j < self.size-2 and self.elements[j] < self.elements[j+1]: j += 1
        if self.elements[j].f < self.elements[k].f: return
        self.ex(j, k)
        self.sink(j)

    def swim(self, k):
        if k <= 1: return
        if self.elements[k].f > self.elements[k/2].f:
            self.ex(k, k/2)
            self.swim(k/2)

    def ex(self, a, b):
        temp = self.elements[a]
        self.elements[a] = self.elements[b]
        self.elements[b] = temp

    def isEmpty(self):
        return self.size == 0
