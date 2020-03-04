from unittest import TestCase

from string_utils import camel_case_to_snake


class CamelCaseToSnakeTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            camel_case_to_snake(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            camel_case_to_snake(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            camel_case_to_snake(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            camel_case_to_snake([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            camel_case_to_snake({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_returns_same_string_if_all_lowercase(self):
        s = 'lower'
        self.assertEqual(camel_case_to_snake(s), s)

    def test_returns_same_string_if_all_uppercase(self):
        s = 'UPPERCASE'
        self.assertEqual(camel_case_to_snake(s), s)

    def test_returns_lowercase_string_for_single_word(self):
        s = 'Hello'
        self.assertEqual(camel_case_to_snake(s), s.lower())

    def test_returns_words_divided_by_underscores_for_each_camel_word(self):
        s = 'CamelCaseStringToTest'
        self.assertEqual(camel_case_to_snake(s), 'camel_case_string_to_test')

    def test_returns_words_divided_by_underscores_for_each_camel_word_even_for_articles(self):
        s = 'ThisIsACamelStringTestB'
        self.assertEqual(camel_case_to_snake(s), 'this_is_a_camel_string_test_b')

    def test_handles_acronyms_gracefully(self):
        s = 'SPAAppsAreVeryPopularOnTheWEBToday'
        self.assertEqual(camel_case_to_snake(s), 'spa_apps_are_very_popular_on_the_web_today')

    def test_should_return_same_string_if_contains_spaces(self):
        s = 'This Is Not A Camel Case String! butThisOneIs'
        self.assertEqual(camel_case_to_snake(s), s)

    def test_should_use_provided_separator(self):
        s = 'CamelCaseString'
        self.assertEqual(camel_case_to_snake(s, '_'), 'camel_case_string')
        self.assertEqual(camel_case_to_snake(s, '||'), 'camel||case||string')
        self.assertEqual(camel_case_to_snake(s, ' '), 'camel case string')
