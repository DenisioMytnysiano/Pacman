from search.cost_functions import CostFn, UniformCostFn
from search.search_states import AllFoodState


class AllFoodProblem:
    def __init__(
        self,
        game_state,
        cost_fn: CostFn = UniformCostFn,
    ) -> None:
        self.food = game_state.data.layout.food.as_list()
        self.cost_fn = cost_fn
        self.start = AllFoodState(
            game_state.get_pacman_position(), frozenset(self.food)
        )

    def get_start(self) -> AllFoodState:
        return self.start

    def is_goal(self, state: AllFoodState) -> bool:
        return len(state.rest) == 0

    def get_neighbor(self, state, position, action):
        rest = (
            state.rest - set([position])
            if position in state.rest
            else state.rest
        )
        next_state = AllFoodState(position, rest)
        cost = self.cost_fn(next_state)
        return next_state, action, cost