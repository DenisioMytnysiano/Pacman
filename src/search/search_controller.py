import time
from typing import NoReturn, Callable
from search.algorithms import dfs, bfs, unisearch
from utils.decorators import print_execution_time
from utils.graphics_utils import GraphicsUtils


class SearchController:
    algorithms = [bfs, dfs, unisearch]
    current_index = 2

    @staticmethod
    def run(game_state):
        SearchController.__update()
        result = SearchController.get_algorithm()(game_state)
        return result

    @staticmethod
    def get_algorithm() -> Callable:
        return SearchController.algorithms[SearchController.current_index]

    @staticmethod
    def __update() -> NoReturn:
        keys = list(GraphicsUtils.keys_pressed()) + list(GraphicsUtils.keys_waiting())
        if "z" in keys or "Z" in keys:
            SearchController.current_index = (SearchController.current_index + 1) % len(SearchController.algorithms)
