from collections import deque
from queue import Queue, PriorityQueue
from utils.action_utils import ActionUtils
from utils.decorators import print_execution_time
from utils.math_utils import MathUtils
from utils.search_utils import SearchUtils


@print_execution_time
def bfs(game_state):
    start = game_state.get_pacman_position()
    goals = [
        game_state.get_ghost_position(i)
        for i in range(1, game_state.get_num_agents())
    ]
    found = [False] * len(goals)
    visited = set()
    memory = dict()
    queue = Queue()
    queue.put((start, 0))

    while not queue.empty():
        parent, cost = queue.get()
        visited.add(parent)

        found = MathUtils.or_vectors(found, [goal == parent for goal in goals])
        if all(found) is True:
            break
        for node in ActionUtils.get_neighbours(parent, game_state.data.layout.walls):
            if node in visited:
                continue
            new_cost = cost + 1
            memory[node] = parent
            queue.put((node, new_cost))

    return [SearchUtils.restore_path(start, goal, memory) for goal in goals]


@print_execution_time
def dfs(game_state):
    start = game_state.get_pacman_position()
    goals = [
        game_state.get_ghost_position(i)
        for i in range(1, game_state.get_num_agents())
    ]
    costs = {start: 0}
    memory = dict()
    stack = deque()
    stack.append(start)

    while not len(stack) == 0:
        parent = stack.pop()
        cost = costs[parent]

        for node in ActionUtils.get_neighbours(parent, game_state.data.layout.walls):
            new_cost = cost + 1
            if costs.get(node, 1000) <= new_cost:
                continue
            memory[node] = parent
            stack.append(node)
            costs[node] = new_cost

    return [SearchUtils.restore_path(start, goal, memory) for goal in goals]


@print_execution_time
def unisearch(game_state):
    start = game_state.get_pacman_position()
    goals = [
        game_state.get_ghost_position(i)
        for i in range(1, game_state.get_num_agents())
    ]

    found = [False] * len(goals)
    costs = {start: 0}
    visited = set()
    memory = dict()
    queue = PriorityQueue()
    queue.put((0, start))

    while not queue.empty():
        cost, parent = queue.get()
        visited.add(parent)
        if costs[parent] < cost:
            continue
        found = MathUtils.or_vectors(found, [goal == parent for goal in goals])
        if all(found) is True:
            break
        for node in ActionUtils.get_neighbours(parent, game_state.data.layout.walls):
            if node in visited:
                continue
            new_cost = cost + 1
            if new_cost < costs.get(node, 1000):
                costs[node] = new_cost
                memory[node] = parent
                queue.put((new_cost, node))

    return [SearchUtils.restore_path(start, goal, memory) for goal in goals]

