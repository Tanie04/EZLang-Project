# EZLang-Project 🚀

EZLang is a custom, lightweight programming language developed as a class project. It features an intuitive syntax and a fully functional interpreter built entirely in Python.

##  Features
- **Variables & Data Types:** Integers, Floats, Strings, and Lists.
- **Control Flow:** `when...then...else` conditional blocks.
- **Loops:** `keep going...until` statements.
- **Functions:** Custom tasks definition and execution (`define task`).
- **Math & Logic:** Full operator precedence (PEMDAS) and boolean logic (`and`, `or`, `not`).

##  Technical Implementation & Architecture
This project is structured modularly, strictly following the compilation pipeline:

1. **Lexical Analysis (`lexer.py`)**
   - Uses Regular Expressions (Regex) to tokenize raw source code into sets of tokens (Identifiers, Keywords, Operators).
   - Handles lexical errors at the very beginning of the interpretation flow.

2. **Syntax Analysis (`parser.py` & `nodes.py`)**
   - Applies the **Recursive Descent Parsing** method to build an Abstract Syntax Tree (AST).
   - Handles operator precedence logically and structurally.
   - Each language construct (Assignment, Print, Binary Ops, Loops, Functions) is represented by a specific node in `nodes.py`.

3. **Scope & Storage Management (`environment.py`)**
   - Serves as the Symbol Table.
   - Manages the runtime representation of variables and functions.
   - Supports scope-based storage and strictly enforces declaration rules (catching Semantic Errors like re-declaration).

4. **Execution Engine (`interpreter.py`)**
   - Uses the **Visitor Pattern** algorithm to traverse the AST.
   - Executes the semantic logic for math, logic, state changes, and block routing.

5. **Test-Driven Reliability (`test_suite.py`)**
   - Includes a professional automated test runner ensuring syntax, semantics, and algorithmic stability across all language features.