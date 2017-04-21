from copy import deepcopy

import sys

def get_clockwise_rotated_figure(figure):
    rotated_figure = set()
    for x, y in figure:
        rotated_figure.add((y, -x))
    return rotated_figure


def get_normalized_figure(figure):
    minx = sys.maxsize
    miny = sys.maxsize
    for x, y in figure:
        minx = x if minx > x else minx
        miny = y if miny > y else miny
    minx *= -1
    miny *= -1
    normalized_figure = set()
    for x, y in figure:
        normalized_figure.add((x + minx, y + miny))
    return normalized_figure


def get_rotations(figure):
    rotations = [figure]
    while True:
        rotation = get_normalized_figure(
            get_clockwise_rotated_figure(rotations[-1]))
        if rotations[0] == rotation:
            break
        rotations.append(rotation)
    return rotations


def generate_figures(squares_amount, prev_squares=[(0, 0)]):
    if len(prev_squares) < squares_amount:
        for start_square in prev_squares:
            for neighbour in get_neighbours(
                    start_square[0],
                    start_square[1],
                    prev_squares):
                if neighbour not in prev_squares:
                    yield from generate_figures(squares_amount,
                                                [*prev_squares, neighbour])
    else:
        yield Figure(set(prev_squares))


def get_neighbours(x, y, blacklist_points=[]):
    neighbours = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if abs(dx) + abs(dy) == 1 and \
                            (x + dx, y + dy) not in blacklist_points:
                neighbours.append((x + dx, y + dy))
    return neighbours


class Figure:
    def __init__(self, points):
        self.rotations = get_rotations(get_normalized_figure(points))
        self.rotation_index = 0

    def get_points(self):
        return self.rotations[self.rotation_index]

    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def __eq__(self, other):
        if not isinstance(other, Figure):
            return False
        for rotation in other.rotations:
            if rotation in self.rotations:
                return True
        return False


for i in range(1, 11):
    figures = list()
    l = 0
    for figure in generate_figures(i):
        l += 1
        if figure not in figures:
            figures.append(figure)
    print("{}: {} => {}".format(i, l, len(figures)))
