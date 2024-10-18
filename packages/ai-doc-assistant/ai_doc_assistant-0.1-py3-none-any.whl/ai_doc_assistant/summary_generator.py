#summary_genarator
from transformers import pipeline

summarizer = pipeline('summarization', model="facebook/bart-large-cnn")

def generate_summary(text, audience="developer"):
    if audience == "developer":
        return summarizer(text, max_length=100, min_length=30, do_sample=False)
    elif audience == "end_user":
        return summarizer(text, max_length=50, min_length=20, do_sample=False)