from utils.graphics_utils import GraphicsUtils

DEFAULT_GRID_SIZE = 15.0
INFO_PANE_HEIGHT = 35
BACKGROUND_COLOR = GraphicsUtils.format_color(0, 0, 0)
WALL_COLOR = GraphicsUtils.format_color(0.5, 0.1, 0.6)
INFO_PANE_COLOR = GraphicsUtils.format_color(.4, .4, 0)
SCORE_COLOR = GraphicsUtils.format_color(.4, 0.13, 0.91)
PACMAN_OUTLINE_WIDTH = 2

GHOST_COLORS = [
    GraphicsUtils.format_color(.1, .75, .7),
    GraphicsUtils.format_color(1.0, 0.6, 0.0),
    GraphicsUtils.format_color(.4, 0.13, 0.91),
    GraphicsUtils.format_color(.9, 0, 0),
    GraphicsUtils.format_color(0, .3, .9),
    GraphicsUtils.format_color(.98, .41, .07)
]


GHOST_SHAPE = [
    (0, 0.3),
    (0.25, 0.75),
    (0.5, 0.3),
    (0.75, 0.75),
    (0.75, -0.5),
    (0.5, -0.75),
    (-0.5, -0.75),
    (-0.75, -0.5),
    (-0.75, 0.75),
    (-0.5, 0.3),
    (-0.25, 0.75)
]
GHOST_SIZE = 0.65
SCARED_COLOR = GraphicsUtils.format_color(1, 1, 1)

GHOST_VEC_COLORS = [GraphicsUtils.color_to_vector(c) for c in GHOST_COLORS]

PACMAN_COLOR = GraphicsUtils.format_color(255.0 / 255.0, 255.0 / 255.0, 61.0 / 255)
PACMAN_SCALE = 0.5

FOOD_COLOR = GraphicsUtils.format_color(1, 1, 1)
FOOD_SIZE = 0.1

CAPSULE_COLOR = GraphicsUtils.format_color(1, 1, 1)
CAPSULE_SIZE = 0.25

WALL_RADIUS = 0.15
