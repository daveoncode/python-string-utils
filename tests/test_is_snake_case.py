from unittest import TestCase

from string_utils import is_snake_case


class IsSnakeCaseTestCase(TestCase):
    def test_return_false_for_non_string_objects(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_snake_case(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_snake_case(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_snake_case(0))

        # noinspection PyTypeChecker
        self.assertFalse(is_snake_case([]))

        # noinspection PyTypeChecker
        self.assertFalse(is_snake_case({'a': 1}))

    def test_string_cannot_be_blank(self):
        self.assertFalse(is_snake_case(''))
        self.assertFalse(is_snake_case(' '))

    def test_string_cannot_be_lowercase_letters_only(self):
        self.assertFalse(is_snake_case('lowercaseonly'))

    def test_string_cannot_be_camel_case(self):
        self.assertFalse(is_snake_case('Banana'))

    def test_string_cannot_be_all_uppercase(self):
        self.assertFalse(is_snake_case('HELLO'))

    def test_string_cannot_contain_only_underscores(self):
        self.assertFalse(is_snake_case('_'))
        self.assertFalse(is_snake_case('__'))
        self.assertFalse(is_snake_case('___'))
        self.assertFalse(is_snake_case('____________________'))

    def test_string_cannot_contain_bad_signs(self):
        self.assertFalse(is_snake_case('1_no_snake'))
        self.assertFalse(is_snake_case('^_no_snake'))
        self.assertFalse(is_snake_case('@_no_snake'))
        self.assertFalse(is_snake_case('%_no_snake'))
        self.assertFalse(is_snake_case('no_snake#'))
        self.assertFalse(is_snake_case('no_!'))
        self.assertFalse(is_snake_case('!no_'))
        self.assertFalse(is_snake_case('.no_'))

    def test_should_accept_valid_snake_strings(self):
        self.assertTrue(is_snake_case('HELLO_WORLD'))
        self.assertTrue(is_snake_case('Hello_World'))
        self.assertTrue(is_snake_case('_hello_world'))
        self.assertTrue(is_snake_case('hello_world_'))
        self.assertTrue(is_snake_case('hello_world'))
        self.assertTrue(is_snake_case('_hello_'))
        self.assertTrue(is_snake_case('_hello__'))
        self.assertTrue(is_snake_case('__hello_'))
        self.assertTrue(is_snake_case('a_'))
        self.assertTrue(is_snake_case('_b'))
        self.assertTrue(is_snake_case('a_b_c_d_e'))
        self.assertTrue(is_snake_case('snake_case_string'))
        self.assertTrue(is_snake_case('snake_2'))
        self.assertTrue(is_snake_case('a_snake_string_4_you'))

    def test_should_consider_custom_separator(self):
        s = 'snake-string-with-dashes'
        self.assertFalse(is_snake_case(s))
        self.assertTrue(is_snake_case(s, separator='-'))
