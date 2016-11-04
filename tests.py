# -*- coding: utf-8 -*-

from unittest.case import TestCase
from uuid import uuid4
import json
import re

from string_utils import *


# string checking tests

class IsStringTestCase(TestCase):
    def test_return_false_for_non_string_objects(self):
        self.assertFalse(is_string(None))
        self.assertFalse(is_string(False))
        self.assertFalse(is_string(0))
        self.assertFalse(is_string([]))
        self.assertFalse(is_string({'a': 1}))

    def test_return_true_for_string_objects(self):
        self.assertTrue(is_string(''))
        self.assertTrue(is_string('hello world'))
        self.assertTrue(is_string(r'[a-z]'))


class IsFullStringTestCase(TestCase):
    def test_empty_string_is_not_full(self):
        self.assertFalse(is_full_string(''))

    def test_white_space_is_not_full(self):
        self.assertFalse(is_full_string(' '))
        self.assertFalse(is_full_string('''
            \n
            \n
            \n
        '''))

    def test_word_string_is_full(self):
        self.assertTrue(is_full_string('ciao'))
        self.assertTrue(is_full_string(' hi '))
        self.assertTrue(is_full_string('1'))
        self.assertTrue(is_full_string(' @*& '))
        self.assertTrue(is_full_string('...'))


class IsUrlTestCase(TestCase):
    def test_should_return_false_for_non_string_objects(self):
        self.assertFalse(is_url(None))
        self.assertFalse(is_url(False))
        self.assertFalse(is_url(0))
        self.assertFalse(is_url([]))
        self.assertFalse(is_url({'a': 1}))

    def test_string_cannot_be_blank(self):
        self.assertFalse(is_url(''))
        self.assertFalse(is_url(' '))

    def test_string_cannot_contain_spaces(self):
        self.assertFalse(is_url(' http://www.google.com'))
        self.assertFalse(is_url('http://www.google.com '))
        self.assertFalse(is_url('http://www.google.com/ ncr'))
        self.assertFalse(is_url('http://www.goo gle.com'))

    def test_scheme_is_required(self):
        self.assertFalse(is_url('google.com'))

    def test_domain_extension_is_required_for_named_urls(self):
        self.assertFalse(is_url('http://google'))
        self.assertFalse(is_url('http://google.'))

    def test_domain_extension_should_be_between_2_and_6_letters(self):
        self.assertFalse(is_url('http://google.c'))
        self.assertFalse(is_url('http://google.abcdefghi'))

    def test_should_accept_any_scheme_by_default(self):
        self.assertTrue(is_url('http://site.com'))
        self.assertTrue(is_url('http://www.site.com'))
        self.assertTrue(is_url('https://site.com'))
        self.assertTrue(is_url('https://www.site.com'))
        self.assertTrue(is_url('ftp://site.com'))
        self.assertTrue(is_url('git://site.com'))

    def test_should_restrict_checking_on_provided_schemes(self):
        self.assertTrue(is_url('git://site.com'))
        self.assertFalse(is_url('git://site.com', allowed_schemes=['http', 'https']))

    def test_url_cannot_start_with_dot(self):
        self.assertFalse(is_url('http://.site.com'))

    def test_url_can_contain_dash(self):
        self.assertTrue(is_url('http://some-site-name.com'))

    def test_url_cannot_start_with_dash(self):
        self.assertFalse(is_url('http://-site.com'))

    def test_url_cannot_start_with_slash(self):
        self.assertFalse(is_url('http:///www.site.com'))

    def test_www_is_optional(self):
        self.assertTrue(is_url('http://www.daveoncode.com'))
        self.assertTrue(is_url('http://daveoncode.com'))

    def test_localhost_is_an_accepted_url(self):
        self.assertTrue(is_url('http://localhost'))

    def test_should_accept_valid_ip_url(self):
        self.assertTrue(is_url('http://123.123.123.123'))
        self.assertTrue(is_url('http://1.123.123.123'))
        self.assertTrue(is_url('http://1.1.123.123'))
        self.assertTrue(is_url('http://1.1.1.123'))
        self.assertTrue(is_url('http://1.1.1.1'))
        self.assertTrue(is_url('http://123.123.123.1'))
        self.assertTrue(is_url('http://123.123.1.1'))
        self.assertTrue(is_url('http://123.1.1.1'))

    def test_should_exclude_invalid_ip(self):
        self.assertFalse(is_url('http://1.2.3'))
        self.assertFalse(is_url('http://1.2.3.'))
        self.assertFalse(is_url('http://123.123.123.1234'))
        self.assertFalse(is_url('http://.123.123.123.123'))
        self.assertFalse(is_url('http://123.123.123.123.'))
        self.assertFalse(is_url('http://123.123...123.123'))
        self.assertFalse(is_url('http://123..123..123.123'))

    def test_url_can_have_port_number(self):
        self.assertTrue(is_url('http://localhost:8080'))

    def test_url_can_contain_sub_folders(self):
        self.assertTrue(is_url('http://www.site.com/one'))
        self.assertTrue(is_url('http://www.site.com/one/'))
        self.assertTrue(is_url('http://www.site.com/one/two'))
        self.assertTrue(is_url('http://www.site.com/one/two/'))
        self.assertTrue(is_url('http://www.site.com/one/two/three/four/five/six'))

    def test_url_can_have_user_and_password(self):
        self.assertTrue(is_url('postgres://myuser:mypassword@localhost:5432/mydb'))

    def test_url_can_contain_file_extension(self):
        self.assertTrue(is_url('http://site.com/foo/photo.jpg'))
        self.assertTrue(is_url('http://site.com/index.html'))

    def test_file_can_contains_multiple_dots(self):
        self.assertTrue(is_url('http://site.com/foo/file.name.ext'))

    def test_url_can_contain_query_string(self):
        self.assertTrue(is_url('http://site.com/foo/?'))
        self.assertTrue(is_url('http://site.com/foo/?foo'))
        self.assertTrue(is_url('http://site.com/foo/?foo=bar'))
        self.assertTrue(is_url('http://site.com/foo/?foo=bar&baz=1'))
        self.assertTrue(is_url('http://site.com/foo/?foo=bar&baz=1&'))

    def test_url_can_have_hash_part(self):
        self.assertTrue(is_url('http://site.com/foo#anchor'))
        self.assertTrue(is_url('http://site.com/foo#anchor2-with_several+signs++'))

    def test_a_full_url(self):
        self.assertTrue(is_url('https://www.site.com/a/b/c/banana/file.html?foo=1&bar=2#hello-world'))


