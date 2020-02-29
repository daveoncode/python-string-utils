from unittest import TestCase

from string_utils import reverse


class ReverseTestCase(TestCase):
    def test_raise_exception_if_object_is_not_a_string(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            reverse(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            reverse(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            reverse(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            reverse([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            reverse({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_returns_original_string_if_unreversible(self):
        self.assertEqual(reverse(''), '')
        self.assertEqual(reverse('x'), 'x')
        self.assertEqual(reverse('!!!'), '!!!')

    def test_returns_reversed_string(self):
        self.assertEqual(reverse('hello world'), 'dlrow olleh')
