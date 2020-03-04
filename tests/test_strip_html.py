import re
from unittest import TestCase

from string_utils import strip_html


class StripHtmlTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_html(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_html(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_html(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_html([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            strip_html({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_should_return_original_string_if_does_not_contain_html(self):
        self.assertEqual('', strip_html(''))
        self.assertEqual(' hello world ', strip_html(' hello world '))
        multi_line_string = '''
            > line 1
            > line 2
            > line 3
        '''
        self.assertEqual(multi_line_string, strip_html(multi_line_string))

    def test_should_remove_html_tags(self):
        self.assertEqual('foo  bar', strip_html('foo <br> bar'))
        self.assertEqual('foo  bar', strip_html('foo <br/> bar'))
        self.assertEqual('foo  bar', strip_html('foo <br /> bar'))
        self.assertEqual('  ', strip_html(' <div></div> '))

    def test_should_be_able_to_remove_multiple_tags(self):
        stripped = strip_html('''
            a <div>on the first line</div>
            a <span>on the second line</span>
            a <strong>on the third line</strong>
            a <hr />
        ''')
        self.assertEqual('aaaa', re.sub(r'\s', '', stripped))
        stripped2 = strip_html('''
            a <div>(on the first line)</div>
            a <span>(on the second line)</span>
            a <strong>(on the third line)</strong>
            a <hr />
        ''', keep_tag_content=True)
        self.assertEqual('a(onthefirstline)a(onthesecondline)a(onthethirdline)a', re.sub(r'\s', '', stripped2))

    def test_should_keep_tag_content_if_specified(self):
        s = 'test: <a href="foo/bar">click here</a>'
        self.assertEqual('test: ', strip_html(s))
        self.assertEqual('test: click here', strip_html(s, keep_tag_content=True))
        multiline_string = '''
            <html>
                <body>
                    <div id="container">
                        <p>content text!<p>
                    </div>
                </body>
            </html>
        '''
        self.assertEqual('content text!', strip_html(multiline_string, keep_tag_content=True).strip())
