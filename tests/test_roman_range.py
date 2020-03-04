from unittest import TestCase

from string_utils.generation import roman_range


class RomanRangeTestCase(TestCase):
    def test_range_raise_exception_if_stop_is_invalid(self):
        msg = '"stop" must be an integer in the range 1-3999'

        with self.assertRaises(ValueError) as raised:
            roman_range(0)

        self.assertEqual(str(raised.exception), msg)

        with self.assertRaises(ValueError) as raised:
            # noinspection PyTypeChecker
            roman_range(9.9)

        self.assertEqual(str(raised.exception), msg)

        with self.assertRaises(ValueError) as raised:
            roman_range(4000)

        self.assertEqual(str(raised.exception), msg)

        with self.assertRaises(ValueError) as raised:
            roman_range(-4000)

        self.assertEqual(str(raised.exception), msg)

    def test_range_returns_expected_generator_for_count_call(self):
        generator = roman_range(10)

        self.assertEqual(generator.__next__(), 'I')
        self.assertEqual(generator.__next__(), 'II')
        self.assertEqual(generator.__next__(), 'III')
        self.assertEqual(generator.__next__(), 'IV')
        self.assertEqual(generator.__next__(), 'V')
        self.assertEqual(generator.__next__(), 'VI')
        self.assertEqual(generator.__next__(), 'VII')
        self.assertEqual(generator.__next__(), 'VIII')
        self.assertEqual(generator.__next__(), 'IX')
        self.assertEqual(generator.__next__(), 'X')

        # generator has been consumed, so another call will raise an exception
        self.assertRaises(StopIteration, generator.__next__)

    def test_range_returns_expected_generator_for_start_stop_call_forward(self):
        generator = roman_range(start=10, stop=18)

        self.assertEqual(generator.__next__(), 'X')
        self.assertEqual(generator.__next__(), 'XI')
        self.assertEqual(generator.__next__(), 'XII')
        self.assertEqual(generator.__next__(), 'XIII')
        self.assertEqual(generator.__next__(), 'XIV')
        self.assertEqual(generator.__next__(), 'XV')
        self.assertEqual(generator.__next__(), 'XVI')
        self.assertEqual(generator.__next__(), 'XVII')
        self.assertEqual(generator.__next__(), 'XVIII')

        # generator has been consumed, so another call will raise an exception
        self.assertRaises(StopIteration, generator.__next__)

    def test_range_returns_expected_generator_for_start_stop_call_backward(self):
        generator = roman_range(start=10, stop=1, step=-1)

        self.assertEqual(generator.__next__(), 'X')
        self.assertEqual(generator.__next__(), 'IX')
        self.assertEqual(generator.__next__(), 'VIII')
        self.assertEqual(generator.__next__(), 'VII')
        self.assertEqual(generator.__next__(), 'VI')
        self.assertEqual(generator.__next__(), 'V')
        self.assertEqual(generator.__next__(), 'IV')
        self.assertEqual(generator.__next__(), 'III')
        self.assertEqual(generator.__next__(), 'II')
        self.assertEqual(generator.__next__(), 'I')

        # generator has been consumed, so another call will raise an exception
        self.assertRaises(StopIteration, generator.__next__)

    def test_range_returns_expected_generator_for_start_stop_step_call(self):
        generator = roman_range(start=10, stop=30, step=5)

        self.assertEqual(generator.__next__(), 'X')
        self.assertEqual(generator.__next__(), 'XV')
        self.assertEqual(generator.__next__(), 'XX')
        self.assertEqual(generator.__next__(), 'XXV')
        self.assertEqual(generator.__next__(), 'XXX')

        # generator has been consumed, so another call will raise an exception
        self.assertRaises(StopIteration, generator.__next__)

    def test_start_param_cannot_be_less_than_1(self):
        self.assertRaises(ValueError, lambda: roman_range(start=0, stop=10))
        self.assertRaises(ValueError, lambda: roman_range(start=-1, stop=10))
        self.assertRaises(ValueError, lambda: roman_range(start=-55, stop=10))

    def test_stop_param_cannot_be_less_than_1(self):
        self.assertRaises(ValueError, lambda: roman_range(start=1, stop=0))
        self.assertRaises(ValueError, lambda: roman_range(start=1, stop=-99, step=-1))

    def test_stop_param_cannot_be_greater_than_3999(self):
        self.assertRaises(ValueError, lambda: roman_range(start=1, stop=4000))
        self.assertRaises(ValueError, lambda: roman_range(start=1, stop=10000))

    def test_start_stop_step_config_cannot_exceed_bounds(self):
        # start (3995) + step (10) will exceed stop (3999)
        self.assertRaises(OverflowError, lambda: roman_range(start=3995, stop=3999, step=10))

        # start (10) + step (200) will exceed stop (100)
        self.assertRaises(OverflowError, lambda: roman_range(start=10, stop=100, step=200))

        # step should be -1 in order to go from 100 to 1
        self.assertRaises(OverflowError, lambda: roman_range(start=100, stop=1, step=1))

        # start (10) + step (-6) will exceed stop (5)
        self.assertRaises(OverflowError, lambda: roman_range(start=10, stop=5, step=-6))
