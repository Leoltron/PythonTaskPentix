# !/usr/bin/env python3
import argparse
from functools import wraps
from tkinter import *
import generated_figures
from game import Game
from grid import *


def check_and_return_size(value, min_size, value_name="value"):
    if value:
        if value < min_size:
            raise argparse.ArgumentError(
                "Invalid {}: {} is less than {}".format(
                    value_name,
                    value,
                    min_size))
        return value
    else:
        return min_size


def main():
    if len(sys.argv) > 1:
        args = parse_args()
        figure_types = set(args.figure_types)

        min_size = max(figure_types) * 2
        width = check_and_return_size(args.width, min_size, "width")
        height = check_and_return_size(args.height, min_size, "height")
        game = Game(grid_width=width,
                    grid_height=height,
                    figure_types=figure_types,
                    balance_types=args.balance_types,
                    cell_colors=args.cells_colors)
    else:
        game = Game()
    root = Tk()
    root.title('Pentrix')
    root.minsize(200, 200)
    root.geometry('400x400')
    root.iconbitmap(r'icon.ico')
    root.resizable(True, True)
    grid_canvas = ResizableGridCanvas(root, game.grid)
    grid_canvas.pack(expand=YES, fill=BOTH)

    root.mainloop()


def parse_args():
    parse = argparse.ArgumentParser(description="Launch a Pentrix game")
    parse.add_argument("-f", "--figure_type", type=int, action='append',
                       help="Add figure type by size",
                       dest='figure_types',
                       default=[5],
                       choices=generated_figures.get_available_figure_sizes())
    parse.add_argument("-w", "-W", "--width", type=int,
                       help="Game field grid width")
    parse.add_argument("-H", "--height", type=int,
                       help="Game field grid height")
    parse.add_argument("-b", "--balance_types", action="store_true",
                       help="Figures of different sizes will have the equal "
                            "chance of appearance")
    parse.add_argument("--cc", "--cells_colors", type=list,
                       dest="cells_colors",
                       default=["blue", "green", "yellow", "red"])
    parse.add_argument("--bg", "--bg_color", type=str, default="black",
                       help="Color of the grid background")
    parse.add_argument("--lc", "--lines_color", type=str, default="white",
                       help="Color of the grid lines")
    return parse.parse_args()


if __name__ == '__main__':
    main()

'''
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

figures = get_figures(5)
i = 0


def game_loop():
    global figures
    global i
    root.title('Pentrix - ' + str(i))
    for coord in color_grid.grid:
        color_grid.grid[coord] = None
    figure = figures[10].get_points()
    for coord in figure:
        color_grid.grid[coord] = "blue"
    i = (i + 1) % len(figures)
    grid_canvas.redraw()

def on_key_pressed(event):
    game_loop()

root.bind("<Key>", on_key_pressed)
game_loop()
root.mainloop()
'''
