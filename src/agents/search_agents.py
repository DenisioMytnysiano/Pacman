from functools import partial
from typing import Callable, Optional
from agents import Agent
from utils.directions import Directions
from search.algorithms import a_star_single_point, a_star_all_food
from search.cost_functions import CostFn, FoodCostFn, UniformCostFn
from search.heuristics import *


class SearchAgent(Agent):
    def __init__(
            self,
            search_fn: Callable = a_star_single_point,
            heuristic: Optional[Callable] = constant,
            cost_fn: CostFn = FoodCostFn,
            greedy: bool = False
    ) -> None:
        self.search_fn = partial(search_fn, heuristic=heuristic, cost_fn=cost_fn, greedy=greedy)

    def get_action(self, game_state) -> int:
        if self.action_idx >= len(self.actions):
            return Directions.STOP
        idx = self.action_idx
        self.action_idx += 1
        return self.actions[idx]

    def register_state(self, game_state) -> None:
        self.action_idx = 0
        self.actions = self.search_fn(game_state)


class AllFoodSearchAgent(SearchAgent):

    def __init__(self, cost_fn: CostFn = UniformCostFn, greedy: bool = False):
        self.search_fn = partial(a_star_all_food, heuristics=manhattan_distance,cost_fn=cost_fn, greedy=greedy)
