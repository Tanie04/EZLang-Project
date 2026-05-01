from nodes import *
from environment import Environment
from lexer import Lexer
from parser import Parser

class Interpreter:
    def __init__(self, env):
        self.env = env

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node):
        return node.value

    def visit_VariableNode(self, node):
        return self.env.lookup(node.name)

    def visit_DeclarationNode(self, node):
        value = self.visit(node.value_node)
        self.env.declare(node.name, value)
        return value

    def visit_AssignmentNode(self, node):
        value = self.visit(node.value_node)
        self.env.assign(node.name, value)
        return value

    def visit_PrintNode(self, node):
        value = self.visit(node.expression)
        print(f"[EZLang Output]: {value}")
        return value
    
    def visit_StringNode(self, node):
        return node.value

if __name__ == "__main__":
    source_code = '''
    let a = 10.
    let b = 20.
    set a to 50.
    print a.
    print b.
    print "Project completed by Yen Nhi".
    '''
    
    try:
        env = Environment()
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter(env)
        
        print("--- Start Executing ---")
        for statement in ast:
            interpreter.visit(statement)
        print("--- Execution Finished ---")
        
    except NameError as e:
        print(f"Semantic Error: {e}")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")