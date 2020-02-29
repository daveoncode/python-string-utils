from unittest import TestCase

from string_utils import is_ip_v6


class IsIpV6TestCase(TestCase):
    def test_return_false_for_non_string_objects(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_ip_v6(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip_v6(1))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip_v6([]))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip_v6({'a': 1}))

        # noinspection PyTypeChecker
        self.assertFalse(is_ip_v6(True))

    def test_ip_cannot_be_blank(self):
        self.assertFalse(is_ip_v6(''))
        self.assertFalse(is_ip_v6(' '))

    def test_ipv4_is_not_recognized(self):
        self.assertFalse(is_ip_v6('255.100.100.75'))

    def test_returns_false_for_invalid_ip_v6(self):
        self.assertFalse(is_ip_v6('2001.db8:85a3:0000:0000:8a2e:370:7334'))
        self.assertFalse(is_ip_v6('2001:db8|85a3:0000:0000:8a2e:370:1'))
        self.assertFalse(is_ip_v6('123:db8:85a3:0000:0000:8a2e:370,1'))
        self.assertFalse(is_ip_v6('2001:db8:85a3:0:0:8a2e:370'))

    def test_recognizes_valid_ip_v6(self):
        self.assertTrue(is_ip_v6('2001:db8:85a3:0000:0000:8a2e:370:7334'))
        self.assertTrue(is_ip_v6('2001:db8:85a3:0000:0000:8a2e:370:1'))
        self.assertTrue(is_ip_v6('123:db8:85a3:0000:0000:8a2e:370:1'))
        self.assertTrue(is_ip_v6('2001:db8:85a3:0:0:8a2e:370:7334'))
