import  numpy as np

class DSU:
    def __init__(self, size):
        self.predecessors = np.linspace(0, size - 1, size)
        self.rank = np.zeros(size)
    def FindSet(self, elem):
        if self.predecessors[elem] != elem:
            self.predecessors[elem] = self.FindSet(int(self.predecessors[elem]))
        return self.predecessors[elem]
    def Unite(self, first, second):
        first = int(self.FindSet(first))
        second = int(self.FindSet(second))
        if first != second:
            if self.rank[first] < self.rank[second]:
               first, second = second, first
            self.predecessors[second] = first
            if self.rank[first] == self.rank[second]:
                self.rank[first] += 1
