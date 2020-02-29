from unittest import TestCase

from string_utils import booleanize


class BooleanizeTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            booleanize(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            booleanize(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            booleanize(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            booleanize([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            booleanize({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_returns_false_for_empty_strings(self):
        self.assertFalse(booleanize(''))
        self.assertFalse(booleanize(' '))

    def test_returns_true_for_positive_strings(self):
        self.assertTrue(booleanize('true'))
        self.assertTrue(booleanize('TRUE'))
        self.assertTrue(booleanize('True'))
        self.assertTrue(booleanize('1'))
        self.assertTrue(booleanize('yes'))
        self.assertTrue(booleanize('YES'))
        self.assertTrue(booleanize('Yes'))
        self.assertTrue(booleanize('y'))
        self.assertTrue(booleanize('Y'))

    def test_returns_false_for_negative_strings(self):
        self.assertFalse(booleanize('false'))
        self.assertFalse(booleanize('FALSE'))
        self.assertFalse(booleanize('False'))
        self.assertFalse(booleanize('0'))
        self.assertFalse(booleanize('banana'))
