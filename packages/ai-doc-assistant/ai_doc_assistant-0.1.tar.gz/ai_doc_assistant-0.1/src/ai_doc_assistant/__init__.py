#init.py

from code_analyzer import CodeAnalyzer
from summary_generator import generate_summary

# Analyze the code
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
