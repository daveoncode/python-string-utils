from unittest import TestCase

from string_utils import is_decimal


class IsDecimalTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_decimal(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_decimal(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_decimal(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_decimal([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_decimal({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_returns_true_for_unsigned_decimals(self):
        self.assertTrue(is_decimal('1.1'))
        self.assertTrue(is_decimal('42.123'))
        self.assertTrue(is_decimal('1.999e3'))

    def test_returns_true_for_signed_decimals(self):
        self.assertTrue(is_decimal('+1.1'))
        self.assertTrue(is_decimal('+42.999'))
        self.assertTrue(is_decimal('+1.999e3'))

        self.assertTrue(is_decimal('-1.999'))
        self.assertTrue(is_decimal('-42.999'))
        self.assertTrue(is_decimal('-1.999e3'))

    def test_cannot_contain_multiple_dots(self):
        self.assertFalse(is_decimal('+1...1'))
        self.assertFalse(is_decimal('+42..999'))
        self.assertFalse(is_decimal('+1..999e3'))

        self.assertFalse(is_decimal('-1..999'))
        self.assertFalse(is_decimal('-42...999'))
        self.assertFalse(is_decimal('-1......999e3'))

    def test_cannot_contain_spaces(self):
        self.assertFalse(is_decimal('1. 1'))
        self.assertFalse(is_decimal('1 .1'))
        self.assertFalse(is_decimal('1 . 1'))
        self.assertFalse(is_decimal(' 1.1'))
        self.assertFalse(is_decimal('1.1 '))
        self.assertFalse(is_decimal(' 1.1 '))

    def test_returns_false_for_integers(self):
        self.assertFalse(is_decimal('1'))
        self.assertFalse(is_decimal('42'))
        self.assertFalse(is_decimal('1e3'))

    def test_returns_false_for_string_that_are_not_numbers(self):
        self.assertFalse(is_decimal('no'))
        self.assertFalse(is_decimal('a1.1'))
        self.assertFalse(is_decimal('ten'))
        self.assertFalse(is_decimal('>1.1'))
        self.assertFalse(is_decimal('1.1?'))
