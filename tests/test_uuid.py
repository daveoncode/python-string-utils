from unittest import TestCase

from string_utils import is_uuid
from string_utils.generation import uuid


class UUIDTestCase(TestCase):
    def test_generates_uuid_string(self):
        uid = uuid()
        self.assertIsInstance(uid, str)
        self.assertTrue(is_uuid(uid))
