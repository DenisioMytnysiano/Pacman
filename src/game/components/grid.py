from dataclasses import dataclass, field


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