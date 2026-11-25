from unicodedata import normalize
from unittest import TestCase

from string_utils import slugify


class SlugifyNormalizationTestCase(TestCase):
    def test_canonically_equivalent_names_have_the_same_slug(self):
        for text, expected in [
            ('M\u00f6nst\u00e9r M\u00e4gn\u00ebt', 'monster-magnet'),
            ('Jalape\u00f1o peppers', 'jalapeno-peppers'),
            ('\u00c5land islands', 'aland-islands'),
        ]:
            with self.subTest(text=text):
                self.assertEqual(slugify(text), expected)
                self.assertEqual(slugify(normalize('NFD', text)), expected)

    def test_decomposed_text_keeps_the_selected_separator(self):
        text = normalize('NFD', 'M\u00f6nst\u00e9r M\u00e4gn\u00ebt')
        self.assertEqual(slugify(text, separator='_'), 'monster_magnet')
