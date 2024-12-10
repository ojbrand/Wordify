import json
from collections import Counter
from pdfminer.high_level import extract_text



def clean_text(text):
    """Clean the input text"""
    bad_chars = [';', ':', '!', "*", ".", "(", ")", '...', ',', '…']
    for i in bad_chars:
        text = text.replace(i, '')
    text = text.lower()
    return text

def json_parser(filename):
    """Parse a JSON file, clean the text, and compute word statistics."""
    with open(filename, 'r') as f:
        raw = json.load(f)
    text = raw['text']
    # Clean the text
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    wc = Counter(words)
    num = len(words)

    return {'wordcount': wc, 'numwords': num}

def pdf_parser(filename):
    """Parse a PDF file, clean the text, and compute word statistics."""
    text = extract_text(filename)
    # Clean the text
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    wc = Counter(words)
    num = len(words)

    return {'wordcount': wc, 'numwords': num}

