from unittest import TestCase

from string_utils import is_slug


class IsSlugTestCase(TestCase):
    def test_non_string_objects_return_false(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_slug(1))

        # noinspection PyTypeChecker
        self.assertFalse(is_slug(['xx']))

        # noinspection PyTypeChecker
        self.assertFalse(is_slug({}))

        # noinspection PyTypeChecker
        self.assertFalse(is_slug(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_slug((1, 2, 3)))

        # noinspection PyTypeChecker
        self.assertFalse(is_slug(object()))

    def test_recognizes_slugs(self):
        self.assertTrue(is_slug('yep-i-am-a-slug'))
        self.assertTrue(is_slug('yep-i-am-a-slug', '-'))
        self.assertTrue(is_slug('yep.i.am.a.slug', '.'))
        self.assertTrue(is_slug('yep_i_am_a_slug', '_'))

    def test_slug_can_have_multiple_consecutive_separator_signs(self):
        self.assertTrue(is_slug('oh-----yeah'))
        self.assertTrue(is_slug('oh_____yeah', '_'))
        self.assertTrue(is_slug('1----2'))

    def test_slug_cannot_contain_spaces(self):
        self.assertFalse(is_slug('not - a - slug'))
        self.assertFalse(is_slug('not- a - slug'))
        self.assertFalse(is_slug('not- a- slug'))
        self.assertFalse(is_slug('not-a- slug'))
        self.assertFalse(is_slug('not-a-slug '))
        self.assertFalse(is_slug(' not-a-slug'))

    def test_slug_cannot_contain_non_ascii_chars(self):
        self.assertFalse(is_slug('foò-bär'))

    def test_slug_cannot_contain_punctuation(self):
        self.assertFalse(is_slug('foo.-bar'))
        self.assertFalse(is_slug('foo-bar.'))
        self.assertFalse(is_slug('foo-bar,'))
        self.assertFalse(is_slug('!foo-bar'))
        self.assertFalse(is_slug('foo-bar?'))
        self.assertFalse(is_slug('foo-bar:'))
        self.assertFalse(is_slug('foo-bar;'))

    def test_exclude_invalid_slugs(self):
        self.assertFalse(is_slug(' nope'))
        self.assertFalse(is_slug('nope '))
        self.assertFalse(is_slug(' nope '))
        self.assertFalse(is_slug('#nope'))
        self.assertFalse(is_slug('-nope-'))
        self.assertFalse(is_slug('-no-no-no-'))
        self.assertFalse(is_slug('100%no-slug!'))
        self.assertFalse(is_slug('NOT-AS-UPPERCASE'))

    def test_slug_can_be_single_word(self):
        self.assertTrue(is_slug('hello'))
        self.assertTrue(is_slug('x'))
        self.assertTrue(is_slug('42'))
        self.assertTrue(is_slug('5'))

    def test_slug_must_have_at_least_one_non_separator_char(self):
        self.assertFalse(is_slug('-'))
