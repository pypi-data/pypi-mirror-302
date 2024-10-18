import ast
from .code_analyzer import CodeAnalyzer
from .summary_generator import generate_summary
from .doc_generator import generate_markdown

__all__ = ['CodeAnalyzer', 'generate_summary', 'generate_markdown']

# Analyze the code only if this module is not being imported for testing
if __name__ == "__main__":
    try:
        with open('your_code.py', 'r') as file:
            tree = ast.parse(file.read())
            analyzer = CodeAnalyzer()
            analyzer.visit(tree)

        # Get the docstring of the first function
        docstring = analyzer.function_data[0]['docstring']

        # Generate a summary for a developer
        dev_summary = generate_summary(docstring, audience="developer")
        print("Developer Summary:", dev_summary)

        # Generate a summary for an end user
        user_summary = generate_summary(docstring, audience="end_user")
        print("End User Summary:", user_summary)

    except FileNotFoundError:
        print("The file 'your_code.py' does not exist. Please create it.")
