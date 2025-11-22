"""
Search helper utilities.

Provides convenient search functions for finding characters and objects.
"""

from evennia.utils.search import search_object


def search_character(caller, target_name):
    """
    Search for a character by name.
    
    Args:
        caller: The object doing the search
        target_name (str): Name to search for
    
    Returns:
        Character object if found, None otherwise
    """
    # Use Evennia's built-in search
    result = caller.search(target_name, global_search=True)
    
    if not result:
        return None
    
    # Make sure result is a character
    if hasattr(result, 'db') and hasattr(result.db, 'stats'):
        return result
    
    caller.msg(f"{result.name} is not a character.")
    return None

