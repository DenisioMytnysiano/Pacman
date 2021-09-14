import os
from typing import NoReturn
from random import randint


class MazeGenerator:

    @staticmethod
    def generate(width: int, height: int, num_ghosts: int = 1, file_name: str = "generatedMaze.lay") -> NoReturn:
        maze = [[None for x in range(width)] for y in range(height)]
        for x in range(height):
            for y in range(width):
                maze[x][y] = "."
                maze[0][y] = maze[height-1][y] = "%"
            maze[x][0] = maze[x][width-1] = "%"

        # Add obstacles
        for i in range(int(width*height/5)):
            x = randint(1, height-1)
            y = randint(1, width-1)
            maze[x][y] = "%"

        # Add agents
        for i in range(num_ghosts + 1):
            x = randint(1, height - 1)
            y = randint(1, width - 1)
            while maze[x][y] == "%" or maze[x][y] == "P":
                x = randint(1, height - 1)
                y = randint(1, width - 1)
            maze[x][y] = "G" if i > 0 else "P"

        with open(os.path.join("layouts", file_name + ".lay"), "w") as file:
            for line in maze:
                file.write("".join(line) + "\n")
