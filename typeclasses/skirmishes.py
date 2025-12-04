"""
Skirmish System for Dune 2d20

Implements skirmish combat with environment-based zones, character positioning, and multi-combatant resolution.
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent


class Skirmish(ObjectParent, DefaultObject):
    """
    A Skirmish represents combat involving multiple combatants in an environment.
    
    Zones represent areas of the environment (not personal zones).
    Multiple characters can be in the same zone.
    Characters move between zones, and assets move with them.
    """
    
    def at_object_creation(self):
        """Initialize skirmish state"""
        super().at_object_creation()
        
        # Combatants (list of characters)
        self.db.combatants = []  # List of character objects
        
        # Current turn order
        self.db.turn_order = []  # List of characters in turn order
        self.db.current_turn_index = 0  # Index of current turn
        
        # Environment zones
        # Format: {zone_name: {"characters": [character_ids], "traits": [trait_names], "description": str}}
        self.db.zones = {}
        
        # Character positions
        # Format: {character_id: zone_name}
        self.db.character_positions = {}
        
        # Assets in the skirmish
        # Format: {asset_id: {"owner": character, "zone": zone_name, "type": "weapon|shield|armor|intangible"}}
        self.db.assets = {}
        
        # Intangible assets (positioning, cover, etc.)
        # Format: {asset_name: {"owner": character, "zone": zone_name, "description": str}}
        self.db.intangible_assets = {}
        
        # Extended tasks for non-minor characters
        # Format: {character_id: {"requirement": int, "points": int, "attackers": [character_ids]}}
        self.db.extended_tasks = {}
        
        # Skirmish state
        self.db.status = "active"  # active, concluded
        self.db.winners = []  # List of winning characters/teams
        self.db.defeated = []  # List of defeated characters
        
        # Room where skirmish takes place
        self.db.location = None
    
    def add_combatant(self, character, starting_zone=None):
        """
        Add a combatant to the skirmish.
        
        Args:
            character: Character object to add
            starting_zone: Zone name to start in (defaults to first zone)
            
        Returns:
            bool: True if added successfully
        """
        if character in self.db.combatants:
            return False
        
        self.db.combatants.append(character)
        
        # Initialize character position
        if not self.db.character_positions:
            self.db.character_positions = {}
        
        # Place in starting zone
        if starting_zone and starting_zone in self.db.zones:
            zone = starting_zone
        elif self.db.zones:
            # Default to first zone
            zone = list(self.db.zones.keys())[0]
        else:
            zone = None
        
        if zone:
            self.db.character_positions[character.id] = zone
            if character.id not in self.db.zones[zone]["characters"]:
                self.db.zones[zone]["characters"].append(character.id)
        
        return True
    
    def add_zone(self, zone_name, description="", traits=None):
        """
        Add a zone to the skirmish environment.
        
        Args:
            zone_name: Name of the zone
            description: Description of the zone
            traits: List of trait names (e.g., ["Dark", "Cover"])
            
        Returns:
            bool: True if added
        """
        if not self.db.zones:
            self.db.zones = {}
        
        self.db.zones[zone_name] = {
            "characters": [],
            "traits": traits or [],
            "description": description
        }
        return True
    
    def get_character_zone(self, character):
        """Get the zone a character is in"""
        if not character:
            return None
        return self.db.character_positions.get(character.id)
    
    def get_characters_in_zone(self, zone_name):
        """
        Get all characters in a specific zone.
        
        Args:
            zone_name: Name of the zone
            
        Returns:
            list: List of character objects
        """
        if zone_name not in self.db.zones:
            return []
        
        character_ids = self.db.zones[zone_name]["characters"]
        characters = []
        for char_id in character_ids:
            for combatant in self.db.combatants:
                if combatant.id == char_id:
                    characters.append(combatant)
                    break
        return characters
    
    def get_adjacent_zones(self, zone_name):
        """
        Get zones adjacent to a given zone.
        
        Args:
            zone_name: Name of the zone
            
        Returns:
            list: List of adjacent zone names
        """
        # For now, all zones are considered adjacent
        # In a full implementation, this could track actual adjacency
        adjacent = []
        for zone in self.db.zones.keys():
            if zone != zone_name:
                adjacent.append(zone)
        return adjacent
    
    def move_character(self, character, target_zone, subtle=False, bold=False):
        """
        Move a character to a different zone.
        
        Args:
            character: Character to move
            target_zone: Target zone name
            subtle: If True, subtle movement (may keep initiative)
            bold: If True, bold movement (may affect enemies)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if character not in self.db.combatants:
            return (False, "Character is not in this skirmish.")
        
        current_zone = self.get_character_zone(character)
        if not current_zone:
            return (False, "Character is not positioned in any zone.")
        
        if target_zone not in self.db.zones:
            return (False, f"Zone '{target_zone}' does not exist.")
        
        if current_zone == target_zone:
            return (False, "Character is already in that zone.")
        
        # Check if target is adjacent (normal movement)
        adjacent = self.get_adjacent_zones(current_zone)
        if target_zone not in adjacent:
            # Non-adjacent movement requires Momentum (handled by command)
            pass
        
        # Remove from current zone
        if character.id in self.db.zones[current_zone]["characters"]:
            self.db.zones[current_zone]["characters"].remove(character.id)
        
        # Add to target zone
        self.db.zones[target_zone]["characters"].append(character.id)
        self.db.character_positions[character.id] = target_zone
        
        # Move all assets with the character
        moved_assets = []
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["owner"].id == character.id:
                asset_data["zone"] = target_zone
                moved_assets.append(asset_data["asset"].name)
        
        move_type = "subtly" if subtle else ("boldly" if bold else "")
        if move_type:
            message = f"Moved {move_type} to {target_zone} zone."
        else:
            message = f"Moved to {target_zone} zone."
        
        if moved_assets:
            message += f" (Assets: {', '.join(moved_assets)})"
        
        return (True, message)
    
    def add_asset(self, character, asset, asset_type="weapon"):
        """
        Add an asset to the skirmish.
        Assets are positioned in the same zone as their owner.
        
        Args:
            character: Character who owns the asset
            asset: Asset object
            asset_type: Type of asset ("weapon", "shield", "armor", "intangible")
            
        Returns:
            bool: True if added successfully
        """
        if not character or not asset:
            return False
        
        if character not in self.db.combatants:
            return False
        
        asset_id = asset.id
        character_zone = self.get_character_zone(character)
        
        if not character_zone:
            return False
        
        if not self.db.assets:
            self.db.assets = {}
        
        self.db.assets[asset_id] = {
            "owner": character,
            "zone": character_zone,
            "type": asset_type,
            "asset": asset
        }
        
        return True
    
    def move_asset_to_zone(self, character, asset, target_zone, move_character=False):
        """
        Move a ranged weapon asset to a different zone (for aiming).
        Optionally move the character with it.
        
        Args:
            character: Character who owns the asset
            asset: Asset object (should be ranged weapon)
            target_zone: Target zone to aim at
            move_character: If True, also move character to target zone
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not character or not asset:
            return (False, "Invalid character or asset.")
        
        asset_id = asset.id
        if asset_id not in self.db.assets:
            return (False, f"{asset.name} is not in this skirmish.")
        
        asset_data = self.db.assets[asset_id]
        if asset_data["owner"].id != character.id:
            return (False, f"You don't own {asset.name}.")
        
        # Check if it's a ranged weapon
        keywords = asset.get_keywords()
        keywords_lower = [k.lower() for k in keywords]
        if "ranged weapon" not in keywords_lower and "ranged" not in keywords_lower:
            return (False, "Only ranged weapons can be aimed at different zones.")
        
        if target_zone not in self.db.zones:
            return (False, f"Zone '{target_zone}' does not exist.")
        
        # Move asset
        asset_data["zone"] = target_zone
        
        # Optionally move character
        if move_character:
            return self.move_character(character, target_zone)
        
        return (True, f"Aimed {asset.name} at {target_zone} zone.")
    
    def get_defensive_assets(self, character):
        """
        Get all defensive assets for a character.
        In skirmishes, all defensive assets apply (not zone-specific).
        
        Args:
            character: Character to check
            
        Returns:
            list: List of defensive asset objects
        """
        defensive = []
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["owner"].id == character.id:
                asset_type = asset_data["type"]
                if asset_type in ["shield", "armor"]:
                    defensive.append(asset_data["asset"])
        
        return defensive
    
    def get_attack_difficulty(self, attacker, target, asset, ranged=False):
        """
        Calculate attack difficulty for a skirmish attack.
        
        Args:
            attacker: Attacking character
            target: Target character
            asset: Weapon asset used
            ranged: If True, this is a ranged attack
            
        Returns:
            int: Difficulty modifier
        """
        base_difficulty = 1
        modifiers = 0
        
        # Get target's defensive assets
        defensive_assets = self.get_defensive_assets(target)
        
        for def_asset in defensive_assets:
            keywords = def_asset.get_keywords()
            keywords_lower = [k.lower() for k in keywords]
            
            if "shield" in keywords_lower:
                if ranged:
                    # Check if half-shield
                    if "half-shield" in keywords_lower or "half shield" in keywords_lower:
                        modifiers += 2  # Ranged vs half-shield: +2
                    else:
                        modifiers += 1  # Ranged vs full shield: +1
                else:
                    modifiers += 1  # Melee vs shield: +1
            elif "armor" in keywords_lower:
                # Armor increases difficulty (heavier = more)
                quality = def_asset.get_quality()
                if isinstance(quality, int):
                    modifiers += quality  # Quality represents armor weight/thickness
                else:
                    modifiers += 1  # Default for non-numeric quality
        
        # Check if target is in same zone
        attacker_zone = self.get_character_zone(attacker)
        target_zone = self.get_character_zone(target)
        
        if ranged and attacker_zone != target_zone:
            # Ranged attack to adjacent zone: +1 difficulty
            if target_zone in self.get_adjacent_zones(attacker_zone):
                modifiers += 1
        
        return base_difficulty + modifiers
    
    def set_extended_task(self, target, requirement, attacker=None):
        """
        Set up or add to an extended task for a non-minor character.
        
        Args:
            target: Target character
            requirement: Number of successes needed
            attacker: Attacking character (adds to existing task if present)
            
        Returns:
            dict: Extended task status
        """
        if not self.db.extended_tasks:
            self.db.extended_tasks = {}
        
        target_id = target.id
        
        if target_id not in self.db.extended_tasks:
            self.db.extended_tasks[target_id] = {
                "requirement": requirement,
                "points": 0,
                "attackers": []
            }
        
        task = self.db.extended_tasks[target_id]
        
        # Update requirement if higher
        if requirement > task["requirement"]:
            task["requirement"] = requirement
        
        # Add attacker if provided
        if attacker and attacker.id not in task["attackers"]:
            task["attackers"].append(attacker.id)
        
        return task
    
    def add_extended_task_points(self, target, points):
        """
        Add points to an extended task.
        
        Args:
            target: Target character
            points: Points to add
            
        Returns:
            bool: True if task is complete
        """
        if not self.db.extended_tasks:
            return False
        
        target_id = target.id
        if target_id not in self.db.extended_tasks:
            return False
        
        task = self.db.extended_tasks[target_id]
        task["points"] += points
        
        return task["points"] >= task["requirement"]
    
    def get_extended_task_status(self, target):
        """Get extended task status for a target"""
        if not self.db.extended_tasks:
            return None
        
        target_id = target.id
        if target_id not in self.db.extended_tasks:
            return None
        
        return self.db.extended_tasks[target_id]
    
    def create_intangible_asset(self, character, name, description, zone=None):
        """
        Create an intangible asset (positioning, cover, etc.).
        
        Args:
            character: Character creating the asset
            name: Name of the intangible asset
            description: Description of what it represents
            zone: Zone where it's located (defaults to character's zone)
            
        Returns:
            bool: True if created
        """
        if not self.db.intangible_assets:
            self.db.intangible_assets = {}
        
        if not zone:
            zone = self.get_character_zone(character)
        
        self.db.intangible_assets[name] = {
            "owner": character,
            "zone": zone,
            "description": description
        }
        
        return True
    
    def conclude_skirmish(self, winners=None, defeated=None):
        """
        Conclude the skirmish.
        
        Args:
            winners: List of winning characters
            defeated: List of defeated characters
        """
        self.db.status = "concluded"
        if winners:
            self.db.winners = winners
        if defeated:
            self.db.defeated = defeated
    
    def get_display(self, viewer):
        """
        Get a formatted display of the skirmish state.
        
        Args:
            viewer: Character viewing the skirmish
            
        Returns:
            str: Formatted skirmish display
        """
        lines = []
        lines.append("|w" + "=" * 80 + "|n")
        lines.append("|wSKIRMISH STATUS|n".center(80))
        lines.append("|w" + "=" * 80 + "|n")
        
        # Show zones and characters
        lines.append("|wZones:|n")
        for zone_name, zone_data in self.db.zones.items():
            characters = self.get_characters_in_zone(zone_name)
            char_names = [c.name for c in characters]
            
            lines.append(f"  |y{zone_name}:|n {', '.join(char_names) if char_names else 'Empty'}")
            
            if zone_data.get("traits"):
                lines.append(f"    Traits: {', '.join(zone_data['traits'])}")
            
            if zone_data.get("description"):
                lines.append(f"    {zone_data['description']}")
        
        lines.append("")
        
        # Show viewer's position
        viewer_zone = self.get_character_zone(viewer)
        if viewer_zone:
            lines.append(f"|wYour Position:|n {viewer_zone}")
            
            # Show assets
            viewer_assets = []
            for asset_id, asset_data in self.db.assets.items():
                if asset_data["owner"].id == viewer.id:
                    viewer_assets.append(asset_data["asset"].name)
            
            if viewer_assets:
                lines.append(f"|wYour Assets:|n {', '.join(viewer_assets)}")
        
        lines.append("|w" + "=" * 80 + "|n")
        return "\n".join(lines)

