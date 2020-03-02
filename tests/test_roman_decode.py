from unittest import TestCase

from string_utils.manipulation import roman_decode


class RomanDecodeTestCase(TestCase):
    def test_decode_throws_input_error_if_input_is_not_a_string_or_is_empty(self):
        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_decode(None))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_decode(42))

        # noinspection PyTypeChecker
        self.assertRaises(ValueError, lambda: roman_decode(True))

        self.assertRaises(ValueError, lambda: roman_decode(''))
        self.assertRaises(ValueError, lambda: roman_decode(' '))

    def test_units_are_decoded_as_expected(self):
        self.assertEqual(roman_decode('I'), 1)
        self.assertEqual(roman_decode('II'), 2)
        self.assertEqual(roman_decode('III'), 3)
        self.assertEqual(roman_decode('IV'), 4)
        self.assertEqual(roman_decode('V'), 5)
        self.assertEqual(roman_decode('VI'), 6)
        self.assertEqual(roman_decode('VII'), 7)
        self.assertEqual(roman_decode('VIII'), 8)
        self.assertEqual(roman_decode('IX'), 9)

    def test_tens_are_decoded_as_expected(self):
        self.assertEqual(roman_decode('X'), 10)
        self.assertEqual(roman_decode('XX'), 20)
        self.assertEqual(roman_decode('XXX'), 30)
        self.assertEqual(roman_decode('XL'), 40)
        self.assertEqual(roman_decode('L'), 50)
        self.assertEqual(roman_decode('LX'), 60)
        self.assertEqual(roman_decode('LXX'), 70)
        self.assertEqual(roman_decode('LXXX'), 80)
        self.assertEqual(roman_decode('XC'), 90)

    def test_tens_and_units_are_decoded_as_expected(self):
        # 1x
        self.assertEqual(11, roman_decode('XI'))
        self.assertEqual(12, roman_decode('XII'))
        self.assertEqual(13, roman_decode('XIII'))
        self.assertEqual(14, roman_decode('XIV'))
        self.assertEqual(15, roman_decode('XV'))
        self.assertEqual(16, roman_decode('XVI'))
        self.assertEqual(17, roman_decode('XVII'))
        self.assertEqual(18, roman_decode('XVIII'))
        self.assertEqual(19, roman_decode('XIX'))

        # 2x
        self.assertEqual(21, roman_decode('XXI'))
        self.assertEqual(22, roman_decode('XXII'))
        self.assertEqual(23, roman_decode('XXIII'))
        self.assertEqual(24, roman_decode('XXIV'))
        self.assertEqual(25, roman_decode('XXV'))
        self.assertEqual(26, roman_decode('XXVI'))
        self.assertEqual(27, roman_decode('XXVII'))
        self.assertEqual(28, roman_decode('XXVIII'))
        self.assertEqual(29, roman_decode('XXIX'))

        # 3x
        self.assertEqual(31, roman_decode('XXXI'))
        self.assertEqual(32, roman_decode('XXXII'))
        self.assertEqual(33, roman_decode('XXXIII'))
        self.assertEqual(34, roman_decode('XXXIV'))
        self.assertEqual(35, roman_decode('XXXV'))
        self.assertEqual(36, roman_decode('XXXVI'))
        self.assertEqual(37, roman_decode('XXXVII'))
        self.assertEqual(38, roman_decode('XXXVIII'))
        self.assertEqual(39, roman_decode('XXXIX'))

        # 4x
        self.assertEqual(41, roman_decode('XLI'))
        self.assertEqual(42, roman_decode('XLII'))
        self.assertEqual(43, roman_decode('XLIII'))
        self.assertEqual(44, roman_decode('XLIV'))
        self.assertEqual(45, roman_decode('XLV'))
        self.assertEqual(46, roman_decode('XLVI'))
        self.assertEqual(47, roman_decode('XLVII'))
        self.assertEqual(48, roman_decode('XLVIII'))
        self.assertEqual(49, roman_decode('XLIX'))

        # 5x
        self.assertEqual(51, roman_decode('LI'))
        self.assertEqual(52, roman_decode('LII'))
        self.assertEqual(53, roman_decode('LIII'))
        self.assertEqual(54, roman_decode('LIV'))
        self.assertEqual(55, roman_decode('LV'))
        self.assertEqual(56, roman_decode('LVI'))
        self.assertEqual(57, roman_decode('LVII'))
        self.assertEqual(58, roman_decode('LVIII'))
        self.assertEqual(59, roman_decode('LIX'))

        # 6x
        self.assertEqual(61, roman_decode('LXI'))
        self.assertEqual(62, roman_decode('LXII'))
        self.assertEqual(63, roman_decode('LXIII'))
        self.assertEqual(64, roman_decode('LXIV'))
        self.assertEqual(65, roman_decode('LXV'))
        self.assertEqual(66, roman_decode('LXVI'))
        self.assertEqual(67, roman_decode('LXVII'))
        self.assertEqual(68, roman_decode('LXVIII'))
        self.assertEqual(69, roman_decode('LXIX'))

        # 7x
        self.assertEqual(71, roman_decode('LXXI'))
        self.assertEqual(72, roman_decode('LXXII'))
        self.assertEqual(73, roman_decode('LXXIII'))
        self.assertEqual(74, roman_decode('LXXIV'))
        self.assertEqual(75, roman_decode('LXXV'))
        self.assertEqual(76, roman_decode('LXXVI'))
        self.assertEqual(77, roman_decode('LXXVII'))
        self.assertEqual(78, roman_decode('LXXVIII'))
        self.assertEqual(79, roman_decode('LXXIX'))

        # 8x
        self.assertEqual(81, roman_decode('LXXXI'))
        self.assertEqual(82, roman_decode('LXXXII'))
        self.assertEqual(83, roman_decode('LXXXIII'))
        self.assertEqual(84, roman_decode('LXXXIV'))
        self.assertEqual(85, roman_decode('LXXXV'))
        self.assertEqual(86, roman_decode('LXXXVI'))
        self.assertEqual(87, roman_decode('LXXXVII'))
        self.assertEqual(88, roman_decode('LXXXVIII'))
        self.assertEqual(89, roman_decode('LXXXIX'))

        # 9x
        self.assertEqual(91, roman_decode('XCI'))
        self.assertEqual(92, roman_decode('XCII'))
        self.assertEqual(93, roman_decode('XCIII'))
        self.assertEqual(94, roman_decode('XCIV'))
        self.assertEqual(95, roman_decode('XCV'))
        self.assertEqual(96, roman_decode('XCVI'))
        self.assertEqual(97, roman_decode('XCVII'))
        self.assertEqual(98, roman_decode('XCVIII'))
        self.assertEqual(99, roman_decode('XCIX'))

    def test_hundreds_are_decoded_as_expected(self):
        self.assertEqual(100, roman_decode('C'))
        self.assertEqual(200, roman_decode('CC'))
        self.assertEqual(300, roman_decode('CCC'))
        self.assertEqual(400, roman_decode('CD'))
        self.assertEqual(500, roman_decode('D'))
        self.assertEqual(600, roman_decode('DC'))
        self.assertEqual(700, roman_decode('DCC'))
        self.assertEqual(800, roman_decode('DCCC'))
        self.assertEqual(900, roman_decode('CM'))

    def test_thousands_are_decoded_as_expected(self):
        self.assertEqual(1000, roman_decode('M'))
        self.assertEqual(2000, roman_decode('MM'))
        self.assertEqual(3000, roman_decode('MMM'))

    def test_combined_numbers_decode(self):
        self.assertEqual(3001, roman_decode('MMMI'))
        self.assertEqual(3090, roman_decode('MMMXC'))
        self.assertEqual(1200, roman_decode('MCC'))
        self.assertEqual(2739, roman_decode('MMDCCXXXIX'))
        self.assertEqual(3999, roman_decode('MMMCMXCIX'))

    def test_decode_raise_exception_for_unexpected_sign(self):
        with self.assertRaises(ValueError) as raised:
            roman_decode('wtf?')

        self.assertEqual(str(raised.exception), 'Invalid token found: "?"')

        with self.assertRaises(ValueError) as raised:
            roman_decode('OK')

        self.assertEqual(str(raised.exception), 'Invalid token found: "K"')

        with self.assertRaises(ValueError) as raised:
            roman_decode('QMMMCMXCIX')

        self.assertEqual(str(raised.exception), 'Invalid token found: "Q"')

    def test_decode_does_not_care_about_case(self):
        self.assertEqual(3, roman_decode('iii'))
        self.assertEqual(30, roman_decode('xxx'))
        self.assertEqual(82, roman_decode('lxxxii'))
        self.assertEqual(roman_decode('VII'), roman_decode('vii'))
        self.assertEqual(roman_decode('VII'), roman_decode('Vii'))
