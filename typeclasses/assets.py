"""
Assets

Assets are items that characters can possess in Dune. There are four types:
- Personal: Items that can be carried by individual characters
- Warfare: Items too large for one person (heavy ordnance, soldiers, vehicles)
- Espionage: Used for assassination, stealth, and information gathering
- Intrigue: Used in social occasions, often intangible (favors, debts, reputation)

Assets are stored as objects in a character's inventory.
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent

# Import all asset data
from world.dune.personal_assets_data import PERSONAL_ASSETS
from world.dune.warfare_assets_data import WARFARE_ASSETS
from world.dune.espionage_assets_data import ESPIONAGE_ASSETS
from world.dune.intrigue_assets_data import INTRIGUE_ASSETS

# Combined asset dictionaries for lookup
ALL_ASSETS = {**PERSONAL_ASSETS, **WARFARE_ASSETS, **ESPIONAGE_ASSETS, **INTRIGUE_ASSETS}


class Asset(ObjectParent, DefaultObject):
    """
    An Asset represents a game item in Dune. Assets can be Personal, Warfare,
    Espionage, or Intrigue types.
    
    Attributes:
        asset_type (str): Type of asset - "Personal", "Warfare", "Espionage", or "Intrigue"
        keywords (list): List of keywords describing the asset (e.g., ["Melee Weapon", "Concealable"])
        quality (int): Quality rating of the asset (0-5, or "Special" for some assets)
        description (str): Full description of the asset
        special (str): Special rules or properties of the asset
    """
    
    def at_object_creation(self):
        """
        Called once when the asset is first created.
        """
        super().at_object_creation()
        
        # Initialize asset properties
        self.db.asset_type = "Personal"  # Default to Personal
        self.db.keywords = []
        self.db.quality = 0
        self.db.description = ""
        self.db.special = ""
        
        # Assets should be visible to their owner but not show in room descriptions
        # They'll be in inventory (character's contents) and visible there
    
    def get_asset_type(self):
        """Get the asset type."""
        return self.db.asset_type or "Personal"
    
    def set_asset_type(self, asset_type):
        """Set the asset type."""
        valid_types = ["Personal", "Warfare", "Espionage", "Intrigue"]
        if asset_type not in valid_types:
            return False
        self.db.asset_type = asset_type
        return True
    
    def get_keywords(self):
        """Get the keywords list."""
        return self.db.keywords or []
    
    def add_keyword(self, keyword):
        """Add a keyword."""
        if not self.db.keywords:
            self.db.keywords = []
        if keyword not in self.db.keywords:
            self.db.keywords.append(keyword)
    
    def remove_keyword(self, keyword):
        """Remove a keyword."""
        if keyword in self.db.keywords:
            self.db.keywords.remove(keyword)
    
    def get_quality(self):
        """Get the quality rating."""
        return self.db.quality or 0
    
    def set_quality(self, quality):
        """Set the quality rating (0-5, or "Special")."""
        if quality == "Special" or (isinstance(quality, int) and 0 <= quality <= 5):
            self.db.quality = quality
            return True
        return False
    
    def get_description(self):
        """Get the full description."""
        return self.db.description or ""
    
    def set_description(self, description):
        """Set the full description."""
        self.db.description = description
    
    def get_special(self):
        """Get special rules/properties."""
        return self.db.special or ""
    
    def set_special(self, special):
        """Set special rules/properties."""
        self.db.special = special
    
    def is_architect_capable(self):
        """
        Determine if this asset can be used in Architect mode (remotely).
        
        Architect-capable assets can be used from a distance without direct
        presence. Examples include:
        - Warfare assets: Squads of soldiers, remote vehicles
        - Espionage assets: Intelligence, anonymous communications
        - Intrigue assets: Favors, debts, blackmail that can be used remotely
        
        Personal assets typically require direct presence (Agent mode).
        
        Returns:
            bool: True if asset can be used remotely, False otherwise
        """
        asset_type = self.get_asset_type()
        keywords = self.get_keywords()
        keywords_lower = [k.lower() for k in keywords]
        
        # Personal assets generally require direct presence (Agent mode)
        if asset_type == "Personal":
            # Exception: Some personal assets might be remote if they have specific keywords
            # For now, Personal assets are agent-mode only
            return False
        
        # Warfare assets are typically architect-capable (soldiers, vehicles, etc.)
        if asset_type == "Warfare":
            return True
        
        # Espionage assets are often architect-capable (intelligence, anonymous methods)
        if asset_type == "Espionage":
            # Most espionage assets can be used remotely
            # Exception: Direct weapons like garrotes require presence
            if any(kw in keywords_lower for kw in ["melee weapon", "garrote", "slip-tip"]):
                return False
            return True
        
        # Intrigue assets are typically architect-capable (favors, debts, blackmail)
        if asset_type == "Intrigue":
            return True
        
        return False
    
    def is_agent_mode_only(self):
        """
        Determine if this asset requires direct presence (Agent mode only).
        
        Returns:
            bool: True if asset requires direct presence, False if it can be used remotely
        """
        return not self.is_architect_capable()
    
    def get_detailed_display(self):
        """
        Get a detailed display of the asset for inventory view.
        
        Returns:
            str: Formatted asset information
        """
        lines = []
        lines.append(f"|w{self.name}|n")
        
        asset_type = self.get_asset_type()
        quality = self.get_quality()
        keywords = self.get_keywords()
        description = self.get_description()
        special = self.get_special()
        
        lines.append(f"|yType:|n {asset_type}")
        
        if quality:
            if quality == "Special":
                lines.append(f"|yQuality:|n Special")
            else:
                lines.append(f"|yQuality:|n {quality}")
        
        if keywords:
            lines.append(f"|yKeywords:|n {', '.join(keywords)}")
        
        # Show playstyle compatibility
        if self.is_architect_capable():
            lines.append(f"|yPlaystyle:|n |cArchitect|n (can be used remotely)")
        else:
            lines.append(f"|yPlaystyle:|n |mAgent|n (requires direct presence)")
        
        if description:
            lines.append(f"|yDescription:|n {description}")
        
        if special:
            lines.append(f"|ySpecial:|n {special}")
        
        return "\n".join(lines)


# Asset creation functions

def create_personal_asset(asset_name, character=None):
    """
    Create a Personal Asset object.
    
    Args:
        asset_name (str): Name of the asset to create
        character (Character, optional): Character to give the asset to
        
    Returns:
        Asset: The created Asset object, or None if asset_name not found
    """
    from evennia import create_object
    
    if asset_name not in PERSONAL_ASSETS:
        return None
    
    asset_data = PERSONAL_ASSETS[asset_name]
    
    # Create the asset object
    asset = create_object(
        Asset,
        key=asset_name,
        location=character if character else None
    )
    
    # Set asset properties
    asset.set_asset_type(asset_data["asset_type"])
    asset.set_quality(asset_data["quality"])
    asset.set_description(asset_data["description"])
    asset.set_special(asset_data["special"])
    
    # Add keywords
    for keyword in asset_data["keywords"]:
        asset.add_keyword(keyword)
    
    return asset


def create_warfare_asset(asset_name, character=None):
    """
    Create a Warfare Asset object.
    
    Args:
        asset_name (str): Name of the asset to create
        character (Character, optional): Character to give the asset to
        
    Returns:
        Asset: The created Asset object, or None if asset_name not found
    """
    from evennia import create_object
    
    if asset_name not in WARFARE_ASSETS:
        return None
    
    asset_data = WARFARE_ASSETS[asset_name]
    
    # Create the asset object
    asset = create_object(
        Asset,
        key=asset_name,
        location=character if character else None
    )
    
    # Set asset properties
    asset.set_asset_type(asset_data["asset_type"])
    asset.set_quality(asset_data["quality"])
    asset.set_description(asset_data["description"])
    asset.set_special(asset_data["special"])
    
    # Add keywords
    for keyword in asset_data["keywords"]:
        asset.add_keyword(keyword)
    
    return asset


def create_espionage_asset(asset_name, character=None):
    """
    Create an Espionage Asset object.
    
    Args:
        asset_name (str): Name of the asset to create
        character (Character, optional): Character to give the asset to
        
    Returns:
        Asset: The created Asset object, or None if asset_name not found
    """
    from evennia import create_object
    
    if asset_name not in ESPIONAGE_ASSETS:
        return None
    
    asset_data = ESPIONAGE_ASSETS[asset_name]
    
    # Create the asset object
    asset = create_object(
        Asset,
        key=asset_name,
        location=character if character else None
    )
    
    # Set asset properties
    asset.set_asset_type(asset_data["asset_type"])
    asset.set_quality(asset_data["quality"])
    asset.set_description(asset_data["description"])
    asset.set_special(asset_data["special"])
    
    # Add keywords
    for keyword in asset_data["keywords"]:
        asset.add_keyword(keyword)
    
    return asset


def create_custom_asset(name, asset_type, character=None, quality=0, keywords=None, description="", special=""):
    """
    Create a custom Asset object (not from predefined data).
    Used for assets created during conflicts or as rewards.
    
    Args:
        name (str): Name of the asset
        asset_type (str): Type of asset ("Personal", "Warfare", "Espionage", "Intrigue")
        character (Character, optional): Character to give the asset to
        quality (int): Quality rating (0-5, default 0)
        keywords (list, optional): List of keywords
        description (str): Description of the asset
        special (str): Special rules or properties
        
    Returns:
        Asset: The created Asset object, or None if invalid
    """
    from evennia import create_object
    
    valid_types = ["Personal", "Warfare", "Espionage", "Intrigue"]
    if asset_type not in valid_types:
        return None
    
    # Create the asset object
    asset = create_object(
        Asset,
        key=name,
        location=character if character else None
    )
    
    # Set asset properties
    asset.set_asset_type(asset_type)
    asset.set_quality(quality)
    asset.set_description(description)
    asset.set_special(special)
    
    # Add keywords
    if keywords:
        for keyword in keywords:
            asset.add_keyword(keyword)
    
    # Mark as custom asset (not from predefined data)
    asset.db.is_custom = True
    
    return asset


def create_intrigue_asset(asset_name, character=None):
    """
    Create an Intrigue Asset object.
    
    Args:
        asset_name (str): Name of the asset to create
        character (Character, optional): Character to give the asset to
        
    Returns:
        Asset: The created Asset object, or None if asset_name not found
    """
    from evennia import create_object
    
    if asset_name not in INTRIGUE_ASSETS:
        return None
    
    asset_data = INTRIGUE_ASSETS[asset_name]
    
    # Create the asset object
    asset = create_object(
        Asset,
        key=asset_name,
        location=character if character else None
    )
    
    # Set asset properties
    asset.set_asset_type(asset_data["asset_type"])
    asset.set_quality(asset_data["quality"])
    asset.set_description(asset_data["description"])
    asset.set_special(asset_data["special"])
    
    # Add keywords
    for keyword in asset_data["keywords"]:
        asset.add_keyword(keyword)
    
    return asset


# Asset name retrieval functions

def get_all_personal_asset_names():
    """
    Get a list of all Personal Asset names.
    
    Returns:
        list: List of asset names
    """
    return sorted(PERSONAL_ASSETS.keys())


def get_all_warfare_asset_names():
    """
    Get a list of all Warfare Asset names.
    
    Returns:
        list: List of asset names
    """
    return sorted(WARFARE_ASSETS.keys())


def get_all_espionage_asset_names():
    """
    Get a list of all Espionage Asset names.
    
    Returns:
        list: List of asset names
    """
    return sorted(ESPIONAGE_ASSETS.keys())


def get_all_intrigue_asset_names():
    """
    Get a list of all Intrigue Asset names.
    
    Returns:
        list: List of asset names
    """
    return sorted(INTRIGUE_ASSETS.keys())


# Re-export for backward compatibility
__all__ = [
    'Asset',
    'PERSONAL_ASSETS',
    'WARFARE_ASSETS',
    'ESPIONAGE_ASSETS',
    'INTRIGUE_ASSETS',
    'ALL_ASSETS',
    'create_personal_asset',
    'create_warfare_asset',
    'create_espionage_asset',
    'create_intrigue_asset',
    'create_custom_asset',
    'get_all_personal_asset_names',
    'get_all_warfare_asset_names',
    'get_all_espionage_asset_names',
    'get_all_intrigue_asset_names',
]

