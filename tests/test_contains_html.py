from unittest import TestCase

from string_utils import contains_html


class ContainsHtmlTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            contains_html(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            contains_html(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            contains_html(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            contains_html([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            contains_html({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_handle_empty_strings_as_expected(self):
        self.assertFalse(contains_html(''))
        self.assertFalse(contains_html(' '))

    def test_handle_text_only_as_expected(self):
        self.assertFalse(contains_html('hello world! No html here :)'))

    def test_ignores_tag_signs_if_not_valid_tag(self):
        self.assertFalse(contains_html('>No html>'))
        self.assertFalse(contains_html('<No <html'))

    def test_is_not_html_tag_if_name_is_missing(self):
        self.assertFalse(contains_html('<>'))
        self.assertFalse(contains_html('<1>'))
        self.assertFalse(contains_html('</123>'))
        self.assertFalse(contains_html('no <> no'))
        self.assertFalse(contains_html('</>'))
        self.assertFalse(contains_html('no </> no'))
        self.assertFalse(contains_html('< />'))
        self.assertFalse(contains_html('< no />'))
        self.assertFalse(contains_html('< />nooooo'))
        self.assertFalse(contains_html('<[nope]>'))
        self.assertFalse(contains_html('<!nope>'))
        self.assertFalse(contains_html('<?nope>'))
        self.assertFalse(contains_html('<#nope>'))

    def test_tag_can_be_self_closing_or_not_and_space_before_closing_is_optional(self):
        self.assertTrue(contains_html('one: <br>'))
        self.assertTrue(contains_html('two: <br/>'))
        self.assertTrue(contains_html('three: <br />'))

    def test_tag_name_can_contain_dashes_but_not_as_first_char(self):
        self.assertTrue(contains_html('test <my-custom-tag /> this'))
        self.assertFalse(contains_html('test <-> this'))
        self.assertFalse(contains_html('test <---> this'))
        self.assertFalse(contains_html('test <---/> this'))
        self.assertFalse(contains_html('test <-nope/> this'))

    def test_html_comment_is_properly_recognized(self):
        self.assertTrue(contains_html('foo bar baz <!-- html comment --> banana'))
        self.assertFalse(contains_html('foo bar baz <!- no html comment -> banana'))

    def test_tag_name_cane_even_contain_number_but_not_as_first_char(self):
        self.assertTrue(contains_html('<daitarn3 />'))
        self.assertFalse(contains_html('<3daitarn />'))

    def test_detects_doctype(self):
        self.assertTrue(contains_html('<!DOCTYPE html>'))

    def test_tag_can_have_properties(self):
        self.assertTrue(contains_html('bla bla <input disabled /> bla bla '))
        self.assertTrue(contains_html('bla bla <div flex>xxx</div> bla bla '))
        self.assertTrue(contains_html('bla bla <a one two three />bla bla '))

    def test_tag_properties_can_have_content(self):
        self.assertTrue(contains_html('bla bla <span id="foo">yo</span> bla bla '))
        self.assertTrue(contains_html('bla bla <div style="width: 300px; height: 50px; background: #000">yo</div>'))
        self.assertTrue(contains_html('bla bla <div id="x" class="container">text</div> bla bla '))

    def test_tag_properties_can_use_single_duble_quotes_or_nothing(self):
        self.assertTrue(contains_html('<span id="foo">yo</span>'))
        self.assertTrue(contains_html('<span id=\'foo\'>yo</span>'))
        self.assertTrue(contains_html('<span id=foo>yo</span>'))

    def test_tag_properties_can_have_space_before_or_after_equal_sign(self):
        self.assertTrue(contains_html('<span id ="foo">yo</span>'))
        self.assertTrue(contains_html('<span id= \'foo\'>yo</span>'))
        self.assertTrue(contains_html('<span id = foo>yo</span>'))

    def test_tag_can_have_both_simple_and_complex_properties(self):
        self.assertTrue(contains_html('bla bla <div id="x" class="container" boom>text</div>'))

    def test_tag_can_have_namespace(self):
        self.assertTrue(contains_html('namespace tag: <dz:foo power="100"></dz:foo>'))
        self.assertTrue(contains_html('namespace tag: <dz:test> content </dz:test>'))
        self.assertTrue(contains_html('namespace tag: <a:test/>'))
        self.assertTrue(contains_html('namespace tag: <dz:banana />'))

    def test_tag_can_contains_any_content(self):
        self.assertTrue(contains_html('<html></html>'))
        self.assertTrue(contains_html('<html> content </html>'))
        self.assertTrue(contains_html('<html> <body><p> content </p></body> </html>'))

    def test_tag_can_be_multi_line(self):
        self.assertTrue(contains_html('''
            multi_line tag here:
            <div
                style="width:200px"
                id="foo"
                class="bar">hello</div>
        '''))

    def test_multi_line_are_handled_properly(self):
        self.assertTrue(contains_html('''

            Text here, followed by html:

            <script>
                document.write('you are fucked!');
            </script>

            end!

        '''))
        self.assertFalse(contains_html('''

            plain text
            here

            ...

            should return false!

        '''))
