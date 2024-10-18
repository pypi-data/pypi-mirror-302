#doc_generator
import markdown

def generate_markdown(function_data):
    doc = f"# Function: {function_data['name']}\n"
    doc += f"**Parameters:** {', '.join(function_data['args'])}\n"
    if function_data['docstring']:
        doc += f"**Description:** {function_data['docstring']}\n"
    return markdown.markdown(doc)

markdown_doc = generate_markdown(analyzer.function_data[0])
print(markdown_doc)
