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


class Character(ObjectParent, DefaultCharacter):
    """
    Character class for the Dune MUSH using Modiphus 2d20 system.
    
    Attributes are stored in self.db.stats dictionary with the following structure:
    
    - attributes: Core attributes (Control, Dexterity, Fitness, Insight, Presence, Reason)
    - skills: Skills with ratings (Battle, Communicate, Discipline, Move, Understand, etc.)
    - focuses: List of skill focuses/specializations
    - traits: Special abilities and characteristics
    - assets: Resources, items, and special possessions
    - stress: Current stress level
    - determination: Current determination points
    - experience: Experience points
    - drives: Character motivations/drives
    
    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.
    """

    def at_object_creation(self):
        """
        Called once, when this object is first created.
        Set up default character stats for 2d20 system.
        """
        super().at_object_creation()
        
        # Initialize stats dictionary
        self.db.stats = {
            # Core Attributes (range typically 6-12 for humans)
            "attributes": {
                "control": 7,      # Mental discipline and willpower
                "dexterity": 7,    # Physical coordination and agility
                "fitness": 7,      # Physical health and endurance
                "insight": 7,      # Awareness and intuition
                "presence": 7,     # Force of personality and leadership
                "reason": 7        # Intelligence and logic
            },
            
            # Skills (range typically 0-5)
            "skills": {
                "battle": 0,       # Combat and warfare
                "communicate": 0,  # Social interaction and persuasion
                "discipline": 0,   # Mental fortitude and focus
                "move": 0,         # Physical movement and athletics
                "understand": 0    # Knowledge and comprehension
            },
            
            # Focuses (specializations within skills)
            "focuses": [],  # Example: ["Battle: Knife Fighting", "Communicate: Persuasion"]
            
            # Traits (special abilities)
            "traits": [],  # Example: ["Mentat Training", "Bene Gesserit Conditioning"]
            
            # Assets (resources and special items)
            "assets": [],  # Example: ["Personal Shield", "Crysknife"]
            
            # Drives (character motivations)
            "drives": {
                "duty": "",       # Obligations and responsibilities
                "faith": "",      # Beliefs and principles
                "justice": "",    # Sense of right and wrong
                "power": "",      # Ambitions and goals
                "truth": ""       # Quest for knowledge
            }
        }
        
        # Resource tracking
        self.db.stress = 0              # Current stress (health damage)
        self.db.determination = 3       # Determination points (player resource)
        self.db.experience = 0          # Experience points
        
        # Derived stats
        self.db.max_stress = self.calculate_max_stress()
        
        # Character description fields
        self.db.shortdesc = ""          # Short description for room displays
        self.db.background = ""         # Character background/history
        self.db.house = ""              # Great House affiliation
        self.db.faction = ""            # Faction/organization membership
        
    def calculate_max_stress(self):
        """
        Calculate maximum stress based on Fitness + Discipline skill.
        Standard 2d20 calculation.
        """
        fitness = self.db.stats.get("attributes", {}).get("fitness", 7)
        discipline = self.db.stats.get("skills", {}).get("discipline", 0)
        return fitness + discipline
        
    def get_attribute(self, attr_name):
        """
        Get an attribute value by name.
        
        Args:
            attr_name (str): Name of the attribute (e.g., "control", "fitness")
            
        Returns:
            int: The attribute value, or 7 (default) if not found
        """
        return self.db.stats.get("attributes", {}).get(attr_name.lower(), 7)
        
    def set_attribute(self, attr_name, value):
        """
        Set an attribute value.
        
        Args:
            attr_name (str): Name of the attribute
            value (int): New value (typically 6-12)
        """
        if "attributes" not in self.db.stats:
            self.db.stats["attributes"] = {}
        self.db.stats["attributes"][attr_name.lower()] = value
        
        # Update max stress if fitness changes
        if attr_name.lower() == "fitness":
            self.db.max_stress = self.calculate_max_stress()
            
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
        
    def add_trait(self, trait):
        """
        Add a trait (special ability).
        
        Args:
            trait (str): Trait name
        """
        if "traits" not in self.db.stats:
            self.db.stats["traits"] = []
        if trait not in self.db.stats["traits"]:
            self.db.stats["traits"].append(trait)
            
    def remove_trait(self, trait):
        """
        Remove a trait.
        
        Args:
            trait (str): Trait to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if trait in self.db.stats.get("traits", []):
            self.db.stats["traits"].remove(trait)
            return True
        return False
        
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
        Remove an asset.
        
        Args:
            asset (str): Asset to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if asset in self.db.stats.get("assets", []):
            self.db.stats["assets"].remove(asset)
            return True
        return False
        
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
        self.db.determination += amount
        
    def award_experience(self, amount):
        """
        Award experience points.
        
        Args:
            amount (int): Amount of XP to award
        """
        self.db.experience += amount
        
    def get_sheet_display(self):
        """
        Get a formatted character sheet for display.
        
        Returns:
            str: Formatted character sheet
        """
        lines = []
        lines.append("|w" + "=" * 78 + "|n")
        lines.append("|w" + f" CHARACTER SHEET: {self.name}".center(78) + "|n")
        lines.append("|w" + "=" * 78 + "|n")
        
        # Basic Info
        lines.append(f"\n|cHouse:|n {self.db.house or 'None'}")
        lines.append(f"|cFaction:|n {self.db.faction or 'None'}")
        
        # Attributes
        lines.append(f"\n|y{'ATTRIBUTES':-^78}|n")
        attrs = self.db.stats.get("attributes", {})
        lines.append(f"  Control:   {attrs.get('control', 7):<2}  Dexterity: {attrs.get('dexterity', 7):<2}  Fitness:  {attrs.get('fitness', 7):<2}")
        lines.append(f"  Insight:   {attrs.get('insight', 7):<2}  Presence:  {attrs.get('presence', 7):<2}  Reason:   {attrs.get('reason', 7):<2}")
        
        # Skills
        lines.append(f"\n|y{'SKILLS':-^78}|n")
        skills = self.db.stats.get("skills", {})
        lines.append(f"  Battle:      {skills.get('battle', 0)}  Communicate: {skills.get('communicate', 0)}  Discipline: {skills.get('discipline', 0)}")
        lines.append(f"  Move:        {skills.get('move', 0)}  Understand:  {skills.get('understand', 0)}")
        
        # Focuses
        focuses = self.db.stats.get("focuses", [])
        if focuses:
            lines.append(f"\n|y{'FOCUSES':-^78}|n")
            for focus in focuses:
                lines.append(f"  • {focus}")
        
        # Traits
        traits = self.db.stats.get("traits", [])
        if traits:
            lines.append(f"\n|y{'TRAITS':-^78}|n")
            for trait in traits:
                lines.append(f"  • {trait}")
        
        # Assets
        assets = self.db.stats.get("assets", [])
        if assets:
            lines.append(f"\n|y{'ASSETS':-^78}|n")
            for asset in assets:
                lines.append(f"  • {asset}")
        
        # Resources
        lines.append(f"\n|y{'RESOURCES':-^78}|n")
        lines.append(f"  Stress:        {self.db.stress}/{self.db.max_stress}")
        lines.append(f"  Determination: {self.db.determination}")
        lines.append(f"  Experience:    {self.db.experience}")
        
        lines.append("|w" + "=" * 78 + "|n")
        
        return "\n".join(lines)
