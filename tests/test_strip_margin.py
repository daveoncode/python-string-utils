from unittest import TestCase

from string_utils import strip_margin


class StripMarginTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_margin(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_margin(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_margin(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_margin([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_margin({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_string_is_not_modified_if_there_is_nothing_to_strip(self):
        self.assertEqual(strip_margin(''), '')
        self.assertEqual(strip_margin('abc'), 'abc')
        self.assertEqual(strip_margin('this will not change'), 'this will not change')
        self.assertEqual(strip_margin('this will not change neither '), 'this will not change neither ')

    def test_margins_are_stripped(self):
        # DO NOT REFORMAT THIS BLOCK (IT MUST STAY AS IS FOR THE TEST!)
        expected_string = '''
1. this is a string to strip

2. this is a string to strip

3. this is a string to strip

4. this is a string to strip

'''

        self.assertEqual(
            strip_margin(
                '''
                1. this is a string to strip
                
                2. this is a string to strip
                
                3. this is a string to strip
                
                4. this is a string to strip
                
                '''
            ),
            expected_string
        )
