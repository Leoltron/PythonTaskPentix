import sys


def get_clockwise_rotated_figure(figure):
    """
    :return: Points of the figure rotated on 90 degrees clockwise 
    """
    rotated_figure = set()
    for x, y in figure:
        rotated_figure.add((y, -x))
    return rotated_figure


def get_normalized_figure(figure):
    """
    :return: Figure "moved" to the left upper corner
    """
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
    """
    :return: All possible figure rotations 
    """
    rotations = [figure]
    while True:
        rotation = get_normalized_figure(
            get_clockwise_rotated_figure(rotations[-1]))
        if rotations[0] == rotation:
            break
        rotations.append(rotation)
    return rotations


def generate_figures(squares_amount, prev_squares=[(0, 0)]):
    """
     Generates a list of figures of the same size with possible collisions
    """
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


def generate_figures_cleared(squares_amount):
    """
        Generates a list of figures of the same size without collisions
    """
    figures = list()
    for figure in generate_figures(squares_amount):
        if figure not in figures:
            figures.append(figure)
    return figures


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
        """
        :return: Normalized figure points 
        """
        return self.rotations[self.rotation_index]

    def get_points_moved(self, x, y):
        """
        :return: Points of figure moved on (x,y) position
        """
        return self._get_rotation_points_dx_dy(self.rotation_index, x, y)

    def get_rotated_points_dx_dy(self, dx, dy):
        """
        :return: Points of figure moved on (x,y) position 
        and rotated on 90 degrees
        """
        rotation_index = (self.rotation_index + 1) % len(self.rotations)
        return self._get_rotation_points_dx_dy(rotation_index, dx, dy)

    def _get_rotation_points_dx_dy(self, rotation_index, dx, dy):
        """
        :return: Points of figure moved on (x,y) position 
        on specified rotation
        """
        points = self.rotations[rotation_index]
        moved_points = set()
        for point in points:
            moved_points.add((point[0] + dx, point[1] + dy))
        return moved_points

    def rotate(self):
        """
        Moves rotation index
        """
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def __eq__(self, other):
        if not isinstance(other, Figure):
            return False
        for rotation in other.rotations:
            if rotation in self.rotations:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "Figure({})".format(self.rotations[0])
