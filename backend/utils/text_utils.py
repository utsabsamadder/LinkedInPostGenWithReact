def count_lines(text: str) -> int:
    """Count the number of lines in a text."""
    if not text:
        return 0
    return len(text.split('\n'))

def categorize_length(line_count: int) -> str:
    """Categorize post length based on line count."""
    if line_count <= 5:
        return "Short"
    elif 6 <= line_count <= 10:
        return "Medium"
    else:
        return "Long"