#!/usr/bin/env python3

import unittest

from game import figures
import game.generated_figures


def is_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str) or len(obj) != 1


class TestIsIterable(unittest.TestCase):
    def test_iterable(self):
        self.assertTrue(is_iterable(list()))
        self.assertTrue(is_iterable(set()))
        self.assertTrue(is_iterable(dict()))
        self.assertTrue(is_iterable(tuple()))
        self.assertTrue(is_iterable("Text"))

    def test__not_iterable(self):
        self.assertFalse(is_iterable(0))
        self.assertFalse(is_iterable("c"), "One char should not be counted as "
                                           "iterable")
        self.assertFalse(is_iterable(0.0))


def is_iterables_equal_no_order(i1, i2):
    if not (is_iterable(i1) and is_iterable(i2)):
        raise TypeError("Both arguments must be iterable!")
    if len(i1) != len(i2):
        return False
    for element1 in i1:
        if is_iterable(element1):
            element1_in_i2 = False
            for element2 in i2:
                if is_iterable(element2) and is_iterables_equal_no_order(
                        element1, element2):
                    element1_in_i2 = True
                    break
            if not element1_in_i2:
                return False
        else:
            if element1 not in i2:
                return False
    return True


class TestIterablesEqualsNoOrder(unittest.TestCase):
    def test_wrong_types(self):
        self.assert_type_error(0, 0)
        self.assert_type_error([], 0)
        self.assert_type_error(0, [])

    def assert_type_error(self, obj1, obj2):
        self.assertRaises(TypeError, is_iterables_equal_no_order,
                          [obj1, obj2])

    def test_fully_equal_iterables(self):
        self.assertTrue(is_iterables_equal_no_order([1, 2, 3], [1, 2, 3]))
        self.assertTrue(is_iterables_equal_no_order(
            ["a", "b", "c"],
            ["a", "b", "c"]))

    def test_fully_not_equal_iterables(self):
        self.assertFalse(is_iterables_equal_no_order([1, 2, 3], [4, 5, 6]))
        self.assertFalse(is_iterables_equal_no_order(
            ["a", "b", "c"],
            ["d", "e", "f"]))

    def test_different_length(self):
        self.assertFalse(is_iterables_equal_no_order([1, 2], [4, 5, 6]))
        self.assertFalse(is_iterables_equal_no_order(
            ["a", "b", "c"],
            ["d", "e"]))

    def test_wrong_order_iterables(self):
        self.assertTrue(is_iterables_equal_no_order([1, 2, 3], [3, 1, 2]))
        self.assertTrue(is_iterables_equal_no_order(
            ["a", "b", "c"],
            ["c", "b", "a"]))

    def test_deep_wrong_order(self):
        i1 = [{(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)},
              {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)},
              {(0, 2), (2, 0), (2, 2), (2, 1), (1, 2)},
              {(0, 0), (2, 0), (1, 0), (2, 1), (1, 2)}]
        i2 = [{(0, 0), (1, 0), (0, 1), (0, 2), (2, 0)},
              {(0, 0), (2, 1), (2, 0), (1, 0), (1, 2)},
              {(0, 2), (2, 2), (2, 1), (2, 0), (1, 2)},
              {(0, 0), (0, 2), (1, 2), (0, 1), (2, 2)}]
        self.assertTrue(is_iterables_equal_no_order(i1, i2))


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

    def test_get_rotations_O(self):
        figure = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.assertEqual([figure], figures.get_rotations(figure))

    def test_get_rotations_L(self):
        figure = {(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)}
        rotations_actual = figures.get_rotations(figure)
        rotations_expected = [{(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)},
                              {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)},
                              {(0, 2), (2, 0), (2, 2), (2, 1), (1, 2)},
                              {(0, 0), (2, 0), (1, 0), (2, 1), (1, 2)}]
        self.assertTrue(is_iterables_equal_no_order(rotations_actual,
                                                    rotations_expected))

    def test_generated_figures_available(self):
        for i in game.generated_figures.get_available_figure_sizes():
            game.generated_figures.get_figures(i)

    def test_generate_figures(self):
        figure_size = 5
        expected = list(game.generated_figures.get_figures(figure_size))
        actual = list(figures.generate_figures_cleared(figure_size))

        self.assertTrue(is_iterables_equal_no_order(expected, actual))

    def test_generate_figures_wrong_size(self):
        self.assertRaises(ValueError, game.generated_figures.get_figures, [-10])
        self.assertRaises(ValueError, game.generated_figures.get_figures, [10])


class TestFigureClass(unittest.TestCase):
    def test_create(self):
        figures.Figure({(0, 0), (0, 1)})
        figures.Figure({(-2, -2), (-2, -1)})

    def test_get_points(self):
        rotations = [{(0, 0), (1, 0)}, {(0, 0), (0, 1)}]
        figure = figures.Figure(rotations[0])
        self.assertIn(figure.get_points(), rotations)

    def test_get_points_dx_dy(self):
        rotations = [{(0, 0), (1, 0)}, {(0, 0), (0, 1)}]
        figure = figures.Figure(rotations[0])
        dx = 10
        dy = 5
        rotations_moved = [{(0 + dx, 0 + dy), (1 + dx, 0 + dy)},
                           {(0 + dx, 0 + dy), (0 + dx, 1 + dy)}]
        self.assertIn(figure.get_points_moved(dx, dy), rotations_moved)

    def test_rotate(self):
        rotations = [{(0, 0), (1, 0)}, {(0, 0), (0, 1)}]
        figure = figures.Figure(rotations[0])
        rotation_1 = figure.get_points()
        figure.rotate()
        self.assertIn(figure.get_points(), rotations)
        self.assertNotEqual(figure.get_points(), rotation_1, "Rotation have "
                                                             "not changed the "
                                                             "figure")

    def test_eq(self):
        rotations = [{(0, 0), (1, 0)}, {(0, 0), (0, 1)}]
        figure1 = figures.Figure(rotations[0])
        figure2 = figures.Figure(rotations[1])
        self.assertEqual(figure1, figure2)
        self.assertNotEqual(figure1, rotations[1])

    def test_neq(self):
        figure1 = figures.Figure({(0, 1), (1, 0), (1, 1)})
        figure2 = figures.Figure({(2, 0), (1, 0), (0, 0)})
        self.assertNotEqual(figure1, figure2)

    def test_repr(self):
        figure1 = figures.Figure({(0, 1), (1, 0), (1, 1)})
        figure2 = figures.Figure({(2, 0), (1, 0), (0, 0)})

        self.assertEqual(repr(figure1), "Figure({(0, 1), (1, 0), (1, 1)})")
        self.assertEqual(repr(figure2), "Figure({(2, 0), (1, 0), (0, 0)})")
