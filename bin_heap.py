class binHeap:
    def __init__(self):
        self.size = 0
        self.elements = []

    def insert(self, v):
        self.elements.append(v)
        if self.size == 0:
            self.elements.append(v)
        self.swim(self.size-1)
        self.size += 1

    def heapify(self):
        for i in range(int((self.size-1)/2), 0, -1):
            self.sink(i)

    def remove(self, waste):
        findW = self.findIndex(waste, 1)
        if findW > -1:
            self.elements.pop(findW)
            self.heapify()
            self.size -= 1

    def pop(self):
        if self.isEmpty(): return None
        max = self.elements[1]
        self.ex(1, self.size-1)
        self.elements.pop()
        self.heapify()
        self.size -= 1
        return max

    def search(self, v):
        return self.search2(v, 1)

    def search2(self, v, k):
        if k >= self.size: return False
        if self.equal(self.elements[k], v): return True
        return self.search2(v, k*2) and self.search2(v, k*2+1)

    def findIndex(self, v, k):
        if k >= self.size: return -1
        if self.equal(self.elements[k], v): return k
        left = self.findIndex(v, k*2)
        if left > -1: return left
        right = self.findIndex(v, k*2+1)
        if right > -1: return right
        return -1

    def equal(self, v1, v2):
        return v1.x == v2.x and v1.y == v2.y

    def sink(self, k):
        if 2*k >= self.size-1: return
        j = 2*k
        if j < self.size-2 and self.elements[j] < self.elements[j+1]: j += 1
        if self.elements[j].getF() < self.elements[k].getF(): return
        self.ex(j, k)
        self.sink(j)

    def swim(self, k):
        if k <= 1: return
        if self.elements[k].getF() > self.elements[int(k/2)].getF():
            self.ex(k, int(k/2))
            self.swim(int(k/2))

    def ex(self, a, b):
        temp = self.elements[a]
        self.elements[a] = self.elements[b]
        self.elements[b] = temp

    def isEmpty(self):
        return self.size == 0
