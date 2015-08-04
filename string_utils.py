# -*- coding: utf-8 -*-

import json
import re
from uuid import uuid4
import random

# module settings
__version__ = '0.2.0'
__all__ = [
    'is_string',
    'is_url',
    'is_email',
    'is_credit_card',
    'is_camel_case',
    'is_snake_case',
    'is_json',
    'is_uuid',
    'is_ip',
    'words_count',
    'camel_case_to_snake',
    'snake_case_to_camel',
    'reverse',
    'uuid',
    'shuffle',
]

# compiled regex
URL_RE = re.compile(
    r'^'
    r'([a-z-]+://)'  # scheme
    r'([a-z_\d-]+:[a-z_\d-]+@)?'  # user:password
    r'(www\.)?'  # www.
    r'((?<!\.)[a-z\d\.-]+\.[a-z]{2,6}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|localhost)'  # domain
    r'(:\d{2,})?'  # port number
    r'(/[a-z\d_%\+-]*)*'  # folders
    r'(\.[a-z\d_%\+-]+)*'  # file extension
    r'(\?[a-z\d_\+%-=]*)?'  # query string
    r'(#\S*)?'  # hash
    r'$',
    re.IGNORECASE
)
EMAIL_RE = re.compile(r'^[a-zA-Z\d\._\+-]+@([a-z\d-]+\.?[a-z\d-]+)+\.[a-z]{2,4}$')
CAMEL_CASE_TEST_RE = re.compile(r'^[a-zA-Z]*([a-z]+[A-Z]+|[A-Z]+[a-z]+)[a-zA-Z\d]*$')
CAMEL_CASE_REPLACE_RE = re.compile(r'([a-z]|[A-Z]+)(?=[A-Z])')
SNAKE_CASE_TEST_RE = re.compile(r'^[a-z]+([a-z\d]+_|_[a-z\d]+)+[a-z\d]+$')
SNAKE_CASE_TEST_DASH_RE = re.compile(r'^[a-z]+([a-z\d]+-|-[a-z\d]+)+[a-z\d]+$')
SNAKE_CASE_REPLACE_RE = re.compile(r'(_)([a-z\d])')
SNAKE_CASE_REPLACE_DASH_RE = re.compile('(-)([a-z\d])')
CREDIT_CARDS = {
    'VISA': re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$'),
    'MASTERCARD': re.compile(r'^5[1-5][0-9]{14}$'),
    'AMERICAN_EXPRESS': re.compile(r'^3[47][0-9]{13}$'),
    'DINERS_CLUB': re.compile(r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$'),
    'DISCOVER': re.compile(r'^6(?:011|5[0-9]{2})[0-9]{12}$'),
    'JCB': re.compile(r'^(?:2131|1800|35\d{3})\d{11}$')
}
JSON_WRAPPER_RE = re.compile(r'^\s*\{\s*(.|\s)*\s*\}\s*$', re.MULTILINE)
UUID_RE = re.compile(r'^[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12}$', re.IGNORECASE)
IP_RE = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
WORDS_COUNT_RE = re.compile(r'\W*[^\W_]+\W*', re.IGNORECASE | re.MULTILINE | re.UNICODE)


# string checking functions


def is_string(obj):
    """
    Checks if an object is a string.

    :param obj: Object to test.
    :return: True if string, false otherwise.
    :rtype: bool
    """
    try:  # basestring is available in python 2 but missing in python 3!
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)


# Full url example:
# scheme://username:password@www.domain.com:8042/folder/subfolder/file.extension?param=value&param2=value2#hash
def is_url(string, allowed_schemes=None):
    """
    Check if a string is a valid url.

    :param string: String to check.
    :param allowed_schemes: List of valid schemes ('http', 'https', 'ftp'...). Default to None (any scheme is valid).
    :return: True if url, false otherwise
    :rtype: bool
    """
    try:
        valid = bool(URL_RE.match(string))
    except TypeError:
        return False
    if allowed_schemes:
        return valid and any([string.startswith(s) for s in allowed_schemes])
    return valid


def is_email(string):
    """
    Check if a string is an email.

    | **IMPORTANT NOTES**:
    | By design, the implementation of this checking does not follow the specification for a valid \
    email address, but instead it's based on real world cases in order to match more than 99% \
    of emails and catch user mistakes. For example the percentage sign "%" is a valid sign for an email, \
    but actually no one use it, instead if such sign is found in a string coming from user input (like a \
    web form) is very likely that the intention was to type "5" (which is on the same key on a US keyboard).

    | You can take a look at "**IsEmailTestCase**" in tests.py for further details.


    :param string: String to check.
    :type string: str
    :return: True if email, false otherwise.
    :rtype: bool
    """
    try:
        return bool(EMAIL_RE.match(string))
    except TypeError:
        return False


def is_credit_card(string, card_type=None):
    """
    Checks if a string is a valid credit card number.
    If card type is provided then it checks that specific type,
    otherwise any known credit card number will be accepted.

    :param string: String to check.
    :type string: str
    :param card_type: Card type.
    :type card_type: str

    Can be one of these:

    * VISA
    * MASTERCARD
    * AMERICAN_EXPRESS
    * DINERS_CLUB
    * DISCOVER
    * JCB

    or None. Default to None (any card).

    :return: True if credit card, false otherwise.
    :rtype: bool
    """
    try:
        if card_type:
            if card_type not in CREDIT_CARDS:
                raise KeyError(
                    'Invalid card type "%s". Valid types are: %s' % (card_type, ', '.join(CREDIT_CARDS.keys()))
                )
            return bool(CREDIT_CARDS[card_type].match(string))
        for c in CREDIT_CARDS:
            if CREDIT_CARDS[c].match(string):
                return True
    except TypeError:
        return False
    return False


