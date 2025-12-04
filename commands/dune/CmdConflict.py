"""
General Conflict Commands for Dune 2d20 System

Handles common conflict actions that apply to all conflict types:
- Turn order and initiative
- Moving assets (subtle/bold)
- Using assets (attack, target, create, overcome obstacle, gain info, aid ally)
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.search import search_object


class CmdConflict(MuxCommand):
    """
    General conflict actions that apply to all conflict types.
    
    Usage:
        +conflict/turn - Show whose turn it is
        +conflict/next - Pass to next character
        +conflict/initiative [keep] - Keep the initiative (spend 2 Momentum)
        +conflict/move <asset> to <zone> [subtle|bold] - Move asset
        +conflict/use <asset> [to <action>] - Use an asset
        +conflict/attack <target> with <asset> - Attack with asset
        +conflict/target <asset> in <zone> - Target opponent's asset
        +conflict/create <name>=<description> [trait|asset] - Create trait or asset
        +conflict/obstacle <zone> - Overcome obstacle
        +conflict/info - Gain information
        +conflict/aid <ally> - Aid a defeated ally
    
    Actions:
        move - Move asset to adjacent zone
        use - Use asset for various purposes
        attack - Attack opponent
        target - Target opponent's asset
        create - Create trait or asset (Difficulty 2)
        obstacle - Overcome obstacle (Difficulty usually 1)
        info - Gain information (Difficulty 0, spend Momentum for questions)
        aid - Aid defeated ally (Difficulty 2 or extended task)
    
    Examples:
        +conflict/move Crysknife to opponent_personal subtle
        +conflict/attack Thug with Crysknife
        +conflict/create "Good Position"=Taking advantage of terrain
        +conflict/info
    """
    
    key = "+conflict"
    aliases = ["conflict", "conf"]
    help_category = "Combat"
    
    def func(self):
        """Handle general conflict commands"""
        
        # Get current conflict (check all types)
        conflict = self._get_current_conflict()
        
        if not conflict:
            self.caller.msg("|rYou are not in any active conflict.|n")
            self.caller.msg("|yUse |w+duel|y, |w+skirmish|y, |w+espionage|y, |w+warfare|y, or |w+intrigue|y commands.|n")
            return
        
        # Show turn
        if "turn" in self.switches or not self.switches:
            self._show_turn(conflict)
            return
        
        # Next turn
        if "next" in self.switches:
            self._next_turn(conflict)
            return
        
        # Keep initiative
        if "initiative" in self.switches or "init" in self.switches:
            self._keep_initiative(conflict)
            return
        
        # Move asset
        if "move" in self.switches:
            self._move_asset(conflict)
            return
        
        # Use asset
        if "use" in self.switches:
            self._use_asset(conflict)
            return
        
        # Attack
        if "attack" in self.switches:
            self._attack(conflict)
            return
        
        # Target asset
        if "target" in self.switches:
            self._target_asset(conflict)
            return
        
        # Create trait/asset
        if "create" in self.switches:
            self._create_trait_asset(conflict)
            return
        
        # Overcome obstacle
        if "obstacle" in self.switches:
            self._overcome_obstacle(conflict)
            return
        
        # Gain information
        if "info" in self.switches or "information" in self.switches:
            self._gain_information(conflict)
            return
        
        # Aid ally
        if "aid" in self.switches or "help" in self.switches:
            self._aid_ally(conflict)
            return
        
        # Default: show turn
        self._show_turn(conflict)
    
    def _get_current_conflict(self):
        """Get the current conflict (any type)"""
        room = self.caller.location
        if not room:
            return None
        
        # Search for all conflict types
        from evennia import search_tag
        conflicts = []
        
        for conflict_type in ["duel", "skirmish", "espionage", "warfare", "intrigue"]:
            found = search_tag(conflict_type, category="combat")
            for conflict in found:
                if conflict.location == room and conflict.db.status == "active":
                    conflicts.append(conflict)
        
        # Return first active conflict
        if conflicts:
            return conflicts[0]
        
        return None
    
    def _show_turn(self, conflict):
        """Show current turn information"""
        # Check if conflict has turn system
        if not hasattr(conflict, 'get_current_turn'):
            self.caller.msg("|yThis conflict type doesn't use turn order.|n")
            return
        
        current_turn = conflict.get_current_turn()
        if current_turn:
            if current_turn == self.caller:
                self.caller.msg(f"|gIt is your turn (Round {conflict.db.current_round if hasattr(conflict.db, 'current_round') else 1}).|n")
            else:
                self.caller.msg(f"|yCurrent turn: {current_turn.name} (Round {conflict.db.current_round if hasattr(conflict.db, 'current_round') else 1}).|n")
        else:
            self.caller.msg("|yTurn order not initialized.|n")
    
    def _next_turn(self, conflict):
        """Pass to next character"""
        if not hasattr(conflict, 'next_turn'):
            self.caller.msg("|rThis conflict type doesn't use turn order.|n")
            return
        
        current_turn = conflict.get_current_turn()
        if current_turn != self.caller:
            self.caller.msg("|rIt is not your turn.|n")
            return
        
        next_char = conflict.next_turn()
        if next_char:
            room = self.caller.location
            if room:
                room.msg_contents(f"|w{self.caller.name} passes to {next_char.name}.|n")
            self.caller.msg(f"|gPassed to {next_char.name}.|n")
        else:
            self.caller.msg("|gTurn passed.|n")
    
    def _keep_initiative(self, conflict):
        """Keep the initiative"""
        if not hasattr(conflict, 'keep_initiative'):
            self.caller.msg("|rThis conflict type doesn't support keeping initiative.|n")
            return
        
        current_turn = conflict.get_current_turn()
        if current_turn != self.caller:
            self.caller.msg("|rIt is not your turn.|n")
            return
        
        # Check Momentum
        momentum = getattr(self.caller.db, 'momentum', 0)
        if momentum < 2:
            self.caller.msg("|rYou need 2 Momentum to keep the initiative. Current: {momentum}|n".format(momentum=momentum))
            return
        
        # Keep initiative
        success, message = conflict.keep_initiative(self.caller, momentum_cost=2)
        if success:
            # Spend Momentum
            self.caller.db.momentum -= 2
            
            room = self.caller.location
            if room:
                room.msg_contents(f"|w{self.caller.name} keeps the initiative!|n")
            
            self.caller.msg(f"|g{message}|n")
            self.caller.msg("|yYou may take an extra action (+1 Difficulty) or allow an ally to act.|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _move_asset(self, conflict):
        """Move an asset (general - delegates to conflict-specific method)"""
        if not self.args or " to " not in self.args:
            self.caller.msg("Usage: +conflict/move <asset> to <zone> [subtle|bold]")
            return
        
        # Delegate to conflict-specific move method
        # This is a wrapper that calls the appropriate method based on conflict type
        conflict_type = None
        if hasattr(conflict, '__class__'):
            class_name = conflict.__class__.__name__
            if 'Duel' in class_name:
                conflict_type = 'duel'
            elif 'Skirmish' in class_name:
                conflict_type = 'skirmish'
            elif 'Espionage' in class_name:
                conflict_type = 'espionage'
            elif 'Warfare' in class_name:
                conflict_type = 'warfare'
            elif 'Intrigue' in class_name:
                conflict_type = 'intrigue'
        
        if conflict_type:
            self.caller.msg(f"|yUse |w+{conflict_type}/move <asset> to <zone>|y for movement.|n")
        else:
            self.caller.msg("|rMovement not available for this conflict type.|n")
    
    def _use_asset(self, conflict):
        """Use an asset for various purposes"""
        if not self.args:
            self.caller.msg("Usage: +conflict/use <asset> [to <action>]")
            self.caller.msg("Actions: attack, target, create, obstacle, info, aid")
            return
        
        self.caller.msg("|yUse specific commands for asset actions:|n")
        self.caller.msg("  |w+conflict/attack|y - Attack with asset")
        self.caller.msg("  |w+conflict/target|y - Target opponent's asset")
        self.caller.msg("  |w+conflict/create|y - Create trait or asset")
        self.caller.msg("  |w+conflict/obstacle|y - Overcome obstacle")
        self.caller.msg("  |w+conflict/info|y - Gain information")
        self.caller.msg("  |w+conflict/aid|y - Aid defeated ally")
    
    def _attack(self, conflict):
        """Attack with an asset (general wrapper)"""
        if not self.args or " with " not in self.args:
            self.caller.msg("Usage: +conflict/attack <target> with <asset>")
            return
        
        # Delegate to conflict-specific attack
        conflict_type = self._get_conflict_type(conflict)
        if conflict_type:
            self.caller.msg(f"|yUse |w+{conflict_type}/attack|y for attacks.|n")
        else:
            self.caller.msg("|rAttacks not available for this conflict type.|n")
    
    def _target_asset(self, conflict):
        """Target an opponent's asset"""
        if not self.args or " in " not in self.args:
            self.caller.msg("Usage: +conflict/target <asset> in <zone>")
            return
        
        parts = self.args.split(" in ", 1)
        asset_name = parts[0].strip()
        zone_name = parts[1].strip()
        
        self.caller.msg(f"|wTargeting {asset_name} in {zone_name}...|n")
        self.caller.msg("|yDifficulty: 2 (or contest if asset is wielded directly)|n")
        self.caller.msg("|yUse appropriate skill test to remove the asset.|n")
        self.caller.msg("|yIntangible assets are destroyed. Tangible assets are set aside and can be recovered.|n")
    
    def _create_trait_asset(self, conflict):
        """Create a trait or asset"""
        if "=" not in self.args:
            self.caller.msg("Usage: +conflict/create <name>=<description> [trait|asset]")
            self.caller.msg("")
            self.caller.msg("|yTo create an asset object (not just a trait):|n")
            self.caller.msg("  +conflict/create <name>=<description> asset [type]")
            self.caller.msg("  Example: +conflict/create 'Good Position'='Taking advantage of terrain' asset Personal")
            return
        
        parts = self.args.split("=", 1)
        name = parts[0].strip().strip('"')
        rest = parts[1].strip()
        
        # Check for trait/asset specification
        is_asset = "asset" in rest.lower()
        is_trait = "trait" in rest.lower() or not is_asset
        
        # Check for asset type specification
        asset_type = None
        valid_types = ["Personal", "Warfare", "Espionage", "Intrigue"]
        for atype in valid_types:
            if atype.lower() in rest.lower():
                asset_type = atype
                break
        
        # Remove trait/asset keywords from description
        description = rest.replace("trait", "").replace("asset", "").strip()
        if asset_type:
            description = description.replace(asset_type, "").strip()
        description = description.strip('"')
        
        self.caller.msg(f"|wCreating {'asset' if is_asset else 'trait'}: {name}...|n")
        self.caller.msg("|yDifficulty: 2|n")
        self.caller.msg("|yUse appropriate skill test to create it.|n")
        
        if is_asset:
            self.caller.msg("|yCreated assets have Quality 0 and are temporary.|n")
            self.caller.msg("|ySpend 2 Momentum to make an asset permanent.|n")
            if asset_type:
                self.caller.msg(f"|yAsset type: {asset_type}|n")
            else:
                self.caller.msg("|yNote: To create an actual Asset object, specify type:|n")
                self.caller.msg("  +conflict/create <name>=<description> asset <type>")
                self.caller.msg("  Types: Personal, Warfare, Espionage, Intrigue")
    
    def _overcome_obstacle(self, conflict):
        """Overcome an obstacle"""
        if not self.args:
            self.caller.msg("Usage: +conflict/obstacle <zone>")
            return
        
        zone_name = self.args.strip()
        
        self.caller.msg(f"|wOvercoming obstacle in {zone_name}...|n")
        self.caller.msg("|yDifficulty: Usually 1 (can be higher for challenging obstacles)|n")
        self.caller.msg("|yUse appropriate skill test based on obstacle type.|n")
        self.caller.msg("|yPhysical: Move, Battle, Discipline|n")
        self.caller.msg("|ySocial: Communicate, Understand|n")
    
    def _gain_information(self, conflict):
        """Gain information"""
        self.caller.msg("|wGaining information...|n")
        self.caller.msg("|yDifficulty: 0 (base, can increase for classified/restricted info)|n")
        self.caller.msg("|ySpend Momentum to ask questions (1 Momentum per question).|n")
        self.caller.msg("|yUse appropriate skill test (Understand, Battle, Communicate, etc.).|n")
        self.caller.msg("|yMomentum can also be used to create traits or remove concealment traits.|n")
    
    def _aid_ally(self, conflict):
        """Aid a defeated ally"""
        if not self.args:
            self.caller.msg("Usage: +conflict/aid <ally>")
            return
        
        ally_name = self.args.strip()
        
        self.caller.msg(f"|wAiding {ally_name}...|n")
        self.caller.msg("|yTo remove a trait: Difficulty 2|n")
        self.caller.msg("|yTo prevent lasting effect: Difficulty 2|n")
        self.caller.msg("|yTo recover defeat: Extended task (requirement = 4 + Quality of defeating asset)|n")
        self.caller.msg("|yUse appropriate skill test based on how you're aiding them.|n")
    
    def _get_conflict_type(self, conflict):
        """Get conflict type string"""
        if hasattr(conflict, '__class__'):
            class_name = conflict.__class__.__name__
            if 'Duel' in class_name:
                return 'duel'
            elif 'Skirmish' in class_name:
                return 'skirmish'
            elif 'Espionage' in class_name:
                return 'espionage'
            elif 'Warfare' in class_name:
                return 'warfare'
            elif 'Intrigue' in class_name:
                return 'intrigue'
        return None