class IsEmailTestCase(TestCase):
    def test_should_return_false_for_non_string_objects(self):
        self.assertFalse(is_email(None))
        self.assertFalse(is_email(False))
        self.assertFalse(is_email(0))
        self.assertFalse(is_email([]))
        self.assertFalse(is_email({'a': 1}))

    def test_string_cannot_be_empty(self):
        self.assertFalse(is_email(''))
        self.assertFalse(is_email(' '))

    def test_domain_part_is_required(self):
        self.assertFalse(is_email('name@'))

    def test_name_part_is_required(self):
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

    def test_name_part_cannot_contain_bad_signs(self):
        self.assertFalse(is_email('#me#@foo.com'))
        self.assertFalse(is_email('me!@foo.com'))
        self.assertFalse(is_email('[][]@foo.com'))
        self.assertFalse(is_email('john%@john5music.net'))

    def test_domain_part_cannot_contain_bad_signs(self):
        self.assertFalse(is_email('me@#foo#.com'))
        self.assertFalse(is_email('me@foo!.com'))
        self.assertFalse(is_email('someone@[foo].com'))

    def test_domain_part_cannot_be_uppercase(self):
        self.assertFalse(is_email('someone@SOMESITE.COM'))

    def test_domain_part_cannot_contain_dots_sequence(self):
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


