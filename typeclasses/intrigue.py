"""
Intrigue System for Dune 2d20

Implements intrigue conflicts with social zones representing people and groups,
disposition tracking, and leverage-based influence.
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent


class IntrigueConflict(ObjectParent, DefaultObject):
    """
    An Intrigue Conflict represents social battles of status, wits, words, and secrets.
    
    Zones represent people and groups involved in the intrigue.
    Assets represent leverage (knowledge, rumors, valuables).
    Disposition tracks relationships and affects difficulty.
    """
    
    def at_object_creation(self):
        """Initialize intrigue conflict state"""
        super().at_object_creation()
        
        # Participants
        self.db.participants = []  # List of character objects
        
        # Zones (people and groups)
        # Format: {zone_name: {"type": "person|group", "disposition": "Allied|Friendly|Neutral|Unfriendly|Opposed", "desire": str, "disposition_toward": {character_id: "Allied|Friendly|..."}, "desire_known": [character_ids]}}
        self.db.zones = {}
        
        # Objectives (what each participant is trying to achieve)
        # Format: {character_id: {"objective": str, "zones": [zone_names]}}
        self.db.objectives = {}
        
        # Assets in the conflict
        # Format: {asset_id: {"owner": character, "zone": zone_name, "type": "knowledge|rumor|valuable", "asset": asset_object, "quality": int}}
        self.db.assets = {}
        
        # Intangible assets (rumors, lies, leverage)
        # Format: {asset_name: {"owner": character, "zone": zone_name, "description": str, "type": "knowledge|rumor|valuable", "quality": int, "verified": bool}}
        self.db.intangible_assets = {}
        
        # Extended tasks for discovering desires
        # Format: {target_zone: {character_id: {"requirement": int, "points": int}}}
        self.db.desire_tasks = {}
        
        # Extended tasks for social attacks
        # Format: {target_character_id: {"requirement": int, "points": int, "attackers": [character_ids]}}
        self.db.attack_tasks = {}
        
        # Conflict state
        self.db.status = "active"  # active, concluded
        self.db.winners = []  # List of winning characters
        self.db.defeated = []  # List of defeated characters
        
        # Room where conflict takes place (if applicable)
        self.db.location = None
    
    def add_participant(self, character, objective=""):
        """
        Add a participant to the intrigue conflict.
        
        Args:
            character: Character object to add
            objective: Their objective in this conflict
            
        Returns:
            bool: True if added successfully
        """
        if character in self.db.participants:
            return False
        
        self.db.participants.append(character)
        
        if not self.db.objectives:
            self.db.objectives = {}
        
        if objective:
            self.db.objectives[character.id] = {
                "objective": objective,
                "zones": []
            }
        
        return True
    
    def add_zone(self, zone_name, zone_type="person", disposition="Neutral", desire=""):
        """
        Add a zone (person or group) to the intrigue conflict.
        
        Args:
            zone_name: Name of the zone (person or group)
            zone_type: Type ("person" or "group")
            disposition: Starting disposition toward player characters ("Allied", "Friendly", "Neutral", "Unfriendly", "Opposed")
            desire: What this person/group wants (can be discovered)
            
        Returns:
            bool: True if added
        """
        if not self.db.zones:
            self.db.zones = {}
        
        self.db.zones[zone_name] = {
            "type": zone_type,
            "disposition": disposition,
            "desire": desire,
            "disposition_toward": {},  # Individual dispositions toward specific characters
            "desire_known": []  # Characters who know this zone's desire
        }
        return True
    
    def set_disposition(self, zone_name, character, disposition):
        """
        Set a zone's disposition toward a specific character.
        
        Args:
            zone_name: Name of the zone
            character: Character the disposition is toward
            disposition: "Allied", "Friendly", "Neutral", "Unfriendly", "Opposed"
            
        Returns:
            bool: True if set
        """
        if zone_name not in self.db.zones:
            return False
        
        valid_dispositions = ["Allied", "Friendly", "Neutral", "Unfriendly", "Opposed"]
        if disposition not in valid_dispositions:
            return False
        
        if not self.db.zones[zone_name]["disposition_toward"]:
            self.db.zones[zone_name]["disposition_toward"] = {}
        
        self.db.zones[zone_name]["disposition_toward"][character.id] = disposition
        return True
    
    def get_disposition(self, zone_name, character):
        """
        Get a zone's disposition toward a character.
        
        Args:
            zone_name: Name of the zone
            character: Character to check disposition toward
            
        Returns:
            str: Disposition level
        """
        if zone_name not in self.db.zones:
            return "Neutral"
        
        # Check specific disposition first
        disposition_toward = self.db.zones[zone_name].get("disposition_toward", {})
        if character.id in disposition_toward:
            return disposition_toward[character.id]
        
        # Fall back to general disposition
        return self.db.zones[zone_name].get("disposition", "Neutral")
    
    def get_disposition_modifier(self, zone_name, character):
        """
        Get the difficulty modifier for a zone's disposition.
        
        Args:
            zone_name: Name of the zone
            character: Character attempting to influence
            
        Returns:
            int: Difficulty modifier (-2 to +2)
        """
        disposition = self.get_disposition(zone_name, character)
        
        modifiers = {
            "Allied": -2,
            "Friendly": -1,
            "Neutral": 0,
            "Unfriendly": 1,
            "Opposed": 2
        }
        
        return modifiers.get(disposition, 0)
    
    def get_adjacent_zones(self, character):
        """
        Get zones adjacent to a character (people they can communicate with).
        
        Args:
            character: Character to check
            
        Returns:
            list: List of adjacent zone names
        """
        # In intrigue, adjacent zones are people/groups the character can communicate with
        # For simplicity, all zones are adjacent unless specified otherwise
        # In a full implementation, this could track communication channels
        adjacent = []
        for zone_name in self.db.zones.keys():
            adjacent.append(zone_name)
        return adjacent
    
    def add_asset(self, character, asset, zone_name, asset_type="knowledge"):
        """
        Add an asset to the intrigue conflict.
        
        Args:
            character: Character who owns the asset
            asset: Asset object or intangible asset name
            zone_name: Zone to place asset in
            asset_type: Type ("knowledge", "rumor", "valuable")
            
        Returns:
            bool: True if added successfully
        """
        if zone_name not in self.db.zones:
            return False
        
        if not self.db.assets:
            self.db.assets = {}
        
        # Handle both tangible assets and intangible assets
        if hasattr(asset, 'id'):
            # Tangible asset object
            asset_id = asset.id
            quality = asset.get_quality() if hasattr(asset, 'get_quality') else 0
            asset_obj = asset
        else:
            # Intangible asset (string name)
            asset_id = f"intangible_{asset}"
            if asset in self.db.intangible_assets:
                asset_data = self.db.intangible_assets[asset]
                quality = asset_data.get("quality", 0)
                asset_obj = asset  # Store as string reference
            else:
                return False
        
        self.db.assets[asset_id] = {
            "owner": character,
            "zone": zone_name,
            "type": asset_type,
            "asset": asset_obj,
            "quality": quality
        }
        
        return True
    
    def create_intangible_asset(self, character, name, description, zone_name, asset_type="knowledge", quality=0):
        """
        Create an intangible asset (knowledge, rumor, valuable).
        
        Args:
            character: Character creating the asset
            name: Name of the asset
            description: Description
            zone_name: Zone where it's located
            asset_type: Type ("knowledge", "rumor", "valuable")
            quality: Quality rating (0-5)
            
        Returns:
            bool: True if created
        """
        if not self.db.intangible_assets:
            self.db.intangible_assets = {}
        
        self.db.intangible_assets[name] = {
            "owner": character,
            "zone": zone_name,
            "description": description,
            "type": asset_type,
            "quality": quality,
            "verified": asset_type != "rumor"  # Rumors start unverified
        }
        
        return True
    
    def move_asset(self, character, asset, target_zone, subtle=False, bold=False):
        """
        Move an asset to a different zone (use leverage).
        
        Args:
            character: Character who owns the asset
            asset: Asset object or intangible asset name
            target_zone: Target zone name
            subtle: If True, subtle movement (innuendo, implication)
            bold: If True, bold movement (direct, forceful)
            
        Returns:
            tuple: (success: bool, message: str, difficulty_modifier: int)
        """
        if target_zone not in self.db.zones:
            return (False, f"Zone '{target_zone}' does not exist.", 0)
        
        # Check if target is adjacent (can communicate)
        adjacent = self.get_adjacent_zones(character)
        if target_zone not in adjacent:
            return (False, f"You cannot communicate with {target_zone} directly.", 0)
        
        # Find asset
        asset_id = None
        asset_data = None
        
        if hasattr(asset, 'id'):
            asset_id = asset.id
        else:
            asset_id = f"intangible_{asset}"
        
        if asset_id not in self.db.assets:
            return (False, "Asset is not in this conflict.", 0)
        
        asset_data = self.db.assets[asset_id]
        
        # Check ownership
        if asset_data["owner"].id != character.id:
            return (False, "You don't own this asset.", 0)
        
        # Get disposition modifier
        disposition_mod = self.get_disposition_modifier(target_zone, character)
        
        # Move asset
        asset_data["zone"] = target_zone
        
        move_type = "subtly" if subtle else ("boldly" if bold else "")
        message = f"Moved {asset if isinstance(asset, str) else asset.name} {move_type} to {target_zone} zone."
        
        return (True, message, disposition_mod)
    
    def get_attack_difficulty(self, attacker, target_zone):
        """
        Calculate attack difficulty for intrigue.
        Base difficulty + disposition modifier.
        
        Args:
            attacker: Attacking character
            target_zone: Zone being attacked
            
        Returns:
            int: Difficulty
        """
        base_difficulty = 1
        
        # Get disposition modifier
        disposition_mod = self.get_disposition_modifier(target_zone, attacker)
        
        final_difficulty = base_difficulty + disposition_mod
        return max(1, final_difficulty)  # Minimum 1
    
    def set_desire_task(self, target_zone, character, requirement):
        """
        Set up extended task to discover a zone's desire.
        
        Args:
            target_zone: Zone whose desire is being discovered
            character: Character attempting to discover
            requirement: Requirement (target's Discipline skill)
            
        Returns:
            dict: Task status
        """
        if not self.db.desire_tasks:
            self.db.desire_tasks = {}
        
        if target_zone not in self.db.desire_tasks:
            self.db.desire_tasks[target_zone] = {}
        
        self.db.desire_tasks[target_zone][character.id] = {
            "requirement": requirement,
            "points": 0
        }
        
        return self.db.desire_tasks[target_zone][character.id]
    
    def add_desire_task_points(self, target_zone, character, points):
        """
        Add points to desire discovery task.
        Points = Understand - 2 per success.
        
        Args:
            target_zone: Zone whose desire is being discovered
            character: Character making progress
            points: Points to add
            
        Returns:
            bool: True if task is complete
        """
        if target_zone not in self.db.desire_tasks:
            return False
        
        if character.id not in self.db.desire_tasks[target_zone]:
            return False
        
        task = self.db.desire_tasks[target_zone][character.id]
        task["points"] += points
        
        if task["points"] >= task["requirement"]:
            # Mark desire as known
            if character.id not in self.db.zones[target_zone]["desire_known"]:
                self.db.zones[target_zone]["desire_known"].append(character.id)
            return True
        
        return False
    
    def set_attack_task(self, target_character, requirement, attacker=None):
        """
        Set up extended task for social attack.
        
        Args:
            target_character: Character being attacked
            requirement: Requirement (target's Discipline skill)
            attacker: Attacking character
            
        Returns:
            dict: Task status
        """
        if not self.db.attack_tasks:
            self.db.attack_tasks = {}
        
        target_id = target_character.id
        
        if target_id not in self.db.attack_tasks:
            self.db.attack_tasks[target_id] = {
                "requirement": requirement,
                "points": 0,
                "attackers": []
            }
        
        task = self.db.attack_tasks[target_id]
        
        # Update requirement if higher
        if requirement > task["requirement"]:
            task["requirement"] = requirement
        
        # Add attacker
        if attacker and attacker.id not in task["attackers"]:
            task["attackers"].append(attacker.id)
        
        return task
    
    def add_attack_task_points(self, target_character, points):
        """
        Add points to attack task.
        
        Args:
            target_character: Character being attacked
            points: Points to add
            
        Returns:
            bool: True if task is complete
        """
        if not self.db.attack_tasks:
            return False
        
        target_id = target_character.id
        if target_id not in self.db.attack_tasks:
            return False
        
        task = self.db.attack_tasks[target_id]
        task["points"] += points
        
        return task["points"] >= task["requirement"]
    
    def target_asset(self, character, asset_name, zone_name):
        """
        Target an opponent's asset (challenge truth, cast doubt).
        
        Args:
            character: Character targeting the asset
            asset_name: Name of asset to target
            zone_name: Zone where asset is located
            
        Returns:
            tuple: (success: bool, message: str, result: str)
        """
        # Find asset
        asset_data = None
        for asset_id, adata in self.db.assets.items():
            if adata["zone"] == zone_name:
                asset_obj = adata["asset"]
                if (isinstance(asset_obj, str) and asset_obj == asset_name) or \
                   (hasattr(asset_obj, 'name') and asset_obj.name == asset_name):
                    asset_data = adata
                    break
        
        if not asset_data:
            return (False, f"Asset '{asset_name}' not found in {zone_name}.", None)
        
        # Check if it's opponent's asset
        if asset_data["owner"].id == character.id:
            return (False, "You cannot target your own asset.", None)
        
        asset_type = asset_data["type"]
        
        if asset_type == "knowledge":
            # Can challenge if you have contradictory information
            return (True, f"Challenged the truth of {asset_name}. If successful, its leverage is diminished.", "challenged")
        
        elif asset_type == "rumor":
            # Easier to remove - loses Quality if doubt is cast
            return (True, f"Casting doubt on {asset_name}. If successful, it loses all Quality.", "doubted")
        
        elif asset_type == "valuable":
            # Can question worth or demonstrate no need
            return (True, f"Questioning the value of {asset_name}. If successful, it becomes less useful as leverage.", "questioned")
        
        return (False, "Cannot target this asset type.", None)
    
    def get_display(self, viewer):
        """
        Get a formatted display of the intrigue conflict state.
        
        Args:
            viewer: Character viewing the conflict
            
        Returns:
            str: Formatted display
        """
        lines = []
        lines.append("|w" + "=" * 80 + "|n")
        lines.append("|wINTRIGUE CONFLICT|n".center(80))
        lines.append("|w" + "=" * 80 + "|n")
        
        # Show zones
        lines.append("|wParticipants:|n")
        for zone_name, zone_data in self.db.zones.items():
            zone_type = zone_data["type"]
            disposition = self.get_disposition(zone_name, viewer)
            disposition_display = {
                "Allied": "|gAllied|n",
                "Friendly": "|cFriendly|n",
                "Neutral": "|yNeutral|n",
                "Unfriendly": "|mUnfriendly|n",
                "Opposed": "|rOpposed|n"
            }.get(disposition, "|yNeutral|n")
            
            lines.append(f"  |y{zone_name}|n ({zone_type}) - Disposition: {disposition_display}")
            
            # Show desire if known
            if viewer.id in zone_data.get("desire_known", []):
                desire = zone_data.get("desire", "")
                if desire:
                    lines.append(f"    Desire: {desire}")
            
            # Show assets in zone
            assets = []
            for asset_id, asset_data in self.db.assets.items():
                if asset_data["zone"] == zone_name and asset_data["owner"].id == viewer.id:
                    asset_obj = asset_data["asset"]
                    asset_name = asset_obj if isinstance(asset_obj, str) else asset_obj.name
                    assets.append(asset_name)
            
            if assets:
                lines.append(f"    Your assets: {', '.join(assets)}")
        
        lines.append("")
        
        # Show objective
        if viewer.id in self.db.objectives:
            obj = self.db.objectives[viewer.id]
            lines.append(f"|wYour Objective:|n {obj.get('objective', 'None')}")
        
        lines.append("|w" + "=" * 80 + "|n")
        return "\n".join(lines)

