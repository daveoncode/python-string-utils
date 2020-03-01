# -*- coding: utf-8 -*-

import json
import string
from typing import Any, Optional, List

__all__ = [
    'is_string',
    'is_number',
    'is_integer',
    'is_decimal',
    'is_full_string',
    'is_url',
    'is_email',
    'is_credit_card',
    'is_camel_case',
    'is_snake_case',
    'is_json',
    'is_uuid',
    'is_ip_v4',
    'is_ip_v6',
    'is_ip',
    'is_palindrome',
    'is_pangram',
    'is_isogram',
    'is_slug',
    'contains_html',
    'words_count',
]

from ._regex import *
from string_utils.errors import InvalidInputError


def is_string(obj: Any) -> bool:
    """
    Checks if an object is a string.

    :param obj: Object to test.
    :return: True if string, false otherwise.
    """
    return isinstance(obj, str)


def is_full_string(input_string: Any) -> bool:
    """
    Check if a string is not empty (it must contains at least one non space character).

    *Examples:*

    >>> is_full_string(None) # returns false
    >>> is_full_string('') # returns false
    >>> is_full_string(' ') # returns false
    >>> is_full_string('hello') # returns true

    :param input_string: String to check.
    :type input_string: str
    :return: True if not empty, false otherwise.
    """
    return is_string(input_string) and input_string.strip() != ''


def is_number(input_string: str) -> bool:
    """
    Checks if a string is a valid number.

    The number can be a signed (eg: +1, -2, -3.3) or unsigned (eg: 1, 2, 3.3) integer or double
    or use the "scientific notation" (eg: 1e5).

    *Examples:*

    >>> is_number('42') # returns true
    >>> is_number('19.99') # returns true
    >>> is_number('-9.12') # returns true
    >>> is_number('1e3') # returns true
    >>> is_number('1 2 3') # returns false

    :param input_string: String to check
    :type input_string: str
    :return: True if the string represents a number, false otherwise
    """
    if not isinstance(input_string, str):
        raise InvalidInputError(input_string)

    return NUMBER_RE.match(input_string) is not None


def is_integer(input_string: str) -> bool:
    """
    Checks whether the given string represents an integer or not.

    An integer may be signed or unsigned or use a "scientific notation".

    *Examples:*

    >>> is_integer('42') # returns true
    >>> is_integer('42.0') # returns false

    :param input_string: String to check
    :type input_string: str
    :return: True if integer, false otherwise
    """
    return is_number(input_string) and '.' not in input_string


def is_decimal(input_string: str) -> bool:
    """
    Checks whether the given string represents a decimal or not.

    A decimal may be signed or unsigned or use a "scientific notation".

    >>> is_decimal('42.0') # returns true
    >>> is_decimal('42') # returns false

    :param input_string: String to check
    :type input_string: str
    :return: True if integer, false otherwise
    """
    return is_number(input_string) and '.' in input_string


# Full url example:
# scheme://username:password@www.domain.com:8042/folder/subfolder/file.extension?param=value&param2=value2#hash
def is_url(input_string: Any, allowed_schemes: Optional[List[str]] = None) -> bool:
    """
    Check if a string is a valid url.

    *Examples:*

    >>> is_url('http://www.mysite.com') # returns true
    >>> is_url('https://mysite.com') # returns true
    >>> is_url('.mysite.com') # returns false

    :param input_string: String to check.
    :type input_string: str
    :param allowed_schemes: List of valid schemes ('http', 'https', 'ftp'...). Default to None (any scheme is valid).
    :type allowed_schemes: Optional[List[str]]
    :return: True if url, false otherwise
    """
    if not is_full_string(input_string):
        return False

    valid = URL_RE.match(input_string) is not None

    if allowed_schemes:
        return valid and any([input_string.startswith(s) for s in allowed_schemes])

    return valid


def is_email(input_string: Any) -> bool:
    """
    Check if a string is an email.

    By design, the implementation of this checking does not follow the specification for a valid \
    email address, but instead it's based on real world cases in order to match more than 99% \
    of emails and catch user mistakes. For example the percentage sign "%" is a valid sign for an email, \
    but actually no one use it, instead if such sign is found in a string coming from user input (like a \
    web form) is very likely that the intention was to type "5" (which is on the same key on a US keyboard).

    *Examples:*

    >>> is_email('my.email@the-provider.com') # returns true
    >>> is_email('@gmail.com') # returns false

    :param input_string: String to check.
    :type input_string: str
    :return: True if email, false otherwise.
    """
    return is_full_string(input_string) and EMAIL_RE.match(input_string) is not None


