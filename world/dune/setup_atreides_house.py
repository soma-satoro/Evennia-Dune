"""
Setup Script for House Atreides

Creates or updates House Atreides with appropriate settings for the
Children of Dune era, where Alia is Regent and the Imperial Seat is on Arrakis.

Usage:
    @py world.dune.setup_atreides_house.setup_house_atreides()
"""

from evennia import create_object, search_object


def setup_house_atreides():
    """
    Create or update House Atreides for the Children of Dune era.
    
    Returns:
        House: The House Atreides object
    """
    print("\n" + "="*70)
    print("SETTING UP HOUSE ATREIDES")
    print("="*70 + "\n")
    
    # Check if House Atreides already exists
    house = search_object("House Atreides", typeclass="typeclasses.houses.House")
    
    if house:
        house = house[0]
        print("House Atreides already exists. Updating settings...")
    else:
        # Create new House
        house = create_object(
            "typeclasses.houses.House",
            key="House Atreides"
        )
        print("Created new House Atreides.")
    
    # Set basic information
    house.db.desc = """House Atreides, the Great House that rules the Imperium from Arrakis. 
Once nobles of Caladan, they now control the desert planet and the spice that is the lifeblood 
of the Imperium. Following Paul Muad'Dib's holy Jihad, House Atreides sits at the pinnacle of 
power, though Paul himself has vanished into the desert. His sister Alia rules as Regent."""
    
    # House traits
    if not hasattr(house.db, 'traits') or not house.db.traits:
        house.db.traits = []
    
    house_traits = [
        "Noble Heritage",
        "Popular Support",
        "Spice Monopoly",
        "Fremen Alliance",
        "Imperial Authority",
        "Prophetic Legacy"
    ]
    
    for trait in house_traits:
        if trait not in house.db.traits:
            house.db.traits.append(trait)
    
    # Set headquarters
    house.db.headquarters = "Arrakeen Palace, Arrakis"
    
    # Set the Regent
    house.db.ruler = "Alia Atreides (Regent)"
    
    # Initialize domains if not present
    if not hasattr(house.db, 'domains') or not house.db.domains:
        house.db.domains = {}
    
    # Set domain values for House Atreides (powerful house)
    domains = {
        "Agents": 8,      # Extensive spy network
        "Allies": 7,      # Many allied houses  
        "Artifacts": 6,   # Ancient Atreides artifacts
        "Lifestock": 8,   # Control of spice/sandworms
        "Military": 9,    # Fremen legions + Imperial Sardaukar
        "Retinue": 8,     # Skilled retainers
        "Spies": 8,       # Excellent intelligence
        "Wealth": 9       # Spice monopoly = immense wealth
    }
    
    for domain, value in domains.items():
        if domain not in house.db.domains:
            house.db.domains[domain] = value
    
    # Set planet
    house.db.homeworld = "Arrakis (Imperial Seat)"
    house.db.original_homeworld = "Caladan"
    
    # Initialize skills if not present
    if not hasattr(house.db, 'skills') or not house.db.skills:
        house.db.skills = {}
    
    # House skills (represent the house's institutional capabilities)
    house_skills = {
        "Battle": 5,       # Legendary military prowess
        "Communicate": 5,  # Diplomatic excellence
        "Discipline": 4,   # Strong but under strain
        "Move": 4,         # Good logistics
        "Understand": 5    # Deep wisdom and learning
    }
    
    for skill, value in house_skills.items():
        if skill not in house.db.skills:
            house.db.skills[skill] = value
    
    # Initialize roles if not present
    if not hasattr(house.db, 'roles') or not house.db.roles:
        house.db.roles = {}
    
    # Set up key roles (these will be filled by roster characters)
    key_roles = {
        "Regent": {
            "character": "Alia Atreides",
            "description": "Rules the Imperium in Paul's absence",
            "permissions": ["full_authority"]
        },
        "Swordmaster": {
            "character": "Duncan Idaho",
            "description": "Master of combat and military training",
            "permissions": ["military", "training"]
        },
        "Warmaster": {
            "character": "Gurney Halleck",
            "description": "Commands the Atreides military forces",
            "permissions": ["military", "warfare"]
        },
        "Advisor": {
            "character": "Lady Jessica",
            "description": "Bene Gesserit counsel and wisdom",
            "permissions": ["counsel", "bene_gesserit"]
        },
        "Marshal": {
            "character": "Stilgar",
            "description": "Commands Fremen forces and guards the heirs",
            "permissions": ["military", "fremen"]
        },
        "Historian": {
            "character": "Irulan Corrino",
            "description": "Chronicles the Atreides legacy",
            "permissions": ["records", "education"]
        },
        "Heir": {
            "character": "Leto II Atreides",
            "description": "Primary heir to House Atreides",
            "permissions": ["succession"]
        },
        "Heir-Designate": {
            "character": "Ghanima Atreides",
            "description": "Secondary heir to House Atreides",
            "permissions": ["succession"]
        }
    }
    
    for role_name, role_data in key_roles.items():
        if role_name not in house.db.roles:
            house.db.roles[role_name] = role_data
    
    # House colors and symbols
    house.db.colors = "Green and Black with the Red Hawk"
    house.db.motto = "There is no call we do not answer, there is no faith we betray"
    
    # Initialize member roster if not present
    if not hasattr(house.db, 'member_roster') or not house.db.member_roster:
        house.db.member_roster = {}
    
    # Special notes for this era
    house.db.historical_period = "Children of Dune Era"
    house.db.special_notes = """House Atreides rules the Imperium from Arrakis following 
Paul Muad'Dib's Jihad. The house is at the height of its power but faces internal strains. 
Regent Alia's mental stability is in question, Paul's children are coming of age, and various 
factions plot to overthrow or manipulate the house. The Fremen integration into Imperial 
society causes tension between tradition and progress."""
    
    # Allies and enemies
    if not hasattr(house.db, 'allies'):
        house.db.allies = []
    
    allies = ["Fremen Tribes", "Spacing Guild (tentative)", "Minor Houses"]
    for ally in allies:
        if ally not in house.db.allies:
            house.db.allies.append(ally)
    
    if not hasattr(house.db, 'enemies'):
        house.db.enemies = []
    
    enemies = ["House Corrino (deposed)", "Bene Gesserit (conflicted)", "Conservative Houses"]
    for enemy in enemies:
        if enemy not in house.db.enemies:
            house.db.enemies.append(enemy)
    
    print("\n" + "="*70)
    print("HOUSE ATREIDES SETUP COMPLETE")
    print("="*70)
    print(f"\nHouse: {house.key}")
    print(f"Ruler: {house.db.ruler}")
    print(f"Headquarters: {house.db.headquarters}")
    print(f"Domains: {house.db.domains}")
    print(f"Key Roles: {len(house.db.roles)}")
    print(f"\nUse +house Atreides to view full house information.")
    print("="*70 + "\n")
    
    return house


