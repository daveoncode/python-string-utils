from unittest.case import TestCase

from string_utils import *


class IsUrlTestCase(TestCase):
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: is_url(None))
        self.assertRaises(TypeError, lambda: is_url(False))
        self.assertRaises(TypeError, lambda: is_url(0))
        self.assertRaises(TypeError, lambda: is_url([]))
        self.assertRaises(TypeError, lambda: is_url({'a': 1}))

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
        self.assertTrue(is_url('https://site.com'))
        self.assertTrue(is_url('ftp://site.com'))
        self.assertTrue(is_url('git://site.com'))

    def test_should_restrict_checking_on_provided_schemes(self):
        self.assertTrue(is_url('git://site.com'))
        self.assertFalse(is_url('git://site.com', allowed_schemes=['http', 'https']))

    def test_url_cannot_start_with_dot(self):
        self.assertTrue(is_url('http://.site.com'))

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
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: is_email(None))
        self.assertRaises(TypeError, lambda: is_email(False))
        self.assertRaises(TypeError, lambda: is_email(0))
        self.assertRaises(TypeError, lambda: is_email([]))
        self.assertRaises(TypeError, lambda: is_email({'a': 1}))

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

    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: is_credit_card(None))
        self.assertRaises(TypeError, lambda: is_credit_card(False))
        self.assertRaises(TypeError, lambda: is_credit_card(0))
        self.assertRaises(TypeError, lambda: is_credit_card([]))
        self.assertRaises(TypeError, lambda: is_credit_card({'a': 1}))

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
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: is_camel_case(None))
        self.assertRaises(TypeError, lambda: is_camel_case(False))
        self.assertRaises(TypeError, lambda: is_camel_case(0))
        self.assertRaises(TypeError, lambda: is_camel_case([]))
        self.assertRaises(TypeError, lambda: is_camel_case({'a': 1}))

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
    def test_cannot_handle_non_string_objects(self):
        self.assertRaises(TypeError, lambda: is_snake_case(None))
        self.assertRaises(TypeError, lambda: is_snake_case(False))
        self.assertRaises(TypeError, lambda: is_snake_case(0))
        self.assertRaises(TypeError, lambda: is_snake_case([]))
        self.assertRaises(TypeError, lambda: is_snake_case({'a': 1}))

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


class ReverseTestCase(TestCase):
    def test_returns_original_string_if_unreversable(self):
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
