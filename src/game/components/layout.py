import os
from dataclasses import dataclass
from typing import NoReturn
from game.components.grid import Grid


@dataclass
class Layout:

    def __init__(self, layout_text: list[str]):
        self.mappings = {
            "wall": "%",
            "food": ".",
            "capsule": "o",
            "pacman": "P",
            "ghost": "G"
        }
        self.width = len(layout_text[0])
        self.height = len(layout_text)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.capsules = []
        self.agent_positions = []
        self.num_ghosts = 0
        self.process_layout_text(layout_text)
        self.layout_text = layout_text

    def deep_copy(self):
        return Layout(self.layout_text[:])

    def process_layout_text(self, layout_text: list[str]) -> NoReturn:
        max_y = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layout_char = layout_text[max_y - y][x]
                self.process_layout_cell(x, y, layout_char)
        self.agent_positions.sort()
        self.agent_positions = [(i == 0, pos) for i, pos in self.agent_positions]

    def process_layout_cell(self, x: int, y: int, layout_char: str) -> NoReturn:
        if layout_char == self.mappings["wall"]:
            self.walls[x][y] = True
        elif layout_char == self.mappings["food"]:
            self.food[x][y] = True
        elif layout_char == self.mappings["capsule"]:
            self.capsules.append((x, y))
        elif layout_char == self.mappings["pacman"]:
            self.agent_positions.append((0, (x, y)))
        elif layout_char == self.mappings["ghost"]:
            self.agent_positions.append((1, (x, y)))
            self.num_ghosts += 1


def get_layout(file_name: str) -> Layout:
    layout_path = os.path.join(os.path.dirname(__file__), "../../layouts", file_name + ".lay")
    try:
        if os.path.exists(layout_path):
            with open(layout_path, "r") as file:
                return Layout([line.strip() for line in file])
    except FileNotFoundError:
        print("Layout file cannot be found in /layouts directory")