class IsCreditCardTestCase(TestCase):
    # numbers generated by: http://www.getcreditcardnumbers.com
    sample_cards = {
        'VISA': [
            '4929108461099666',
            '4485341431836919',
            '4929383875909178',
            '4024007178235312',
            '4929943872251997'
        ],
        'MASTERCARD': [
            '5593685744413543',
            '5299068126557657',
            '5519706741220334',
            '5349375673926726',
            '5536077751185034'
        ],
        'DISCOVER': [
            '6011738421556670',
            '6011902207467698',
            '6011066039342048',
            '6011084365330958',
            '6011417613048024'
        ],
        'AMERICAN_EXPRESS': [
            '378255041294558',
            '344411347420469',
            '376197548847524',
            '348870102379192',
            '340073988128712'
        ],
        'JCB': [
            '3528968052436214',
            '213140714369305',
            '180095242210070',
            '213122809097983',
            '213181044765010'
        ],
        'DINERS_CLUB': [
            '30161673137117',
            '38476920787395',
            '38652978387607',
            '36802519893181',
            '30347192978103'
        ]
    }

    def test_should_return_false_for_non_string_objects(self):
        self.assertFalse(is_credit_card(None))
        self.assertFalse(is_credit_card(False))
        self.assertFalse(is_credit_card(0))
        self.assertFalse(is_credit_card([]))
        self.assertFalse(is_credit_card({'a': 1}))

    def test_string_cannot_be_empty(self):
        self.assertFalse(is_credit_card(''))
        self.assertFalse(is_credit_card(' '))

    def test_string_cannot_contain_letters(self):
        self.assertFalse(is_credit_card('not a credit card for sure'))

    def test_numbers_in_string_should_be_15_at_least(self):
        self.assertFalse(is_credit_card('1' * 14))

    def test_should_accept_any_valid_card_number_if_type_is_not_specified(self):
        for card_type in self.sample_cards:
            for card_number in self.sample_cards[card_type]:
                self.assertTrue(is_credit_card(card_number), 'Invalid card: %s (%s)' % (card_number, card_type))

    def test_should_validate_only_specific_card_type_if_specified(self):
        for card_type in self.sample_cards:
            for card_number in self.sample_cards[card_type]:
                self.assertTrue(
                    is_credit_card(card_number, card_type=card_type),
                    'Invalid card: %s (%s)' % (card_number, card_type)
                )
                other_cards = self.sample_cards.copy()
                del other_cards[card_type]
                for other_card in other_cards:
                    self.assertFalse(
                        is_credit_card(card_number, card_type=other_card),
                        'Card %s should not be a valid %s' % (card_number, other_card)
                    )

    def test_cannot_provide_unsupported_card_type(self):
        self.assertRaises(KeyError, lambda: is_credit_card(self.sample_cards['VISA'][0], card_type='FOO_CARD'))


class IsCamelCaseTestCase(TestCase):
    def test_should_return_false_for_non_string_objects(self):
        self.assertFalse(is_camel_case(None))
        self.assertFalse(is_camel_case(False))
        self.assertFalse(is_camel_case(0))
        self.assertFalse(is_camel_case([]))
        self.assertFalse(is_camel_case({'a': 1}))

    def test_string_cannot_be_empty(self):
        self.assertFalse(is_camel_case(''))
        self.assertFalse(is_camel_case(' '))

    def test_string_cannot_be_all_lowercase(self):
        self.assertFalse(is_camel_case('lowercase'))

    def test_string_cannot_be_all_uppercase(self):
        self.assertFalse(is_camel_case('UPPERCASE'))

    def test_string_cannot_contain_spaces(self):
        self.assertFalse(is_camel_case(' CamelCase '))

    def test_string_cannot_start_with_number(self):
        self.assertFalse(is_camel_case('1000Times'))

    def test_string_cannot_contain_invalid_chars(self):
        self.assertFalse(is_camel_case('<#NotCamelCaseHere!?>'))

    def test_should_accept_valid_camel_case_string(self):
        self.assertTrue(is_camel_case('Camel'))
        self.assertTrue(is_camel_case('CamelCase'))
        self.assertTrue(is_camel_case('camelCase'))
        self.assertTrue(is_camel_case('CamelCaseTOO'))
        self.assertTrue(is_camel_case('ACamelCaseIsAlsoAStringLikeThis1'))
        self.assertTrue(is_camel_case('camelCaseStartingLowerEndingUPPER'))


class IsSnakeCaseTestCase(TestCase):
    def test_return_false_for_non_string_objects(self):
        self.assertFalse(is_snake_case(None))
        self.assertFalse(is_snake_case(False))
        self.assertFalse(is_snake_case(0))
        self.assertFalse(is_snake_case([]))
        self.assertFalse(is_snake_case({'a': 1}))

    def test_string_cannot_be_blank(self):
        self.assertFalse(is_snake_case(''))
        self.assertFalse(is_snake_case(' '))

    def test_string_cannot_be_lowercase_letters_only(self):
        self.assertFalse(is_snake_case('lowercaseonly'))

    def test_string_cannot_be_camel_case(self):
        self.assertFalse(is_snake_case('Banana'))

    def test_string_cannot_be_all_uppercase(self):
        self.assertFalse(is_snake_case('HELLO'))

    def test_string_cannot_contain_bad_signs(self):
        self.assertFalse(is_snake_case('1_no_snake'))
        self.assertFalse(is_snake_case('%_no_snake'))
        self.assertFalse(is_snake_case('no_snake#'))

    def test_should_consider_single_chars_only_snake_sequence_invalid(self):
        self.assertFalse(is_snake_case('a_b_c_d_e'))

    def test_snake_string_cannot_be_uppercase(self):
        self.assertFalse(is_snake_case('HELLO_WORLD'))

    def test_string_cannot_start_with_underscore(self):
        self.assertFalse(is_snake_case('_hello_world'))

    def test_string_cannot_end_with_underscore(self):
        self.assertFalse(is_snake_case('hello_world_'))

    def test_should_accept_valid_snake_strings(self):
        self.assertTrue(is_snake_case('hello_world'))
        self.assertTrue(is_snake_case('snake_case_string'))
        self.assertTrue(is_snake_case('snake_2'))
        self.assertTrue(is_snake_case('a_snake_string_4_you'))

    def test_should_consider_custom_separator(self):
        s = 'snake-string-with-dashes'
        self.assertFalse(is_snake_case(s))
        self.assertTrue(is_snake_case(s, separator='-'))


