"""
NPCs (Non-Player Characters)

NPCs are similar to Characters but are controlled by staff rather than players.
They use the same 2d20 system but may have simplified stats or special traits.

This implementation uses the Modiphus 2d20 system for Dune.
"""

from evennia.objects.objects import DefaultCharacter
from .objects import ObjectParent


class NPC(ObjectParent, DefaultCharacter):
    """
    NPC class for the Dune MUSH using Modiphus 2d20 system.
    
    NPCs use the same stat system as player characters but may have:
    - Simplified attribute/skill blocks for minor NPCs
    - Special traits for significant NPCs
    - Threat generation capabilities for antagonists
    
    The npc_tier attribute determines the NPC's importance:
    - "minor": Simple NPCs with basic stats (guards, servants, etc.)
    - "notable": NPCs with moderate abilities (officers, advisors)
    - "major": Significant NPCs with full character sheets (nobles, leaders)
    """

    def at_object_creation(self):
        """
        Called once, when this NPC is first created.
        Set up default NPC stats for 2d20 system.
        """
        super().at_object_creation()
        
        # NPC classification
        self.db.npc_tier = "minor"  # minor, notable, major
        self.db.npc_type = "generic"  # guard, noble, mentat, soldier, etc.
        
        # Initialize stats dictionary (same structure as player characters)
        self.db.stats = {
            # Core Attributes (range typically 6-12 for humans)
            "attributes": {
                "control": 7,
                "dexterity": 7,
                "fitness": 7,
                "insight": 7,
                "presence": 7,
                "reason": 7
            },
            
            # Skills (range typically 0-5)
            "skills": {
                "battle": 0,
                "communicate": 0,
                "discipline": 0,
                "move": 0,
                "understand": 0
            },
            
            # Focuses (specializations within skills)
            "focuses": [],
            
            # Traits (special abilities)
            "traits": [],
            
            # Assets (resources and special items)
            "assets": [],
            
            # Drives (not typically used for minor NPCs)
            "drives": {}
        }
        
        # Resource tracking
        self.db.stress = 0
        self.db.max_stress = self.calculate_max_stress()
        
        # NPCs don't typically have determination (GMs use Threat instead)
        # But major NPCs might have it for special circumstances
        self.db.determination = 0
        
        # Combat and behavior flags
        self.db.is_hostile = False
        self.db.is_aggressive = False
        self.db.combat_target = None
        
        # Description fields
        self.db.shortdesc = ""
        self.db.background = ""
        self.db.house = ""
        self.db.faction = ""
        
        # AI/Behavior settings (for future automation)
        self.db.ai_enabled = False
        self.db.ai_behavior = "passive"  # passive, defensive, aggressive, guard
        self.db.patrol_route = []
        
    def calculate_max_stress(self):
        """
        Calculate maximum stress based on Fitness + Discipline skill.
        Standard 2d20 calculation.
        """
        fitness = self.db.stats.get("attributes", {}).get("fitness", 7)
        discipline = self.db.stats.get("skills", {}).get("discipline", 0)
        return fitness + discipline
        
    def set_as_minor_npc(self, npc_type="generic"):
        """
        Configure as a minor NPC with simplified stats.
        Minor NPCs typically have attributes around 6-8 and skills 0-2.
        
        Args:
            npc_type (str): Type of NPC (guard, servant, etc.)
        """
        self.db.npc_tier = "minor"
        self.db.npc_type = npc_type
        
        # Simplified stats for minor NPCs
        if npc_type == "guard":
            self.db.stats["attributes"]["fitness"] = 8
            self.db.stats["attributes"]["dexterity"] = 7
            self.db.stats["skills"]["battle"] = 2
            self.db.stats["skills"]["discipline"] = 1
            self.db.stats["focuses"] = ["Battle: Maula Pistol"]
            self.db.stats["assets"] = ["Maula Pistol", "Light Armor"]
        elif npc_type == "soldier":
            self.db.stats["attributes"]["fitness"] = 9
            self.db.stats["attributes"]["control"] = 7
            self.db.stats["skills"]["battle"] = 3
            self.db.stats["skills"]["discipline"] = 2
            self.db.stats["focuses"] = ["Battle: Lasgun", "Battle: Kindjal"]
            self.db.stats["assets"] = ["Lasgun", "Kindjal", "Combat Armor"]
        elif npc_type == "servant":
            self.db.stats["attributes"]["insight"] = 8
            self.db.stats["skills"]["communicate"] = 1
            self.db.stats["skills"]["understand"] = 1
        
        self.db.max_stress = self.calculate_max_stress()
        
    def set_as_notable_npc(self, npc_type="generic"):
        """
        Configure as a notable NPC with moderate abilities.
        Notable NPCs have attributes around 8-10 and skills 2-4.
        
        Args:
            npc_type (str): Type of NPC (officer, advisor, etc.)
        """
        self.db.npc_tier = "notable"
        self.db.npc_type = npc_type
        
        if npc_type == "officer":
            self.db.stats["attributes"]["presence"] = 9
            self.db.stats["attributes"]["fitness"] = 8
            self.db.stats["skills"]["battle"] = 4
            self.db.stats["skills"]["communicate"] = 3
            self.db.stats["skills"]["discipline"] = 3
            self.db.stats["focuses"] = [
                "Battle: Tactics",
                "Battle: Lasgun",
                "Communicate: Leadership"
            ]
            self.db.stats["assets"] = ["Personal Shield", "Lasgun", "Officer's Insignia"]
        elif npc_type == "advisor":
            self.db.stats["attributes"]["reason"] = 10
            self.db.stats["attributes"]["insight"] = 9
            self.db.stats["skills"]["understand"] = 4
            self.db.stats["skills"]["communicate"] = 3
            self.db.stats["focuses"] = [
                "Understand: Politics",
                "Communicate: Persuasion"
            ]
        
        self.db.max_stress = self.calculate_max_stress()
        
    def set_as_major_npc(self):
        """
        Configure as a major NPC with full character abilities.
        Major NPCs should be customized manually like player characters.
        """
        self.db.npc_tier = "major"
        # Major NPCs get determination like players
        self.db.determination = 3
        
    # Include all the same helper methods as Character class
    def get_attribute(self, attr_name):
        """Get an attribute value by name."""
        return self.db.stats.get("attributes", {}).get(attr_name.lower(), 7)
        
    def set_attribute(self, attr_name, value):
        """Set an attribute value."""
        if "attributes" not in self.db.stats:
            self.db.stats["attributes"] = {}
        self.db.stats["attributes"][attr_name.lower()] = value
        if attr_name.lower() == "fitness":
            self.db.max_stress = self.calculate_max_stress()
            
    def get_skill(self, skill_name):
        """Get a skill value by name."""
        return self.db.stats.get("skills", {}).get(skill_name.lower(), 0)
        
    def set_skill(self, skill_name, value):
        """Set a skill value."""
        if "skills" not in self.db.stats:
            self.db.stats["skills"] = {}
        self.db.stats["skills"][skill_name.lower()] = value
        if skill_name.lower() == "discipline":
            self.db.max_stress = self.calculate_max_stress()
            
    def add_focus(self, focus):
        """Add a focus (skill specialization)."""
        if "focuses" not in self.db.stats:
            self.db.stats["focuses"] = []
        if focus not in self.db.stats["focuses"]:
            self.db.stats["focuses"].append(focus)
            
    def remove_focus(self, focus):
        """Remove a focus."""
        if focus in self.db.stats.get("focuses", []):
            self.db.stats["focuses"].remove(focus)
            return True
        return False
        
    def add_trait(self, trait):
        """Add a trait (special ability)."""
        if "traits" not in self.db.stats:
            self.db.stats["traits"] = []
        if trait not in self.db.stats["traits"]:
            self.db.stats["traits"].append(trait)
            
    def remove_trait(self, trait):
        """Remove a trait."""
        if trait in self.db.stats.get("traits", []):
            self.db.stats["traits"].remove(trait)
            return True
        return False
        
    def add_asset(self, asset):
        """Add an asset (resource/item)."""
        if "assets" not in self.db.stats:
            self.db.stats["assets"] = []
        if asset not in self.db.stats["assets"]:
            self.db.stats["assets"].append(asset)
            
    def remove_asset(self, asset):
        """Remove an asset."""
        if asset in self.db.stats.get("assets", []):
            self.db.stats["assets"].remove(asset)
            return True
        return False
        
    def take_stress(self, amount):
        """Apply stress (damage) to the NPC."""
        self.db.stress = min(self.db.stress + amount, self.db.max_stress)
        is_incapacitated = self.db.stress >= self.db.max_stress
        return (self.db.stress, is_incapacitated)
        
    def heal_stress(self, amount):
        """Heal stress."""
        self.db.stress = max(0, self.db.stress - amount)
        return self.db.stress
        
    def get_sheet_display(self):
        """
        Get a formatted NPC stat block for display.
        
        Returns:
            str: Formatted NPC sheet
        """
        lines = []
        lines.append("|w" + "=" * 78 + "|n")
        lines.append("|w" + f" NPC: {self.name} ({self.db.npc_tier.upper()} - {self.db.npc_type})".center(78) + "|n")
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
        
        # Combat Status
        lines.append(f"\n|y{'STATUS':-^78}|n")
        lines.append(f"  Stress:        {self.db.stress}/{self.db.max_stress}")
        if self.db.npc_tier == "major":
            lines.append(f"  Determination: {self.db.determination}")
        lines.append(f"  Hostile:       {'Yes' if self.db.is_hostile else 'No'}")
        lines.append(f"  Aggressive:    {'Yes' if self.db.is_aggressive else 'No'}")
        
        lines.append("|w" + "=" * 78 + "|n")
        
        return "\n".join(lines)

