from nodes import *

class Interpreter:
    def __init__(self, env):
        self.env = env

    def visit(self, node):
        method = f'visit_{type(node).__name__}'
        visitor = getattr(self, method)
        return visitor(node)

    def visit_NumberNode(self, node): return node.value
    def visit_StringNode(self, node): return node.value
    def visit_VariableNode(self, node): return self.env.lookup(node.name)

    def visit_ListNode(self, node):
        return [self.visit(x) for x in node.elements]

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right) 
        # Xử lý phép cộng (Số + Số HOẶC Chuỗi + Chuỗi)
        if node.op == 'PLUS':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
            
        if node.op == 'MINUS': return left - right
        if node.op == 'MUL': return left * right
        if node.op == 'DIV': return left / right
        if node.op == 'MOD': return left % right
        if node.op == 'GT': return left > right
        if node.op == 'LT': return left < right
        if node.op == 'GE': return left >= right
        if node.op == 'LE': return left <= right
        if node.op == 'EQ': return left == right
        if node.op == 'AND': return left and right
        if node.op == 'OR': return left or right

    def visit_UnaryOpNode(self, node):
        val = self.visit(node.operand)
        if node.op == 'MINUS': return -val
        if node.op == 'NOT': return not val

    def visit_DeclarationNode(self, node):
        val = self.visit(node.value_node)
        self.env.declare(node.name, val)

    def visit_AssignmentNode(self, node):
        val = self.visit(node.value_node)
        self.env.assign(node.name, val)

    def visit_PrintNode(self, node):
        print(self.visit(node.expression))

    def visit_InputNode(self, node):
        # Sửa lỗi: Dùng input() để nhận dữ liệu thực tế
        val = input(node.prompt + " ")

        # Cố gắng chuyển sang số nếu có thể, không thì giữ là chuỗi
        try:
            if '.' in val: val = float(val)
            else: val = int(val)
        except ValueError:
            pass
        self.env.declare(node.name, val)

    def visit_IfNode(self, node):
        if self.visit(node.condition):
            for stmt in node.then_block:
                self.visit(stmt)
        else:
            for stmt in node.else_block:
                self.visit(stmt)

    def visit_LoopNode(self, node):
        # Thực hiện Body trước khi check điều kiện (theo EBNF của Nam)
        while True:
            for stmt in node.body:
                self.visit(stmt)
            if self.visit(node.condition):
                break

    def visit_FunctionDefNode(self, node):
        self.env.functions[node.name] = node

    def visit_FunctionCallNode(self, node):
        if node.name not in self.env.functions:
            raise Exception(f"Undefined function '{node.name}'")
        func = self.env.functions[node.name]
        for stmt in func.body:
            self.visit(stmt)
