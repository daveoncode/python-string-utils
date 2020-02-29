from unittest import TestCase

from string_utils import is_email


class IsEmailTestCase(TestCase):
    def test_should_return_false_for_non_string_objects(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_email(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_email(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_email(0))

        # noinspection PyTypeChecker
        self.assertFalse(is_email([]))

        # noinspection PyTypeChecker
        self.assertFalse(is_email({'a': 1}))

    def test_string_cannot_be_empty(self):
        self.assertFalse(is_email(''))
        self.assertFalse(is_email(' '))

    def test_domain_part_is_required(self):
        self.assertFalse(is_email('name@'))

    def test_name_part_is_required(self):
        self.assertFalse(is_email('@foo.com'))

    def test_at_sign_is_required(self):
        self.assertFalse(is_email('name.site.com'))

    def test_domain_extension_is_required(self):
        self.assertFalse(is_email('name@site'))
        self.assertFalse(is_email('name@site.'))

    def test_domain_extension_should_be_letters_only_from_2_to_4_chars(self):
        self.assertFalse(is_email('me@foo.123'))
        self.assertFalse(is_email('me@foo.c'))
        self.assertFalse(is_email('me@foo.!!'))
        self.assertFalse(is_email('me@foo.___'))
        self.assertFalse(is_email('me@foo.toolongext'))

    def test_name_part_cannot_contain_bad_signs(self):
        self.assertFalse(is_email('#me#@foo.com'))
        self.assertFalse(is_email('me!@foo.com'))
        self.assertFalse(is_email('[][]@foo.com'))
        self.assertFalse(is_email('john%@john5music.net'))

    def test_domain_part_cannot_contain_bad_signs(self):
        self.assertFalse(is_email('me@#foo#.com'))
        self.assertFalse(is_email('me@foo!.com'))
        self.assertFalse(is_email('someone@[foo].com'))

    def test_domain_part_cannot_be_uppercase(self):
        self.assertFalse(is_email('someone@SOMESITE.COM'))

    def test_domain_part_cannot_contain_dots_sequence(self):
        self.assertFalse(is_email('name@em..ail.net'))
        self.assertFalse(is_email('name@email..net'))

    def test_domain_cannot_be_single_char(self):
        self.assertFalse(is_email('name@d.com'))

    def test_should_accept_valid_emails(self):
        self.assertTrue(is_email('me@foo.com'))
        self.assertTrue(is_email('name@gmail.com'))
        self.assertTrue(is_email('name2@gmail.com'))
        self.assertTrue(is_email('PeterParker@gmail.com'))
        self.assertTrue(is_email('first_name.last_name@yahoo.it'))
        self.assertTrue(is_email('foo@domamin.subdomain.com'))
        self.assertTrue(is_email('is1email@domain.org'))
        self.assertTrue(is_email('UPPER_CASE_EMAIL@somesite.com'))
