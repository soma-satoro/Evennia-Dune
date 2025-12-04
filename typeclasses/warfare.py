"""
Warfare System for Dune 2d20

Implements warfare conflicts with strategic zones, military assets, and large-scale combat.
Requires Architect-level play.
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent


class WarfareConflict(ObjectParent, DefaultObject):
    """
    A Warfare Conflict represents large-scale military combat.
    
    Zones represent strategic locations (gates, roads, hills, mines, factories, etc.).
    Assets represent military units (infantry, vehicles, aircraft, fortifications).
    Requires Architect-level play to participate.
    """
    
    def at_object_creation(self):
        """Initialize warfare conflict state"""
        super().at_object_creation()
        
        # Participants (commanders/spymasters)
        self.db.participants = []  # List of character objects
        
        # Strategic zones
        # Format: {zone_name: {"description": str, "benefits": [str], "problems": [str], "controlled_by": character_id or None}}
        self.db.zones = {}
        
        # Objectives (what each side is trying to achieve)
        # Format: {character_id: {"objective": str, "zones": [zone_names]}}
        self.db.objectives = {}
        
        # Assets in the conflict
        # Format: {asset_id: {"owner": character, "zone": zone_name, "type": "infantry|vehicle|aircraft|fortification", "asset": asset_object, "quality": int, "defeated": bool}}
        self.db.assets = {}
        
        # Intangible assets (ambushes, tactical ploys, intelligence)
        # Format: {asset_name: {"owner": character, "zone": zone_name, "description": str, "type": "ambush|ploy|intelligence"}}
        self.db.intangible_assets = {}
        
        # Extended tasks for non-minor characters
        # Format: {character_id: {"requirement": int, "points": int}}
        self.db.extended_tasks = {}
        
        # Character positions (where commanders are)
        # Format: {character_id: zone_name}
        self.db.character_positions = {}
        
        # Conflict state
        self.db.status = "active"  # active, concluded
        self.db.winners = []  # List of winning characters/teams
        self.db.defeated = []  # List of defeated characters
        
        # Room where conflict takes place (if applicable)
        self.db.location = None
    
    def add_participant(self, character, objective="", objective_zones=None):
        """
        Add a participant to the warfare conflict.
        Requires Architect-level access.
        
        Args:
            character: Character object to add
            objective: Their objective in this conflict
            objective_zones: List of zone names that are objectives
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Check Architect access
        if not hasattr(character, 'can_use_architect_mode'):
            return (False, "Character cannot participate in warfare conflicts.")
        
        if not character.can_use_architect_mode():
            access_level = character.get_architect_access_level()
            title = character.get_title()
            role = character.get_role()
            if access_level == "limited":
                return (False, "You have limited Architect access. Warfare requires full Architect access (Major/Noble titles or full-access roles).")
            else:
                source = title if title else (role if role else "title or role")
                return (False, f"You must have an appropriate title (Major/Noble) or role (Ruler, Marshal, Warmaster, etc.) to participate in warfare. Currently: {source}")
        
        if character in self.db.participants:
            return (False, "Character is already in this conflict.")
        
        self.db.participants.append(character)
        
        if not self.db.objectives:
            self.db.objectives = {}
        
        if objective:
            self.db.objectives[character.id] = {
                "objective": objective,
                "zones": objective_zones or []
            }
        
        return (True, f"{character.name} joined the warfare conflict.")
    
    def add_zone(self, zone_name, description="", benefits=None, problems=None):
        """
        Add a strategic zone to the warfare conflict.
        
        Args:
            zone_name: Name of the zone
            description: Description of the strategic location
            benefits: List of benefits this zone provides
            problems: List of problems/terrain issues
            
        Returns:
            bool: True if added
        """
        if not self.db.zones:
            self.db.zones = {}
        
        self.db.zones[zone_name] = {
            "description": description,
            "benefits": benefits or [],
            "problems": problems or [],
            "controlled_by": None
        }
        return True
    
    def set_character_position(self, character, zone_name):
        """Set where a character (commander) is positioned"""
        if not self.db.character_positions:
            self.db.character_positions = {}
        
        if zone_name not in self.db.zones:
            return False
        
        self.db.character_positions[character.id] = zone_name
        return True
    
    def get_character_position(self, character):
        """Get where a character is positioned"""
        if not self.db.character_positions:
            return None
        return self.db.character_positions.get(character.id)
    
    def add_asset(self, character, asset, zone_name, asset_type="infantry"):
        """
        Add a military asset to the warfare conflict.
        
        Args:
            character: Character who owns the asset
            asset: Asset object
            zone_name: Zone to place asset in
            asset_type: Type ("infantry", "vehicle", "aircraft", "fortification")
            
        Returns:
            bool: True if added successfully
        """
        if zone_name not in self.db.zones:
            return False
        
        if not self.db.assets:
            self.db.assets = {}
        
        asset_id = asset.id
        quality = asset.get_quality() if hasattr(asset, 'get_quality') else 0
        
        self.db.assets[asset_id] = {
            "owner": character,
            "zone": zone_name,
            "type": asset_type,
            "asset": asset,
            "quality": quality,
            "defeated": False
        }
        
        return True
    
    def get_assets_in_zone(self, zone_name, character=None):
        """
        Get all assets in a specific zone.
        
        Args:
            zone_name: Name of the zone
            character: If provided, only show assets owned by this character
            
        Returns:
            list: List of asset data dictionaries
        """
        assets = []
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["zone"] == zone_name and not asset_data.get("defeated", False):
                if character is None or asset_data["owner"].id == character.id:
                    assets.append(asset_data)
        
        return assets
    
    def get_allied_assets_in_zone(self, character, zone_name):
        """Get all allied assets in a zone (for difficulty calculation)"""
        assets = []
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["zone"] == zone_name and asset_data["owner"].id == character.id:
                if not asset_data.get("defeated", False):
                    assets.append(asset_data)
        
        return assets
    
    def get_adjacent_zones(self, zone_name):
        """
        Get zones adjacent to a given zone.
        
        Args:
            zone_name: Name of the zone
            
        Returns:
            list: List of adjacent zone names
        """
        # For warfare, all zones are considered adjacent
        # (unlike skirmish where adjacency might be more specific)
        adjacent = []
        for zone in self.db.zones.keys():
            if zone != zone_name:
                adjacent.append(zone)
        return adjacent
    
    def is_asset_fast(self, asset_data):
        """Check if an asset is 'Fast' (aircraft, high-speed vehicles)"""
        asset = asset_data.get("asset")
        if not asset:
            return False
        
        keywords = asset.get_keywords() if hasattr(asset, 'get_keywords') else []
        keywords_lower = [k.lower() for k in keywords]
        
        # Aircraft are fast
        if asset_data["type"] == "aircraft":
            return True
        
        # Check for "Fast" keyword
        if "fast" in keywords_lower:
            return True
        
        return False
    
    def is_asset_immobile(self, asset_data):
        """Check if an asset is immobile (fortifications)"""
        return asset_data["type"] == "fortification"
    
    def move_asset(self, character, asset, target_zone, subtle=False, bold=False, move_character=False):
        """
        Move an asset to a different zone.
        
        Args:
            character: Character who owns the asset
            asset: Asset object
            target_zone: Target zone name
            subtle: If True, subtle movement
            bold: If True, bold movement
            move_character: If True, move character with asset
            
        Returns:
            tuple: (success: bool, message: str, difficulty_modifier: int, momentum_cost: int)
        """
        if target_zone not in self.db.zones:
            return (False, f"Zone '{target_zone}' does not exist.", 0, 0)
        
        # Find asset
        asset_id = asset.id
        if asset_id not in self.db.assets:
            return (False, "Asset is not in this conflict.", 0, 0)
        
        asset_data = self.db.assets[asset_id]
        
        # Check ownership
        if asset_data["owner"].id != character.id:
            return (False, "You don't own this asset.", 0, 0)
        
        # Check if defeated
        if asset_data.get("defeated", False):
            return (False, "This asset has been defeated and withdrawn.", 0, 0)
        
        # Check if immobile
        if self.is_asset_immobile(asset_data):
            return (False, "Fortifications cannot be moved.", 0, 0)
        
        # Check if fast (aircraft move one additional zone)
        is_fast = self.is_asset_fast(asset_data)
        
        # Check character position for difficulty reduction
        character_zone = self.get_character_position(character)
        same_zone = character_zone == asset_data["zone"]
        
        difficulty_modifier = 0
        momentum_cost = 0
        
        # If character not in same zone, can reduce Momentum cost to 1
        if not same_zone:
            momentum_cost = 1  # Reduced from 2
        
        # Move asset
        asset_data["zone"] = target_zone
        
        # Move character if requested
        if move_character:
            self.set_character_position(character, target_zone)
        
        move_type = "subtly" if subtle else ("boldly" if bold else "")
        message = f"Moved {asset.name} {move_type} to {target_zone} zone."
        
        if is_fast:
            message += " (Fast asset - moved one additional zone)"
        
        if same_zone:
            message += " (Character in same zone - -1 Difficulty)"
        
        return (True, message, difficulty_modifier, momentum_cost)
    
    def get_attack_difficulty(self, attacker, target_zone, attacking_asset):
        """
        Calculate attack difficulty for warfare.
        Base +1 per additional allied asset in same zone.
        
        Args:
            attacker: Attacking character
            target_zone: Zone being attacked
            attacking_asset: Asset making the attack
            
        Returns:
            int: Difficulty
        """
        base_difficulty = 1
        
        # Get all allied assets in the same zone as attacking asset
        attacking_asset_zone = None
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["asset"].id == attacking_asset.id:
                attacking_asset_zone = asset_data["zone"]
                break
        
        if attacking_asset_zone:
            allied_assets = self.get_allied_assets_in_zone(attacker, attacking_asset_zone)
            # +1 for each additional asset (beyond the attacking one)
            additional_assets = len(allied_assets) - 1
            if additional_assets > 0:
                return base_difficulty + additional_assets
        
        return base_difficulty
    
    def defeat_asset(self, asset_id):
        """
        Mark an asset as defeated (withdrawn from battle).
        Can be rallied later with -1 Quality.
        
        Args:
            asset_id: ID of the asset
            
        Returns:
            bool: True if defeated
        """
        if asset_id not in self.db.assets:
            return False
        
        asset_data = self.db.assets[asset_id]
        asset_data["defeated"] = True
        
        # Reduce quality by 1 for when it's rallied
        asset_data["rally_quality"] = max(0, asset_data["quality"] - 1)
        
        return True
    
    def rally_asset(self, asset_id):
        """
        Rally a defeated asset back into battle.
        Returns with -1 Quality.
        
        Args:
            asset_id: ID of the asset
            
        Returns:
            bool: True if rallied
        """
        if asset_id not in self.db.assets:
            return False
        
        asset_data = self.db.assets[asset_id]
        if not asset_data.get("defeated", False):
            return False
        
        asset_data["defeated"] = False
        asset_data["quality"] = asset_data.get("rally_quality", max(0, asset_data["quality"] - 1))
        
        return True
    
    def control_zone(self, character, zone_name):
        """Set a character as controlling a zone"""
        if zone_name not in self.db.zones:
            return False
        
        self.db.zones[zone_name]["controlled_by"] = character.id
        return True
    
    def check_objective(self, character):
        """
        Check if a character has achieved their objective.
        
        Args:
            character: Character to check
            
        Returns:
            bool: True if objective achieved
        """
        if character.id not in self.db.objectives:
            return False
        
        objective = self.db.objectives[character.id]
        objective_zones = objective.get("zones", [])
        
        # Check if character controls all objective zones
        for zone_name in objective_zones:
            if zone_name not in self.db.zones:
                return False
            
            controlled_by = self.db.zones[zone_name].get("controlled_by")
            if controlled_by != character.id:
                return False
        
        return True
    
    def create_intangible_asset(self, character, name, description, zone_name, asset_type="ploy"):
        """
        Create an intangible asset (ambush, ploy, intelligence).
        
        Args:
            character: Character creating the asset
            name: Name of the intangible asset
            description: Description
            zone_name: Zone where it's located
            asset_type: Type ("ambush", "ploy", "intelligence")
            
        Returns:
            bool: True if created
        """
        if not self.db.intangible_assets:
            self.db.intangible_assets = {}
        
        self.db.intangible_assets[name] = {
            "owner": character,
            "zone": zone_name,
            "description": description,
            "type": asset_type
        }
        
        return True
    
    def get_display(self, viewer):
        """
        Get a formatted display of the warfare conflict state.
        
        Args:
            viewer: Character viewing the conflict
            
        Returns:
            str: Formatted display
        """
        lines = []
        lines.append("|w" + "=" * 80 + "|n")
        lines.append("|wWARFARE CONFLICT|n".center(80))
        lines.append("|w" + "=" * 80 + "|n")
        
        # Show zones
        lines.append("|wStrategic Zones:|n")
        for zone_name, zone_data in self.db.zones.items():
            controlled_by = zone_data.get("controlled_by")
            controller = None
            if controlled_by:
                for participant in self.db.participants:
                    if participant.id == controlled_by:
                        controller = participant.name
                        break
            
            control_status = f"|g[Controlled by {controller}]|n" if controller else "|y[Uncontrolled]|n"
            lines.append(f"  |y{zone_name}|n {control_status}")
            
            if zone_data.get("description"):
                lines.append(f"    {zone_data['description']}")
            
            if zone_data.get("benefits"):
                lines.append(f"    Benefits: {', '.join(zone_data['benefits'])}")
            
            if zone_data.get("problems"):
                lines.append(f"    Problems: {', '.join(zone_data['problems'])}")
            
            # Show assets
            assets = self.get_assets_in_zone(zone_name, viewer)
            if assets:
                asset_names = [a["asset"].name for a in assets]
                lines.append(f"    Your assets: {', '.join(asset_names)}")
        
        lines.append("")
        
        # Show character position
        char_pos = self.get_character_position(viewer)
        if char_pos:
            lines.append(f"|wYour Position:|n {char_pos}")
        
        # Show objective
        if viewer.id in self.db.objectives:
            obj = self.db.objectives[viewer.id]
            lines.append(f"|wYour Objective:|n {obj.get('objective', 'None')}")
            if obj.get("zones"):
                lines.append(f"  Objective zones: {', '.join(obj['zones'])}")
        
        lines.append("|w" + "=" * 80 + "|n")
        return "\n".join(lines)

