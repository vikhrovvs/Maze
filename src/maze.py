import random
from queue import Queue
from .consts import *
from .dsu import DSU

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
        self.path = []
        self.hints = 0
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
        self.path = []
        self.hints = 0
        wallsNumbers = list(range(self.walls_quantity))
        random.shuffle(wallsNumbers)
        for wall in wallsNumbers:
            x1, y1, x2, y2 = self.get_cell(wall)
            if self.cells.FindSet(y1*self.size_x + x1) != self.cells.FindSet(y2*self.size_x + x2):
                self.walls[wall] = False
                self.cells.Unite(y1*self.size_x + x1, y2*self.size_x + x2)
    def solve(self):
        queue = Queue()
        queue.put((0, 0))
        predecessors = [[(-1, -1)] * self.size_y for i in range(self.size_x)]
        visited = [[False] * self.size_y for i in range(self.size_x)]
        visited[0][0] = True
        while not queue.empty():
            x, y = queue.get()
            for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                wall = self.get_wall_number(x, y, x + i, y + j)
                if wall is not None and not self.walls[wall]:
                    if not visited[x + i][y + j]:
                        predecessors[x + i][y + j] = (x, y)
                        visited[x + i][y + j] = True
                        queue.put((x + i, y + j))
        self.path = [(self.size_x - 1, self.size_y - 1)]
        pred = predecessors[self.size_x - 1][self.size_y - 1] #FINISH
        while pred != (-1, -1):
            self.path.insert(0, (pred[0], pred[1]))
            pred = predecessors[pred[0]][pred[1]]

    def get_next_move(self):
        if len(self.path) == 0:
            self.solve()
        for x, y in self.path:
            if self.walkthrough[x][y] == NOT_VISITED:
                self.hints += 1
                self.walkthrough[x][y] = HINT
                return
            if self.walkthrough[x][y] == HINT:
                return
