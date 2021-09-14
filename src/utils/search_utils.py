class SearchUtils:

    @staticmethod
    def restore_path(start, goal, memory):
        path = []
        while goal in memory:
            parent = memory[goal]
            if parent == start:
                break
            goal = parent
            path.append(parent)
        path.reverse()
        return path