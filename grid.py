from tkinter import Canvas


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
        self._grid = dict()
        for x in range(width):
            for y in range(height):
                self._grid[(x, y)] = None

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def line_color(self):
        return self._line_color

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value):
        self._grid = dict()
        for x in range(self._width):
            for y in range(self._height):
                self._grid[(x, y)] = None
        for coords, color in value.items():
            self._grid[coords] = color

    def is_line_full(self, line_number):
        if not 0 <= line_number < self.height:
            return False
        for x in range(self.width):
            if not self.grid[(x, line_number)]:
                return False
        return True


class ResizableGridCanvas(Canvas):
    def __init__(self, parent, grid,
                 line_color="white",
                 bg_color="black",
                 **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.grid = grid
        self.line_color = line_color
        self.bg_color = bg_color
        self.update_size()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.update_size()

    def update_size(self):
        self._update_cell_size()
        self._update_sides()
        self.redraw()

    def _update_cell_size(self):
        av_w = self.width - self.grid.width + 1
        av_h = self.height - self.grid.height + 1
        av_cw = av_w // self.grid.width
        av_ch = av_h // self.grid.height
        self._cell_size = av_ch if av_ch < av_cw else av_cw

    def _update_sides(self):
        self._left = (self.width
                      - self._cell_size * self.grid.width
                      - self.grid.width + 1) // 2
        self._up = (self.height
                    - self._cell_size * self.grid.height
                    - self.grid.height + 1) // 2
        self._right = (self._left +
                       self._cell_size * self.grid.width +
                       self.grid.width - 1)
        self._bottom = (self._up +
                        self._cell_size * self.grid.height +
                        self.grid.height - 1)

    def redraw(self):
        self._draw_bg(self.bg_color)
        x = self._left
        for grid_x in range(self.grid.width):
            y = self._up
            for grid_y in range(self.grid.height):
                if self.grid.grid[(grid_x, grid_y)]:
                    self.draw_cell(x, y, grid_x, grid_y)
                y += 1 + self._cell_size
            x += 1 + self._cell_size
        self._draw_grid_lines()

    def _draw_grid_lines(self):
        x = self._left + self._cell_size
        for i in range(self.grid.width - 1):
            self.create_line(x, self._up, x, self._bottom,
                             fill=self.line_color)
            x += 1 + self._cell_size
        y = self._up + self._cell_size
        for i in range(self.grid.height - 1):
            self.create_line(self._left, y, self._right, y,
                             fill=self.line_color)
            y += 1 + self._cell_size

    def draw_cell(self, x, y, grid_x, grid_y):
        self.create_rectangle(x, y,
                              x + self._cell_size,
                              y + self._cell_size,
                              fill=self.grid.grid[(grid_x, grid_y)],
                              outline="")

    def _draw_bg(self, color="black", alt_color="white"):
        self.create_rectangle(0, 0, self.width, self.height, fill=alt_color)
        self.create_rectangle(self._left, self._up, self._right, self._bottom,
                              fill=color)
