import binascii
import os
import random
from typing import Generator
from uuid import uuid4
import string

from string_utils import is_integer, roman_encode

__all__ = [
    'uuid',
    'random_string',
    'secure_random_hex',
    'roman_range',
]


def uuid(as_hex: bool = False) -> str:
    """
    Generated an UUID string (using `uuid.uuid4()`).

    *Example:*

    >>> uuid() # possible output: '97e3a716-6b33-4ab9-9bb1-8128cb24d76b'

    :param as_hex: True to return the hex value of the UUID, False to get its default representation (default).
    :return: uuid string.
    """
    uid = uuid4()

    if as_hex:
        return uid.hex

    return str(uid)


def random_string(size: int) -> str:
    """
    Returns a string of the specified size containing random characters (uppercase/lowercase ascii letters and digits).

    *Example:*

    >>> random_string(9) # possible output: "cx3QQbzYg"

    :param size: Desired string size
    :type size: int
    :return: Random string
    """
    if not is_integer(str(size)) or size < 1:
        raise ValueError('size must be >= 1')

    chars = string.ascii_letters + string.digits
    buffer = [random.choice(chars) for _ in range(size)]
    out = ''.join(buffer)

    return out


def secure_random_hex(byte_count: int) -> str:
    """
    Generates a random string using secure low level random generator (os.urandom).

    BEAR IN MIND: due to hex conversion, the returned string will have a size that is exactly\
    the double of the given `byte_count`.

    *Example:*

    >>> secure_random_hex(9) # possible output: 'aac4cf1d1d87bd5036'

    :param byte_count: Number of random bytes to generate
    :type byte_count: int
    :return: Hexadecimal string representation of generated random bytes
    """
    if not is_integer(str(byte_count)) or byte_count < 1:
        raise ValueError('byte_count must be >= 1')

    random_bytes = os.urandom(byte_count)
    hex_bytes = binascii.hexlify(random_bytes)
    hex_string = hex_bytes.decode()

    return hex_string


def roman_range(stop: int, start: int = 1, step: int = 1) -> Generator:
    """
    Similarly to native Python's `range()`, returns a Generator object which generates a new roman number
    on each iteration instead of an integer.

    *Example:*

    >>> for n in roman_range(7): print(n) # prints: I, II, III, IV, V, VI, VII

    :param stop: Number at which the generation must stop (must be <= 3999).
    :param start: Number at which the generation must start (must be >= 1).
    :param step: Increment of each generation step (default to 1).
    :return: Generator of roman numbers.
    """

    def validate(arg_value, arg_name):
        if not isinstance(arg_value, int) or (arg_value < 1 or arg_value > 3999):
            raise ValueError('"{}" must be an integer in the range 1-3999'.format(arg_name))

    def generate():
        current_step = start

        while current_step < stop + 1:
            yield roman_encode(current_step)
            current_step += step

    validate(stop, 'stop')
    validate(start, 'start')
    validate(step, 'step')

    return generate()
