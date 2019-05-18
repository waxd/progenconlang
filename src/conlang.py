#!/usr/bin/python3

import hashlib
import random
import re
import string
import xmlschema
import xml.etree.ElementTree
from typing import Mapping, List, Any, Union
from enum import Enum


class LanguageType(Enum):
    CIPHER = "cipher"
    LEXICON = "lexicon"


class Conlang:
    schema = xmlschema.XMLSchema("../schemas/conlang.xsd")

    def __init__(self,
                 name: str = None,
                 language_type: "LanguageType" = LanguageType.CIPHER,
                 seed: int = None,
                 word_file: str = None):
        self.language_name = name
        self.language_type = language_type
        if seed:
            self.seed = seed
        else:
            random.seed()
            self.seed = random.randint(0, 4294967295)

        if self.language_type is LanguageType.CIPHER:
            self.translator = CipherTranslator(self.seed)
        elif self.language_type is LanguageType.LEXICON:
            self.translator = LexiconTranslator(self.seed, word_file)
        else:
            # Sanity check: A new language type may need to be added.
            assert False, \
                "{} is an unknown language type.".format(self.language_type)

        if name is None:
            self.language_name = self.translate_to_conlang("Language")

    def save(self, filename: str):
        with open(filename, 'w') as file_out:
            file_out.write(
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

    @staticmethod
    def load(filename: str):
        Conlang.schema.validate(filename)
        tree = xml.etree.ElementTree.parse(filename)
        root = tree.getroot()
        language_name = root.find("{waxd.dev/Conlang}LanguageName").text
        language_type = LanguageType(root.find("{waxd.dev/Conlang}LanguageType").text)
        seed = int(root.find("{waxd.dev/Conlang}seed").text)
        return Conlang(name=language_name,
                       language_type=language_type,
                       seed=seed)

    def translate_to_conlang(self, text: str) -> str:
        return self.translator.translate(text)

    def translate_from_conlang(self, text: str) -> str:
        return self.translator.translate(text, reverse=True)


class Translator:
    def __init__(self):
        pass


class CipherTranslator(Translator):
    def __init__(self, seed: int):
        vowels = 'aeiouy'
        consonants = string.ascii_lowercase.translate(
            str.maketrans('', '', vowels))
        letters = ''.join([vowels, consonants])
        random.seed(seed)
        cipher_vowels = random.sample(vowels, len(vowels))
        cipher_consonants = random.sample(consonants, len(consonants))
        cipher_letters = ''.join(cipher_vowels + cipher_consonants)
        assert len(letters) == len(cipher_letters)
        self.cipher_to = dict(zip(letters, cipher_letters))
        self.cipher_from = dict(zip(cipher_letters, letters))

    def translate(self, text: str, reverse: bool = False) -> str:
        translation = []
        if reverse:
            cipher = self.cipher_from
        else:
            cipher = self.cipher_to
        for l in text:
            if l.lower() in cipher:
                if l.isupper():
                    translation.append(cipher[l.lower()].upper())
                else:
                    translation.append(cipher[l])
            else:
                translation.append(l)
        assert len(text) is len(translation)
        return ''.join(translation)

    def _set_cipher(self, cipher: Mapping[str, str]):
        """For testing"""
        self.cipher_to = cipher
        self.cipher_from = dict(zip(cipher.values(), cipher.keys()))


class LexiconTranslator(Translator):
    schema = xmlschema.XMLSchema('../schemas/lexicon.xsd')

    def __init__(self, seed: int, word_file: str = None):
        self.letters = string.ascii_lowercase
        self.seed = seed
        self.lexicon_to = {}
        if word_file:
            self.load_from_file(word_file)
        self.lexicon_from = dict(zip(self.lexicon_to.values(),
                                     self.lexicon_to.keys()))

    def load_from_file(self, filename: str):
        assert filename is not None
        LexiconTranslator.schema.validate(filename)
        tree = xml.etree.ElementTree.parse(filename)
        for element in tree.findall("{waxd.dev/Lexicon}word"):
            self.add_word(element.text)

    def add_word(self, w: str):
        word = w.lower()
        word_seed = hashlib.md5(bytes(word + str(self.seed), "utf-8")).hexdigest()
        random.seed(word_seed)
        length_difference = int(random.normalvariate(0.5, 2))
        length = len(word) + length_difference
        new_word = []
        if length < 1:
            length = 1
        for _ in range(length):
            new_word.append(random.choice(self.letters))
        self.lexicon_to[word] = ''.join(new_word)

    def translate(self, text: str, reverse: bool = False) -> str:
        translation = []
        for w in re.split(r'(\W+)', text):
            if w.isalnum():
                translation.append(self._translate_word(w, reverse))
            else:
                translation.append(w)
        return ''.join(translation)

    def _translate_word(self, text: str, reverse: bool = False) -> str:
        assert text.isalnum(), "{text}: expected only a-zA-Z".format(text=text)
        if reverse:
            lexicon = self.lexicon_from
        else:
            lexicon = self.lexicon_to

        word = text.lower()
        if word in lexicon:
            if text.istitle():
                return lexicon[word].title()
            elif text.isupper():
                return lexicon[word].upper()
            elif text.islower():
                return lexicon[word].lower()
            else:
                # TODO Maintain weird mixed caps (e.g. "HelLO"
                pass
        else:
            return text

    def _set_lexicon(self, lexicon: Mapping[str, str]):
        """For testing"""
        self.lexicon_to = lexicon
        self.lexicon_from = dict(zip(lexicon.values(), lexicon.keys()))
