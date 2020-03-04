from unittest import TestCase

from string_utils import shuffle


class ShuffleTestCase(TestCase):
    original_string = 'Hello World!'

    def test_raise_exception_if_object_is_not_a_string(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            shuffle(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            shuffle(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            shuffle(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            shuffle([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            shuffle({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_shuffled_string_should_be_different_from_original_one(self):
        self.assertNotEqual(self.original_string, shuffle(self.original_string))

    def test_original_string_is_not_modified(self):
        shuffle(self.original_string)
        self.assertEqual(self.original_string, 'Hello World!')

    def test_shuffle_generates_new_string_for_each_call(self):
        self.assertNotEqual(shuffle(self.original_string), shuffle(self.original_string))

    def test_shuffled_string_should_have_same_len_of_original_one(self):
        shuffled = shuffle(self.original_string)
        self.assertTrue(len(self.original_string), len(shuffled))

    def test_sorted_strings_should_match(self):
        shuffled = shuffle(self.original_string)
        self.assertEqual(sorted(self.original_string), sorted(shuffled))
