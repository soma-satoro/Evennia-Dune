"""
Archetypes for Dune Character Generation

Archetypes define the starting package for characters including:
- Trait (archetype name)
- Primary and secondary skills
- Suggested focuses
- Suggested talents
- Suggested drives
"""

ARCHETYPES = {
    # BATTLE ARCHETYPES
    "Duelist": {
        "trait": "Duelist",
        "category": "Battle",
        "description": "Mastery of the blade is a valuable skill in the Imperium, and those who are especially capable are highly sought-after by the rulers of noble Houses, serving as bodyguards, champions, favored gladiators, and even tutors, teaching their skills to others in the House.",
        "primary_skill": "Battle",
        "secondary_skill": "Move",
        "suggested_focuses": ["Dueling", "Short Blades"],
        "suggested_talents": ["The Slow Blade"],
        "suggested_drives": ["Justice", "Faith"],
    },
    "Sergeant": {
        "trait": "Sergeant",
        "category": "Battle",
        "description": "Amongst the rank-and-file troops of a House, and similarly amongst the various mercenary companies that drift from world to world, a select few stand out as leaders, earning the respect and loyalty of their subordinates.",
        "primary_skill": "Battle",
        "secondary_skill": "Communicate",
        "suggested_focuses": ["Long Blades", "Strategy"],
        "suggested_talents": ["Master-at-Arms"],
        "suggested_drives": ["Duty", "Justice"],
    },
    "Tactician": {
        "trait": "Tactician",
        "category": "Battle",
        "description": "Where a strategist orchestrates the grand plan of battle, tacticians direct the fighting on a smaller scale. A mercenary company, or a House regiment, may have a handful of tactical experts.",
        "primary_skill": "Battle",
        "secondary_skill": "Understand",
        "suggested_focuses": ["Combat Awareness", "Tactics"],
        "suggested_talents": ["Decisive Action"],
        "suggested_drives": ["Power", "Justice"],
    },
    "Warrior": {
        "trait": "Warrior",
        "category": "Battle",
        "description": "Might at arms is a necessary part of the politics of the Imperium. While restrained by the traditions and rules of kanly, each House maintains a standing army for defending its people and territory.",
        "primary_skill": "Battle",
        "secondary_skill": "Discipline",
        "suggested_focuses": ["Dirty Fighting", "Long Blade"],
        "suggested_talents": ["To Fight Someone Is to Know Them"],
        "suggested_drives": ["Power", "Justice"],
    },
    
    # COMMUNICATE ARCHETYPES
    "Commander": {
        "trait": "Commander",
        "category": "Communicate",
        "description": "Commanders are senior leaders of military forces; their role is to decide upon a plan of action and give orders to their subordinates.",
        "primary_skill": "Communicate",
        "secondary_skill": "Battle",
        "suggested_focuses": ["Inspiration", "Leadership"],
        "suggested_talents": ["Specialist (Warfare Assets)"],
        "suggested_drives": ["Duty", "Power"],
    },
    "Courtier": {
        "trait": "Courtier",
        "category": "Communicate",
        "description": "Courtiers are the assorted attendants, advisors, clerks, agents, and others with positions at court, or access to the rulers of the House.",
        "primary_skill": "Communicate",
        "secondary_skill": "Understand",
        "suggested_focuses": ["Charm", "Musical Instrument"],
        "suggested_talents": ["Subtle Words"],
        "suggested_drives": ["Power", "Duty"],
    },
    "Envoy": {
        "trait": "Envoy",
        "category": "Communicate",
        "description": "Representatives of their employers in negotiations and diplomacy, envoys are charged with traveling from place to place, conveying the will and words of their masters wherever it is required.",
        "primary_skill": "Communicate",
        "secondary_skill": "Move",
        "suggested_focuses": ["Diplomacy", "Persuasion"],
        "suggested_talents": ["Binding Promise"],
        "suggested_drives": ["Duty", "Justice"],
    },
    "Steward": {
        "trait": "Steward",
        "category": "Communicate",
        "description": "The running of a House is a complex, burdensome matter, and those who rule over each House typically delegate many of those tasks and responsibilities to trusted subordinates.",
        "primary_skill": "Communicate",
        "secondary_skill": "Discipline",
        "suggested_focuses": ["Leadership", "Negotiation"],
        "suggested_talents": ["Stirring Rhetoric"],
        "suggested_drives": ["Duty", "Power"],
    },
    
    # DISCIPLINE ARCHETYPES
    "Analyst": {
        "trait": "Analyst",
        "category": "Discipline",
        "description": "Analysts are often in the employ of noble Houses to study the details and trends of business, politics, and warfare. Mentats are especially valuable as analysts.",
        "primary_skill": "Discipline",
        "secondary_skill": "Understand",
        "suggested_focuses": ["Attention to Detail", "Composure"],
        "suggested_talents": ["Intense Study"],
        "suggested_drives": ["Truth", "Duty"],
    },
    "Herald": {
        "trait": "Herald",
        "category": "Discipline",
        "description": "Many Houses in the Landsraad appoint ceremonial officers to handle matters of heraldry, genealogy, and similar matters of rank and pedigree.",
        "primary_skill": "Discipline",
        "secondary_skill": "Communicate",
        "suggested_focuses": ["Command", "Composure"],
        "suggested_talents": ["Rigorous Control"],
        "suggested_drives": ["Faith", "Duty"],
    },
    "Infiltrator": {
        "trait": "Infiltrator",
        "category": "Discipline",
        "description": "Skilled at finding their way into secure places, infiltrators are an important part of the interplay between Houses and the other great organizations of the Imperium.",
        "primary_skill": "Discipline",
        "secondary_skill": "Move",
        "suggested_focuses": ["Infiltration", "Precision"],
        "suggested_talents": ["Subtle Step"],
        "suggested_drives": ["Truth", "Power"],
    },
    "Protector": {
        "trait": "Protector",
        "category": "Discipline",
        "description": "Security is a must for anyone of wealth and status, and protectors are those most capable of providing that. Any House will contain a cadre of trained bodyguards and security personnel.",
        "primary_skill": "Discipline",
        "secondary_skill": "Battle",
        "suggested_focuses": ["Resolve", "Self-Control"],
        "suggested_talents": ["Bolster"],
        "suggested_drives": ["Duty", "Justice"],
    },
    
    # MOVE ARCHETYPES
    "Athlete": {
        "trait": "Athlete",
        "category": "Move",
        "description": "Athletes are those who hone their bodies to achieve great feats of physical prowess. They're often employed as practitioners of sports and games to entertain, but also as teachers and trainers.",
        "primary_skill": "Move",
        "secondary_skill": "Discipline",
        "suggested_focuses": ["Grace", "Stamina"],
        "suggested_talents": ["Nimble"],
        "suggested_drives": ["Power", "Faith"],
    },
    "Messenger": {
        "trait": "Messenger",
        "category": "Move",
        "description": "Sending messages and packages quickly and securely is a vital part of the business of the Houses, and they rely heavily upon those who can move a communiqué or valuable item reliably to its destination.",
        "primary_skill": "Move",
        "secondary_skill": "Communicate",
        "suggested_focuses": ["Pilot", "Unobtrusive"],
        "suggested_talents": ["Masterful Innuendo"],
        "suggested_drives": ["Power", "Faith"],
    },
    "Scout": {
        "trait": "Scout",
        "category": "Move",
        "description": "Working alongside military units and exploratory groups, scouts take on the perilous task of venturing ahead of their comrades to discover what lays ahead.",
        "primary_skill": "Move",
        "secondary_skill": "Understand",
        "suggested_focuses": ["Endurance", "Stealth"],
        "suggested_talents": ["Putting Theory into Practice"],
        "suggested_drives": ["Duty", "Truth"],
    },
    "Smuggler": {
        "trait": "Smuggler",
        "category": "Move",
        "description": "Valuable goods often find their ways into hands through unusual or illicit channels, and Smugglers are how that happens.",
        "primary_skill": "Move",
        "secondary_skill": "Battle",
        "suggested_focuses": ["Pilot", "Unobtrusive"],
        "suggested_talents": ["Subtle Step"],
        "suggested_drives": ["Power", "Justice"],
    },
    
    # UNDERSTAND ARCHETYPES
    "Empath": {
        "trait": "Empath",
        "category": "Understand",
        "description": "The ability to detect truth and falsehood when others speak is a valuable and powerful one. Only the Reverend Mothers of the Bene Gesserit have mastered full truthsense, but some individuals are simply born with the knack.",
        "primary_skill": "Understand",
        "secondary_skill": "Communicate",
        "suggested_focuses": ["Body Language", "Social Awareness"],
        "suggested_talents": ["Passive Scrutiny"],
        "suggested_drives": ["Truth", "Power"],
    },
    "Scholar": {
        "trait": "Scholar",
        "category": "Understand",
        "description": "Knowledge is power, and a scholar is a seeker and curator of knowledge. Whether working independently or appointed as an expert advisor to a House, scholars collect, study, and archive information.",
        "primary_skill": "Understand",
        "secondary_skill": "Discipline",
        "suggested_focuses": ["Data Analysis", "Deductive Reasoning"],
        "suggested_talents": ["Intense Study"],
        "suggested_drives": ["Truth", "Power"],
    },
    "Spy": {
        "trait": "Spy",
        "category": "Understand",
        "description": "Espionage is an integral part of the politics between the Houses, the Landsraad, the Spacing Guild, CHOAM, and the other factions in the Imperium, and spies are the ones who perform this work.",
        "primary_skill": "Understand",
        "secondary_skill": "Move",
        "suggested_focuses": ["Deductive Reasoning", "Kanly"],
        "suggested_talents": ["Hidden Motives"],
        "suggested_drives": ["Truth", "Duty"],
    },
    "Strategist": {
        "trait": "Strategist",
        "category": "Understand",
        "description": "Warfare, even within the rules of kanly, is a complex and nuanced affair. Strategists are employed to sift through reams of intelligence on the enemy, and compose the orders of battle, supply chains, deployment of forces, and the overall strategy of war.",
        "primary_skill": "Understand",
        "secondary_skill": "Battle",
        "suggested_focuses": ["Kanly", "Strategy"],
        "suggested_talents": ["Master-at-Arms"],
        "suggested_drives": ["Power", "Faith"],
    },
    
    # FREMEN ARCHETYPES
    "Naib": {
        "trait": "Naib",
        "category": "Battle",
        "requires_faction": "Fremen",
        "description": "The naib fulfils the role of war-leader and protector of the whole sietch, representing the ideals of Fremen society. As such, a naib is also a religious leader in some ways, as the spiritual well-being of the tribe is as important as its physical well-being. The naib must be the toughest and most remorseless of all those who dwell in their sietch.",
        "primary_skill": "Battle",
        "secondary_skill": "Understand",
        "suggested_focuses": ["Dueling", "Leadership"],
        "suggested_talents": ["Ways of the Ichwan Bedwine", "To Fight Someone Is to Know Them"],
        "suggested_drives": ["Duty"],
    },
    "Fedaykin": {
        "trait": "Fedaykin",
        "category": "Battle",
        "requires_faction": "Fremen",
        "description": "Originally the term Fedaykin was simply another word for a warrior or guerilla fighter among the Fremen. However, those who bore the title were among the most dedicated fighters the Fremen had to offer, excelling in hand to hand combat. With the coming of Muad'Dib, the name became synonymous with his elite guard, later considered Paul's 'death commandoes'.",
        "primary_skill": "Battle",
        "secondary_skill": "Move",
        "suggested_focuses": ["Dueling", "Short Blades"],
        "suggested_talents": ["Bold (Battle)", "Crysknife Master"],
        "suggested_drives": ["Justice", "Faith"],
    },
    "Sayyadina": {
        "trait": "Sayyadina",
        "category": "Understand",
        "requires_faction": "Fremen",
        "description": "The spiritual well-being of a tribe is almost as important as water. So nearly each sietch also possesses Sayyadina: priestesses or wise-women. The Sayyadina is a role of great importance, particularly given the Fremen belief in the accuracy of prophecy. It is the Sayyadina who are the keepers of the wisdom and lore the Fremen have accreted over their millennia struggling to survive.",
        "primary_skill": "Understand",
        "secondary_skill": "Communicate",
        "suggested_focuses": ["Deductive Reasoning", "Empathy"],
        "suggested_talents": ["Ways of the Ichwan Bedwine"],
        "suggested_drives": ["Truth"],
    },
    "Sand Runner": {
        "trait": "Sand Runner",
        "category": "Move",
        "requires_faction": "Fremen",
        "description": "While all Fremen learn to ride a worm, some are more skilled than others. Those who prove especially adept are often used as messengers between the tribes. They can call a worm quickly and tame one large enough to take them for a long distance at great speed.",
        "primary_skill": "Move",
        "secondary_skill": "Discipline",
        "suggested_focuses": ["Resolve", "Self-Control"],
        "suggested_talents": ["Chosen of Shai-Hulud", "Peace of Shai-Hulud"],
        "suggested_drives": ["Duty", "Power", "Truth"],
    },
    "Wali": {
        "trait": "Wali",
        "category": "Discipline",
        "requires_faction": "Fremen",
        "description": "The young, untested members of the sietch are known as wali. They are the future of the tribe, still unblooded, untested. Still yet to make their way across the vast desert alone or as part of a small team. Instead, they must wait close to the sietch, listening and learning and abiding by the strict laws of their teachers.",
        "primary_skill": "Discipline",
        "secondary_skill": "Battle",
        "suggested_focuses": ["Self-Control", "Stamina"],
        "suggested_talents": ["Walk Without Rhythm", "Water Wisdom"],
        "suggested_drives": ["Faith", "Power"],
    },
    "Ecologist": {
        "trait": "Ecologist",
        "category": "Discipline",
        "requires_faction": "Fremen",
        "description": "Pardot Kynes dream of a transformed Arrakis fills you with longing and dedication. The ecologist works tirelessly and in secret to see that dream made a reality. It is a dream they know they may never see fulfilled in their lifetime, but that doesn't matter. What matters is the Arrakis they leave for the children of their tribe.",
        "primary_skill": "Discipline",
        "secondary_skill": "Understand",
        "suggested_focuses": ["Ecology", "Precision"],
        "suggested_talents": ["Fremen Technology", "Water Wisdom"],
        "suggested_drives": ["Faith", "Discipline"],
    },
    
    # SPACING GUILD ARCHETYPES
    "Guild Engineer": {
        "trait": "Guild Engineer",
        "category": "Understand",
        "requires_faction": "Spacing Guild",
        "description": "While most people first think of the famous Navigators when the topic of space travel arises, there would be no ships to navigate without the engineers who design and build them. Many Guild engineers never leave their shipyards or drydocks to travel into the field, but plenty of others do, either in service of the Guild or as independent agents.",
        "primary_skill": "Understand",
        "secondary_skill": "Discipline",
        "suggested_focuses": ["Advanced Technology", "Spaceship Technology"],
        "suggested_talents": ["Cool Under Pressure (Understand)", "Putting Theory into Practice"],
        "suggested_drives": ["Duty", "Faith"],
    },
    "Guild Financier": {
        "trait": "Guild Financier",
        "category": "Understand",
        "requires_faction": "Spacing Guild",
        "description": "The Guild's banking institutions are as widespread as its transport facilities and just as important in binding the Imperium together. A legion of clerks and administrators run the system, and above them are an equal number of financial experts who manage the accounts of the noble Houses and try to predict fiscal trends across the Known Universe.",
        "primary_skill": "Understand",
        "secondary_skill": "Communicate",
        "suggested_focuses": ["Finance", "Guild Bureaucracy"],
        "suggested_talents": ["Check the Books", "Methodical Efficiency"],
        "suggested_drives": ["Faith", "Duty", "Justice"],
    },
    "Guild Scientist": {
        "trait": "Guild Scientist",
        "category": "Understand",
        "requires_faction": "Spacing Guild",
        "description": "In many respects the Spacing Guild has operated in the same way for thousands of years, but it still has need for innovation in its technologies and methods. Guild Scientists can travel the Known Universe to study just about anything, though, especially unique phenomena, strange locations, and important discoveries the Guild might want to exploit.",
        "primary_skill": "Understand",
        "secondary_skill": "Communicate",
        "suggested_focuses": ["Mathematics", "Physics"],
        "suggested_talents": ["Intense Study", "Power of Neutrality"],
        "suggested_drives": ["Truth", "Power"],
    },
    "Guild Spy": {
        "trait": "Guild Spy",
        "category": "Communicate",
        "requires_faction": "Spacing Guild",
        "description": "Specially trained Guild Agents perform the dangerous work of infiltrating the territory, installations, and even households of other factions to gain intelligence for the Spacing Guild. In some operations they pose as someone else, while in others their goal is to never be seen at all.",
        "primary_skill": "Communicate",
        "secondary_skill": "Battle",
        "suggested_focuses": ["Espionage", "Infiltration"],
        "suggested_talents": ["Code of Secrecy", "Play Both Ends Against the Middle"],
        "suggested_drives": ["Duty", "Power"],
    },
    "Guild Scout": {
        "trait": "Guild Scout",
        "category": "Move",
        "requires_faction": "Spacing Guild",
        "description": "The Guild has many reasons to send explorers out into the Known Universe. Some of them explore newly discovered planets or seek out cosmic phenomena, the better to understand the universe and its hazards. A few are dedicated to the quest for additional planets where spice exists, or something like it.",
        "primary_skill": "Move",
        "secondary_skill": "Battle",
        "suggested_focuses": ["Pilot (Spaceship)", "Space Navigation"],
        "suggested_talents": ["Power of Neutrality", "Rapid Maneuver"],
        "suggested_drives": ["Duty", "Faith"],
    },
}


