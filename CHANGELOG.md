# Python String Utils Changelog

## v1.0.0 (March 2020)

### Project reboot:

I've started this project back in 2015, then abandoned it one year later, thinking no one care about it.\
Recently I've instead discovered that it's actually being used by several projects on GitHub 
(despite it has only few stars).\
So I'm rebooting it with new found enthusiasm and a brand new version with tons of new api and improvements.

Besides the code, the project configuration is now mature and professional: 
- Automatic builds and testing against multiple python versions with Travis CI
- Automatic code coverage reporting on codecov.io
- Automatic documentation generated on readthedocs.io
- Better descriptions and provided examples


### Deprecations:

We are in 2020 and finally old versions of Python have been 
[officially deprecated](https://www.python.org/doc/sunset-python-2/).
So the following versions are **no longer supported**:

- 2.7.x
- 3.3.x
- 3.4.x

(suite tests are now being executed against all currently supported versions: 3.5, 3.6, 3.7 and 3.8)

### Added:

- `compress()`: compress strings into shorter ones that can be restored later on
- `decompress()`: restore a previously compressed string
- `roman_encode()`: encode integers/strings into roman number strings
- `roman_decode()`: decode roman number into an integer
- `roman_range()`: generator which returns roman numbers on each iteration
- `asciify()`: Force string content to be ascii-only by translating all non-ascii chars into the closest possible
 representation 
- `is_ip_v4()`: checks only for v4 ips
- `is_ip_v6()`: checks only for v6 ips
- `is_isbn_13()`: checks if the given string is a valid ISBN 13
- `is_isbn_10()`: checks if the given string is a valid ISBN 10
- `is_isbn()`: checks if the given string is a valid ISBN (any version)
- `is_number()`: checks if the given string is a valid number (either an integer or a decimal)
- `is_integer()`: checks if the given string is a valid integer
- `is_decimal()`: checks if the given string is a valid decimal
- `booleanize()`: turns string into boolean based on its content
- `strip_margin()`: remove left margin from multi line strings so you don't have to bother about indentation 
in your code (inspired by Scala)
- `random_string()`: generates string of given size with random alpha-numeric chars
- `secure_random_hex()`: generates hexadecimal string of the given bytes count using secure random generator

### Fixes:

- `is_email()` is now fully compliant with email specifications (https://tools.ietf.org/html/rfc3696#section-3)
- `is_ip()` now checks both ip v4 (and validates 0-255 range) and ip v6 
(the previous implementation was really shallow, my apologies :P)
- `is_json()` now considers as valid json array objects (eg. `is_json('[1, 2, 3]')` returns true now)
- `prettify()` does not screw up urls or emails anymore (from now on it won't consider those as text to be formatted)
- Solved deprecation warnings over invalid escape sequences in Python >= 3.7 

### Changes:

- Old module `string_utils.py` has been replaced by a package with submodules (`validation.py`, `manipulation.py`, 
`generation.py` and `errors.py`), anyway all the functions are still 
importable as before (`from string_utils import xxx`). Similarly `tests.py` has been refactored into a package 
with a module for each test case
- `is_snake_case()` now considers as "snake case" strings with mixed upper and lower case characters, strings with 
leading or trailing underscores and string containing multiple underscores in sequence
- `is_slug()` now allows multiple consecutive separator signs between words

### Improvements:

- Added Python type hints to all functions arguments and return types 
(this is now feasible since the minimum supported Python version is the 3.5)
- Each method that expect a valid string as input now will raise a more detailed `InvalidInputError` exception 
(eg: ***Expected "str", received "list"***)
- `reverse()`, `shuffle()`, `prettify()` now raise the detailed `InvalidInputError` if input is not a valid string
- String checks should now be a bit faster (switched from `.search()` to `.match()` in internal regex when the goal 
is to match the full string)
- `is_palindrome()` algorithm has been redesigned to offer a faster check and better memory usage 
(only 2 chars are now being access at the same time instead of the whole string)... 
signature has changed (now it has two optional boolean arguments: `ignore_spaces` and `ignore_case`)
- `slugify()` is now able to translate more non-ascii chars during the string conversion 
(it now makes use of the new extracted method `asciify()`)
- `is_uuid()` has now a second parameter `allow_hex` that if true, considers as valid UUID hex value
- `uuid()` has now an optional boolean parameter `as_hex` which allows to return UUID string as hex representation
- `shuffle()` is now faster

---



## v0.6.0

### Added:

- slugify
- is_slug

## v0.5.0

### Added:

- is_full_string
- is_isogram

## v0.4.2

### Fixed:

- is_url

## v0.4.1

### Changed:

- is_palindrome and is_pangram now return False if the given object is not a string instead of raising an exception

## v0.4.0

### Added:

- is_palindrome
- is_pangram

### Changed:

- reverse (improved implementation)

## v0.3.0

### Added:

- contains_html
- strip_html
- prettify


## v0.2.0

### Changed:

- Checking methods (those ones starting with "is_") now don't raise **TypeError** exception
if a non string objects is passed, instead **False** is returned (string_utils.is_url(1) -> **False**).
- Forced **UTF-8** encoding for module file 

### Added:

- is_string
- is_ip
- words_count


## v0.1.2

### Added:

- is_url
- is_email
- is_credit_card
- is_camel_case
- is_snake_case
- is_json
- is_uuid
- camel_case_to_snake
- snake_case_to_camel
- reverse
- uuid
- shuffle
