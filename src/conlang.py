#!/usr/bin/python3

import random, string
import xml.etree.ElementTree
from typing import Mapping
from enum import Enum

class LanguageType(Enum):
    CIPHER = "cipher"

class Conlang:
    def __init__(self,
                 name: str = None,
                 language_type: "LanguageType" = LanguageType.CIPHER,
                 seed: int = None):
        self.language_name = name
        self.language_type = LanguageType.CIPHER
        self.seed = seed
        if seed is None:
            self.seed = random.randint(0,4294967295)
        if self.language_type is LanguageType.CIPHER:
            self.__generate_cipher()
        if name is None:
            self.language_name = self.translate_to_conlang("Language")
            
    def save(self, filename: str):
        with open(filename, 'w') as fout:
            fout.write(
                '<?xml version="1.0"?>\n'
                '<conlang\n'
                '    xmlns="waxd.dev/Conlang"\n'
                '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
                '    xsi:schemaLocation="waxd.dev/Conlang schemas/conlang.xsd">\n'
                '  <LanguageName>{name}</LanguageName>\n'
                '  <LanguageType>{type}</LanguageType>\n'
                '  <seed>{seed}</seed>\n'
                '</conlang>\n'.format(
                    name=self.language_name,
                    type=str(self.language_type.value),
                    seed=self.seed))

    def load(filename: str):
        tree = xml.etree.ElementTree.parse(filename)
        root = tree.getroot()
        language_name = root.find("{waxd.dev/Conlang}LanguageName").text
        language_type = root.find("{waxd.dev/Conlang}LanguageType").text
        seed = int(root.find("{waxd.dev/Conlang}seed").text)
        if language_type is LanguageType.CIPHER.value:
            language_type = LanguageType.CIPHER
        return Conlang(name=language_name,
                       language_type=language_type,
                       seed=seed)

    def translate_to_conlang(self, text: str) -> str:
        return self.__translate_with_cipher(text, self.cipher_to_conlang)

    def translate_from_conlang(self, text: str) -> str:
        return self.__translate_with_cipher(text, self.cipher_from_conlang)

    def __translate_with_cipher(self, text: str, cipher: Mapping[str, str]) -> str:
        translation = []
        for l in text:
            if l in cipher:
                translation.append(cipher[l])
            else:
                translation.append(l)
        assert len(text) is len(translation)
        return ''.join(translation)
            
    def __generate_cipher(self):
        vowels_lowercase = 'aeiouy'
        vowels_uppercase = 'AEIOUY'
        consonants_lowercase = string.ascii_lowercase.translate(
            str.maketrans('', '', vowels_lowercase))
        consonants_uppercase = string.ascii_uppercase.translate(
            str.maketrans('', '', vowels_uppercase))
        letters = ''.join([vowels_lowercase,
                           vowels_uppercase,
                           consonants_lowercase,
                           consonants_uppercase])
        random.seed(self.seed)
        conlang_vowels_lowercase = random.sample(vowels_lowercase,
                                                 len(vowels_lowercase))
        conlang_consonants_lowercase = random.sample(consonants_lowercase,
                                                     len(consonants_lowercase))
        random.seed(self.seed)
        conlang_vowels_uppercase = random.sample(vowels_uppercase,
                                                 len(vowels_uppercase))
        conlang_consonants_uppercase = random.sample(consonants_uppercase,
                                                     len(consonants_uppercase))
        conlang_letters = ''.join(conlang_vowels_lowercase
                                  + conlang_vowels_uppercase
                                  + conlang_consonants_lowercase
                                  + conlang_consonants_uppercase)
        assert len(letters) == len(conlang_letters)
        self.cipher_to_conlang = dict(zip(letters, conlang_letters))
        self.cipher_from_conlang = dict(zip(conlang_letters, letters))
