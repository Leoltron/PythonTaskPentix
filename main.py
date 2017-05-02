# !/usr/bin/env python3
from functools import wraps
from tkinter import *

from game import Game
from grid import *


def mix_colors(color1, color2):
    if not (isinstance(color1, int) and isinstance(color2, int)):
        raise TypeError("Colors must be integers!")
    return (color1 + color2) / 2


root = Tk()
root.title('Pentrix')
root.minsize(200, 200)
root.geometry('400x400')
root.iconbitmap(r'icon.ico')
root.resizable(True, True)
game = Game(grid_width=10,
            grid_height=20,
            figures_types={4},
            balance_types=False,
            cell_colors=["green"])
grid_canvas = ResizableGridCanvas(root,
                                  game.grid,
                                  width=200,
                                  height=200)
game.connect_to_grid_canvas(grid_canvas)
grid_canvas.pack(expand=YES, fill=BOTH)

update_period = 1000
paused = False


def try_and_call(func):
    def try_and_call_func(f):
        @wraps(f)
        def new_f(*args, **kwargs):
            if f(*args, **kwargs):
                func()

        return new_f

    return try_and_call_func


def game_loop():
    global paused
    if not paused:
        global update_period
        game.loop()
        grid_canvas.redraw()
    root.after(update_period, game_loop)


@try_and_call(grid_canvas.redraw)
def on_key_left_press(event):
    return game.try_move_left()


root.bind("<Left>", on_key_left_press)
root.bind("<a>", on_key_left_press)


@try_and_call(grid_canvas.redraw)
def on_key_right_press(event):
    return game.try_move_right()


root.bind("<Right>", on_key_right_press)
root.bind("<d>", on_key_right_press)


@try_and_call(grid_canvas.redraw)
def on_down_key_press(event):
    return game.try_move_down()


root.bind("<Down>", on_down_key_press)
root.bind("<s>", on_down_key_press)


@try_and_call(grid_canvas.redraw)
def on_up_key_press(event):
    return game.try_rotate()


root.bind("<Up>", on_up_key_press)
root.bind("<w>", on_up_key_press)


def on_space_press(event):
    game.drop_current_figure()
    grid_canvas.redraw()


root.bind("<space>", on_space_press)


def on_pause_key(event):
    global paused
    paused = not paused
    grid_canvas.redraw()


root.bind("<p>", on_pause_key)

game_loop()
root.mainloop()
