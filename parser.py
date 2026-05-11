# parser.py — Recursive Descent Parser
# Fixes applied:
#   1. primary() now guards against None current_token (EOF crash fix).
#   2. statement() now guards against None current_token (EOF crash fix).
#   3. function_call_stmt() produces a more diagnostic error so that calling
#      a variable by mistake gives a helpful parser-level message.
#   4. All expect() failures now include the current token in the message
#      for easier debugging.

from nodes import (
    NumberNode, StringNode, VariableNode,
    BinOpNode, UnaryOpNode,
    DeclarationNode, AssignmentNode,
    PrintNode, IfNode, LoopNode,
    ListNode, FunctionDefNode, FunctionCallNode,
    InputNode,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def advance(self):
        self.pos += 1
        self.current_token = (
            self.tokens[self.pos] if self.pos < len(self.tokens) else None
        )

    def expect(self, token_type, error_msg):
        """
        Consume the current token if it matches token_type, otherwise raise
        SyntaxError with a message that includes what was actually found.
        """
        if not self.current_token or self.current_token[0] != token_type:
            found = (
                f"'{self.current_token[1]}' ({self.current_token[0]})"
                if self.current_token
                else "end of input"
            )
            raise SyntaxError(f"{error_msg} — got {found} instead.")
        self.advance()

    # ------------------------------------------------------------------
    # Top-level parse
    # ------------------------------------------------------------------

    def parse(self):
        statements = []
        while self.current_token:
            if self.current_token[0] in ('NEWLINE', 'DOT'):
                self.advance()
                continue
            statements.append(self.statement())
        return statements

    # ------------------------------------------------------------------
    # Statement dispatch — Fix: guard against unexpected EOF
    # ------------------------------------------------------------------

    def statement(self):
        # Fix 2: explicit EOF check before reading current_token[0]
        if not self.current_token:
            raise SyntaxError(
                "Syntax Error: Unexpected end of input — expected a statement."
            )

        t = self.current_token[0]

        if t == 'INPUT':      return self.input_stmt()
        if t == 'LET':        return self.let_stmt()
        if t == 'SET':        return self.set_stmt()
        if t == 'PRINT':      return self.print_stmt()
        if t == 'WHEN':       return self.when_stmt()
        if t == 'KEEP_GOING': return self.loop_stmt()
        if t == 'DEFINE':     return self.function_def_stmt()
        if t == 'ID':         return self.function_call_stmt()

        raise SyntaxError(
            f"Syntax Error: Unexpected token '{self.current_token[1]}' "
            f"({t}) at position {self.pos}."
        )

    # ------------------------------------------------------------------
    # Individual statement parsers
    # ------------------------------------------------------------------

    def let_stmt(self):
        self.advance()                              # consume 'let'
        name = self.current_token[1]
        self.advance()                              # consume identifier
        self.expect('ASSIGN', "Expected '=' after variable name")
        val = self.expression()
        self.expect('DOT', "Expected '.' to end 'let' statement")
        return DeclarationNode(name, val)

    def set_stmt(self):
        self.advance()                              # consume 'set'
        name = self.current_token[1]
        self.advance()                              # consume identifier
        self.expect('TO', "Expected 'to' after variable name in 'set'")
        val = self.expression()
        self.expect('DOT', "Expected '.' to end 'set' statement")
        return AssignmentNode(name, val)

    def print_stmt(self):
        self.advance()                              # consume 'print'
        val = self.expression()
        self.expect('DOT', "Expected '.' to end 'print' statement")
        return PrintNode(val)

    def when_stmt(self):
        self.advance()                              # consume 'when'
        cond = self.expression()
        self.expect('THEN', "Expected 'then' after condition in 'when'")

        true_b = []
        while self.current_token and self.current_token[0] not in ('ELSE', 'STOP'):
            true_b.append(self.statement())

        false_b = []
        if self.current_token and self.current_token[0] == 'ELSE':
            self.advance()                          # consume 'else'
            while self.current_token and self.current_token[0] != 'STOP':
                false_b.append(self.statement())

        self.expect('STOP', "Missing 'stop'")
        self.expect('DOT', "Expected '.' after 'stop'")
        return IfNode(cond, true_b, false_b)

    def loop_stmt(self):
        self.advance()                              # consume 'keep going'
        self.expect('COLON', "Expected ':' after 'keep going'")

        body = []
        while self.current_token and self.current_token[0] != 'UNTIL':
            body.append(self.statement())

        self.expect('UNTIL', "Expected 'until' to close loop")
        cond = self.expression()
        self.expect('DOT', "Expected '.' after loop condition")
        return LoopNode(body, cond)

    def function_def_stmt(self):
        self.advance()                              # consume 'define'
        self.expect('TASK', "Expected 'task' after 'define'")

        if not self.current_token or self.current_token[0] != 'ID':
            raise SyntaxError("Expected a task name (identifier) after 'define task'.")
        name = self.current_token[1]
        self.advance()                              # consume task name

        body = []
        while self.current_token and self.current_token[0] != 'END':
            body.append(self.statement())

        self.expect('END', "Expected 'end' to close task definition")
        self.expect('TASK', "Expected 'task' after 'end'")
        self.expect('DOT', "Expected '.' after 'end task'")
        return FunctionDefNode(name, body)

    def function_call_stmt(self):
        """
        Fix 3 — clearer diagnostics: an identifier followed by '.' is treated
        as a function call. If the dot is missing we raise a helpful message
        instead of a generic 'Expected DOT' that gives no context.
        """
        name = self.current_token[1]
        self.advance()                              # consume identifier

        if not self.current_token or self.current_token[0] != 'DOT':
            found = (
                f"'{self.current_token[1]}'"
                if self.current_token
                else "end of input"
            )
            raise SyntaxError(
                f"Syntax Error: Expected '.' after '{name}' to call it as a task, "
                f"but got {found}. "
                f"If '{name}' is a variable, it cannot appear as a standalone statement."
            )

        self.advance()                              # consume '.'
        return FunctionCallNode(name)

    def input_stmt(self):
        self.advance()                              # consume 'input'

        if not self.current_token or self.current_token[0] != 'ID':
            raise SyntaxError("Expected a variable name after 'input'.")
        name = self.current_token[1]
        self.advance()                              # consume variable name

        self.expect('WITH', "Expected 'with' in input statement")

        if not self.current_token or self.current_token[0] != 'STRING':
            raise SyntaxError("Expected a string prompt after 'with' in input statement.")
        prompt = self.current_token[1]
        self.advance()                              # consume prompt string

        self.expect('DOT', "Expected '.' to end input statement")
        return InputNode(name, prompt)

    # ------------------------------------------------------------------
    # Expression parsing — PEMDAS enforced structurally
    # ------------------------------------------------------------------

    def expression(self):
        return self.or_expr()

    def or_expr(self):
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
        if self.current_token and self.current_token[0] == 'NOT':
            op = self.current_token[0]
            self.advance()
            return UnaryOpNode(op, self.comparison())
        return self.comparison()

    def comparison(self):
        node = self.add_expr()
        if self.current_token and self.current_token[0] in ('EQ', 'GT', 'LT', 'GE', 'LE'):
            op = self.current_token[0]
            self.advance()
            node = BinOpNode(node, op, self.add_expr())
        return node

    def add_expr(self):
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
        if self.current_token and self.current_token[0] == 'MINUS':
            op = self.current_token[0]
            self.advance()
            return UnaryOpNode(op, self.unary_expr())
        return self.primary()

    def primary(self):
        # Fix 1: explicit EOF guard — prevents TypeError from unpacking None
        if not self.current_token:
            raise SyntaxError(
                "Syntax Error: Unexpected end of input — expected a value or expression."
            )

        t_type, t_val = self.current_token

        if t_type == 'NUMBER':
            self.advance()
            return NumberNode(t_val)

        if t_type == 'STRING':
            self.advance()
            return StringNode(t_val)

        if t_type == 'ID':
            self.advance()
            return VariableNode(t_val)

        if t_type == 'LPAREN':
            self.advance()
            node = self.expression()
            self.expect('RPAREN', "Expected closing ')'")
            return node

        if t_type == 'LBRACKET':
            self.advance()
            elements = []
            # Handle empty list []
            if self.current_token and self.current_token[0] != 'RBRACKET':
                elements.append(self.expression())
                while self.current_token and self.current_token[0] == 'COMMA':
                    self.advance()
                    elements.append(self.expression())
            self.expect('RBRACKET', "Expected closing ']' in list literal")
            return ListNode(elements)

        raise SyntaxError(
            f"Syntax Error: Unexpected token '{t_val}' ({t_type}) — "
            f"expected a number, string, variable, or '('."
        )