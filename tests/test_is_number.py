from unittest import TestCase

from string_utils import is_number


class IsNumberTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_number(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_number(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_number(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_number([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            is_number({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_returns_false_if_string_is_empty(self):
        self.assertFalse(is_number(''))
        self.assertFalse(is_number(' '))

    def test_returns_false_if_string_contains_number_but_has_spaces(self):
        self.assertFalse(is_number(' 1'))
        self.assertFalse(is_number('99 '))
        self.assertFalse(is_number(' 1234 '))
        self.assertFalse(is_number(' +1234567890'))
        self.assertFalse(is_number(' 1.2 '))

    def test_returns_false_if_string_is_sign_only(self):
        self.assertFalse(is_number('+'))
        self.assertFalse(is_number('-'))

    def test_returns_false_if_contains_operations(self):
        self.assertFalse(is_number('1 + 1'))
        self.assertFalse(is_number('1+1'))
        self.assertFalse(is_number('1 - 1'))
        self.assertFalse(is_number('1-1'))

    def test_returns_true_for_unsigned_integers(self):
        self.assertTrue(is_number('1'))
        self.assertTrue(is_number('99'))
        self.assertTrue(is_number('1234567890'))

    def test_returns_true_for_signed_integers(self):
        self.assertTrue(is_number('+1'))
        self.assertTrue(is_number('+99'))
        self.assertTrue(is_number('+1234567890'))

        self.assertTrue(is_number('-1'))
        self.assertTrue(is_number('-99'))
        self.assertTrue(is_number('-1234567890'))

    def test_returns_true_for_unsigned_double(self):
        self.assertTrue(is_number('1.0'))
        self.assertTrue(is_number('.007'))
        self.assertTrue(is_number('1.000'))
        self.assertTrue(is_number('99.99'))
        self.assertTrue(is_number('1234567890.000123456'))

    def test_returns_true_for_signed_double(self):
        self.assertTrue(is_number('+1.0'))
        self.assertTrue(is_number('+.007'))
        self.assertTrue(is_number('+1.000'))
        self.assertTrue(is_number('+99.99'))
        self.assertTrue(is_number('+1234567890.000123456'))

        self.assertTrue(is_number('-1.0'))
        self.assertTrue(is_number('-.007'))
        self.assertTrue(is_number('-1.000'))
        self.assertTrue(is_number('-99.99'))
        self.assertTrue(is_number('-1234567890.000123456'))

    def test_double_cannot_contain_multiple_dots(self):
        self.assertFalse(is_number('+1..0'))
        self.assertFalse(is_number('+..007'))
        self.assertFalse(is_number('+1..000'))
        self.assertFalse(is_number('+99..99'))
        self.assertFalse(is_number('+1234567890..000123456'))

        self.assertFalse(is_number('-1..0'))
        self.assertFalse(is_number('-..007'))
        self.assertFalse(is_number('-1..000'))
        self.assertFalse(is_number('-99..99'))
        self.assertFalse(is_number('-1234567890..000123456'))

    def test_number_cannot_contain_multiple_sign(self):
        self.assertFalse(is_number('+-1'))
        self.assertFalse(is_number('++1'))
        self.assertFalse(is_number('--1'))
        self.assertFalse(is_number('+-1.1'))
        self.assertFalse(is_number('++1.1'))
        self.assertFalse(is_number('--1.1'))

    def test_returns_true_for_scientific_notation(self):
        self.assertTrue(is_number('1e3'))
        self.assertTrue(is_number('50e2'))
        self.assertTrue(is_number('1.245e10'))
