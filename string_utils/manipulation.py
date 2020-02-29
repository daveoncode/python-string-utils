# -*- coding: utf-8 -*-

import base64
import random
import unicodedata
from typing import Union
from uuid import uuid4

__all__ = [
    'camel_case_to_snake',
    'snake_case_to_camel',
    'reverse',
    'shuffle',
    'strip_html',
    'prettify',
    'slugify',
    'booleanize',
    'strip_margin',
    'StringCompressor',
    'RomanNumbers',
]

import zlib

from ._regex import *
from .errors import InvalidInputError
from .validation import is_snake_case, is_full_string, is_camel_case, is_integer, is_string


def reverse(input_string: str) -> str:
    """
    Returns the string reversed ("abc" -> "cba").

    :param input_string: String to revert.
    :type input_string: str
    :return: Reversed string.
    :rtype: str
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    return input_string[::-1]


def camel_case_to_snake(input_string, separator='_'):
    """
    Convert a camel case string into a snake case one.
    (The original string is returned if is not a valid camel case string)

    :param input_string: String to convert.
    :type input_string: str
    :param separator: Sign to use as separator.
    :type separator: str
    :return: Converted string.
    :rtype: str
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    if not is_camel_case(input_string):
        return input_string

    return CAMEL_CASE_REPLACE_RE.sub(lambda m: m.group(1) + separator, input_string).lower()


def snake_case_to_camel(input_string: str, upper_case_first: bool = True, separator: str = '_') -> str:
    """
    Convert a snake case string into a camel case one.
    (The original string is returned if is not a valid snake case string)

    :param input_string: String to convert.
    :type input_string: str
    :param upper_case_first: True to turn the first letter into uppercase (default).
    :type upper_case_first: bool
    :param separator: Sign to use as separator (default to "_").
    :type separator: str
    :return: Converted string
    :rtype: str
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    if not is_snake_case(input_string, separator):
        return input_string

    tokens = [s.title() for s in input_string.split(separator) if is_full_string(s)]

    if not upper_case_first:
        tokens[0] = tokens[0].lower()

    out = ''.join(tokens)

    return out


def shuffle(input_string: str) -> str:
    """
    Return a new string containing shuffled items.

    :param input_string: String to shuffle
    :type input_string: str
    :return: Shuffled string
    :rtype: str
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    # turn the string into a list of chars
    chars = sorted(input_string)

    # shuffle the list
    random.shuffle(chars)

    # convert the shuffled list back to string
    return ''.join(chars)


