#!/usr/bin/python3

import unittest, sys, os

sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir,
    "src"))

print(sys.path)

from conlang import Conlang

class CipherGenerationTestCase(unittest.TestCase):
    def setUp(self):
        self.conlang = Conlang.generate(1)

    def test_save_config(self):
        self.assertTrue(False)
    
    def test_translate_to_conlang(self):
        en_string = "Hello world"
        conlang_string = self.conlang.translate_to(en_string)
        self.assertEqual(conlang_string, "Somes string")

    def test_translate_from_conlang(self):
        conlang_string = "Somes string"
        en_string = self.conlang.translate_from(en_string)
        self.assertEqual(en_string, "Hello world")

class CipherLoadTestCase(unittest.TestCase):
    def setUp(self):
        self.conlang = Conlang("testdata/basic_cipher.xml")

    def test_translate_to_conlang(self):
        pass

    def test_tranlsate_from_conlang(self):
        pass

if __name__ == '__main__':
    unittest.main()
