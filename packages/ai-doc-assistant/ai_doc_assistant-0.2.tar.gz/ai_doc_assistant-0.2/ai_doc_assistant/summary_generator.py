#summary_genarator
from transformers import pipeline

summarizer = pipeline('summarization', model="facebook/bart-large-cnn")

# def generate_summary(text, audience="developer"):
#     if audience == "developer":
#         return summarizer(text, max_length=100, min_length=30, do_sample=False)
#     elif audience == "end_user":
#         return summarizer(text, max_length=50, min_length=20, do_sample=False)
def generate_summary(docstring, audience="developer"):
    if audience == "developer":
        result = f"Developer Summary: {docstring}"
    elif audience == "end_user":
        result = f"User Summary: {docstring}"
    else:
        result = "Invalid audience"
    
    print(type(result))  # Debugging line to check the type
    return result
