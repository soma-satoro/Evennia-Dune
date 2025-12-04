"""
Warfare Commands for Dune 2d20 System

Manages warfare conflicts with strategic zones and large-scale military assets.
Requires Architect-level play.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.search import search_object
from typeclasses.warfare import WarfareConflict


class CmdWarfare(MuxCommand):
    """
    Manage warfare conflicts - large-scale military combat with strategic zones.
    Requires Architect-level play (full access titles or roles).
    
    Usage:
        +warfare/start [=<objective>] - Start a new warfare conflict (staff)
        +warfare/join [=<objective>] - Join the current warfare conflict
        +warfare/status - Show current warfare conflict status
        +warfare/end - End the current conflict (staff or participant)
        +warfare/zone <name> [=<description>] - Add a strategic zone (staff)
        +warfare/objective <zones> - Set your objective zones
        +warfare/position <zone> - Set your commander position
        +warfare/add <asset> to <zone> - Add military asset to zone
        +warfare/move <asset> to <zone> [subtle|bold] [with me] - Move asset
        +warfare/attack <zone> with <asset> - Attack a zone with asset
        +warfare/rally <asset> - Rally a defeated asset back into battle
        +warfare/create <name>=<description> [in <zone>] - Create intangible asset
        +warfare/info <asset> [from <zone>] - Gather information using asset
        +warfare/obstacle <zone> - Overcome obstacle in zone
        +warfare/victory - Check if you've achieved your objective
    
    Asset Types:
        infantry - Squads/platoons of soldiers (close range only)
        vehicle - Ground vehicles (can transport infantry)
        aircraft - Ornithopters, etc. (Fast - move +1 zone)
        fortification - Walls, defenses (Immobile - cannot move)
    
    Examples:
        +warfare/start=Control the mining deposit
        +warfare/zone Mining Deposit=Rich spice mining site
        +warfare/zone Command Bunker=House Arcuri command center
        +warfare/objective Mining Deposit
        +warfare/add Tank to Mining Deposit
        +warfare/move Ornithopter to Mining Deposit
        +warfare/attack Command Bunker with Ornithopter
    """
    
    key = "+warfare"
    aliases = ["warfare", "war"]
    help_category = "Combat"
    
    def func(self):
        """Handle warfare commands"""
        
        # Get current warfare conflict
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
            self.caller.msg("|rThere is no active warfare conflict. Use |w+warfare/start|r to start one (staff).|n")
            return
        
        # Zone management (staff)
        if "zone" in self.switches:
            self._manage_zone(conflict)
            return
        
        # Set objective
        if "objective" in self.switches:
            self._set_objective(conflict)
            return
        
        # Set position
        if "position" in self.switches:
            self._set_position(conflict)
            return
        
        # Add asset
        if "add" in self.switches:
            self._add_asset(conflict)
            return
        
        # Move asset
        if "move" in self.switches:
            self._move_asset(conflict)
            return
        
        # Attack
        if "attack" in self.switches:
            self._attack(conflict)
            return
        
        # Rally asset
        if "rally" in self.switches:
            self._rally_asset(conflict)
            return
        
        # Create intangible asset
        if "create" in self.switches:
            self._create_intangible(conflict)
            return
        
        # Gather information
        if "info" in self.switches or "information" in self.switches:
            self._gather_info(conflict)
            return
        
        # Overcome obstacle
        if "obstacle" in self.switches:
            self._overcome_obstacle(conflict)
            return
        
        # Check victory
        if "victory" in self.switches:
            self._check_victory(conflict)
            return
        
        # Default: show status
        if conflict:
            self.caller.msg(conflict.get_display(self.caller))
        else:
            self._show_no_conflict()
    
    def _get_current_conflict(self):
        """Get the current warfare conflict"""
        room = self.caller.location
        if not room:
            return None
        
        # Search for warfare conflict objects
        from evennia import search_tag
        conflicts = search_tag("warfare", category="combat")
        
        for conflict in conflicts:
            if conflict.location == room and conflict.db.status == "active":
                return conflict
        
        return None
    
    def _start_conflict(self):
        """Start a new warfare conflict (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can start warfare conflicts.|n")
            return
        
        # Check if conflict already exists
        if self._get_current_conflict():
            self.caller.msg("|rThere is already an active warfare conflict.|n")
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
            WarfareConflict,
            key=f"Warfare Conflict in {room.name}",
            location=room
        )
        
        # Tag it
        conflict.tags.add("warfare", category="combat")
        
        # Add caller as first participant
        success, message = conflict.add_participant(self.caller, objective)
        if success:
            room.msg_contents(f"|w{self.caller.name} initiates a warfare conflict!|n")
            self.caller.msg("|gWarfare conflict started!|n")
            if objective:
                self.caller.msg(f"|yObjective: {objective}|n")
            self.caller.msg("|yUse |w+warfare/zone <name>|y to add strategic zones.|n")
        else:
            self.caller.msg(f"|r{message}|n")
            conflict.delete()
    
    def _join_conflict(self, conflict):
        """Join the current warfare conflict"""
        if not conflict:
            self.caller.msg("|rThere is no active warfare conflict to join.|n")
            return
        
        if self.caller in conflict.db.participants:
            self.caller.msg("|yYou are already in this conflict.|n")
            return
        
        # Parse objective
        objective = ""
        if "=" in self.args:
            objective = self.args.split("=", 1)[1].strip()
        
        success, message = conflict.add_participant(self.caller, objective)
        if success:
            room = self.caller.location
            if room:
                room.msg_contents(f"|w{self.caller.name} joins the warfare conflict!|n")
            self.caller.msg(f"|g{message}|n")
            if objective:
                self.caller.msg(f"|yYour objective: {objective}|n")
        else:
            self.caller.msg(f"|r{message}|n")
            self.caller.msg("|yWarfare requires full Architect access.|n")
            self.caller.msg("|cFull access titles:|n Major/Noble titles (Prince, Duke, Count, etc.)")
            self.caller.msg("|cFull access roles:|n Ruler, Marshal, Warmaster, etc.")
    
    def _show_no_conflict(self):
        """Show message when no conflict active"""
        self.caller.msg("|yThere is no active warfare conflict.|n")
        if self.caller.check_permstring("Builder"):
            self.caller.msg("Use |w+warfare/start|n to start one.")
    
    def _end_conflict(self, conflict):
        """End a warfare conflict"""
        if not conflict:
            self.caller.msg("|rThere is no active warfare conflict.|n")
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
            room.msg_contents(f"|wThe warfare conflict has ended.|n")
        
        conflict.delete()
        self.caller.msg("|gWarfare conflict ended.|n")
    
    def _manage_zone(self, conflict):
        """Manage zones (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can manage zones.|n")
            return
        
        if not self.args:
            # List zones
            if conflict.db.zones:
                self.caller.msg("|wStrategic Zones:|n")
                for zone_name, zone_data in conflict.db.zones.items():
                    self.caller.msg(f"  |y{zone_name}|n")
                    if zone_data.get("description"):
                        self.caller.msg(f"    {zone_data['description']}")
            else:
                self.caller.msg("|yNo zones defined.|n")
            return
        
        # Add zone
        if "=" in self.args:
            zone_name, description = self.args.split("=", 1)
            zone_name = zone_name.strip()
            description = description.strip()
        else:
            zone_name = self.args.strip()
            description = ""
        
        if conflict.add_zone(zone_name, description):
            self.caller.msg(f"|gAdded strategic zone '{zone_name}'.|n")
            if description:
                self.caller.msg(f"  Description: {description}")
        else:
            self.caller.msg(f"|rFailed to add zone.|n")
    
    def _set_objective(self, conflict):
        """Set objective zones"""
        if not self.args:
            self.caller.msg("Usage: +warfare/objective <zone1> [<zone2> ...]")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        objective_zones = self.args.split()
        
        # Update objective
        if self.caller.id in conflict.db.objectives:
            conflict.db.objectives[self.caller.id]["zones"] = objective_zones
        else:
            conflict.db.objectives[self.caller.id] = {
                "objective": "",
                "zones": objective_zones
            }
        
        self.caller.msg(f"|gObjective set: Control {', '.join(objective_zones)}|n")
    
    def _set_position(self, conflict):
        """Set commander position"""
        if not self.args:
            self.caller.msg("Usage: +warfare/position <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        zone_name = self.args.strip()
        
        if conflict.set_character_position(self.caller, zone_name):
            self.caller.msg(f"|gPosition set to {zone_name}.|n")
            self.caller.msg("|yBeing in same zone as assets: -1 Difficulty to actions|n")
            self.caller.msg("|yNot in same zone: Reduce Momentum cost to 1|n")
        else:
            self.caller.msg(f"|rZone '{zone_name}' does not exist.|n")
    
    def _add_asset(self, conflict):
        """Add a military asset to the conflict"""
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +warfare/add <asset> to <zone>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        parts = self.args.split(" to ", 1)
        asset_name = parts[0].strip()
        zone_name = parts[1].strip()
        
        # Find asset
        asset = self.caller.has_asset(asset_name)
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
            return
        
        # Determine asset type
        asset_type = "infantry"
        keywords = asset.get_keywords()
        keywords_lower = [k.lower() for k in keywords]
        
        if "aircraft" in keywords_lower or "ornithopter" in keywords_lower:
            asset_type = "aircraft"
        elif "vehicle" in keywords_lower or "tank" in keywords_lower or "groundcar" in keywords_lower:
            asset_type = "vehicle"
        elif "fortification" in keywords_lower or "fortress" in keywords_lower or "shield" in keywords_lower:
            asset_type = "fortification"
        
        # Add to conflict
        if conflict.add_asset(self.caller, asset, zone_name, asset_type):
            self.caller.msg(f"|gAdded {asset.name} ({asset_type}) to {zone_name} zone.|n")
        else:
            self.caller.msg(f"|rFailed to add {asset.name}.|n")
    
    def _move_asset(self, conflict):
        """Move an asset to a different zone"""
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +warfare/move <asset> to <zone> [subtle|bold] [with me]")
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
        move_character = "with me" in self.args or "with" in args and "me" in args
        
        # Find asset
        asset = self.caller.has_asset(asset_name)
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
            return
        
        # Check if asset is in conflict
        if asset.id not in conflict.db.assets:
            self.caller.msg(f"|r{asset.name} is not in this conflict. Use |w+warfare/add {asset_name} to <zone>|r first.|n")
            return
        
        # Move asset
        success, message, difficulty_mod, momentum_cost = conflict.move_asset(
            self.caller, asset, target_zone, subtle, bold, move_character
        )
        
        if success:
            self.caller.msg(f"|g{message}|n")
            if momentum_cost > 0:
                self.caller.msg(f"|yMomentum cost: {momentum_cost} (reduced from 2 if not in same zone)|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _attack(self, conflict):
        """Attack a zone with an asset"""
        if not self.args or " with " not in self.args:
            self.caller.msg("Usage: +warfare/attack <zone> with <asset>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        parts = self.args.split(" with ", 1)
        target_zone = parts[0].strip()
        asset_name = parts[1].strip()
        
        # Find asset
        asset = self.caller.has_asset(asset_name)
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
            return
        
        # Check if asset is in conflict
        if asset.id not in conflict.db.assets:
            self.caller.msg(f"|r{asset.name} is not in this conflict.|n")
            return
        
        # Check asset type for range
        asset_data = conflict.db.assets[asset.id]
        asset_type = asset_data["type"]
        
        # Infantry can only attack same zone
        if asset_type == "infantry":
            asset_zone = asset_data["zone"]
            if asset_zone != target_zone:
                self.caller.msg(f"|rInfantry can only attack assets in the same zone. {asset.name} is in {asset_zone}.|n")
                return
        
        # Calculate difficulty
        difficulty = conflict.get_attack_difficulty(self.caller, target_zone, asset)
        
        self.caller.msg(f"|wAttacking {target_zone} with {asset.name}...|n")
        self.caller.msg(f"|yDifficulty: {difficulty} (base 1 + {difficulty - 1} from additional allied assets in zone)|n")
        
        # Check character position
        char_pos = conflict.get_character_position(self.caller)
        asset_zone = asset_data["zone"]
        if char_pos == asset_zone:
            self.caller.msg("|yCharacter in same zone: -1 Difficulty (minimum 1)|n")
        
        # Prompt for roll
        self.caller.msg(f"|yUse |w+roll <drive> + battle vs {difficulty}|y to make the attack.|n")
        self.caller.msg("|yIf successful, it will contribute to defeating enemy assets.|n")
    
    def _rally_asset(self, conflict):
        """Rally a defeated asset back into battle"""
        if not self.args:
            self.caller.msg("Usage: +warfare/rally <asset>")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        # Find asset
        asset = self.caller.has_asset(self.args.strip())
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{self.args.strip()}'.|n")
            return
        
        if asset.id not in conflict.db.assets:
            self.caller.msg(f"|r{asset.name} is not in this conflict.|n")
            return
        
        asset_data = conflict.db.assets[asset.id]
        if not asset_data.get("defeated", False):
            self.caller.msg(f"|y{asset.name} is not defeated.|n")
            return
        
        if conflict.rally_asset(asset.id):
            new_quality = asset_data["quality"]
            self.caller.msg(f"|gRallied {asset.name} back into battle!|n")
            self.caller.msg(f"|yNew Quality: {new_quality} (reduced by 1 from casualties)|n")
        else:
            self.caller.msg(f"|rFailed to rally {asset.name}.|n")
    
    def _create_intangible(self, conflict):
        """Create an intangible asset"""
        if "=" not in self.args:
            self.caller.msg("Usage: +warfare/create <name>=<description> [in <zone>]")
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
        asset_type = "ploy"
        name_lower = name.lower()
        if "ambush" in name_lower:
            asset_type = "ambush"
        elif "intelligence" in name_lower or "intel" in name_lower:
            asset_type = "intelligence"
        
        if conflict.create_intangible_asset(self.caller, name, description, zone_name, asset_type):
            self.caller.msg(f"|gCreated intangible asset: {name} - {description}|n")
        else:
            self.caller.msg("|rFailed to create intangible asset.|n")
    
    def _gather_info(self, conflict):
        """Gather information using an allied asset"""
        if not self.args:
            self.caller.msg("Usage: +warfare/info <asset> [from <zone>]")
            return
        
        # Check if in conflict
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        # Parse
        parts = self.args.split()
        asset_name = parts[0]
        
        # Find asset
        asset = self.caller.has_asset(asset_name)
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
            return
        
        if asset.id not in conflict.db.assets:
            self.caller.msg(f"|r{asset.name} is not in this conflict.|n")
            return
        
        asset_data = conflict.db.assets[asset.id]
        asset_zone = asset_data["zone"]
        
        # Get adjacent zones
        adjacent = conflict.get_adjacent_zones(asset_zone) if hasattr(conflict, 'get_adjacent_zones') else []
        
        self.caller.msg(f"|wGathering information using {asset.name}...|n")
        self.caller.msg(f"|yAsset location: {asset_zone}|n")
        self.caller.msg(f"|yCan gather from: {asset_zone} or adjacent zones ({', '.join(adjacent) if adjacent else 'none'})|n")
        self.caller.msg("|yUse |w+roll <drive> + understand|y to process information.|n")
        self.caller.msg("|yUse |w+roll <drive> + battle|y to judge enemy strength.|n")
        self.caller.msg("|yUse |w+roll <drive> + communicate|y to decipher intercepted communications.|n")
    
    def _overcome_obstacle(self, conflict):
        """Overcome an obstacle in a zone"""
        if not self.args:
            self.caller.msg("Usage: +warfare/obstacle <zone>")
            return
        
        zone_name = self.args.strip()
        
        self.caller.msg(f"|yOvercoming obstacle in {zone_name}...|n")
        self.caller.msg("|yUse |w+roll <drive> + battle|y, |w+communicate|y, or |w+discipline|y to coordinate forces.|n")
        self.caller.msg("|yUse |w+roll <drive> + move|y to lead by example.|n")
        self.caller.msg("|yUse |w+roll <drive> + understand|y to find effective routes.|n")
    
    def _check_victory(self, conflict):
        """Check if objective has been achieved"""
        if self.caller not in conflict.db.participants:
            self.caller.msg("|rYou are not in this conflict.|n")
            return
        
        if conflict.check_objective(self.caller):
            self.caller.msg("|gVICTORY! You have achieved your objective!|n")
        else:
            self.caller.msg("|yYou have not yet achieved your objective.|n")
            
            if self.caller.id in conflict.db.objectives:
                obj = conflict.db.objectives[self.caller.id]
                obj_zones = obj.get("zones", [])
                if obj_zones:
                    self.caller.msg(f"|yObjective zones: {', '.join(obj_zones)}|n")
                    for zone_name in obj_zones:
                        controlled_by = conflict.db.zones[zone_name].get("controlled_by")
                        if controlled_by == self.caller.id:
                            self.caller.msg(f"  |g{zone_name}: Controlled|n")
                        else:
                            self.caller.msg(f"  |r{zone_name}: Not controlled|n")

