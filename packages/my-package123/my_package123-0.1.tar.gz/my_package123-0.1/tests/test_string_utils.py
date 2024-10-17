# test_string_utils.py
import unittest
from my_package123.string_utils import uppercase, reverse_string, count_vowels

class TestStringUtils(unittest.TestCase):
    def test_uppercase(self):
        self.assertEqual(uppercase("hello"), "HELLO")

    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello world"), 3)
