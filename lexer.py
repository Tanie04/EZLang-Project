import re

TOKEN_SPEC = [
    ('KEEP_GOING', r'\bkeep\s+going\b'),
    ('UNTIL',      r'\buntil\b'),
    ('WHEN',       r'\bwhen\b'),
    ('THEN',       r'\bthen\b'),
    ('ELSE',       r'\belse\b'),
    ('STOP',       r'\bstop\b'),
    ('LET',        r'\blet\b'),
    ('SET',        r'\bset\b'),
    ('TO',         r'\bto\b'),
    ('PRINT',      r'\bprint\b'),
    ('INPUT',      r'\binput\b'),
    ('WITH',       r'\bwith\b'),
    ('AND',        r'\band\b'),
    ('OR',         r'\bor\b'),
    ('NOT',        r'\bnot\b'),
    ('MOD',        r'\bmod\b'),
    ('NUMBER',     r'\d+(\.\d+)?'),
    ('STRING',     r'"[^"]*"'),
    ('ID',         r'[a-zA-Z_]\w*'),
    ('EQ',         r'=='),
    ('GE',         r'>='),
    ('LE',         r'<='),
    ('ASSIGN',     r'='),
    ('PLUS',       r'\+'),
    ('MINUS',      r'-'),
    ('MUL',        r'\*'),
    ('DIV',        r'/'),
    ('GT',         r'>'),
    ('LT',         r'<'),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('DOT',        r'\.'),
    ('COLON',      r':'),
    ('SKIP',       r'[ \t]+'),
    ('NEWLINE',    r'\n'),
    ('MISMATCH',   r'.'),
    ('LBRACKET',  r'\['),
    ('RBRACKET',  r'\]'),
    ('COMMA',     r','),
    ('DEFINE_TASK', r'\bdefine\s+task\b'),
    ('END_TASK', r'\bend\s+task\b'),
]

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code

    def tokenize(self):
        tokens = []
        regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
        for match in re.finditer(regex, self.source_code):
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
