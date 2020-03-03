from unittest import TestCase

from string_utils import is_string


class IsStringTestCase(TestCase):
    def test_return_false_for_non_string_objects(self):
        self.assertFalse(is_string(None))
        self.assertFalse(is_string(False))
        self.assertFalse(is_string(0))
        self.assertFalse(is_string([]))
        self.assertFalse(is_string({'a': 1}))

    def test_bytes_sequence_is_ont_considered_string(self):
        self.assertFalse(is_string(b'nope!'))

    def test_return_true_for_string_objects(self):
        self.assertTrue(is_string(''))
        self.assertTrue(is_string('hello world'))
        self.assertTrue(is_string(r'[a-z]'))
