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
        
        if description:
            lines.append(f"|yDescription:|n {description}")
        
        if special:
            lines.append(f"|ySpecial:|n {special}")
        
        return "\n".join(lines)

