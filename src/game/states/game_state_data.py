from dataclasses import dataclass
from game.components import Cell
from game.states.agent_state import AgentState
from utils.directions import Directions


@dataclass(eq=True, unsafe_hash=True)
class GameStateData:

    def __init__(self, prev_state=None):
        if prev_state is not None:
            self.food = prev_state.food.copy()
            self.capsules = prev_state.capsules[:]
            self.agent_states = self.copy_agent_states(prev_state.agent_states)
            self.layout = prev_state.layout
            self._eaten = prev_state._eaten
            self.score = prev_state.score

        self._food_eaten = None
        self._food_added = None
        self._capsule_eaten = None
        self._agent_moved = None
        self._lose = False
        self._win = False
        self.score_change = 0
        self.paths = list()

    def deep_copy(self):
        state = GameStateData(self)
        state.food = self.food.copy()
        state.layout = self.layout.deep_copy()
        state._agent_moved = self._agent_moved
        state._food_eaten = self._food_eaten
        state._food_added = self._food_added
        state._capsule_eaten = self._capsule_eaten
        return state

    def copy_agent_states(self, agent_states):
        copied_states = []
        for agent_state in agent_states:
            copied_states.append(agent_state.copy())
        return copied_states

    def initialize(self, layout, num_ghost_agents):
        self.food = layout.food.copy()
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.score_change = 0

        self.agent_states = []
        num_ghosts = 0
        for is_pacman, pos in layout.agent_positions:
            if not is_pacman:
                if num_ghosts == num_ghost_agents:
                    continue
                else:
                    num_ghosts += 1
            self.agent_states.append(AgentState(Cell(pos, Directions.STOP), is_pacman))
        self._eaten = [False for a in self.agent_states]
