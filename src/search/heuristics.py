from math import sqrt


def manhattan_distance(point, goal):
    return abs(point[0] - goal[0]) + abs(point[1] - goal[1])


def minkovski_distance(point, goal, p=4):
    return pow(abs(point[0] - goal[0]) ** p + abs(point[1] - goal[1]) ** p, 1 / p)


def constant(point, goal):
    return 4


def euclidean_distance(point, goal):
    return sqrt((point[0] - goal[0]) ** 2 + (point[1] - goal[1]) ** 2)
