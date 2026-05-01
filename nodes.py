#Structure of types of nodes in the AST 
class ASTNode:
    """Base class for all nodes in the AST"""
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"{self.value}"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'"{self.value}"'

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"{self.name}"

class BinOpNode(ASTNode):
    """Handles operations like +, -, *, /, and comparisons like >=, =="""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

class DeclarationNode(ASTNode):
    """Handles: let x = 10."""
    def __init__(self, name, value_node):
        self.name = name
        self.value_node = value_node
    def __repr__(self):
        return f"let {self.name} = {self.value_node}"

class AssignmentNode(ASTNode):
    """Handles: set x to 20."""
    def __init__(self, name, value_node):
        self.name = name
        self.value_node = value_node
    def __repr__(self):
        return f"set {self.name} to {self.value_node}"

class PrintNode(ASTNode):
    """Handles: print x."""
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f"print({self.expression})"

class IfNode(ASTNode):
    """Handles: when x >= 10 then ... stop."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"when {self.condition} then {self.body} stop"