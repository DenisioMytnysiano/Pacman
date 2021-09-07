import random
from dataclasses import dataclass, field
from agents.agent import Agent
from utils.directions import Directions
from utils.graphics_utils import GraphicsUtils


@dataclass
class KeyboardAgent(Agent):

    last_move: Directions = Directions.STOP
    keys: list = field(default_factory=lambda: [])

    def get_action(self, state):
        keys = list(GraphicsUtils.keys_pressed()) + list(GraphicsUtils.keys_waiting())
        if keys:
            self.keys = keys

        legal = state.get_legal_actions(self.index)
        move = self.get_move(legal)

        if move == Directions.STOP:
            if self.last_move in legal:
                move = self.last_move

        if move not in legal:
            move = random.choice(legal)

        self.last_move = move
        return move

    def get_move(self, legal):
        move = Directions.STOP
        if ('Left' in self.keys) and Directions.WEST in legal:
            move = Directions.WEST
        if ('Right' in self.keys) and Directions.EAST in legal:
            move = Directions.EAST
        if ('Up' in self.keys) and Directions.NORTH in legal:
            move = Directions.NORTH
        if ('Down' in self.keys) and Directions.SOUTH in legal:
            move = Directions.SOUTH
        return move
