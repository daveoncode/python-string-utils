from unittest import TestCase

from string_utils import is_email


class IsEmailTestCase(TestCase):
    """
    Definitions:

    "head" -> the part before "@"
    "tail" -> the part after "@"
    """

    def test_should_return_false_for_non_string_objects(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_email(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_email(False))

        # noinspection PyTypeChecker
        self.assertFalse(is_email(0))

        # noinspection PyTypeChecker
        self.assertFalse(is_email([]))

        # noinspection PyTypeChecker
        self.assertFalse(is_email({'a': 1}))

    def test_string_cannot_be_empty(self):
        self.assertFalse(is_email(''))
        self.assertFalse(is_email(' '))

    def test_tail_is_required(self):
        self.assertFalse(is_email('name@'))

    def test_head_is_required(self):
        self.assertFalse(is_email('@foo.com'))

    def test_at_sign_is_required(self):
        self.assertFalse(is_email('name.site.com'))

    def test_domain_extension_is_required(self):
        self.assertFalse(is_email('name@site'))
        self.assertFalse(is_email('name@site.'))

    def test_domain_extension_should_be_letters_only_from_2_to_4_chars(self):
        self.assertFalse(is_email('me@foo.123'))
        self.assertFalse(is_email('me@foo.c'))
        self.assertFalse(is_email('me@foo.!!'))
        self.assertFalse(is_email('me@foo.___'))
        self.assertFalse(is_email('me@foo.toolongext'))

    def test_head_cannot_contain_suqare_brackets(self):
        self.assertFalse(is_email('[myemail@foo.com'))
        self.assertFalse(is_email('my]email@foo.com'))

    def test_tail_cannot_contain_bad_signs(self):
        self.assertFalse(is_email('me@#foo#.com'))
        self.assertFalse(is_email('me@foo!.com'))
        self.assertFalse(is_email('someone@[foo].com'))

    def test_tail_cannot_be_uppercase(self):
        self.assertFalse(is_email('someone@SOMESITE.COM'))

    def test_tail_cannot_contain_dots_sequence(self):
        self.assertFalse(is_email('name@em..ail.net'))
        self.assertFalse(is_email('name@email..net'))

    def test_domain_cannot_be_single_char(self):
        self.assertFalse(is_email('name@d.com'))

    def test_should_accept_valid_emails(self):
        self.assertTrue(is_email('me@foo.com'))
        self.assertTrue(is_email('name@gmail.com'))
        self.assertTrue(is_email('name2@gmail.com'))
        self.assertTrue(is_email('PeterParker@gmail.com'))
        self.assertTrue(is_email('first_name.last_name@yahoo.it'))
        self.assertTrue(is_email('foo@domamin.subdomain.com'))
        self.assertTrue(is_email('is1email@domain.org'))
        self.assertTrue(is_email('UPPER_CASE_EMAIL@somesite.com'))

    def test_max_email_length_is_respected(self):
        invalid_email = ('a' * 320) + '@gmail.com'
        self.assertFalse(is_email(invalid_email))

    def test_head_length_is_respected(self):
        # max head size is 64
        invalid_email = ('a' * 65) + '@gmail.com'
        self.assertFalse(is_email(invalid_email))

    def test_tail_length_is_respected(self):
        # max tail size is 255
        invalid_email = 'a@{}.com'.format(255 * 'x')
        self.assertFalse(is_email(invalid_email))

    def test_plus_is_valid_char_in_head(self):
        self.assertTrue(is_email('my+mail@gmail.com'))

    def test_plus_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@foo+bar.com'))

    def test_minus_is_valid_char_in_head(self):
        self.assertTrue(is_email('my-mail@gmail.com'))

    def test_slash_is_valid_char_in_head(self):
        self.assertTrue(is_email('my/mail@gmail.com'))

    def test_slash_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@foo/bar.com'))

    def test_back_slash_is_valid_char_in_head(self):
        self.assertTrue(is_email('my\\mail@gmail.com'))

    def test_equal_is_valid_char_in_head(self):
        self.assertTrue(is_email('my=mail@gmail.com'))

    def test_equal_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gm=ail.com'))

    def test_question_mark_is_valid_char_in_head(self):
        self.assertTrue(is_email('my?mail@gmail.com'))

    def test_question_mark_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gm?ail.com'))

    def test_sharp_is_valid_char_in_head(self):
        self.assertTrue(is_email('my#mail@gmail.com'))

    def test_sharp_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gma#il.com'))

    def test_dollar_is_valid_char_in_head(self):
        self.assertTrue(is_email('my$mail@gmail.com'))

    def test_dollar_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gm$ail.com'))

    def test_and_is_valid_char_in_head(self):
        self.assertTrue(is_email('my&mail@gmail.com'))

    def test_and_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gm&ail.com'))

    def test_asterisk_is_valid_char_in_head(self):
        self.assertTrue(is_email('my*mail@gmail.com'))

    def test_asterisk_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gmai*l.com'))

    def test_apostrophe_is_valid_char_in_head(self):
        self.assertTrue(is_email('my\'mail@gmail.com'))

    def test_apostrophe_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gma\'il.com'))

    def test_acute_accent_is_valid_char_in_head(self):
        self.assertTrue(is_email('my`mail@gmail.com'))

    def test_acute_accent_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gma`il.com'))

    def test_percentage_is_valid_char_in_head(self):
        self.assertTrue(is_email('my%mail@gmail.com'))

    def test_percentage_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gma%il.com'))

    def test_exclamation_mark_is_valid_char_in_head(self):
        self.assertTrue(is_email('my!mail@gmail.com'))

    def test_exclamation_mark_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gm!ail.com'))

    def test_caret_is_valid_char_in_head(self):
        self.assertTrue(is_email('my^mail@gmail.com'))

    def test_caret_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gma^il.com'))

    def test_pipe_is_valid_char_in_head(self):
        self.assertTrue(is_email('my|mail@gmail.com'))

    def test_pipe_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gm|ail.com'))

    def test_tilde_is_valid_char_in_head(self):
        self.assertTrue(is_email('my~mail@gmail.com'))

    def test_tilde_is_invalid_char_in_tail(self):
        self.assertFalse(is_email('mymail@gma~il.com'))

    def test_curly_braces_are_valid_char_in_head(self):
        self.assertTrue(is_email('my{mail@gmail.com'))
        self.assertTrue(is_email('my}mail@gmail.com'))
        self.assertTrue(is_email('{mymail}@gmail.com'))

    def test_head_cannot_start_with_period(self):
        self.assertFalse(is_email('.myemail@gmail.com'))

    def test_head_cannot_end_with_period(self):
        self.assertFalse(is_email('myemail.@gmail.com'))

    def test_head_cannot_have_multiple_consecutive_periods(self):
        self.assertFalse(is_email('my..email@gmail.com'))
        self.assertFalse(is_email('my.email...nope@gmail.com'))

    def test_empty_spaces_are_allowed_only_if_escaped(self):
        self.assertFalse(is_email('my mail@gmail.com'))
        self.assertTrue(is_email('my\\ mail@gmail.com'))
        self.assertTrue(is_email('"my mail"@gmail.com'))

    def test_head_can_be_quoted(self):
        self.assertTrue(is_email('"foo"@example.com'))

    def test_head_quotes_must_be_correct(self):
        self.assertFalse(is_email('"nope@gmail.com'))
        self.assertFalse(is_email('no"pe@gmail.com'))
        self.assertFalse(is_email('nope"@gmail.com'))
        self.assertFalse(is_email('""@gmail.com'))
        self.assertFalse(is_email('"no"pe"@gmail.com'))

    def test_with_quoted_string_multiple_at_are_accepted(self):
        self.assertTrue(is_email('"Abc@def"@example.com'))

    def test_with_escape_multiple_at_are_accepted(self):
        self.assertTrue(is_email('Abc\\@def@example.com'))

    def test_head_can_have_self_escape(self):
        self.assertTrue(is_email('Joe.\\\\Blow@example.com'))
