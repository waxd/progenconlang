import os, xmlschema

os.chdir('../')
print('Loading schema')
schema = xmlschema.XMLSchema('conlang.xsd')
print('Schema Loaded')
print('Validating xml')
schema.validate('basic_cipher.xml')
print('Valdation complete')
exit(0)
