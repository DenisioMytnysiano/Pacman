from abc import ABC
from functools import partial
from typing import Callable, Generator, Optional, Union
from dataclasses import dataclass, field

from agents import Agent
from game.states.game_state import GameState
from multiagent.state import ReflexState
from multiagent.utility_function import utility_fn
from multiagent.utils import get_maze_dists, adjlist_to_adjmatrix
from utils.directions import Directions
from utils.reflection import get_arg_names

StateGenerator = Generator[ReflexState, None, None]
UtilityFn = Callable[[ReflexState], Union[float, int]]


@dataclass(order=True)
class Value:
    cost: Union = 0
    action: int = field(default=Directions.STOP, compare=False)


class ReflexAgent(Agent, ABC):
    def __init__(
            self, index: int = 0,
            depth: int = 3, utility: UtilityFn = utility_fn
    ) -> None:
        super().__init__(index=index)
        self.depth = depth
        self.utility = utility

    def register_state(self, game_state: GameState) -> None:
        walls = game_state.get_walls()
        maze_dists = get_maze_dists(*adjlist_to_adjmatrix(walls.get_adjlist()))

        if "maze_dists" in get_arg_names(self.utility):
            self.utility = partial(self.utility, maze_dists=maze_dists)

    def _get_next_states(self, state: ReflexState) -> StateGenerator:
        num_agents = state.game_state.get_num_agents()

        depth = state.depth + (1 if state.agent == num_agents - 1 else 0)
        agent = (state.agent + 1) % num_agents

        for action in state.game_state.get_legal_actions(state.agent):
            if action != Directions.STOP:
                game_state = state.game_state.generate_successor(
                    state.agent, action
                )
                next_state = ReflexState(game_state, agent, depth)
                yield next_state

    def _is_terminate(self, state: ReflexState) -> bool:
        return (
            True
            if state.depth == self.depth
               or state.game_state.is_win()
               or state.game_state.is_lose()
            else False
        )


class MinimaxAgent(ReflexAgent):
    def get_action(self, game_state: GameState):
        value = self.__alpha_beta(
            ReflexState(game_state, agent=self.index),
            alpha=-1000,
            beta=1000,
        )
        return value.action

    def __alpha_beta(self, state: ReflexState, alpha, beta) -> Value:
        if self._is_terminate(state):
            return Value(self.utility(state))
        if state.agent == 0:
            return self.__max_value(state, alpha, beta)
        return self.__min_value(state, alpha, beta)

    def __max_value(self, state: ReflexState, alpha, beta) -> Value:
        value = Value(-1000)
        for next in self._get_next_states(state):
            value = max(value, Value(self.__alpha_beta(next, alpha, beta).cost, next.action))
            if value.cost >= beta:
                return value
            alpha = max(alpha, value.cost)
        return value

    def __min_value(self, state: ReflexState, alpha, beta) -> Value:
        value = Value(1000)
        for next in self._get_next_states(state):
            value = min(value, Value(self.__alpha_beta(next, alpha, beta).cost, next.action))
            if value.cost <= alpha:
                return value
            beta = min(beta, value.cost)
        return value


class ExpectimaxAgent(ReflexAgent):
    def get_action(self, game_state):
        value = self.__expectimax(ReflexState(game_state, agent=self.index))
        return value.action

    def __expectimax(self, state: ReflexState) -> Value:
        if self._is_terminate(state):
            return Value(self.utility(state))
        if state.agent == 0:
            return self.__max_value(state)
        return self.__expectation(state)

    def __max_value(self, state: ReflexState) -> Value:
        value = Value(-1000)
        for next_state in self._get_next_states(state):
            value = max(value, Value(self.__expectimax(next_state).cost, next_state.action))
        return value

    def __expectation(self, state: ReflexState) -> Value:
        next_states = list(self._get_next_states(state))
        value = Value()

        for next_state in next_states:
            value.cost += self.__expectimax(next_state).cost

        value.cost /= len(next_states)
        return value