def clean_text(text):
    """Clean whitespace and symbols."""
    return text.strip().replace("\n", " ") if text else ""
