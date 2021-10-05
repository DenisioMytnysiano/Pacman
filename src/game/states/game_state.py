from dataclasses import dataclass
from game.rules.pacman_rules import PacmanRules
from game.rules.ghost_rules import GhostRules
from game.states.game_state_data import GameStateData

TIME_PENALTY = 1


@dataclass(eq=True, unsafe_hash=True)
class GameState:

    def __init__(self, prev_state=None):
        if prev_state is not None:
            self.data = GameStateData(prev_state.data)
        else:
            self.data = GameStateData()

    def deep_copy(self):
        state = GameState(self)
        state.data = self.data.deep_copy()
        return state

    def initialize(self, layout, numGhostAgents=1000):
        self.data.initialize(layout, numGhostAgents)

    def get_legal_actions(self, agent_index=0):
        if self.is_win() or self.is_lose():
            return list()

        if agent_index == 0:
            return PacmanRules.get_legal_actions(self)
        else:
            return GhostRules.get_legal_actions(self, agent_index)

    def generate_successor(self, agentIndex, action):
        if self.is_win() or self.\
                is_lose():
            raise Exception('Can\'t generate a successor of a terminal state.')

        state = GameState(self)
        if agentIndex == 0:
            state.data._eaten = [False for i in range(state.get_num_agents())]
            PacmanRules.apply_action(state, action)
        else:
            GhostRules.apply_action(state, action, agentIndex)

        if agentIndex == 0:
            state.data.score_change += -TIME_PENALTY
        else:
            GhostRules.decrement_timer(state.data.agent_states[agentIndex])

        GhostRules.check_death(state, agentIndex)
        state.data._agent_moved = agentIndex
        state.data.score += state.data.score_change
        return state

    def get_pacman_state(self):
        return self.data.agent_states[0].copy()

    def get_pacman_position(self):
        return self.data.agent_states[0].get_position()

    def get_ghost_state(self, agent_index):
        if agent_index == 0 or agent_index >= self.get_num_agents():
            raise Exception("Invalid index passed to get_ghost_state")
        return self.data.agent_states[agent_index]

    def get_ghost_position(self, agentIndex):
        if agentIndex == 0:
            raise Exception("Pacman's index passed to get_ghost_position")
        return self.data.agent_states[agentIndex].get_position()

    def get_num_agents(self):
        return len(self.data.agent_states)

    def get_score(self):
        return float(self.data.score)

    def get_capsules(self):
        return self.data.capsules

    def get_num_food(self):
        return self.data.food.count()

    def is_lose(self):
        return self.data._lose

    def is_win(self):
        return self.data._win

