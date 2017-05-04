import random
import figures
from generated_figures import get_figures
from grid import ColorGrid


class FiguresList:
    def __init__(self, figures_types={5}, balance_types=False):
        self._balance_types = balance_types
        if balance_types:
            self._figures = dict()
            for figure_type in figures_types:
                self._figures[figure_type] = get_figures(figure_type)
        else:
            self._figures = list()
            for figure_type in figures_types:
                self._figures.extend(get_figures(figure_type))

    def get_random_figure(self):
        if self._balance_types:
            return random.choice(random.choice(self._figures.values()))
        else:
            return random.choice(self._figures)


class Game:
    def __init__(self,
                 grid_width=15,
                 grid_height=30,
                 figure_types={5},
                 balance_types=False,
                 cell_colors=["blue", "red", "green", "yellow"],
                 grid_canvas=None):
        self.figures = FiguresList(figures_types=figure_types,
                                   balance_types=balance_types)
        self.cell_colors = cell_colors
        self.grid = ColorGrid(grid_width, grid_height)
        self._max_figure_size = max(figure_types)

    def _get_new_figure(self):
        self._current_figure = self.figures.get_random_figure()
        current_figure_width = \
            max(self._current_figure.get_points(), key=lambda p: p[0])[0] + 1
        current_figure_height = \
            max(self._current_figure.get_points(), key=lambda p: p[1])[1] + 1

        self.current_figure_x = random.randint(0,
                                               self.grid.width -
                                               current_figure_width)
        self.current_figure_y = -current_figure_height

        self.current_figure_color = random.choice(self.cell_colors)
        for x, y in self._current_figure.get_points_moved(
                self.current_figure_x, self.current_figure_y):
            self.grid.grid[(x, y)] = self.current_figure_color

    def _try_move(self, dx, dy):
        figure_coords = self._current_figure.get_points_moved(
            self.current_figure_x, self.current_figure_y)
        new_figure_coords = self._current_figure.get_points_moved(
            self.current_figure_x + dx, self.current_figure_y + dy
        )
        result = self._try_replace(figure_coords, new_figure_coords)
        if result:
            self.current_figure_x += dx
            self.current_figure_y += dy
        return result

    def _try_replace(self, figure_coords, new_figure_coords):
        for coords in new_figure_coords:
            if not (0 <= coords[0] < self.grid.width and
                            coords[1] < self.grid.height):
                return False
            if coords not in figure_coords \
                    and coords in self.grid.grid and self.grid.grid[coords]:
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
        return self._try_move(0, 1)

    def check_for_completed_lines(self):
        cleared_lines = 0
        for line_y in range(self.grid.height - 1, -1, -1):
            while self.grid.is_line_full(line_y):
                cleared_lines += 1
                for x in range(self.grid.width):
                    self.grid.grid[(x, line_y)] = None
                for y in range(line_y, 0, -1):
                    for x in range(self.grid.width):
                        self.grid.grid[(x, y)] = self.grid.grid[(x, y - 1)]
                        self.grid.grid[(x, y - 1)] = None

    def check_for_loss(self):
        for x, y in self.grid.grid:
            if y < 0 and self.grid.grid[x, y]:
                self.restart_game(self.grid.width, self.grid.height)
                return True
        return False

    def loop(self):
        if not self.try_move_down():
            self.summarize_figure_flight()

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
        self.summarize_figure_flight()

    def summarize_figure_flight(self):
        if not self.check_for_loss():
            self.check_for_completed_lines()
            self._get_new_figure()
