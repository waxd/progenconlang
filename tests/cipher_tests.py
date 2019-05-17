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


class CipherGenerationTestCase(unittest.TestCase):
    def setUp(self):
        self.conlang = Conlang(seed=12)

    def test_save_config(self):
        self.conlang.save("temp_cipher_save.xml")
        self.assertFalse(main.diff_files("temp_cipher_save.xml",
                                         "testdata/basic_cipher.xml"))
        # Cleanup
        os.remove("temp_cipher_save.xml")
    
    def test_translate_to_conlang(self):
        en_string = "Hello world"
        conlang_string = self.conlang.translate_to_conlang(en_string)
        self.assertEqual(conlang_string, "Wimma gazml")

    def test_translate_from_conlang(self):
        conlang_string = "Wimma gazml"
        en_string = self.conlang.translate_from_conlang(conlang_string)
        self.assertEqual(en_string, "Hello world")


class CipherLoadTestCase(unittest.TestCase):
    def setUp(self):
        self.conlang = Conlang.load("testdata/basic_cipher.xml")

    def test_translate_to_conlang(self):
        en_string = "Hello world"
        conlang_string = self.conlang.translate_to_conlang(en_string)
        self.assertEqual(conlang_string, "Wimma gazml")

    def test_tranlsate_from_conlang(self):
        conlang_string = "Wimma gazml"
        en_string = self.conlang.translate_from_conlang(conlang_string)
        self.assertEqual(en_string, "Hello world")


if __name__ == '__main__':
    unittest.main()
