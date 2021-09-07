import numpy as np


class MathUtils:

    @staticmethod
    def manhattan_distance(vector_1, vector_2):
        return abs(vector_1[0] - vector_2[0]) + abs(vector_1[1] - vector_2[1])

    @staticmethod
    def add_vectors(vector_1, vector_2):
        return vector_1[0] + vector_2[0], vector_1[1] + vector_2[1]

    @staticmethod
    def add_vectors(vector_1, vector_2):
        return vector_1[0] + vector_2[0], vector_1[1] + vector_2[1]

    @staticmethod
    def nearest_grid_point(pos):
        current_row, current_col = pos
        grid_row = int(current_row + 0.5)
        grid_col = int(current_col + 0.5)
        return grid_row, grid_col

    @staticmethod
    def normalize(distribution: dict) -> dict:
        total = float(sum(distribution.values()))
        if total > 0:
            for key in distribution.keys():
                distribution[key] = distribution[key] / total
        return distribution

    @staticmethod
    def sample(distribution, values=None):
        if isinstance(distribution, dict):
            items = sorted(distribution.items())
            distribution = np.array([i[1] for i in items])
            values = [i[0] for i in items]
        if sum(distribution) != 1:
            distribution = distribution / np.linalg.norm(distribution)
        choice = np.random.choice(values, p=distribution)
        return choice



