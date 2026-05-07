from lexer import Lexer
from parser import Parser
from environment import Environment
from interpreter import Interpreter

def run(code):
    try:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        interp = Interpreter(Environment())
        for node in ast:
            interp.visit(node)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_code = '''
    let x = 10.
    input name with "Enter name:".
    when x > 5 then
       print "Hello " + name.
        print "Condition is true!".
    stop.

    keep going:
        set x to x - 1.
        print "Countdown:".
        print x.
    until x == 0.
    '''
    run(test_code)