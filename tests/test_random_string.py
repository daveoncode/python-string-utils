from unittest import TestCase

from string_utils.generation import random_string


class RandomStringTestCase(TestCase):
    def test_throws_error_if_size_is_null(self):
        with self.assertRaises(ValueError) as raised:
            # noinspection PyTypeChecker
            random_string(None)

        self.assertEqual(str(raised.exception), 'size must be >= 1')

    def test_throws_error_if_size_is_less_than_1(self):
        msg = 'size must be >= 1'

        with self.assertRaises(ValueError) as raised:
            random_string(-12)

        self.assertEqual(str(raised.exception), msg)

        with self.assertRaises(ValueError) as raised:
            random_string(0)

        self.assertEqual(str(raised.exception), msg)

    def test_returns_string_of_the_desired_size(self):
        rs1 = random_string(2)
        self.assertEqual(len(rs1), 2)
        self.assertTrue(rs1.isalnum())

        rs2 = random_string(9)
        self.assertEqual(len(rs2), 9)
        self.assertTrue(rs2.isalnum())

        rs3 = random_string(36)
        self.assertEqual(len(rs3), 36)
        self.assertTrue(rs3.isalnum())

    def test_returns_different_string_at_each_call(self):
        count = 1000
        strings = [random_string(9) for _ in range(count)]

        self.assertEqual(len(strings), count)
        self.assertEqual(len(set(strings)), count)
