"""
Text Processing Utilities

Universal text processing functions for consistent handling of
special characters and formatting across the game.
"""

from django.conf import settings
from world.utils.ansi_subs import parse_subs


def process_special_characters(text):
    """
    Process special character substitutions in text input.
    
    Uses the centralized substitution system from world.utils.ansi_subs.
    
    Default substitutions:
    - %r = newline/carriage return
    - %t = tab character
    
    Args:
        text (str): The input text to process
        
    Returns:
        str: The processed text with substitutions applied
        
    Example:
        >>> process_special_characters("Line 1%rLine 2%r%rNew paragraph%tIndented text")
        "Line 1\nLine 2\n\nNew paragraph\tIndented text"
    """
    if not text:
        return text
        
    # Check if substitutions are enabled
    if not getattr(settings, 'ENABLE_SPECIAL_CHAR_SUBSTITUTIONS', True):
        return text
    
    # Use the centralized substitution system
    return parse_subs(text)


def apply_text_formatting(text, apply_substitutions=True):
    """
    Apply all text formatting including special character substitutions.
    
    This is the main function that should be called for all user input
    that needs text processing.
    
    Args:
        text (str): The input text to format
        apply_substitutions (bool): Whether to apply special character substitutions
        
    Returns:
        str: The fully formatted text
    """
    if not text:
        return text
        
    if apply_substitutions:
        text = process_special_characters(text)
        
    return text 