def strip_html(input_string: str, keep_tag_content: bool = False) -> str:
    """
    Remove html code contained into the given string.

    :param input_string: String to manipulate.
    :type input_string: str
    :param keep_tag_content: True to preserve tag content, False to remove tag and its content too (default).
    :type keep_tag_content: bool
    :return: String with html removed.
    :rtype: str
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    r = HTML_TAG_ONLY_RE if keep_tag_content else HTML_RE

    return r.sub('', input_string)


def prettify(input_string: str) -> str:
    """
    Turns an ugly text string into a beautiful one by applying a regex pipeline which ensures the following:

    - String cannot start or end with spaces
    - String cannot have multiple sequential spaces, empty lines or punctuation (except for "?", "!" and ".")
    - Arithmetic operators (+, -, /, *, =) must have one, and only one space before and after themselves
    - The first letter after a dot, an exclamation or a question mark must be uppercase
    - One, and only one space should follow a dot, an exclamation or a question mark
    - Text inside double quotes cannot start or end with spaces, but one, and only one space must come first and \
    after quotes (foo" bar"baz -> foo "bar" baz)
    - Text inside round brackets cannot start or end with spaces, but one, and only one space must come first and \
    after brackets ("foo(bar )baz" -> "foo (bar) baz")
    - Percentage sign ("%") cannot be preceded by a space if there is a number before ("100 %" -> "100%")
    - Saxon genitive is correct ("Dave' s dog" -> "Dave's dog")

    :param input_string: String to manipulate
    :return: Prettified string.
    :rtype: str
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    def uppercase_first_char(regex_match):
        return regex_match.group(0).upper()

    def remove_duplicates(regex_match):
        return regex_match.group(1)[0]

    def uppercase_first_letter_after_sign(regex_match):
        match = regex_match.group(1)
        return match[:-1] + match[2].upper()

    def ensure_right_space_only(regex_match):
        return regex_match.group(1).strip() + ' '

    def ensure_left_space_only(regex_match):
        return ' ' + regex_match.group(1).strip()

    def ensure_spaces_around(regex_match):
        return ' ' + regex_match.group(1).strip() + ' '

    def remove_internal_spaces(regex_match):
        return regex_match.group(1).strip()

    def fix_saxon_genitive(regex_match):
        return regex_match.group(1).replace(' ', '') + ' '

    # generates a placeholder to inject temporary into the string, it will be replaced with the original
    # value at the end of the process
    def placeholder_key():
        return '$' + uuid4().hex + '$'

    # map of temporary placeholders
    placeholders = {}

    # looks for url or email and updates placeholders map with found values
    placeholders.update({placeholder_key(): m[0] for m in URLS_RE.findall(input_string)})
    placeholders.update({placeholder_key(): m for m in EMAILS_RE.findall(input_string)})

    # replace original value with the placeholder key
    for p in placeholders:
        input_string = input_string.replace(placeholders[p], p, 1)

    prettified = PRETTIFY_RE['UPPERCASE_FIRST_LETTER'].sub(uppercase_first_char, input_string)
    prettified = PRETTIFY_RE['DUPLICATES'].sub(remove_duplicates, prettified)
    prettified = PRETTIFY_RE['RIGHT_SPACE'].sub(ensure_right_space_only, prettified)
    prettified = PRETTIFY_RE['LEFT_SPACE'].sub(ensure_left_space_only, prettified)
    prettified = PRETTIFY_RE['SPACES_AROUND'].sub(ensure_spaces_around, prettified)
    prettified = PRETTIFY_RE['SPACES_INSIDE'].sub(remove_internal_spaces, prettified)
    prettified = PRETTIFY_RE['UPPERCASE_AFTER_SIGN'].sub(uppercase_first_letter_after_sign, prettified)
    prettified = PRETTIFY_RE['SAXON_GENITIVE'].sub(fix_saxon_genitive, prettified)
    prettified = prettified.strip()

    # restore placeholder keys with their associated original value
    for p in placeholders:
        prettified = prettified.replace(p, placeholders[p], 1)

    return prettified


def slugify(input_string: str, separator: str = '-') -> str:
    """
    Converts a string into a slug using provided separator.

    Example:

    >>> slugify(' This Is A "Test"! ') # returns: "this-is-a-test"

    :param input_string: String to convert.
    :type input_string: str
    :param separator: Sign used to join string tokens (default to "-").
    :type separator: str
    :return: Slugified string
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    # replace any character that is NOT letter or number with spaces
    s = NO_LETTERS_OR_NUMBERS_RE.sub(' ', input_string.lower()).strip()

    # replace spaces with join sign
    s = SPACES_RE.sub(separator, s)

    # normalize joins (remove duplicates)
    s = re.sub(re.escape(separator) + r'+', separator, s)

    # translate non-ascii signs
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')

    return s


def booleanize(input_string: str) -> bool:
    """
    Turns a string into a boolean based on its content (CASE INSENSITIVE).
    A positive boolean (True) is returned if the string value is one of the following:
    - "true"
    - "1"
    - "yes"
    - "y"
    Otherwise False is returned.

    Example:

    >>> booleanize('true') # returns True

    :param input_string: String to convert
    :return: True if the string contains a boolean-like positive value, false otherwise
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    return input_string.lower() in ('true', '1', 'yes', 'y')


