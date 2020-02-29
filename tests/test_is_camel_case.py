from unittest import TestCase

from string_utils import is_camel_case


class IsCamelCaseTestCase(TestCase):
    def test_should_return_false_for_non_string_objects(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_camel_case(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_camel_case(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_camel_case(0))

        # noinspection PyTypeChecker
        self.assertFalse(is_camel_case([]))

        # noinspection PyTypeChecker
        self.assertFalse(is_camel_case({'a': 1}))

    def test_string_cannot_be_empty(self):
        self.assertFalse(is_camel_case(''))
        self.assertFalse(is_camel_case(' '))

    def test_string_cannot_be_all_lowercase(self):
        self.assertFalse(is_camel_case('lowercase'))

    def test_string_cannot_be_all_uppercase(self):
        self.assertFalse(is_camel_case('UPPERCASE'))

    def test_string_cannot_contain_spaces(self):
        self.assertFalse(is_camel_case(' CamelCase '))

    def test_string_cannot_start_with_number(self):
        self.assertFalse(is_camel_case('1000Times'))

    def test_string_cannot_contain_invalid_chars(self):
        self.assertFalse(is_camel_case('<#NotCamelCaseHere!?>'))

    def test_should_accept_valid_camel_case_string(self):
        self.assertTrue(is_camel_case('Camel'))
        self.assertTrue(is_camel_case('CamelCase'))
        self.assertTrue(is_camel_case('camelCase'))
        self.assertTrue(is_camel_case('CamelCaseTOO'))
        self.assertTrue(is_camel_case('ACamelCaseIsAlsoAStringLikeThis1'))
        self.assertTrue(is_camel_case('camelCaseStartingLowerEndingUPPER'))
