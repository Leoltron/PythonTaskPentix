# !/usr/bin/env python3
import tkinter
from functools import wraps

from gui.grid_canvas import ResizableGridCanvas


def init_gui(game, bg_color, lines_color):
    root = tkinter.Tk()
    root.title('Pentrix')
    root.minsize(200, 200)
    root.geometry('400x400')
    root.iconbitmap(r'gui/icon.ico')
    root.resizable(True, True)
    grid_canvas = ResizableGridCanvas(root, game.grid,
                                      line_color=lines_color,
                                      bg_color=bg_color)
    grid_canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH,
                     side=tkinter.BOTTOM)
    register_events(root, grid_canvas, game)

    def game_loop():
        game.loop()
        grid_canvas.redraw()
        root.title('Pentrix - Score: '+str(game.score))
        root.after(1000, game_loop)

    game_loop()
    root.mainloop()


def register_events(root, grid_canvas, game):
    def redraw_canvas(f):
        @wraps(f)
        def new_f(*args, **kwargs):
            f(*args, **kwargs)
            grid_canvas.redraw()

        return new_f

    def try_and_redraw_canvas(f):
        @wraps(f)
        def new_f(*args, **kwargs):
            if f(*args, **kwargs):
                grid_canvas.redraw()

        return new_f

    @try_and_redraw_canvas
    def on_left_key_pressed(event):
        return game.try_move_left()

    root.bind("<Left>", on_left_key_pressed)
    root.bind("<a>", on_left_key_pressed)
    root.bind("<A>", on_left_key_pressed)

    @try_and_redraw_canvas
    def on_right_key_pressed(event):
        return game.try_move_right()

    root.bind("<Right>", on_right_key_pressed)
    root.bind("<d>", on_right_key_pressed)
    root.bind("<D>", on_right_key_pressed)

    @try_and_redraw_canvas
    def on_down_key_pressed(event):
        return game.try_move_down()

    root.bind("<Down>", on_down_key_pressed)
    root.bind("<s>", on_down_key_pressed)
    root.bind("<S>", on_down_key_pressed)

    @try_and_redraw_canvas
    def on_rotate_key_pressed(event):
        return game.try_rotate()

    root.bind("<Up>", on_rotate_key_pressed)
    root.bind("<w>", on_rotate_key_pressed)
    root.bind("<W>", on_rotate_key_pressed)

    @redraw_canvas
    def on_drop_key_pressed(event):
        game.drop_current_figure()

    root.bind("<space>", on_drop_key_pressed)
