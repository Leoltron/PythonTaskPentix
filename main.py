# !/usr/bin/env python3
import functools
import random
from tkinter import *
from grid import *
from figures import *

root = Tk()
root.title('Pentrix')
root.minsize(200, 200)
root.geometry('400x400')
root.iconbitmap(r'icon.ico')
root.resizable(True, True)
color_grid = ColorGrid(10, 10)
grid_canvas = ResizableGridCanvas(root,
                                  color_grid,
                                  width=200,
                                  height=200)
grid_canvas.pack(expand=YES, fill=BOTH)

"""
def refresh():
    global figure
    for coord in color_grid.grid:
        color_grid.grid[coord] = color_grid.default_cell_color
    figure = generate_normalized_figure()
    for coord in figure:
        color_grid.grid[coord] = "red"
    grid_canvas.redraw()

    root.after(1000, refresh)

def rotate(event):
    global figure
    for coord in color_grid.grid:
        color_grid.grid[coord] = color_grid.default_cell_color
    figure = get_normalized_figure(get_rotated_figure(figure))
    for coord in figure:
        color_grid.grid[coord] = "blue"
    grid_canvas.redraw()

root.bind("<Key>", rotate)
refresh()
"""
figures = list()
for figure in generate_figures(6):
    if figure not in figures:
        figures.append(figure)
i = 0


def game_loop():
    global figures
    global i
    root.title('Pentrix - '+str(i))
    for coord in color_grid.grid:
        color_grid.grid[coord] = color_grid.default_cell_color
    figure = figures[i].get_points()
    for coord in figure:
        color_grid.grid[coord] = "blue"
    i = (i + 1) % len(figures)
    grid_canvas.redraw()

    root.after(100, game_loop)

game_loop()
root.mainloop()
