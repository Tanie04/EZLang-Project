class ASTNode:
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
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    def __repr__(self):
        return f"({self.op}{self.operand})"

class DeclarationNode(ASTNode):
    def __init__(self, name, value_node):
        self.name = name
        self.value_node = value_node

class AssignmentNode(ASTNode):
    def __init__(self, name, value_node):
        self.name = name
        self.value_node = value_node

class PrintNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class InputNode(ASTNode):
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class LoopNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"{self.elements}"

class FunctionDefNode(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def __repr__(self):
        return f"<function {self.name}>"

class FunctionCallNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<call {self.name}>"
