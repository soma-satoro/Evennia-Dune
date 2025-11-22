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

