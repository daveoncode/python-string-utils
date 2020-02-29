from unittest import TestCase

from string_utils.manipulation import RomanNumbers


class RomanNumberTestCase(TestCase):
    def test_encode_throws_an_exception_if_number_is_less_than_1(self):
        self.assertRaises(ValueError, lambda: RomanNumbers.encode(0))
        self.assertRaises(ValueError, lambda: RomanNumbers.encode(-12))

    def test_encode_throws_an_exception_if_number_is_decimal(self):
        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.encode(1.1))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.encode(-4.3))

    def test_encode_throws_an_exception_if_input_is_not_a_number(self):
        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.encode(None))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.encode(False))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.encode([11]))

    def test_decode_throws_input_error_if_input_is_not_a_string_or_is_empty(self):
        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.decode(None))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.decode(42))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: RomanNumbers.decode(True))

        self.assertRaises(ValueError, lambda: RomanNumbers.decode(''))
        self.assertRaises(ValueError, lambda: RomanNumbers.decode(' '))

    def test_encode_accepts_strings(self):
        self.assertEqual(RomanNumbers.encode('15'), 'XV')
        self.assertEqual(RomanNumbers.encode('9'), 'IX')
        self.assertEqual(RomanNumbers.encode('30'), 'XXX')

    def test_units_are_encoded_as_expected(self):
        self.assertEqual(RomanNumbers.encode(1), 'I')
        self.assertEqual(RomanNumbers.encode(2), 'II')
        self.assertEqual(RomanNumbers.encode(3), 'III')
        self.assertEqual(RomanNumbers.encode(4), 'IV')
        self.assertEqual(RomanNumbers.encode(5), 'V')
        self.assertEqual(RomanNumbers.encode(6), 'VI')
        self.assertEqual(RomanNumbers.encode(7), 'VII')
        self.assertEqual(RomanNumbers.encode(8), 'VIII')
        self.assertEqual(RomanNumbers.encode(9), 'IX')

    def test_units_are_decoded_as_expected(self):
        self.assertEqual(RomanNumbers.decode('I'), 1)
        self.assertEqual(RomanNumbers.decode('II'), 2)
        self.assertEqual(RomanNumbers.decode('III'), 3)
        self.assertEqual(RomanNumbers.decode('IV'), 4)
        self.assertEqual(RomanNumbers.decode('V'), 5)
        self.assertEqual(RomanNumbers.decode('VI'), 6)
        self.assertEqual(RomanNumbers.decode('VII'), 7)
        self.assertEqual(RomanNumbers.decode('VIII'), 8)
        self.assertEqual(RomanNumbers.decode('IX'), 9)

    def test_tens_are_encoded_as_expected(self):
        self.assertEqual(RomanNumbers.encode(10), 'X')
        self.assertEqual(RomanNumbers.encode(20), 'XX')
        self.assertEqual(RomanNumbers.encode(30), 'XXX')
        self.assertEqual(RomanNumbers.encode(40), 'XL')
        self.assertEqual(RomanNumbers.encode(50), 'L')
        self.assertEqual(RomanNumbers.encode(60), 'LX')
        self.assertEqual(RomanNumbers.encode(70), 'LXX')
        self.assertEqual(RomanNumbers.encode(80), 'LXXX')
        self.assertEqual(RomanNumbers.encode(90), 'XC')

    def test_tens_are_decoded_as_expected(self):
        self.assertEqual(RomanNumbers.decode('X'), 10)
        self.assertEqual(RomanNumbers.decode('XX'), 20)
        self.assertEqual(RomanNumbers.decode('XXX'), 30)
        self.assertEqual(RomanNumbers.decode('XL'), 40)
        self.assertEqual(RomanNumbers.decode('L'), 50)
        self.assertEqual(RomanNumbers.decode('LX'), 60)
        self.assertEqual(RomanNumbers.decode('LXX'), 70)
        self.assertEqual(RomanNumbers.decode('LXXX'), 80)
        self.assertEqual(RomanNumbers.decode('XC'), 90)

    def test_tens_and_units_are_encoded_as_expected(self):
        # 1x
        self.assertEqual(RomanNumbers.encode(11), 'XI')
        self.assertEqual(RomanNumbers.encode(12), 'XII')
        self.assertEqual(RomanNumbers.encode(13), 'XIII')
        self.assertEqual(RomanNumbers.encode(14), 'XIV')
        self.assertEqual(RomanNumbers.encode(15), 'XV')
        self.assertEqual(RomanNumbers.encode(16), 'XVI')
        self.assertEqual(RomanNumbers.encode(17), 'XVII')
        self.assertEqual(RomanNumbers.encode(18), 'XVIII')
        self.assertEqual(RomanNumbers.encode(19), 'XIX')

        # 2x
        self.assertEqual(RomanNumbers.encode(21), 'XXI')
        self.assertEqual(RomanNumbers.encode(22), 'XXII')
        self.assertEqual(RomanNumbers.encode(23), 'XXIII')
        self.assertEqual(RomanNumbers.encode(24), 'XXIV')
        self.assertEqual(RomanNumbers.encode(25), 'XXV')
        self.assertEqual(RomanNumbers.encode(26), 'XXVI')
        self.assertEqual(RomanNumbers.encode(27), 'XXVII')
        self.assertEqual(RomanNumbers.encode(28), 'XXVIII')
        self.assertEqual(RomanNumbers.encode(29), 'XXIX')

        # 3x
        self.assertEqual(RomanNumbers.encode(31), 'XXXI')
        self.assertEqual(RomanNumbers.encode(32), 'XXXII')
        self.assertEqual(RomanNumbers.encode(33), 'XXXIII')
        self.assertEqual(RomanNumbers.encode(34), 'XXXIV')
        self.assertEqual(RomanNumbers.encode(35), 'XXXV')
        self.assertEqual(RomanNumbers.encode(36), 'XXXVI')
        self.assertEqual(RomanNumbers.encode(37), 'XXXVII')
        self.assertEqual(RomanNumbers.encode(38), 'XXXVIII')
        self.assertEqual(RomanNumbers.encode(39), 'XXXIX')

        # 4x
        self.assertEqual(RomanNumbers.encode(41), 'XLI')
        self.assertEqual(RomanNumbers.encode(42), 'XLII')
        self.assertEqual(RomanNumbers.encode(43), 'XLIII')
        self.assertEqual(RomanNumbers.encode(44), 'XLIV')
        self.assertEqual(RomanNumbers.encode(45), 'XLV')
        self.assertEqual(RomanNumbers.encode(46), 'XLVI')
        self.assertEqual(RomanNumbers.encode(47), 'XLVII')
        self.assertEqual(RomanNumbers.encode(48), 'XLVIII')
        self.assertEqual(RomanNumbers.encode(49), 'XLIX')

        # 5x
        self.assertEqual(RomanNumbers.encode(51), 'LI')
        self.assertEqual(RomanNumbers.encode(52), 'LII')
        self.assertEqual(RomanNumbers.encode(53), 'LIII')
        self.assertEqual(RomanNumbers.encode(54), 'LIV')
        self.assertEqual(RomanNumbers.encode(55), 'LV')
        self.assertEqual(RomanNumbers.encode(56), 'LVI')
        self.assertEqual(RomanNumbers.encode(57), 'LVII')
        self.assertEqual(RomanNumbers.encode(58), 'LVIII')
        self.assertEqual(RomanNumbers.encode(59), 'LIX')

        # 6x
        self.assertEqual(RomanNumbers.encode(61), 'LXI')
        self.assertEqual(RomanNumbers.encode(62), 'LXII')
        self.assertEqual(RomanNumbers.encode(63), 'LXIII')
        self.assertEqual(RomanNumbers.encode(64), 'LXIV')
        self.assertEqual(RomanNumbers.encode(65), 'LXV')
        self.assertEqual(RomanNumbers.encode(66), 'LXVI')
        self.assertEqual(RomanNumbers.encode(67), 'LXVII')
        self.assertEqual(RomanNumbers.encode(68), 'LXVIII')
        self.assertEqual(RomanNumbers.encode(69), 'LXIX')

        # 7x
        self.assertEqual(RomanNumbers.encode(71), 'LXXI')
        self.assertEqual(RomanNumbers.encode(72), 'LXXII')
        self.assertEqual(RomanNumbers.encode(73), 'LXXIII')
        self.assertEqual(RomanNumbers.encode(74), 'LXXIV')
        self.assertEqual(RomanNumbers.encode(75), 'LXXV')
        self.assertEqual(RomanNumbers.encode(76), 'LXXVI')
        self.assertEqual(RomanNumbers.encode(77), 'LXXVII')
        self.assertEqual(RomanNumbers.encode(78), 'LXXVIII')
        self.assertEqual(RomanNumbers.encode(79), 'LXXIX')

        # 8x
        self.assertEqual(RomanNumbers.encode(81), 'LXXXI')
        self.assertEqual(RomanNumbers.encode(82), 'LXXXII')
        self.assertEqual(RomanNumbers.encode(83), 'LXXXIII')
        self.assertEqual(RomanNumbers.encode(84), 'LXXXIV')
        self.assertEqual(RomanNumbers.encode(85), 'LXXXV')
        self.assertEqual(RomanNumbers.encode(86), 'LXXXVI')
        self.assertEqual(RomanNumbers.encode(87), 'LXXXVII')
        self.assertEqual(RomanNumbers.encode(88), 'LXXXVIII')
        self.assertEqual(RomanNumbers.encode(89), 'LXXXIX')

        # 9x
        self.assertEqual(RomanNumbers.encode(91), 'XCI')
        self.assertEqual(RomanNumbers.encode(92), 'XCII')
        self.assertEqual(RomanNumbers.encode(93), 'XCIII')
        self.assertEqual(RomanNumbers.encode(94), 'XCIV')
        self.assertEqual(RomanNumbers.encode(95), 'XCV')
        self.assertEqual(RomanNumbers.encode(96), 'XCVI')
        self.assertEqual(RomanNumbers.encode(97), 'XCVII')
        self.assertEqual(RomanNumbers.encode(98), 'XCVIII')
        self.assertEqual(RomanNumbers.encode(99), 'XCIX')

    def test_tens_and_units_are_decoded_as_expected(self):
        # 1x
        self.assertEqual(11, RomanNumbers.decode('XI'))
        self.assertEqual(12, RomanNumbers.decode('XII'))
        self.assertEqual(13, RomanNumbers.decode('XIII'))
        self.assertEqual(14, RomanNumbers.decode('XIV'))
        self.assertEqual(15, RomanNumbers.decode('XV'))
        self.assertEqual(16, RomanNumbers.decode('XVI'))
        self.assertEqual(17, RomanNumbers.decode('XVII'))
        self.assertEqual(18, RomanNumbers.decode('XVIII'))
        self.assertEqual(19, RomanNumbers.decode('XIX'))

        # 2x
        self.assertEqual(21, RomanNumbers.decode('XXI'))
        self.assertEqual(22, RomanNumbers.decode('XXII'))
        self.assertEqual(23, RomanNumbers.decode('XXIII'))
        self.assertEqual(24, RomanNumbers.decode('XXIV'))
        self.assertEqual(25, RomanNumbers.decode('XXV'))
        self.assertEqual(26, RomanNumbers.decode('XXVI'))
        self.assertEqual(27, RomanNumbers.decode('XXVII'))
        self.assertEqual(28, RomanNumbers.decode('XXVIII'))
        self.assertEqual(29, RomanNumbers.decode('XXIX'))

        # 3x
        self.assertEqual(31, RomanNumbers.decode('XXXI'))
        self.assertEqual(32, RomanNumbers.decode('XXXII'))
        self.assertEqual(33, RomanNumbers.decode('XXXIII'))
        self.assertEqual(34, RomanNumbers.decode('XXXIV'))
        self.assertEqual(35, RomanNumbers.decode('XXXV'))
        self.assertEqual(36, RomanNumbers.decode('XXXVI'))
        self.assertEqual(37, RomanNumbers.decode('XXXVII'))
        self.assertEqual(38, RomanNumbers.decode('XXXVIII'))
        self.assertEqual(39, RomanNumbers.decode('XXXIX'))

        # 4x
        self.assertEqual(41, RomanNumbers.decode('XLI'))
        self.assertEqual(42, RomanNumbers.decode('XLII'))
        self.assertEqual(43, RomanNumbers.decode('XLIII'))
        self.assertEqual(44, RomanNumbers.decode('XLIV'))
        self.assertEqual(45, RomanNumbers.decode('XLV'))
        self.assertEqual(46, RomanNumbers.decode('XLVI'))
        self.assertEqual(47, RomanNumbers.decode('XLVII'))
        self.assertEqual(48, RomanNumbers.decode('XLVIII'))
        self.assertEqual(49, RomanNumbers.decode('XLIX'))

        # 5x
        self.assertEqual(51, RomanNumbers.decode('LI'))
        self.assertEqual(52, RomanNumbers.decode('LII'))
        self.assertEqual(53, RomanNumbers.decode('LIII'))
        self.assertEqual(54, RomanNumbers.decode('LIV'))
        self.assertEqual(55, RomanNumbers.decode('LV'))
        self.assertEqual(56, RomanNumbers.decode('LVI'))
        self.assertEqual(57, RomanNumbers.decode('LVII'))
        self.assertEqual(58, RomanNumbers.decode('LVIII'))
        self.assertEqual(59, RomanNumbers.decode('LIX'))

        # 6x
        self.assertEqual(61, RomanNumbers.decode('LXI'))
        self.assertEqual(62, RomanNumbers.decode('LXII'))
        self.assertEqual(63, RomanNumbers.decode('LXIII'))
        self.assertEqual(64, RomanNumbers.decode('LXIV'))
        self.assertEqual(65, RomanNumbers.decode('LXV'))
        self.assertEqual(66, RomanNumbers.decode('LXVI'))
        self.assertEqual(67, RomanNumbers.decode('LXVII'))
        self.assertEqual(68, RomanNumbers.decode('LXVIII'))
        self.assertEqual(69, RomanNumbers.decode('LXIX'))

        # 7x
        self.assertEqual(71, RomanNumbers.decode('LXXI'))
        self.assertEqual(72, RomanNumbers.decode('LXXII'))
        self.assertEqual(73, RomanNumbers.decode('LXXIII'))
        self.assertEqual(74, RomanNumbers.decode('LXXIV'))
        self.assertEqual(75, RomanNumbers.decode('LXXV'))
        self.assertEqual(76, RomanNumbers.decode('LXXVI'))
        self.assertEqual(77, RomanNumbers.decode('LXXVII'))
        self.assertEqual(78, RomanNumbers.decode('LXXVIII'))
        self.assertEqual(79, RomanNumbers.decode('LXXIX'))

        # 8x
        self.assertEqual(81, RomanNumbers.decode('LXXXI'))
        self.assertEqual(82, RomanNumbers.decode('LXXXII'))
        self.assertEqual(83, RomanNumbers.decode('LXXXIII'))
        self.assertEqual(84, RomanNumbers.decode('LXXXIV'))
        self.assertEqual(85, RomanNumbers.decode('LXXXV'))
        self.assertEqual(86, RomanNumbers.decode('LXXXVI'))
        self.assertEqual(87, RomanNumbers.decode('LXXXVII'))
        self.assertEqual(88, RomanNumbers.decode('LXXXVIII'))
        self.assertEqual(89, RomanNumbers.decode('LXXXIX'))

        # 9x
        self.assertEqual(91, RomanNumbers.decode('XCI'))
        self.assertEqual(92, RomanNumbers.decode('XCII'))
        self.assertEqual(93, RomanNumbers.decode('XCIII'))
        self.assertEqual(94, RomanNumbers.decode('XCIV'))
        self.assertEqual(95, RomanNumbers.decode('XCV'))
        self.assertEqual(96, RomanNumbers.decode('XCVI'))
        self.assertEqual(97, RomanNumbers.decode('XCVII'))
        self.assertEqual(98, RomanNumbers.decode('XCVIII'))
        self.assertEqual(99, RomanNumbers.decode('XCIX'))

    def test_hundreds_are_encoded_as_expected(self):
        self.assertEqual(RomanNumbers.encode(100), 'C')
        self.assertEqual(RomanNumbers.encode(200), 'CC')
        self.assertEqual(RomanNumbers.encode(300), 'CCC')
        self.assertEqual(RomanNumbers.encode(400), 'CD')
        self.assertEqual(RomanNumbers.encode(500), 'D')
        self.assertEqual(RomanNumbers.encode(600), 'DC')
        self.assertEqual(RomanNumbers.encode(700), 'DCC')
        self.assertEqual(RomanNumbers.encode(800), 'DCCC')
        self.assertEqual(RomanNumbers.encode(900), 'CM')

    def test_hundreds_are_decoded_as_expected(self):
        self.assertEqual(100, RomanNumbers.decode('C'))
        self.assertEqual(200, RomanNumbers.decode('CC'))
        self.assertEqual(300, RomanNumbers.decode('CCC'))
        self.assertEqual(400, RomanNumbers.decode('CD'))
        self.assertEqual(500, RomanNumbers.decode('D'))
        self.assertEqual(600, RomanNumbers.decode('DC'))
        self.assertEqual(700, RomanNumbers.decode('DCC'))
        self.assertEqual(800, RomanNumbers.decode('DCCC'))
        self.assertEqual(900, RomanNumbers.decode('CM'))

    def test_thousands_are_encoded_as_expected(self):
        self.assertEqual(RomanNumbers.encode(1000), 'M')
        self.assertEqual(RomanNumbers.encode(2000), 'MM')
        self.assertEqual(RomanNumbers.encode(3000), 'MMM')

    def test_thousands_are_decoded_as_expected(self):
        self.assertEqual(1000, RomanNumbers.decode('M'))
        self.assertEqual(2000, RomanNumbers.decode('MM'))
        self.assertEqual(3000, RomanNumbers.decode('MMM'))

    def test_combined_numbers_encode(self):
        self.assertEqual(RomanNumbers.encode(3001), 'MMMI')
        self.assertEqual(RomanNumbers.encode(3090), 'MMMXC')
        self.assertEqual(RomanNumbers.encode(1200), 'MCC')
        self.assertEqual(RomanNumbers.encode(2739), 'MMDCCXXXIX')
        self.assertEqual(RomanNumbers.encode(3999), 'MMMCMXCIX')

    def test_combined_numbers_decode(self):
        self.assertEqual(3001, RomanNumbers.decode('MMMI'))
        self.assertEqual(3090, RomanNumbers.decode('MMMXC'))
        self.assertEqual(1200, RomanNumbers.decode('MCC'))
        self.assertEqual(2739, RomanNumbers.decode('MMDCCXXXIX'))
        self.assertEqual(3999, RomanNumbers.decode('MMMCMXCIX'))

    def test_decode_raise_exception_for_unexpected_sign(self):
        with self.assertRaises(ValueError) as raised:
            RomanNumbers.decode('wtf?')

        self.assertEqual(str(raised.exception), 'Invalid token found: "?"')

        with self.assertRaises(ValueError) as raised:
            RomanNumbers.decode('OK')

        self.assertEqual(str(raised.exception), 'Invalid token found: "K"')

        with self.assertRaises(ValueError) as raised:
            RomanNumbers.decode('QMMMCMXCIX')

        self.assertEqual(str(raised.exception), 'Invalid token found: "Q"')

    def test_decode_does_not_care_about_case(self):
        self.assertEqual(3, RomanNumbers.decode('iii'))
        self.assertEqual(30, RomanNumbers.decode('xxx'))
        self.assertEqual(82, RomanNumbers.decode('lxxxii'))
        self.assertEqual(RomanNumbers.decode('VII'), RomanNumbers.decode('vii'))
        self.assertEqual(RomanNumbers.decode('VII'), RomanNumbers.decode('Vii'))
