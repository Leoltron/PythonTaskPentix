# !/usr/bin/env python3
import argparse

import sys

from game.generated_figures import get_available_figure_sizes
from game.pentrix_game import PentrixGame
from gui.gui_main import init_gui


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
    if len(sys.argv) > 1:
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
        game = PentrixGame(grid_width=width,
                           grid_height=height,
                           figure_types=figure_types,
                           balance_types=parsed_args.balance_types,
                           cell_colors=parsed_args.cells_colors)
    else:
        game = PentrixGame()
        lines_color = "white"
        bg_color = "black"
    init_gui(game, bg_color, lines_color)


def parse_args():
    parse = argparse.ArgumentParser(description="Launch a Pentrix game")
    parse.add_argument("-f", "--figure_type",
                       type=int,
                       action='append',
                       help="Add figure type by size",
                       dest='figure_types',
                       choices=get_available_figure_sizes())
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
