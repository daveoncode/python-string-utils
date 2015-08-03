# Python String Utils Changelog


## v0.2.0

### Changed:

- Checking methods (those ones starting with "is_") now don't raise **TypeError** exception
if a non string objects is passed, instead **False** is returned (string_utils.is_url(1) -> **False**).
- Forced **UTF-8** encoding for module file 

### Added

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
