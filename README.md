1.Technical Implementation & Architecture
This section describes how the team implemented the Syntactic & Semantic Specification requirements through a modular structure:
- Lexical Analysis (lexer.py):
    + Uses regular expressions to identify sets of tokens (Identifiers, Keywords, Operators).
    + Handles lexical errors from the very beginning of the interpretation flow.

- Syntax Analysis (parser.py & nodes.py):
    + Applies the Recursive Descent Parsing method to build an Abstract Syntax Tree (AST).
    + Each language structure (Assignment, Print, Binary Ops) is represented by a specific node in nodes.py.

- Scope & Storage Management (environment.py):
    + Manages runtime representations of variables.
    + Supports scope-based storage, ensuring data encapsulation as required by the Syllabus.

- Interpretation Process (interpreter.py): uses the Visitor Pattern algorithm to traverse the AST tree and execute semantic logic.