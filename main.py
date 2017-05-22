# !/usr/bin/env python3
import argparse
from functools import wraps
import tkinter
import generated_figures
from game import Game
import grid


def check_and_return_size(value, min_size, value_name="value"):
    if value:
        if value < min_size:
            raise ValueError(
                "Invalid {}: {} is less than {}".format(
                    value_name,
                    value,
                    min_size))
        return value
    else:
        return min_size


def main():
    if len(tkinter.sys.argv) > 1:
        parsed_args = parse_args()

        if parsed_args.figure_types:
            figure_types = set(parsed_args.figure_types)
        else:
            figure_types = {5}

        min_size = max(figure_types) * 2
        width = check_and_return_size(parsed_args.width, min_size, "width")
        height = check_and_return_size(parsed_args.height, min_size, "height")

        lines_color = parsed_args.lines_color
        bg_color = parsed_args.bg_color
        game = Game(grid_width=width,
                    grid_height=height,
                    figure_types=figure_types,
                    balance_types=parsed_args.balance_types,
                    cell_colors=parsed_args.cells_colors)
    else:
        game = Game()
        lines_color = "white"
        bg_color = "black"
    root = tkinter.Tk()
    root.title('Pentrix')
    root.minsize(200, 200)
    root.geometry('400x400')
    root.iconbitmap(r'icon.ico')
    root.resizable(True, True)
    grid_canvas = grid.ResizableGridCanvas(root, game.grid,
                                           line_color=lines_color,
                                           bg_color=bg_color)
    grid_canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH,
                     side=tkinter.BOTTOM)

    register_events(root, grid_canvas, game)

    def game_loop():
        game.loop()
        grid_canvas.redraw()
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


def parse_args():
    parse = argparse.ArgumentParser(description="Launch a Pentrix game")
    parse.add_argument("-f", "--figure_type",
                       type=int,
                       action='append',
                       help="Add figure type by size",
                       dest='figure_types',
                       choices=generated_figures.get_available_figure_sizes())
    parse.add_argument("-w", "-W", "--width",
                       type=int,
                       help="Game field grid width")
    parse.add_argument("-H", "--height",
                       type=int,
                       help="Game field grid height")
    parse.add_argument("-b", "--balance_types",
                       action="store_true",
                       help="Figures of different sizes will have the equal "
                            "chance of appearance")
    parse.add_argument("--cc", "--cells_colors",
                       type=str,
                       dest="cells_colors",
                       nargs='+',
                       default=["blue", "green", "yellow", "red"])
    parse.add_argument("--bg", "--bg_color",
                       dest="bg_color",
                       type=str,
                       default="black",
                       help="Color of the grid background")
    parse.add_argument("--lc", "--lines_color",
                       dest="lines_color",
                       type=str,
                       default="white",
                       help="Color of the grid lines")
    return parse.parse_args()


if __name__ == '__main__':
    main()
