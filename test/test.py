import os
import unittest

from hl7.hl7_parser import is_parseable_hl7

_MESSAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "messages")


class ParsingTests(unittest.TestCase):
    def test_valid_messages(self):
        valid_message = self._read("example.hl7")
        self.assertTrue(is_parseable_hl7(valid_message))

        valid_message = self._read("escapes.hl7")
        self.assertTrue(is_parseable_hl7(valid_message))

    def test_empty_string(self):
        self.assertFalse(is_parseable_hl7(""))

    def test_missing_msh(self):
        self.assertFalse(is_parseable_hl7("EVN|test"))

    def test_wrong_delimiters(self):
        self.assertFalse(is_parseable_hl7("MSH|^~|TEST"))  # too few
        self.assertFalse(is_parseable_hl7("MSH|^~\\&X|TEST"))  # too many

    def _read(self, filename):
        with open(os.path.join(_MESSAGES_DIR, filename)) as file:
            return file.read()
