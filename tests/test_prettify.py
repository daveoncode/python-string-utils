from unittest import TestCase

from string_utils import prettify, is_email


class PrettifyTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            prettify(None)

        self.assertEqual(str(raised.exception), 'Expected "str", received "NoneType"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            prettify(False)

        self.assertEqual(str(raised.exception), 'Expected "str", received "bool"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            prettify(0)

        self.assertEqual(str(raised.exception), 'Expected "str", received "int"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            prettify([])

        self.assertEqual(str(raised.exception), 'Expected "str", received "list"')

        with self.assertRaises(TypeError) as raised:
            # noinspection PyTypeChecker
            prettify({'a': 1})

        self.assertEqual(str(raised.exception), 'Expected "str", received "dict"')

    def test_should_return_empty_string_from_empty_string_or_space_only_string(self):
        self.assertEqual('', prettify(''))
        self.assertEqual('', prettify(' '))

    def test_should_uppercase_first_letter(self):
        self.assertEqual('Hello world', prettify('hello world'))

    def test_should_strip_string(self):
        self.assertEqual('Hello world', prettify(' hello world '))

    def test_should_strip_empty_lines(self):
        self.assertEqual('Hello world', prettify('''

            hello world

        '''))

    def test_should_replace_multiple_brackets_with_single_ones(self):
        self.assertEqual('(foo)', prettify('((foo)'))
        self.assertEqual('(foo)', prettify('(foo))'))
        self.assertEqual('(foo)', prettify('((foo))'))
        self.assertEqual('(foo)', prettify('((((((((foo)))'))
        self.assertEqual('[foo]', prettify('[[foo]'))
        self.assertEqual('[foo]', prettify('[foo]]'))
        self.assertEqual('[foo]', prettify('[[foo]]'))
        self.assertEqual('[foo]', prettify('[[[[[[[[foo]]]'))
        self.assertEqual('{foo}', prettify('{{foo}'))
        self.assertEqual('{foo}', prettify('{foo}}'))
        self.assertEqual('{foo}', prettify('{{foo}}'))
        self.assertEqual('{foo}', prettify('{{{{{{{{foo}}}'))

    def test_should_remove_internal_spaces_in_brackets(self):
        self.assertEqual('(foo)', prettify('( foo)'))
        self.assertEqual('(foo)', prettify('(foo )'))
        self.assertEqual('(foo)', prettify('( foo )'))

    def test_should_add_spaces_outside_brackets(self):
        self.assertEqual('Boo (bar) baz', prettify('boo(bar)baz'))

    def test_should_not_add_right_space_after_bracket_if_followed_by_punctuation(self):
        self.assertEqual('Foo (bar)? Yes!', prettify('Foo(bar)? Yes!'))
        self.assertEqual('Foo (bar): Yes!', prettify('Foo(bar): Yes!'))
        self.assertEqual('Foo (bar). Yes!', prettify('Foo(bar). Yes!'))
        self.assertEqual('Foo (bar); yes!', prettify('Foo(bar); yes!'))
        self.assertEqual('Foo (bar), yes!', prettify('Foo(bar), yes!'))

    def test_should_replace_multiple_commas_with_single_ones(self):
        self.assertEqual('Hello, world', prettify('Hello,,, world'))
        self.assertEqual('Hello, world, banana', prettify('Hello,,, world,, banana'))

    def test_should_replace_multiple_colons_with_single_ones(self):
        self.assertEqual('Hello: world', prettify('Hello::: world'))
        self.assertEqual('Hello: world: banana', prettify('Hello::: world:: banana'))

    def test_should_replace_multiple_semicolons_with_single_ones(self):
        self.assertEqual('Hello; world', prettify('Hello;;; world'))
        self.assertEqual('Hello; world; banana', prettify('Hello;;; world;; banana'))

    def test_should_replace_multiple_double_quotes_with_single_ones(self):
        self.assertEqual('"hello" world', prettify('""hello"" world'))
        self.assertEqual('"hello" world', prettify('""hello" world'))
        self.assertEqual('"hello" world', prettify('"hello"" world'))
        self.assertEqual('"hello" world', prettify('""""""hello""""" world'))

    def test_should_add_spaces_for_double_quotes(self):
        self.assertEqual('Foo "bar" baz', prettify('foo"bar"baz'))
        self.assertEqual('Foo "bar" baz', prettify('foo"bar" baz'))
        self.assertEqual('Foo "bar" baz', prettify('foo "bar"baz'))

    def test_should_trim_spaces_inside_double_quotes(self):
        self.assertEqual('Foo "bar" baz', prettify('foo " bar " baz'))
        self.assertEqual('Foo "bar" baz', prettify('foo "bar " baz'))
        self.assertEqual('Foo "bar" baz', prettify('foo " bar" baz'))

    def test_should_not_add_right_space_after_double_quotes_if_followed_by_punctuation(self):
        self.assertEqual('Foo "bar"? Yes!', prettify('Foo"bar"? Yes!'))
        self.assertEqual('Foo "bar": Yes!', prettify('Foo"bar": Yes!'))
        self.assertEqual('Foo "bar". Yes!', prettify('Foo"bar". Yes!'))
        self.assertEqual('Foo "bar"; yes!', prettify('Foo"bar"; yes!'))
        self.assertEqual('Foo "bar", yes!', prettify('Foo"bar", yes!'))

    def test_should_replace_multiple_single_quotes_with_single_ones(self):
        self.assertEqual('Dave\'s job', prettify("Dave''s job"))
        self.assertEqual("'destiny'", prettify("'''destiny'''"))

    def test_should_fix_saxon_genitive_spaces(self):
        self.assertEqual("Dave's dog", prettify("Dave' s dog"))
        self.assertEqual("Dave's dog", prettify("Dave 's dog"))
        self.assertEqual("Dave's dog", prettify("Dave 'sdog"))

    def test_should_replace_multiple_percentage_with_single_ones(self):
        self.assertEqual('%', prettify('%%%'))
        self.assertEqual('A % b % c', prettify('a %% b %%%%%% c'))

    def test_should_add_space_after_comma_if_missing(self):
        self.assertEqual('One, two, three', prettify('one,two,three'))

    def test_should_not_add_right_space_after_dot_for_numbers(self):
        self.assertEqual('12,55', prettify('12,55'))

    def test_should_remove_space_before_comma(self):
        self.assertEqual('One, two, three', prettify('one , two , three'))

    def test_should_uppercase_first_letter_after_period(self):
        self.assertEqual('Foo. Bar', prettify('Foo. bar'))

    def test_should_add_space_after_period_if_missing(self):
        self.assertEqual('One. Two. Three', prettify('one.two.three'))

    def test_should_not_add_right_space_after_comma_for_numbers(self):
        self.assertEqual('12.55', prettify('12.55'))

    def test_should_remove_space_before_period(self):
        self.assertEqual('One. Two. Three', prettify('one . two . three'))

    def test_should_add_space_after_colon_if_missing(self):
        self.assertEqual('Test: this', prettify('Test:this'))

    def test_should_remove_space_before_colon(self):
        self.assertEqual('Test: this', prettify('Test :this'))
        self.assertEqual('Test:', prettify('Test :'))

    def test_should_add_space_after_semicolon_if_missing(self):
        self.assertEqual('Test; this', prettify('Test;this'))

    def test_should_remove_space_before_semicolon(self):
        self.assertEqual('Test; this', prettify('Test ;this'))
        self.assertEqual('Test;', prettify('Test ;'))

    def test_should_uppercase_first_letter_after_exclamation(self):
        self.assertEqual('Foo! Bar', prettify('Foo! bar'))

    def test_should_add_space_after_exclamation_if_missing(self):
        self.assertEqual('Test! This', prettify('Test!this'))

    def test_should_remove_space_before_exclamation(self):
        self.assertEqual('Test! This', prettify('Test !this'))
        self.assertEqual('Test!', prettify('Test !'))

    def test_should_uppercase_first_letter_after_question(self):
        self.assertEqual('Foo? Bar', prettify('Foo? bar'))

    def test_should_add_space_after_question_if_missing(self):
        self.assertEqual('Test? This', prettify('Test?this'))

    def test_should_remove_space_before_question(self):
        self.assertEqual('Test? This', prettify('Test ?this'))
        self.assertEqual('Test?', prettify('Test ?'))

    def test_should_remove_space_before_dot(self):
        self.assertEqual('Test. This', prettify('Test . This'))
        self.assertEqual('Test.', prettify('Test .'))

    def test_should_remove_space_after_number_if_followed_by_percentage(self):
        self.assertEqual('100% python', prettify('100 % python'))
        self.assertEqual('100%', prettify('100 %'))

    def test_should_add_space_after_percentage_if_missing(self):
        self.assertEqual('100% python code', prettify('100%python code'))

    def test_should_add_spaces_around_plus_if_missing(self):
        self.assertEqual('5 + 2', prettify('5 +2'))
        self.assertEqual('5 + 2', prettify('5+ 2'))
        self.assertEqual('5 + 2', prettify('5+2'))

    def test_should_add_spaces_around_minus_if_missing(self):
        self.assertEqual('5 - 2', prettify('5 -2'))
        self.assertEqual('5 - 2', prettify('5- 2'))
        self.assertEqual('5 - 2', prettify('5-2'))

    def test_should_add_spaces_around_equal_if_missing(self):
        self.assertEqual('5 - 2 = 3', prettify('5 - 2=3'))
        self.assertEqual('5 - 2 = 3', prettify('5 - 2 =3'))
        self.assertEqual('5 - 2 = 3', prettify('5 - 2= 3'))

    def test_should_add_spaces_around_division_if_missing(self):
        self.assertEqual('5 / 2 = 2.5', prettify('5/ 2 = 2.5'))
        self.assertEqual('5 / 2 = 2.5', prettify('5 /2 = 2.5'))
        self.assertEqual('5 / 2 = 2.5', prettify('5/2 = 2.5'))

    def test_should_add_spaces_around_multiplication_if_missing(self):
        self.assertEqual('5 * 2 = 10', prettify('5* 2 = 10'))
        self.assertEqual('5 * 2 = 10', prettify('5 *2 = 10'))
        self.assertEqual('5 * 2 = 10', prettify('5*2 = 10'))

    def test_triple_dot_preserved(self):
        self.assertEqual('Test...', prettify('Test...'))
        self.assertEqual('Test... This', prettify('Test...This'))

    def test_triple_exclamation_preserved(self):
        self.assertEqual('Test!!!', prettify('Test!!!'))
        self.assertEqual('Test!!! This', prettify('Test!!!This'))

    def test_triple_question_preserved(self):
        self.assertEqual('Test???', prettify('Test???'))
        self.assertEqual('Test??? This', prettify('Test???This'))

    def test_should_prettify_string_as_expected(self):
        original = ' unprettified string ,, like this one,will be"prettified" .it\' s awesome!( like python)) '
        pretty = 'Unprettified string, like this one, will be "prettified". It\'s awesome! (like python)'
        self.assertEqual(pretty, prettify(original))

    def test_should_work_as_expected_for_multiple_lines_string(self):
        original = '''

        unprettified string ,,

        like this one,will be"prettified"

        .it' s awesome!( like python))

        '''
        pretty = 'Unprettified string, like this one, will be "prettified". It\'s awesome! (like python)'
        self.assertEqual(pretty, prettify(original))

    def test_does_not_try_to_format_email(self):
        email = 'my.email_name@gmail.com'
        self.assertTrue(is_email(email))
        self.assertEqual(email, prettify(email))
        self.assertEqual('This is the email: {}'.format(email), prettify('this is the email : {}'.format(email)))

        multiple_emails = ['mail.one@gmail.com', 'mail.two@gmail.com', 'mail.three@gmail.com']
        self.assertEqual(prettify(','.join(multiple_emails)), ', '.join(multiple_emails))

    def test_does_not_try_to_format_url(self):
        url = 'https://www.mysite.com/path/page.php?query=foo'
        self.assertEqual(url, prettify(url))
        self.assertEqual('This is the url: {}'.format(url), prettify('this is the url : {}'.format(url)))

        multiple_urls = ['http://www.site1.com', 'http://foo.com', 'https://www.something.it']
        self.assertEqual(prettify(','.join(multiple_urls)), ', '.join(multiple_urls))

    def test_does_not_try_to_format_ip(self):
        ip = '127.0.0.1'
        self.assertEqual(ip, prettify(ip))
        self.assertEqual('This is the ip: {}'.format(ip), prettify('this is the ip : {}'.format(ip)))

        multiple_ip = ['255.255.10.1', '255.255.10.2', '255.255.10.3']
        self.assertEqual(prettify(' '.join(multiple_ip)), ' '.join(multiple_ip))
