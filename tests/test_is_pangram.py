from unittest import TestCase

from string_utils import is_pangram


class IsPangramTestCase(TestCase):
    def test_non_string_objects_return_false(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_pangram(1))

        # noinspection PyTypeChecker
        self.assertFalse(is_pangram(['xx']))

        # noinspection PyTypeChecker
        self.assertFalse(is_pangram({}))

        # noinspection PyTypeChecker
        self.assertFalse(is_pangram(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_pangram((1, 2, 3)))

        # noinspection PyTypeChecker
        self.assertFalse(is_pangram(object()))

    def test_is_pangram_returns_false_if_not_pangram(self):
        self.assertFalse(is_pangram('hello world'))

    def test_is_pangram_returns_true_if_pangram(self):
        self.assertTrue(is_pangram('The quick brown fox jumps over the lazy dog'))

    def test_pangram_is_case_insensitive(self):
        for value in ('THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG',
                      'Sphinx of black quartz, judge my vow.',
                      'AbCdEfGhIjKlMnOpQrStUvWxYz'):
            with self.subTest(value=value):
                self.assertTrue(is_pangram(value))

    def test_uppercase_does_not_make_an_incomplete_alphabet_a_pangram(self):
        for value in ('THE QUICK BROWN FOX JUMPS OVER THE DOG',
                      'ABCDEFGHIJKLMNOPQRSTUVWXY', '123!?'):
            with self.subTest(value=value):
                self.assertFalse(is_pangram(value))
