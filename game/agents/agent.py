from abc import ABC, abstractmethod
from dataclasses import dataclass
from game.states.game_state import GameState


@dataclass
class Agent(ABC):

    index: int = 0

    @abstractmethod
    def get_action(self, state: GameState):
        pass
