"""
Formatting utilities for text display.

Provides functions for creating headers, footers, and formatted text.
"""


def header(text, width=78, color="|w"):
    """
    Create a header bar with text.
    
    Args:
        text (str): Text to display in header
        width (int): Width of the header
        color (str): Color code
    
    Returns:
        str: Formatted header
    """
    bar = "=" * width
    centered_text = text.center(width)
    return f"{color}{bar}|n\n{color}{centered_text}|n\n{color}{bar}|n"


def footer(width=78, color="|w"):
    """
    Create a footer bar.
    
    Args:
        width (int): Width of the footer
        color (str): Color code
    
    Returns:
        str: Formatted footer
    """
    bar = "=" * width
    return f"{color}{bar}|n"


def divider(width=78, char="-", color="|w"):
    """
    Create a divider line.
    
    Args:
        width (int): Width of the divider
        char (str): Character to use for divider
        color (str): Color code
    
    Returns:
        str: Formatted divider
    """
    line = char * width
    return f"{color}{line}|n"


def format_stat(name, value, max_value=None, width=30):
    """
    Format a stat for display.
    
    Args:
        name (str): Name of the stat
        value (int): Current value
        max_value (int): Maximum value (optional)
        width (int): Total width
    
    Returns:
        str: Formatted stat line
    """
    if max_value:
        stat_str = f"{name}: {value}/{max_value}"
    else:
        stat_str = f"{name}: {value}"
    
    return f"{stat_str:<{width}}"