class IsJsonTestCase(TestCase):
    def test_non_string_objects_are_properly_handled(self):
        self.assertFalse(is_json({'a': 1}))
        self.assertFalse(is_json(None))
        self.assertFalse(is_json([1, 2, 3]))
        self.assertFalse(is_json(500))
        self.assertFalse(is_json(True))
        self.assertFalse(is_json(set([1, 2])))

    def test_empty_string_are_invalid(self):
        self.assertFalse(is_json(''))
        self.assertFalse(is_json(' '))

    def test_json_object_can_be_empty(self):
        self.assertTrue(is_json('{}'))

    def test_external_spaces_are_ignored(self):
        self.assertTrue(is_json('{"foo":"bar"}'))
        self.assertTrue(is_json(' { "foo": "bar" } '))
        self.assertTrue(is_json('''
            {
                "foo": "bar"
            }
        '''))

    def test_attributes_quotes_are_mandatory(self):
        self.assertFalse(is_json('{foo: 1}'))

    def test_attributes_quotes_should_be_double_quotes(self):
        self.assertFalse(is_json("{'foo': 1}"))

    def test_string_values_should_be_wrapped_by_double_quotes(self):
        self.assertFalse(is_json('{"foo": hello}'))
        self.assertFalse(is_json('{"foo": \'hello\'}'))
        self.assertTrue(is_json('{"foo": "hello"}'))

    def test_boolean_should_be_lowercase(self):
        self.assertFalse(is_json('{"bool": True}'))
        self.assertFalse(is_json('{"bool": FALSE}'))
        self.assertTrue(is_json('{"bool": true}'))
        self.assertIsInstance(json.loads('{"bool": true}'), dict)
        self.assertTrue(is_json('{"bool": false}'))
        self.assertIsInstance(json.loads('{"bool": false}'), dict)

    def test_null_should_be_lowercase(self):
        self.assertFalse(is_json('{"null": NULL}'))
        self.assertFalse(is_json('{"null": Null}'))
        self.assertTrue(is_json('{"null": null}'))
        self.assertIsInstance(json.loads('{"null": null}'), dict)

    def test_int_number_can_be_any_length(self):
        self.assertTrue(is_json('{"number": 1}'))
        self.assertTrue(is_json('{"number": 99}'))
        self.assertTrue(is_json('{"number": 1000}'))
        self.assertTrue(is_json('{"number": 1234567890}'))

    def test_float_numbers_should_use_dot_as_separator(self):
        self.assertFalse(is_json('{"float": 4,5}'))
        self.assertTrue(is_json('{"float": 4.5}'))
        self.assertIsInstance(json.loads('{"float": 4.5}'), dict)

    def test_negative_numbers_should_be_start_with_minus(self):
        self.assertFalse(is_json('{"number": - 2}'))
        self.assertFalse(is_json('{"number": - 2.5}'))
        self.assertTrue(is_json('{"number": -2}'))
        self.assertTrue(is_json('{"number": -2.5}'))

    def test_array_can_be_empty(self):
        self.assertTrue(is_json('{"array": []}'))
        self.assertTrue(is_json('{"array": [ ]}'))

    def test_object_can_be_empty(self):
        self.assertTrue(is_json('{"obj": {}}'))
        self.assertTrue(is_json('{"obj": { }}'))

    def test_cannot_have_trailing_comma_in_array(self):
        self.assertFalse(is_json('{"numbers": [1,2,3,]}'))

    def test_cannot_have_multiple_comma_in_array(self):
        self.assertFalse(is_json('{"numbers": [1,2,,3]}'))

    def test_cannot_have_trailing_comma_in_object(self):
        self.assertFalse(is_json('{"numbers": {"a": 1, "b": 2,}}'))

    def test_cannot_have_multiple_comma_in_object(self):
        self.assertFalse(is_json('{"numbers": {"a": 1,, "b": 2}}'))

    def test_string_can_contain_escaped_quotes(self):
        s = '{"string": "Look: \\"escaped string here!\\""}'
        self.assertTrue(is_json(s))
        self.assertIsInstance(json.loads(s), dict)

    def test_array_is_not_json(self):
        self.assertFalse(is_json('[1,2,3]'))

    def test_complete_json_case(self):
        string = '''
            {
                "books": [
                    {
                        "title": "Book title 1",
                        "author": "FirstName LastName",
                        "tags": ["tech", "programming", "python"],
                        "available": true,
                        "pageCount": 516,
                        "rating": 4.5,
                        "comments": [
                            {
                                "author": "FirstName LastName",
                                "content": "Nice book!"
                            }
                        ]
                    },
                    {
                        "title": "Book title 2",
                        "author": "FirstName LastName",
                        "tags": ["tech", "programming", "javascript"],
                        "available": true,
                        "rating": 4,
                        "pageCount": 422,
                        "comments": [

                        ]
                    }
                ]
            }
        '''
        self.assertTrue(is_json(string))
        self.assertIsInstance(json.loads(string), dict)


