#Build an AST tree from the tokens
from lexer import Lexer
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        """Move to the next token in the list."""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        """Main entry point: Program = { Statement }"""
        statements = []
        while self.current_token is not None:
            # Skip empty lines or stray dots
            if self.current_token[0] in ('NEWLINE', 'DOT'):
                self.advance()
                continue
            statements.append(self.statement())
        return statements

    def statement(self):
        """Determine the statement type based on the leading keyword."""
        token_type = self.current_token[0]
        
        if token_type == 'LET':
            return self.let_statement()
        elif token_type == 'SET':
            return self.set_statement()
        elif token_type == 'PRINT':
            return self.print_statement()
        elif token_type == 'WHEN':
            return self.when_statement()
        
        raise SyntaxError(f"Parser Error: Unexpected token {self.current_token} at position {self.pos}")

    def let_statement(self):
        """Parse: let <ID> = <EXPRESSION>."""
        self.advance() # Skip 'let'
        if self.current_token[0] != 'ID':
            raise SyntaxError("Expected identifier after 'let'")
        
        var_name = self.current_token[1]
        self.advance() # Skip ID
        
        if self.current_token[0] != 'ASSIGN':
            raise SyntaxError("Expected '=' in variable declaration")
            
        self.advance() # Skip '='
        value = self.expression()
        return DeclarationNode(var_name, value)

    def set_statement(self):
        """Parse: set <ID> to <EXPRESSION>."""
        self.advance() # Skip 'set'
        var_name = self.current_token[1]
        self.advance() # Skip ID
        
        if self.current_token[0] != 'TO':
            raise SyntaxError("Expected 'to' in assignment statement")
            
        self.advance() # Skip 'to'
        value = self.expression()
        return AssignmentNode(var_name, value)

    def print_statement(self):
        """Parse: print <EXPRESSION>."""
        self.advance() # Skip 'print'
        value = self.expression()
        return PrintNode(value)

    def expression(self):
        """Handle basic literals and identifiers."""
        token_type, token_val = self.current_token
        
        if token_type == 'NUMBER':
            self.advance()
            return NumberNode(token_val)
        elif token_type == 'ID':
            self.advance()
            return VariableNode(token_val)
        elif token_type == 'STRING':
            self.advance()
            return StringNode(token_val)
            
        raise SyntaxError(f"Expected expression but found {token_type}")

# --- EXECUTION FOR TESTING ---
if __name__ == "__main__":
    code = '''
    let x = 10.
    set x to 20.
    print x.
    '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("--- AST STRUCTURE ---")
        for node in ast:
            print(node)
    except Exception as e:
        print(f"Compilation Error: {e}")