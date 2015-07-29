import re

# module settings
__version__ = '0.0.0'
__all__ = [
    'is_url',
    'is_email',
    'is_credit_card',
    'is_camel_case',
    'is_snake_case',
    'camel_case_to_snake',
    'snake_case_to_camel',
    'reverse',
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
EMAIL_RE = re.compile('^[a-zA-Z\d\._\+-]+@([a-z\d-]+\.?[a-z\d-]+)+\.[a-z]{2,4}$')
CAMEL_CASE_TEST_RE = re.compile('^[a-zA-Z]*([a-z]+[A-Z]+|[A-Z]+[a-z]+)[a-zA-Z\d]*$')
CAMEL_CASE_REPLACE_RE = re.compile('([a-z]|[A-Z]+)(?=[A-Z])')
SNAKE_CASE_TEST_RE = re.compile('^[a-z]+([a-z\d]+_|_[a-z\d]+)+[a-z\d]+$')
SNAKE_CASE_TEST_DASH_RE = re.compile('^[a-z]+([a-z\d]+-|-[a-z\d]+)+[a-z\d]+$')
SNAKE_CASE_REPLACE_RE = re.compile('(_)([a-z\d])')
SNAKE_CASE_REPLACE_DASH_RE = re.compile('(-)([a-z\d])')
CREDIT_CARDS = {
    'VISA': re.compile('^4[0-9]{12}(?:[0-9]{3})?$'),
    'MASTERCARD': re.compile('^5[1-5][0-9]{14}$'),
    'AMERICAN_EXPRESS': re.compile('^3[47][0-9]{13}$'),
    'DINERS_CLUB': re.compile('^3(?:0[0-5]|[68][0-9])[0-9]{11}$'),
    'DISCOVER': re.compile('^6(?:011|5[0-9]{2})[0-9]{12}$'),
    'JCB': re.compile('^(?:2131|1800|35\d{3})\d{11}$')
}


# string checking functions


# scheme://username:password@www.domain.com:8042/folder/subfolder/file.extension?param=value&param2=value2#hash
def is_url(string, allowed_schemes=None):
    valid = bool(URL_RE.match(string))
    if allowed_schemes:
        return valid and any([string.startswith(s) for s in allowed_schemes])
    return valid


def is_email(string):
    """
    Returns true if the string is a valid email.
    IMPORTANT NOTES:
    By design, the implementation of this checking does not follow the specification for a valid
    email address, but instead it's based on real world cases in order to match more than 99%
    of emails and catch user mistakes. For example the percentage sign "%" is a valid sign for an email,
    but actually no one use it, instead if such sign is found in a string coming from user input (like a
    web form) is very likely that the intention was to type "5" (which is on the same key on a US keyboard).
    You can take a look at "IsEmailTestCase" in tests.py for further details.

    :param string: String to check
    :return: True if email, false otherwise
    """
    return bool(EMAIL_RE.match(string))


def is_credit_card(string, card_type=None):
    """
    Checks if a string is a valid credit card number.
    If card type is provided then it checks that specific type,
    otherwise any known credit card number will be accepted.

    :param string: String to check.
    :param card_type: Card type (can be: 'VISA', 'MASTERCARD', 'AMERICAN_EXPRESS', 'DINERS_CLUB', 'DISCOVER', 'JCB'
    or None). Default to None (any card).
    :return: :raise KeyError:
    """
    if card_type:
        if card_type not in CREDIT_CARDS:
            raise KeyError(
                'Invalid card type "%s". Valid types are: %s' % (card_type, ', '.join(CREDIT_CARDS.keys()))
            )
        return bool(CREDIT_CARDS[card_type].match(string))
    for c in CREDIT_CARDS:
        if CREDIT_CARDS[c].match(string):
            return True
    return False


def is_camel_case(string):
    """
    Checks if a string is formatted as camel case.
    A string is considered camel case when:
    - its composed only by letters ([a-zA-Z]) and optionally numbers ([0-9])
    - it contains both lowercase and uppercase letters
    - it does not start with a number

    :param string: String to test.
    :return: True for a camel case string, false otherwise.
    """
    return bool(CAMEL_CASE_TEST_RE.match(string))


def is_snake_case(string, separator='_'):
    """
    Checks if a string is formatted as snake case.
    A string is considered snake case when:
    - its composed only by lowercase letters ([a-z]), underscores (or provided separator) and
    optionally numbers ([0-9])
    - it does not start/end with an underscore (or provided separator)
    - it does not start with a number

    :param string: String to test.
    :return: True for a snake case string, false otherwise.
    """
    re_map = {
        '_': SNAKE_CASE_TEST_RE,
        '-': SNAKE_CASE_TEST_DASH_RE
    }
    re_template = '^[a-z]+([a-z\d]+{sign}|{sign}[a-z\d]+)+[a-z\d]+$'
    r = re_map.get(separator, re.compile(re_template.format(sign=re.escape(separator))))
    return bool(r.match(string))


# string manipulation functions

def reverse(string):
    """
    Returns the string reversed ("abc" -> "cba").

    :param string: String to revert.
    :return: Reversed string.
    """
    return ''.join(list(reversed(string)))


# def shuffle(string):
#     pass
#
#
# def is_multiline(string):
#     pass
#
# def is_zip_code(string, country_code=None):
#     pass


def camel_case_to_snake(string, separator='_'):
    """
    Convert a camel case string into a snake case one.
    (The original string is returned if is not a valid camel case string)

    :param string: String to convert.
    :param separator: Sign to use as separator.
    :return: Converted string
    """
    if not is_camel_case(string):
        return string
    return CAMEL_CASE_REPLACE_RE.sub(lambda m: m.group(1) + separator, string).lower()


def snake_case_to_camel(string, upper_case_first=True, separator='_'):
    """
    Convert a snake case string into a camel case one.
    (The original string is returned if is not a valid snake case string)

    :param string: String to convert.
    :param upper_case_first: True to turn the first letter into uppercase (default).
    :param separator: Sign to use as separator (default to "_").
    :return: Converted string
    """
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
