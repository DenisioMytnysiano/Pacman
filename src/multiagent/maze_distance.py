from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Union
import numpy as np


@dataclass(eq=False)
class MazeDistance:
    maze_dists: np.ndarray
    mapping: defaultdict
    goal_mapping: Optional[dict[int, int]]

    def get(self, start, end) -> Union[int, float]:
        start = (int(start[0]), int(start[1]))
        end = (int(end[0]), int(end[1]))
        end = self.mapping[end]
        if self.goal_mapping is not None:
            end = self.goal_mapping[end]
        start = self.mapping[start]
        return self.maze_dists[end, start]