def strip_margin(input_string: str) -> str:
    """
    Removes tab indentation from multi line strings (inspired by analogous Scala function).

    :param input_string: String to format
    :return: A string without left margins
    """
    if not is_string(input_string):
        raise InvalidInputError(input_string)

    line_separator = '\n'
    lines = [MARGIN_RE.sub('', line) for line in input_string.split(line_separator)]
    out = line_separator.join(lines)

    return out


class StringCompressor:

    @staticmethod
    def __require_valid_input_and_encoding(input_string: str, encoding: str):
        if not is_string(input_string):
            raise InvalidInputError(input_string)

        if len(input_string) == 0:
            raise ValueError('Input string cannot be empty')

        if not is_string(encoding):
            raise ValueError('Invalid encoding')

    @classmethod
    def compress(cls, input_string: str, encoding: str = 'utf-8', compression_level: int = 9) -> str:
        """
        Compress the given string by returning a shorter one that can be safely used in any context (like URL) and
        restored back to its original state using `StringCompressor.decompress()`.

        Besides the provided `compression_level`, the compression result (how much the string is actually compressed
        by resulting into a shorter string) depends on the amount and type of data contained inside the string.
        For instance, short strings might not provide a significant compression result or even be longer than the
        given input string (this is due to the fact that some bytes have to be embedded into the compressed string
        in order to be able to restore it later on).

        Behind the scenes this method makes use of the standard Python's zlib and base64 libraries.

        :param input_string: String to compress (must be not empty or a ValueError will be raised).
        :param encoding: String encoding (default to "utf-8").
        :param compression_level: A value between 0 (no compression) and 9 (best compression), default to 9.
        :return: Compressed string.
        """
        cls.__require_valid_input_and_encoding(input_string, encoding)

        if not is_integer(str(compression_level)) or compression_level < 0 or compression_level > 9:
            raise ValueError('Invalid compression_level: it must be an "int" between 0 and 9')

        # turns input string into a sequence of bytes using provided encoding
        original_bytes = input_string.encode(encoding)

        # compress bytes using zlib library
        compressed_bytes = zlib.compress(original_bytes, compression_level)

        # encode compressed bytes using base64
        # (this ensure that all characters will be available and that the output string can be used safely in any
        # context such URLs)
        encoded_bytes = base64.urlsafe_b64encode(compressed_bytes)

        # finally turns base64 bytes into a string
        output = encoded_bytes.decode(encoding)

        return output

    @classmethod
    def decompress(cls, input_string: str, encoding: str = 'utf-8') -> str:
        """
        Restore a previously compressed string (obtained using `StringCompressor.compress()`)
        back to its original state.

        :param input_string: String to restore.
        :param encoding: Original string encoding.
        :return: Decompressed string.
        """

        cls.__require_valid_input_and_encoding(input_string, encoding)

        # turns input string into a sequence of bytes
        # (the string is assumed to be a previously compressed string, therefore we have to decode it using base64)
        input_bytes = base64.urlsafe_b64decode(input_string)

        # decompress bytes using zlib
        decompressed_bytes = zlib.decompress(input_bytes)

        # decode the decompressed bytes to get the original string back
        original_string = decompressed_bytes.decode(encoding)

        return original_string


