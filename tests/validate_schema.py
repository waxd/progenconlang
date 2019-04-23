#!/usr/bin/python3
import os, xmlschema

print('Loading schema')
schema = xmlschema.XMLSchema('../schemas/conlang.xsd')
print('Schema Loaded')
print('Validating xml')
schema.validate('testdata/basic_cipher.xml')
print('Valdation complete')
exit(0)
