from dataclasses import dataclass


@dataclass(eq=False)
class CostFn:

    def __call__(self, cell, game_state):
        raise NotImplementedError


@dataclass(eq=False)
class UniformCostFn(CostFn):
    cost: int = 1

    def __call__(self, cell, game_state):
        return self.cost


@dataclass(eq=False)
class FoodCostFn(CostFn):

    empty_cost: int = 2
    food_cost: int = 1

    def __call__(self, cell, game_state):
        xx, yy = cell
        return self.food_cost if game_state.data.layout.food[int(xx)][int(yy)] else self.empty_cost
