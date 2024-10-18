#code_analyzer
import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_data = []

    def visit_FunctionDef(self, node):
        self.function_data.append({
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'docstring': ast.get_docstring(node)
        })
        self.generic_visit(node)

# Usage example
with open('your_code.py', 'r') as file:
    tree = ast.parse(file.read())
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    print(analyzer.function_data)
