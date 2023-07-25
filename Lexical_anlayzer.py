import nltk

import re

cfile = open('cSample.c', 'r')
program = cfile.read()

RE_keywords = 'auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|?int?|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struc|include'
RE_operators = "(\++)|(-)|(=)|(\*)|(/)|(%)|(--)|(<=)|(>=)"
RE_numerals = "^(\d+)$"
RE_special_characters = "[\[@&~!#$\^\|{}\]:;<>?,\.']|\(\)|\(|\)|{}|\[\]|\""
RE_Identifiers = '^[a-zA-Z_]+[a-zA-Z0-9_]*'
RE_headers = "([a-zA-Z]+\.[h])"

Identifiers_Output = []
keywords_Output = []
symbols_Output = []
operators_Output = []
numerals_Output = []
headers_Output = []
missing_semicolon = []
spelling_error = []


def remove_Spaces(program):
    scanned_Program = []
    for line in prog:
        if line.strip() != '':
            scanned_Program.append(line.strip())
    return scanned_Program


def remove_Comments(program):
    program_Multi_Comments_Removed = \
        re.sub("/\*[^*]*\*+(?:[^/*][^*]*\*+)*/", '', program)
    program_Single_Comments_Removed = re.sub('//.*', '', program_Multi_Comments_Removed)
    program_Comments_removed = program_Single_Comments_Removed
    return program_Comments_removed


program_Comments_removed = remove_Comments(program)
prog = program_Comments_removed.split('\n')

scanned_Prog = remove_Spaces(prog)
scanned_Program = '\n'.join([str(elem) for elem in scanned_Prog])

Source_Code = scanned_Program.split('\n')

i = 0
for line in Source_Code:
    i += 1
    if line[0] == '#' or line[0:1] == 'if' or line[0] == '}' or line[0] \
        == '{' or line[0:4] == 'elif' or line[0:4] == 'else' \
            or line[-1] == '(':
        continue
    elif line[-1] == ')' and Source_Code[i][0] == '{':
        continue
    elif line[-1] != ';':

        missing_semicolon.append(line)

count = 0

for line in Source_Code:
    count = count + 1
    if line.startswith('#include'):
        tokens = nltk.word_tokenize(line)
    else:
        tokens = nltk.wordpunct_tokenize(line)
        print(tokens)
    for token in tokens:
        if re.findall(RE_keywords, token):
            keywords_Output.append(token)
        elif re.findall(RE_headers, token):
            headers_Output.append(token)
        elif re.findall(RE_operators, token):
            operators_Output.append(token)
        elif re.findall(RE_numerals, token):
            numerals_Output.append(token)
        elif re.findall(RE_special_characters, token):
            symbols_Output.append(token)
        elif re.findall(RE_Identifiers, token):
            Identifiers_Output.append(token)
        else:
            spelling_error.append(token)

print('There Are', len(keywords_Output), 'Keywords :',keywords_Output)
print ('\n')
print('There Are', len(Identifiers_Output), 'Identifiers :',Identifiers_Output)
print ('\n')
print('There Are', len(headers_Output), 'Header Files :',headers_Output)
print ('\n')
print('There Are', len(symbols_Output), 'Symbols :', symbols_Output)
print ('\n')
print('There Are', len(operators_Output), 'Opertors :',operators_Output)
print ('\n')
print('There Are', len(numerals_Output), 'Numerals :', numerals_Output)
print ('\n')
print('There Are', len(missing_semicolon), 'Missing Semicolon in :',missing_semicolon)
print ('\n')
print('There Are', len(spelling_error), 'Spelling Errors in :',spelling_error)
print ('\n')
