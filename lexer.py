#Devide code into Tokens
import re

# Token specification
TOKEN_SPEC = [
    ('KEEP_GOING', r'\bkeep\s+going\b'),
    ('LET',        r'\blet\b'),
    ('SET',        r'\bset\b'),
    ('TO',         r'\bto\b'),
    ('PRINT',      r'\bprint\b'),
    ('WHEN',       r'\bwhen\b'),
    ('THEN',       r'\bthen\b'),
    ('STOP',       r'\bstop\b'),
    ('NUMBER',     r'\d+(\.\d+)?'),
    ('STRING',     r'"[^"]*"'),
    ('ID',         r'[a-zA-Z_]\w*'),
    ('ASSIGN',     r'='),
    ('PLUS',       r'\+'),
    ('DOT',        r'\.'),
    ('SKIP',       r'[ \t]+'),
    ('NEWLINE',    r'\n'),
    ('MISMATCH',   r'.'),
]

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code

    def tokenize(self):
        tokens = []
        master_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
        for match in re.finditer(master_regex, self.source_code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'STRING':
                value = value[1:-1]
            elif kind == 'SKIP' or kind == 'NEWLINE':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f"Unexpected character {value}")
            tokens.append((kind, value))
        return tokens

if __name__ == "__main__":
    test_code = "let x = 10."
    lexer_instance = Lexer(test_code) 
    print("Lexer is working! Output:")
    print(lexer_instance.tokenize())