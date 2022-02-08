import gui
import sys
import random_grids

if __name__ == '__main__':
    # if no arguments provided, generate a random grid, and display that with a*
    if len(sys.argv) == 1:
        random_grids.makeRandomGrids(100, 50, 1)
        gui.run("grids/grid1.txt", False)
    else:
        # if g is the first argument, generate 50 random grids and do nothing else
        if sys.argv[1] == "g":
            random_grids.makeRandomGrids(100, 50, 50)
            print("50 fresh grids generated!")
        # if the first argument is not g, it is assumed it will be a file name
        # the second argument determines whether or not it will use a* or theta* to find the shortest path
        else:
            if sys.argv[2] == "t":
                gui.run(sys.argv[1], False)
            else:
                gui.run(sys.argv[1], True)
