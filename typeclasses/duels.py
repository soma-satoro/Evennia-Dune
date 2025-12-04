"""
Duel System for Dune 2d20

Implements turn-based dueling with zones, asset positioning, and combat resolution.
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent


class Duel(ObjectParent, DefaultObject):
    """
    A Duel represents a one-on-one combat between two characters.
    
    Each combatant has:
    - 1 personal zone (themselves)
    - 2 guard zones (left/right or high/low)
    
    Assets can be positioned in zones and moved between them.
    Attacks require moving assets into the opponent's zone.
    """
    
    def at_object_creation(self):
        """Initialize duel state"""
        super().at_object_creation()
        
        # Combatants
        self.db.combatant1 = None  # Character object
        self.db.combatant2 = None  # Character object
        
        # Current turn
        self.db.current_turn = None  # Character whose turn it is
        self.db.initiative_holder = None  # Character who has initiative
        self.db.current_round = 1  # Current round number
        self.db.initiative_kept = False  # Whether initiative was kept this round
        
        # Zones for each combatant
        # Format: {combatant_id: {"personal": [], "left_guard": [], "right_guard": []}}
        self.db.zones = {}
        
        # Assets in the duel
        # Format: {asset_id: {"owner": character, "zone": "personal|left_guard|right_guard", "type": "weapon|shield|armor|intangible"}}
        self.db.assets = {}
        
        # Intangible assets (positioning, aiming, etc.)
        # Format: {asset_name: {"owner": character, "zone": zone, "description": str}}
        self.db.intangible_assets = {}
        
        # Duel state
        self.db.status = "active"  # active, concluded
        self.db.winner = None
        self.db.defeat_type = None  # surrender, unconscious, injury, death
        
        # Extended task for non-minor characters
        self.db.extended_task = None  # {"requirement": int, "points": int}
        
        # Room where duel takes place
        self.db.location = None
    
    def add_combatant(self, character):
        """
        Add a combatant to the duel.
        
        Args:
            character: Character object to add
            
        Returns:
            bool: True if added, False if duel is full
        """
        if not self.db.combatant1:
            self.db.combatant1 = character
            self._initialize_zones(character)
            return True
        elif not self.db.combatant2:
            self.db.combatant2 = character
            self._initialize_zones(character)
            return True
        return False
    
    def _initialize_zones(self, character):
        """Initialize zones for a combatant"""
        if not self.db.zones:
            self.db.zones = {}
        
        char_id = character.id
        self.db.zones[char_id] = {
            "personal": [],
            "left_guard": [],
            "right_guard": []
        }
    
    def get_opponent(self, character):
        """Get the opponent of a given character"""
        if self.db.combatant1 and self.db.combatant1.id == character.id:
            return self.db.combatant2
        elif self.db.combatant2 and self.db.combatant2.id == character.id:
            return self.db.combatant1
        return None
    
    def get_zones(self, character):
        """Get zones for a character"""
        if not character:
            return None
        return self.db.zones.get(character.id)
    
    def get_opponent_zones(self, character):
        """Get opponent's zones"""
        opponent = self.get_opponent(character)
        if opponent:
            return self.get_zones(opponent)
        return None
    
    def add_asset(self, character, asset, zone="personal", asset_type="weapon"):
        """
        Add an asset to the duel and position it in a zone.
        
        Args:
            character: Character who owns the asset
            asset: Asset object
            zone: Zone name ("personal", "left_guard", "right_guard")
            asset_type: Type of asset ("weapon", "shield", "armor", "intangible")
            
        Returns:
            bool: True if added successfully
        """
        if not character or not asset:
            return False
        
        char_id = character.id
        asset_id = asset.id
        
        # Initialize zones if needed
        if char_id not in self.db.zones:
            self._initialize_zones(character)
        
        # Validate zone
        if zone not in ["personal", "left_guard", "right_guard"]:
            return False
        
        # Add to asset tracking
        if not self.db.assets:
            self.db.assets = {}
        
        self.db.assets[asset_id] = {
            "owner": character,
            "zone": zone,
            "type": asset_type,
            "asset": asset
        }
        
        # Add to zone
        self.db.zones[char_id][zone].append(asset_id)
        
        return True
    
    def move_asset(self, character, asset, target_zone, subtle=False):
        """
        Move an asset from one zone to another.
        
        Args:
            character: Character who owns the asset
            asset: Asset object to move
            target_zone: Target zone name
            subtle: If True, this is a subtle move (opponent may not notice)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not character or not asset:
            return (False, "Invalid character or asset.")
        
        asset_id = asset.id
        
        # Check if asset is in the duel
        if asset_id not in self.db.assets:
            return (False, f"{asset.name} is not in this duel.")
        
        asset_data = self.db.assets[asset_id]
        
        # Check ownership
        if asset_data["owner"].id != character.id:
            return (False, f"You don't own {asset.name}.")
        
        # Check if it's a shield (full shields can't move)
        if asset_data["type"] == "shield":
            # Check if it's a full shield (can't move) or half-shield (can move to adjacent)
            keywords = asset.get_keywords()
            keywords_lower = [k.lower() for k in keywords]
            
            if "half-shield" not in keywords_lower and "half shield" not in keywords_lower:
                # Full shield - can't move
                return (False, "Full shields cannot be moved.")
            
            # Half-shield can only move to adjacent zones
            current_zone = asset_data["zone"]
            if target_zone == current_zone:
                return (False, "Asset is already in that zone.")
            
            # For half-shields, can only move to personal zone or adjacent guard zones
            if current_zone == "personal":
                if target_zone not in ["left_guard", "right_guard"]:
                    return (False, "Half-shields can only move to adjacent guard zones.")
            elif current_zone in ["left_guard", "right_guard"]:
                if target_zone != "personal":
                    return (False, "Half-shields can only move to the personal zone or adjacent guard zones.")
        
        # Validate target zone
        if target_zone not in ["personal", "left_guard", "right_guard"]:
            # Check if moving to opponent's zone (for attacks)
            opponent = self.get_opponent(character)
            if opponent and target_zone in ["opponent_personal", "opponent_left_guard", "opponent_right_guard"]:
                # Convert to opponent's actual zone
                if target_zone == "opponent_personal":
                    target_zone = "personal"
                elif target_zone == "opponent_left_guard":
                    target_zone = "left_guard"
                elif target_zone == "opponent_right_guard":
                    target_zone = "right_guard"
                
                # Move to opponent's zone (for attack)
                opponent_zones = self.get_opponent_zones(character)
                if opponent_zones:
                    # Remove from current zone
                    current_zone = asset_data["zone"]
                    char_id = character.id
                    if asset_id in self.db.zones[char_id][current_zone]:
                        self.db.zones[char_id][current_zone].remove(asset_id)
                    
                    # Add to opponent's zone
                    opponent_id = opponent.id
                    if opponent_id not in self.db.zones:
                        self._initialize_zones(opponent)
                    self.db.zones[opponent_id][target_zone].append(asset_id)
                    asset_data["zone"] = f"opponent_{target_zone}"
                    return (True, f"Moved {asset.name} to opponent's {target_zone.replace('_', ' ')} zone.")
            else:
                return (False, "Invalid target zone.")
        
        # Normal movement within own zones
        current_zone = asset_data["zone"]
        if current_zone == target_zone:
            return (False, "Asset is already in that zone.")
        
        char_id = character.id
        
        # Remove from current zone
        if asset_id in self.db.zones[char_id][current_zone]:
            self.db.zones[char_id][current_zone].remove(asset_id)
        
        # Add to target zone
        self.db.zones[char_id][target_zone].append(asset_id)
        asset_data["zone"] = target_zone
        
        move_type = "subtly" if subtle else "boldly"
        return (True, f"Moved {asset.name} {move_type} to {target_zone.replace('_', ' ')} zone.")
    
    def get_assets_in_zone(self, character, zone):
        """
        Get all assets in a specific zone.
        
        Args:
            character: Character whose zones to check
            zone: Zone name
            
        Returns:
            list: List of asset objects
        """
        zones = self.get_zones(character)
        if not zones or zone not in zones:
            return []
        
        asset_ids = zones[zone]
        assets = []
        for asset_id in asset_ids:
            if asset_id in self.db.assets:
                asset_data = self.db.assets[asset_id]
                assets.append(asset_data["asset"])
        
        return assets
    
    def get_defensive_assets_in_zone(self, character, zone):
        """
        Get defensive assets (shields, armor, weapons used defensively) in a zone.
        
        Args:
            character: Character whose zones to check
            zone: Zone name
            
        Returns:
            list: List of defensive asset objects
        """
        assets = self.get_assets_in_zone(character, zone)
        defensive = []
        
        for asset in assets:
            asset_id = asset.id
            if asset_id in self.db.assets:
                asset_data = self.db.assets[asset_id]
                asset_type = asset_data["type"]
                if asset_type in ["shield", "armor"]:
                    defensive.append(asset)
                elif asset_type == "weapon":
                    # Weapons can be used defensively if in guard zones
                    if zone in ["left_guard", "right_guard"]:
                        defensive.append(asset)
        
        return defensive
    
    def set_current_turn(self, character):
        """Set whose turn it is"""
        self.db.current_turn = character
    
    def get_current_turn(self):
        """Get whose turn it is"""
        return self.db.current_turn
    
    def set_initiative(self, character):
        """Set who has initiative"""
        self.db.initiative_holder = character
    
    def get_initiative_holder(self):
        """Get who has initiative"""
        return self.db.initiative_holder
    
    def keep_initiative(self, character, momentum_cost=2):
        """
        Keep the initiative (take extra action or allow ally to act).
        
        Args:
            character: Character keeping initiative
            momentum_cost: Cost in Momentum (default 2)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.db.initiative_kept:
            return (False, "Initiative has already been kept this round.")
        
        if character != self.db.current_turn:
            return (False, "You can only keep initiative on your turn.")
        
        self.db.initiative_kept = True
        self.db.initiative_holder = character
        
        return (True, f"{character.name} keeps the initiative!")
    
    def next_turn(self):
        """Move to next turn in the duel"""
        if not self.db.combatant1 or not self.db.combatant2:
            return None
        
        current = self.db.current_turn
        
        # Switch to opponent
        if current == self.db.combatant1:
            self.db.current_turn = self.db.combatant2
        elif current == self.db.combatant2:
            self.db.current_turn = self.db.combatant1
            # Round complete
            self.db.current_round += 1
            self.db.initiative_kept = False
        else:
            # Initialize
            self.db.current_turn = self.db.combatant1
            self.db.current_round = 1
        
        return self.db.current_turn
    
    def get_current_round(self):
        """Get current round number"""
        return self.db.current_round or 1
    
    def create_intangible_asset(self, character, name, description, zone="personal"):
        """
        Create an intangible asset (positioning, aiming, etc.).
        
        Args:
            character: Character creating the asset
            name: Name of the intangible asset
            description: Description of what it represents
            zone: Zone where it's located
            
        Returns:
            bool: True if created
        """
        if not self.db.intangible_assets:
            self.db.intangible_assets = {}
        
        self.db.intangible_assets[name] = {
            "owner": character,
            "zone": zone,
            "description": description
        }
        
        return True
    
    def remove_intangible_asset(self, name):
        """Remove an intangible asset"""
        if self.db.intangible_assets and name in self.db.intangible_assets:
            del self.db.intangible_assets[name]
            return True
        return False
    
    def set_extended_task(self, requirement):
        """
        Set up an extended task for a non-minor character.
        
        Args:
            requirement: Number of successes needed (typically opponent's Battle skill)
        """
        self.db.extended_task = {
            "requirement": requirement,
            "points": 0
        }
    
    def add_extended_task_points(self, points):
        """
        Add points to the extended task.
        
        Args:
            points: Points to add
            
        Returns:
            bool: True if task is complete
        """
        if not self.db.extended_task:
            return False
        
        self.db.extended_task["points"] += points
        requirement = self.db.extended_task["requirement"]
        current_points = self.db.extended_task["points"]
        
        return current_points >= requirement
    
    def get_extended_task_status(self):
        """Get extended task status"""
        if not self.db.extended_task:
            return None
        
        return {
            "points": self.db.extended_task["points"],
            "requirement": self.db.extended_task["requirement"]
        }
    
    def conclude_duel(self, winner, defeat_type="surrender"):
        """
        Conclude the duel.
        
        Args:
            winner: Character who won
            defeat_type: Type of defeat (surrender, unconscious, injury, death)
        """
        self.db.status = "concluded"
        self.db.winner = winner
        self.db.defeat_type = defeat_type
    
    def get_display(self, viewer):
        """
        Get a formatted display of the duel state.
        
        Args:
            viewer: Character viewing the duel
            
        Returns:
            str: Formatted duel display
        """
        lines = []
        lines.append("|w" + "=" * 80 + "|n")
        lines.append("|wDUEL STATUS|n".center(80))
        lines.append("|w" + "=" * 80 + "|n")
        
        if not self.db.combatant1 or not self.db.combatant2:
            lines.append("|rDuel is not properly initialized.|n")
            return "\n".join(lines)
        
        combatant1 = self.db.combatant1
        combatant2 = self.db.combatant2
        
        # Show combatants
        lines.append(f"|wCombatants:|n {combatant1.name} vs {combatant2.name}")
        lines.append("")
        
        # Show current turn
        current_turn = self.get_current_turn()
        if current_turn:
            lines.append(f"|wCurrent Turn:|n {current_turn.name}")
        else:
            lines.append("|wCurrent Turn:|n Not set")
        
        # Show initiative
        initiative = self.get_initiative_holder()
        if initiative:
            lines.append(f"|wInitiative:|n {initiative.name}")
        lines.append("")
        
        # Show zones for viewer's character
        if viewer == combatant1 or viewer == combatant2:
            lines.append(f"|wYour Zones:|n")
            zones = self.get_zones(viewer)
            if zones:
                lines.append(f"  |yPersonal Zone:|n {len(zones['personal'])} assets")
                lines.append(f"  |yLeft Guard:|n {len(zones['left_guard'])} assets")
                lines.append(f"  |yRight Guard:|n {len(zones['right_guard'])} assets")
                lines.append("")
                
                # List assets in each zone
                for zone_name, zone_display in [("personal", "Personal Zone"), ("left_guard", "Left Guard"), ("right_guard", "Right Guard")]:
                    assets = self.get_assets_in_zone(viewer, zone_name)
                    if assets:
                        lines.append(f"  |y{zone_display}:|n")
                        for asset in assets:
                            asset_id = asset.id
                            if asset_id in self.db.assets:
                                asset_data = self.db.assets[asset_id]
                                asset_type = asset_data["type"]
                                lines.append(f"    • {asset.name} ({asset_type})")
        
        lines.append("|w" + "=" * 80 + "|n")
        return "\n".join(lines)

