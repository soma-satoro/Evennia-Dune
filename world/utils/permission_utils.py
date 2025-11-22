"""
Permission checking utilities for consistent access control.
"""

# Standard permission levels
PERMISSION_LEVELS = {
    'PLAYER': 'all()',
    'BUILDER': 'perm(builders)',
    'ADMIN': 'perm(admin)',
    'STAFF': 'perm(staff)',
    'STORYTELLER': 'perm(storyteller)'
}

def check_staff_permission(caller, required_level="Builder"):
    """
    Check if caller has staff-level permissions.
    
    Args:
        caller: The character/account making the request
        required_level: Minimum required permission level
        
    Returns:
        bool: True if caller has staff permissions
    """
    # Check traditional staff permissions
    if (caller.check_permstring("builders") or 
        caller.check_permstring("admin") or 
        caller.check_permstring("staff")):
        return True
    
    # Check for Storyteller flag for Builder-level commands
    if required_level == "Builder":
        return check_storyteller_permission(caller)
    
    return False

def check_admin_permission(caller):
    """
    Check if caller has admin-level permissions.
    
    Args:
        caller: The character/account making the request
        
    Returns:
        bool: True if caller has admin permissions
    """
    return caller.check_permstring("admin")

def check_builder_permission(caller):
    """
    Check if caller has builder-level permissions.
    
    Args:
        caller: The character/account making the request
        
    Returns:
        bool: True if caller has builder permissions
    """
    return (caller.check_permstring("builders") or 
            caller.check_permstring("admin") or
            check_storyteller_permission(caller))

def check_storyteller_permission(caller):
    """
    Check if caller has the Storyteller flag.
    
    Args:
        caller: The character/account making the request
        
    Returns:
        bool: True if caller has Storyteller flag
    """
    # Check if character has storyteller flag
    if hasattr(caller, 'db') and caller.db.storyteller:
        return True
    
    # Check if account has storyteller flag (for account-level permissions)
    if hasattr(caller, 'account') and hasattr(caller.account, 'db') and caller.account.db.storyteller:
        return True
    
    return False

def check_mystery_permission(caller):
    """
    Check if caller can manage mysteries (staff or storyteller).
    
    Args:
        caller: The character/account making the request
        
    Returns:
        bool: True if caller can manage mysteries
    """
    return check_staff_permission(caller) or check_storyteller_permission(caller)

def check_npc_control_permission(caller, npc):
    """
    Check if caller can control an NPC.
    
    Args:
        caller: The character/account making the request
        npc: The NPC object
        
    Returns:
        bool: True if caller can control the NPC
    """
    # Staff and storytellers can control any NPC
    if check_staff_permission(caller) or check_storyteller_permission(caller):
        return True
    
    # Check if caller is the creator
    if hasattr(npc, 'db') and npc.db.creator == caller:
        return True
    
    # Check if caller is in the controllers list
    if hasattr(npc, 'db') and npc.db.controllers and caller in npc.db.controllers:
        return True
    
    return False

def can_modify_character_stats(caller, target):
    """
    Check if caller can modify target character's stats.
    
    Args:
        caller: The character/account making the request
        target: The target character
        
    Returns:
        tuple: (can_modify: bool, reason: str)
    """
    # Staff can always modify stats
    if check_staff_permission(caller):
        return True, "Staff permission"
    
    # Players can only modify their own stats
    if target != caller:
        return False, "Can only modify your own stats"
    
    # Check if character is approved (approved characters can't self-modify)
    is_npc = hasattr(target, 'db') and target.db.is_npc
    if not is_npc and target.db.approved:
        return False, "Character is approved - only staff can modify stats"
    
    return True, "Self-modification allowed"

def format_permission_error(required_level):
    """
    Format a standardized permission error message.
    
    Args:
        required_level: The required permission level
        
    Returns:
        str: Formatted error message
    """
    return f"You don't have permission to use this command. Required: {required_level}"
