class Environment:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def declare(self, name, value):
        if name in self.variables:
            raise NameError(f"Variable '{name}' already declared")
        self.variables[name] = value

    def assign(self, name, value):
        if name not in self.variables:
            raise NameError(f"Variable '{name}' not declared")
        self.variables[name] = value

    def lookup(self, name):
        if name in self.variables:
            return self.variables[name]
        raise NameError(f"Variable '{name}' undefined")