class RomanNumbers:
    # internal rule mappings for encode()
    __mappings = [
        # units
        {1: 'I', 5: 'V'},
        # tens
        {1: 'X', 5: 'L'},
        # hundreds
        {1: 'C', 5: 'D'},
        # thousands
        {1: 'M'},
    ]

    # swap key/value definitions for decode()
    __reversed_mappings = [{v: k for k, v in m.items()} for m in __mappings]

    @classmethod
    def __convert_digit(cls, index: int, value: int) -> str:
        # if digit is zero, there is no sign to display
        if value == 0:
            return ''

        if value < 9:
            # from 1 to 3 we have just to repeat the sign N times (eg: III, XXX...)
            if value <= 3:
                return cls.__mappings[index][1] * value

            # if 4 we have to add unit prefix
            if value == 4:
                return cls.__mappings[index][1] + cls.__mappings[index][5]

            # if is 5, is a straight map
            if value == 5:
                return cls.__mappings[index][5]

            # if 6, 7 or 8 we have to append unit suffixes
            suffix = cls.__mappings[index][1] * (value - 5)
            return cls.__mappings[index][5] + suffix

        # if 9 we have to prepend current unit to next
        return cls.__mappings[index][1] + cls.__mappings[index + 1][1]

    @classmethod
    def encode(cls, input_number: Union[str, int]) -> str:
        """
        Convert the given number/string into a roman number.
        The passed input must represents a positive integer in the range 1-3999 (inclusive).

        Why this limit? You may be wondering:

        1. zero is forbidden since there is no related representation in roman numbers
        2. the upper bound 3999 is due to the limitation in the ascii charset
        (the higher quantity sign displayable in ascii is "M" which is equal to 1000, therefore based on
        roman numbers rules we can use 3 times M to reach 3000 but we can't go any further in thousands without
        special "boxed chars").

        :param input_number: An integer or a string to be converted.
        :return: Roman number string.
        """

        # force input conversion to a string (we need it in order to iterate on each digit)
        input_string = str(input_number)

        if not is_integer(input_string):
            raise ValueError('Invalid input, only strings or integers are allowed')

        value = int(input_string)

        if value < 1 or value > 3999:
            raise ValueError('Input must be >= 1 and <= 3999')

        # turns the given number into a sequence of integers (eg. from 1256 to [1, 2, 5, 6])
        int_tokens = [int(v) for v in input_string]

        # flip tokens in order to start from units first, then go up to tens, hundreds and thousands
        reversed_int_tokens = list(reversed(int_tokens))

        # for each token obtain the relative roman string representation
        converted_tokens = [cls.__convert_digit(i, v) for i, v in enumerate(reversed_int_tokens)]

        # flip back tokens in order to have them placed correctly
        # (units on the right then tens, hundreds, thousands on the left)
        sorted_tokens = list(reversed(converted_tokens))

        # final output string
        output = ''.join(sorted_tokens)

        return output

    @classmethod
    def __index_for_sign(cls, sign: str) -> int:
        for index, mapping in enumerate(cls.__reversed_mappings):
            if sign in mapping:
                return index

        raise ValueError('Invalid token found: "{}"'.format(sign))

    @classmethod
    def decode(cls, input_string: str) -> int:
        """
        Decode a roman number string into an integer if the provided string is valid.

        :param input_string: (Assumed) Roman number
        :return: Integer value
        """

        if not is_full_string(input_string):
            raise ValueError('Input must be a non empty string')

        # reverse the provided string so that we can start parsing from units to thousands
        reversed_string = reverse(input_string.upper())

        # track last used value
        last_value = None

        # computed number to return
        output = 0

        # for each sign in the string we get its numeric value and add or subtract it to the computed output
        for sign in reversed_string:
            # are we dealing with units, tens, hundreds or thousands?
            index = cls.__index_for_sign(sign)

            # it's basically 1 or 5 (based on mapping rules definitions)
            key_value = cls.__reversed_mappings[index][sign]

            # Based on the level (tens, hundreds...) we have to add as many zeroes as the level into which we are
            # in order to have the actual sign value.
            # For instance, if we are at level 2 we are dealing with hundreds, therefore instead of 1 or 5, we will
            # obtain 100 or 500 by adding 2 zeroes
            sign_value = int(str(key_value) + '0' * index)

            # increase total value if we are moving on with level
            if last_value is None or sign_value >= last_value:
                output += sign_value

            # Decrease value if we are back to a previous level
            # For instance, if we are parsing "IX", we first encounter "X" which is ten then "I" which is unit,
            # So we have to do the following operation in order to get 9 (the final result): 10 - 1
            else:
                output -= sign_value

            last_value = sign_value

        return output
