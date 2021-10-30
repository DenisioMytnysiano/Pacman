import heapq
from typing import Any, Union


class PriorityQueue:
    def __init__(self) -> None:
        self.queue = []

    def push(self, item: Any, priority: Union[int, float]) -> None:
        heapq.heappush(self.queue, (priority, item))

    def pop(self) -> tuple[Any, Union[int, float]]:
        priority, item = heapq.heappop(self.queue)
        return item, priority

    def is_empty(self) -> bool:
        return len(self.queue) == 0