def is_credit_card(input_string: Any, card_type: str = None) -> bool:
    """
    Checks if a string is a valid credit card number.
    If card type is provided then it checks that specific type,
    otherwise any known credit card number will be accepted.

    :param input_string: String to check.
    :type input_string: str
    :param card_type: Card type. Can be one of these:

    * VISA
    * MASTERCARD
    * AMERICAN_EXPRESS
    * DINERS_CLUB
    * DISCOVER
    * JCB

    or None. Default to None (any card).

    :type card_type: str

    :return: True if credit card, false otherwise.
    """
    if not is_full_string(input_string):
        return False

    if card_type:
        if card_type not in CREDIT_CARDS:
            raise KeyError(
                'Invalid card type "{}". Valid types are: {}'.format(card_type, ', '.join(CREDIT_CARDS.keys()))
            )
        return CREDIT_CARDS[card_type].match(input_string) is not None

    for c in CREDIT_CARDS:
        if CREDIT_CARDS[c].match(input_string) is not None:
            return True

    return False


def is_camel_case(input_string: Any) -> bool:
    """
    Checks if a string is formatted as camel case.

    A string is considered camel case when:

    - it's composed only by letters ([a-zA-Z]) and optionally numbers ([0-9])
    - it contains both lowercase and uppercase letters
    - it does not start with a number

    *Examples:*

    >>> is_camel_case('MyString') # returns true
    >>> is_camel_case('mystring') # returns false

    :param input_string: String to test.
    :type input_string: str
    :return: True for a camel case string, false otherwise.
    """
    return is_full_string(input_string) and CAMEL_CASE_TEST_RE.match(input_string) is not None


def is_snake_case(input_string: Any, separator: str = '_') -> bool:
    """
    Checks if a string is formatted as "snake case".

    A string is considered snake case when:

    * it's composed only by lowercase letters ([a-z]), underscores (or provided separator) \
    and optionally numbers ([0-9])
    * it does not start/end with an underscore (or provided separator)
    * it does not start with a number

    *Examples:*

    >>> is_snake_case('foo_bar_baz') # returns true
    >>> is_snake_case('foo') # returns false

    :param input_string: String to test.
    :type input_string: str
    :param separator: String to use as separator.
    :type separator: str
    :return: True for a snake case string, false otherwise.
    """
    if is_full_string(input_string):
        re_map = {
            '_': SNAKE_CASE_TEST_RE,
            '-': SNAKE_CASE_TEST_DASH_RE
        }
        re_template = r'([a-z]+\d*{sign}[a-z\d{sign}]*|{sign}+[a-z\d]+[a-z\d{sign}]*)'
        r = re_map.get(
            separator,
            re.compile(re_template.format(sign=re.escape(separator)), re.IGNORECASE)
        )

        return r.match(input_string) is not None

    return False


def is_json(input_string: Any) -> bool:
    """
    Check if a string is a valid json.

    *Examples:*

    >>> is_json('{"name": "Peter"}') # returns true
    >>> is_json('[1, 2, 3]') # returns true
    >>> is_json('{nope}') # returns false

    :param input_string: String to check.
    :type input_string: str
    :return: True if json, false otherwise
    """
    if is_full_string(input_string) and JSON_WRAPPER_RE.match(input_string) is not None:
        try:
            return isinstance(json.loads(input_string), (dict, list))
        except (TypeError, ValueError, OverflowError):
            pass

    return False


def is_uuid(input_string: Any, allow_hex: bool = False) -> bool:
    """
    Check if a string is a valid UUID.

    *Example:*

    >>> is_uuid('6f8aa2f9-686c-4ac3-8766-5712354a04cf') # returns true
    >>> is_uuid('6f8aa2f9686c4ac387665712354a04cf') # returns false
    >>> is_uuid('6f8aa2f9686c4ac387665712354a04cf', allow_hex=True) # returns true

    :param input_string: String to check.
    :type input_string: str
    :param allow_hex: True to allow UUID hex representation as valid, false otherwise (default)
    :type allow_hex: bool
    :return: True if UUID, false otherwise
    """
    # string casting is used to allow UUID itself as input data type
    s = str(input_string)

    if allow_hex:
        return UUID_HEX_OK_RE.match(s) is not None

    return UUID_RE.match(s) is not None


