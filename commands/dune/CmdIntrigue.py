"""
Intrigue Commands for Dune 2d20 System

Manages intrigue conflicts with social zones, disposition tracking, and leverage-based influence.
Personal/Agent-level play.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.search import search_object
from typeclasses.intrigue import IntrigueConflict


class CmdIntrigue(MuxCommand):
    """
    Manage intrigue conflicts - social battles of status, wits, words, and secrets.
    Personal/Agent-level play (no Architect requirement).
    
    Usage:
        +intrigue/start [=<objective>] - Start a new intrigue conflict (staff)
        +intrigue/join [=<objective>] - Join the current intrigue conflict
        +intrigue/status - Show current intrigue conflict status
        +intrigue/end - End the current conflict (staff or participant)
        +intrigue/zone <name> [=<type>[:<disposition>]] - Add a zone (staff)
        +intrigue/disposition <zone> [toward <character>]=<disposition> - Set disposition (staff)
        +intrigue/desire <zone>=<desire> - Set zone's desire (staff)
        +intrigue/add <asset> to <zone> - Add asset to zone
        +intrigue/move <asset> to <zone> [subtle|bold] - Move asset (use leverage)
        +intrigue/create <name>=<description> [in <zone>] - Create intangible asset
        +intrigue/attack <zone> - Social attack on a zone
        +intrigue/target <asset> in <zone> - Target opponent's asset
        +intrigue/info disposition <zone> [toward <character>] - Learn disposition (spend Momentum)
        +intrigue/info desire <zone> - Discover zone's desire (extended task)
        +intrigue/obstacle <zone> - Overcome obstacle to access zone
    
    Dispositions:
        Allied (-2 Difficulty), Friendly (-1), Neutral (0), Unfriendly (+1), Opposed (+2)
    
    Asset Types:
        knowledge - Secrets, information (harder to challenge)
        rumor - Lies, false information (easier to create/destroy)
        valuable - Physical items, contracts, resources
    
    Examples:
        +intrigue/start=Get better spice deal
        +intrigue/zone Spice Merchant=person:Unfriendly
        +intrigue/zone Merchant Husband=person:Friendly
        +intrigue/create "Suspicious Rumor"=Rumor about merchant's activities
        +intrigue/move "Suspicious Rumor" to Merchant Husband subtle
        +intrigue/info desire Spice Merchant
        +intrigue/attack Spice Merchant
    """
    
    key = "+intrigue"
    aliases = ["intrigue"]
    help_category = "Combat"
    
    def func(self):
        """Handle intrigue commands"""
        
        # Get current intrigue conflict
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
            self.caller.msg("|rThere is no active intrigue conflict. Use |w+intrigue/start|r to start one (staff).|n")
            return
        
        # Zone management (staff)
        if "zone" in self.switches:
            self._manage_zone(conflict)
            return
        
        # Set disposition (staff)
        if "disposition" in self.switches or "disp" in self.switches:
            self._set_disposition(conflict)
            return
        
        # Set desire (staff)
        if "desire" in self.switches:
            self._set_desire(conflict)
            return
        
        # Add asset
        if "add" in self.switches:
            self._add_asset(conflict)
            return
        
        # Move asset
        if "move" in self.switches:
            self._move_asset(conflict)
            return
        
        # Create intangible asset
        if "create" in self.switches:
            self._create_intangible(conflict)
            return
        
        # Attack
        if "attack" in self.switches:
            self._attack(conflict)
            return
        
        # Target asset
        if "target" in self.switches:
            self._target_asset(conflict)
            return
        
        # Gather information
        if "info" in self.switches or "information" in self.switches:
            self._gather_info(conflict)
            return
        
        # Overcome obstacle
        if "obstacle" in self.switches:
            self._overcome_obstacle(conflict)
            return
        
        # Default: show status
        if conflict:
            self.caller.msg(conflict.get_display(self.caller))
        else:
            self._show_no_conflict()
    
    def _get_current_conflict(self):
        """Get the current intrigue conflict"""
        room = self.caller.location
        if not room:
            return None
        
        # Search for intrigue conflict objects
        from evennia import search_tag
        conflicts = search_tag("intrigue", category="combat")
        
        for conflict in conflicts:
            if conflict.location == room and conflict.db.status == "active":
                return conflict
        
        return None
    
    def _start_conflict(self):
        """Start a new intrigue conflict (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can start intrigue conflicts.|n")
            return
        
        # Check if conflict already exists
        if self._get_current_conflict():
            self.caller.msg("|rThere is already an active intrigue conflict.|n")
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
            IntrigueConflict,
            key=f"Intrigue Conflict in {room.name}",
            location=room
        )
        
        # Tag it
        conflict.tags.add("intrigue", category="combat")
        
        # Add caller as first participant
        conflict.add_participant(self.caller, objective)
        
        room.msg_contents(f"|w{self.caller.name} initiates an intrigue conflict!|n")
        self.caller.msg("|gIntrigue conflict started!|n")
        if objective:
            self.caller.msg(f"|yObjective: {objective}|n")
        self.caller.msg("|yUse |w+intrigue/zone <name>|y to add participants (people/groups).|n")
    
    def _join_conflict(self, conflict):
        """Join the current intrigue conflict"""
        if not conflict:
            self.caller.msg("|rThere is no active intrigue conflict to join.|n")
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
                room.msg_contents(f"|w{self.caller.name} joins the intrigue conflict!|n")
            self.caller.msg("|gYou join the intrigue conflict!|n")
            if objective:
                self.caller.msg(f"|yYour objective: {objective}|n")
        else:
            self.caller.msg("|rFailed to join conflict.|n")
    
    def _show_no_conflict(self):
        """Show message when no conflict active"""
        self.caller.msg("|yThere is no active intrigue conflict.|n")
        if self.caller.check_permstring("Builder"):
            self.caller.msg("Use |w+intrigue/start|n to start one.")
    
    def _end_conflict(self, conflict):
        """End an intrigue conflict"""
        if not conflict:
            self.caller.msg("|rThere is no active intrigue conflict.|n")
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
            room.msg_contents(f"|wThe intrigue conflict has ended.|n")
        
        conflict.delete()
        self.caller.msg("|gIntrigue conflict ended.|n")
    
    def _manage_zone(self, conflict):
        """Manage zones (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can manage zones.|n")
            return
        
        if not self.args:
            # List zones
            if conflict.db.zones:
                self.caller.msg("|wZones (Participants):|n")
                for zone_name, zone_data in conflict.db.zones.items():
                    zone_type = zone_data["type"]
                    disposition = zone_data.get("disposition", "Neutral")
                    self.caller.msg(f"  |y{zone_name}|n ({zone_type}) - {disposition}")
            else:
                self.caller.msg("|yNo zones defined.|n")
            return
        
        # Add zone
        # Format: name=type:disposition or name=type or name
        if "=" in self.args:
            parts = self.args.split("=", 1)
            zone_name = parts[0].strip()
            rest = parts[1].strip()
            
            if ":" in rest:
                zone_type, disposition = rest.split(":", 1)
                zone_type = zone_type.strip()
                disposition = disposition.strip()
            else:
                zone_type = rest
                disposition = "Neutral"
        else:
            zone_name = self.args.strip()
            zone_type = "person"
            disposition = "Neutral"
        
        if conflict.add_zone(zone_name, zone_type, disposition):
            self.caller.msg(f"|gAdded zone '{zone_name}' ({zone_type}) with disposition {disposition}.|n")
        else:
            self.caller.msg(f"|rFailed to add zone.|n")
    
    def _set_disposition(self, conflict):
        """Set disposition (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can set disposition.|n")
            return
        
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +intrigue/disposition <zone> [toward <character>]=<disposition>")
            self.caller.msg("Dispositions: Allied, Friendly, Neutral, Unfriendly, Opposed")
            return
        
        # Parse
        parts = self.args.split("=", 1)
        left = parts[0].strip()
        disposition = parts[1].strip()
        
        # Check for "toward <character>"
        target_character = None
        if " toward " in left:
            parts2 = left.split(" toward ", 1)
            zone_name = parts2[0].strip()
            char_name = parts2[1].strip()
            target_character = self.caller.search(char_name)
            if not target_character:
                return
        else:
            zone_name = left.strip()
        
        if target_character:
            if conflict.set_disposition(zone_name, target_character, disposition):
                self.caller.msg(f"|gSet {zone_name}'s disposition toward {target_character.name} to {disposition}.|n")
            else:
                self.caller.msg(f"|rFailed to set disposition.|n")
        else:
            # Set general disposition
            if zone_name in conflict.db.zones:
                conflict.db.zones[zone_name]["disposition"] = disposition
                self.caller.msg(f"|gSet {zone_name}'s general disposition to {disposition}.|n")
            else:
                self.caller.msg(f"|rZone '{zone_name}' not found.|n")
    
    def _set_desire(self, conflict):
        """Set zone's desire (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can set desires.|n")
            return
        
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +intrigue/desire <zone>=<desire>")
            return
        
        zone_name, desire = self.args.split("=", 1)
        zone_name = zone_name.strip()
        desire = desire.strip()
        
        if zone_name in conflict.db.zones:
            conflict.db.zones[zone_name]["desire"] = desire
            self.caller.msg(f"|gSet {zone_name}'s desire to: {desire}|n")
        else:
            self.caller.msg(f"|rZone '{zone_name}' not found.|n")
    
    def _add_asset(self, conflict):
        """Add an asset to the conflict"""
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +intrigue/add <asset> to <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        parts = self.args.split(" to ", 1)
        asset_name = parts[0].strip()
        zone_name = parts[1].strip()
        
        # Find asset (tangible or intangible)
        asset = self.caller.has_asset(asset_name)
        if not asset:
            # Check if it's an intangible asset
            if asset_name in conflict.db.intangible_assets:
                asset = asset_name
            else:
                self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
                return
        
        # Determine asset type
        asset_type = "knowledge"
        if isinstance(asset, str):
            # Intangible asset
            if asset in conflict.db.intangible_assets:
                asset_type = conflict.db.intangible_assets[asset].get("type", "knowledge")
        else:
            # Tangible asset
            keywords = asset.get_keywords()
            keywords_lower = [k.lower() for k in keywords]
            if "valuable" in keywords_lower or "contract" in keywords_lower:
                asset_type = "valuable"
        
        # Add to conflict
        if conflict.add_asset(self.caller, asset, zone_name, asset_type):
            self.caller.msg(f"|gAdded {asset_name} ({asset_type}) to {zone_name} zone.|n")
        else:
            self.caller.msg(f"|rFailed to add {asset_name}.|n")
    
    def _move_asset(self, conflict):
        """Move an asset to a different zone (use leverage)"""
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +intrigue/move <asset> to <zone> [subtle|bold]")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
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
            # Check if it's an intangible asset
            if asset_name in conflict.db.intangible_assets:
                asset = asset_name
            else:
                self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
                return
        
        # Move asset
        success, message, disposition_mod = conflict.move_asset(self.caller, asset, target_zone, subtle, bold)
        if success:
            self.caller.msg(f"|g{message}|n")
            if disposition_mod != 0:
                mod_str = f"+{disposition_mod}" if disposition_mod > 0 else str(disposition_mod)
                self.caller.msg(f"|yDisposition modifier: {mod_str} Difficulty|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _create_intangible(self, conflict):
        """Create an intangible asset"""
        if "=" not in self.args:
            self.caller.msg("Usage: +intrigue/create <name>=<description> [in <zone>] [type <type>]")
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
        asset_type = "knowledge"
        
        # Check for "in <zone>"
        if " in " in rest:
            parts2 = rest.split(" in ", 1)
            description = parts2[0].strip()
            rest2 = parts2[1].strip()
            
            # Check for "type <type>"
            if " type " in rest2:
                parts3 = rest2.split(" type ", 1)
                zone_name = parts3[0].strip()
                asset_type = parts3[1].strip()
            else:
                zone_name = rest2.strip()
        else:
            # Check for "type <type>"
            if " type " in rest:
                parts2 = rest.split(" type ", 1)
                description = parts2[0].strip()
                asset_type = parts2[1].strip()
            else:
                description = rest
        
        if conflict.create_intangible_asset(self.caller, name, description, zone_name, asset_type):
            self.caller.msg(f"|gCreated intangible asset: {name} ({asset_type}) - {description}|n")
        else:
            self.caller.msg("|rFailed to create intangible asset.|n")
    
    def _attack(self, conflict):
        """Social attack on a zone"""
        if not self.args:
            self.caller.msg("Usage: +intrigue/attack <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        target_zone = self.args.strip()
        
        if target_zone not in conflict.db.zones:
            self.caller.msg(f"|rZone '{target_zone}' not found.|n")
            return
        
        # Calculate difficulty
        difficulty = conflict.get_attack_difficulty(self.caller, target_zone)
        disposition = conflict.get_disposition(target_zone, self.caller)
        
        self.caller.msg(f"|wSocial attack on {target_zone}...|n")
        self.caller.msg(f"|yDisposition: {disposition} (modifier: {conflict.get_disposition_modifier(target_zone, self.caller)})|n")
        self.caller.msg(f"|yDifficulty: {difficulty}|n")
        
        # Check if target is a character (for extended task)
        # For now, assume non-minor characters need extended task
        self.caller.msg("|yUse |w+roll <drive> + communicate vs {difficulty}|y to make the attack.|n".format(difficulty=difficulty))
        self.caller.msg("|yOpponent may use |w+discipline|y or |w+communicate|y to resist.|n")
        self.caller.msg("|yIf you fail, target may seek revenge (possibly a duel challenge).|n")
        self.caller.msg("|yIf successful against non-minor character, extended task (requirement = target's Discipline).|n")
    
    def _target_asset(self, conflict):
        """Target an opponent's asset"""
        if not self.args or " in " not in self.args:
            self.caller.msg("Usage: +intrigue/target <asset> in <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        parts = self.args.split(" in ", 1)
        asset_name = parts[0].strip()
        zone_name = parts[1].strip()
        
        # Target the asset
        success, message, result = conflict.target_asset(self.caller, asset_name, zone_name)
        if success:
            self.caller.msg(f"|g{message}|n")
            self.caller.msg("|yUse appropriate skill test to challenge/question the asset.|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _gather_info(self, conflict):
        """Gather information (disposition or desire)"""
        if not self.args:
            self.caller.msg("Usage: +intrigue/info disposition <zone> [toward <character>]")
            self.caller.msg("       +intrigue/info desire <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        args = self.args.split()
        
        if args[0].lower() == "disposition":
            # Learn disposition (spend Momentum)
            if len(args) < 2:
                self.caller.msg("Usage: +intrigue/info disposition <zone> [toward <character>]")
                return
            
            zone_name = args[1]
            target_character = None
            
            if "toward" in args and args.index("toward") < len(args) - 1:
                toward_index = args.index("toward")
                char_name = args[toward_index + 1]
                target_character = self.caller.search(char_name)
                if not target_character:
                    return
            
            if zone_name not in conflict.db.zones:
                self.caller.msg(f"|rZone '{zone_name}' not found.|n")
                return
            
            disposition = conflict.get_disposition(zone_name, target_character if target_character else self.caller)
            self.caller.msg(f"|wLearning {zone_name}'s disposition...|n")
            self.caller.msg("|ySpend 1 Momentum to learn disposition.|n")
            self.caller.msg(f"|yCurrent disposition: {disposition}|n")
        
        elif args[0].lower() == "desire":
            # Discover desire (extended task)
            if len(args) < 2:
                self.caller.msg("Usage: +intrigue/info desire <zone>")
                return
            
            zone_name = args[1]
            
            if zone_name not in conflict.db.zones:
                self.caller.msg(f"|rZone '{zone_name}' not found.|n")
                return
            
            # Check if already known
            if self.caller.id in conflict.db.zones[zone_name].get("desire_known", []):
                desire = conflict.db.zones[zone_name].get("desire", "")
                self.caller.msg(f"|y{zone_name}'s desire: {desire}|n")
                return
            
            # Get target's Discipline (for requirement)
            # For now, assume Discipline 3 as default
            requirement = 3  # Would normally be target's Discipline skill
            
            # Set up extended task
            task = conflict.set_desire_task(zone_name, self.caller, requirement)
            
            # Calculate points per success (Understand - 2)
            understand = self.caller.get_skill("understand") if hasattr(self.caller, 'get_skill') else 0
            points_per_success = max(0, understand - 2)
            
            self.caller.msg(f"|wDiscovering {zone_name}'s desire...|n")
            self.caller.msg(f"|yRequirement: {requirement} points|n")
            self.caller.msg(f"|yPoints per success: {understand} - 2 = {points_per_success}|n")
            self.caller.msg(f"|yCurrent progress: {task['points']}/{task['requirement']}|n")
            self.caller.msg("|yUse |w+roll <drive> + understand|y to gather information.|n")
            self.caller.msg("|ySpend 2 Momentum to add +1 to points scored.|n")
        
        else:
            self.caller.msg("Usage: +intrigue/info disposition <zone> | +intrigue/info desire <zone>")
    
    def _overcome_obstacle(self, conflict):
        """Overcome an obstacle to access a zone"""
        if not self.args:
            self.caller.msg("Usage: +intrigue/obstacle <zone>")
            return
        
        zone_name = self.args.strip()
        
        self.caller.msg(f"|yOvercoming obstacle to access {zone_name}...|n")
        self.caller.msg("|yUse |w+roll <drive> + communicate|y or |w+understand|y to establish access.|n")
        self.caller.msg("|yUse |w+roll <drive> + battle|y, |w+move|y, or |w+discipline|y for tests of worth.|n")

