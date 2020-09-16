# Kevin Huynh
# Phase 3.2

import copy
from pl_parser import PTInteriorNode
from scanner import Token

# Define class for evaluator object
class Evaluator(object):
    def __init__(self):
        self.op_index = 0
        self.stack = list()
        self.memory = {}
        self.setup_ops()

    def __call__(self):
        self.evaluate_state(self.root)
        return self.memory

    # Setup dict for logical operators
    def setup_ops(self):
        self.ops = {
            '+' : self.add,
            '-' : self.sub,
            '*' : self.mul,
            '/' : self.div,
        }

    # Load tree into evaluator
    def load_tree(self, ast):
        self.root = ast

    # Evaluate tree
    def evaluate_state(self, tree):
        token = tree.value
        if token.value == ';':
            self.evaluate_state(tree.left)      # Evaluates tree.left first
            tree_state = tree.right
            del tree                            # Removes unnecessary token
            self.evaluate_state(tree_state)     # then evaluates tree.right
        elif token.value == ':=':
            self.evaluate_assign(tree)
        elif token.value == 'if':
            self.evaluate_if(tree)
        elif token.value == 'while':
            self.evaluate_while(tree)

    # Evaluate assignment expression
    def evaluate_assign(self, tree):
        self.evaluate_expr(tree.right)
        value = self.stack.pop()                # Returns final value from expression
        token = tree.left.value
        self.memory[token.value] = value        # Creates/Adjusts memory
        del tree.left                           # Delete unnecessary tokens
        del tree

    # Evaluate if expression
    def evaluate_if(self, tree):
        self.evaluate_expr(tree.left)
        condition = self.stack.pop()
        tree_state = ''
        if condition:
            self.delete_tree(tree.right)    # Delete unnecessary part of tree
            tree_state = tree.middle
        else:
            self.delete_tree(tree.middle)   # Same as above
            tree_state = tree.right

        del tree                            # Delete unnecessary token
        self.evaluate_state(tree_state)     # Evaluate new tree state

    # Evaluate while expression
    def evaluate_while(self, tree):
        self.evaluate_expr(tree.left)
        condition = self.stack.pop()
        if condition:
            # Add copy of tree.right to new node along with tree
            tree = PTInteriorNode(Token('PUNCTUATION', ';'), copy.deepcopy(tree.right), tree)
            self.evaluate_state(tree)       # Evaluate new tree
        else:
            self.delete_tree(tree)

    # Recursively delete references to token objects
    def delete_tree(self, tree):
        if (tree.left is not None):
            self.delete_tree(tree.left)

        if (tree.middle is not None):
            self.delete_tree(tree.middle)

        if (tree.right is not None):
            self.delete_tree(tree.right)

        del tree

    # Pre-order traverse expression tree
    def evaluate_expr(self, tree):
        token = tree.value
        value = ''
        if token.name == 'NUMBER':
            value = int(token.value)        # Push numbers as integers
        elif token.name == 'IDENTIFIER':
            if token.value not in self.memory.keys():
                raise ValueError("Error: %s variable has not been initialized." % token.value)
            value = self.memory[token.value]
        else:
            value = token.value

        self.stack.append(value)
        self.check_stack()

        if (tree.left is not None):
            self.evaluate_expr(tree.left)
            self.check_stack()

        if (tree.right is not None):
            self.evaluate_expr(tree.right)
            self.check_stack()

        del tree

    # Check top 3 elements of self.stack
    def check_stack(self):
        length = len(self.stack)
        if length > 2:
            if isinstance(self.stack[length-2], int) and isinstance(self.stack[length-1], int):
                var2 = self.stack.pop()
                var1 = self.stack.pop()
                op = self.stack.pop()

                self.stack.append(self.ops[op](var1, var2))

    def add(self, x, y):
        return x + y

    def sub(self, x, y):
        value = x - y
        if (value < 0):
            value = 0
        return value

    def mul(self, x, y):
        return x * y

    def div(self, x, y):
        if y == 0:
            raise ValueError("Error: Cannot divide by 0 in %d / %d" % (x, y))

        return x // y
