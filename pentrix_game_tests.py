# !/usr/bin/env python3

import unittest

from game.pentrix_game import ColorGrid, FiguresList, PentrixGame


class TestColorGrid(unittest.TestCase):
    def test_create(self):
        ColorGrid(10, 10)

    def test_create_wrong(self):
        self.assertRaises(ValueError, ColorGrid, width=-10, height=10)
        self.assertRaises(ValueError, ColorGrid, width=10, height=-10)
        self.assertRaises(ValueError, ColorGrid, width=-10, height=-10)
        self.assertRaises(TypeError, ColorGrid, width="10", height=10)

    def test_properties(self):
        grid = ColorGrid(10, 20)
        self.assertEqual(grid.width, 10)
        self.assertEqual(grid.height, 20)

    def test_is_line_full(self):
        grid = ColorGrid(10, 20)
        for x in range(10):
            grid.grid[x, 5] = "white"
        for y in range(20):
            grid.grid[5, y] = "black"
        for y in range(30):
            if y == 5:
                self.assertTrue(grid.is_line_full(y))
            else:
                self.assertFalse(grid.is_line_full(y))

    def test_is_line_full_same_color(self):
        grid = ColorGrid(10, 20)
        for x in range(10):
            grid.grid[x, 5] = "white"
        for y in range(20):
            grid.grid[5, y] = "black"
        for y in range(30):
            self.assertFalse(grid.is_line_full_same_color(y))
        grid.grid[5, 5] = "white"
        self.assertTrue(grid.is_line_full_same_color(5))
        grid.grid[5, 5] = "rainbow"
        self.assertTrue(grid.is_line_full_same_color(5))

    def test_clear(self):
        grid = ColorGrid(10, 20)
        for x in range(10):
            grid.grid[x, 5] = "white"
        for y in range(20):
            grid.grid[5, y] = "black"
        grid.clear()
        for x, y in grid.grid:
            self.assertTrue(grid.grid[x, y] is None)


class TestFiguresList(unittest.TestCase):
    def test_create(self):
        FiguresList({1, 2, 3}, False)
        FiguresList({1, 2, 3}, True)

    def test_rand_figure(self):
        l1 = FiguresList({1, 2, 3}, False)
        l1.get_random_figure()
        l2 = FiguresList({1, 2, 3}, True)
        l2.get_random_figure()


class TestPentrixGame(unittest.TestCase):
    def test_create(self):
        PentrixGame()

    def test_moving(self):
        game = PentrixGame(figure_types={1}, grid_width=10, grid_height=10)
        x = game.current_figure_x
        y = game.current_figure_y
        game.loop()
        self.assertTupleEqual((x, y + 1), (game.current_figure_x,
                                           game.current_figure_y))
        if game.try_move_left():
            x -= 1
        self.assertTupleEqual((x, y + 1), (game.current_figure_x,
                                           game.current_figure_y))
        if game.try_move_right():
            x += 1
        self.assertTupleEqual((x, y + 1), (game.current_figure_x,
                                           game.current_figure_y))

    def test_finish_figure_flight(self):
        game = PentrixGame(grid_width=20, grid_height=20)
        for x in range(20):
            game.grid.grid[x, 19] = "black"
        game.drop_current_figure()
        self.assertEqual(game.score, 700)

    def test_update_bombs(self):
        game = PentrixGame(grid_width=20, grid_height=20)
        for x in range(4, 7):
            for y in range(4, 7):
                game.grid.grid[x, y] = "red"
        game.grid.grid[5, 5] = "1:red"
        game.update_time_bombs()
        for x in range(4, 7):
            for y in range(4, 7):
                self.assertTrue(game.grid.grid[x, y] is None)

    def test_explode(self):
        game = PentrixGame(grid_width=20, grid_height=20)
        for x in range(4, 7):
            for y in range(4, 7):
                game.grid.grid[x, y] = "red"
        game.explode_at(5, 5)
        for x in range(4, 7):
            for y in range(4, 7):
                self.assertTrue(game.grid.grid[x, y] is None)

    def test_try_rotate(self):
        game = PentrixGame(figure_types={1}, grid_width=10, grid_height=10)
        x = game.current_figure_x
        y = game.current_figure_y
        game.loop()
        self.assertTrue(game.try_rotate())
        self.assertTupleEqual((x, y + 1), (game.current_figure_x,
                                           game.current_figure_y))
