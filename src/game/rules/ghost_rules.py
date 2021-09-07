from utils.action_utils import ActionUtils
from utils.directions import Directions
from utils.math_utils import MathUtils

COLLISION_TOLERANCE = 0.7
GHOST_SPEED = 1.0


class GhostRules:

    @staticmethod
    def get_legal_actions(state, ghost_index):
        conf = state.get_ghost_state(ghost_index).cell
        possible_actions = ActionUtils.get_possible_actions(conf, state.data.layout.walls)
        reverse = ActionUtils.reverse_direction(conf.direction)
        if Directions.STOP in possible_actions:
            possible_actions.remove(Directions.STOP)
        if reverse in possible_actions and len(possible_actions) > 1:
            possible_actions.remove(reverse)
        return possible_actions

    @staticmethod
    def apply_action(state, action, ghost_index):
        legal = GhostRules.get_legal_actions(state, ghost_index)
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))
        ghost_state = state.data.agent_states[ghost_index]
        speed = GHOST_SPEED
        if ghost_state.scared_timer > 0:
            speed /= 2.0
        vector = ActionUtils.direction_to_vector(action, speed)
        ghost_state.cell = ghost_state.cell.generate_successor(vector)

    @staticmethod
    def decrement_timer(ghost_state):
        timer = ghost_state.scared_timer
        if timer == 1:
            ghost_state.cell.pos = MathUtils.nearest_grid_point(ghost_state.cell.pos)
        ghost_state.scared_timer = max(0, timer - 1)

    @staticmethod
    def check_death(state, agentIndex):
        pacman_position = state.get_pacman_position()
        if agentIndex == 0:
            for index in range(1, len(state.data.agent_states)):
                ghost_state = state.data.agent_states[index]
                ghost_position = ghost_state.cell.get_position()
                if GhostRules.can_kill(pacman_position, ghost_position):
                    GhostRules.collide(state, ghost_state, index)
        else:
            ghost_state = state.data.agent_states[agentIndex]
            ghost_position = ghost_state.cell.get_position()
            if GhostRules.can_kill(pacman_position, ghost_position):
                GhostRules.collide(state, ghost_state, agentIndex)

    @staticmethod
    def collide(state, ghostState, agentIndex):
        if ghostState.scared_timer > 0:
            state.data.score_change += 200
            GhostRules.place_ghost(ghostState)
            ghostState.scared_timer = 0
            state.data._eaten[agentIndex] = True
        else:
            if not state.data._win:
                state.data.score_change -= 500
                state.data._lose = True

    @staticmethod
    def can_kill(pacman_position, ghost_position):
        return MathUtils.manhattan_distance(ghost_position, pacman_position) <= COLLISION_TOLERANCE

    @staticmethod
    def place_ghost(ghost_state):
        ghost_state.cell = ghost_state.start
