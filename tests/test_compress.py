from unittest import TestCase

from string_utils import compress
from string_utils.errors import InvalidInputError


class CompressTestCase(TestCase):
    input_string_with_utf8_chars = ', '.join(
        ['Test æåëýþÿìäçìíó¿æåëëýþÿüïöœäßðèéùúĳøáçìíñ¡ªº£€ {}'.format(i) for i in range(50)]
    )

    def test_compress_raise_exception_if_provided_input_is_not_string(self):
        with self.assertRaises(InvalidInputError) as raised:
            # noinspection PyTypeChecker
            compress(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

    def test_compress_raise_exception_if_provided_encoding_is_not_string(self):
        with self.assertRaises(ValueError) as raised:
            # noinspection PyTypeChecker
            compress('A string to compress', encoding=None)

        self.assertEqual(str(raised.exception), 'Invalid encoding')

    def test_compress_raise_exception_if_provided_level_is_invalid(self):
        expected_msg = 'Invalid compression_level: it must be an "int" between 0 and 9'

        with self.assertRaises(ValueError) as raised:
            # noinspection PyTypeChecker
            compress('A string to compress', compression_level=None)

        self.assertEqual(str(raised.exception), expected_msg)

        with self.assertRaises(ValueError) as raised:
            compress('A string to compress', compression_level=-1)

        self.assertEqual(str(raised.exception), expected_msg)

        with self.assertRaises(ValueError) as raised:
            # noinspection PyTypeChecker
            compress('A string to compress', compression_level=5.5)

        self.assertEqual(str(raised.exception), expected_msg)

        with self.assertRaises(ValueError) as raised:
            compress('A string to compress', compression_level=10)

        self.assertEqual(str(raised.exception), expected_msg)

    def test_compress_raise_exception_if_string_if_empty(self):
        with self.assertRaises(ValueError) as raised:
            compress('')

        self.assertEqual(str(raised.exception), 'Input string cannot be empty')

    def test_compress_returns_compressed_string_if_input_is_valid(self):
        compressed = compress(self.input_string_with_utf8_chars)

        self.assertTrue(isinstance(compressed, str))
        self.assertTrue(len(compressed) < len(self.input_string_with_utf8_chars))
        self.assertFalse(' ' in compressed)
