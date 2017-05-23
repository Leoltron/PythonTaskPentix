# !/usr/bin/env python3
from tkinter import Canvas


class ResizableGridCanvas(Canvas):
    def __init__(self, parent, grid,
                 line_color="white",
                 bg_color="black",
                 **kwargs):
        super().__init__(parent, **kwargs)
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
        self.delete('all')
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
        color = self.grid.grid[(grid_x, grid_y)]
        if color == 'rainbow':
            self.draw_rainbow_cell(x, y)
        elif color.startswith("*"):
            self.draw_eraser(x, y, color[1:])
        elif ":" in color:
            splitted_color = color.split(":", 1)
            self.draw_time_bomb(x, y, splitted_color[1],
                                int(splitted_color[0]))
        else:
            self.draw_normal_cell(x, y, color)

    def draw_normal_cell(self, x, y, color):
        self.create_rectangle(x, y,
                              x + self._cell_size,
                              y + self._cell_size,
                              fill=color,
                              outline="")

    def draw_rainbow_cell(self, x, y):
        a = self._cell_size / 4
        self.draw_normal_cell(x, y, 'green')
        self.create_polygon([x, y, x, y + a * 3, x + a * 3, y],
                            fill="yellow", outline="")
        self.create_polygon([x, y, x, y + a * 2, x + a * 2, y],
                            fill="orange", outline="")
        self.create_polygon([x, y, x, y + a, x + a, y], fill="red",
                            outline="")
        a *= -1
        x += self._cell_size
        y += self._cell_size
        self.create_polygon([x, y, x, y + a * 3, x + a * 3, y],
                            fill="cyan", outline="")
        self.create_polygon([x, y, x, y + a * 2, x + a * 2, y],
                            fill="blue", outline="")
        self.create_polygon([x, y, x, y + a, x + a, y], fill="purple",
                            outline="")

    def _draw_bg(self, color="black", alt_color="white"):
        self.create_rectangle(0, 0, self.width, self.height, fill=alt_color,
                              outline="")
        self.create_rectangle(self._left, self._up, self._right, self._bottom,
                              fill=color,
                              outline="")

    ERASER_BORDER_WIDTH = 4

    def draw_eraser(self, x, y, color):
        hw = self.ERASER_BORDER_WIDTH / 2
        self.create_rectangle(x + hw,
                              y + hw,
                              x + self._cell_size - hw,
                              y + self._cell_size - hw,
                              outline=color,
                              width=str(self.ERASER_BORDER_WIDTH))

    def draw_time_bomb(self, x, y, color, time):
        c_x = x + self._cell_size / 2
        c_y = y + self._cell_size / 2
        if time >= 1:
            self.create_polygon(
                [c_x, y, c_x, c_y, x, c_y],
                fill=color,
                outline="")
        if time >= 2:
            self.create_polygon(
                [c_x, y, c_x, c_y, x + self._cell_size, c_y],
                fill=color,
                outline="")
        if time >= 3:
            self.create_polygon(
                [c_x, y + self._cell_size, c_x, c_y, x + self._cell_size, c_y],
                fill=color,
                outline="")
        if time >= 4:
            self.create_polygon(
                [c_x, y + self._cell_size, c_x, c_y, x, c_y],
                fill=color,
                outline="")
