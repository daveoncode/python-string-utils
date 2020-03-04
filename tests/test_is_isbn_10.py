from unittest import TestCase

from string_utils.errors import InvalidInputError
from string_utils.validation import is_isbn_10


class IsISBN10TestCase(TestCase):
    def test_requires_valid_string(self):
        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_10(None))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_10(True))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_10(9780312498580))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_10([9780312498580]))

    def test_returns_true_for_valid_isbn_10(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertTrue(is_isbn_10('1506715214'))
        self.assertTrue(is_isbn_10('1506715532'))
        self.assertTrue(is_isbn_10('0451494504'))
        self.assertTrue(is_isbn_10('0718079183'))
        self.assertTrue(is_isbn_10('8830102180'))

    def test_dashes_are_not_considered_by_default(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertTrue(is_isbn_10('150-6715214'))
        self.assertTrue(is_isbn_10('150-671-5532'))
        self.assertTrue(is_isbn_10('045-14-94-50-4'))
        self.assertTrue(is_isbn_10('071-8-0-7-9-1-8-3'))
        self.assertTrue(is_isbn_10('8-8-3-0-1-0-2-1-8-0'))

    def test_isbn_not_recognized_if_normalization_is_disabled(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertFalse(is_isbn_10('150-6715214', normalize=False))
        self.assertFalse(is_isbn_10('150-671-521-4', normalize=False))

    def test_returns_false_if_isbn_13(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertFalse(is_isbn_10('978-8830102187'))
        self.assertFalse(is_isbn_10('9788830102187'))

    def test_returns_false_if_not_isbn(self):
        self.assertFalse(is_isbn_10('1506715214!'))
        self.assertFalse(is_isbn_10(' 1506715214'))
        self.assertFalse(is_isbn_10('1506715214y'))
        self.assertFalse(is_isbn_10('x' * 10))
        self.assertFalse(is_isbn_10(''))
