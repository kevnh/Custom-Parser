# Kevin Huynh
# Phase 3.2
# https://gist.github.com/blinks/47989 used as reference

import re

# Define class for Tokens
class Token(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return 'Token(%r)' % str(self)

    def __str__(self):
        return '%s : %s' % (self.value, self.name)


# Define class for unrecognized characters
class UnrecognizedCharacter(ValueError):
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return 'Error: %s is an unrecognized character' % self.char


# Define class for Scanner object
class Scanner(object):
    # Takes dictionary of regexes as tokens
    def __init__(self, tokens):
        self.tokens = tokens
        self.compile()
        self.ignores = set()

    # Takes in a single line of text then scans it for tokens
    def __call__(self, line):
        tokens = list()
        pos = 0
        while pos < len(line):
            m = self.regex.match(line, pos)
            if m is None:
                raise UnrecognizedCharacter(line[pos:pos+1])
            elif m.lastgroup in self.ignores:
                pos = m.end()
            else:
                tokens.append(Token(m.lastgroup, m.group()))
                pos = m.end()
        return tokens

    # Puts regexes together then calls re.compile
    def compile(self):
        self.regex = re.compile('|'.join('(?P<%s>%s)' % (name, self.tokens[name]) for name in self.tokens))

    # Adds Token to ignore
    def ignore(self, key):
        self.ignores.add(key)

    # Removes Token from ignore set
    def unignore(self, key):
        self.ignores.discard(key)
