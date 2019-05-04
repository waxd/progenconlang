#!/usr/bin/python3

import os
import sys
import unittest

sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir,
    "src"))

from conlang import Conlang

class InternalFunctionTests(unittest.TestCase):
    """
    Unlike external functions, the functionality of internal functions
    may change beteen major versions.
    """
    def setUp(self):
        self.conlang = Conlang()

    def test_translate_with_cipher(self):
        expected = "cba"
        output = self.conlang._Conlang__translate_with_cipher(
            "abc",
            {'a': 'c', 'b':'b', 'c':'a'})
        self.assertEqual(output, expected)

    def test_translate_with_lexicon(self):
        output = self.conlang._Conlang__translate_with_lexicon(
            "hello world",
            {"hello": "goodnight", "world": "moon"})
        self.assertEqual(output, "goodnight moon")

    def test_translate_word(self):
        output = self.conlang._Conlang__translate_word_with_lexicon(
            "hello",
            {"hello": "goodnight", "world": "moon"})
        self.assertEqual(output, "goodnight")
        output = self.conlang._Conlang__translate_word_with_lexicon(
            "world",
            {"hello": "goodnight", "world": "moon"})
        self.assertEqual(output, "moon")

if __name__ == '__main__':
    unittest.main()
