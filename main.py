# main.py — EZLang Entry Point
# Coordinates the full interpretation pipeline:
#   Source Code → Lexer → Tokens → Parser → AST → Interpreter → Output

from lexer import Lexer
from parser import Parser
from environment import Environment
from interpreter import Interpreter


def run_compiler(source_code):
    """
    Execute an EZLang program given as a plain string.

    Pipeline stages:
      1. Lexical Analysis  — tokenise raw source into a token stream
      2. Syntax Analysis   — parse tokens into an Abstract Syntax Tree
      3. Environment Setup — create the global symbol table / scope
      4. Interpretation    — walk the AST and execute each node

    Errors are caught at the appropriate stage and reported clearly.
    """
    try:
        print("--- EZLang System Initialization ---")

        # Stage 1: Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # Stage 2: Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()

        # Stage 3: Global Environment (root scope — no parent)
        env = Environment()

        # Stage 4: Execution
        interpreter = Interpreter(env)

        print("--- Start Executing Program ---")
        for node in ast:
            interpreter.visit(node)
        print("--- Execution Completed Successfully ---")

    except SyntaxError as e:
        print(f"[Syntax Error]: {e}")
    except NameError as e:
        print(f"[Semantic Error]: {e}")
    except RuntimeError as e:
        print(f"[Runtime Error]: {e}")
    except Exception as e:
        # Catch-all so the runner never crashes ungracefully
        print(f"[Internal Error]: {e}")


# ------------------------------------------------------------------
# Manual smoke-tests — run with: python main.py
# ------------------------------------------------------------------

if __name__ == "__main__":

    # --- Test 1: Basic variables and output ---
    print("\n========== Test 1: Basic Variables ==========")
    run_compiler('''
        let a = 10.
        let b = 20.
        set a to 50.
        print a.
        print b.
        print "EZLang — running correctly".
    ''')

    # --- Test 2: Scope isolation — local variable must NOT leak ---
    print("\n========== Test 2: Scope Isolation ==========")
    run_compiler('''
        let global_x = 100.

        define task localTest
            let local_var = 999.
            print local_var.
        end task.

        localTest.
        print global_x.
    ''')
    # Expected: local_var prints 999 inside the task, but is NOT accessible
    # in the global scope after the call (no crash, no pollution).

    # --- Test 3: Function modifying global state via scope chain ---
    print("\n========== Test 3: Global State Mutation from Task ==========")
    run_compiler('''
        let counter = 0.

        define task increment
            set counter to counter + 1.
        end task.

        increment.
        increment.
        increment.
        print counter.
    ''')
    # Expected output: 3

    # --- Test 4: EOF / malformed input produces clean SyntaxError ---
    print("\n========== Test 4: Clean EOF Error ==========")
    run_compiler('let x = .')
    # Expected: [Syntax Error]: Unexpected token ...

    # --- Test 5: Calling a variable as a task gives a clear error ---
    print("\n========== Test 5: Variable-as-task Error ==========")
    run_compiler('''
        let notATask = 42.
        notATask.
    ''')
    # Expected: [Runtime Error]: 'notATask' is a variable, not a task ...

    # --- Test 6: Fibonacci (algorithmic correctness) ---
    print("\n========== Test 6: Fibonacci (n=7, expected 13) ==========")
    run_compiler('''
        let a = 0.
        let b = 1.
        let temp = 0.
        let i = 0.
        keep going:
            set temp to a + b.
            set a to b.
            set b to temp.
            set i to i + 1.
        until i == 7.
        print b.
    ''')
    # Expected output: 13