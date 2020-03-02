from unittest import TestCase

from string_utils import decompress, compress
from string_utils.errors import InvalidInputError


class DecompressTestCase(TestCase):
    input_string_with_utf8_chars = ', '.join(
        ['Test æåëýþÿìäçìíó¿æåëëýþÿüïöœäßðèéùúĳøáçìíñ¡ªº£€ {}'.format(i) for i in range(50)]
    )

    def test_decompress_raise_exception_if_provided_input_is_not_string(self):
        with self.assertRaises(InvalidInputError) as raised:
            # noinspection PyTypeChecker
            decompress(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

    def test_decompress_raise_exception_if_provided_encoding_is_not_string(self):
        with self.assertRaises(ValueError) as raised:
            # noinspection PyTypeChecker
            decompress('A string to decompress', encoding=None)

        self.assertEqual(str(raised.exception), 'Invalid encoding')

    def test_decompress_returns_original_string(self):
        compressed = compress(self.input_string_with_utf8_chars)
        decompressed = decompress(compressed)

        self.assertNotEqual(self.input_string_with_utf8_chars, compressed)
        self.assertEqual(self.input_string_with_utf8_chars, decompressed)
