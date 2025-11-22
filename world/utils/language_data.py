"""
Language data for Numenera setting.

This module contains all available languages in the Ninth World, organized by
their geographic and cultural origins.
"""

# Dictionary of all available languages in Numenera
# Key format: normalized lowercase, Value: proper display name
AVAILABLE_LANGUAGES = {
    # Steadfast Languages
    "the truth": "The Truth",
    "truth": "The Truth",
    "sadarac": "Sadarac",
    "wyrac": "Wyrac",
    "tithac": "Tithac",
    
    # Coras and its dialects
    "coras": "Coras",
    "coras northern": "Coras (Northern)",
    "coras central": "Coras (Central)",
    "coras south": "Coras (South)",
    
    # Beyond Languages
    "mathan": "Mathan",
    "maran": "Maran",
    "seshan": "Seshan",
    "salter": "Salter",
    "ba-du": "Ba-Du",
    
    # Black Riage Languages (various isolated communities)
    "black riage north": "Black Riage (North)",
    "black riage central": "Black Riage (Central)",
    "black riage south": "Black Riage (South)",
    "black riage east": "Black Riage (East)",
    "black riage west": "Black Riage (West)",
    
    # Plains and Jungle Languages
    "kataru": "Kataru",
    "kataru nomadic": "Kataru (Nomadic)",
    "caecilian": "Caecilian",
    "plains trader": "Plains Trader",
    
    # Beyond the Beyond
    "augurian": "Augurian",
    
    # Trade and Common Tongues
    "trader's cant": "Trader's Cant",
    "traveler's tongue": "Traveler's Tongue",
}

# Language family information for reference
LANGUAGE_FAMILIES = {
    "River Languages": {
        "description": "Languages based around major rivers in the Steadfast",
        "languages": ["Sadarac", "Wyrac", "Tithac"],
        "notes": "Spread by trade and historical empires like the Pytharon Empire"
    },
    "Coastal Languages": {
        "description": "Languages spoken along coastlines with distinct regional dialects",
        "languages": ["Coras", "Coras (Northern)", "Coras (Central)", "Coras (South)"],
        "notes": "Heavy maritime trade influence, especially in Central dialect"
    },
    "Divided Seas Family": {
        "description": "Related languages around the Divided Seas region",
        "languages": ["Maran", "Seshan", "Salter"],
        "notes": "Similar enough for rough communication, but distinct dialects"
    },
    "Isolated Languages": {
        "description": "Languages of remote or isolated communities",
        "languages": ["Mathan", "Ba-Du", "Augurian"],
        "notes": "Limited outside influence, unique characteristics"
    },
    "Black Riage Variants": {
        "description": "Isolated mountain communities with unique dialects",
        "languages": ["Black Riage (North)", "Black Riage (Central)", "Black Riage (South)", 
                     "Black Riage (East)", "Black Riage (West)"],
        "notes": "Each community speaks differently due to treacherous terrain limiting contact"
    }
}

# Regional speaking patterns - what languages are common in which areas
REGIONAL_LANGUAGES = {
    "Navarene": ["The Truth", "Tithac", "Coras (Northern)"],
    "Ghan": ["Wyrac", "Coras (Northern)", "The Truth"],
    "Iscobal": ["Sadarac", "Wyrac", "Coras (Central)", "Coras (South)"],
    "Malevich": ["Sadarac", "Wyrac"],
    "Draolis": ["Coras (Central)", "The Truth"],
    "Milave": ["Sadarac", "The Truth"],
    "Ancuan": ["Sadarac", "Coras (South)"],
    "Thaemor": ["Wyrac", "The Truth"],
    "Pytharon Empire": ["Sadarac", "The Truth"],
    "Matheunis": ["Mathan", "Sadarac", "Maran", "Coras (South)"],
    "Seshar": ["Seshan", "Maran"],
    "Ba-Adenu Forest": ["Ba-Du", "Seshan"],
    "Errid Kaloum": ["Salter", "Maran"],
    "Salachia": ["Maran"],
    "Amorphous Fields": ["Maran"],
    "Plains of Kataru": ["Kataru", "Kataru (Nomadic)", "The Truth"],
    "Caecilian Jungle": ["Caecilian"],
    "Augur-Kala": ["Augurian"],
    "The Black Riage": ["Black Riage (North)", "Black Riage (Central)", 
                        "Black Riage (South)", "Black Riage (East)", 
                        "Black Riage (West)", "The Truth"]
}

# Language difficulty for learning (1 = easiest, 5 = hardest)
# This could be used for future implementation of learning time/difficulty
LANGUAGE_DIFFICULTY = {
    "The Truth": 1,  # Most common, widespread
    "Sadarac": 2,
    "Wyrac": 2,
    "Tithac": 2,
    "Coras": 2,
    "Coras (Northern)": 2,
    "Coras (Central)": 1,  # Heavy Truth influence
    "Coras (South)": 3,  # Mixed with Mathan
    "Mathan": 3,
    "Maran": 2,
    "Seshan": 3,
    "Salter": 3,
    "Ba-Du": 4,
    "Black Riage (North)": 4,
    "Black Riage (Central)": 4,
    "Black Riage (South)": 4,
    "Black Riage (East)": 4,
    "Black Riage (West)": 4,
    "Kataru": 3,
    "Kataru (Nomadic)": 3,
    "Caecilian": 4,
    "Augurian": 5,  # Superior humans, difficult to grasp
    "Trader's Cant": 2,
    "Traveler's Tongue": 2,
}

