from unittest import TestCase

from string_utils import is_full_string


class IsFullStringTestCase(TestCase):
    def test_empty_string_is_not_full(self):
        self.assertFalse(is_full_string(''))

    def test_white_space_is_not_full(self):
        self.assertFalse(is_full_string(' '))
        self.assertFalse(is_full_string('\t'))
        self.assertFalse(is_full_string('''
            \n
            \n
            \n
        '''))

    def test_word_string_is_full(self):
        self.assertTrue(is_full_string('ciao'))
        self.assertTrue(is_full_string(' hi '))
        self.assertTrue(is_full_string('1'))
        self.assertTrue(is_full_string(' @*& '))
        self.assertTrue(is_full_string('...'))
