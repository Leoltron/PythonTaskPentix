# !/usr/bin/env python3
import functools
import random
from tkinter import *
from grid import *


def generate_normalized_figure():
    return get_normalized_figure(generate_figure())


def get_normalized_figure(figure):
    minx = sys.maxsize
    miny = sys.maxsize
    for x, y in figure:
        minx = x if minx > x else minx
        miny = y if miny > y else miny
    minx *= -1
    miny *= -1
    normalized_figure = list()
    for x, y in figure:
        normalized_figure.append((x + minx, y + miny))
    return normalized_figure


def generate_figure():
    figure = [(0, 0)]
    while len(figure) < 5:
        start = random.choice(figure)
        figure.append(random.choice(get_neighbours(*start, figure)))
    return figure


def get_neighbours(x, y, blacklist_points):
    neighbours = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if abs(dx) + abs(dy) == 1 and \
                            (x + dx, y + dy) not in blacklist_points:
                neighbours.append((x + dx, y + dy))
    return neighbours


root = Tk()
root.title('Pentrix')
root.minsize(200, 200)
root.geometry('400x400')
root.iconbitmap(r'icon.ico')
root.resizable(True, True)
color_grid = ColorGrid(5, 5)
grid_canvas = ResizableGridCanvas(root,
                                  color_grid,
                                  width=200,
                                  height=200)
grid_canvas.pack(expand=YES, fill=BOTH)


def refresh():
    for coord in color_grid.grid:
        color_grid.grid[coord] = color_grid.default_cell_color
    for coord in generate_normalized_figure():
        color_grid.grid[coord] = "blue"
    grid_canvas.redraw()

    root.after(1000, refresh)


refresh()
root.mainloop()
