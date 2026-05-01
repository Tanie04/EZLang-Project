from lexer import Lexer
from parser import Parser
from environment import Environment
from interpreter import Interpreter

def run_compiler(source_code):
    """
    This function coordinates the full compilation and execution pipeline:
    Source Code -> Lexer -> Tokens -> Parser -> AST -> Interpreter -> Output
    """
    try:
        print("--- EZLang System Initialization ---")
        
        # 1. Lexical Analysis: Break source code into tokens
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # 2. Syntax Analysis: Build the Abstract Syntax Tree (AST)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 3. Environment Setup: Create a memory space for variables
        env = Environment()
        
        # 4. Execution: Interpret the AST nodes
        interpreter = Interpreter(env)
        
        print("--- Start Executing Program ---")
        for node in ast:
            interpreter.visit(node)
        print("--- Execution Completed Successfully ---")

    except SyntaxError as e:
        print(f"[Syntax Error]: {e}")
    except NameError as e:
        print(f"[Semantic Error]: {e}")
    except Exception as e:
        print(f"[Runtime Error]: {e}")

if __name__ == "__main__":
    # Test script including variables, assignments, and string output
    ezlang_code = '''
    let a = 10.
    let b = 20.
    set a to 50.
    print a.
    print b.
    print "EZLang Project - Done developed".
    '''
    
    run_compiler(ezlang_code)