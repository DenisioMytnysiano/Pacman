from dataclasses import dataclass
from utils.action_utils import ActionUtils
from utils.directions import Directions


@dataclass(eq=True, unsafe_hash=True)
class Cell:

    pos: tuple[int, int]
    direction: Directions

    def get_position(self):
        return self.pos

    def get_direction(self):
        return self.direction

    def is_integer(self):
        x, y = self.pos
        return x == int(x) and y == int(y)

    def generate_successor(self, vector):
        x, y = self.pos
        dx, dy = vector
        direction = ActionUtils.vector_to_direction(vector)
        if direction == Directions.STOP:
            direction = self.direction
        return Cell((x + dx, y + dy), direction)
