# Kevin Huynh
# Phase 3.2

import sys
from scanner import Scanner
from pl_parser import Parser
from evaluator import Evaluator

# Iterate through tree to build graphical parse tree
def print_tree(tree, tabs):
    string = ""
    tabs_str = ""
    for i in range(tabs):
        tabs_str += "\t"
    string += "%s%s\n" % (tabs_str, str(tree))

    if (tree.left is not None):
        string += print_tree(tree.left, tabs+1)
    if (tree.middle is not None):
        string += print_tree(tree.middle, tabs+1)
    if (tree.right is not None):
        string += print_tree(tree.right, tabs+1)

    return string

# Print memory in readable format
def print_memory(memory):
    string = ""
    for key in memory:
        string += "%s = %d\n" % (key, memory[key])

    return string

# Test function for parser
def test_by_file():
    regexes = {
        'KEYWORD' : r'(if\b|then\b|else\b|endif\b|while\b|do\b|endwhile\b|skip\b)',
        'IDENTIFIER' : r'([a-zA-Z]([a-zA-Z]|[0-9])*)',
        'NUMBER' : r'[0-9]+',
        'PUNCTUATION' : r'(\+|\-|\*|/|\(|\)|:=|;)',
        'SPACE' : r'\s+'
    }

    input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "test_output.txt"

    scanner = Scanner(regexes)
    scanner.ignore('SPACE')
    parser = Parser()
    evaluator = Evaluator()
    tokens = list()
        
    try:
        _in = open(input_file, 'r')

        with open(output_file, 'w') as _out:
            try:
                for line in _in.readlines():    # Scan through entire file before parsing
                    line = line.strip("\n")
                    tokens += scanner(line)
                _out.write("Tokens:\n\n")
                for token in tokens:
                    _out.write(str(token)+"\n")
                parser.load_tokens(tokens)
                tree = parser()
                _out.write("\nAST:\n\n")
                _out.write(print_tree(tree, 0))
                evaluator.load_tree(tree)
                output = evaluator()
                _out.write("\nOutput:\n")
                _out.write(print_memory(output))
            except ValueError as e:
                _out.write(str(e))
                _in.close()
                return
        _in.close()
    except IOError:
        print("Unable to open requested file: %s." % input_file)

    return 0


# Test function for parser
def test_by_line():
    regexes = {
        'KEYWORD' : r'(if\b|then\b|else\b|endif\b|while\b|do\b|endwhile\b|skip\b)',
        'IDENTIFIER' : r'([a-zA-Z]([a-zA-Z]|[0-9])*)',
        'NUMBER' : r'[0-9]+',
        'PUNCTUATION' : r'(\+|\-|\*|/|\(|\)|:=|;)',
        'SPACE' : r'\s+'
    }

    input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "test_output.txt"

    scanner = Scanner(regexes)
    scanner.ignore('SPACE')
    parser = Parser()
    evaluator = Evaluator()
    tokens = list()

    try:
        _in = open(input_file, 'r')
        
        with open(output_file, 'w') as _out:
            try:
                for line in _in.readlines():    # Scan and parse line by line
                    line = line.strip("\n")
                    tokens += scanner(line)
                    _out.write("Tokens:\n\n")
                    for token in tokens:
                        _out.write(str(token)+"\n")
                    parser.load_tokens(tokens)
                    tree = parser()
                    _out.write("\nAST:\n\n")
                    _out.write(print_tree(tree, 0))
                    evaluator.load_tree(tree)
                    output = evaluator()
                    _out.write("\nOutput: %d\n" % output)
            except ValueError as e:
                _out.write(str(e))
                _in.close()
                return
        _in.close()
    except IOError:
        print("Unable to open requested file: %s." % input_file)

    return 0


if __name__ == '__main__':
    test_by_file()
    #test_by_line()