from unittest import TestCase

from string_utils import is_palindrome


class IsPalindromeTestCase(TestCase):
    def test_non_string_objects_return_false(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_palindrome(1))

        # noinspection PyTypeChecker
        self.assertFalse(is_palindrome(['xx']))

        # noinspection PyTypeChecker
        self.assertFalse(is_palindrome({}))

        # noinspection PyTypeChecker
        self.assertFalse(is_palindrome(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_palindrome((1, 2, 3)))

        # noinspection PyTypeChecker
        self.assertFalse(is_palindrome(object()))

    def test_empty_strings_are_not_palindromes(self):
        self.assertFalse(is_palindrome(''))
        self.assertFalse(is_palindrome(' '))
        self.assertFalse(is_palindrome(' \n\t '))

    def test_strict_checking(self):
        self.assertFalse(is_palindrome('nope!'))
        self.assertFalse(is_palindrome('i topi non avevano nipoti'))
        self.assertTrue(is_palindrome('otto'))

    def test_no_strict_mode(self):
        self.assertFalse(is_palindrome('nope!', False))
        self.assertTrue(is_palindrome('i topi non avevano nipoti', False))
        self.assertTrue(is_palindrome('otto', False))
