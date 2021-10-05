from graphics.constants import INFO_PANE_HEIGHT, SCORE_COLOR
from utils.graphics_utils import GraphicsUtils


class InfoPanel:
    def __init__(self, layout, grid_size):
        self.grid_size = grid_size
        self.width = layout.width * grid_size
        self.base = (layout.height + 1) * grid_size
        self.height = INFO_PANE_HEIGHT
        self.font_size = 24
        self.text_color = SCORE_COLOR
        self.draw()

    def to_screen(self, pos, y=None):
        if y is None:
            x, y = pos
        else:
            x = pos

        x = self.grid_size + x
        y = self.base + y
        return x, y

    def draw(self):
        self.score_text = GraphicsUtils.text(self.to_screen(0, 0), self.text_color, "", "Times", self.font_size, "bold")

    def update(self, score):
        GraphicsUtils.change_text(self.score_text, f"SCORE: {score}")

