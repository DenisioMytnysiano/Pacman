from dataclasses import dataclass
from game.components import Cell


@dataclass(eq=True, unsafe_hash=True)
class AgentState:

    start: Cell
    is_pacman: bool
    scared_timer: int = 0

    def __post_init__(self):
        self.cell = self.start

    def copy(self):
        state = AgentState(self.start, self.is_pacman)
        state.cell = self.cell
        state.scared_timer = self.scared_timer
        return state

    def get_position(self):
        if self.cell is None:
            return None
        return self.cell.get_position()

    def get_direction(self):
        return self.cell.get_direction()
