"""
Custom ANSI substitution system for special characters.

This module provides custom text substitutions for use in descriptions,
poses, say commands, and emits.

Supported substitutions:
    %r: Carriage return/newline
    %t: Tab character
"""


# Define custom substitution patterns
CUSTOM_SUBS = {
    '%r': '\n',  # Carriage return (newline)
    '%t': '\t'   # Tab character
}


def parse_subs(text):
    """
    Parse and replace custom substitution codes in text.
    
    Args:
        text (str): The text to process.
        
    Returns:
        str: The text with substitutions applied.
    """
    if not text:
        return text
    
    result = text
    for pattern, replacement in CUSTOM_SUBS.items():
        result = result.replace(pattern, replacement)
    
    return result
