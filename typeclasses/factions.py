"""
Factions for Dune Character Generation

Factions define organizations that characters can belong to, along with
their mandatory talents and requirements.
"""

# Valid castes
CASTES = [
    "Na-Familia",  # Nobility
    "Bondsman",    # Free individuals, middle class
    "Pyon",        # Lowest classes, hard laborers
]

# Faction definitions with mandatory talents
FACTIONS = {
    "Bene Gesserit Sisterhood": {
        "mandatory_talents": ["Prana-bindu Conditioning"],
        "description": "The Bene Gesserit are a secretive, matriarchal religious and political organization.",
    },
    "Fremen": {
        "mandatory_talents": [
            "Dedication",
            "Driven",
            "Master-at-Arms",
            "Rapid Recovery",
            "Resilience (Battle)",
            "Subtle Step",
            "The Reason I Fight",
        ],
        "description": "The Fremen are the native inhabitants of Arrakis, adapted to the harsh desert environment.",
        "note": "Must have at least ONE of the mandatory talents",
    },
    "Mentat Academies": {
        "mandatory_talents": [
            "Calculated Prediction",
            "Mentat Discipline",
            "Mind Palace",
            "Twisted Mentat",
            "Verify",
        ],
        "description": "Mentats are human computers, trained to process vast amounts of information.",
        "note": "Must have at least ONE of the mandatory talents",
    },
    "Spacing Guild": {
        "mandatory_talents": ["Guildsman"],
        "description": "The Spacing Guild controls all interstellar travel and commerce.",
    },
    "Suk Doctors": {
        "mandatory_talents": ["Imperial Conditioning"],
        "description": "Suk Doctors are the most trusted physicians in the Imperium, bound by conditioning.",
    },
    "CHOAM": {
        "mandatory_talents": ["Hand of CHOAM"],
        "description": "CHOAM (Combine Honnete Ober Advancer Mercantiles) controls commerce across the Imperium.",
    },
    "Sardaukar Legions": {
        "mandatory_talents": ["Unquestionable Loyalty"],
        "description": "The Sardaukar are the elite military forces of the Padishah Emperor.",
    },
    "Tleilaxu Face Dancer": {
        "mandatory_talents": ["Facedance", "Muscular Conditioning"],
        "description": "Face Dancers are shape-shifting agents of the Tleilaxu.",
        "note": "Must have BOTH mandatory talents",
    },
    "Ixians": {
        "mandatory_talents": [],
        "description": "Ixians are master technologists and engineers, known for their advanced technology.",
    },
    "Swordmasters of Ginaz": {
        "mandatory_talents": ["Weapon Focus"],
        "description": "The Swordmasters of Ginaz are the finest warriors and duelists in the Imperium.",
    },
    "Qizarate": {
        "mandatory_talents": ["Holy Presence of Muad'Dib"],
        "description": "The Qizarate is the religious bureaucracy of the Atreides Empire.",
    },
    "House Jongleur": {
        "mandatory_talents": ["Project Emotion"],
        "mandatory_focuses": [
            "Acting",
            "Acrobatics",
            "Dance",
            "Disguise",
            "Etiquette",
            "Empathy",
            "Grace",
            "Music",
            "Physical Empathy",
            "Self-Control",
        ],
        "description": "House Jongleur are entertainers and performers, skilled in the arts of emotion and performance.",
        "note": "Must have Project Emotion talent AND at least one of the mandatory focuses",
    },
}


def get_faction(name):
    """Get a faction by name (case-insensitive)."""
    name_lower = name.lower()
    for key, faction in FACTIONS.items():
        if key.lower() == name_lower:
            return faction
    return None


def get_all_faction_names():
    """Get a list of all faction names."""
    return sorted(FACTIONS.keys())


def validate_faction_talents(character, faction_name):
    """
    Validate that a character has the required talents for a faction.
    
    Args:
        character: The character to validate
        faction_name: Name of the faction
        
    Returns:
        tuple: (is_valid: bool, message: str, missing: list)
    """
    faction = get_faction(faction_name)
    if not faction:
        return (False, f"Unknown faction: {faction_name}", [])
    
    mandatory_talents = faction.get("mandatory_talents", [])
    if not mandatory_talents:
        return (True, "No mandatory talents required", [])
    
    character_talents = character.db.stats.get("talents", [])
    if not character_talents:
        character_talents = character.db.stats.get("traits", [])
    
    # Convert to lowercase for comparison
    char_talents_lower = [t.lower() for t in character_talents]
    
    # Check if faction requires ALL talents or just ONE
    note = faction.get("note", "")
    requires_all = "both" in note.lower() or "all" in note.lower() or len(mandatory_talents) == 1
    requires_one = "at least one" in note.lower() or "one of" in note.lower()
    
    # Special case: Tleilaxu Face Dancer requires both
    if faction_name == "Tleilaxu Face Dancer":
        requires_all = True
    
    if requires_all and not requires_one:
        # Must have all mandatory talents
        missing = []
        for talent in mandatory_talents:
            # Check for exact match or partial match (for talents with parameters like "Resilience (Battle)")
            talent_lower = talent.lower()
            found = False
            for char_talent in char_talents_lower:
                # Check if talent matches (handles "Resilience (Battle)" vs "Resilience")
                if talent_lower == char_talent or talent_lower in char_talent or char_talent in talent_lower:
                    found = True
                    break
            if not found:
                missing.append(talent)
        
        if missing:
            return (False, f"Missing required talents: {', '.join(missing)}", missing)
        return (True, "All mandatory talents present", [])
    
    else:
        # Must have at least one
        found_any = False
        for talent in mandatory_talents:
            talent_lower = talent.lower()
            for char_talent in char_talents_lower:
                # Check if talent matches (handles "Resilience (Battle)" vs "Resilience")
                if talent_lower == char_talent or talent_lower in char_talent or char_talent in talent_lower:
                    found_any = True
                    break
            if found_any:
                break
        
        if not found_any:
            return (False, f"Must have at least one of: {', '.join(mandatory_talents)}", mandatory_talents)
        return (True, "Required talent(s) present", [])


def validate_faction_focuses(character, faction_name):
    """
    Validate that a character has the required focuses for a faction.
    
    Args:
        character: The character to validate
        faction_name: Name of the faction
        
    Returns:
        tuple: (is_valid: bool, message: str, missing: list)
    """
    faction = get_faction(faction_name)
    if not faction:
        return (False, f"Unknown faction: {faction_name}", [])
    
    mandatory_focuses = faction.get("mandatory_focuses", [])
    if not mandatory_focuses:
        return (True, "No mandatory focuses required", [])
    
    character_focuses = character.db.stats.get("focuses", [])
    if not character_focuses:
        return (False, f"Must have at least one of: {', '.join(mandatory_focuses)}", mandatory_focuses)
    
    # Convert to lowercase for comparison
    char_focuses_lower = [f.lower() for f in character_focuses]
    
    # Check if any focus matches (allows for "skill: focus" format)
    found_any = False
    for required_focus in mandatory_focuses:
        required_lower = required_focus.lower()
        for char_focus in char_focuses_lower:
            # Check if the required focus appears in the character's focus
            # Handles both "Acting" and "Communicate: Acting" formats
            if required_lower in char_focus or char_focus.endswith(required_lower):
                found_any = True
                break
        if found_any:
            break
    
    if not found_any:
        return (False, f"Must have at least one focus from: {', '.join(mandatory_focuses)}", mandatory_focuses)
    return (True, "Required focus(es) present", [])

