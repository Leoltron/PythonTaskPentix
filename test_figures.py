#!/usr/bin/env python3

import unittest
import figures


class TestFigures(unittest.TestCase):
    def test_normalize_figure(self):
        figure = {(-1, -1), (-1, -2), (-2, -1), (-2, -2)}
        normalized_figure = figures.get_normalized_figure(figure)
        self.assertEqual(normalized_figure, {(0, 0), (0, 1), (1, 0), (1, 1)})

    def test_rotate_figure_L(self):
        figure = {(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)}
        self.assertEqual(
            figures.get_normalized_figure(
                figures.get_clockwise_rotated_figure(figure)
            ),
            {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)})

    def test_rotate_figure_O(self):
        figure = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.assertEqual(
            figures.get_normalized_figure(
                figures.get_clockwise_rotated_figure(figure)
            ),
            {(0, 0), (0, 1), (1, 0), (1, 1)})

    def test_neighbours(self):
        neighbours = set(figures.get_neighbours(0, 0))
        expected = {(0, 1), (1, 0), (-1, 0), (0, -1)}
        self.assertEqual(neighbours, expected)

    def test_neighbours_blacklist(self):
        neighbours = set(figures.get_neighbours(0, 0, [(0, -1)]))
        expected = {(0, 1), (1, 0), (-1, 0)}
        self.assertEqual(neighbours, expected)
