class ASTNode: pass

class NumberNode(ASTNode):
    def __init__(self, value): self.value = value
class StringNode(ASTNode):
    def __init__(self, value): self.value = value
class VariableNode(ASTNode):
    def __init__(self, name): self.name = name

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op, node):
        self.op = op
        self.node = node

class DeclarationNode(ASTNode):
    def __init__(self, name, value_node):
        self.name = name
        self.value_node = value_node

class AssignmentNode(ASTNode):
    def __init__(self, name, value_node):
        self.name = name
        self.value_node = value_node

class PrintNode(ASTNode):
    def __init__(self, expression): self.expression = expression

class IfNode(ASTNode):
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

class LoopNode(ASTNode):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

class ListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class FunctionDefNode(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class FunctionCallNode(ASTNode):
    def __init__(self, name):
        self.name = name

class InputNode(ASTNode):
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt