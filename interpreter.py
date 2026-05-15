# interpreter.py — AST Visitor / Execution Engine
# Fixes applied:
#   1. visit_FunctionCallNode now creates a child scope so function-local
#      variables do not pollute the global environment.
#   2. visit_FunctionCallNode produces a clear, actionable error message
#      when an identifier that is not a function is called as one.
#   3. visit_BinOpNode now raises RuntimeError for unknown operators
#      instead of silently returning None.

from environment import Environment


class Interpreter:
    def __init__(self, env):
        self.env = env

    # ------------------------------------------------------------------
    # Visitor dispatch
    # ------------------------------------------------------------------

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._no_visitor)
        return visitor(node)

    def _no_visitor(self, node):
        raise RuntimeError(
            f"Interpreter Error: No visit method implemented for node type "
            f"'{type(node).__name__}'."
        )

    # ------------------------------------------------------------------
    # Literals & Variables
    # ------------------------------------------------------------------

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_VariableNode(self, node):
        return self.env.lookup(node.name)

    # ------------------------------------------------------------------
    # Variable management
    # ------------------------------------------------------------------

    def visit_DeclarationNode(self, node):
        value = self.visit(node.value_node)
        return self.env.declare(node.name, value)

    def visit_AssignmentNode(self, node):
        value = self.visit(node.value_node)
        return self.env.assign(node.name, value)

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def visit_PrintNode(self, node):
        val = self.visit(node.expression)
        if isinstance(val, list):
            output = "[" + ", ".join(str(x) for x in val) + "]"
        else:
            output = val
        print(f"[EZLang Output]: {output}")
        return output

    # ------------------------------------------------------------------
    # Expressions
    # ------------------------------------------------------------------

    def visit_BinOpNode(self, node):
        l = self.visit(node.left)
        r = self.visit(node.right)
        op = node.op

        if op == 'PLUS':
            # String concatenation when either side is a string
            if isinstance(l, str) or isinstance(r, str):
                return str(l) + str(r)
            return l + r
        if op == 'MINUS':
            return l - r
        if op == 'MUL':
            return l * r
        if op == 'DIV':
            if r == 0:
                raise RuntimeError("Runtime Error: Division by zero.")
            return l / r
        if op == 'MOD':
            if r == 0:
                raise RuntimeError("Runtime Error: Modulo by zero.")
            return l % r
        if op == 'EQ':
            return 1 if l == r else 0
        if op == 'GT':
            return 1 if l > r else 0
        if op == 'LT':
            return 1 if l < r else 0
        if op == 'GE':
            return 1 if l >= r else 0
        if op == 'LE':
            return 1 if l <= r else 0
        if op == 'AND':
            return 1 if l and r else 0
        if op == 'OR':
            return 1 if l or r else 0

        # Catch-all: should never reach here with a well-formed AST
        raise RuntimeError(f"Runtime Error: Unknown binary operator '{op}'.")

    def visit_UnaryOpNode(self, node):
        v = self.visit(node.node)
        if node.op == 'MINUS':
            return -v
        if node.op == 'NOT':
            return 0 if v else 1
        raise RuntimeError(f"Runtime Error: Unknown unary operator '{node.op}'.")

    # ------------------------------------------------------------------
    # Control flow
    # ------------------------------------------------------------------

    def visit_IfNode(self, node):
        if self.visit(node.condition):
            for stmt in node.true_block:
                self.visit(stmt)
        else:
            for stmt in node.false_block:
                self.visit(stmt)

    def visit_LoopNode(self, node):
        while True:
            for stmt in node.body:
                self.visit(stmt)
            if self.visit(node.condition):
                break

    # ------------------------------------------------------------------
    # Collections
    # ------------------------------------------------------------------

    def visit_ListNode(self, node):
        return [self.visit(element) for element in node.elements]

    # ------------------------------------------------------------------
    # Functions — FIX: child scope isolates local variables
    # ------------------------------------------------------------------

    def visit_FunctionDefNode(self, node):
        """
        Store the function's body in the current environment.
        Functions are stored as plain dicts with an 'is_function' sentinel
        so the interpreter can distinguish them from ordinary variables.
        """
        self.env.declare(node.name, {'is_function': True, 'body': node.body})

    def visit_FunctionCallNode(self, node):
        """
        Execute a previously-defined task.

        Fix 1 — child scope: creates a fresh Environment whose parent is the
        current scope. Variables declared inside the function stay local;
        they are garbage-collected when the child env goes out of use.
        Variables from the enclosing scope are still readable (and writable
        via the parent-chain assign) so global state modification still works.

        Fix 2 — clear error: if the name exists but is not a function, the
        error message now names the identifier and explains the problem
        instead of producing a confusing generic RuntimeError.
        """
        func = self.env.lookup(node.name)

        if not isinstance(func, dict) or not func.get('is_function'):
            raise RuntimeError(
                f"Runtime Error: '{node.name}' is a variable, not a task. "
                f"Did you mean to call a task defined with 'define task'?"
            )

        # Create an isolated local scope for this call
        local_env = self.env.create_child_scope()
        local_interpreter = Interpreter(local_env)

        for stmt in func['body']:
            local_interpreter.visit(stmt)

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def visit_InputNode(self, node):
        """
        Display a prompt, read user input, and coerce the value to a number
        when possible. The variable is auto-declared in the current scope if
        it does not already exist (matching the original behaviour).
        """
        raw = input(node.prompt)

        # Attempt numeric coercion
        try:
            value = float(raw) if '.' in raw else int(raw)
        except ValueError:
            value = raw  # keep as string

        # Auto-declare if the variable doesn't exist yet in any scope
        try:
            self.env.assign(node.name, value)
        except NameError:
            self.env.declare(node.name, value)

        return value