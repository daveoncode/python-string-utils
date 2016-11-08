# Python String Utils Changelog

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
