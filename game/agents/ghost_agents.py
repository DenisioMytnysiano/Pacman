from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from agents.agent import Agent
from game.states.game_state import GameState
from utils.action_utils import ActionUtils
from utils.directions import Directions
from utils.math_utils import MathUtils


@dataclass
class GhostAgent(Agent, ABC):

    def get_action(self, state: GameState):
        dist = self.get_distribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return MathUtils.sample(dist)

    @abstractmethod
    def get_distribution(self, state: GameState):
        pass


@dataclass
class RandomGhost(GhostAgent):

    def get_distribution(self, state: GameState):
        dist = defaultdict(lambda x: 0.0, dict())
        for a in state.get_legal_actions(self.index):
            dist[a] = 1.0
        dist = MathUtils.normalize(dist)
        return dist


@dataclass
class DirectionalGhost(GhostAgent):

    prob_attack: int = 0.8
    prob_scared: int = 0.8

    def get_distribution(self, state):
        ghost_state = state.get_ghost_state(self.index)
        legal_actions = state.get_legal_actions(self.index)
        pos = state.get_ghost_position(self.index)
        is_scared = ghost_state.scared_timer > 0

        speed = 1
        if is_scared:
            speed = 0.5

        action_vectors = [ActionUtils.direction_to_vector(a, speed) for a in legal_actions]
        new_positions = [(pos[0]+a[0], pos[1]+a[1]) for a in action_vectors]
        pacman_position = state.get_pacman_position()

        distances_to_pacman = [MathUtils.manhattan_distance(pos, pacman_position) for pos in new_positions]
        if is_scared:
            best_score = max(distances_to_pacman)
            best_prob = self.prob_scared
        else:
            best_score = min(distances_to_pacman)
            best_prob = self.prob_attack
        best_actions = [action for action, distance in zip(legal_actions, distances_to_pacman) if distance == best_score]

        dist = defaultdict(lambda: 0.0, dict())
        for a in best_actions:
            dist[a] = best_prob / len(best_actions)
        for a in legal_actions:
            dist[a] += (1-best_prob) / len(legal_actions)

        dist = MathUtils.normalize(dist)
        return dist