def is_camel_case(string):
    """
    Checks if a string is formatted as camel case.
    A string is considered camel case when:

    - it's composed only by letters ([a-zA-Z]) and optionally numbers ([0-9])
    - it contains both lowercase and uppercase letters
    - it does not start with a number


    :param string: String to test.
    :type string: str
    :return: True for a camel case string, false otherwise.
    :rtype: bool
    """
    try:
        return bool(CAMEL_CASE_TEST_RE.match(string))
    except TypeError:
        return False


def is_snake_case(string, separator='_'):
    """
    Checks if a string is formatted as snake case.
    A string is considered snake case when:

    * it's composed only by lowercase letters ([a-z]), underscores (or provided separator) \
    and optionally numbers ([0-9])
    * it does not start/end with an underscore (or provided separator)
    * it does not start with a number


    :param string: String to test.
    :type string: str
    :param separator: String to use as separator.
    :type separator: str
    :return: True for a snake case string, false otherwise.
    :rtype: bool
    """
    re_map = {
        '_': SNAKE_CASE_TEST_RE,
        '-': SNAKE_CASE_TEST_DASH_RE
    }
    re_template = '^[a-z]+([a-z\d]+{sign}|{sign}[a-z\d]+)+[a-z\d]+$'
    r = re_map.get(separator, re.compile(re_template.format(sign=re.escape(separator))))
    try:
        return bool(r.match(string))
    except TypeError:
        return False


def is_json(string):
    """
    Check if a string is a valid json.

    :param string: String to check.
    :type string: str
    :return: True if json, false otherwise
    :rtype: bool
    """
    s = str(string)
    if bool(JSON_WRAPPER_RE.match(s)):
        try:
            return isinstance(json.loads(s), dict)
        except (TypeError, ValueError, OverflowError):
            return False
    return False


def is_uuid(string):
    """
    Check if a string is a valid UUID.

    :param string: String to check.
    :type string: str
    :return: True if UUID, false otherwise
    :rtype: bool
    """
    return bool(UUID_RE.match(str(string)))


def is_ip(string):
    """
    Checks if a string is a valid ip.

    :param string: String to check.
    :type string: str
    :return: True if an ip, false otherwise.
    :rtype: bool
    """
    try:
        return bool(IP_RE.match(string))
    except TypeError:
        return False


def words_count(string):
    """
    Returns the number of words contained into the given string.

    This method is smart, it does consider only sequence of one or more letter and/or numbers
    as "words", so a string like this: "! @ # % ... []" will return zero!
    Moreover it is aware of punctuation, so the count for a string like "one,two,three.stop"
    will be 4 not 1 (even if there are no spaces in the string).

    :param string: String to check.
    :type string: str
    :return: Number of words.
    :rtype: int
    """
    return len(WORDS_COUNT_RE.findall(string))


# string manipulation functions

def reverse(string):
    """
    Returns the string reversed ("abc" -> "cba").

    :param string: String to revert.
    :type string: str
    :return: Reversed string.
    :rtype: str
    """
    return ''.join(list(reversed(string)))


def camel_case_to_snake(string, separator='_'):
    """
    Convert a camel case string into a snake case one.
    (The original string is returned if is not a valid camel case string)

    :param string: String to convert.
    :type string: str
    :param separator: Sign to use as separator.
    :type separator: str
    :return: Converted string.
    :rtype: str
    """
    if not is_string(string):
        raise TypeError('Expected string')
    if not is_camel_case(string):
        return string
    return CAMEL_CASE_REPLACE_RE.sub(lambda m: m.group(1) + separator, string).lower()


def snake_case_to_camel(string, upper_case_first=True, separator='_'):
    """
    Convert a snake case string into a camel case one.
    (The original string is returned if is not a valid snake case string)

    :param string: String to convert.
    :type string: str
    :param upper_case_first: True to turn the first letter into uppercase (default).
    :type upper_case_first: bool
    :param separator: Sign to use as separator (default to "_").
    :type separator: str
    :return: Converted string
    :rtype: str
    """
    if not is_string(string):
        raise TypeError('Expected string')
    if not is_snake_case(string, separator):
        return string
    re_map = {
        '_': SNAKE_CASE_REPLACE_RE,
        '-': SNAKE_CASE_REPLACE_DASH_RE
    }
    r = re_map.get(separator, re.compile('({sign})([a-z\d])'.format(sign=re.escape(separator))))
    string = r.sub(lambda m: m.group(2).upper(), string)
    if upper_case_first:
        return string[0].upper() + string[1:]
    return string


def uuid():
    """
    Generated an UUID string (using uuid.uuid4()).

    :return: uuid string.
    :rtype: str
    """
    return str(uuid4())


def shuffle(string):
    """
    Return a new string containing shuffled items.

    :param string: String to shuffle
    :type string: str
    :return: Shuffled string
    :rtype: str
    """
    s = sorted(string)  # turn the string into a list of chars
    random.shuffle(s)  # shuffle the list
    return ''.join(s)  # convert the shuffled list back to string
