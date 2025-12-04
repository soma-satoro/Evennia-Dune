"""
Espionage System for Dune 2d20

Implements espionage conflicts with abstract zones representing people, groups, and places.
"""

from evennia.objects.objects import DefaultObject
from .objects import ObjectParent


class EspionageConflict(ObjectParent, DefaultObject):
    """
    An Espionage Conflict represents an information-gathering operation.
    
    Zones represent:
    - People (individuals)
    - Groups (organizations, factions)
    - Places (locations)
    - Events (time-sensitive gatherings)
    
    Connections between zones represent relationships and access paths.
    Zones and connections can be hidden and revealed through actions.
    """
    
    def at_object_creation(self):
        """Initialize espionage conflict state"""
        super().at_object_creation()
        
        # Participants (spymasters/agents)
        self.db.participants = []  # List of character objects
        
        # Zones (people, groups, places, events)
        # Format: {zone_name: {"type": "person|group|place|event", "description": str, "hidden": bool, "revealed_to": [character_ids]}}
        self.db.zones = {}
        
        # Connections between zones
        # Format: {zone1: {zone2: {"type": str, "description": str, "hidden": bool, "revealed_to": [character_ids]}}}
        self.db.connections = {}
        
        # Assets in the conflict
        # Format: {asset_id: {"owner": character, "zone": zone_name, "type": "spy|informant|surveillance|security", "asset": asset_object}}
        self.db.assets = {}
        
        # Intangible assets (rumors, information leaks, propaganda, security procedures)
        # Format: {asset_name: {"owner": character, "zone": zone_name, "description": str, "type": "rumor|leak|propaganda|procedure"}}
        self.db.intangible_assets = {}
        
        # Extended tasks for information gathering
        # Format: {task_id: {"requirement": int, "points": int, "zones": [zone_names], "participants": [character_ids]}}
        self.db.extended_tasks = {}
        
        # Conflict state
        self.db.status = "active"  # active, concluded
        self.db.objectives = {}  # {character_id: objective_description}
        
        # Room where conflict takes place (if applicable)
        self.db.location = None
    
    def add_participant(self, character, objective=""):
        """
        Add a participant to the espionage conflict.
        
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
            self.db.objectives[character.id] = objective
        
        return True
    
    def add_zone(self, zone_name, zone_type="place", description="", hidden=False):
        """
        Add a zone to the espionage conflict.
        
        Args:
            zone_name: Name of the zone
            zone_type: Type ("person", "group", "place", "event")
            description: Description of the zone
            hidden: If True, zone is hidden from players
            
        Returns:
            bool: True if added
        """
        if not self.db.zones:
            self.db.zones = {}
        
        self.db.zones[zone_name] = {
            "type": zone_type,
            "description": description,
            "hidden": hidden,
            "revealed_to": []
        }
        return True
    
    def reveal_zone(self, zone_name, character):
        """Reveal a hidden zone to a character"""
        if zone_name not in self.db.zones:
            return False
        
        if character.id not in self.db.zones[zone_name]["revealed_to"]:
            self.db.zones[zone_name]["revealed_to"].append(character.id)
            self.db.zones[zone_name]["hidden"] = False
        return True
    
    def add_connection(self, zone1, zone2, connection_type="", description="", hidden=False):
        """
        Add a connection between two zones.
        
        Args:
            zone1: First zone name
            zone2: Second zone name
            connection_type: Type of connection (e.g., "Runs", "Trades With", "Lives On")
            description: Description of the connection
            hidden: If True, connection is hidden
            
        Returns:
            bool: True if added
        """
        if zone1 not in self.db.zones or zone2 not in self.db.zones:
            return False
        
        if not self.db.connections:
            self.db.connections = {}
        
        if zone1 not in self.db.connections:
            self.db.connections[zone1] = {}
        
        self.db.connections[zone1][zone2] = {
            "type": connection_type,
            "description": description,
            "hidden": hidden,
            "revealed_to": []
        }
        
        # Also add reverse connection
        if zone2 not in self.db.connections:
            self.db.connections[zone2] = {}
        
        self.db.connections[zone2][zone1] = {
            "type": connection_type,
            "description": description,
            "hidden": hidden,
            "revealed_to": []
        }
        
        return True
    
    def reveal_connection(self, zone1, zone2, character):
        """Reveal a hidden connection to a character"""
        if zone1 not in self.db.connections or zone2 not in self.db.connections[zone1]:
            return False
        
        conn = self.db.connections[zone1][zone2]
        if character.id not in conn["revealed_to"]:
            conn["revealed_to"].append(character.id)
            conn["hidden"] = False
        
        # Also reveal reverse
        if zone2 in self.db.connections and zone1 in self.db.connections[zone2]:
            conn_reverse = self.db.connections[zone2][zone1]
            if character.id not in conn_reverse["revealed_to"]:
                conn_reverse["revealed_to"].append(character.id)
                conn_reverse["hidden"] = False
        
        return True
    
    def get_adjacent_zones(self, zone_name, character=None):
        """
        Get zones adjacent (connected) to a given zone.
        Only shows connections revealed to the character.
        
        Args:
            zone_name: Name of the zone
            character: Character viewing (None = show all)
            
        Returns:
            list: List of adjacent zone names
        """
        if zone_name not in self.db.connections:
            return []
        
        adjacent = []
        for connected_zone, conn_data in self.db.connections[zone_name].items():
            if character:
                # Only show if revealed to this character or not hidden
                if not conn_data["hidden"] or character.id in conn_data["revealed_to"]:
                    adjacent.append(connected_zone)
            else:
                # Show all if no character specified
                adjacent.append(connected_zone)
        
        return adjacent
    
    def get_character_spy_quality(self, character):
        """
        Calculate Quality for a character acting as a spy.
        Quality = lowest of Understand and Move, minus 4.
        
        Args:
            character: Character object
            
        Returns:
            int: Spy Quality rating
        """
        if not hasattr(character, 'get_skill'):
            return 0
        
        understand = character.get_skill("understand")
        move = character.get_skill("move")
        
        lowest = min(understand, move)
        quality = max(0, lowest - 4)  # Don't go below 0
        
        return quality
    
    def add_asset(self, character, asset, zone_name, asset_type="spy"):
        """
        Add an asset to the espionage conflict.
        
        Args:
            character: Character who owns the asset
            asset: Asset object (or character if acting as spy)
            zone_name: Zone to place asset in
            asset_type: Type ("spy", "informant", "surveillance", "security")
            
        Returns:
            bool: True if added successfully
        """
        if zone_name not in self.db.zones:
            return False
        
        # Check if zone is hidden
        if self.db.zones[zone_name]["hidden"]:
            if character.id not in self.db.zones[zone_name]["revealed_to"]:
                return False
        
        if not self.db.assets:
            self.db.assets = {}
        
        # Handle character acting as spy
        if hasattr(asset, 'id') and hasattr(asset, 'get_quality'):
            # Regular asset object
            asset_id = asset.id
        else:
            # Character acting as spy - use character ID
            asset_id = f"char_{asset.id}"
        
        self.db.assets[asset_id] = {
            "owner": character,
            "zone": zone_name,
            "type": asset_type,
            "asset": asset
        }
        
        return True
    
    def get_security_measures(self, zone_name):
        """
        Get all security measure assets in a zone.
        
        Args:
            zone_name: Name of the zone
            
        Returns:
            list: List of security asset objects with their Quality
        """
        security = []
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["zone"] == zone_name and asset_data["type"] == "security":
                asset_obj = asset_data["asset"]
                quality = asset_obj.get_quality() if hasattr(asset_obj, 'get_quality') else 0
                security.append({"asset": asset_obj, "quality": quality})
        
        return security
    
    def get_highest_security_quality(self, zone_name):
        """Get the highest Quality security measure in a zone"""
        security = self.get_security_measures(zone_name)
        if not security:
            return 0
        
        return max([s["quality"] for s in security])
    
    def move_asset(self, character, asset, target_zone, subtle=False, bold=False):
        """
        Move an asset to a different zone.
        
        Args:
            character: Character who owns the asset
            asset: Asset object (or character if acting as spy)
            target_zone: Target zone name
            subtle: If True, subtle movement (stealth)
            bold: If True, bold movement (attention-grabbing)
            
        Returns:
            tuple: (success: bool, message: str, difficulty_modifier: int)
        """
        if target_zone not in self.db.zones:
            return (False, f"Zone '{target_zone}' does not exist.", 0)
        
        # Check if zone is hidden
        if self.db.zones[target_zone]["hidden"]:
            if character.id not in self.db.zones[target_zone]["revealed_to"]:
                return (False, f"Zone '{target_zone}' is not known to you.", 0)
        
        # Find asset
        asset_id = None
        asset_data = None
        
        if hasattr(asset, 'id'):
            asset_id = asset.id
        else:
            # Character acting as spy
            asset_id = f"char_{asset.id}"
        
        if asset_id not in self.db.assets:
            return (False, "Asset is not in this conflict.", 0)
        
        asset_data = self.db.assets[asset_id]
        
        # Check ownership
        if asset_data["owner"].id != character.id:
            return (False, "You don't own this asset.", 0)
        
        # Check if surveillance device (can't move)
        if asset_data["type"] == "surveillance":
            return (False, "Surveillance devices cannot be moved once placed.", 0)
        
        # Check security for spy/informant movement
        difficulty_modifier = 0
        if asset_data["type"] in ["spy", "informant"]:
            # Get spy quality
            if hasattr(asset, 'get_quality'):
                spy_quality = asset.get_quality()
            elif asset_id.startswith("char_"):
                # Character acting as spy
                spy_quality = self.get_character_spy_quality(asset)
            else:
                spy_quality = 0
            
            security_quality = self.get_highest_security_quality(target_zone)
            
            # If security is higher, need subtle/bold movement
            if security_quality > spy_quality and not subtle and not bold:
                return (False, f"Security in {target_zone} (Quality {security_quality}) is too high for this asset (Quality {spy_quality}). Use subtle or bold movement.", 0)
            
            # Difficulty increases by +1 per security measure
            security_measures = self.get_security_measures(target_zone)
            difficulty_modifier = len(security_measures)
        
        # Move asset
        asset_data["zone"] = target_zone
        
        move_type = "subtly" if subtle else ("boldly" if bold else "")
        message = f"Moved {asset.name if hasattr(asset, 'name') else 'asset'} {move_type} to {target_zone} zone."
        
        return (True, message, difficulty_modifier)
    
    def get_assets_in_zone(self, zone_name, character=None):
        """
        Get all assets in a specific zone.
        
        Args:
            zone_name: Name of the zone
            character: If provided, only show assets owned by this character
            
        Returns:
            list: List of asset objects
        """
        assets = []
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["zone"] == zone_name:
                if character is None or asset_data["owner"].id == character.id:
                    assets.append(asset_data["asset"])
        
        return assets
    
    def get_information_assets(self, zone_name, character=None):
        """
        Get assets that can gather information in a zone.
        (spies, informants, surveillance devices)
        
        Args:
            zone_name: Name of the zone
            character: If provided, only show assets owned by this character
            
        Returns:
            list: List of asset objects
        """
        info_assets = []
        for asset_id, asset_data in self.db.assets.items():
            if asset_data["zone"] == zone_name:
                if asset_data["type"] in ["spy", "informant", "surveillance"]:
                    if character is None or asset_data["owner"].id == character.id:
                        info_assets.append(asset_data["asset"])
        
        return info_assets
    
    def get_information_difficulty(self, zone_name, character=None):
        """
        Calculate difficulty for gathering information in a zone.
        Base difficulty +1 per security measure.
        
        Args:
            zone_name: Name of the zone
            character: Character attempting to gather information
            
        Returns:
            int: Difficulty modifier
        """
        security_measures = self.get_security_measures(zone_name)
        return len(security_measures)
    
    def create_intangible_asset(self, character, name, description, zone_name, asset_type="rumor"):
        """
        Create an intangible asset (rumor, leak, propaganda, security procedure).
        
        Args:
            character: Character creating the asset
            name: Name of the intangible asset
            description: Description
            zone_name: Zone where it's located
            asset_type: Type ("rumor", "leak", "propaganda", "procedure")
            
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
    
    def target_asset(self, character, target_asset, zone_name):
        """
        Target an opponent's asset (expose spy, destroy surveillance, etc.).
        
        Args:
            character: Character targeting the asset
            target_asset: Asset to target
            zone_name: Zone where asset is located
            
        Returns:
            tuple: (success: bool, message: str, result: str)
            result: "exposed", "destroyed", "bypassed"
        """
        # Find asset
        asset_id = None
        asset_data = None
        
        for aid, adata in self.db.assets.items():
            if adata["asset"] == target_asset and adata["zone"] == zone_name:
                asset_id = aid
                asset_data = adata
                break
        
        if not asset_data:
            return (False, "Asset not found in that zone.", None)
        
        # Check if it's opponent's asset
        if asset_data["owner"].id == character.id:
            return (False, "You cannot target your own asset.", None)
        
        asset_type = asset_data["type"]
        
        if asset_type == "spy":
            # Expose spy - remove from play but not eliminated
            del self.db.assets[asset_id]
            return (True, f"Exposed {target_asset.name if hasattr(target_asset, 'name') else 'spy'}. They must withdraw and rebuild cover.", "exposed")
        
        elif asset_type == "informant":
            # Expose informant - destroyed
            del self.db.assets[asset_id]
            return (True, f"Exposed {target_asset.name if hasattr(target_asset, 'name') else 'informant'}. They are captured and executed.", "destroyed")
        
        elif asset_type == "surveillance":
            # Destroy surveillance device
            del self.db.assets[asset_id]
            return (True, f"Destroyed surveillance device. Information gathered is lost.", "destroyed")
        
        elif asset_type == "security":
            # Bypass security - create trait allowing bypass
            return (True, f"Created way to bypass {target_asset.name if hasattr(target_asset, 'name') else 'security'}. Asset is ineffective until breach is discovered.", "bypassed")
        
        return (False, "Cannot target this asset type.", None)
    
    def get_display(self, viewer):
        """
        Get a formatted display of the espionage conflict state.
        
        Args:
            viewer: Character viewing the conflict
            
        Returns:
            str: Formatted display
        """
        lines = []
        lines.append("|w" + "=" * 80 + "|n")
        lines.append("|wESPIONAGE CONFLICT|n".center(80))
        lines.append("|w" + "=" * 80 + "|n")
        
        # Show known zones
        lines.append("|wKnown Zones:|n")
        for zone_name, zone_data in self.db.zones.items():
            # Only show if not hidden or revealed to viewer
            if not zone_data["hidden"] or viewer.id in zone_data["revealed_to"]:
                zone_type = zone_data["type"]
                lines.append(f"  |y{zone_name}|n ({zone_type})")
                
                if zone_data.get("description"):
                    lines.append(f"    {zone_data['description']}")
                
                # Show connections
                adjacent = self.get_adjacent_zones(zone_name, viewer)
                if adjacent:
                    lines.append(f"    Connected to: {', '.join(adjacent)}")
                
                # Show assets
                assets = self.get_assets_in_zone(zone_name, viewer)
                if assets:
                    asset_names = [a.name if hasattr(a, 'name') else str(a) for a in assets]
                    lines.append(f"    Your assets: {', '.join(asset_names)}")
        
        lines.append("")
        
        # Show objective
        if viewer.id in self.db.objectives:
            lines.append(f"|wYour Objective:|n {self.db.objectives[viewer.id]}")
        
        lines.append("|w" + "=" * 80 + "|n")
        return "\n".join(lines)

