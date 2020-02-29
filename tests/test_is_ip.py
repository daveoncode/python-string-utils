from unittest import TestCase

from string_utils import is_ip


class IsIpTestCase(TestCase):
    def test_return_false_for_non_string_objects(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_ip(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip(1))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip([]))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip({'a': 1}))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip(True))

    def test_recognize_ip_v4_strings(self):
        self.assertTrue(is_ip('127.0.0.1'))
        self.assertTrue(is_ip('0.0.0.0'))
        self.assertTrue(is_ip('255.255.10.1'))

    def test_returns_false_if_ipv4_out_of_range(self):
        self.assertFalse(is_ip('999.200.100.75'))
        self.assertFalse(is_ip('255.999.100.75'))
        self.assertFalse(is_ip('255.200.999.75'))
        self.assertFalse(is_ip('255.200.100.999'))

    def test_ip_v4_cannot_contain_spaces(self):
        self.assertFalse(is_ip(' 127.0.0.1 '))
        self.assertFalse(is_ip('0.0.0.0 '))
        self.assertFalse(is_ip(' 255.255.10.1'))
        self.assertFalse(is_ip('255. 255.10.1'))

    def test_ip_v4_cannot_have_multiple_dots(self):
        self.assertFalse(is_ip('127.0.0..1'))
        self.assertFalse(is_ip('0..0.0.0'))
        self.assertFalse(is_ip('255.255.10.1.'))

    def test_numbers_cannot_be_divided_by_other_signs_in_ipv4(self):
        self.assertFalse(is_ip('127:0:0:1'))
        self.assertFalse(is_ip('127-0-0-1'))
        self.assertFalse(is_ip('0_0_0_0'))
        self.assertFalse(is_ip('255,255,10,1'))

    def test_ip_cannot_be_blank(self):
        self.assertFalse(is_ip(''))
        self.assertFalse(is_ip(' '))
