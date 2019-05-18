#!/usr/bin/python3

import os
import sys
import unittest
from xmldiff import main

sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir,
    "src"))

from conlang import Conlang
from conlang import LanguageType

class LexiconGenerationTestsCase(unittest.TestCase):
    def setUp(self):
        self.conlang = Conlang(language_type=LanguageType.LEXICON,
                               seed=12,
                               word_file="../wordlists/en_3000.xml")

    def test_save_config(self):
        self.conlang.save("temp_lexicon_save.xml")
        self.assertFalse(main.diff_files("temp_lexicon_save.xml",
                                         "testdata/basic_lexicon.xml"))
        # Cleanup
        os.remove("temp_lexicon_save.xml")

    def test_translate_to_conlang(self):
        expected = "Takooru lcidm"
        actual = self.conlang.translate_to_conlang("Hello world")
        self.assertEqual(expected, actual)

    def test_translate_from_conlang(self):
        expected = "Hello world"
        actual = self.conlang.translate_from_conlang("Takooru lcidm")
        self.assertEqual(expected, actual)

class WordGenerationTestCase(unittest.TestCase):
    def test_word_gen(self):
        pass

if __name__ == '__main__':
    unittest.main()