class IsUUIDTestCase(TestCase):
    def test_should_consider_false_non_string_objects(self):
        self.assertFalse(is_uuid(None))
        self.assertFalse(is_uuid(1))
        self.assertFalse(is_uuid([]))
        self.assertFalse(is_uuid({'a': 1}))
        self.assertFalse(is_uuid(True))

    def test_should_accept_valid_uuid_objects(self):
        for i in range(1000):
            self.assertTrue(is_uuid(uuid4()))

    def test_should_accept_valid_uuid_strings(self):
        for i in range(1000):
            self.assertTrue(is_uuid(str(uuid4())))


class IsIpTestCase(TestCase):
    def test_return_false_for_non_string_objects(self):
        self.assertFalse(is_ip(None))
        self.assertFalse(is_ip(1))
        self.assertFalse(is_ip([]))
        self.assertFalse(is_ip({'a': 1}))
        self.assertFalse(is_ip(True))

    def test_recognize_ip_strings(self):
        self.assertTrue(is_ip('127.0.0.1'))
        self.assertTrue(is_ip('0.0.0.0'))
        self.assertTrue(is_ip('255.255.10.1'))

    def test_ip_cannot_contain_spaces(self):
        self.assertFalse(is_ip(' 127.0.0.1 '))
        self.assertFalse(is_ip('0.0.0.0 '))
        self.assertFalse(is_ip(' 255.255.10.1'))
        self.assertFalse(is_ip('255. 255.10.1'))

    def test_ip_cannot_have_multiple_dots(self):
        self.assertFalse(is_ip('127.0.0..1'))
        self.assertFalse(is_ip('0..0.0.0'))
        self.assertFalse(is_ip('255.255.10.1.'))

    def test_numbers_cannot_be_divided_by_other_signs(self):
        self.assertFalse(is_ip('127-0-0-1'))
        self.assertFalse(is_ip('0_0_0_0'))
        self.assertFalse(is_ip('255,255,10,1'))

    def test_ip_cannot_be_blank(self):
        self.assertFalse(is_ip(''))
        self.assertFalse(is_ip(' '))


class WordsCountTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: words_count(None))
        self.assertRaises(TypeError, lambda: words_count(False))
        self.assertRaises(TypeError, lambda: words_count(0))
        self.assertRaises(TypeError, lambda: words_count([]))
        self.assertRaises(TypeError, lambda: words_count({'a': 1}))

    def test_signs_are_not_considered_words(self):
        self.assertEqual(words_count('. . ! <> [] {} + % --- _ = @ # ~ | \ / " \''), 0)

    def test_case_doesnt_matter(self):
        self.assertEqual(words_count('hello world'), 2)
        self.assertEqual(words_count('HELLO WORLD'), 2)
        self.assertEqual(words_count('hello WORLD'), 2)

    def test_support_multiline(self):
        self.assertEqual(words_count('''

            hello

            world

        '''), 2)

    def test_word_with_numbers_is_considered_single_word(self):
        self.assertEqual(words_count('jinja2'), 1)
        self.assertEqual(words_count('Area52'), 1)

    def test_words_divided_by_underscore_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello _world'), 2)
        self.assertEqual(words_count('hello _ world'), 2)
        self.assertEqual(words_count('hello_ world'), 2)
        self.assertEqual(words_count('hello_world'), 2)

    def test_words_divided_by_dash_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello - world'), 2)
        self.assertEqual(words_count('hello -world'), 2)
        self.assertEqual(words_count('hello- world'), 2)
        self.assertEqual(words_count('hello-world'), 2)

    def test_words_divided_by_pipe_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello | world'), 2)
        self.assertEqual(words_count('hello |world'), 2)
        self.assertEqual(words_count('hello| world'), 2)
        self.assertEqual(words_count('hello|world'), 2)

    def test_words_divided_by_plus_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello + world'), 2)
        self.assertEqual(words_count('hello +world'), 2)
        self.assertEqual(words_count('hello+ world'), 2)
        self.assertEqual(words_count('hello+world'), 2)

    def test_words_divided_by_colons_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello : world'), 2)
        self.assertEqual(words_count('hello :world'), 2)
        self.assertEqual(words_count('hello: world'), 2)
        self.assertEqual(words_count('hello:world'), 2)

    def test_words_divided_by_semicolons_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello ; world'), 2)
        self.assertEqual(words_count('hello ;world'), 2)
        self.assertEqual(words_count('hello; world'), 2)
        self.assertEqual(words_count('hello;world'), 2)

    def test_words_divided_by_equal_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello = world'), 2)
        self.assertEqual(words_count('hello =world'), 2)
        self.assertEqual(words_count('hello= world'), 2)
        self.assertEqual(words_count('hello=world'), 2)

    def test_words_divided_by_question_mark_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello ? world'), 2)
        self.assertEqual(words_count('hello ?world'), 2)
        self.assertEqual(words_count('hello? world'), 2)
        self.assertEqual(words_count('hello?world'), 2)

    def test_words_divided_by_exclamation_mark_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello ! world'), 2)
        self.assertEqual(words_count('hello !world'), 2)
        self.assertEqual(words_count('hello! world'), 2)
        self.assertEqual(words_count('hello!world'), 2)

    def test_words_divided_by_apos_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello \' world'), 2)
        self.assertEqual(words_count('hello \'world'), 2)
        self.assertEqual(words_count('hello\' world'), 2)
        self.assertEqual(words_count('hello\'world'), 2)

    def test_words_divided_by_and_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('joseph & joseph'), 2)
        self.assertEqual(words_count('joseph &joseph'), 2)
        self.assertEqual(words_count('joseph& joseph'), 2)
        self.assertEqual(words_count('joseph&joseph'), 2)

    def test_words_divided_by_comma_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello , world'), 2)
        self.assertEqual(words_count('hello ,world'), 2)
        self.assertEqual(words_count('hello, world'), 2)
        self.assertEqual(words_count('hello,world'), 2)

    def test_words_divided_by_dot_are_considered_multiple_even_if_space_is_missing(self):
        self.assertEqual(words_count('hello . world'), 2)
        self.assertEqual(words_count('hello .world'), 2)
        self.assertEqual(words_count('hello. world'), 2)
        self.assertEqual(words_count('hello.world'), 2)

    def test_quoted_text_is_handled_properly(self):
        self.assertEqual(words_count('this text "is quoted"'), 4)
        self.assertEqual(words_count('this text"is quoted"'), 4)

    def test_parenthesis_are_properly_handled(self):
        self.assertEqual(words_count('Does it work? (just a test)'), 6)
        self.assertEqual(words_count('Does it work?(just a test)'), 6)
        self.assertEqual(words_count('Does it work? (just a test)I hope'), 8)

    def test_return_expected_count(self):
        self.assertEqual(words_count('hello'), 1)
        self.assertEqual(words_count('hello world'), 2)
        self.assertEqual(words_count('a couple of words and the number 1'), 8)
        self.assertEqual(words_count('Testing (this)'), 2)
        self.assertEqual(words_count('''
            this is my list:

            - (1) one
            - (2) two
            - (3) three

        '''), 10)

    def test_should_count_non_ascii_words(self):
        self.assertEqual(words_count('é vero o é falso?'), 5)


class ContainsHtmlTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: contains_html(None))
        self.assertRaises(TypeError, lambda: contains_html(False))
        self.assertRaises(TypeError, lambda: contains_html(0))
        self.assertRaises(TypeError, lambda: contains_html([]))
        self.assertRaises(TypeError, lambda: contains_html({'a': 1}))

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

    def test_tag_can_be_multiline(self):
        self.assertTrue(contains_html('''
            multiline tag here:
            <div
                style="width:200px"
                id="foo"
                class="bar">hello</div>
        '''))

    def test_multiline_are_handled_properly(self):
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


