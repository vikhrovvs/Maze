from .dsu import DSU
import random

NOT_VISITED = 0
VISITED = 1
START = 2
FINISH = -1

class Maze:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.walls_quantity = size_x*(size_y-1) + size_y * (size_x - 1)
        self.cells = DSU(size_x*size_y)
        self.walls = [True] * self.walls_quantity
        self.walkthrough = [[NOT_VISITED] * size_y for i in range(size_x)]
        self.walkthrough[0][0] = START
        self.walkthrough[size_x - 1][size_y - 1] = FINISH

    # Порядок стен на примере лабиринта 3x2:
    #.|.|.
    #- - -
    #.|.|.
    #
    # .0.1.
    # 2 3 4
    # .5.6.
    #

    def get_wall_number(self, x1, y1, x2, y2):
        if ((x1 >= self.size_x) or (y1 >= self.size_y) or (x1 < 0) or (y1 < 0) or
                (x2 >= self.size_x) or (y2 >= self.size_y) or (x2 < 0) or (y2 < 0)):
            return  None
        if x1 == x2:
            if y1 == y2 + 1:
                return y2 * (2 * self.size_x - 1) + self.size_x  - 1 + x1
            if y2 == y1 + 1:
                return y1 * (2 * self.size_x - 1) + self.size_x  - 1 + x1
        if y1 == y2:
            if x1 == x2 + 1:
                return y1 * (2 * self.size_x - 1) + x1 - 1
            if x2 == x1 + 1:
                return y1 * (2 * self.size_x - 1) + x2 - 1
        return None

    def get_cell(self, wall_number):
        if wall_number < 0 or wall_number >= self.walls_quantity:
            return None
        y1 = wall_number // (2 * self.size_x - 1)
        wall_number = wall_number % (2 * self.size_x - 1)
        if wall_number < self.size_x - 1:
            y2 = y1
            x1 = wall_number
            x2 = wall_number + 1
            return x1, y1, x2, y2
        else: #size_x - 1 <= wall_number < 2*size_x - 1
            y2 = y1 + 1
            x1 = (wall_number + 1) % self.size_x
            x2 = x1
            return x1, y1, x2, y2

    def create_random_maze(self):
        self.cells = DSU(self.size_x*self.size_y)
        self.walls = [True] * self.walls_quantity
        self.walkthrough = [[NOT_VISITED] * self.size_y for i in range(self.size_x)]
        self.walkthrough[0][0] = START
        self.walkthrough[self.size_x - 1][self.size_y - 1] = FINISH
        wallsNumbers = list(range(self.walls_quantity))
        random.shuffle(wallsNumbers)
        for wall in wallsNumbers:
            x1, y1, x2, y2 = self.get_cell(wall)
            if self.cells.FindSet(y1*self.size_x + x1) != self.cells.FindSet(y2*self.size_x + x2):
                self.walls[wall] = False
                self.cells.Unite(y1*self.size_x + x1, y2*self.size_x + x2)

