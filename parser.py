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

    def peek(self):
        next_pos = self.pos + 1
        if next_pos < len(self.tokens):
            return self.tokens[next_pos]
        return None

    def parse(self):
        statements = []
        while self.current_token is not None:
            if self.current_token[0] in ('NEWLINE', 'DOT'):
                self.advance()
                continue
            stmt = self.statement()
            statements.append(stmt)
            if self.current_token and self.current_token[0] == 'DOT':
                self.advance()
        return statements

    def statement(self):
        token_type = self.current_token[0]
        if token_type == 'LET':
            return self.variable_decl()
        if token_type == 'SET':
            return self.assignment()
        if token_type == 'PRINT':
            return self.print_stmt()
        if token_type == 'INPUT':
            return self.input_stmt()
        if token_type == 'WHEN':
            return self.if_stmt()
        if token_type == 'KEEP_GOING':
            return self.loop_stmt()
        if token_type == 'DEFINE_TASK':
            return self.function_def()
        if token_type == 'ID' and self.peek() and self.peek()[0] == 'DOT':
            return self.function_call()
        raise SyntaxError(f"Invalid statement: {token_type}")

    def variable_decl(self):
        self.advance()
        name = self.current_token[1]
        self.advance()
        self.advance()
        value = self.expression()
        return DeclarationNode(name, value)

    def assignment(self):
        self.advance()
        name = self.current_token[1]
        self.advance()
        self.advance()
        value = self.expression()
        return AssignmentNode(name, value)

    def print_stmt(self):
        self.advance()
        value = self.expression()
        return PrintNode(value)

    def input_stmt(self):
        self.advance()
        name = self.current_token[1]
        self.advance()
        self.advance()
        prompt = self.current_token[1]
        self.advance()
        return InputNode(name, prompt)

    def if_stmt(self):
        self.advance()
        condition = self.condition()
        if self.current_token[0] != 'THEN':
            raise SyntaxError("Expected 'then'")
        self.advance()
        then_block = []
        else_block = []
        while self.current_token and self.current_token[0] not in ('ELSE', 'STOP'):
            if self.current_token[0] in ('NEWLINE', 'DOT'):
                self.advance()
                continue
            then_block.append(self.statement())
            if self.current_token and self.current_token[0] == 'DOT':
                self.advance()
        if self.current_token and self.current_token[0] == 'ELSE':
            self.advance()
            while self.current_token and self.current_token[0] != 'STOP':
                if self.current_token[0] in ('NEWLINE', 'DOT'):
                    self.advance()
                    continue
                else_block.append(self.statement())
                if self.current_token and self.current_token[0] == 'DOT':
                    self.advance()
        if self.current_token[0] != 'STOP':
            raise SyntaxError("Expected 'stop'")
        self.advance()
        return IfNode(condition, then_block, else_block)

    def loop_stmt(self):
        self.advance()
        if self.current_token[0] != 'COLON':
            raise SyntaxError(f"Expected ':' but found {self.current_token[0]}")
        self.advance()
        body = []
        while self.current_token and self.current_token[0] != 'UNTIL':
            if self.current_token[0] in ('NEWLINE', 'DOT'):
                self.advance()
                continue
            stmt = self.statement()
            body.append(stmt)
            if self.current_token and self.current_token[0] == 'DOT':
                self.advance()
        if not self.current_token or self.current_token[0] != 'UNTIL':
            raise SyntaxError("Expected 'until' at end of loop")
        self.advance()
        condition = self.condition()
        return LoopNode(condition, body)

    def function_def(self):
        self.advance()
        name = self.current_token[1]
        self.advance()
        body = []
        while self.current_token and self.current_token[0] != 'END_TASK':
            if self.current_token[0] in ('NEWLINE', 'DOT'):
                self.advance()
                continue
            body.append(self.statement())
            if self.current_token and self.current_token[0] == 'DOT':
                self.advance()
        if not self.current_token:
            raise SyntaxError("Expected 'end task'")
        self.advance()
        return FunctionDefNode(name, body)

    def function_call(self):
        name = self.current_token[1]
        self.advance()
        return FunctionCallNode(name)

    def condition(self):
        node = self.and_expr()
        while self.current_token and self.current_token[0] == 'OR':
            op = self.current_token[0]
            self.advance()
            node = BinOpNode(node, op, self.and_expr())
        return node

    def and_expr(self):
        node = self.not_expr()
        while self.current_token and self.current_token[0] == 'AND':
            op = self.current_token[0]
            self.advance()
            node = BinOpNode(node, op, self.not_expr())
        return node

    def not_expr(self):
        if self.current_token[0] == 'NOT':
            self.advance()
            return UnaryOpNode('NOT', self.comparison())
        return self.comparison()

    def comparison(self):
        left = self.expression()
        if self.current_token and self.current_token[0] in ('GT', 'LT', 'EQ', 'GE', 'LE'):
            op = self.current_token[0]
            self.advance()
            return BinOpNode(left, op, self.expression())
        return left

    def expression(self):
        node = self.mul_expr()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[0]
            self.advance()
            node = BinOpNode(node, op, self.mul_expr())
        return node

    def mul_expr(self):
        node = self.unary_expr()
        while self.current_token and self.current_token[0] in ('MUL', 'DIV', 'MOD'):
            op = self.current_token[0]
            self.advance()
            node = BinOpNode(node, op, self.unary_expr())
        return node

    def unary_expr(self):
        if self.current_token[0] == 'MINUS':
            self.advance()
            return UnaryOpNode('MINUS', self.primary())
        return self.primary()

    def primary(self):
        token = self.current_token
        if token[0] == 'NUMBER':
            self.advance()
            return NumberNode(token[1])
        if token[0] == 'STRING':
            self.advance()
            return StringNode(token[1])
        if token[0] == 'ID':
            self.advance()
            return VariableNode(token[1])
        if token[0] == 'LBRACKET':
            return self.list_expr()
        if token[0] == 'LPAREN':
            self.advance()
            node = self.expression()
            if self.current_token[0] != 'RPAREN':
                raise SyntaxError("Expected ')'")
            self.advance()
            return node
        raise SyntaxError(f"Unexpected token: {token[0]}")

    def list_expr(self):
        elements = []
        self.advance()
        if self.current_token[0] != 'RBRACKET':
            elements.append(self.expression())
            while self.current_token[0] == 'COMMA':
                self.advance()
                elements.append(self.expression())
        if self.current_token[0] != 'RBRACKET':
            raise SyntaxError("Expected ']'")
        self.advance()
        return ListNode(elements)
