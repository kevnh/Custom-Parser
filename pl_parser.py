# Kevin Huynh
# Phase 3.2

# Define base class for PTNode
class PTNode(object):
    def __init__(self):
        self.left = None
        self.middle = None
        self.right = None


# Define class for PTNode with operation
class PTInteriorNode(PTNode):
    def __init__(self, op, left, right):
        super().__init__()
        self.value = op
        self.left = left
        self.right = right

    def __str__(self):
        return '%s' % self.value


# Define class for PTNode ifstatements
class PTTripleNode(PTNode):
    def __init__(self, key, left, middle, right):
        self.value = key
        self.left = left
        self.middle = middle
        self.right = right

    def __str__(self):
        return '%s' % self.value


# Define class for PTNode leaf
class PTLeafNode(PTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return '%s' % self.value


# Define class for parser object
class Parser(object):
    def __init__(self):
        self.tokens = None
        self.next_token = None

    # Runs grammar on current tokens and returns tree (or returns error if there is one)
    def __call__(self):
        #return self.parse_expr()
        return self.parse_state()

    # Load in new tokens due to scanner scanning tokens per line
    def load_tokens(self, tokens):
        self.tokens = tokens
        self.consume_token()

    # Iterate through tokens (and eventually delete token objects when not referenced anywhere)
    def consume_token(self):
        try:
            self.next_token = self.tokens.pop(0)
        except IndexError:
            pass

    # Grammar for statement
    def parse_state(self):
        tree = self.parse_base()
        while (self.next_token.value == ';'):
            temp = self.next_token
            self.consume_token()
            tree = PTInteriorNode(temp, tree, self.parse_base())

        return tree

    # Grammar for basestatement
    def parse_base(self):
        tree = ""
        if (self.next_token.name == 'IDENTIFIER'):
            tree = self.parse_assign()
        elif (self.next_token.value == 'if'):
            tree = self.parse_if()
        elif (self.next_token.value == 'while'):
            tree = self.parse_while()
        elif (self.next_token.value == 'skip'):
            temp = self.next_token
            self.consume_token()
            return PTLeafNode(temp)
        else:
            raise ValueError("Error: Expected IDENTIFIER, if, while, or skip instead of %s" % self.next_token)
        return tree

    # Grammar for assignment
    def parse_assign(self):
        tree = PTLeafNode(self.next_token)
        self.consume_token()
        if (self.next_token.value == ':='):
            temp = self.next_token
            self.consume_token()
            tree = PTInteriorNode(temp, tree, self.parse_expr())
        else:
            raise ValueError("Error: Expected := (PUNCTUATION) instead of %s" % self.next_token)

        return tree

    # Grammar for ifstatement
    def parse_if(self):
        key = self.next_token
        self.consume_token()
        tree = self.parse_expr()
        if (self.next_token.value == 'then'):
            self.consume_token()
            mid = self.parse_state()
            if (self.next_token.value == 'else'):
                self.consume_token()
                tree = PTTripleNode(key, tree, mid, self.parse_state())
                if (self.next_token.value == 'endif'):
                    self.consume_token()
                    return tree
                else:
                    raise ValueError("Error: Expected endif (KEYWORD) instead of %s" % self.next_token)
            else:
                raise ValueError("Error: Expected else (KEYWORD) instead of %s" % self.next_token)
        else:
            raise ValueError("Error: Expected then (KEYWORD) instead of %s" % self.next_token)

    # Grammar for whilestatement
    def parse_while(self):
        key = self.next_token
        self.consume_token()
        tree = self.parse_expr()
        if (self.next_token.value == 'do'):
            self.consume_token()
            tree = PTInteriorNode(key, tree, self.parse_state())
            if (self.next_token.value == 'endwhile'):
                self.consume_token()
                return tree
            else:
                raise ValueError("Error: Expected endwhile (KEYWORD) instead of %s" % self.next_token)
        else:
            raise ValueError("Error: Expected do (KEYWORD) instead of %s" % self.next_token)

    # Start of grammar for expression
    def parse_expr(self):
        tree = self.parse_term()
        while (self.next_token.value == '+'):
            op = self.next_token
            self.consume_token()
            tree = PTInteriorNode(op, tree, self.parse_term())

        return tree

    # Grammar for term
    def parse_term(self):
        tree = self.parse_factor()
        while (self.next_token.value == '-'):
            op = self.next_token
            self.consume_token()
            tree = PTInteriorNode(op, tree, self.parse_factor())

        return tree

    # Grammar for factor
    def parse_factor(self):
        tree = self.parse_piece()
        while (self.next_token.value == '/'):
            op = self.next_token
            self.consume_token()
            tree = PTInteriorNode(op, tree, self.parse_piece())

        return tree

    # Grammar for piece
    def parse_piece(self):
        tree = self.parse_element()
        while (self.next_token.value == '*'):
            op = self.next_token
            self.consume_token()
            tree = PTInteriorNode(op, tree, self.parse_element())

        return tree

    # Grammar for element
    def parse_element(self):
        if (self.next_token.value == '('):
            self.consume_token()
            tree = self.parse_expr()
            if (self.next_token.value == ')'):
                self.consume_token()
                return tree
            else:
                raise ValueError("Error: Expected ) (PUNCTUATION), got %s instead.\n" % self.next_token)
        elif (self.next_token.name == 'NUMBER'):
            node = PTLeafNode(self.next_token)
            self.consume_token()
            return node
        elif (self.next_token.name == 'IDENTIFIER'):
            node = PTLeafNode(self.next_token)
            self.consume_token()
            return node
        else:
            raise ValueError("Error: Expected IDENTIFIER or NUMBER, got %s instead.\n" % self.next_token)
