from utils.action_utils import ActionUtils
from utils.math_utils import MathUtils
SCARED_TIME = 40
PACMAN_SPEED = 1


class PacmanRules:

    @staticmethod
    def get_legal_actions(state):
        return ActionUtils.get_possible_actions(state.get_pacman_state().cell, state.data.layout.walls)

    @staticmethod
    def apply_action(state, action):
        legal = PacmanRules.get_legal_actions(state)
        if action not in legal:
            return

        pacman_state = state.data.agent_states[0]

        vector = ActionUtils.direction_to_vector(action, PACMAN_SPEED)
        pacman_state.cell = pacman_state.cell.generate_successor(vector)

        next = pacman_state.cell.get_position()
        nearest = MathUtils.nearest_grid_point(next)
        if MathUtils.manhattan_distance(nearest, next) <= 0.5:
            PacmanRules.consume(nearest, state)

    @staticmethod
    def consume(position, state):
        x, y = position
        if state.data.food[x][y]:
            state.data.score_change += 10
            state.data.food = state.data.food.copy()
            state.data.food[x][y] = False
            state.data._food_eaten = position
            num_food = state.get_num_food()
            if num_food == 0 and not state.data._lose:
                state.data.score_change += 500
                state.data._win = True

        if position in state.get_capsules():
            state.data.capsules.remove(position)
            state.data._capsule_eaten = position
            for index in range(1, len(state.data.agent_states)):
                state.data.agent_states[index].scared_timer = SCARED_TIME