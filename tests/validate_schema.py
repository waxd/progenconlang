#!/usr/bin/python3

import os
import sys
import unittest
import xmlschema

sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir,
    "src"))

from conlang import Conlang

class ValidateXMLTestCase(unittest.TestCase):
    def test_all_good_examples_load_without_error(self):
        Conlang.load("testdata/basic_cipher.xml")
        Conlang.load("testdata/basic_lexicon.xml")

    def test_all_bad_examples_throw_error(self):
        with self.assertRaises(
                xmlschema.validators.exceptions.XMLSchemaValidationError):
            Conlang.load("testdata/bad_cipher.xml")

if __name__ == '__main__':
    unittest.main()
