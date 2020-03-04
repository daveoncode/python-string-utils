from unittest import TestCase

from string_utils import is_integer


class IsIntegerTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_integer(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_integer(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_integer(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_integer([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_integer({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_returns_true_for_unsigned_integers(self):
        self.assertTrue(is_integer('1'))
        self.assertTrue(is_integer('42'))
        self.assertTrue(is_integer('1e3'))

    def test_returns_true_for_signed_integers(self):
        self.assertTrue(is_integer('+1'))
        self.assertTrue(is_integer('+42'))
        self.assertTrue(is_integer('+1e3'))

        self.assertTrue(is_integer('-1'))
        self.assertTrue(is_integer('-42'))
        self.assertTrue(is_integer('-1e3'))

    def test_returns_false_for_decimals(self):
        self.assertFalse(is_integer('1.1'))
        self.assertFalse(is_integer('42.1'))
        self.assertFalse(is_integer('1.1e3'))

    def test_returns_false_for_string_that_are_not_numbers(self):
        self.assertFalse(is_integer('no'))
        self.assertFalse(is_integer('a1'))
        self.assertFalse(is_integer('ten'))
        self.assertFalse(is_integer('beast666'))
