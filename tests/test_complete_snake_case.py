from unittest import TestCase

from string_utils import is_snake_case, snake_case_to_camel


class CompleteSnakeCaseTestCase(TestCase):
    def test_custom_separators_do_not_accept_only_a_prefix(self):
        for separator in ['.', ':', '+']:
            for suffix in ['!', ' more words', '\n']:
                text = 'hello' + separator + 'world' + suffix
                with self.subTest(separator=separator, suffix=suffix):
                    self.assertFalse(is_snake_case(text, separator=separator))
                    self.assertEqual(snake_case_to_camel(text, separator=separator), text)

    def test_valid_custom_separators_still_convert(self):
        for separator in ['.', ':', '+', '_', '-']:
            text = 'hello' + separator + 'world'
            with self.subTest(separator=separator):
                self.assertTrue(is_snake_case(text, separator=separator))
                self.assertEqual(snake_case_to_camel(text, separator=separator), 'HelloWorld')

    def test_builtin_separators_also_reject_a_trailing_newline(self):
        for text, separator in [('hello_world\n', '_'), ('hello-world\n', '-')]:
            with self.subTest(separator=separator):
                self.assertFalse(is_snake_case(text, separator=separator))
                self.assertEqual(snake_case_to_camel(text, separator=separator), text)
