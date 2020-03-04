from unittest import TestCase
from uuid import uuid4, uuid1

from string_utils import is_uuid


class IsUUIDTestCase(TestCase):
    def test_should_consider_false_non_string_objects(self):
        # noinspection PyTypeChecker
        self.assertFalse(is_uuid(None))

        # noinspection PyTypeChecker
        self.assertFalse(is_uuid(1))

        # noinspection PyTypeChecker
        self.assertFalse(is_uuid([]))

        # noinspection PyTypeChecker
        self.assertFalse(is_uuid({'a': 1}))

        # noinspection PyTypeChecker
        self.assertFalse(is_uuid(True))

    def test_should_accept_valid_uuid_objects(self):
        for i in range(1000):
            # noinspection PyTypeChecker
            self.assertTrue(is_uuid(uuid4()))
            self.assertTrue(is_uuid(uuid1()))

    def test_should_accept_valid_uuid_strings(self):
        for i in range(1000):
            self.assertTrue(is_uuid(str(uuid4())))
            self.assertTrue(is_uuid(str(uuid1())))

    def test_accepts_hex_value_of_uuid(self):
        for i in range(1000):
            # noinspection PyTypeChecker
            self.assertTrue(is_uuid(uuid4().hex, True))
            self.assertTrue(is_uuid(uuid1().hex, True))
