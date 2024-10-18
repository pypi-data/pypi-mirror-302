# ai_doc_assistant/code_analyzer.py
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

def analyze_code(code):
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.function_data

# Example usage
if __name__ == "__main__":
    sample_code = """
def sample_function(arg1, arg2):
    \"\"\"This is a sample function.\"\"\"
    return arg1 + arg2
    """
    result = analyze_code(sample_code)
    print(result)