from unittest import TestCase

from string_utils.errors import InvalidInputError
from string_utils.validation import is_isbn


class IsISBNTestCase(TestCase):
    def test_requires_valid_string(self):
        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn(None))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn(True))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn(9780312498580))

        # noinspection PyTypeChecker
        self.assertRaises(InvalidInputError, lambda: is_isbn([9780312498580]))

    def test_returns_true_for_valid_isbn_10(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertTrue(is_isbn('1506715214'))
        self.assertTrue(is_isbn('1506715532'))
        self.assertTrue(is_isbn('0451494504'))
        self.assertTrue(is_isbn('0718079183'))
        self.assertTrue(is_isbn('8830102180'))
        
    def test_returns_true_for_valid_isbn_13(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertTrue(is_isbn('9780312498580'))
        self.assertTrue(is_isbn('9781941325827'))
        self.assertTrue(is_isbn('9780062853851'))
        self.assertTrue(is_isbn('9781250107817'))
        self.assertTrue(is_isbn('9788891229243'))

    def test_hyphens_are_not_considered_by_default(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertTrue(is_isbn('150-6715214'))
        self.assertTrue(is_isbn('150-671-5532'))
        self.assertTrue(is_isbn('045-14-94-50-4'))
        self.assertTrue(is_isbn('071-8-0-7-9-1-8-3'))
        self.assertTrue(is_isbn('8-8-3-0-1-0-2-1-8-0'))
        self.assertTrue(is_isbn('978-0312498580'))
        self.assertTrue(is_isbn('978-194-132-582-7'))
        self.assertTrue(is_isbn('978-0-0-6-2-8-5-3-8-5-1'))

    def test_isbn_not_recognized_if_normalization_is_disabled(self):
        # isbn numbers have been taken from actual books on amazon
        self.assertFalse(is_isbn('150-6715214', normalize=False))
        self.assertFalse(is_isbn('150-671-521-4', normalize=False))
        self.assertFalse(is_isbn('978-0312498580', normalize=False))
        self.assertFalse(is_isbn('978-194-132-582-7', normalize=False))
        self.assertFalse(is_isbn('978-0-0-6-2-8-5-3-8-5-1', normalize=False))

    def test_returns_false_if_not_isbn(self):
        self.assertFalse(is_isbn('9780312498580!'))
        self.assertFalse(is_isbn(' 1506715214'))
        self.assertFalse(is_isbn('1506715214y'))
