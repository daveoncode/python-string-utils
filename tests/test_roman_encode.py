from unittest import TestCase

from string_utils.manipulation import roman_encode


class RomanEncodeTestCase(TestCase):
    def test_encode_throws_an_exception_if_number_is_less_than_1(self):
        self.assertRaises(ValueError, lambda: roman_encode(0))
        self.assertRaises(ValueError, lambda: roman_encode(-12))

    def test_encode_throws_an_exception_if_number_is_decimal(self):
        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_encode(1.1))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_encode(-4.3))

    def test_encode_throws_an_exception_if_input_is_not_a_number(self):
        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_encode(None))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_encode(False))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_encode([11]))

    def test_encode_accepts_strings(self):
        self.assertEqual(roman_encode('15'), 'XV')
        self.assertEqual(roman_encode('9'), 'IX')
        self.assertEqual(roman_encode('30'), 'XXX')

    def test_units_are_encoded_as_expected(self):
        self.assertEqual(roman_encode(1), 'I')
        self.assertEqual(roman_encode(2), 'II')
        self.assertEqual(roman_encode(3), 'III')
        self.assertEqual(roman_encode(4), 'IV')
        self.assertEqual(roman_encode(5), 'V')
        self.assertEqual(roman_encode(6), 'VI')
        self.assertEqual(roman_encode(7), 'VII')
        self.assertEqual(roman_encode(8), 'VIII')
        self.assertEqual(roman_encode(9), 'IX')

    def test_tens_are_encoded_as_expected(self):
        self.assertEqual(roman_encode(10), 'X')
        self.assertEqual(roman_encode(20), 'XX')
        self.assertEqual(roman_encode(30), 'XXX')
        self.assertEqual(roman_encode(40), 'XL')
        self.assertEqual(roman_encode(50), 'L')
        self.assertEqual(roman_encode(60), 'LX')
        self.assertEqual(roman_encode(70), 'LXX')
        self.assertEqual(roman_encode(80), 'LXXX')
        self.assertEqual(roman_encode(90), 'XC')

    def test_tens_and_units_are_encoded_as_expected(self):
        # 1x
        self.assertEqual(roman_encode(11), 'XI')
        self.assertEqual(roman_encode(12), 'XII')
        self.assertEqual(roman_encode(13), 'XIII')
        self.assertEqual(roman_encode(14), 'XIV')
        self.assertEqual(roman_encode(15), 'XV')
        self.assertEqual(roman_encode(16), 'XVI')
        self.assertEqual(roman_encode(17), 'XVII')
        self.assertEqual(roman_encode(18), 'XVIII')
        self.assertEqual(roman_encode(19), 'XIX')

        # 2x
        self.assertEqual(roman_encode(21), 'XXI')
        self.assertEqual(roman_encode(22), 'XXII')
        self.assertEqual(roman_encode(23), 'XXIII')
        self.assertEqual(roman_encode(24), 'XXIV')
        self.assertEqual(roman_encode(25), 'XXV')
        self.assertEqual(roman_encode(26), 'XXVI')
        self.assertEqual(roman_encode(27), 'XXVII')
        self.assertEqual(roman_encode(28), 'XXVIII')
        self.assertEqual(roman_encode(29), 'XXIX')

        # 3x
        self.assertEqual(roman_encode(31), 'XXXI')
        self.assertEqual(roman_encode(32), 'XXXII')
        self.assertEqual(roman_encode(33), 'XXXIII')
        self.assertEqual(roman_encode(34), 'XXXIV')
        self.assertEqual(roman_encode(35), 'XXXV')
        self.assertEqual(roman_encode(36), 'XXXVI')
        self.assertEqual(roman_encode(37), 'XXXVII')
        self.assertEqual(roman_encode(38), 'XXXVIII')
        self.assertEqual(roman_encode(39), 'XXXIX')

        # 4x
        self.assertEqual(roman_encode(41), 'XLI')
        self.assertEqual(roman_encode(42), 'XLII')
        self.assertEqual(roman_encode(43), 'XLIII')
        self.assertEqual(roman_encode(44), 'XLIV')
        self.assertEqual(roman_encode(45), 'XLV')
        self.assertEqual(roman_encode(46), 'XLVI')
        self.assertEqual(roman_encode(47), 'XLVII')
        self.assertEqual(roman_encode(48), 'XLVIII')
        self.assertEqual(roman_encode(49), 'XLIX')

        # 5x
        self.assertEqual(roman_encode(51), 'LI')
        self.assertEqual(roman_encode(52), 'LII')
        self.assertEqual(roman_encode(53), 'LIII')
        self.assertEqual(roman_encode(54), 'LIV')
        self.assertEqual(roman_encode(55), 'LV')
        self.assertEqual(roman_encode(56), 'LVI')
        self.assertEqual(roman_encode(57), 'LVII')
        self.assertEqual(roman_encode(58), 'LVIII')
        self.assertEqual(roman_encode(59), 'LIX')

        # 6x
        self.assertEqual(roman_encode(61), 'LXI')
        self.assertEqual(roman_encode(62), 'LXII')
        self.assertEqual(roman_encode(63), 'LXIII')
        self.assertEqual(roman_encode(64), 'LXIV')
        self.assertEqual(roman_encode(65), 'LXV')
        self.assertEqual(roman_encode(66), 'LXVI')
        self.assertEqual(roman_encode(67), 'LXVII')
        self.assertEqual(roman_encode(68), 'LXVIII')
        self.assertEqual(roman_encode(69), 'LXIX')

        # 7x
        self.assertEqual(roman_encode(71), 'LXXI')
        self.assertEqual(roman_encode(72), 'LXXII')
        self.assertEqual(roman_encode(73), 'LXXIII')
        self.assertEqual(roman_encode(74), 'LXXIV')
        self.assertEqual(roman_encode(75), 'LXXV')
        self.assertEqual(roman_encode(76), 'LXXVI')
        self.assertEqual(roman_encode(77), 'LXXVII')
        self.assertEqual(roman_encode(78), 'LXXVIII')
        self.assertEqual(roman_encode(79), 'LXXIX')

        # 8x
        self.assertEqual(roman_encode(81), 'LXXXI')
        self.assertEqual(roman_encode(82), 'LXXXII')
        self.assertEqual(roman_encode(83), 'LXXXIII')
        self.assertEqual(roman_encode(84), 'LXXXIV')
        self.assertEqual(roman_encode(85), 'LXXXV')
        self.assertEqual(roman_encode(86), 'LXXXVI')
        self.assertEqual(roman_encode(87), 'LXXXVII')
        self.assertEqual(roman_encode(88), 'LXXXVIII')
        self.assertEqual(roman_encode(89), 'LXXXIX')

        # 9x
        self.assertEqual(roman_encode(91), 'XCI')
        self.assertEqual(roman_encode(92), 'XCII')
        self.assertEqual(roman_encode(93), 'XCIII')
        self.assertEqual(roman_encode(94), 'XCIV')
        self.assertEqual(roman_encode(95), 'XCV')
        self.assertEqual(roman_encode(96), 'XCVI')
        self.assertEqual(roman_encode(97), 'XCVII')
        self.assertEqual(roman_encode(98), 'XCVIII')
        self.assertEqual(roman_encode(99), 'XCIX')

    def test_hundreds_are_encoded_as_expected(self):
        self.assertEqual(roman_encode(100), 'C')
        self.assertEqual(roman_encode(200), 'CC')
        self.assertEqual(roman_encode(300), 'CCC')
        self.assertEqual(roman_encode(400), 'CD')
        self.assertEqual(roman_encode(500), 'D')
        self.assertEqual(roman_encode(600), 'DC')
        self.assertEqual(roman_encode(700), 'DCC')
        self.assertEqual(roman_encode(800), 'DCCC')
        self.assertEqual(roman_encode(900), 'CM')

    def test_thousands_are_encoded_as_expected(self):
        self.assertEqual(roman_encode(1000), 'M')
        self.assertEqual(roman_encode(2000), 'MM')
        self.assertEqual(roman_encode(3000), 'MMM')

    def test_combined_numbers_encode(self):
        self.assertEqual(roman_encode(3001), 'MMMI')
        self.assertEqual(roman_encode(3090), 'MMMXC')
        self.assertEqual(roman_encode(1200), 'MCC')
        self.assertEqual(roman_encode(2739), 'MMDCCXXXIX')
        self.assertEqual(roman_encode(3999), 'MMMCMXCIX')
