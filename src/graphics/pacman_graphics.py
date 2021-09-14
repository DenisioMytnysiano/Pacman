import math
from graphics.constants import *
from utils.graphics_utils import GraphicsUtils
from graphics.info_panel import InfoPanel
from utils.directions import Directions
from utils.math_utils import MathUtils


class PacmanGraphics:

    def __init__(self, zoom=1.0, frame_time=0.0):
        self.zoom = zoom
        self.grid_size = DEFAULT_GRID_SIZE * zoom
        self.frame_time = frame_time

    def initialize(self, state):
        self.__start_graphics(state)
        self.__draw_static_objects()
        self.__draw_agent_objects(state)

    def __start_graphics(self, state):
        self.layout = state.layout
        layout = self.layout
        self.width = layout.width
        self.height = layout.height
        self.make_window(self.width, self.height)
        self.infoPane = InfoPanel(layout, self.grid_size)
        self.currentState = layout

    def __draw_static_objects(self):
        layout = self.layout
        self.draw_walls(layout.walls)
        self.food = self.draw_food(layout.food)
        self.capsules = self.draw_capsules(layout.capsules)
        GraphicsUtils.refresh()

    def __draw_agent_objects(self, state):
        self.agent_images = []
        for index, agent in enumerate(state.agent_states):
            if agent.is_pacman:
                image = self.draw_pacman(agent)
                self.agent_images.append((agent, image))
            else:
                image = self.draw_ghost(agent, index)
                self.agent_images.append((agent, image))
        GraphicsUtils.refresh()

    def update(self, new_state):
        agent_index = new_state._agent_moved
        agent_state = new_state.agent_states[agent_index]
        prev_state, prev_image = self.agent_images[agent_index]
        if agent_state.is_pacman:
            self.animate_pacman(agent_state, prev_state, prev_image)
        else:
            self.move_ghost(agent_state, agent_index, prev_state, prev_image)
        self.agent_images[agent_index] = (agent_state, prev_image)
        self.draw_paths(new_state)
        if new_state._food_eaten is not None:
            self.remove_food(new_state._food_eaten, self.food)
        if new_state._capsule_eaten is not None:
            self.remove_capsule(new_state._capsule_eaten, self.capsules)
        self.infoPane.update(new_state.score)

    def make_window(self, width, height):
        grid_width = (width - 1) * self.grid_size
        grid_height = (height - 1) * self.grid_size
        screen_width = 2 * self.grid_size + grid_width
        screen_height = 2 * self.grid_size + grid_height + INFO_PANE_HEIGHT
        GraphicsUtils.begin_graphics(screen_width, screen_height, BACKGROUND_COLOR, "Pacman")

    def draw_pacman(self, pacman):
        position = self.get_position(pacman)
        screen_point = self.to_screen(position)
        endpoints = self.get_endpoints(self.get_direction(pacman))

        return [GraphicsUtils.circle(screen_point, PACMAN_SCALE * self.grid_size,
                                     fill_color=PACMAN_COLOR, outline_color=PACMAN_COLOR,
                                     endpoints=endpoints,
                                     width=PACMAN_OUTLINE_WIDTH)]

    def get_endpoints(self, direction, position=(0, 0)):
        x, y = position
        pos = x - int(x) + y - int(y)
        width = 30 + 80 * math.sin(math.pi * pos)

        delta = width / 2
        if direction == 'West':
            endpoints = (180 + delta, 180 - delta)
        elif direction == 'North':
            endpoints = (90 + delta, 90 - delta)
        elif direction == 'South':
            endpoints = (270 + delta, 270 - delta)
        else:
            endpoints = (0 + delta, 0 - delta)
        return endpoints

    def move_pacman(self, position, direction, image):
        screen_position = self.to_screen(position)
        endpoints = self.get_endpoints(direction, position)
        r = PACMAN_SCALE * self.grid_size
        GraphicsUtils.move_circle(image[0], screen_position, r, endpoints)
        GraphicsUtils.refresh()

    def animate_pacman(self, pacman, prev_pacman, image):
        if self.frame_time > 0.01 or self.frame_time < 0:
            fx, fy = self.get_position(prev_pacman)
            px, py = self.get_position(pacman)
            frames = 5
            for i in range(1, int(frames) + 1):
                pos = px * i / frames + fx * (frames - i) / frames, py * i / frames + fy * (frames - i) / frames
                self.move_pacman(pos, self.get_direction(pacman), image)
                GraphicsUtils.refresh()
                GraphicsUtils.sleep(abs(self.frame_time) / frames)
        else:
            self.move_pacman(self.get_position(pacman), self.get_direction(pacman), image)
        GraphicsUtils.refresh()

    def __get_ghost_color(self, ghost, ghostIndex):
        if ghost.scared_timer > 0:
            return SCARED_COLOR
        else:
            return GHOST_COLORS[ghostIndex]

    def draw_ghost(self, ghost, agent_index):
        screen_x, screen_y = self.to_screen(self.get_position(ghost))
        coords = [
            (
                x * self.grid_size * GHOST_SIZE + screen_x,
                y * self.grid_size * GHOST_SIZE + screen_y,
            )
            for x, y in GHOST_SHAPE
        ]
        colour = self.__get_ghost_color(ghost, agent_index)
        body = GraphicsUtils.polygon(coords, colour, filled=1)
        return [body]

    def move_ghost(self, ghost, ghost_index, prev_ghost, ghost_image):
        old_x, old_y = self.to_screen(self.get_position(prev_ghost))
        new_x, new_y = self.to_screen(self.get_position(ghost))
        delta = new_x - old_x, new_y - old_y
        GraphicsUtils.move_by(ghost_image, delta)
        GraphicsUtils.refresh()
        if ghost.scared_timer > 0:
            color = SCARED_COLOR
        else:
            color = GHOST_COLORS[ghost_index]
        GraphicsUtils.edit(ghost_image[0], ('fill', color), ('outline', color))
        GraphicsUtils.refresh()

    def get_position(self, agent_state):
        if agent_state.cell is None:
            return -1000, -1000
        return agent_state.get_position()

    def get_direction(self, agent_state):
        if agent_state.cell is None:
            return Directions.STOP
        return agent_state.cell.get_direction()

    def finish(self):
        GraphicsUtils.end_graphics()

    def to_screen(self, point):
        (x, y) = point
        x = (x + 1) * self.grid_size
        y = (self.height - y) * self.grid_size
        return (x, y)

    def to_screen2(self, point):
        (x, y) = point
        x = (x + 1) * self.grid_size
        y = (self.height - y) * self.grid_size
        return (x, y)

    def draw_walls(self, walls):
        for xNum, x in enumerate(walls):
            for yNum, cell in enumerate(x):
                if cell:
                    pos = (xNum, yNum)
                    screen = self.to_screen(pos)

                    west_is_wall = self.is_wall(xNum - 1, yNum, walls)
                    east_is_wall = self.is_wall(xNum + 1, yNum, walls)
                    north_is_wall = self.is_wall(xNum, yNum + 1, walls)
                    south_is_wall = self.is_wall(xNum, yNum - 1, walls)

                    if ((south_is_wall and north_is_wall)
                            or (south_is_wall and north_is_wall)
                            or (west_is_wall and south_is_wall)
                            or south_is_wall
                    ):
                        end_shift = (0, self.grid_size)
                        GraphicsUtils.line(
                            screen,
                            MathUtils.add_vectors(screen,end_shift),
                            WALL_COLOR,
                        )
                    if ((east_is_wall and west_is_wall)
                            or (south_is_wall and east_is_wall)
                            or (east_is_wall and north_is_wall)
                            or east_is_wall
                    ):
                        end_shift = (self.grid_size, 0)
                        GraphicsUtils.line(
                            screen,
                            MathUtils.add_vectors(screen, end_shift),
                            WALL_COLOR,
                        )

    def is_wall(self, x, y, walls):
        if x < 0 or y < 0 or x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    def draw_food(self, food_matrix):
        food_images = []
        color = FOOD_COLOR
        for index_x, x in enumerate(food_matrix):
            image_row = []
            food_images.append(image_row)
            for index_y, cell in enumerate(x):
                if cell:
                    screen = self.to_screen((index_x, index_y))
                    dot = GraphicsUtils.circle(screen,
                                               FOOD_SIZE * self.grid_size,
                                               outline_color=color, fill_color=color,
                                               width=1)
                    image_row.append(dot)
                else:
                    image_row.append(None)
        return food_images

    def draw_paths(self, game_state):
        if hasattr(self, "ghost_paths"):
            for path in self.ghost_paths:
                GraphicsUtils.remove_from_screen(path)
        ghost_paths = []

        for idx, path in enumerate(game_state.paths):
            color = GHOST_COLORS[idx + 1]

            for node in path:
                screen = self.to_screen(node)
                image = GraphicsUtils.circle(
                    screen,
                    0.2 * self.grid_size,
                    color,
                    style="arc",
                    width=5,
                )
                ghost_paths.append(image)
        self.ghost_paths = ghost_paths

    def draw_capsules(self, capsules):
        capsule_images = {}
        for capsule in capsules:
            (screen_x, screen_y) = self.to_screen(capsule)
            dot = GraphicsUtils.circle(
                (screen_x, screen_y),
                CAPSULE_SIZE * self.grid_size,
                outline_color=CAPSULE_COLOR,
                fill_color=CAPSULE_COLOR,
                width=1
            )
            capsule_images[capsule] = dot
        return capsule_images

    def remove_food(self, cell, food_images):
        x, y = cell
        GraphicsUtils.remove_from_screen(food_images[x][y])

    def remove_capsule(self, cell, capsuleImages):
        x, y = cell
        GraphicsUtils.remove_from_screen(capsuleImages[(x, y)])

def add(x, y):
    return x[0] + y[0], x[1] + y[1]