"""
Skirmish Commands for Dune 2d20 System

Manages skirmish combat with environment-based zones and multi-combatant resolution.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.search import search_object
from typeclasses.skirmishes import Skirmish


class CmdSkirmish(MuxCommand):
    """
    Manage skirmishes - multi-combatant combat with environment-based zones.
    
    Usage:
        +skirmish/start - Start a new skirmish (staff)
        +skirmish/join - Join the current skirmish
        +skirmish/status - Show current skirmish status
        +skirmish/end - End the current skirmish (staff or participant)
        +skirmish/zone <name> [=<description>] - Add a zone (staff)
        +skirmish/zone <name>/trait <trait> - Add trait to zone (staff)
        +skirmish/move <zone> [subtle|bold] - Move to a zone
        +skirmish/add <asset> - Add an asset to the skirmish
        +skirmish/aim <asset> at <zone> - Aim ranged weapon at zone
        +skirmish/attack <target> [with <asset>] - Attack a target
        +skirmish/defend - Prepare defensive stance
        +skirmish/create <name>=<description> - Create an intangible asset
        +skirmish/obstacle - Overcome an obstacle in current zone
        +skirmish/info - Gather information about opponents or environment
    
    Zones:
        Zones represent areas of the environment. Multiple characters can be in the same zone.
        Characters in the same zone can attack each other with melee weapons.
        Ranged weapons can attack adjacent zones at +1 Difficulty.
    
    Movement:
        - Normal: Move to adjacent zone
        - Spend 2 Momentum: Move additional zone OR allow ally to move
        - Subtle: Stealthy movement, may keep initiative
        - Bold: Dramatic movement, may affect enemies
    
    Examples:
        +skirmish/start
        +skirmish/zone entrance=Near the main road
        +skirmish/zone fire_escape=Area with ladder
        +skirmish/move fire_escape
        +skirmish/add Crysknife
        +skirmish/attack Thug with Crysknife
        +skirmish/aim Maula Pistol at entrance
    """
    
    key = "+skirmish"
    aliases = ["skirmish"]
    help_category = "Combat"
    
    def func(self):
        """Handle skirmish commands"""
        
        # Get current skirmish
        skirmish = self._get_current_skirmish()
        
        # Start skirmish (staff)
        if "start" in self.switches:
            self._start_skirmish()
            return
        
        # Join skirmish
        if "join" in self.switches:
            self._join_skirmish(skirmish)
            return
        
        # Show status
        if "status" in self.switches or not self.switches:
            if skirmish:
                self.caller.msg(skirmish.get_display(self.caller))
            else:
                self._show_no_skirmish()
            return
        
        # End skirmish
        if "end" in self.switches:
            self._end_skirmish(skirmish)
            return
        
        # Need an active skirmish for remaining commands
        if not skirmish:
            self.caller.msg("|rThere is no active skirmish. Use |w+skirmish/start|r to start one (staff).|n")
            return
        
        # Zone management (staff)
        if "zone" in self.switches:
            self._manage_zone(skirmish)
            return
        
        # Move
        if "move" in self.switches:
            self._move_character(skirmish)
            return
        
        # Add asset
        if "add" in self.switches:
            self._add_asset(skirmish)
            return
        
        # Aim ranged weapon
        if "aim" in self.switches:
            self._aim_weapon(skirmish)
            return
        
        # Attack
        if "attack" in self.switches:
            self._attack(skirmish)
            return
        
        # Defend
        if "defend" in self.switches:
            self._defend(skirmish)
            return
        
        # Create intangible asset
        if "create" in self.switches:
            self._create_intangible(skirmish)
            return
        
        # Overcome obstacle
        if "obstacle" in self.switches:
            self._overcome_obstacle(skirmish)
            return
        
        # Gather information
        if "info" in self.switches or "information" in self.switches:
            self._gather_info(skirmish)
            return
        
        # Default: show status
        if skirmish:
            self.caller.msg(skirmish.get_display(self.caller))
        else:
            self._show_no_skirmish()
    
    def _get_current_skirmish(self):
        """Get the current skirmish in the room"""
        room = self.caller.location
        if not room:
            return None
        
        # Search for skirmish objects in the room
        from evennia import search_tag
        skirmishes = search_tag("skirmish", category="combat")
        
        for skirmish in skirmishes:
            if skirmish.location == room and skirmish.db.status == "active":
                return skirmish
        
        return None
    
    def _start_skirmish(self):
        """Start a new skirmish (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can start skirmishes.|n")
            return
        
        # Check if skirmish already exists
        if self._get_current_skirmish():
            self.caller.msg("|rThere is already an active skirmish in this room.|n")
            return
        
        room = self.caller.location
        if not room:
            self.caller.msg("|rYou must be in a room to start a skirmish.|n")
            return
        
        # Create skirmish object
        from evennia import create_object
        skirmish = create_object(
            Skirmish,
            key=f"Skirmish in {room.name}",
            location=room
        )
        
        # Tag it
        skirmish.tags.add("skirmish", category="combat")
        
        # Add caller as first combatant
        skirmish.add_combatant(self.caller)
        
        room.msg_contents(f"|w{self.caller.name} starts a skirmish!|n")
        self.caller.msg("|gSkirmish started! Use |w+skirmish/zone <name>|g to add zones.|n")
        self.caller.msg("|yOthers can join with |w+skirmish/join|y|n")
    
    def _join_skirmish(self, skirmish):
        """Join the current skirmish"""
        if not skirmish:
            self.caller.msg("|rThere is no active skirmish to join.|n")
            return
        
        if self.caller in skirmish.db.combatants:
            self.caller.msg("|yYou are already in this skirmish.|n")
            return
        
        if skirmish.add_combatant(self.caller):
            room = self.caller.location
            if room:
                room.msg_contents(f"|w{self.caller.name} joins the skirmish!|n")
            self.caller.msg("|gYou join the skirmish!|n")
        else:
            self.caller.msg("|rFailed to join skirmish.|n")
    
    def _show_no_skirmish(self):
        """Show message when no skirmish active"""
        self.caller.msg("|yThere is no active skirmish.|n")
        if self.caller.check_permstring("Builder"):
            self.caller.msg("Use |w+skirmish/start|n to start one.")
    
    def _end_skirmish(self, skirmish):
        """End a skirmish"""
        if not skirmish:
            self.caller.msg("|rThere is no active skirmish.|n")
            return
        
        # Check permissions
        is_participant = self.caller in skirmish.db.combatants
        is_staff = self.caller.check_permstring("Builder")
        
        if not is_participant and not is_staff:
            self.caller.msg("|rYou can only end skirmishes you are participating in.|n")
            return
        
        # Delete the skirmish
        room = skirmish.location
        if room:
            room.msg_contents(f"|wThe skirmish has ended.|n")
        
        skirmish.delete()
        self.caller.msg("|gSkirmish ended.|n")
    
    def _manage_zone(self, skirmish):
        """Manage zones (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can manage zones.|n")
            return
        
        if not self.args:
            # List zones
            if skirmish.db.zones:
                self.caller.msg("|wZones:|n")
                for zone_name, zone_data in skirmish.db.zones.items():
                    chars = skirmish.get_characters_in_zone(zone_name)
                    self.caller.msg(f"  |y{zone_name}:|n {len(chars)} characters")
                    if zone_data.get("traits"):
                        self.caller.msg(f"    Traits: {', '.join(zone_data['traits'])}")
            else:
                self.caller.msg("|yNo zones defined. Use |w+skirmish/zone <name> [=<description>]|y to add one.|n")
            return
        
        # Parse zone command
        if "/trait" in self.args:
            # Add trait to zone
            parts = self.args.split("/trait", 1)
            zone_name = parts[0].strip()
            trait = parts[1].strip() if len(parts) > 1 else ""
            
            if zone_name not in skirmish.db.zones:
                self.caller.msg(f"|rZone '{zone_name}' does not exist.|n")
                return
            
            if not trait:
                self.caller.msg("Usage: +skirmish/zone <name>/trait <trait>")
                return
            
            if trait not in skirmish.db.zones[zone_name]["traits"]:
                skirmish.db.zones[zone_name]["traits"].append(trait)
                self.caller.msg(f"|gAdded trait '{trait}' to zone '{zone_name}'.|n")
            else:
                self.caller.msg(f"|yZone '{zone_name}' already has trait '{trait}'.|n")
        else:
            # Add zone
            if "=" in self.args:
                zone_name, description = self.args.split("=", 1)
                zone_name = zone_name.strip()
                description = description.strip()
            else:
                zone_name = self.args.strip()
                description = ""
            
            if skirmish.add_zone(zone_name, description):
                self.caller.msg(f"|gAdded zone '{zone_name}'.|n")
                if description:
                    self.caller.msg(f"  Description: {description}")
            else:
                self.caller.msg(f"|rFailed to add zone.|n")
    
    def _move_character(self, skirmish):
        """Move character to a different zone"""
        if not self.args:
            self.caller.msg("Usage: +skirmish/move <zone> [subtle|bold]")
            return
        
        # Check if in skirmish
        if self.caller not in skirmish.db.combatants:
            self.caller.msg("|rYou are not in this skirmish. Use |w+skirmish/join|r first.|n")
            return
        
        args = self.args.split()
        target_zone = args[0]
        subtle = "subtle" in args
        bold = "bold" in args
        
        # Check if adjacent (normal movement) or requires Momentum
        current_zone = skirmish.get_character_zone(self.caller)
        if current_zone:
            adjacent = skirmish.get_adjacent_zones(current_zone)
            if target_zone not in adjacent:
                self.caller.msg(f"|y{target_zone} is not adjacent. Spend 2 Momentum to move there.|n")
                # Could check for Momentum here
        
        success, message = skirmish.move_character(self.caller, target_zone, subtle, bold)
        if success:
            self.caller.msg(f"|g{message}|n")
            
            # Notify room
            room = self.caller.location
            if room:
                move_type = "subtly" if subtle else ("boldly" if bold else "")
                if move_type:
                    room.msg_contents(
                        f"|w{self.caller.name} moves {move_type} to {target_zone}.|n",
                        exclude=self.caller
                    )
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _add_asset(self, skirmish):
        """Add an asset to the skirmish"""
        if not self.args:
            self.caller.msg("Usage: +skirmish/add <asset>")
            return
        
        # Check if in skirmish
        if self.caller not in skirmish.db.combatants:
            self.caller.msg("|rYou are not in this skirmish.|n")
            return
        
        # Find asset
        asset = self.caller.has_asset(self.args.strip())
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{self.args.strip()}'.|n")
            return
        
        # Determine asset type
        asset_type = "weapon"
        keywords = asset.get_keywords()
        keywords_lower = [k.lower() for k in keywords]
        
        if "shield" in keywords_lower:
            asset_type = "shield"
        elif "armor" in keywords_lower:
            asset_type = "armor"
        
        # Add to skirmish
        if skirmish.add_asset(self.caller, asset, asset_type):
            self.caller.msg(f"|gAdded {asset.name} to the skirmish.|n")
        else:
            self.caller.msg(f"|rFailed to add {asset.name} to the skirmish.|n")
    
    def _aim_weapon(self, skirmish):
        """Aim a ranged weapon at a zone"""
        if not self.args or " at " not in self.args:
            self.caller.msg("Usage: +skirmish/aim <asset> at <zone>")
            return
        
        # Check if in skirmish
        if self.caller not in skirmish.db.combatants:
            self.caller.msg("|rYou are not in this skirmish.|n")
            return
        
        parts = self.args.split(" at ", 1)
        asset_name = parts[0].strip()
        target_zone = parts[1].strip()
        
        # Find asset
        asset = self.caller.has_asset(asset_name)
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
            return
        
        # Aim weapon
        success, message = skirmish.move_asset_to_zone(self.caller, asset, target_zone, move_character=False)
        if success:
            self.caller.msg(f"|g{message}|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _attack(self, skirmish):
        """Attack a target"""
        if not self.args:
            self.caller.msg("Usage: +skirmish/attack <target> [with <asset>]")
            return
        
        # Check if in skirmish
        if self.caller not in skirmish.db.combatants:
            self.caller.msg("|rYou are not in this skirmish.|n")
            return
        
        # Parse arguments
        args = self.args.split()
        target_name = args[0]
        asset_name = None
        
        if "with" in args:
            with_index = args.index("with")
            if with_index < len(args) - 1:
                asset_name = args[with_index + 1]
        
        # Find target
        target = None
        for combatant in skirmish.db.combatants:
            if combatant.name.lower() == target_name.lower():
                target = combatant
                break
        
        if not target:
            self.caller.msg(f"|rTarget '{target_name}' not found in skirmish.|n")
            return
        
        if target == self.caller:
            self.caller.msg("|rYou cannot attack yourself.|n")
            return
        
        # Check if in same zone (for melee) or adjacent (for ranged)
        attacker_zone = skirmish.get_character_zone(self.caller)
        target_zone = skirmish.get_character_zone(target)
        
        if not attacker_zone or not target_zone:
            self.caller.msg("|rCannot determine zones.|n")
            return
        
        # Find weapon asset
        asset = None
        if asset_name:
            asset = self.caller.has_asset(asset_name)
            if not asset:
                self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
                return
        else:
            # Find first weapon asset
            for asset_id, asset_data in skirmish.db.assets.items():
                if asset_data["owner"].id == self.caller.id and asset_data["type"] == "weapon":
                    asset = asset_data["asset"]
                    break
        
        if not asset:
            self.caller.msg("|rYou need a weapon to attack. Use |w+skirmish/add <weapon>|r first.|n")
            return
        
        # Check if ranged weapon
        keywords = asset.get_keywords()
        keywords_lower = [k.lower() for k in keywords]
        ranged = "ranged weapon" in keywords_lower or "ranged" in keywords_lower
        
        # Check zone requirements
        if not ranged and attacker_zone != target_zone:
            self.caller.msg(f"|r{target.name} is not in your zone. Melee attacks require same zone.|n")
            return
        
        if ranged and attacker_zone != target_zone:
            adjacent = skirmish.get_adjacent_zones(attacker_zone)
            if target_zone not in adjacent:
                self.caller.msg(f"|r{target.name} is not in an adjacent zone. Ranged attacks require same or adjacent zone.|n")
                return
        
        # Calculate difficulty
        difficulty = skirmish.get_attack_difficulty(self.caller, target, asset, ranged)
        
        self.caller.msg(f"|wAttacking {target.name} with {asset.name}...|n")
        self.caller.msg(f"|yDifficulty: {difficulty}|n")
        
        if ranged and attacker_zone != target_zone:
            self.caller.msg("|yRanged attack to adjacent zone: +1 Difficulty|n")
        
        # Check if target is minor character or requires extended task
        target_battle = target.get_skill("battle") if hasattr(target, 'get_skill') else 0
        
        if target_battle > 0:
            # Non-minor character - set up extended task
            task = skirmish.set_extended_task(target, target_battle, self.caller)
            self.caller.msg(f"|yTarget requires {task['requirement']} successes to defeat (extended task).|n")
            
            task_status = skirmish.get_extended_task_status(target)
            if task_status:
                self.caller.msg(f"|yExtended task progress: {task_status['points']}/{task_status['requirement']} successes|n")
                self.caller.msg(f"|yAttackers contributing: {len(task_status['attackers'])}|n")
        
        # Prompt for roll
        self.caller.msg(f"|yUse |w+roll <drive> + battle vs {difficulty}|y to make the attack.|n")
        self.caller.msg("|yIf successful, it will contribute to defeating your opponent.|n")
    
    def _defend(self, skirmish):
        """Prepare defensive stance"""
        self.caller.msg("|yYou prepare a defensive stance.|n")
        
        # Show defensive assets
        defensive_assets = skirmish.get_defensive_assets(self.caller)
        if defensive_assets:
            self.caller.msg(f"|yDefensive assets: {', '.join([a.name for a in defensive_assets])}|n")
        else:
            self.caller.msg("|yYou have no defensive assets.|n")
    
    def _create_intangible(self, skirmish):
        """Create an intangible asset"""
        if "=" not in self.args:
            self.caller.msg("Usage: +skirmish/create <name>=<description>")
            return
        
        name, description = self.args.split("=", 1)
        name = name.strip()
        description = description.strip()
        
        if skirmish.create_intangible_asset(self.caller, name, description):
            self.caller.msg(f"|gCreated intangible asset: {name} - {description}|n")
        else:
            self.caller.msg("|rFailed to create intangible asset.|n")
    
    def _overcome_obstacle(self, skirmish):
        """Overcome an obstacle in current zone"""
        current_zone = skirmish.get_character_zone(self.caller)
        if not current_zone:
            self.caller.msg("|rYou are not positioned in any zone.|n")
            return
        
        zone_data = skirmish.db.zones.get(current_zone, {})
        traits = zone_data.get("traits", [])
        
        self.caller.msg(f"|yOvercoming obstacle in {current_zone} zone...|n")
        if traits:
            self.caller.msg(f"|yZone traits: {', '.join(traits)}|n")
        
        self.caller.msg("|yUse |w+roll <drive> + move|y to overcome terrain obstacles.|n")
        self.caller.msg("|yUse |w+roll <drive> + understand|y to find an easy path.|n")
        self.caller.msg("|yUse |w+roll <drive> + discipline|y to force through with grit.|n")
    
    def _gather_info(self, skirmish):
        """Gather information about opponents or environment"""
        current_zone = skirmish.get_character_zone(self.caller)
        
        self.caller.msg("|yGathering information...|n")
        if current_zone:
            self.caller.msg(f"|yCurrent zone: {current_zone}|n")
        
        self.caller.msg("|yUse |w+roll <drive> + understand|y or |w+roll <drive> + battle|y to learn about opponents.|n")
        self.caller.msg("|yThis can help identify weaknesses, detect hidden weapons, or spot environmental details.|n")

