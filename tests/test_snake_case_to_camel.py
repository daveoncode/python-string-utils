from unittest import TestCase

from string_utils import snake_case_to_camel


class SnakeCaseToCamelTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            snake_case_to_camel(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            snake_case_to_camel(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            snake_case_to_camel(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            snake_case_to_camel([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            snake_case_to_camel({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_returns_original_string_if_not_snake_case(self):
        self.assertEqual(snake_case_to_camel(''), '')
        self.assertEqual(snake_case_to_camel('foo'), 'foo')
        self.assertEqual(snake_case_to_camel('foo bar baz'), 'foo bar baz')
        self.assertEqual(snake_case_to_camel('not_snake_!'), 'not_snake_!')
        self.assertEqual(snake_case_to_camel('(not_snake)'), '(not_snake)')
        self.assertEqual(snake_case_to_camel('123not_snake'), '123not_snake')

    def test_returns_camel_case_from_correct_snake_case(self):
        self.assertEqual(snake_case_to_camel('hello_world'), 'HelloWorld')
        self.assertEqual(snake_case_to_camel('the_snake_is_green'), 'TheSnakeIsGreen')
        self.assertEqual(snake_case_to_camel('the_number_of_the_beast_is_666'), 'TheNumberOfTheBeastIs666')
        self.assertEqual(snake_case_to_camel('a_b_c_d'), 'ABCD')
        self.assertEqual(snake_case_to_camel('_one'), 'One')
        self.assertEqual(snake_case_to_camel('__one'), 'One')
        self.assertEqual(snake_case_to_camel('one_'), 'One')
        self.assertEqual(snake_case_to_camel('_one_'), 'One')

    def test_should_consider_custom_separator(self):
        s = 'snake-case-using-dashes'
        self.assertEqual(snake_case_to_camel(s), s)
        self.assertEqual(snake_case_to_camel(s, separator='-'), 'SnakeCaseUsingDashes')

    def test_should_not_capitalize_first_letter_if_specified(self):
        self.assertEqual(snake_case_to_camel('this_will_starts_lower_case', False), 'thisWillStartsLowerCase')
        self.assertEqual(snake_case_to_camel('hello_world', False), 'helloWorld')
        self.assertEqual(snake_case_to_camel('the_snake_is_green', False), 'theSnakeIsGreen')
        self.assertEqual(snake_case_to_camel('the_number_of_the_beast_is_666', False), 'theNumberOfTheBeastIs666')
        self.assertEqual(snake_case_to_camel('a_b_c_d', False), 'aBCD')
        self.assertEqual(snake_case_to_camel('_one', False), 'one')
        self.assertEqual(snake_case_to_camel('__one', False), 'one')
        self.assertEqual(snake_case_to_camel('one_', False), 'one')
        self.assertEqual(snake_case_to_camel('_one_', False), 'one')
