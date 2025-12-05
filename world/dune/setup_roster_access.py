"""
Setup Roster Character Access

This module provides functions to make roster characters accessible and puppetable.
It handles setting proper locks, creating optional Account objects, and making
characters findable by the +sheet command.

Usage:
    @py from world.dune.setup_roster_access import setup_all_roster_access; setup_all_roster_access()
"""

from evennia import create_account, search_object
from evennia.utils.create import create_object


def setup_character_access(character, create_account_obj=False, set_global_search=True):
    """
    Set up a roster character to be accessible and puppetable.
    
    Args:
        character: The Character object to set up
        create_account_obj (bool): If True, creates an Account object for the character
        set_global_search (bool): If True, makes character globally searchable
        
    Returns:
        tuple: (character, account) - account will be None if not created
    """
    print(f"\n  Setting up access for: {character.name}")
    
    # Set locks to allow puppeting
    # pperm(Developer) means Developers and above can puppet
    # You can change this to pperm(Player) to allow any player to puppet
    character.locks.add("puppet:pperm(Builder)")  # Builders+ can puppet
    character.locks.add("call:true()")  # Can be called/paged
    character.locks.add("examine:perm(Builder)")  # Builders can examine
    
    # Make character globally searchable if requested
    if set_global_search:
        # Add a tag that makes it easier to find
        character.tags.add("roster_character", category="character_type")
        character.tags.add("available", category="roster")
    
    account = None
    if create_account_obj:
        # Check if account already exists
        account = search_object(character.name, typeclass="typeclasses.accounts.Account")
        
        if account:
            account = account[0]
            print(f"    ✓ Account already exists: {account.name}")
        else:
            # Create an account for this character
            # Password will be the same as character name (should be changed!)
            account = create_account(
                character.name,
                email=f"{character.key.lower().replace(' ', '_')}@roster.dune",
                password=character.name,  # CHANGE THIS!
                typeclass="typeclasses.accounts.Account"
            )
            print(f"    ✓ Created account: {account.name} (password: {character.name})")
            print(f"      |rWARNING: Default password is character name - should be changed!|n")
        
        # Link character to account
        if account:
            character.locks.add(f"puppet:pid({account.id}) or pperm(Builder)")
            # Add character to account's character list
            if character not in account.characters:
                account.db._playable_characters = account.db._playable_characters or []
                if character not in account.db._playable_characters:
                    account.db._playable_characters.append(character)
            print(f"    ✓ Linked {character.name} to account {account.name}")
    
    # Set home to a more appropriate location than Limbo if needed
    # (You can customize this based on your game)
    if character.home and character.home.key == "Limbo":
        print(f"    • Character home is Limbo (you may want to set a proper home)")
    
    print(f"    ✓ Access configured for {character.name}")
    
    return character, account


def setup_all_roster_access(create_accounts=False, set_global_search=True):
    """
    Set up access for all roster characters.
    
    Args:
        create_accounts (bool): If True, creates Account objects for each character
        set_global_search (bool): If True, makes characters globally searchable
        
    Returns:
        dict: Dictionary of character names to (character, account) tuples
    """
    print("\n" + "="*70)
    print("SETTING UP ROSTER CHARACTER ACCESS")
    print("="*70)
    
    roster_names = [
        "Alia Atreides",
        "Leto II Atreides",
        "Ghanima Atreides",
        "Duncan Idaho",
        "Irulan Corrino",
        "Lady Jessica",
        "Stilgar",
        "Gurney Halleck"
    ]
    
    results = {}
    accounts_created = []
    
    for name in roster_names:
        char = search_object(name, typeclass="typeclasses.characters.Character")
        if not char:
            print(f"\n  ⚠ Character '{name}' not found - skipping")
            continue
        
        char = char[0]
        character, account = setup_character_access(
            char,
            create_account_obj=create_accounts,
            set_global_search=set_global_search
        )
        results[name] = (character, account)
        
        if account:
            accounts_created.append(account)
    
    print("\n" + "="*70)
    print("SETUP COMPLETE!")
    print("="*70)
    print(f"\nConfigured {len(results)} roster characters")
    
    if accounts_created:
        print(f"\n|yCreated {len(accounts_created)} accounts:|n")
        for acc in accounts_created:
            print(f"  - {acc.name} (password: {acc.name})")
        print("\n|rIMPORTANT: Change default passwords with:|n")
        print("  @password <character_name> = <new_password>")
    
    print("\n|gRoster characters are now:|n")
    print("  ✓ Puppetable by Builders+")
    print("  ✓ Tagged as roster characters")
    print("  ✓ Callable/pageable")
    
    if create_accounts:
        print("\n|gTo log in as a roster character:|n")
        print("  connect <character_name> <password>")
    else:
        print("\n|gTo puppet a roster character:|n")
        print("  @ic <character_name>")
    
    print("\n|gTo view sheets (now accessible):|n")
    print("  +sheet (when puppeting the character)")
    print("  @py from evennia import search_object; char = search_object('Alia Atreides')[0]; caller.msg(char.get_sheet_display())")
    
    print("\n" + "="*70 + "\n")
    
    return results


