import random
import bin_heap


class Thingie:
    def __init__(self):
        self.f = random.randrange(0, 100)

    def __str__(self):
        return "Thingie: " + str(self.f)

    def getF(self):
        return self.f


if __name__ == '__main__':
    stuff = bin_heap.binHeap()
    for i in range(25):
        stuff.insert(Thingie())
    while not stuff.isEmpty():
        print(stuff.pop())
