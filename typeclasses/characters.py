"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

This implementation uses the Modiphus 2d20 system for Dune.
"""

from evennia.objects.objects import DefaultCharacter
from .objects import ObjectParent
from typeclasses.titles import get_title, get_architect_access_for_title

# Architect mode role restrictions
# Full architect access - can use all architect capabilities
FULL_ARCHITECT_ROLES = [
    "Ruler", "Consort", "Advisor", "Heir", "Councilor", "Envoy",
    "Marshal", "Spymaster", "Swordmaster", "Treasurer", "Warmaster"
]

# Limited architect access - lower-level architect options
LIMITED_ARCHITECT_ROLES = [
    "Spy", "Agent", "Officer", "Security"
]

# No architect access - agent mode only
NO_ARCHITECT_ROLES = [
    "Chief Physician", "Scholar"
]


class Character(ObjectParent, DefaultCharacter):
    """
    Character class for the Dune MUSH using Modiphus 2d20 system.
    
    Character data is stored in self.db.stats dictionary with the following structure:
    
    - skills: Skills with ratings 0-5 (Battle, Communicate, Discipline, Move, Understand)
    - focuses: List of skill focuses/specializations (e.g., "Short Blades", "music/baliset")
    - talents: Special abilities and characteristics
    - assets: Resources, items, and special possessions
    - drives: Character motivations (duty, faith, justice, power, truth)
    
    Other character attributes:
    - stress: Current stress level (damage)
    - max_stress: Maximum stress (typically 10)
    - determination: Current determination points
    - experience: Experience points
    - house: Great House affiliation
    - faction: Faction/organization membership
    - role: Character role/archetype
    - personality_traits: Personality traits
    - ambition: Character ambition
    - background: Character background/history
    
    Note: Dune 2d20 does not use attributes like other 2d20 games.
    """

    def at_object_creation(self):
        """
        Called once, when this object is first created.
        Set up default character stats for Dune 2d20 system.
        """
        super().at_object_creation()
        
        # Initialize stats dictionary
        self.db.stats = {
            # Skills (range typically 0-5)
            "skills": {
                "battle": 0,       # Combat and warfare
                "communicate": 0,  # Social interaction and persuasion
                "discipline": 0,   # Mental fortitude and focus
                "move": 0,         # Physical movement and athletics
                "understand": 0    # Knowledge and comprehension
            },
            
            # Focuses (specializations within skills)
            "focuses": [],  # Example: ["Short Blades", "music/baliset"]
            
            # Talents (special abilities/traits)
            "talents": [],  # Example: ["Mentat Training", "Bene Gesserit Conditioning"]
            
            # Assets (resources and special items)
            "assets": [],  # Example: ["Personal Shield", "Crysknife"]
            
            # Drives (character motivations)
            # Each drive is stored as {"rating": int, "statement": str}
            # Ratings must be 8, 7, 6, 5, 4 (one of each)
            # Statements are required for drives with rating 6+
            "drives": {
                "duty": {"rating": 0, "statement": ""},       # Obligations and responsibilities
                "faith": {"rating": 0, "statement": ""},      # Beliefs and principles
                "justice": {"rating": 0, "statement": ""},    # Sense of right and wrong
                "power": {"rating": 0, "statement": ""},      # Ambitions and goals
                "truth": {"rating": 0, "statement": ""}       # Quest for knowledge
            }
        }
        
        # Resource tracking
        self.db.stress = 0              # Current stress (health damage)
        self.db.determination = 1       # Determination points (start with 1 per adventure, max 3)
        self.db.experience = 0
        
        # Playstyle mode: "agent" (default) or "architect"
        # Agent mode: Direct action requiring personal presence
        # Architect mode: Remote action using assets from a distance
        self.db.playstyle_mode = "agent"  # Default to agent mode          # Experience points
        
        # Complications - temporary negative effects from rolling 20
        self.db.complications = []  # List of {"skill": str, "name": str, "description": str}
        
        # Crossed out drives - drives that have been challenged and need recovery
        self.db.crossed_out_drives = []  # List of drive names that are crossed out
        
        # Derived stats - In Dune, max stress is typically 10 base
        self.db.max_stress = 10
        
        # Character description fields
        self.db.shortdesc = ""          # Short description for room displays
        self.db.background = ""         # Character background/history
        self.db.house = ""              # Great House affiliation
        self.db.faction = ""            # Faction/organization membership
        self.db.role = ""               # Character role/archetype
        self.db.personality_traits = "" # Personality traits
        self.db.ambition = ""           # Character ambition
        
    def calculate_max_stress(self):
        """
        Calculate maximum stress for Dune.
        Base stress is typically 10 in Dune 2d20.
        """
        return 10
            
    def get_skill(self, skill_name):
        """
        Get a skill value by name.
        
        Args:
            skill_name (str): Name of the skill (e.g., "battle", "communicate")
            
        Returns:
            int: The skill value, or 0 if not found
        """
        return self.db.stats.get("skills", {}).get(skill_name.lower(), 0)
        
    def set_skill(self, skill_name, value):
        """
        Set a skill value.
        
        Args:
            skill_name (str): Name of the skill
            value (int): New value (typically 0-5)
        """
        if "skills" not in self.db.stats:
            self.db.stats["skills"] = {}
        self.db.stats["skills"][skill_name.lower()] = value
        
        # Update max stress if discipline changes
        if skill_name.lower() == "discipline":
            self.db.max_stress = self.calculate_max_stress()
            
    def add_focus(self, focus):
        """
        Add a focus (skill specialization).
        
        Args:
            focus (str): Focus description (e.g., "Battle: Knife Fighting")
        """
        if "focuses" not in self.db.stats:
            self.db.stats["focuses"] = []
        if focus not in self.db.stats["focuses"]:
            self.db.stats["focuses"].append(focus)
            
    def remove_focus(self, focus):
        """
        Remove a focus.
        
        Args:
            focus (str): Focus to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if focus in self.db.stats.get("focuses", []):
            self.db.stats["focuses"].remove(focus)
            return True
        return False
        
    def add_talent(self, talent):
        """
        Add a talent (special ability).
        
        Args:
            talent (str): Talent name
        """
        if "talents" not in self.db.stats:
            self.db.stats["talents"] = []
        if talent not in self.db.stats["talents"]:
            self.db.stats["talents"].append(talent)
    
    def add_trait(self, trait):
        """Legacy method - redirects to add_talent for backwards compatibility."""
        return self.add_talent(trait)
            
    def remove_talent(self, talent):
        """
        Remove a talent.
        
        Args:
            talent (str): Talent to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if talent in self.db.stats.get("talents", []):
            self.db.stats["talents"].remove(talent)
            return True
        return False
    
    def remove_trait(self, trait):
        """Legacy method - redirects to remove_talent for backwards compatibility."""
        return self.remove_talent(trait)
        
    def add_asset(self, asset):
        """
        Add an asset (resource/item).
        
        Args:
            asset (str): Asset description
        """
        if "assets" not in self.db.stats:
            self.db.stats["assets"] = []
        if asset not in self.db.stats["assets"]:
            self.db.stats["assets"].append(asset)
            
    def remove_asset(self, asset):
        """
        Remove an asset (legacy method for string-based assets).
        Note: New assets should be Asset objects in inventory, not strings.
        
        Args:
            asset (str): Asset to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if asset in self.db.stats.get("assets", []):
            self.db.stats["assets"].remove(asset)
            return True
        return False
    
    def get_assets(self):
        """
        Get all Asset objects from inventory.
        
        Returns:
            list: List of Asset objects
        """
        from typeclasses.assets import Asset
        assets = []
        for obj in self.contents:
            if obj.is_typeclass("typeclasses.assets.Asset", exact=False):
                assets.append(obj)
        return assets
    
    def get_assets_by_type(self, asset_type):
        """
        Get assets of a specific type.
        
        Args:
            asset_type (str): Type of asset ("Personal", "Warfare", "Espionage", "Intrigue")
            
        Returns:
            list: List of Asset objects of the specified type
        """
        assets = self.get_assets()
        return [asset for asset in assets if asset.get_asset_type() == asset_type]
    
    def has_asset(self, asset_name):
        """
        Check if character has an asset by name.
        
        Args:
            asset_name (str): Name of the asset to check
            
        Returns:
            Asset or None: The asset if found, None otherwise
        """
        assets = self.get_assets()
        asset_name_lower = asset_name.lower()
        for asset in assets:
            if asset_name_lower == asset.name.lower():
                return asset
        return None
    
    def get_role(self):
        """
        Get the character's role from their House or Organizations.
        Checks both house roles and organization roles.
        
        Returns:
            str: Role name if found, empty string otherwise
        """
        # First check character's direct role attribute
        if self.db.role:
            return self.db.role
        
        # Check house roles
        if self.db.house:
            house = self.db.house
            if hasattr(house, 'db') and hasattr(house.db, 'roles'):
                for role_name, role_info in house.db.roles.items():
                    role_holder = role_info.get("character", "")
                    if role_holder.lower() == self.key.lower():
                        return role_name
        
        # Check organization roles
        if hasattr(self.db, 'organizations') and self.db.organizations:
            for org in self.db.organizations:
                if hasattr(org, 'db') and hasattr(org.db, 'roles'):
                    for role_name, role_info in org.db.roles.items():
                        role_holder = role_info.get("character", "")
                        if role_holder.lower() == self.key.lower():
                            return role_name
        
        return ""
    
    def get_title(self):
        """
        Get the character's title display name.
        
        Returns:
            str: Title display name if found, empty string otherwise
        """
        title_key = self.db.title
        if not title_key:
            return ""
        
        # Get character's gender if set
        gender = getattr(self.db, 'gender', 'masculine')
        if gender not in ['masculine', 'feminine']:
            gender = 'masculine'
        
        from typeclasses.titles import get_title_display_name
        display_name = get_title_display_name(title_key, gender)
        return display_name or ""
    
    def get_architect_access_level(self):
        """
        Determine the character's architect access level based on their title or role.
        Titles take precedence over roles if both exist.
        
        Returns:
            str: "full", "limited", or "none"
        """
        # First check title (titles take precedence)
        title_key = self.db.title
        if title_key:
            title_access = get_architect_access_for_title(title_key)
            if title_access != "none":
                return title_access
        
        # Then check role
        role = self.get_role()
        if not role:
            return "none"
        
        role_lower = role.lower()
        
        # Check for full architect access
        for full_role in FULL_ARCHITECT_ROLES:
            if role_lower == full_role.lower():
                return "full"
        
        # Check for limited architect access
        for limited_role in LIMITED_ARCHITECT_ROLES:
            if role_lower == limited_role.lower():
                return "limited"
        
        # Check for no architect access
        for no_role in NO_ARCHITECT_ROLES:
            if role_lower == no_role.lower():
                return "none"
        
        # Default: no access if role doesn't match any category
        return "none"
    
    def can_use_architect_mode(self):
        """
        Check if character can use Architect mode at all.
        
        Returns:
            bool: True if character has full or limited architect access
        """
        access_level = self.get_architect_access_level()
        return access_level in ["full", "limited"]
    
    def get_playstyle_mode(self):
        """
        Get the character's current playstyle mode.
        
        Returns:
            str: "agent" (default) or "architect"
        """
        return self.db.playstyle_mode or "agent"
    
    def set_playstyle_mode(self, mode):
        """
        Set the character's playstyle mode.
        Enforces role-based restrictions.
        
        Args:
            mode (str): "agent" or "architect"
            
        Returns:
            tuple: (success: bool, message: str)
        """
        valid_modes = ["agent", "architect"]
        if mode.lower() not in valid_modes:
            return (False, "Invalid mode. Must be 'agent' or 'architect'.")
        
        # Agent mode is always allowed
        if mode.lower() == "agent":
            self.db.playstyle_mode = "agent"
            return (True, "Playstyle mode set to Agent.")
        
        # Architect mode requires appropriate title or role
        if mode.lower() == "architect":
            access_level = self.get_architect_access_level()
            if access_level == "none":
                title = self.get_title()
                role = self.get_role()
                if title:
                    return (False, f"You cannot use Architect mode with the title '{title}'. Only Major, Noble, or Minor titles have access to Architect playstyle.")
                elif role:
                    return (False, f"You cannot use Architect mode with the role '{role}'. Only certain roles have access to Architect playstyle.")
                else:
                    return (False, "You must have an appropriate title or role to use Architect mode. Titles take precedence over roles.")
            
            self.db.playstyle_mode = "architect"
            access_msg = "full" if access_level == "full" else "limited"
            title = self.get_title()
            role = self.get_role()
            source = title if title else role
            return (True, f"Playstyle mode set to Architect ({access_msg} access via {source}).")
        
        return (False, "Failed to set playstyle mode.")
    
    def get_architect_capable_assets(self):
        """
        Get all assets that can be used in Architect mode (remotely).
        
        Returns:
            list: List of Asset objects that can be used remotely
        """
        assets = self.get_assets()
        return [asset for asset in assets if asset.is_architect_capable()]
    
    def get_agent_mode_assets(self):
        """
        Get all assets that require direct presence (Agent mode only).
        
        Returns:
            list: List of Asset objects that require direct presence
        """
        assets = self.get_assets()
        return [asset for asset in assets if asset.is_agent_mode_only()]
    
    def get_drive_rating(self, drive_name):
        """
        Get a drive rating by name.
        
        Args:
            drive_name (str): Name of the drive (e.g., "duty", "faith")
            
        Returns:
            int: The drive rating, or 0 if not found
        """
        drives = self.db.stats.get("drives", {})
        drive = drives.get(drive_name.lower(), {})
        
        # Handle legacy format (string instead of dict)
        if isinstance(drive, str):
            return 0
        
        return drive.get("rating", 0) if isinstance(drive, dict) else 0
    
    def get_drive_statement(self, drive_name):
        """
        Get a drive statement by name.
        
        Args:
            drive_name (str): Name of the drive (e.g., "duty", "faith")
            
        Returns:
            str: The drive statement, or empty string if not found
        """
        drives = self.db.stats.get("drives", {})
        drive = drives.get(drive_name.lower(), {})
        
        # Handle legacy format (string instead of dict)
        if isinstance(drive, str):
            return drive if drive else ""
        
        return drive.get("statement", "") if isinstance(drive, dict) else ""
    
    def set_drive_rating(self, drive_name, rating):
        """
        Set a drive rating. Validates that ratings are 8, 7, 6, 5, 4 (one of each).
        
        Args:
            drive_name (str): Name of the drive
            rating (int): New rating (must be 4, 5, 6, 7, or 8)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        drive_name = drive_name.lower()
        valid_drives = ["duty", "faith", "justice", "power", "truth"]
        
        if drive_name not in valid_drives:
            return (False, f"Invalid drive name. Must be one of: {', '.join(valid_drives)}")
        
        if rating not in [4, 5, 6, 7, 8]:
            return (False, "Drive rating must be 4, 5, 6, 7, or 8")
        
        if "drives" not in self.db.stats:
            self.db.stats["drives"] = {}
        
        # Get current drive ratings to check for conflicts
        current_ratings = {}
        for dname in valid_drives:
            d = self.db.stats["drives"].get(dname, {})
            if isinstance(d, dict):
                current_ratings[dname] = d.get("rating", 0)
            else:
                current_ratings[dname] = 0
        
        # Check if this rating is already assigned to another drive
        if rating != 0 and rating in current_ratings.values():
            for dname, r in current_ratings.items():
                if r == rating and dname != drive_name:
                    return (False, f"Rating {rating} is already assigned to {dname}. Each rating (4, 5, 6, 7, 8) must be unique.")
        
        # Initialize drive as dict if it's still in legacy format
        if not isinstance(self.db.stats["drives"].get(drive_name), dict):
            old_statement = ""
            if isinstance(self.db.stats["drives"].get(drive_name), str):
                old_statement = self.db.stats["drives"][drive_name]
            self.db.stats["drives"][drive_name] = {"rating": 0, "statement": old_statement}
        
        # Set the rating - Evennia needs the entire dict reassigned for nested changes
        self.db.stats["drives"][drive_name]["rating"] = rating
        # Force save by reassigning the drives dict
        self.db.stats["drives"] = dict(self.db.stats["drives"])
        
        return (True, f"Set {drive_name} drive rating to {rating}")
    
    def set_drive_statement(self, drive_name, statement):
        """
        Set a drive statement. Only drives with rating 6+ should have statements.
        
        Args:
            drive_name (str): Name of the drive
            statement (str): The drive statement
            
        Returns:
            tuple: (success: bool, message: str)
        """
        drive_name = drive_name.lower()
        valid_drives = ["duty", "faith", "justice", "power", "truth"]
        
        if drive_name not in valid_drives:
            return (False, f"Invalid drive name. Must be one of: {', '.join(valid_drives)}")
        
        if "drives" not in self.db.stats:
            self.db.stats["drives"] = {}
        
        # Initialize drive as dict if it's still in legacy format
        drive_obj = self.db.stats["drives"].get(drive_name)
        if not drive_obj or not hasattr(drive_obj, 'get'):
            old_rating = 0
            if isinstance(drive_obj, str):
                # If it was a string, it was probably a statement, so rating is 0
                old_rating = 0
            self.db.stats["drives"][drive_name] = {"rating": old_rating, "statement": ""}
            # Force save
            self.db.stats["drives"] = dict(self.db.stats["drives"])
        
        # Check rating - statements should only be set for rating 6+
        # Access rating from _SaverDict properly
        drive_obj = self.db.stats["drives"].get(drive_name)
        if drive_obj and hasattr(drive_obj, 'get'):
            # Convert _SaverDict to regular dict to get rating
            try:
                drive_dict = dict(drive_obj) if drive_obj else {}
                rating = drive_dict.get("rating", 0) if isinstance(drive_dict, dict) else 0
            except (TypeError, ValueError):
                rating = drive_obj.get("rating", 0) if hasattr(drive_obj, 'get') else 0
        else:
            rating = 0
        
        if rating < 6 and statement:
            return (False, f"Cannot set statement for {drive_name} (rating {rating}). Statements are only for drives with rating 6 or higher.")
        
        # Set the statement - Evennia needs the entire dict reassigned for nested changes
        self.db.stats["drives"][drive_name]["statement"] = statement
        # Force save by reassigning the drives dict
        self.db.stats["drives"] = dict(self.db.stats["drives"])
        
        return (True, f"Set {drive_name} drive statement: {statement}")
    
    def validate_drive_ratings(self):
        """
        Validate that drive ratings are valid (8, 7, 6, 5, 4, one of each).
        
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        valid_drives = ["duty", "faith", "justice", "power", "truth"]
        required_ratings = [8, 7, 6, 5, 4]
        
        if "drives" not in self.db.stats:
            return (False, "Drives not initialized")
        
        current_ratings = []
        for drive_name in valid_drives:
            drive = self.db.stats["drives"].get(drive_name, {})
            if isinstance(drive, dict):
                rating = drive.get("rating", 0)
            else:
                rating = 0
            
            if rating > 0:
                current_ratings.append(rating)
        
        # Check if we have exactly the required ratings
        if sorted(current_ratings) != sorted(required_ratings):
            return (False, f"Drive ratings must be exactly {required_ratings}. Current: {sorted(current_ratings)}")
        
        return (True, "Drive ratings are valid")
        
    def take_stress(self, amount):
        """
        Apply stress (damage) to the character.
        
        Args:
            amount (int): Amount of stress to take
            
        Returns:
            tuple: (new_stress, is_incapacitated)
        """
        self.db.stress = min(self.db.stress + amount, self.db.max_stress)
        is_incapacitated = self.db.stress >= self.db.max_stress
        return (self.db.stress, is_incapacitated)
        
    def heal_stress(self, amount):
        """
        Heal stress.
        
        Args:
            amount (int): Amount of stress to heal
            
        Returns:
            int: New stress value
        """
        self.db.stress = max(0, self.db.stress - amount)
        return self.db.stress
        
    def spend_determination(self, amount=1):
        """
        Spend determination points.
        
        Args:
            amount (int): Amount to spend (default 1)
            
        Returns:
            bool: True if successful, False if not enough points
        """
        if self.db.determination >= amount:
            self.db.determination -= amount
            return True
        return False
        
    def gain_determination(self, amount=1):
        """
        Gain determination points.
        
        Args:
            amount (int): Amount to gain (default 1)
        """
        # Cap at 3 maximum
        self.db.determination = min(3, self.db.determination + amount)
    
    def cross_out_drive(self, drive_name):
        """
        Cross out a drive (challenged drive that can't be used until recovered).
        
        Args:
            drive_name (str): Name of the drive to cross out
        """
        if not hasattr(self.db, 'crossed_out_drives'):
            self.db.crossed_out_drives = []
        if drive_name.lower() not in [d.lower() for d in self.db.crossed_out_drives]:
            self.db.crossed_out_drives.append(drive_name.lower())
    
    def recover_drive(self, drive_name):
        """
        Recover a crossed out drive.
        
        Args:
            drive_name (str): Name of the drive to recover
        """
        if not hasattr(self.db, 'crossed_out_drives'):
            self.db.crossed_out_drives = []
        self.db.crossed_out_drives = [d for d in self.db.crossed_out_drives if d.lower() != drive_name.lower()]
    
    def is_drive_crossed_out(self, drive_name):
        """
        Check if a drive is crossed out.
        
        Args:
            drive_name (str): Name of the drive to check
            
        Returns:
            bool: True if crossed out, False otherwise
        """
        if not hasattr(self.db, 'crossed_out_drives'):
            self.db.crossed_out_drives = []
        return drive_name.lower() in [d.lower() for d in self.db.crossed_out_drives]
        
    def award_experience(self, amount):
        """
        Award experience points.
        
        Args:
            amount (int): Amount of XP to award
        """
        self.db.experience += amount
    
    def _wrap_text(self, text, width, indent=0):
        """
        Wrap text to fit within a given width, with optional indentation.
        
        Args:
            text (str): Text to wrap
            width (int): Maximum width of each line
            indent (int): Number of spaces to indent wrapped lines
            
        Returns:
            list: List of wrapped lines
        """
        if not text:
            return []
        
        import re
        lines = []
        indent_str = " " * indent
        wrap_width = width - indent
        
        # Remove ANSI codes for length calculation
        ansi_pattern = re.compile(r'\x1b\[[0-9;]*m|\|n|\|c|\|w|\|y|\|r|\|g|\|m|\|b')
        
        # Simple word wrap
        words = text.split()
        current_line = indent_str
        
        for word in words:
            # Check if adding this word would exceed the line width
            test_line = current_line + (" " if current_line.strip() else "") + word
            # Count visible chars by removing ANSI codes
            visible_chars = len(ansi_pattern.sub('', test_line))
            
            if visible_chars > wrap_width and current_line.strip():
                # Start a new line
                lines.append(current_line.rstrip())
                current_line = indent_str + word
            else:
                # Add to current line
                if current_line.strip():
                    current_line += " " + word
                else:
                    current_line = indent_str + word
        
        if current_line.strip():
            lines.append(current_line.rstrip())
        
        return lines
        
    def get_sheet_display(self):
        """
        Get a formatted character sheet for display.
        Compact format that fits on one screen (80 chars wide).
        
        Returns:
            str: Formatted character sheet
        """
        lines = []
        lines.append("|w" + "=" * 80 + "|n")
        lines.append("|w" + f" {self.name}".center(80) + "|n")
        lines.append("|w" + "=" * 80 + "|n")
        
        # BACKGROUND - Compact single line format
        # Handle house being either a string or a House object
        house = self.db.house
        if house:
            # If it's a House object, get its key (name)
            if hasattr(house, 'key'):
                house = house.key
            else:
                house = str(house)
        else:
            house = "None"
        
        # Get role using the new method (checks both house and organization roles)
        role = self.get_role() or "None"
        faction = self.db.faction or "None"
        caste = self.db.caste or "None"
        
        # Show archetype if available
        archetype_info = ""
        archetype = self.db.chargen_archetype
        if archetype:
            archetype_trait = archetype.get('trait', '')
            if archetype_trait:
                archetype_info = f" |wArchetype:|n {archetype_trait}"
        
        # Character Information Section
        lines.append(f"|wHouse:|n {house:<12} |wRole:|n {role:<12} |wFaction:|n {faction}")
        
        # Second line: Caste, Archetype, and Playstyle Mode
        info_line = ""
        if caste != "None":
            info_line += f"|wCaste:|n {caste:<12} "
        if archetype_info:
            info_line += archetype_info
        # Add playstyle mode
        playstyle = self.get_playstyle_mode()
        playstyle_display = "|cArchitect|n" if playstyle == "architect" else "|mAgent|n"
        info_line += f" |wPlaystyle:|n {playstyle_display}"
        if info_line:
            lines.append(info_line.strip())
        
        # Show reputation trait and ambition if set (Step 8 finishing touches)
        bio_info = []
        if self.db.reputation_trait:
            bio_info.append(f"|wTrait:|n {self.db.reputation_trait}")
        if self.db.ambition:
            bio_info.append(f"|wAmbition:|n {self.db.ambition}")
        if bio_info:
            lines.append("|w" + "-" * 80 + "|n")
            lines.append("  ".join(bio_info))
        
        # Show personality, appearance, and relationships if set (compact format)
        personal_info = []
        if self.db.personality_traits:
            # Truncate if too long for single line
            personality = self.db.personality_traits
            if len(personality) > 60:
                personality = personality[:57] + "..."
            personal_info.append(f"|wPersonality:|n {personality}")
        if self.db.appearance:
            appearance = self.db.appearance
            if len(appearance) > 60:
                appearance = appearance[:57] + "..."
            personal_info.append(f"|wAppearance:|n {appearance}")
        if self.db.relationships:
            relationships = self.db.relationships
            if len(relationships) > 60:
                relationships = relationships[:57] + "..."
            personal_info.append(f"|wRelationships:|n {relationships}")
        
        if personal_info:
            lines.append("|w" + "-" * 80 + "|n")
            for info in personal_info:
                lines.append(info)
        
        # DRIVES - Show ratings and statements (same format as skills)
        # Access drives exactly like skills are accessed
        drives = self.db.stats.get("drives", {})
        drive_names = ["duty", "faith", "justice", "power", "truth"]
        
        # Check if we have any drives with ratings > 0
        # _SaverDict supports dict-like operations, so we can use it directly
        has_drives = False
        for drive_name in drive_names:
            # Use .get() which works on _SaverDict
            drive = drives.get(drive_name) if drives else None
            if not drive:
                continue
            
            # Handle dict format (new format) - _SaverDict supports .get()
            if hasattr(drive, 'get'):
                rating = drive.get("rating", 0)
                if rating > 0:
                    has_drives = True
                    break
            elif isinstance(drive, str) and drive:
                has_drives = True
                break
        
        if has_drives:
            lines.append("|w" + "-" * 80 + "|n")
            for drive_name in drive_names:
                # Use .get() which works on _SaverDict
                drive = drives.get(drive_name) if drives else None
                if not drive:
                    continue
                
                # Handle legacy format (string instead of dict)
                if isinstance(drive, str):
                    if drive:
                        # Legacy format: show as statement without rating
                        lines.append(f"|c{drive_name.capitalize():<12}|n")
                        # Wrap statement at 80 chars with 4-space indentation
                        wrapped = self._wrap_text(drive, 80, 4)
                        for line in wrapped:
                            lines.append(line)
                    continue
                
                # Handle dict format (new format) - _SaverDict supports .get()
                if hasattr(drive, 'get'):
                    # Convert _SaverDict to regular dict to ensure proper access
                    try:
                        drive_dict = dict(drive) if drive else {}
                    except (TypeError, ValueError):
                        drive_dict = {}
                    
                    rating = drive_dict.get("rating", 0) if isinstance(drive_dict, dict) else drive.get("rating", 0)
                    statement = drive_dict.get("statement", "") if isinstance(drive_dict, dict) else drive.get("statement", "")
                    
                    # Ensure statement is a string
                    if statement is None:
                        statement = ""
                    else:
                        statement = str(statement).strip()
                    
                    if rating > 0:
                        # Format like skills: name and rating on first line
                        lines.append(f"|c{drive_name.capitalize():<12}|n {rating}")
                        
                        # Show statement if it exists and is not empty
                        if statement:
                            # Wrap statement at 80 chars with 4-space indentation
                            wrapped = self._wrap_text(statement, 80, 4)
                            for line in wrapped:
                                lines.append(line)
        
        # SKILLS & FOCUSES - Two column layout
        lines.append("|w" + "-" * 80 + "|n")
        skills = self.db.stats.get("skills", {})
        focuses = self.db.stats.get("focuses", [])
        
        # Categorize focuses by skill (using DUNE_FOCUSES mapping)
        from commands.dune.CmdSheet import DUNE_FOCUSES
        
        skill_focus_map = {
            "battle": [],
            "communicate": [],
            "discipline": [],
            "move": [],
            "understand": []
        }
        
        # Map each focus to its skill
        for focus in focuses:
            focus_lower = focus.lower()
            mapped = False
            
            for skill_name, valid_focuses in DUNE_FOCUSES.items():
                for valid_focus in valid_focuses:
                    # Check if this focus matches
                    if "/" in focus_lower:
                        base_focus = focus_lower.split("/")[0].strip()
                        if base_focus == valid_focus.lower():
                            skill_focus_map[skill_name].append(focus)
                            mapped = True
                            break
                    elif focus_lower == valid_focus.lower():
                        skill_focus_map[skill_name].append(focus)
                        mapped = True
                        break
                if mapped:
                    break
        
        # Display skills in compact format
        skill_names = ["battle", "communicate", "discipline", "move", "understand"]
        
        for skill in skill_names:
            skill_val = skills.get(skill, 0)
            skill_focuses = skill_focus_map[skill]
            
            # Skill name and value on first line
            lines.append(f"|c{skill.capitalize():<12}|n {skill_val}")
            
            if skill_focuses:
                # Show all focuses, wrapped at 80 chars with 4-space indentation
                focus_text = ", ".join(skill_focuses)
                wrapped = self._wrap_text(focus_text, 80, 4)
                for line in wrapped:
                    lines.append(line)
        
        # TALENTS - Compact list (Assets are shown in inventory, not on sheet)
        talents = self.db.stats.get("talents", [])
        if not talents:
            talents = self.db.stats.get("traits", [])
        
        if talents:
            lines.append("|w" + "-" * 80 + "|n")
            # Show talents in comma-separated format
            talent_text = ", ".join(talents)
            if len(talent_text) > 70:
                # Wrap if needed
                lines.append("|yTalents:|n")
                for talent in talents:
                    lines.append(f"  {talent}")
            else:
                lines.append(f"|yTalents:|n {talent_text}")
        
        # RESOURCES - Single line
        lines.append("|w" + "-" * 80 + "|n")
        crossed_out = getattr(self.db, 'crossed_out_drives', [])
        det_display = f"{self.db.determination}/3"
        if crossed_out:
            det_display += f" |r(Crossed out: {', '.join([d.title() for d in crossed_out])})|n"
        lines.append(f"|wStress:|n {self.db.stress}/{self.db.max_stress}  "
                    f"|wDetermination:|n {det_display}  "
                    f"|wXP:|n {self.db.experience}")
        
        # COMPLICATIONS - Show active complications
        complications = self.db.complications if hasattr(self.db, 'complications') else []
        if complications:
            lines.append("|w" + "-" * 80 + "|n")
            lines.append("|rComplications:|n")
            for comp in complications:
                skill = comp.get("skill", "unknown").title()
                name = comp.get("name", "Unknown")
                lines.append(f"  |r{name}|n ({skill})")
        
        lines.append("|w" + "=" * 80 + "|n")
        
        return "\n".join(lines)
    
    def get_languages(self):
        """
        Get the list of languages this character knows.
        
        Returns:
            list: List of language names the character knows
        """
        if not hasattr(self.db, 'languages') or not self.db.languages:
            # Default to The Truth if no languages set
            return ["The Truth"]
        return self.db.languages if isinstance(self.db.languages, list) else [self.db.languages]
    
    def get_speaking_language(self):
        """
        Get the character's currently set speaking language.
        
        Returns:
            str or None: The current speaking language, or None if not set
        """
        return getattr(self.db, 'speaking_language', None)
    
    def prepare_say(self, speech, viewer=None, skip_english=False, language_only=False):
        """
        Prepare speech messages with language handling.
        
        Handles language-tagged speech (starting with ~) and formats messages
        for different viewers based on whether they understand the language.
        
        Args:
            speech (str): The speech text (may start with ~ for language tagging)
            viewer (Character, optional): The character viewing the message
            skip_english (bool): If True, don't default to English
            language_only (bool): If True, only process language tags, don't format full say messages
        
        Returns:
            tuple: (msg_self, msg_understand, msg_not_understand, language)
                - msg_self: Message for the speaker
                - msg_understand: Message for those who understand the language
                - msg_not_understand: Message for those who don't understand
                - language: The language being spoken (or None for default/English)
        """
        # Check if speech starts with ~ (language tag)
        is_language_tagged = speech.startswith('~')
        language = None
        
        if is_language_tagged:
            # Remove the ~ prefix
            speech = speech[1:].lstrip()
            # Get the speaking language
            language = self.get_speaking_language()
            if not language:
                # Default to The Truth if no language set
                language = "The Truth"
        
        # If skip_english and no language, treat as no language
        if skip_english and not language:
            language = None
        
        # Format the speaker's name
        # Use get_display_name if available, otherwise fall back to name
        if viewer and viewer != self:
            try:
                speaker_name = self.get_display_name(viewer)
            except AttributeError:
                speaker_name = self.name
        else:
            speaker_name = self.name
        
        # Build messages
        if language_only:
            # For language_only mode, just return the speech text
            # The caller will handle formatting
            if language:
                return (speech, speech, f"[foreign speech in {language}]", language)
            else:
                return (speech, speech, speech, None)
        
        # Standard say format: "Speaker says, \"message\""
        if language:
            # Language-tagged speech
            msg_self = f'You say in {language}, "{speech}"'
            msg_understand = f'{speaker_name} says in {language}, "{speech}"'
            msg_not_understand = f'{speaker_name} says something in {language}.'
        else:
            # Default/English speech
            msg_self = f'You say, "{speech}"'
            msg_understand = f'{speaker_name} says, "{speech}"'
            msg_not_understand = f'{speaker_name} says, "{speech}"'  # Same for default language
        
        return (msg_self, msg_understand, msg_not_understand, language)
    
    def record_scene_activity(self):
        """
        Record scene activity for tracking purposes.
        
        This can be used to track when characters are active in scenes
        for logging, statistics, or other purposes.
        """
        # Basic implementation - can be extended later
        # For now, this is a no-op to prevent errors
        pass