def get_archetype(name):
    """Get an archetype by name (case-insensitive)."""
    name_lower = name.lower()
    for key, archetype in ARCHETYPES.items():
        if key.lower() == name_lower:
            return archetype
    return None


def list_archetypes_by_category():
    """Return archetypes organized by category."""
    categories = {
        "Battle": [],
        "Communicate": [],
        "Discipline": [],
        "Move": [],
        "Understand": [],
    }
    
    for name, archetype in ARCHETYPES.items():
        category = archetype.get("category", "Other")
        if category in categories:
            categories[category].append((name, archetype))
    
    return categories


def get_all_archetype_names():
    """Get a list of all archetype names."""
    return sorted(ARCHETYPES.keys())


def get_archetypes_by_faction(faction_name):
    """Get all archetypes available to a specific faction."""
    archetypes = []
    for name, archetype in ARCHETYPES.items():
        required_faction = archetype.get("requires_faction")
        if required_faction and required_faction.lower() == faction_name.lower():
            archetypes.append((name, archetype))
    return sorted(archetypes)


def can_character_take_archetype(character, archetype_name):
    """
    Check if a character can take a specific archetype.
    
    Args:
        character: The character to check
        archetype_name: Name of the archetype
        
    Returns:
        tuple: (can_take: bool, reason: str)
    """
    archetype = get_archetype(archetype_name)
    if not archetype:
        return (False, f"Unknown archetype: {archetype_name}")
    
    required_faction = archetype.get("requires_faction")
    if not required_faction:
        return (True, "Available to all characters")
    
    character_faction = character.db.faction
    if not character_faction:
        return (False, f"This archetype requires the {required_faction} faction. You must set your faction first.")
    
    if character_faction.lower() != required_faction.lower():
        return (False, f"This archetype requires the {required_faction} faction. Your faction ({character_faction}) does not match.")
    
    return (True, f"Available to {required_faction} faction members")