# string manipulation tests

class ReverseTestCase(TestCase):
    def test_returns_original_string_if_unreversible(self):
        self.assertEqual(reverse(''), '')
        self.assertEqual(reverse('x'), 'x')
        self.assertEqual(reverse('!!!'), '!!!')

    def test_returns_reversed_string(self):
        self.assertEqual(reverse('hello world'), 'dlrow olleh')


class CamelCaseToSnakeTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: camel_case_to_snake(None))
        self.assertRaises(TypeError, lambda: camel_case_to_snake(False))
        self.assertRaises(TypeError, lambda: camel_case_to_snake(0))
        self.assertRaises(TypeError, lambda: camel_case_to_snake([]))
        self.assertRaises(TypeError, lambda: camel_case_to_snake({'a': 1}))

    def test_returns_same_string_if_all_lowercase(self):
        s = 'lower'
        self.assertEqual(camel_case_to_snake(s), s)

    def test_returns_same_string_if_all_uppercase(self):
        s = 'UPPERCASE'
        self.assertEqual(camel_case_to_snake(s), s)

    def test_returns_lowercase_string_for_single_word(self):
        s = 'Hello'
        self.assertEqual(camel_case_to_snake(s), s.lower())

    def test_returns_words_divided_by_underscores_for_each_camel_word(self):
        s = 'CamelCaseStringToTest'
        self.assertEqual(camel_case_to_snake(s), 'camel_case_string_to_test')

    def test_returns_words_divided_by_underscores_for_each_camel_word_even_for_articles(self):
        s = 'ThisIsACamelStringTestB'
        self.assertEqual(camel_case_to_snake(s), 'this_is_a_camel_string_test_b')

    def test_handles_acronyms_gracefully(self):
        s = 'SPAAppsAreVeryPopularOnTheWEBToday'
        self.assertEqual(camel_case_to_snake(s), 'spa_apps_are_very_popular_on_the_web_today')

    def test_should_return_same_string_if_contains_spaces(self):
        s = 'This Is Not A Camel Case String! butThisOneIs'
        self.assertEqual(camel_case_to_snake(s), s)

    def test_should_use_provided_separator(self):
        s = 'CamelCaseString'
        self.assertEqual(camel_case_to_snake(s, '_'), 'camel_case_string')
        self.assertEqual(camel_case_to_snake(s, '||'), 'camel||case||string')
        self.assertEqual(camel_case_to_snake(s, ' '), 'camel case string')


class SnakeCaseToCamelTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: snake_case_to_camel(None))
        self.assertRaises(TypeError, lambda: snake_case_to_camel(False))
        self.assertRaises(TypeError, lambda: snake_case_to_camel(0))
        self.assertRaises(TypeError, lambda: snake_case_to_camel([]))
        self.assertRaises(TypeError, lambda: snake_case_to_camel({'a': 1}))

    def test_returns_original_string_if_not_snake_case(self):
        self.assertEqual(snake_case_to_camel(''), '')
        self.assertEqual(snake_case_to_camel('foo'), 'foo')
        self.assertEqual(snake_case_to_camel('foo bar baz'), 'foo bar baz')
        self.assertEqual(snake_case_to_camel('__not_snake'), '__not_snake')
        self.assertEqual(snake_case_to_camel('_still_not_snake'), '_still_not_snake')
        self.assertEqual(snake_case_to_camel('not_snake_!'), 'not_snake_!')
        self.assertEqual(snake_case_to_camel('(not_snake)'), '(not_snake)')
        self.assertEqual(snake_case_to_camel('123not_snake'), '123not_snake')

    def test_returns_camel_case_from_correct_snake_case(self):
        self.assertEqual(snake_case_to_camel('hello_world'), 'HelloWorld')
        self.assertEqual(snake_case_to_camel('the_snake_is_green'), 'TheSnakeIsGreen')
        self.assertEqual(snake_case_to_camel('the_number_of_the_beast_is_666'), 'TheNumberOfTheBeastIs666')

    def test_should_consider_custom_separator(self):
        s = 'snake-case-using-dashes'
        self.assertEqual(snake_case_to_camel(s), s)
        self.assertEqual(snake_case_to_camel(s, separator='-'), 'SnakeCaseUsingDashes')

    def test_should_not_capitalize_first_letter_if_specified(self):
        self.assertEqual(snake_case_to_camel('this_will_starts_lower_case', False), 'thisWillStartsLowerCase')


