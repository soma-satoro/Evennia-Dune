"""
Titles for Dune Character Generation

Titles define noble ranks within Houses. Higher titles allow architect-level play,
while lower titles are primarily for roleplay and background information.
"""

# Title definitions
# Structure: {
#   "title_key": {
#       "masculine": "Title",
#       "feminine": "Title",
#       "category": "Major|Noble|Minor|Lesser|Singular",
#       "hierarchy_level": int,  # Higher = more authority (for architect access)
#       "hereditary": bool,
#       "architect_access": "full|limited|none",
#       "description": "Description of the title"
#   }
# }

TITLES = {
    # Singular titles
    "padishah_emperor": {
        "masculine": "Padishah Emperor",
        "feminine": "Padishah Empress",
        "category": "Singular",
        "hierarchy_level": 100,
        "hereditary": True,
        "architect_access": "full",
        "description": "The supreme ruler of the Known Universe, the Padishah Emperor holds absolute authority over all Great Houses and the Imperium.",
    },
    
    # Major Titles (hereditary, hierarchical)
    "prince": {
        "masculine": "Prince",
        "feminine": "Princess",
        "category": "Major",
        "hierarchy_level": 9,
        "hereditary": True,
        "architect_access": "full",
        "description": "The highest noble rank, typically held by leaders of Great Houses. Princes have full authority over their domains.",
    },
    "archduke": {
        "masculine": "Archduke",
        "feminine": "Archduchess",
        "category": "Major",
        "hierarchy_level": 8,
        "hereditary": True,
        "architect_access": "full",
        "description": "A high-ranking noble title, second only to Prince. Archdukes command vast territories and resources.",
    },
    "grand_duke": {
        "masculine": "Grand Duke",
        "feminine": "Grand Duchess",
        "category": "Major",
        "hierarchy_level": 7,
        "hereditary": True,
        "architect_access": "full",
        "description": "A prestigious noble title indicating leadership of a major House or significant domain.",
    },
    "duke": {
        "masculine": "Duke",
        "feminine": "Duchess",
        "category": "Major",
        "hierarchy_level": 6,
        "hereditary": True,
        "architect_access": "full",
        "description": "A powerful noble title, often held by leaders of Major Houses. Dukes have significant authority and resources.",
    },
    "duce": {
        "masculine": "Duce",
        "feminine": "Duchess",  # Same as Duke
        "category": "Major",
        "hierarchy_level": 6,
        "hereditary": True,
        "architect_access": "full",
        "description": "An alternative title for Duke, used by some Houses with different cultural traditions.",
    },
    "doge": {
        "masculine": "Doge",
        "feminine": "Duchess",  # Same as Duke
        "category": "Major",
        "hierarchy_level": 6,
        "hereditary": True,
        "architect_access": "full",
        "description": "An alternative title for Duke, used by some Houses with different cultural traditions.",
    },
    "emir": {
        "masculine": "Emir",
        "feminine": "Emira",
        "category": "Major",
        "hierarchy_level": 6,
        "hereditary": True,
        "architect_access": "full",
        "description": "An alternative title for Duke, used by some Houses with different cultural traditions.",
    },
    "jarl": {
        "masculine": "Jarl",
        "feminine": "Jarless",
        "category": "Major",
        "hierarchy_level": 5,
        "hereditary": True,
        "architect_access": "full",
        "description": "A noble title used by some Houses, typically indicating leadership of a Major House.",
    },
    
    # Noble Titles (hereditary, non-hierarchical - same authority level)
    "marquess": {
        "masculine": "Marquess",
        "feminine": "Marchioness",
        "category": "Noble",
        "hierarchy_level": 4,
        "hereditary": True,
        "architect_access": "full",
        "description": "A high-ranking noble title, often held by leaders of Major Houses. Equivalent in authority to Count or Viscount.",
    },
    "margrave": {
        "masculine": "Margrave",
        "feminine": "Margravine",
        "category": "Noble",
        "hierarchy_level": 4,
        "hereditary": True,
        "architect_access": "full",
        "description": "An alternative title for Marquess, used by some Houses with different cultural traditions.",
    },
    "count": {
        "masculine": "Count",
        "feminine": "Countess",
        "category": "Noble",
        "hierarchy_level": 4,
        "hereditary": True,
        "architect_access": "full",
        "description": "A high-ranking noble title, often held by leaders of Major Houses. Equivalent in authority to Marquess or Viscount.",
    },
    "earl": {
        "masculine": "Earl",
        "feminine": "Countess",  # Same as Count
        "category": "Noble",
        "hierarchy_level": 4,
        "hereditary": True,
        "architect_access": "full",
        "description": "An alternative title for Count, used by some Houses with different cultural traditions.",
    },
    "viscount": {
        "masculine": "Viscount",
        "feminine": "Viscountess",
        "category": "Noble",
        "hierarchy_level": 4,
        "hereditary": True,
        "architect_access": "full",
        "description": "A high-ranking noble title, often held by leaders of Major Houses. Equivalent in authority to Marquess or Count.",
    },
    
    # Minor Titles (hereditary, hierarchical from 'baron')
    "baron": {
        "masculine": "Baron",
        "feminine": "Baroness",
        "category": "Minor",
        "hierarchy_level": 3,
        "hereditary": True,
        "architect_access": "limited",
        "description": "A minor noble title, often held by leaders of Minor Houses. Barons have limited architect access.",
    },
    "baronet": {
        "masculine": "Baronet",
        "feminine": "Baronetess",
        "category": "Minor",
        "hierarchy_level": 2,
        "hereditary": True,
        "architect_access": "limited",
        "description": "A minor hereditary title, below Baron in hierarchy. Baronets have limited architect access.",
    },
    "castellan": {
        "masculine": "Castellan",
        "feminine": "Castellan",
        "category": "Minor",
        "hierarchy_level": 2,
        "hereditary": True,
        "architect_access": "limited",
        "description": "A minor hereditary title, often indicating leadership of a Minor House or fortress. Equivalent to Baronet.",
    },
    "burgrave": {
        "masculine": "Burgrave",
        "feminine": "Burgravine",
        "category": "Minor",
        "hierarchy_level": 1,
        "hereditary": True,
        "architect_access": "none",
        "description": "A minor hereditary title, below Baronet in hierarchy. Primarily for roleplay.",
    },
    
    # Lesser Titles (non-hereditary, non-hierarchical)
    "vidame": {
        "masculine": "Vidame",
        "feminine": "Vidame",
        "category": "Lesser",
        "hierarchy_level": 1,
        "hereditary": False,
        "architect_access": "none",
        "description": "A non-hereditary title awarded for service to a House. Primarily for roleplay.",
    },
    "knight": {
        "masculine": "Knight",
        "feminine": "Dame",
        "category": "Lesser",
        "hierarchy_level": 1,
        "hereditary": False,
        "architect_access": "none",
        "description": "A non-hereditary title awarded for service to a House. Primarily for roleplay.",
    },
    "lord": {
        "masculine": "Lord",
        "feminine": "Lady",
        "category": "Lesser",
        "hierarchy_level": 1,
        "hereditary": False,
        "architect_access": "none",
        "description": "A non-hereditary title awarded for service to a House. Primarily for roleplay.",
    },
    "fidalgo": {
        "masculine": "Fidalgo",
        "feminine": "Fidalga",
        "category": "Lesser",
        "hierarchy_level": 1,
        "hereditary": False,
        "architect_access": "none",
        "description": "A non-hereditary title awarded for service to a House. Primarily for roleplay.",
    },
    "esquire": {
        "masculine": "Esquire",
        "feminine": "Esquire",
        "category": "Lesser",
        "hierarchy_level": 1,
        "hereditary": False,
        "architect_access": "none",
        "description": "A non-hereditary title awarded for service to a House. Primarily for roleplay.",
    },
    "sidi": {
        "masculine": "Sidi",
        "feminine": "Sidi",
        "category": "Lesser",
        "hierarchy_level": 1,
        "hereditary": False,
        "architect_access": "none",
        "description": "A non-hereditary title awarded for service to a House. Primarily for roleplay.",
    },
}

