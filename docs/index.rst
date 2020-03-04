Python String Utils: Overview
-----------------------------

This is a handy library to validate, manipulate and generate strings, which is:

- Simple and "pythonic"
- Fully documented and with examples!
- 100% code coverage!
- Tested against all officially supported Python versions: 3.5, 3.6, 3.7, 3.8.
- Fast (mostly based on compiled regex)
- Free from external dependencies
- PEP8 compliant


Installing
----------

>>> pip install python-string-utils


Checking installed version
--------------------------

>>> import string_utils
>>> string_utils.__version__
>>> '1.0.0' # (if '1.0.0' is the installed version)


Library structure
-----------------

The library basically consists in the python package `string_utils`, containing the following modules:

- `validation.py` (contains string check api)
- `manipulation.py` (contains string transformation api)
- `generation.py` (contains string generation api)
- `errors.py` (contains library-specific errors)
- `_regex.py` (contains compiled regex **FOR INTERNAL USAGE ONLY**)

Plus a secondary package `tests` which includes several submodules.
Specifically one for each test suite and named according to the api to test (eg. tests for `is_ip()`
will be in `test_is_ip.py` and so on).
All the public API are importable directly from the main package `string_utils`, so this:

>>> from string_utils.validation import is_ip

can be simplified as:

>>> from string_utils import is_ip


Modules
-------

.. toctree::
   :maxdepth: 3

   validation
   manipulation
   generation
   errors


Function Indices
----------------

* :ref:`genindex`