def is_ip_v4(input_string: Any) -> bool:
    """
    Checks if a string is a valid ip v4.

    *Examples:*

    >>> is_ip_v4('255.200.100.75') # returns true
    >>> is_ip_v4('nope') # returns false (not an ip)
    >>> is_ip_v4('255.200.100.999') # returns false (999 is out of range)

    :param input_string: String to check.
    :type input_string: str
    :return: True if an ip v4, false otherwise.
    """
    if not is_full_string(input_string) or SHALLOW_IP_V4_RE.match(input_string) is None:
        return False

    # checks that each entry in the ip is in the valid range (0 to 255)
    for token in input_string.split('.'):
        if not (0 <= int(token) <= 255):
            return False

    return True


def is_ip_v6(input_string: Any) -> bool:
    """
    Checks if a string is a valid ip v6.

    *Examples:*

    >>> is_ip_v6('2001:db8:85a3:0000:0000:8a2e:370:7334') # returns true
    >>> is_ip_v6('2001:db8:85a3:0000:0000:8a2e:370:?') # returns false (invalid "?")

    :param input_string: String to check.
    :type input_string: str
    :return: True if a v6 ip, false otherwise.
    """
    return is_full_string(input_string) and IP_V6_RE.match(input_string) is not None


def is_ip(input_string: Any) -> bool:
    """
    Checks if a string is a valid ip (either v4 or v6).

    *Examples:*

    >>> is_ip('255.200.100.75') # returns true
    >>> is_ip('2001:db8:85a3:0000:0000:8a2e:370:7334') # returns true
    >>> is_ip('1.2.3') # returns false

    :param input_string: String to check.
    :type input_string: str
    :return: True if an ip, false otherwise.
    """
    return is_ip_v6(input_string) or is_ip_v4(input_string)


def is_palindrome(input_string: Any, strict: bool = True) -> bool:
    """
    Checks if the string is a palindrome (https://en.wikipedia.org/wiki/Palindrome).

    :param input_string: String to check.
    :type input_string: str
    :param strict: True if white spaces matter (default), false otherwise.
    :type strict: bool
    :return: True if the string is a palindrome (like "otto", or "i topi non avevano nipoti" if strict=False),\
    False otherwise
    """
    if is_full_string(input_string):
        if strict:
            string_len = len(input_string)

            # Traverse the string one char at step, and for each step compares the
            # "head_char" (the one on the left of the string) to the "tail_char" (the one on the right).
            # In this way we avoid to manipulate the whole string in advance if not necessary and provide a faster
            # algorithm which can scale very well for long strings.
            for index in range(string_len):
                head_char = input_string[index]
                tail_char = input_string[string_len - index - 1]

                if head_char != tail_char:
                    return False

            return True

        return is_palindrome(SPACES_RE.sub('', input_string))

    return False


def is_pangram(input_string: Any) -> bool:
    """
    Checks if the string is a pangram (https://en.wikipedia.org/wiki/Pangram).

    :param input_string: String to check.
    :type input_string: str
    :return: True if the string is a pangram, False otherwise.
    """
    if not is_full_string(input_string):
        return False

    return set(SPACES_RE.sub('', input_string)).issuperset(set(string.ascii_lowercase))


def is_isogram(input_string: Any) -> bool:
    """
    Checks if the string is an isogram (https://en.wikipedia.org/wiki/Isogram).

    :param input_string: String to check.
    :type input_string: str
    :return: True if isogram, false otherwise.
    """
    return is_full_string(input_string) and len(set(input_string)) == len(input_string)


def is_slug(input_string: Any, sign: str = '-') -> bool:
    """
    Checks if a given string is a slug.

    :param input_string: String to check.
    :type input_string: str
    :param sign: Join sign used by the slug.
    :type sign: str
    :return: True if slug, false otherwise.
    """
    if not is_full_string(input_string):
        return False

    rex = r'^([a-z\d]+' + re.escape(sign) + r'?)*[a-z\d]$'

    return re.match(rex, input_string) is not None


def contains_html(input_string: str) -> bool:
    """
    Checks if the given string contains html code.
    By design, this function is very permissive regarding what to consider html code, don't expect to use it
    as an html validator, its goal is to detect "malicious" or undesired html tags in the text.

    :param input_string: Text to check
    :type input_string: str
    :return: True if string contains html, false otherwise.
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    return HTML_RE.search(input_string) is not None


def words_count(input_string: str) -> int:
    """
    Returns the number of words contained into the given string.

    This method is smart, it does consider only sequence of one or more letter and/or numbers
    as "words", so a string like this: "! @ # % ... []" will return zero!
    Moreover it is aware of punctuation, so the count for a string like "one,two,three.stop"
    will be 4 not 1 (even if there are no spaces in the string).

    :param input_string: String to check.
    :type input_string: str
    :return: Number of words.
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    return len(WORDS_COUNT_RE.findall(input_string))
