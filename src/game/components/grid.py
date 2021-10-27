from collections import defaultdict
from dataclasses import dataclass, field
from queue import Queue

import numpy as np

from utils.action_utils import ActionUtils
from utils.directions import Directions
from utils.math_utils import MathUtils


@dataclass(eq=True, unsafe_hash=True)
class Grid:
    width: int
    height: int
    initial_value: bool = field(default=False)
    data: list[list[bool]] = field(init=False, hash=False)

    def __post_init__(self):
        self.data = [[self.initial_value for y in range(self.height)] for x in range(self.width)]

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def count(self, item=True):
        return sum([x.count(item) for x in self.data])

    def as_list(self, key=True):
        result = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    result.append((x, y))
        return result

    def invert(self) -> "Grid":
        grid = self.copy()
        grid.data = (~np.array(grid.data)).tolist()
        return grid

    def get_neighbors(self, position):
        neighbors = []
        for action, move in ActionUtils.directions_as_list:
            if action != Directions.STOP:
                next = MathUtils.add_vectors(position, move)
                if not self.data[int(next[0])][int(next[1])]:
                    neighbors.append(next)
        return neighbors

    def get_adjlist(self):
        adjlist = defaultdict(list)
        visited = set()

        for start in self.invert().as_list():
            queue = Queue()
            queue.put(start)

            while not queue.empty():
                parent = queue.get()
                if parent in visited:
                    continue
                visited.add(parent)

                for neighbor in self.get_neighbors(parent):
                    queue.put(neighbor)
                    adjlist[parent].append((neighbor, 1))
        return adjlist
