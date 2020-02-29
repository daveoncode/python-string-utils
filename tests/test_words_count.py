from unittest import TestCase

from string_utils import words_count


class WordsCountTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            words_count(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            words_count(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            words_count(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            words_count([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            words_count({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_signs_are_not_considered_words(self):
        self.assertEqual(words_count(r'. . ! <> [] {} + % --- _ = @ # ~ | \ / " \''), 0)

    def test_case_doesnt_matter(self):
        self.assertEqual(words_count('hello world'), 2)
        self.assertEqual(words_count('HELLO WORLD'), 2)
        self.assertEqual(words_count('hello WORLD'), 2)

    def test_support_multi_line(self):
        self.assertEqual(words_count('''

            hello

            world

        '''), 2)

    def test_word_with_numbers_is_considered_single_word(self):
        self.assertEqual(words_count('jinja2'), 1)
        self.assertEqual(words_count('Area52'), 1)

    def test_words_divided_by_underscore_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello _world'), 2)
        self.assertEqual(words_count('hello _ world'), 2)
        self.assertEqual(words_count('hello_ world'), 2)
        self.assertEqual(words_count('hello_world'), 2)

    def test_words_divided_by_dash_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello - world'), 2)
        self.assertEqual(words_count('hello -world'), 2)
        self.assertEqual(words_count('hello- world'), 2)
        self.assertEqual(words_count('hello-world'), 2)

    def test_words_divided_by_pipe_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello | world'), 2)
        self.assertEqual(words_count('hello |world'), 2)
        self.assertEqual(words_count('hello| world'), 2)
        self.assertEqual(words_count('hello|world'), 2)

    def test_words_divided_by_plus_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello + world'), 2)
        self.assertEqual(words_count('hello +world'), 2)
        self.assertEqual(words_count('hello+ world'), 2)
        self.assertEqual(words_count('hello+world'), 2)

    def test_words_divided_by_colons_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello : world'), 2)
        self.assertEqual(words_count('hello :world'), 2)
        self.assertEqual(words_count('hello: world'), 2)
        self.assertEqual(words_count('hello:world'), 2)

    def test_words_divided_by_semicolons_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello ; world'), 2)
        self.assertEqual(words_count('hello ;world'), 2)
        self.assertEqual(words_count('hello; world'), 2)
        self.assertEqual(words_count('hello;world'), 2)

    def test_words_divided_by_equal_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello = world'), 2)
        self.assertEqual(words_count('hello =world'), 2)
        self.assertEqual(words_count('hello= world'), 2)
        self.assertEqual(words_count('hello=world'), 2)

    def test_words_divided_by_question_mark_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello ? world'), 2)
        self.assertEqual(words_count('hello ?world'), 2)
        self.assertEqual(words_count('hello? world'), 2)
        self.assertEqual(words_count('hello?world'), 2)

    def test_words_divided_by_exclamation_mark_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello ! world'), 2)
        self.assertEqual(words_count('hello !world'), 2)
        self.assertEqual(words_count('hello! world'), 2)
        self.assertEqual(words_count('hello!world'), 2)

    def test_words_divided_by_apos_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello \' world'), 2)
        self.assertEqual(words_count('hello \'world'), 2)
        self.assertEqual(words_count('hello\' world'), 2)
        self.assertEqual(words_count('hello\'world'), 2)

    def test_words_divided_by_and_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('joseph & joseph'), 2)
        self.assertEqual(words_count('joseph &joseph'), 2)
        self.assertEqual(words_count('joseph& joseph'), 2)
        self.assertEqual(words_count('joseph&joseph'), 2)

    def test_words_divided_by_comma_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello , world'), 2)
        self.assertEqual(words_count('hello ,world'), 2)
        self.assertEqual(words_count('hello, world'), 2)
        self.assertEqual(words_count('hello,world'), 2)

    def test_words_divided_by_dot_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello . world'), 2)
        self.assertEqual(words_count('hello .world'), 2)
        self.assertEqual(words_count('hello. world'), 2)
        self.assertEqual(words_count('hello.world'), 2)

    def test_quoted_text_is_handled_properly(self):
        self.assertEqual(words_count('this text "is quoted"'), 4)
        self.assertEqual(words_count('this text"is quoted"'), 4)

    def test_parenthesis_are_properly_handled(self):
        self.assertEqual(words_count('Does it work? (just a test)'), 6)
        self.assertEqual(words_count('Does it work?(just a test)'), 6)
        self.assertEqual(words_count('Does it work? (just a test)I hope'), 8)

    def test_return_expected_count(self):
        self.assertEqual(words_count('hello'), 1)
        self.assertEqual(words_count('hello world'), 2)
        self.assertEqual(words_count('a couple of words and the number 1'), 8)
        self.assertEqual(words_count('Testing (this)'), 2)
        self.assertEqual(words_count('''
            this is my list:

            - (1) one
            - (2) two
            - (3) three

        '''), 10)

    def test_should_count_non_ascii_words(self):
        self.assertEqual(words_count('é vero o é falso?'), 5)