def create_roster_viewing_command():
    """
    Alternative: Create a custom command for viewing any roster character sheet.
    This is a workaround for the +sheet command's location-based search.
    """
    print("\nNOTE: To view roster sheets without being in the same location:")
    print("Use @examine or create a custom +rsheet command.")
    print("\nExample viewing script:")
    print("  @py from evennia import search_object")
    print("  @py char = search_object('Alia Atreides')[0]")
    print("  @py me.msg(char.get_sheet_display())")


def move_rosters_to_location(location_name="Arrakeen Palace - Throne Room"):
    """
    Move all roster characters to a specific location.
    
    Args:
        location_name (str): Name of the room to move characters to
        
    Returns:
        list: Characters that were moved
    """
    print("\n" + "="*70)
    print(f"MOVING ROSTER CHARACTERS TO {location_name}")
    print("="*70)
    
    # Find the location
    location = search_object(location_name, typeclass="typeclasses.rooms.Room")
    if not location:
        print(f"\n|rERROR: Location '{location_name}' not found!|n")
        print("Create the location first or specify a different one.")
        return []
    
    location = location[0]
    print(f"\nTarget location: {location.name} (#{location.id})")
    
    roster_names = [
        "Alia Atreides",
        "Leto II Atreides",
        "Ghanima Atreides",
        "Duncan Idaho",
        "Irulan Corrino",
        "Lady Jessica",
        "Stilgar",
        "Gurney Halleck"
    ]
    
    moved = []
    for name in roster_names:
        char = search_object(name, typeclass="typeclasses.characters.Character")
        if not char:
            print(f"  ⚠ '{name}' not found - skipping")
            continue
        
        char = char[0]
        char.location = location
        print(f"  ✓ Moved {name} to {location.name}")
        moved.append(char)
    
    print(f"\n✓ Moved {len(moved)} characters to {location.name}")
    print("\nNow you can:")
    print(f"  1. Go to {location.name}")
    print("  2. Use +sheet <character name> to view any roster character")
    print("="*70 + "\n")
    
    return moved


def set_roster_homes(location_name="Arrakeen Palace - Throne Room"):
    """
    Set the home location for all roster characters.
    
    Args:
        location_name (str): Name of the room to set as home
        
    Returns:
        list: Characters whose homes were set
    """
    print("\n" + "="*70)
    print(f"SETTING ROSTER CHARACTER HOMES")
    print("="*70)
    
    # Find the location
    location = search_object(location_name, typeclass="typeclasses.rooms.Room")
    if not location:
        print(f"\n|rERROR: Location '{location_name}' not found!|n")
        return []
    
    location = location[0]
    print(f"\nHome location: {location.name} (#{location.id})")
    
    roster_names = [
        "Alia Atreides",
        "Leto II Atreides",
        "Ghanima Atreides",
        "Duncan Idaho",
        "Irulan Corrino",
        "Lady Jessica",
        "Stilgar",
        "Gurney Halleck"
    ]
    
    updated = []
    for name in roster_names:
        char = search_object(name, typeclass="typeclasses.characters.Character")
        if not char:
            print(f"  ⚠ '{name}' not found - skipping")
            continue
        
        char = char[0]
        char.home = location
        print(f"  ✓ Set home for {name}")
        updated.append(char)
    
    print(f"\n✓ Set homes for {len(updated)} characters")
    print("="*70 + "\n")
    
    return updated


# Quick access functions
def quick_setup_no_accounts():
    """Quick setup: Just fix locks and tags, don't create accounts."""
    return setup_all_roster_access(create_accounts=False, set_global_search=True)


def quick_setup_with_accounts():
    """Quick setup: Create accounts for all roster characters."""
    return setup_all_roster_access(create_accounts=True, set_global_search=True)


def quick_move_to_throne_room():
    """Quick setup: Move all roster characters to throne room."""
    return move_rosters_to_location("Arrakeen Palace - Throne Room")


if __name__ == "__main__":
    # Default behavior when run directly
    setup_all_roster_access(create_accounts=False, set_global_search=True)

