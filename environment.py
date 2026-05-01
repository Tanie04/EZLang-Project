#The variable storage
class Environment:
    """
    Symbol Table to manage variable storage and retrieval.
    Strict enforcement of declaration before usage.
    """
    def __init__(self):
        # The primary storage for variable names and values
        self.variables = {}

    def declare(self, name, value):
        """Used for 'let' statements. Prevents re-declaration in the same scope."""
        if name in self.variables:
            raise NameError(f"Semantic Error: Variable '{name}' is already declared.")
        self.variables[name] = value

    def assign(self, name, value):
        """Used for 'set' statements. Ensures the variable exists before assignment."""
        if name not in self.variables:
            raise NameError(f"Semantic Error: Cannot assign to undeclared variable '{name}'.")
        self.variables[name] = value

    def lookup(self, name):
        """Retrieves the value of a variable. Throws error if undefined."""
        if name in self.variables:
            return self.variables[name]
        raise NameError(f"Semantic Error: Undefined variable '{name}'.")

# --- INTERNAL TEST ---
if __name__ == "__main__":
    env = Environment()
    try:
        #Try to declare variables
        print("Testing Variable Declaration...")
        env.declare("nhi_score", 10)
        print(f"nhi_score = {env.lookup('nhi_score')}")
        
        #Try to update variables
        print("\nTesting Variable Assignment...")
        env.assign("nhi_score", 25)
        print(f"nhi_score updated to = {env.lookup('nhi_score')}")
        
        # This should trigger an error
        # env.lookup("y") 
    except NameError as e:
        print(e)

