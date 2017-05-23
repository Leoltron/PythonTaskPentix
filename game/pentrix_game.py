import random

from game.figures import Figure
from game.generated_figures import get_figures


def check_for_positive_integer(value, value_name="Value"):
    if not isinstance(value, int):
        raise TypeError(value_name + " must be integer!")
    if value <= 0:
        raise ValueError(value_name + " must be positive!")


class ColorGrid:
    def __init__(self, width, height):
        check_for_positive_integer(width, "Width")
        check_for_positive_integer(height, "Height")
        self._width = width
        self._height = height
        self.grid = dict()
        for x in range(width):
            for y in range(height):
                self.grid[(x, y)] = None

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def is_line_full(self, line_number):
        if not 0 <= line_number < self.height:
            return False
        for x in range(self.width):
            if not self.grid[(x, line_number)]:
                return False
        return True

    def is_line_full_same_color(self, line_number):
        if not 0 <= line_number < self.height:
            return False
        color = None
        for x in range(self.width):
            cell_color = self.grid[(x, line_number)]
            if not cell_color:
                return False
            if cell_color != 'rainbow':
                if color is None:
                    color = cell_color
                elif color != cell_color:
                    return False
        return True

    def clear(self):
        for coords in self.grid:
            self.grid[coords] = None


class FiguresList:
    def __init__(self, figures_types={5}, balance_types=False):
        self._balance_types = balance_types
        if balance_types:
            self._figures = list()
            for figure_type in figures_types:
                self._figures.append(get_figures(figure_type))
        else:
            self._figures = list()
            for figure_type in figures_types:
                self._figures.extend(get_figures(figure_type))

    def get_random_figure(self):
        if self._balance_types:
            return random.choice(random.choice(self._figures))
        else:
            return random.choice(self._figures)


