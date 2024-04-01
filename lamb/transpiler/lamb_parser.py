import ast

class LambParser:
    def __init__(self):
        # Initialize any necessary attributes or states
        
    def parse(self, lamb_code):
        try:
            lamb_ast = ast.parse(lamb_code)
            return lamb_ast
        except SyntaxError as e:
            # Handle parsing errors
            raise Exception(f"Parsing error: {e}")