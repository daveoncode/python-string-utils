from unittest import TestCase

from string_utils import is_ip, is_ip_v6


class IsIpV6TestCase(TestCase):
    def test_compressed_and_ipv4_embedded_addresses(self):
        for address in ('7::128.128.0.127', '::ffff:192.0.2.1',
                        '0:0:0:0:0:ffff:192.0.2.1', '::', '::1',
                        '2001:db8::1', '2001:DB8::'):
            with self.subTest(address=address):
                self.assertTrue(is_ip_v6(address))
                self.assertTrue(is_ip(address))

    def test_invalid_compression_and_embedded_ipv4(self):
        for address in ('1::2::3', '1:2:3:4:5:6:7::8', '::ffff:256.0.2.1',
                        '::ffff:192.0.2', 'gggg:0:0:0:0:0:0:1',
                        ':::::::', '[::1]', '::1/128', 'fe80::1%eth0',
                        ' ::1', '::1 '):
            with self.subTest(address=address):
                self.assertFalse(is_ip_v6(address))
                self.assertFalse(is_ip(address))

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
