from collections import Callable
from search.cost_functions import CostFn
from search.data_structures import PriorityQueue
from utils.action_utils import ActionUtils


def a_star_single_point(game_state, heuristic: Callable, cost_fn: CostFn, greedy=False, start=None, goal=None):
    if start is None:
        start = game_state.get_pacman_position()
    if goal is None:
        goal = game_state.data.layout.food.as_list()[0]
    costs = {start: 0}
    visited = set()
    queue = PriorityQueue()
    queue.push((start, []), 0)

    while not queue.is_empty():
        (parent, actions), _ = queue.pop()
        cost = costs[parent]
        if parent[0] == goal[0] and parent[1] == goal[1]:
            return actions
        for node, action in ActionUtils.get_neighbours(parent, game_state.data.layout.walls):
            if node in visited:
                continue
            new_cost = cost_fn()(node, game_state)
            if not greedy:
                new_cost += cost
            if new_cost < costs.get(node, 1000):
                new_actions = actions + [action]
                priority = new_cost + heuristic(node, goal)
                costs[node] = new_cost
                queue.push((node, new_actions), priority)

    return []


def a_star_all_food(game_state, heuristics, cost_fn, greedy=False):
    start = game_state.get_pacman_position()
    points = [start] + game_state.data.layout.food.as_list()
    rest_food = sorted(points, key=lambda x: heuristics(x, start))
    actions = []
    for i in range(len(rest_food)-1):
        current_start = rest_food[0]
        current_goal = rest_food[1]
        actions.extend(a_star_single_point(game_state, heuristics, cost_fn, greedy, start=current_start, goal=current_goal))
        rest_food = rest_food[1:]
        rest_food = sorted(rest_food, key=lambda x: heuristics(x, current_start))
    return actions




