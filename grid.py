from tkinter import Canvas


class ColorGrid:
    def __init__(self, width, height, default_cell_color="black",
                 line_color="white"):
        self._width = width
        self._height = height
        self._default_cell_color = default_cell_color
        self._line_color = line_color
        self._grid = dict()
        for x in range(width):
            for y in range(height):
                self._grid[(x, y)] = default_cell_color

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def default_cell_color(self):
        return self._default_cell_color

    @property
    def line_color(self):
        return self._line_color

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, value):
        if not isinstance(value, dict):
            raise ValueError("grid is dictionary!")
        for coords in value:
            if not isinstance(coords, tuple):
                raise ValueError(str(coords) + "must be tuple!")
            for i in range(2):
                if not isinstance(coords[i], int):
                    raise ValueError(str(coords[i]) + "must be integer!")
                if coords[i] < 0:
                    raise ValueError(str(coords[i]) + "must not be negative!")
                if coords[0] >= self._width or coords[1] >= self._height:
                    raise ValueError(
                        "{} is out of grid bounds: ({},{})"
                            .format(str(coords), self._width, self._height))
        self._grid = dict()
        for x in range(self._width):
            for y in range(self._height):
                self._grid[(x, y)] = self._default_cell_color
        for coords, color in value.items():
            self._grid[coords] = color


class ResizableGridCanvas(Canvas):
    def __init__(self, parent, grid, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.grid = grid
        self.update_size()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        # self.config(width=self.width, height=self.height)
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
        self._draw_bg(self.grid.default_cell_color)
        x = self._left
        for grid_x in range(self.grid.width):
            y = self._up
            for grid_y in range(self.grid.height):
                if self.grid.grid[(grid_x, grid_y)] != \
                        self.grid.default_cell_color:
                    self.draw_cell(x, y, grid_x, grid_y)
                y += 1 + self._cell_size
            x += 1 + self._cell_size
        self._draw_grid()

    def _draw_grid(self):
        x = self._left + self._cell_size
        for i in range(self.grid.width - 1):
            self.create_line(x, self._up, x, self._bottom,
                             fill=self.grid.line_color)
            x += 1 + self._cell_size
        y = self._up + self._cell_size
        for i in range(self.grid.height - 1):
            self.create_line(self._left, y, self._right, y,
                             fill=self.grid.line_color)
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
