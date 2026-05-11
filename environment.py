# environment.py — Symbol Table with Lexical Scoping
# Fix: Added parent-chain model so function calls get their own local scope,
# preventing variable pollution of the global environment.

class Environment:
    """
    Symbol Table to manage variable/function storage and retrieval.
    Supports lexical scoping via a parent-chain: each child environment
    delegates lookups to its parent when a name is not found locally.
    """

    def __init__(self, parent=None):
        # The primary storage for variable names and values in this scope
        self.variables = {}
        # Reference to the enclosing scope (None for the global scope)
        self.parent = parent

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def declare(self, name, value):
        """
        Used for 'let' statements and function definitions.
        Prevents re-declaration within the SAME scope (not parent scopes).
        """
        if name in self.variables:
            raise NameError(f"Semantic Error: Variable '{name}' is already declared in this scope.")
        self.variables[name] = value

    def assign(self, name, value):
        """
        Used for 'set' statements.
        Walks up the scope chain to find where the variable was declared,
        then updates it there (mirrors how Python/JS closures work).
        """
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value)
            return
        raise NameError(f"Semantic Error: Cannot assign to undeclared variable '{name}'.")

    def lookup(self, name):
        """
        Retrieves the value of a name. Walks up the scope chain if not
        found locally. Raises NameError if the name is undefined everywhere.
        """
        if name in self.variables:
            return self.variables[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise NameError(f"Semantic Error: Undefined variable '{name}'.")

    def create_child_scope(self):
        """
        Convenience factory: returns a new Environment whose parent is self.
        Used by the interpreter when entering a function body.
        """
        return Environment(parent=self)


# ------------------------------------------------------------------
# Internal smoke-test
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Scope Chain Test ===")

    global_env = Environment()
    global_env.declare("x", 10)
    global_env.declare("greet", {"is_function": True, "body": []})

    # Child scope (simulates a function call)
    local_env = global_env.create_child_scope()
    local_env.declare("x", 99)          # shadows global x in local scope

    print(f"global x  = {global_env.lookup('x')}")   # 10
    print(f"local  x  = {local_env.lookup('x')}")    # 99
    print(f"greet visible from local? {local_env.lookup('greet') is not None}")  # True

    # assign through scope chain
    local_env.assign("x", 42)           # updates the LOCAL x, not global
    print(f"global x after local assign = {global_env.lookup('x')}")  # still 10

    # Re-declaration guard still works
    try:
        local_env.declare("x", 0)
    except NameError as e:
        print(f"Re-declaration caught: {e}")

    print("=== All scope tests passed ===")