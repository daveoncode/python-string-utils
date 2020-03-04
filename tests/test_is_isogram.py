from unittest import TestCase

from string_utils import is_isogram


class IsIsogramTestCase(TestCase):
    def test_non_string_objects_return_false(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_isogram(1))

        # noinspection PyTypeChecker
        self.assertFalse(is_isogram(['xx']))

        # noinspection PyTypeChecker
        self.assertFalse(is_isogram({}))

        # noinspection PyTypeChecker
        self.assertFalse(is_isogram(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_isogram((1, 2, 3)))

        # noinspection PyTypeChecker
        self.assertFalse(is_isogram(object()))

    def test_empty_strings_are_not_isograms(self):
        self.assertFalse(is_isogram(''))
        self.assertFalse(is_isogram(' '))
        self.assertFalse(is_isogram(' \n \t '))

    def test_is_isogram_returns_true_if_isogram(self):
        self.assertTrue(is_isogram('dermatoglyphics'))
        self.assertTrue(is_isogram('abcdefghilmnopqrs'))

    def test_is_isogram_returns_false_if_not_isogram(self):
        self.assertFalse(is_isogram('hello'))
        self.assertFalse(is_isogram('hello world, how are you?'))
