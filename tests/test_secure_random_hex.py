from unittest import TestCase

from string_utils import secure_random_hex


class SecureRandomHexTestCase(TestCase):
    def test_throws_error_if_size_is_null(self):
        with self.assertRaises(ValueError) as raised:
            # noinspection PyTypeChecker
            secure_random_hex(None)

        self.assertEqual(str(raised.exception), 'byte_count must be >= 1')

    def test_throws_error_if_size_is_less_than_1(self):
        msg = 'byte_count must be >= 1'

        with self.assertRaises(ValueError) as raised:
            secure_random_hex(-12)

        self.assertEqual(str(raised.exception), msg)

        with self.assertRaises(ValueError) as raised:
            secure_random_hex(0)

        self.assertEqual(str(raised.exception), msg)

    def test_returns_random_hex(self):
        sr = secure_random_hex(9)
        self.assertEqual(len(sr), 18)
        self.assertTrue(sr.isalnum())

    def test_returns_different_string_on_each_call(self):
        strings = [secure_random_hex(12) for _ in range(1000)]

        self.assertEqual(len(strings), len(set(strings)))