class UUUIDTestCase(TestCase):
    def test_generates_uuid_string(self):
        uid = uuid()
        self.assertIsInstance(uid, str)
        self.assertTrue(is_uuid(uid))


class ShuffleTestCase(TestCase):
    original_string = 'Hello World!'

    def test_shuffled_string_should_be_different_from_original_one(self):
        self.assertNotEqual(self.original_string, shuffle(self.original_string))

    def test_original_string_is_not_modified(self):
        shuffle(self.original_string)
        self.assertEqual(self.original_string, 'Hello World!')

    def test_shuffle_generates_new_string_for_each_call(self):
        self.assertNotEqual(shuffle(self.original_string), shuffle(self.original_string))

    def test_shuffled_string_should_have_same_len_of_original_one(self):
        shuffled = shuffle(self.original_string)
        self.assertTrue(len(self.original_string), len(shuffled))

    def test_sorted_strings_should_match(self):
        shuffled = shuffle(self.original_string)
        self.assertEqual(sorted(self.original_string), sorted(shuffled))


class StripHtmlTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: strip_html(None))
        self.assertRaises(TypeError, lambda: strip_html(False))
        self.assertRaises(TypeError, lambda: strip_html(0))
        self.assertRaises(TypeError, lambda: strip_html([]))
        self.assertRaises(TypeError, lambda: strip_html({'a': 1}))

    def test_should_return_original_string_if_does_not_contain_html(self):
        self.assertEqual('', strip_html(''))
        self.assertEqual(' hello world ', strip_html(' hello world '))
        multiline_string = '''
            > line 1
            > line 2
            > line 3
        '''
        self.assertEqual(multiline_string, strip_html(multiline_string))

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


class PrettifyTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: words_count(None))
        self.assertRaises(TypeError, lambda: words_count(False))
        self.assertRaises(TypeError, lambda: words_count(0))
        self.assertRaises(TypeError, lambda: words_count([]))
        self.assertRaises(TypeError, lambda: words_count({'a': 1}))

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


class IsPalindromeTestCase(TestCase):
    def test_non_string_objects_return_false(self):
        self.assertFalse(is_palindrome(1))
        self.assertFalse(is_palindrome(['xx']))
        self.assertFalse(is_palindrome({}))
        self.assertFalse(is_palindrome(False))
        self.assertFalse(is_palindrome((1, 2, 3)))
        self.assertFalse(is_palindrome(object()))

    def test_empty_strings_are_not_palindromes(self):
        self.assertFalse(is_palindrome(''))
        self.assertFalse(is_palindrome(' '))
        self.assertFalse(is_palindrome(' \n\t '))

    def test_strict_checking(self):
        self.assertFalse(is_palindrome('nope!'))
        self.assertFalse(is_palindrome('i topi non avevano nipoti'))
        self.assertTrue(is_palindrome('otto'))

    def test_no_strict_mode(self):
        self.assertFalse(is_palindrome('nope!', False))
        self.assertTrue(is_palindrome('i topi non avevano nipoti', False))
        self.assertTrue(is_palindrome('otto', False))


class IsPangramTestCase(TestCase):
    def test_non_string_objects_return_false(self):
        self.assertFalse(is_pangram(1))
        self.assertFalse(is_pangram(['xx']))
        self.assertFalse(is_pangram({}))
        self.assertFalse(is_pangram(False))
        self.assertFalse(is_pangram((1, 2, 3)))
        self.assertFalse(is_pangram(object()))

    def test_is_pangram_returns_expected_bool(self):
        self.assertFalse(is_pangram('hello world'))
        self.assertTrue(is_pangram('The quick brown fox jumps over the lazy dog'))


class IsIsogramTestCase(TestCase):
    def test_non_string_objects_return_false(self):
        self.assertFalse(is_isogram(1))
        self.assertFalse(is_isogram(['xx']))
        self.assertFalse(is_isogram({}))
        self.assertFalse(is_isogram(False))
        self.assertFalse(is_isogram((1, 2, 3)))
        self.assertFalse(is_isogram(object()))

    def test_empty_strings_are_not_isograms(self):
        self.assertFalse(is_isogram(''))
        self.assertFalse(is_isogram(' '))
        self.assertFalse(is_isogram(' \n \t '))

    def test_is_isogram_returns_expected_bool(self):
        self.assertFalse(is_isogram('hello'))
        self.assertFalse(is_isogram('hello world, how are you?'))
        self.assertTrue(is_isogram('dermatoglyphics'))
        self.assertTrue(is_isogram('abcdefghilmnopqrs'))
