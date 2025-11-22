"""
ANSI utilities for text wrapping and formatting.

Provides utilities for working with ANSI-colored text.
"""

from evennia.utils.ansi import ANSIString


def wrap_ansi(text, width=78, left_padding=0):
    """
    Wrap text that contains ANSI codes while preserving color codes.
    
    Args:
        text (str): The text to wrap (may contain ANSI codes)
        width (int): The maximum width for each line
        left_padding (int): Number of spaces to pad on the left
        
    Returns:
        str: Wrapped text with ANSI codes preserved
    """
    # Convert to ANSIString for proper handling
    ansi_text = ANSIString(text)
    
    # Create padding string
    padding = " " * left_padding
    
    # Simple wrapping - split by spaces and reassemble
    words = str(ansi_text).split()
    lines = []
    current_line = padding
    current_length = left_padding
    
    for word in words:
        # Get the clean length (without ANSI codes)
        word_ansi = ANSIString(word)
        word_length = len(word_ansi.clean())
        
        # Check if adding this word would exceed width
        if current_length + word_length + 1 > width and current_line.strip():
            lines.append(current_line.rstrip())
            current_line = padding + word
            current_length = left_padding + word_length
        else:
            if current_line.strip():
                current_line += " " + word
                current_length += word_length + 1
            else:
                current_line += word
                current_length += word_length
    
    # Add the last line
    if current_line.strip():
        lines.append(current_line.rstrip())
    
    return "\n".join(lines)


def strip_ansi_length(text):
    """
    Get the length of text without ANSI codes.
    
    Args:
        text (str): Text that may contain ANSI codes
        
    Returns:
        int: Length of text without ANSI codes
    """
    return len(ANSIString(text).clean())


def center_ansi(text, width=78, fillchar=' '):
    """
    Center text that contains ANSI codes.
    
    Args:
        text (str): Text to center (may contain ANSI codes)
        width (int): Total width
        fillchar (str): Character to fill with
        
    Returns:
        str: Centered text
    """
    clean_length = strip_ansi_length(text)
    padding = width - clean_length
    left_pad = padding // 2
    right_pad = padding - left_pad
    
    return fillchar * left_pad + text + fillchar * right_pad

