from utils.directions import Directions
from utils.math_utils import MathUtils
TOLERANCE = .001


class ActionUtils:

    directions = {Directions.NORTH: (0, 1),
                  Directions.SOUTH: (0, -1),
                  Directions.EAST: (1, 0),
                  Directions.WEST: (-1, 0),
                  Directions.STOP: (0, 0)}

    directions_as_list = directions.items()

    @staticmethod
    def reverse_direction(action):
        if action == Directions.NORTH:
            return Directions.SOUTH
        if action == Directions.SOUTH:
            return Directions.NORTH
        if action == Directions.EAST:
            return Directions.WEST
        if action == Directions.WEST:
            return Directions.EAST
        return action

    @staticmethod
    def vector_to_direction(vector):
        dx, dy = vector
        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx < 0:
            return Directions.WEST
        if dx > 0:
            return Directions.EAST
        return Directions.STOP

    @staticmethod
    def direction_to_vector(direction, speed=1.0):
        dx, dy = ActionUtils.directions[direction]
        return dx * speed, dy * speed

    @staticmethod
    def get_possible_actions(config, walls):
        possible = []
        x, y = config.pos
        x_int, y_int = MathUtils.nearest_grid_point(config.pos)

        if abs(x - x_int) + abs(y - y_int) > TOLERANCE:
            return [config.get_direction()]

        for direction, vector in ActionUtils.directions_as_list:
            dx, dy = vector
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                possible.append(direction)

        return possible

