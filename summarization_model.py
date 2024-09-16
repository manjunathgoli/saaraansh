from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=200, min_length=50):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=True)
    return summary[0]['summary_text']

