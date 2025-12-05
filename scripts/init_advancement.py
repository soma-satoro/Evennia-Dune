"""
Initialize Advancement Tracking for Existing Characters

This script adds advancement tracking to existing characters who
don't have it yet. Run this once after implementing the advancement
system.

Usage:
    @py from scripts.init_advancement import init_all_characters; init_all_characters()
"""

from evennia import ObjectDB
from typeclasses.characters import Character


def init_character_advancement(character):
    """
    Initialize advancement tracking for a single character.
    
    Args:
        character: The character object to initialize
        
    Returns:
        bool: True if initialized, False if already had tracking
    """
    needs_init = False
    
    # Check if advancement tracking exists
    if not hasattr(character.db, 'advancement_points'):
        character.db.advancement_points = 0
        needs_init = True
    
    if not hasattr(character.db, 'advancement_history'):
        character.db.advancement_history = []
        needs_init = True
    
    if not hasattr(character.db, 'skill_advances'):
        character.db.skill_advances = {
            "battle": 0,
            "communicate": 0,
            "discipline": 0,
            "move": 0,
            "understand": 0
        }
        needs_init = True
    
    if not hasattr(character.db, 'total_skill_advances'):
        character.db.total_skill_advances = 0
        needs_init = True
    
    return needs_init


def init_all_characters():
    """
    Initialize advancement tracking for all characters in the database.
    
    Returns:
        dict: Statistics about initialization
    """
    # Get all character objects
    characters = ObjectDB.objects.filter(db_typeclass_path="typeclasses.characters.Character")
    
    stats = {
        "total": 0,
        "initialized": 0,
        "already_had": 0,
        "errors": 0
    }
    
    for char in characters:
        stats["total"] += 1
        
        try:
            # Check if character has stats
            if not hasattr(char.db, 'stats'):
                print(f"  Skipping {char.name} (no stats)")
                continue
            
            # Initialize advancement tracking
            if init_character_advancement(char):
                stats["initialized"] += 1
                print(f"  ✓ Initialized {char.name}")
            else:
                stats["already_had"] += 1
                print(f"  - {char.name} already had tracking")
        
        except Exception as e:
            stats["errors"] += 1
            print(f"  ✗ Error with {char.name}: {e}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("ADVANCEMENT INITIALIZATION SUMMARY")
    print("=" * 70)
    print(f"Total Characters: {stats['total']}")
    print(f"Newly Initialized: {stats['initialized']}")
    print(f"Already Had Tracking: {stats['already_had']}")
    print(f"Errors: {stats['errors']}")
    print("=" * 70)
    
    return stats


def init_specific_character(character_name):
    """
    Initialize advancement tracking for a specific character by name.
    
    Args:
        character_name (str): Name of the character to initialize
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Find the character
    characters = ObjectDB.objects.filter(
        db_typeclass_path="typeclasses.characters.Character",
        db_key__iexact=character_name
    )
    
    if not characters:
        print(f"Character '{character_name}' not found.")
        return False
    
    if len(characters) > 1:
        print(f"Multiple characters found with name '{character_name}':")
        for char in characters:
            print(f"  - {char.name} (#{char.id})")
        return False
    
    char = characters[0]
    
    # Check if character has stats
    if not hasattr(char.db, 'stats'):
        print(f"{char.name} does not have stats initialized.")
        return False
    
    # Initialize advancement tracking
    if init_character_advancement(char):
        print(f"✓ Initialized advancement tracking for {char.name}")
        return True
    else:
        print(f"- {char.name} already had advancement tracking")
        return True


# Example usage:
# @py from scripts.init_advancement import init_all_characters; init_all_characters()
# @py from scripts.init_advancement import init_specific_character; init_specific_character("Paul")

