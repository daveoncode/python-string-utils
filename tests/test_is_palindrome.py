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
        self.assertFalse(is_palindrome('\n\t\n'))

    def test_returns_true_if_palindrome_with_default_options(self):
        self.assertTrue(is_palindrome('LOL'))
        self.assertTrue(is_palindrome('otto'))

    def test_returns_false_if_not_palindrome_with_default_options(self):
        self.assertFalse(is_palindrome('nope!'))
        self.assertFalse(is_palindrome('ROTFL'))

    def test_if_not_specified_case_matters(self):
        self.assertFalse(is_palindrome('Lol'))
        self.assertTrue(is_palindrome('Lol', ignore_case=True))

    def test_if_not_specified_spaces_matter(self):
        self.assertFalse(is_palindrome('i topi non avevano nipoti'))
        self.assertTrue(is_palindrome('i topi non avevano nipoti', ignore_spaces=True))