# Title categories for organization
TITLE_CATEGORIES = {
    "Singular": ["padishah_emperor"],
    "Major": ["prince", "archduke", "grand_duke", "duke", "duce", "doge", "emir", "jarl"],
    "Noble": ["marquess", "margrave", "count", "earl", "viscount"],
    "Minor": ["baron", "baronet", "castellan", "burgrave"],
    "Lesser": ["vidame", "knight", "lord", "fidalgo", "esquire", "sidi"],
}

# Get all title keys
ALL_TITLE_KEYS = list(TITLES.keys())


def get_title(title_key):
    """Get a title definition by key (case-insensitive)."""
    title_key_lower = title_key.lower().replace(" ", "_").replace("-", "_")
    for key, title in TITLES.items():
        if key.lower() == title_key_lower:
            return title
        # Also check masculine/feminine names
        if title["masculine"].lower() == title_key_lower or title["feminine"].lower() == title_key_lower:
            return title
    return None


def get_title_by_name(title_name, gender="masculine"):
    """
    Get a title by its display name (masculine or feminine).
    
    Args:
        title_name: The display name of the title
        gender: "masculine" or "feminine" to determine which form to match
        
    Returns:
        tuple: (title_key, title_dict) or (None, None)
    """
    title_name_lower = title_name.lower().strip()
    for key, title in TITLES.items():
        if gender == "masculine" and title["masculine"].lower() == title_name_lower:
            return (key, title)
        elif gender == "feminine" and title["feminine"].lower() == title_name_lower:
            return (key, title)
        # Also try both
        if title["masculine"].lower() == title_name_lower or title["feminine"].lower() == title_name_lower:
            return (key, title)
    return (None, None)


def get_all_titles():
    """Get all title definitions."""
    return TITLES


def get_titles_by_category(category):
    """Get all title keys in a specific category."""
    return TITLE_CATEGORIES.get(category, [])


def get_title_display_name(title_key, gender="masculine"):
    """
    Get the display name for a title based on gender.
    
    Args:
        title_key: The key of the title
        gender: "masculine" or "feminine"
        
    Returns:
        str: The display name, or None if title not found
    """
    title = TITLES.get(title_key)
    if not title:
        return None
    return title.get(gender, title["masculine"])


def get_architect_access_for_title(title_key):
    """
    Get the architect access level for a title.
    
    Args:
        title_key: The key of the title
        
    Returns:
        str: "full", "limited", or "none"
    """
    title = TITLES.get(title_key)
    if not title:
        return "none"
    return title.get("architect_access", "none")


def is_title_hereditary(title_key):
    """Check if a title is hereditary."""
    title = TITLES.get(title_key)
    if not title:
        return False
    return title.get("hereditary", False)

