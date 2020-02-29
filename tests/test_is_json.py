import json
from unittest import TestCase

from string_utils import is_json


class IsJsonTestCase(TestCase):
    def test_non_string_objects_are_properly_handled(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_json({'a': 1}))

        # noinspection PyTypeChecker
        self.assertFalse(is_json(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_json([1, 2, 3]))

        # noinspection PyTypeChecker
        self.assertFalse(is_json(500))

        # noinspection PyTypeChecker
        self.assertFalse(is_json(True))

        # noinspection PyTypeChecker
        self.assertFalse(is_json({1, 2}))

    def test_empty_string_are_invalid(self):
        self.assertFalse(is_json(''))
        self.assertFalse(is_json(' '))

    def test_json_object_can_be_empty(self):
        self.assertTrue(is_json('{}'))

    def test_json_array_can_be_empty(self):
        self.assertTrue(is_json('[]'))

    def test_external_spaces_are_ignored(self):
        self.assertTrue(is_json('{"foo":"bar"}'))
        self.assertTrue(is_json(' { "foo": "bar" } '))
        self.assertTrue(is_json('''
            {
                "foo": "bar"
            }
        '''))
        self.assertTrue(is_json('''
        [
            1, 2, 3
        ]
        '''))

    def test_attributes_quotes_are_mandatory(self):
        self.assertFalse(is_json('{foo: 1}'))

    def test_quotes_should_be_double_quotes(self):
        self.assertFalse(is_json("{'foo': 1}"))
        self.assertFalse(is_json("['boo', 'bar']"))

    def test_string_values_should_be_wrapped_by_double_quotes(self):
        self.assertFalse(is_json('{"foo": hello}'))
        self.assertFalse(is_json('{"foo": \'hello\'}'))
        self.assertTrue(is_json('{"foo": "hello"}'))

    def test_boolean_should_be_lowercase(self):
        self.assertFalse(is_json('{"bool": True}'))
        self.assertFalse(is_json('{"bool": FALSE}'))
        self.assertTrue(is_json('{"bool": true}'))
        self.assertIsInstance(json.loads('{"bool": true}'), dict)
        self.assertTrue(is_json('{"bool": false}'))
        self.assertIsInstance(json.loads('{"bool": false}'), dict)

    def test_null_should_be_lowercase(self):
        self.assertFalse(is_json('{"null": NULL}'))
        self.assertFalse(is_json('{"null": Null}'))
        self.assertTrue(is_json('{"null": null}'))
        self.assertIsInstance(json.loads('{"null": null}'), dict)

    def test_int_number_can_be_any_length(self):
        self.assertTrue(is_json('{"number": 1}'))
        self.assertTrue(is_json('{"number": 99}'))
        self.assertTrue(is_json('{"number": 1000}'))
        self.assertTrue(is_json('{"number": 1234567890}'))

    def test_float_numbers_should_use_dot_as_separator(self):
        self.assertFalse(is_json('{"float": 4,5}'))
        self.assertTrue(is_json('{"float": 4.5}'))
        self.assertIsInstance(json.loads('{"float": 4.5}'), dict)

    def test_negative_numbers_should_be_start_with_minus(self):
        self.assertFalse(is_json('{"number": - 2}'))
        self.assertFalse(is_json('{"number": - 2.5}'))
        self.assertTrue(is_json('{"number": -2}'))
        self.assertTrue(is_json('{"number": -2.5}'))

    def test_array_can_be_empty(self):
        self.assertTrue(is_json('{"array": []}'))
        self.assertTrue(is_json('{"array": [ ]}'))

    def test_object_can_be_empty(self):
        self.assertTrue(is_json('{"obj": {}}'))
        self.assertTrue(is_json('{"obj": { }}'))

    def test_cannot_have_trailing_comma_in_array(self):
        self.assertFalse(is_json('{"numbers": [1,2,3,]}'))

    def test_cannot_have_multiple_comma_in_array(self):
        self.assertFalse(is_json('{"numbers": [1,2,,3]}'))

    def test_cannot_have_trailing_comma_in_object(self):
        self.assertFalse(is_json('{"numbers": {"a": 1, "b": 2,}}'))

    def test_cannot_have_multiple_comma_in_object(self):
        self.assertFalse(is_json('{"numbers": {"a": 1,, "b": 2}}'))

    def test_string_can_contain_escaped_quotes(self):
        s = '{"string": "Look: \\"escaped string here!\\""}'
        self.assertTrue(is_json(s))
        self.assertIsInstance(json.loads(s), dict)

    def test_array_is_json(self):
        self.assertTrue(is_json('[1,2,3]'))
        self.assertTrue(is_json('[]'))
        self.assertTrue(is_json('["foo", "bar"]'))
        self.assertTrue(is_json('[true]'))
        self.assertTrue(is_json('[false]'))
        self.assertTrue(is_json('[{"a": "b"}]'))

    def test_complete_json_case(self):
        string = '''
            {
                "books": [
                    {
                        "title": "Book title 1",
                        "author": "FirstName LastName",
                        "tags": ["tech", "programming", "python"],
                        "available": true,
                        "pageCount": 516,
                        "rating": 4.5,
                        "comments": [
                            {
                                "author": "FirstName LastName",
                                "content": "Nice book!"
                            }
                        ]
                    },
                    {
                        "title": "Book title 2",
                        "author": "FirstName LastName",
                        "tags": ["tech", "programming", "javascript"],
                        "available": true,
                        "rating": 4,
                        "pageCount": 422,
                        "comments": [

                        ]
                    }
                ]
            }
        '''
        self.assertTrue(is_json(string))
        self.assertIsInstance(json.loads(string), dict)
