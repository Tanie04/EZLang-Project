# nodes.py — Abstract Syntax Tree Node Definitions
# This file is intentionally data-only: no logic, no imports.
# Each class represents one grammatical construct in EZLang.
# The Interpreter (visitor) reads these attributes to execute the program.


class ASTNode:
    """Base class for all AST nodes. Acts as a type marker."""
    pass


# ------------------------------------------------------------------
# Literals
# ------------------------------------------------------------------

class NumberNode(ASTNode):
    """A numeric literal: integer or float. e.g. 42, 3.14"""
    def __init__(self, value):
        self.value = value  # int | float


class StringNode(ASTNode):
    """A string literal (quotes already stripped). e.g. "hello" """
    def __init__(self, value):
        self.value = value  # str


class VariableNode(ASTNode):
    """A reference to a declared variable by name."""
    def __init__(self, name):
        self.name = name  # str


# ------------------------------------------------------------------
# Expressions
# ------------------------------------------------------------------

class BinOpNode(ASTNode):
    """
    A binary operation between two sub-expressions.
    op is a token-type string: 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
    'EQ', 'GT', 'LT', 'GE', 'LE', 'AND', 'OR'.
    """
    def __init__(self, left, op, right):
        self.left = left    # ASTNode
        self.op = op        # str
        self.right = right  # ASTNode


class UnaryOpNode(ASTNode):
    """
    A unary operation applied to one sub-expression.
    op is 'MINUS' (numeric negation) or 'NOT' (boolean negation).
    """
    def __init__(self, op, node):
        self.op = op      # str
        self.node = node  # ASTNode


# ------------------------------------------------------------------
# Variable management
# ------------------------------------------------------------------

class DeclarationNode(ASTNode):
    """
    'let name = expression.'
    Declares a new variable in the current scope.
    """
    def __init__(self, name, value_node):
        self.name = name              # str
        self.value_node = value_node  # ASTNode


class AssignmentNode(ASTNode):
    """
    'set name to expression.'
    Re-assigns an already-declared variable (walks the scope chain).
    """
    def __init__(self, name, value_node):
        self.name = name              # str
        self.value_node = value_node  # ASTNode


# ------------------------------------------------------------------
# I/O
# ------------------------------------------------------------------

class PrintNode(ASTNode):
    """'print expression.' — evaluates expression and outputs the result."""
    def __init__(self, expression):
        self.expression = expression  # ASTNode


class InputNode(ASTNode):
    """
    'input name with "prompt".'
    Displays prompt, reads a line, coerces to number if possible,
    and stores the result in name.
    """
    def __init__(self, name, prompt):
        self.name = name      # str — variable to store the result
        self.prompt = prompt  # str — text shown to the user


# ------------------------------------------------------------------
# Control flow
# ------------------------------------------------------------------

class IfNode(ASTNode):
    """
    'when condition then ... [else ...] stop.'
    true_block and false_block are lists of ASTNodes.
    false_block is an empty list when there is no 'else' branch.
    """
    def __init__(self, condition, true_block, false_block):
        self.condition = condition      # ASTNode
        self.true_block = true_block    # list[ASTNode]
        self.false_block = false_block  # list[ASTNode]


class LoopNode(ASTNode):
    """
    'keep going: ... until condition.'
    Executes body repeatedly, checking condition after each iteration.
    Stops when condition is truthy.
    """
    def __init__(self, body, condition):
        self.body = body          # list[ASTNode]
        self.condition = condition  # ASTNode


# ------------------------------------------------------------------
# Collections
# ------------------------------------------------------------------

class ListNode(ASTNode):
    """
    '[expr, expr, ...]'
    elements is a (possibly empty) list of ASTNodes.
    """
    def __init__(self, elements):
        self.elements = elements  # list[ASTNode]


# ------------------------------------------------------------------
# Functions (Tasks)
# ------------------------------------------------------------------

class FunctionDefNode(ASTNode):
    """
    'define task name ... end task.'
    Stores the function's name and its body (list of statements).
    """
    def __init__(self, name, body):
        self.name = name  # str
        self.body = body  # list[ASTNode]


class FunctionCallNode(ASTNode):
    """
    'name.'  (identifier followed by a dot as a standalone statement)
    Triggers execution of the named task.
    """
    def __init__(self, name):
        self.name = name  # str