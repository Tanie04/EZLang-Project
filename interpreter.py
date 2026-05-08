class Interpreter:
    def __init__(self, env):
        self.env = env

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name)
        return visitor(node)

    def visit_NumberNode(self, node): return node.value
    def visit_StringNode(self, node): return node.value
    def visit_VariableNode(self, node): return self.env.lookup(node.name)
    
    def visit_DeclarationNode(self, node):
        return self.env.declare(node.name, self.visit(node.value_node))
    
    def visit_AssignmentNode(self, node):
        return self.env.assign(node.name, self.visit(node.value_node))
    
    def visit_PrintNode(self, node):
        val = self.visit(node.expression)
        # Handle string representation of lists
        if isinstance(val, list):
            output = "[" + ", ".join(str(x) for x in val) + "]"
        else:
            output = val
        print(f"[EZLang Output]: {output}")
        return output

    def visit_BinOpNode(self, node):
        l, r = self.visit(node.left), self.visit(node.right)
        op = node.op
        if op == 'PLUS':
            # Handle string concatenation safely
            if isinstance(l, str) or isinstance(r, str):
                return str(l) + str(r)
            return l + r
        if op == 'MINUS': return l - r
        if op == 'MUL': return l * r
        if op == 'DIV':
            if r == 0: raise RuntimeError("Division by zero")
            return l / r
        if op == 'MOD': return l % r
        if op == 'EQ': return 1 if l == r else 0
        if op == 'GT': return 1 if l > r else 0
        if op == 'LT': return 1 if l < r else 0
        if op == 'GE': return 1 if l >= r else 0
        if op == 'LE': return 1 if l <= r else 0
        if op == 'AND': return 1 if l and r else 0
        if op == 'OR': return 1 if l or r else 0

    def visit_UnaryOpNode(self, node):
        v = self.visit(node.node)
        return -v if node.op == 'MINUS' else (0 if v else 1)

    def visit_IfNode(self, node):
        if self.visit(node.condition):
            for s in node.true_block: self.visit(s)
        else:
            for s in node.false_block: self.visit(s)

    def visit_LoopNode(self, node):
        while True:
            for s in node.body: self.visit(s)
            if self.visit(node.condition): break

    def visit_ListNode(self, node):
        return [self.visit(element) for element in node.elements]

    def visit_FunctionDefNode(self, node):
        # We store the function body directly in the environment variables
        self.env.declare(node.name, {'is_function': True, 'body': node.body})

    def visit_FunctionCallNode(self, node):
        func = self.env.lookup(node.name)
        if not isinstance(func, dict) or not func.get('is_function'):
            raise RuntimeError(f"'{node.name}' is not a function")
        
        # Execute the function body
        for s in func['body']:
            self.visit(s)