def setup_arrakis_palace():
    """
    Create the Arrakeen Palace throne room as a starting location.
    
    Returns:
        Room: The throne room
    """
    print("\n" + "="*70)
    print("CREATING ARRAKEEN PALACE - THRONE ROOM")
    print("="*70 + "\n")
    
    # Check if throne room exists
    throne_room = search_object("Arrakeen Palace - Throne Room", typeclass="typeclasses.rooms.Room")
    
    if throne_room:
        throne_room = throne_room[0]
        print("Throne room already exists. Updating...")
    else:
        throne_room = create_object(
            "typeclasses.rooms.Room",
            key="Arrakeen Palace - Throne Room"
        )
        print("Created throne room.")
    
    # Set description
    throne_room.db.desc = """This vast chamber serves as the throne room of House Atreides, 
the ruling power of the Imperium. High vaulted ceilings soar overhead, decorated with the 
green and black banners of House Atreides - the Red Hawk prominent among them. Massive 
pillars of polished stone support the ceiling, and desert-filtered light streams through 
tall windows.

The throne itself sits on a raised dais at the far end - a chair of dark wood and green 
cushions, austere in its simplicity yet commanding in its presence. Around the room, 
Fremen guards in traditional robes stand alongside uniformed Atreides soldiers. The air 
carries the faint scent of spice.

This is where Alia Atreides, Regent of the Imperium, holds court."""
    
    # Set room attributes
    throne_room.db.planet = "Arrakis"
    throne_room.db.location_type = "Palace"
    throne_room.db.importance = "Capital"
    
    print(f"✓ Throne room created: {throne_room.key} (#{throne_room.id})")
    print("="*70 + "\n")
    
    return throne_room


def setup_all():
    """
    Complete setup: Create House Atreides and initial locations.
    
    Returns:
        tuple: (house, throne_room)
    """
    print("\n" + "="*70)
    print("COMPLETE SETUP FOR CHILDREN OF DUNE ERA")
    print("="*70 + "\n")
    
    house = setup_house_atreides()
    throne_room = setup_arrakis_palace()
    
    print("\n" + "="*70)
    print("SETUP COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Create roster characters: @py world.dune.roster_characters.create_all_roster()")
    print("2. View house: +house Atreides")
    print("3. Teleport characters to throne room if needed")
    print("="*70 + "\n")
    
    return house, throne_room


if __name__ == "__main__":
    # Can be run as a standalone script
    setup_all()

