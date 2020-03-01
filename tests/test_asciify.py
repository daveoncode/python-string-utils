from unittest import TestCase

from string_utils.errors import InvalidInputError
from string_utils.manipulation import asciify


class AsciifyTestCase(TestCase):
    def test_raise_exception_if_not_string(self):
        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: asciify(None))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: asciify(1))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: asciify(True))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: asciify(['nope']))

    def test_returns_same_string_if_ascii(self):
        self.assertEqual(asciify(''), '')
        self.assertEqual(asciify(' '), ' ')
        self.assertEqual(asciify('Hello World!'), 'Hello World!')
        self.assertEqual(asciify('-12.99'), '-12.99')
        self.assertEqual(asciify('<foo></foo>'), '<foo></foo>')

    def test_returns_asciified_string(self):
        self.assertEqual('eeuuooaaeynAAACIINOE', asciify('èéùúòóäåëýñÅÀÁÇÌÍÑÓË'))
