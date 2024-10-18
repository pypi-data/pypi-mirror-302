import unittest
import ast
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_doc_assistant import CodeAnalyzer, generate_summary, generate_markdown

class TestAIDocAssistant(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = CodeAnalyzer()

    def test_code_analysis(self):
        code = """
def sample_function(arg1, arg2):
    \"\"\"This function adds two numbers.\"\"\" 
    return arg1 + arg2
"""
        self.analyzer.visit(ast.parse(code))
        self.assertEqual(len(self.analyzer.function_data), 1)
        self.assertEqual(self.analyzer.function_data[0]['name'], 'sample_function')

    def test_summary_generation(self):
        summary = generate_summary("This function adds two numbers.", audience="developer")
        self.assertIn('function adds two numbers', summary.lower())

    def test_markdown_generation(self):
        function_data = {
            'name': 'sample_function',
            'args': ['arg1', 'arg2'],
            'docstring': 'This function adds two numbers.'
        }
        markdown_doc = generate_markdown(function_data)
        self.assertIn('<h1>Function: sample_function</h1>', markdown_doc)  # Updated check

if __name__ == '__main__':
    unittest.main()
