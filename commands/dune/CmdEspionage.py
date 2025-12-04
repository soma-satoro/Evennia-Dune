"""
Espionage Commands for Dune 2d20 System

Manages espionage conflicts with abstract zones representing people, groups, and places.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.search import search_object
from typeclasses.espionage import EspionageConflict


class CmdEspionage(MuxCommand):
    """
    Manage espionage conflicts - information gathering with abstract zones.
    
    Usage:
        +espionage/start [=<objective>] - Start a new espionage conflict (staff)
        +espionage/join [=<objective>] - Join the current espionage conflict
        +espionage/status - Show current espionage conflict status
        +espionage/end - End the current conflict (staff or participant)
        +espionage/zone <name>=<type>[:<description>] - Add a zone (staff)
        +espionage/connect <zone1> to <zone2> [=<connection type>] - Connect zones (staff)
        +espionage/reveal <zone> - Reveal a hidden zone (staff)
        +espionage/move <asset> to <zone> [subtle|bold] - Move asset to zone
        +espionage/add <asset> to <zone> - Add asset to zone
        +espionage/info [from <zone>] - Gather information
        +espionage/target <asset> in <zone> - Target opponent's asset
        +espionage/create <name>=<description> [in <zone>] - Create intangible asset
        +espionage/obstacle <zone> - Overcome obstacle to access zone
        +espionage/attack <target> - Attempt assassination (rare)
    
    Zone Types:
        person - Individual person
        group - Organization or faction
        place - Physical location
        event - Time-sensitive gathering
    
    Asset Types:
        spy - Trained operative (can move, gather info)
        informant - Less capable but well-placed (can move, gather info)
        surveillance - Device that gathers info (cannot move once placed)
        security - Guards, locks, etc. (blocks entry, increases difficulty)
    
    Examples:
        +espionage/start=Investigate spice smuggling
        +espionage/zone Arrakis=place:The desert planet
        +espionage/zone Fremen=group:Desert-dwelling people
        +espionage/connect Arrakis to Fremen=Lives On
        +espionage/add Spy to Fremen
        +espionage/move Spy to Arrakis subtle
        +espionage/info from Fremen
    """
    
    key = "+espionage"
    aliases = ["espionage", "spy"]
    help_category = "Combat"
    
    def func(self):
        """Handle espionage commands"""
        
        # Get current espionage conflict
        conflict = self._get_current_conflict()
        
        # Start conflict (staff)
        if "start" in self.switches:
            self._start_conflict()
            return
        
        # Join conflict
        if "join" in self.switches:
            self._join_conflict(conflict)
            return
        
        # Show status
        if "status" in self.switches or not self.switches:
            if conflict:
                self.caller.msg(conflict.get_display(self.caller))
            else:
                self._show_no_conflict()
            return
        
        # End conflict
        if "end" in self.switches:
            self._end_conflict(conflict)
            return
        
        # Need an active conflict for remaining commands
        if not conflict:
            self.caller.msg("|rThere is no active espionage conflict. Use |w+espionage/start|r to start one (staff).|n")
            return
        
        # Zone management (staff)
        if "zone" in self.switches:
            self._manage_zone(conflict)
            return
        
        # Connect zones (staff)
        if "connect" in self.switches:
            self._connect_zones(conflict)
            return
        
        # Reveal zone (staff)
        if "reveal" in self.switches:
            self._reveal_zone(conflict)
            return
        
        # Move asset
        if "move" in self.switches:
            self._move_asset(conflict)
            return
        
        # Add asset
        if "add" in self.switches:
            self._add_asset(conflict)
            return
        
        # Gather information
        if "info" in self.switches or "information" in self.switches:
            self._gather_info(conflict)
            return
        
        # Target asset
        if "target" in self.switches:
            self._target_asset(conflict)
            return
        
        # Create intangible asset
        if "create" in self.switches:
            self._create_intangible(conflict)
            return
        
        # Overcome obstacle
        if "obstacle" in self.switches:
            self._overcome_obstacle(conflict)
            return
        
        # Attack (assassination)
        if "attack" in self.switches:
            self._attack(conflict)
            return
        
        # Default: show status
        if conflict:
            self.caller.msg(conflict.get_display(self.caller))
        else:
            self._show_no_conflict()
    
    def _get_current_conflict(self):
        """Get the current espionage conflict"""
        room = self.caller.location
        if not room:
            return None
        
        # Search for espionage conflict objects
        from evennia import search_tag
        conflicts = search_tag("espionage", category="combat")
        
        for conflict in conflicts:
            if conflict.location == room and conflict.db.status == "active":
                return conflict
        
        return None
    
    def _start_conflict(self):
        """Start a new espionage conflict (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can start espionage conflicts.|n")
            return
        
        # Check if conflict already exists
        if self._get_current_conflict():
            self.caller.msg("|rThere is already an active espionage conflict.|n")
            return
        
        room = self.caller.location
        if not room:
            self.caller.msg("|rYou must be in a room to start a conflict.|n")
            return
        
        # Parse objective
        objective = ""
        if "=" in self.args:
            objective = self.args.split("=", 1)[1].strip()
        
        # Create conflict object
        from evennia import create_object
        conflict = create_object(
            EspionageConflict,
            key=f"Espionage Conflict in {room.name}",
            location=room
        )
        
        # Tag it
        conflict.tags.add("espionage", category="combat")
        
        # Add caller as first participant
        conflict.add_participant(self.caller, objective)
        
        room.msg_contents(f"|w{self.caller.name} initiates an espionage conflict!|n")
        self.caller.msg("|gEspionage conflict started!|n")
        if objective:
            self.caller.msg(f"|yObjective: {objective}|n")
        self.caller.msg("|yUse |w+espionage/zone <name>=<type>|y to add zones.|n")
    
    def _join_conflict(self, conflict):
        """Join the current espionage conflict"""
        if not conflict:
            self.caller.msg("|rThere is no active espionage conflict to join.|n")
            return
        
        if self.caller in conflict.db.participants:
            self.caller.msg("|yYou are already in this conflict.|n")
            return
        
        # Parse objective
        objective = ""
        if "=" in self.args:
            objective = self.args.split("=", 1)[1].strip()
        
        if conflict.add_participant(self.caller, objective):
            room = self.caller.location
            if room:
                room.msg_contents(f"|w{self.caller.name} joins the espionage conflict!|n")
            self.caller.msg("|gYou join the espionage conflict!|n")
            if objective:
                self.caller.msg(f"|yYour objective: {objective}|n")
        else:
            self.caller.msg("|rFailed to join conflict.|n")
    
    def _show_no_conflict(self):
        """Show message when no conflict active"""
        self.caller.msg("|yThere is no active espionage conflict.|n")
        if self.caller.check_permstring("Builder"):
            self.caller.msg("Use |w+espionage/start|n to start one.")
    
    def _end_conflict(self, conflict):
        """End an espionage conflict"""
        if not conflict:
            self.caller.msg("|rThere is no active espionage conflict.|n")
            return
        
        # Check permissions
        is_participant = self.caller in conflict.db.participants
        is_staff = self.caller.check_permstring("Builder")
        
        if not is_participant and not is_staff:
            self.caller.msg("|rYou can only end conflicts you are participating in.|n")
            return
        
        # Delete the conflict
        room = conflict.location
        if room:
            room.msg_contents(f"|wThe espionage conflict has ended.|n")
        
        conflict.delete()
        self.caller.msg("|gEspionage conflict ended.|n")
    
    def _manage_zone(self, conflict):
        """Manage zones (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can manage zones.|n")
            return
        
        if not self.args:
            # List zones
            if conflict.db.zones:
                self.caller.msg("|wZones:|n")
                for zone_name, zone_data in conflict.db.zones.items():
                    zone_type = zone_data["type"]
                    hidden = "|r[Hidden]|n" if zone_data["hidden"] else ""
                    self.caller.msg(f"  |y{zone_name}|n ({zone_type}) {hidden}")
            else:
                self.caller.msg("|yNo zones defined.|n")
            return
        
        # Add zone
        if "=" in self.args:
            parts = self.args.split("=", 1)
            zone_name = parts[0].strip()
            rest = parts[1].strip()
            
            # Parse type and description
            if ":" in rest:
                zone_type, description = rest.split(":", 1)
                zone_type = zone_type.strip()
                description = description.strip()
            else:
                zone_type = rest
                description = ""
        else:
            zone_name = self.args.strip()
            zone_type = "place"
            description = ""
        
        if conflict.add_zone(zone_name, zone_type, description):
            self.caller.msg(f"|gAdded zone '{zone_name}' ({zone_type}).|n")
            if description:
                self.caller.msg(f"  Description: {description}")
        else:
            self.caller.msg(f"|rFailed to add zone.|n")
    
    def _connect_zones(self, conflict):
        """Connect two zones (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can connect zones.|n")
            return
        
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +espionage/connect <zone1> to <zone2> [=<connection type>]")
            return
        
        parts = self.args.split(" to ", 1)
        zone1 = parts[0].strip()
        rest = parts[1].strip()
        
        if "=" in rest:
            zone2, conn_type = rest.split("=", 1)
            zone2 = zone2.strip()
            conn_type = conn_type.strip()
        else:
            zone2 = rest.strip()
            conn_type = ""
        
        if conflict.add_connection(zone1, zone2, conn_type):
            self.caller.msg(f"|gConnected {zone1} to {zone2}.|n")
            if conn_type:
                self.caller.msg(f"  Connection type: {conn_type}")
        else:
            self.caller.msg(f"|rFailed to connect zones.|n")
    
    def _reveal_zone(self, conflict):
        """Reveal a hidden zone (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can reveal zones.|n")
            return
        
        if not self.args:
            self.caller.msg("Usage: +espionage/reveal <zone>")
            return
        
        zone_name = self.args.strip()
        
        # Reveal to all participants
        for participant in conflict.db.participants:
            if conflict.reveal_zone(zone_name, participant):
                participant.msg(f"|yZone '{zone_name}' has been revealed to you!|n")
        
        self.caller.msg(f"|gRevealed zone '{zone_name}' to all participants.|n")
    
    def _move_asset(self, conflict):
        """Move an asset to a different zone"""
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +espionage/move <asset> to <zone> [subtle|bold]")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict. Use |w+espionage/join|r first.|n")
            return
        
        parts = self.args.split(" to ", 1)
        asset_name = parts[0].strip()
        rest = parts[1].strip()
        
        args = rest.split()
        target_zone = args[0]
        subtle = "subtle" in args
        bold = "bold" in args
        
        # Find asset
        asset = self.caller.has_asset(asset_name)
        if not asset:
            # Check if caller is acting as spy
            if asset_name.lower() == "self" or asset_name.lower() == self.caller.name.lower():
                asset = self.caller
            else:
                self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
                return
        
        # Move asset
        success, message, difficulty_mod = conflict.move_asset(self.caller, asset, target_zone, subtle, bold)
        if success:
            self.caller.msg(f"|g{message}|n")
            if difficulty_mod > 0:
                self.caller.msg(f"|yDifficulty modifier: +{difficulty_mod} (from security measures)|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _add_asset(self, conflict):
        """Add an asset to the conflict"""
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +espionage/add <asset> to <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        parts = self.args.split(" to ", 1)
        asset_name = parts[0].strip()
        zone_name = parts[1].strip()
        
        # Find asset or check if character is acting as spy
        asset = self.caller.has_asset(asset_name)
        if not asset:
            # Check if caller is acting as spy
            if asset_name.lower() == "self" or asset_name.lower() == self.caller.name.lower():
                asset = self.caller
                spy_quality = conflict.get_character_spy_quality(self.caller)
                self.caller.msg(f"|yActing as spy (Quality {spy_quality} = lowest of Understand/Move - 4).|n")
            else:
                self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
                self.caller.msg("|yUse 'self' or your name to act as a spy directly.|n")
                return
        
        # Determine asset type
        asset_type = "spy"
        keywords = asset.get_keywords()
        keywords_lower = [k.lower() for k in keywords]
        
        if "surveillance" in keywords_lower or "device" in keywords_lower:
            asset_type = "surveillance"
        elif "informant" in keywords_lower:
            asset_type = "informant"
        elif "security" in keywords_lower or "guard" in keywords_lower:
            asset_type = "security"
        
        # Add to conflict
        if conflict.add_asset(self.caller, asset, zone_name, asset_type):
            self.caller.msg(f"|gAdded {asset.name} to {zone_name} zone.|n")
        else:
            self.caller.msg(f"|rFailed to add {asset.name}. Zone may be hidden.|n")
    
    def _gather_info(self, conflict):
        """Gather information from a zone"""
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        # Parse zone
        zone_name = None
        if " from " in self.args:
            parts = self.args.split(" from ", 1)
            zone_name = parts[1].strip()
        elif self.args:
            zone_name = self.args.strip()
        else:
            # Default to zones with information assets
            info_zones = []
            for zone_name_check, zone_data in conflict.db.zones.items():
                if not zone_data["hidden"] or self.caller.id in zone_data["revealed_to"]:
                    info_assets = conflict.get_information_assets(zone_name_check, self.caller)
                    if info_assets:
                        info_zones.append(zone_name_check)
            
            if info_zones:
                self.caller.msg(f"|yZones with information assets: {', '.join(info_zones)}|n")
                self.caller.msg("Usage: +espionage/info [from <zone>]")
            else:
                self.caller.msg("|rYou have no information assets in any zone.|n")
            return
        
        # Check for information assets
        info_assets = conflict.get_information_assets(zone_name, self.caller)
        if not info_assets:
            self.caller.msg(f"|rYou have no information assets (spy, informant, or surveillance) in {zone_name}.|n")
            return
        
        # Calculate difficulty
        difficulty = conflict.get_information_difficulty(zone_name, self.caller)
        
        self.caller.msg(f"|wGathering information from {zone_name}...|n")
        self.caller.msg(f"|yInformation assets: {', '.join([a.name if hasattr(a, 'name') else str(a) for a in info_assets])}|n")
        self.caller.msg(f"|yDifficulty: {difficulty + 1} (base 1 + {difficulty} from security measures)|n")
        self.caller.msg("|yUse |w+roll <drive> + understand vs {difficulty}|y to gather information.|n".format(difficulty=difficulty + 1))
        self.caller.msg("|yYou can spend Momentum to ask additional questions.|n")
    
    def _target_asset(self, conflict):
        """Target an opponent's asset"""
        if not self.args or " in " not in self.args:
            self.caller.msg("Usage: +espionage/target <asset> in <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        parts = self.args.split(" in ", 1)
        asset_name = parts[0].strip()
        zone_name = parts[1].strip()
        
        # Find opponent's asset
        target_asset = None
        for asset_id, asset_data in conflict.db.assets.items():
            if asset_data["zone"] == zone_name and asset_data["owner"].id != self.caller.id:
                asset_obj = asset_data["asset"]
                if hasattr(asset_obj, 'name') and asset_obj.name.lower() == asset_name.lower():
                    target_asset = asset_obj
                    break
        
        if not target_asset:
            self.caller.msg(f"|rNo opponent asset named '{asset_name}' found in {zone_name}.|n")
            return
        
        # Target the asset
        success, message, result = conflict.target_asset(self.caller, target_asset, zone_name)
        if success:
            self.caller.msg(f"|g{message}|n")
            if result == "exposed":
                self.caller.msg("|yThe spy must withdraw and rebuild cover.|n")
            elif result == "destroyed":
                self.caller.msg("|yThe asset is eliminated.|n")
            elif result == "bypassed":
                self.caller.msg("|yYou can now bypass this security until the breach is discovered.|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _create_intangible(self, conflict):
        """Create an intangible asset"""
        if "=" not in self.args:
            self.caller.msg("Usage: +espionage/create <name>=<description> [in <zone>]")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        # Parse
        parts = self.args.split("=", 1)
        name = parts[0].strip()
        rest = parts[1].strip()
        
        zone_name = None
        if " in " in rest:
            parts2 = rest.split(" in ", 1)
            description = parts2[0].strip()
            zone_name = parts2[1].strip()
        else:
            description = rest
        
        # Determine type
        asset_type = "rumor"
        name_lower = name.lower()
        if "procedure" in name_lower or "patrol" in name_lower:
            asset_type = "procedure"
        elif "propaganda" in name_lower:
            asset_type = "propaganda"
        elif "leak" in name_lower:
            asset_type = "leak"
        
        if conflict.create_intangible_asset(self.caller, name, description, zone_name, asset_type):
            self.caller.msg(f"|gCreated intangible asset: {name} - {description}|n")
        else:
            self.caller.msg("|rFailed to create intangible asset.|n")
    
    def _overcome_obstacle(self, conflict):
        """Overcome an obstacle to access a zone"""
        if not self.args:
            self.caller.msg("Usage: +espionage/obstacle <zone>")
            return
        
        zone_name = self.args.strip()
        
        self.caller.msg(f"|yOvercoming obstacle to access {zone_name}...|n")
        self.caller.msg("|yUse |w+roll <drive> + communicate|y to establish legitimate access.|n")
        self.caller.msg("|yUse |w+roll <drive> + understand|y to find a way in.|n")
        self.caller.msg("|yUse |w+roll <drive> + battle|y, |w+move|y, or |w+discipline|y for tests of worth.|n")
    
    def _attack(self, conflict):
        """Attempt assassination (rare in espionage)"""
        if not self.args:
            self.caller.msg("Usage: +espionage/attack <target>")
            return
        
        self.caller.msg("|rAssassination attempts are rare in espionage conflicts.|n")
        self.caller.msg("|yUse |w+roll <drive> + move vs <difficulty>|y to get close enough.|n")
        self.caller.msg("|yOpponent may use |w+discipline|y or |w+understand|y to resist.|n")
        self.caller.msg("|yIf you fail, the scene may become a skirmish or duel.|n")

