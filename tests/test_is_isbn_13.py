from unittest import TestCase

from string_utils.errors import InvalidInputError
from string_utils.validation import is_isbn_13


class IsISBN13TestCase(TestCase):
    def test_requires_valid_string(self):
        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_13(None))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_13(True))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_13(9780312498580))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn_13([9780312498580]))

    def test_returns_true_for_valid_isbn_13(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertTrue(is_isbn_13('9780312498580'))
        self.assertTrue(is_isbn_13('9781941325827'))
        self.assertTrue(is_isbn_13('9780062853851'))
        self.assertTrue(is_isbn_13('9781250107817'))
        self.assertTrue(is_isbn_13('9788891229243'))

    def test_dashes_are_not_considered_by_default(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertTrue(is_isbn_13('978-0312498580'))
        self.assertTrue(is_isbn_13('978-194-132-582-7'))
        self.assertTrue(is_isbn_13('978-0-0-6-2-8-5-3-8-5-1'))

    def test_isbn_not_recognized_if_normalization_is_disabled(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertFalse(is_isbn_13('978-0312498580', normalize=False))
        self.assertFalse(is_isbn_13('978-194-132-582-7', normalize=False))
        self.assertFalse(is_isbn_13('978-0-0-6-2-8-5-3-8-5-1', normalize=False))

    def test_returns_false_if_isbn_10(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertFalse(is_isbn_13('8891229245'))

    def test_returns_false_if_not_isbn(self):
        self.assertFalse(is_isbn_13('9780312498580!'))
        self.assertFalse(is_isbn_13(' 9780312498580'))
        self.assertFalse(is_isbn_13('x9780312498580'))
        self.assertFalse(is_isbn_13('x' * 13))
        self.assertFalse(is_isbn_13(''))
