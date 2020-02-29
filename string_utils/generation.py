import binascii
import os
import random
from uuid import uuid4
import string

from string_utils import is_integer

__all__ = [
    'uuid',
    'random_string',
    'secure_random_hex',
]


def uuid() -> str:
    """
    Generated an UUID string (using `uuid.uuid4()`).

    :return: uuid string.
    """
    return str(uuid4())


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
