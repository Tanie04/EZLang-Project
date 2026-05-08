from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def expect(self, token_type, error_msg):
        if not self.current_token or self.current_token[0] != token_type:
            raise SyntaxError(error_msg)
        self.advance()

    def parse(self):
        statements = []
        while self.current_token:
            if self.current_token[0] in ('NEWLINE', 'DOT'):
                self.advance()
                continue
            statements.append(self.statement())
        return statements

    def statement(self):
        t = self.current_token[0]
        if t == 'LET': return self.let_stmt()
        if t == 'SET': return self.set_stmt()
        if t == 'PRINT': return self.print_stmt()
        if t == 'WHEN': return self.when_stmt()
        if t == 'KEEP_GOING': return self.loop_stmt()
        if t == 'DEFINE': return self.function_def_stmt()
        if t == 'ID': return self.function_call_stmt()
        raise SyntaxError(f"Parser Error: Unexpected token {self.current_token} at position {self.pos}")

    def let_stmt(self):
        self.advance()
        name = self.current_token[1]
        self.advance()
        self.expect('ASSIGN', "Expected '='")
        val = self.expression()
        self.expect('DOT', "Expected '.'")
        return DeclarationNode(name, val)

    def set_stmt(self):
        self.advance()
        name = self.current_token[1]
        self.advance()
        self.expect('TO', "Expected 'to'")
        val = self.expression()
        self.expect('DOT', "Expected '.'")
        return AssignmentNode(name, val)

    def print_stmt(self):
        self.advance()
        val = self.expression()
        self.expect('DOT', "Expected '.'")
        return PrintNode(val)

    def when_stmt(self):
        self.advance()
        cond = self.expression()
        self.expect('THEN', "Expected 'then'")
        true_b = []
        while self.current_token and self.current_token[0] not in ('ELSE', 'STOP'):
            true_b.append(self.statement())
        false_b = []
        if self.current_token and self.current_token[0] == 'ELSE':
            self.advance()
            while self.current_token and self.current_token[0] != 'STOP':
                false_b.append(self.statement())
        self.expect('STOP', "Missing 'stop'")
        self.expect('DOT', "Expected '.' after 'stop'")
        return IfNode(cond, true_b, false_b)

    def loop_stmt(self):
        self.advance()
        self.expect('COLON', "Expected ':'")
        body = []
        while self.current_token and self.current_token[0] != 'UNTIL':
            body.append(self.statement())
        self.expect('UNTIL', "Expected 'until'")
        cond = self.expression()
        self.expect('DOT', "Expected '.'")
        return LoopNode(body, cond)

    def function_def_stmt(self):
        self.advance() # skip define
        self.expect('TASK', "Expected 'task'")
        name = self.current_token[1]
        self.advance() # skip ID
        body = []
        while self.current_token and self.current_token[0] != 'END':
            body.append(self.statement())
        self.expect('END', "Expected 'end'")
        self.expect('TASK', "Expected 'task' after 'end'")
        self.expect('DOT', "Expected '.'")
        return FunctionDefNode(name, body)

    def function_call_stmt(self):
        name = self.current_token[1]
        self.advance() # skip ID
        self.expect('DOT', "Expected '.' for function call")
        return FunctionCallNode(name)

    # PEMDAS & Logic Expression Parsing
    def expression(self): return self.or_expr()
    
    def or_expr(self):
        node = self.and_expr()
        while self.current_token and self.current_token[0] == 'OR':
            op = self.current_token[0]; self.advance()
            node = BinOpNode(node, op, self.and_expr())
        return node
        
    def and_expr(self):
        # SỬA Ở ĐÂY: Gọi not_expr thay vì comparison
        node = self.not_expr()
        while self.current_token and self.current_token[0] == 'AND':
            op = self.current_token[0]; self.advance()
            node = BinOpNode(node, op, self.not_expr())
        return node

    # THÊM HÀM MỚI NÀY: Để tuân thủ đúng EBNF của nhóm
    def not_expr(self):
        if self.current_token and self.current_token[0] == 'NOT':
            op = self.current_token[0]; self.advance()
            return UnaryOpNode(op, self.comparison())
        return self.comparison()

    def comparison(self):
        node = self.add_expr()
        if self.current_token and self.current_token[0] in ('EQ', 'GT', 'LT', 'GE', 'LE'):
            op = self.current_token[0]; self.advance()
            node = BinOpNode(node, op, self.add_expr())
        return node
        
    def add_expr(self):
        node = self.mul_expr()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[0]; self.advance()
            node = BinOpNode(node, op, self.mul_expr())
        return node
        
    def mul_expr(self):
        node = self.unary_expr()
        while self.current_token and self.current_token[0] in ('MUL', 'DIV', 'MOD'):
            op = self.current_token[0]; self.advance()
            node = BinOpNode(node, op, self.unary_expr())
        return node
        
    def unary_expr(self):
        # SỬA Ở ĐÂY: Bỏ 'NOT' đi, chỉ giữ lại 'MINUS' cho số âm
        if self.current_token and self.current_token[0] == 'MINUS':
            op = self.current_token[0]; self.advance()
            return UnaryOpNode(op, self.unary_expr())
        return self.primary()
    
    def primary(self):
        t_type, t_val = self.current_token
        if t_type == 'NUMBER': self.advance(); return NumberNode(t_val)
        if t_type == 'STRING': self.advance(); return StringNode(t_val)
        if t_type == 'ID': self.advance(); return VariableNode(t_val)
        if t_type == 'LPAREN':
            self.advance(); node = self.expression()
            self.expect('RPAREN', "Expected ')'")
            return node
        if t_type == 'LBRACKET':
            self.advance()
            elements = []
            if self.current_token[0] != 'RBRACKET':
                elements.append(self.expression())
                while self.current_token[0] == 'COMMA':
                    self.advance()
                    elements.append(self.expression())
            self.expect('RBRACKET', "Expected ']'")
            return ListNode(elements)
        raise SyntaxError(f"Unexpected token {t_type}")