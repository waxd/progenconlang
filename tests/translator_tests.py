#!/usr/bin/python3

import os
import sys
import unittest

sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir,
    "src"))

from conlang import CipherTranslator
from conlang import LexiconTranslator


class CipherTranslatorTests(unittest.TestCase):
    def setUp(self):
        self.translator = CipherTranslator(seed=12)
        self.translator._set_cipher({'a': 'b', 'b': 'c', 'c': 'a'})

    def test_translate_lowercase(self):
        expected = "bca"
        actual = self.translator.translate("abc")
        self.assertEqual(expected, actual)

    def test_translate_uppercase(self):
        expected = "BCA"
        actual = self.translator.translate("ABC")
        self.assertEqual(expected, actual)

    def test_translate_non_cipher_letters_preserved(self):
        expected = "!.?"
        actual = self.translator.translate("!.?")
        self.assertEqual(expected, actual)

    def test_reverse_translate_lowercase(self):
        expected = "abc"
        actual = self.translator.translate("bca", reverse=True)
        self.assertEqual(expected, actual)


class LexiconGenerationTests(unittest.TestCase):
    def setUp(self):
        self.translator = LexiconTranslator(seed=12, words=["hello", "world"])

    def test_non_word_translate(self):
        expected = "dog"
        actual = self.translator.translate("dog")
        self.assertEqual(expected, actual)

    def test_add_word(self):
        output = self.translator.translate("dog")
        self.assertEqual("dog", output)
        self.translator.add_word("dog")
        output = self.translator.translate("dog")
        self.assertEqual("gbch", output)

    def test_translate_multiple_words(self):
        expected = "Takooru, lcidmfg"
        actual = self.translator.translate("Hello, world")
        self.assertEqual(expected, actual)


class LexiconTranslatorTests(unittest.TestCase):
    def setUp(self):
        self.translator = LexiconTranslator(seed=12)
        self.translator._set_lexicon({"hello": "goodnight", "world": "moon"})

    def test_translate_lowercase(self):
        expected = "goodnight moon"
        actual = self.translator.translate("hello world")
        self.assertEqual(expected, actual)

    def test_translate_title_case(self):
        expected = "Goodnight Moon"
        actual = self.translator.translate("Hello World")
        self.assertEqual(expected, actual)

    def test_translate_uppercase(self):
        expected = "GOODNIGHT MOON"
        actual = self.translator.translate("HELLO WORLD")
        self.assertEqual(expected, actual)

    def test_translate_unknown_word(self):
        expected = "goodnight mars"
        actual = self.translator.translate("hello mars")
        self.assertEqual(expected, actual)

    def test_reverse_translate_lowerrcase(self):
        expected = "hello world"
        actual = self.translator.translate("goodnight moon", reverse=True)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