class PentrixGame:
    def __init__(self,
                 grid_width=15,
                 grid_height=30,
                 figure_types={5},
                 balance_types=False,
                 cell_colors=None,
                 color_lines_enabled=True,
                 eraser_enabled=True,
                 time_bomb_enabled=True):
        if cell_colors is None:
            cell_colors = ["blue", "red", "green", "yellow"]
        self._eraser_enabled = eraser_enabled
        self._color_lines_enabled = color_lines_enabled \
                                    and len(cell_colors) > 1
        self._time_bomb_enabled = time_bomb_enabled
        self.figures = FiguresList(figures_types=figure_types,
                                   balance_types=balance_types)
        self.cell_colors = cell_colors
        self.grid = ColorGrid(grid_width, grid_height)
        self._max_figure_size = max(figure_types)
        self.score = 0
        self._eraser_strafe_lock = False
        self.start_new_game()

    def start_new_game(self):
        self.score = 0
        self.grid.clear()
        self._get_new_figure()

    RAINBOW_PROBABILITY = 0.05
    ERASER_PROBABILITY = 0.05
    TIME_BOMB_PROBABILITY = 0.05
    TIME_BOMB_TIME = 5

    def _get_new_figure(self):
        if self._eraser_enabled and \
                        random.random() <= self.ERASER_PROBABILITY:
            self._current_figure = Figure({(0, 0)})
            self.current_figure_color = "*" + random.choice(self.cell_colors)
        elif self._time_bomb_enabled and \
                        random.random() <= self.TIME_BOMB_PROBABILITY:
            self._current_figure = Figure({(0, 0)})
            self.current_figure_color = str(self.TIME_BOMB_TIME) + ":" + \
                                        random.choice(self.cell_colors)
        else:
            if self._color_lines_enabled and \
                            random.random() <= self.RAINBOW_PROBABILITY:
                self.current_figure_color = 'rainbow'
            else:
                self.current_figure_color = random.choice(self.cell_colors)
            self._current_figure = self.figures.get_random_figure()
        current_figure_width = \
            max(self._current_figure.get_points(), key=lambda p: p[0])[0] + 1
        current_figure_height = \
            max(self._current_figure.get_points(), key=lambda p: p[1])[1] + 1

        self.current_figure_x = random.randint(0,
                                               self.grid.width -
                                               current_figure_width)
        self.current_figure_y = -current_figure_height
        for coords in self._current_figure.get_points_moved(
                self.current_figure_x, self.current_figure_y):
            self.grid.grid[coords] = self.current_figure_color

    def _try_move(self, dx, dy):
        is_eraser = self.current_figure_color.startswith("*")
        if is_eraser and dx != 0 and self._eraser_strafe_lock:
            return False
        figure_coords = self._current_figure.get_points_moved(
            self.current_figure_x, self.current_figure_y)
        new_figure_coords = self._current_figure.get_points_moved(
            self.current_figure_x + dx, self.current_figure_y + dy
        )
        result = self._try_replace(figure_coords, new_figure_coords,
                                   is_eraser)
        if result:
            if is_eraser:
                self._eraser_strafe_lock = dx != 0
            self.current_figure_x += dx
            self.current_figure_y += dy
        elif is_eraser and dy > 0:
            self.current_figure_color = self.current_figure_color.replace("*",
                                                                          "")
            self._try_replace(figure_coords, figure_coords)
        return result

    def _try_replace(self, figure_coords,
                     new_figure_coords,
                     eraser_mode=False):
        for coords in new_figure_coords:
            if not (0 <= coords[0] < self.grid.width
                    and coords[1] < self.grid.height):
                return False
            if not eraser_mode \
                    and coords not in figure_coords \
                    and coords in self.grid.grid \
                    and self.grid.grid[coords]:
                return False
        for coords in figure_coords:
            self.grid.grid[coords] = None
        for coords in new_figure_coords:
            self.grid.grid[coords] = self.current_figure_color
        return True

    def try_move_left(self):
        return self._try_move(-1, 0)

    def try_move_right(self):
        return self._try_move(1, 0)

    def try_move_down(self):
        result = self._try_move(0, 1)
        if not result:
            self.summarize_figure_flight()
        return result

    def check_for_completed_lines(self):
        cleared_lines = 0
        for line_y in range(self.grid.height - 1, -1, -1):
            while self.grid.is_line_full(line_y):
                cleared_lines += 1
                if self._color_lines_enabled and \
                        self.grid.is_line_full_same_color(line_y):
                    cleared_lines += 2
                for x in range(self.grid.width):
                    self.grid.grid[(x, line_y)] = None
                for y in range(line_y, 0, -1):
                    for x in range(self.grid.width):
                        self.grid.grid[(x, y)] = self.grid.grid[(x, y - 1)]
                        self.grid.grid[(x, y - 1)] = None
        return cleared_lines

    def check_for_loss(self):
        for x, y in self.grid.grid:
            if y < 0 and self.grid.grid[x, y]:
                self.start_new_game()
                return True
        return False

    def loop(self):
        self.try_move_down()

    def try_rotate(self):
        figure_coords = self._current_figure.get_points_moved(
            self.current_figure_x, self.current_figure_y)
        rotated_figure_coords = self._current_figure.get_rotated_points_dx_dy(
            self.current_figure_x, self.current_figure_y
        )
        result = self._try_replace(figure_coords, rotated_figure_coords)
        if result:
            self._current_figure.rotate()
        return result

    def drop_current_figure(self):
        while self.try_move_down():
            pass
        pass

    def summarize_figure_flight(self):
        if not self.check_for_loss():
            self.add_score(self.check_for_completed_lines())
            if self._time_bomb_enabled:
                self.update_time_bombs()
            self._get_new_figure()

    def add_score(self, lines_cleared):
        score_added = 0
        for i in range(lines_cleared):
            score_added = score_added * 2 + 100
        self.score += score_added

    def update_time_bombs(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.is_bomb(x, y):
                    splitted_type = self.grid.grid[x, y].split(":", 1)
                    time = int(splitted_type[0])
                    if time <= 1:
                        self.explode_at(x, y)
                    else:
                        self.grid.grid[x, y] = str(time - 1) + ":" + \
                                               splitted_type[1]

    def explode_at(self, bomb_x, bomb_y):
        self.grid.grid[bomb_x, bomb_y] = None
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self.is_bomb(bomb_x + x, bomb_y + y):
                    self.explode_at(bomb_x + x, bomb_y + y)
                else:
                    self.grid.grid[bomb_x + x, bomb_y + y] = None

    def is_bomb(self, x, y):
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return False
        cell_type = self.grid.grid[x, y]
        return cell_type is not None and ":" in cell_type
