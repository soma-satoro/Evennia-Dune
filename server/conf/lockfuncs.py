"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

# def myfalse(accessing_obj, accessed_obj, *args, **kwargs):
#    """
#    called in lockstring with myfalse().
#    A simple logger that always returns false. Prints to stdout
#    for simplicity, should use utils.logger for real operation.
#    """
#    print "%s tried to access %s. Access denied." % (accessing_obj, accessed_obj)
#    return False


# ============================================================================
# House/Affiliation Lock Functions
# ============================================================================

def house(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object serves a specific House.
    
    Usage:
        traverse:house(House Atreides)
        traverse:house(Atreides)
    
    Args:
        First argument should be the House name (case-insensitive)
    
    Returns:
        True if character serves the specified House, False otherwise
    """
    if not args:
        return False
    
    # Get the House name from arguments
    house_name = " ".join(str(arg) for arg in args).strip()
    
    # Check if accessing_obj has a house attribute
    if not hasattr(accessing_obj.db, 'house') or not accessing_obj.db.house:
        return False
    
    # Compare house names (case-insensitive)
    return accessing_obj.db.house.key.lower() == house_name.lower()


def hashouse(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object serves any House.
    
    Usage:
        traverse:hashouse()
    
    Returns:
        True if character serves any House, False if no House affiliation
    """
    return hasattr(accessing_obj.db, 'house') and accessing_obj.db.house is not None


def nohouse(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object does NOT serve any House.
    Useful for areas restricted to non-affiliated individuals.
    
    Usage:
        traverse:nohouse()
    
    Returns:
        True if character serves no House, False if affiliated
    """
    return not hasattr(accessing_obj.db, 'house') or accessing_obj.db.house is None


def housetype(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object's House is of a specific type.
    
    Usage:
        traverse:housetype(Minor)
        traverse:housetype(House Major)
        traverse:housetype(Great House)
    
    Valid types:
        - Nascent House, House Minor, House Major, Great House
        - Or just: Nascent, Minor, Major, Great
    
    Returns:
        True if character's House matches the specified type, False otherwise
    """
    if not args:
        return False
    
    # Get the type from arguments
    house_type = " ".join(str(arg) for arg in args).strip()
    
    # Check if accessing_obj has a house
    if not hasattr(accessing_obj.db, 'house') or not accessing_obj.db.house:
        return False
    
    # Get the House's type
    actual_type = accessing_obj.db.house.db.house_type
    
    # Normalize the comparison (handle both "Minor" and "House Minor")
    house_type_lower = house_type.lower()
    actual_type_lower = actual_type.lower()
    
    # Direct match
    if house_type_lower == actual_type_lower:
        return True
    
    # Partial match (e.g., "minor" matches "House Minor")
    if house_type_lower in actual_type_lower:
        return True
    
    # Reverse partial match (e.g., "House Minor" matches "minor")
    if actual_type_lower in house_type_lower:
        return True
    
    return False


def houseor(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object serves one of multiple specified Houses.
    Useful for areas accessible to allied Houses.
    
    Usage:
        traverse:houseor(House Atreides, House Molay)
        traverse:houseor(Atreides, Molay, Vernius)
    
    Note: Separate house names with commas
    
    Returns:
        True if character serves any of the specified Houses, False otherwise
    """
    if not args:
        return False
    
    # Check if accessing_obj has a house
    if not hasattr(accessing_obj.db, 'house') or not accessing_obj.db.house:
        return False
    
    # Get character's house name
    char_house = accessing_obj.db.house.key.lower()
    
    # Check against all provided house names
    # Args might be comma-separated or space-separated
    house_names = []
    for arg in args:
        # Split by comma if present
        if ',' in str(arg):
            house_names.extend([h.strip().lower() for h in str(arg).split(',')])
        else:
            house_names.append(str(arg).strip().lower())
    
    # Check if character's house matches any of the allowed houses
    for house_name in house_names:
        if char_house == house_name or char_house == f"house {house_name}":
            return True
    
    return False


def not_house(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object does NOT serve a specific House.
    Useful for restricting enemy Houses from certain areas.
    
    Usage:
        traverse:not_house(House Harkonnen)
        traverse:not_house(Harkonnen)
    
    Returns:
        True if character does NOT serve the specified House, False if they do
    """
    if not args:
        return True  # If no house specified, allow access
    
    # Get the House name from arguments
    house_name = " ".join(str(arg) for arg in args).strip()
    
    # If character has no house, they pass the "not_house" check
    if not hasattr(accessing_obj.db, 'house') or not accessing_obj.db.house:
        return True
    
    # Compare house names (case-insensitive) - return True if NOT a match
    return accessing_obj.db.house.key.lower() != house_name.lower()


def housealliance(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object's House is allied with the specified House.
    
    Usage:
        traverse:housealliance(House Atreides)
    
    Note: This requires an alliance system to be implemented.
          Currently returns False - placeholder for future development.
    
    Returns:
        True if character's House is allied with specified House, False otherwise
    """
    # Placeholder for future alliance system
    # Would check if accessing_obj.db.house is in accessed House's allies list
    return False


def houserole(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object holds a specific role in their House.
    
    Usage:
        traverse:houserole(Ruler)
        traverse:houserole(Spymaster)
        traverse:houserole(Warmaster)
    
    Returns:
        True if character holds the specified role in their House, False otherwise
    """
    if not args:
        return False
    
    # Get the role name from arguments
    role_name = " ".join(str(arg) for arg in args).strip()
    
    # Check if accessing_obj has a house
    if not hasattr(accessing_obj.db, 'house') or not accessing_obj.db.house:
        return False
    
    house = accessing_obj.db.house
    
    # Check if the role exists and is filled by this character
    if role_name not in house.db.roles:
        return False
    
    # Check if this character holds the role
    role_holder = house.db.roles[role_name].get('character', '')
    return role_holder.lower() == accessing_obj.key.lower()


def housemintype(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Check if the accessing object's House is at least a certain type.
    Hierarchy: Nascent < Minor < Major < Great
    
    Usage:
        traverse:housemintype(Minor)     - Allows Minor, Major, Great
        traverse:housemintype(Major)     - Allows Major, Great only
        traverse:housemintype(Great)     - Allows Great only
    
    Returns:
        True if character's House type meets minimum requirement, False otherwise
    """
    if not args:
        return False
    
    # Get the minimum type from arguments
    min_type = " ".join(str(arg) for arg in args).strip().lower()
    
    # Check if accessing_obj has a house
    if not hasattr(accessing_obj.db, 'house') or not accessing_obj.db.house:
        return False
    
    # Get the House's type
    actual_type = accessing_obj.db.house.db.house_type.lower()
    
    # Hierarchy values
    hierarchy = {
        "nascent": 0,
        "nascent house": 0,
        "minor": 1,
        "house minor": 1,
        "major": 2,
        "house major": 2,
        "great": 3,
        "great house": 3
    }
    
    # Get hierarchy values
    min_value = hierarchy.get(min_type, 999)
    actual_value = hierarchy.get(actual_type, -1)
    
    return actual_value >= min_value
