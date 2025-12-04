"""
Duel Commands for Dune 2d20 System

Manages turn-based dueling with zones, asset positioning, and combat resolution.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.search import search_object
from typeclasses.duels import Duel


class CmdDuel(MuxCommand):
    """
    Manage duels - one-on-one combat with zones and asset positioning.
    
    Usage:
        +duel/challenge <opponent> - Challenge someone to a duel
        +duel/accept - Accept a pending duel challenge
        +duel/decline - Decline a pending duel challenge
        +duel/status - Show current duel status
        +duel/end - End the current duel (staff or participant)
        +duel/add <asset> [to <zone>] - Add an asset to the duel
        +duel/move <asset> to <zone> [subtle] - Move an asset to a zone
        +duel/attack <asset> - Attack with an asset (must be in opponent's zone)
        +duel/defend - Prepare defensive stance
        +duel/create <name>=<description> - Create an intangible asset
        +duel/target <asset> - Target an opponent's asset (disarm, etc.)
        +duel/info - Gather information about opponent
        +duel/turn - Show whose turn it is
        +duel/next - Pass to next turn
        +duel/initiative - Keep the initiative (spend 2 Momentum)
    
    Zones:
        Each combatant has:
        - personal: Their own zone
        - left_guard: Left defensive zone
        - right_guard: Right defensive zone
    
    Asset Movement:
        - Weapons can be moved between zones
        - Full shields cannot move
        - Half-shields can move to adjacent zones only
        - Moving to opponent's zone allows attacks
    
    Examples:
        +duel/challenge Nasir
        +duel/add Crysknife to left_guard
        +duel/move Crysknife to opponent_personal
        +duel/attack Crysknife
        +duel/create "Good Position"=Taking advantage of opponent's stance
    """
    
    key = "+duel"
    aliases = ["duel"]
    help_category = "Combat"
    
    def func(self):
        """Handle duel commands"""
        
        # Get current duel
        duel = self._get_current_duel()
        
        # Challenge someone
        if "challenge" in self.switches or "chall" in self.switches:
            self._challenge_duel()
            return
        
        # Accept challenge
        if "accept" in self.switches:
            self._accept_duel()
            return
        
        # Decline challenge
        if "decline" in self.switches:
            self._decline_duel()
            return
        
        # Show status
        if "status" in self.switches or not self.switches:
            if duel:
                self.caller.msg(duel.get_display(self.caller))
            else:
                self._show_no_duel()
            return
        
        # End duel
        if "end" in self.switches:
            self._end_duel(duel)
            return
        
        # Need an active duel for remaining commands
        if not duel:
            self.caller.msg("|rYou are not in a duel. Use |w+duel/challenge <opponent>|r to start one.|n")
            return
        
        # Add asset
        if "add" in self.switches:
            self._add_asset(duel)
            return
        
        # Move asset
        if "move" in self.switches:
            self._move_asset(duel)
            return
        
        # Attack
        if "attack" in self.switches:
            self._attack(duel)
            return
        
        # Defend
        if "defend" in self.switches:
            self._defend(duel)
            return
        
        # Create intangible asset
        if "create" in self.switches:
            self._create_intangible(duel)
            return
        
        # Target asset
        if "target" in self.switches:
            self._target_asset(duel)
            return
        
        # Gather information
        if "info" in self.switches or "information" in self.switches:
            self._gather_info(duel)
            return
        
        # Show turn
        if "turn" in self.switches:
            self._show_turn(duel)
            return
        
        # Next turn
        if "next" in self.switches:
            self._next_turn(duel)
            return
        
        # Keep initiative
        if "initiative" in self.switches or "init" in self.switches:
            self._keep_initiative(duel)
            return
        
        # Default: show status
        if duel:
            self.caller.msg(duel.get_display(self.caller))
        else:
            self._show_no_duel()
    
    def _get_current_duel(self):
        """Get the current duel for the caller"""
        # Check if there's a duel in the room
        room = self.caller.location
        if not room:
            return None
        
        # Search for duel objects in the room
        from evennia import search_tag
        duels = search_tag("duel", category="combat")
        
        for duel in duels:
            if duel.location == room:
                # Check if caller is a participant
                if (duel.db.combatant1 and duel.db.combatant1.id == self.caller.id) or \
                   (duel.db.combatant2 and duel.db.combatant2.id == self.caller.id):
                    return duel
        
        return None
    
    def _challenge_duel(self):
        """Challenge someone to a duel"""
        if not self.args:
            self.caller.msg("Usage: +duel/challenge <opponent>")
            return
        
        # Check if already in a duel
        if self._get_current_duel():
            self.caller.msg("|rYou are already in a duel.|n")
            return
        
        # Find opponent
        opponent = self.caller.search(self.args)
        if not opponent:
            return
        
        if opponent == self.caller:
            self.caller.msg("|rYou cannot challenge yourself.|n")
            return
        
        # Check if opponent is in a duel
        room = self.caller.location
        if not room:
            self.caller.msg("|rYou must be in a room to challenge someone.|n")
            return
        
        # Create duel object
        from evennia import create_object
        duel = create_object(
            Duel,
            key=f"Duel: {self.caller.name} vs {opponent.name}",
            location=room
        )
        
        # Tag it
        duel.tags.add("duel", category="combat")
        
        # Add combatants
        duel.add_combatant(self.caller)
        duel.add_combatant(opponent)
        
        # Set initial turn (challenger goes first)
        duel.set_current_turn(self.caller)
        duel.set_initiative(self.caller)
        duel.db.current_round = 1
        duel.db.initiative_kept = False
        
        # Notify both parties
        self.caller.msg(f"|gYou challenge {opponent.name} to a duel!|n")
        opponent.msg(f"|y{self.caller.name} challenges you to a duel!|n")
        opponent.msg("Use |w+duel/accept|n to accept or |w+duel/decline|n to decline.")
        
        # Notify room
        room.msg_contents(
            f"|w{self.caller.name} challenges {opponent.name} to a duel!|n",
            exclude=[self.caller, opponent]
        )
    
    def _accept_duel(self):
        """Accept a duel challenge"""
        # Find pending duel
        room = self.caller.location
        if not room:
            self.caller.msg("|rYou must be in a room.|n")
            return
        
        from evennia import search_tag
        duels = search_tag("duel", category="combat")
        
        pending_duel = None
        for duel in duels:
            if duel.location == room:
                if (duel.db.combatant1 and duel.db.combatant1.id == self.caller.id) or \
                   (duel.db.combatant2 and duel.db.combatant2.id == self.caller.id):
                    pending_duel = duel
                    break
        
        if not pending_duel:
            self.caller.msg("|rYou have no pending duel challenge.|n")
            return
        
        # Duel is already active if both combatants are set
        if pending_duel.db.combatant1 and pending_duel.db.combatant2:
            self.caller.msg("|yThe duel is already active.|n")
            return
        
        # Notify room
        room.msg_contents(f"|w{self.caller.name} accepts the duel!|n")
        self.caller.msg("|gDuel accepted! The duel begins.|n")
    
    def _decline_duel(self):
        """Decline a duel challenge"""
        # Find pending duel
        room = self.caller.location
        if not room:
            return
        
        from evennia import search_tag
        duels = search_tag("duel", category="combat")
        
        pending_duel = None
        for duel in duels:
            if duel.location == room:
                if (duel.db.combatant1 and duel.db.combatant1.id == self.caller.id) or \
                   (duel.db.combatant2 and duel.db.combatant2.id == self.caller.id):
                    pending_duel = duel
                    break
        
        if not pending_duel:
            self.caller.msg("|rYou have no pending duel challenge.|n")
            return
        
        # Delete the duel
        challenger = pending_duel.db.combatant1
        if challenger and challenger.id == self.caller.id:
            challenger = pending_duel.db.combatant2
        
        if challenger:
            challenger.msg(f"|y{self.caller.name} declines your duel challenge.|n")
        
        self.caller.msg("|yYou decline the duel challenge.|n")
        room.msg_contents(
            f"|w{self.caller.name} declines the duel challenge.|n",
            exclude=[self.caller, challenger] if challenger else [self.caller]
        )
        
        pending_duel.delete()
    
    def _show_no_duel(self):
        """Show message when not in a duel"""
        self.caller.msg("|yYou are not currently in a duel.|n")
        self.caller.msg("Use |w+duel/challenge <opponent>|n to challenge someone.")
    
    def _end_duel(self, duel):
        """End a duel"""
        if not duel:
            self.caller.msg("|rYou are not in a duel.|n")
            return
        
        # Check permissions
        is_participant = (duel.db.combatant1 and duel.db.combatant1.id == self.caller.id) or \
                        (duel.db.combatant2 and duel.db.combatant2.id == self.caller.id)
        
        if not is_participant and not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou can only end duels you are participating in.|n")
            return
        
        # Delete the duel
        room = duel.location
        if room:
            room.msg_contents(f"|wThe duel between {duel.db.combatant1.name if duel.db.combatant1 else 'Unknown'} and {duel.db.combatant2.name if duel.db.combatant2 else 'Unknown'} has ended.|n")
        
        duel.delete()
        self.caller.msg("|gDuel ended.|n")
    
    def _add_asset(self, duel):
        """Add an asset to the duel"""
        if not self.args:
            self.caller.msg("Usage: +duel/add <asset> [to <zone>]")
            self.caller.msg("Zones: personal, left_guard, right_guard")
            return
        
        # Parse arguments
        args = self.args.split()
        asset_name = args[0]
        zone = "personal"  # Default
        
        # Check for "to <zone>" pattern
        if "to" in args and args.index("to") < len(args) - 1:
            to_index = args.index("to")
            zone = args[to_index + 1]
        
        # Find asset in caller's inventory
        asset = self.caller.has_asset(asset_name)
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
            return
        
        # Determine asset type
        asset_type = "weapon"
        keywords = asset.get_keywords()
        keywords_lower = [k.lower() for k in keywords]
        
        if "shield" in keywords_lower:
            asset_type = "shield"
        elif "armor" in keywords_lower:
            asset_type = "armor"
        
        # Add to duel
        if duel.add_asset(self.caller, asset, zone, asset_type):
            self.caller.msg(f"|gAdded {asset.name} to {zone.replace('_', ' ')} zone.|n")
            
            # Notify opponent
            opponent = duel.get_opponent(self.caller)
            if opponent:
                opponent.msg(f"|y{self.caller.name} adds {asset.name} to the duel.|n")
        else:
            self.caller.msg(f"|rFailed to add {asset.name} to the duel.|n")
    
    def _move_asset(self, duel):
        """Move an asset to a different zone"""
        if not self.args:
            self.caller.msg("Usage: +duel/move <asset> to <zone> [subtle]")
            self.caller.msg("Zones: personal, left_guard, right_guard, opponent_personal, opponent_left_guard, opponent_right_guard")
            return
        
        # Parse arguments
        args = self.args.split()
        asset_name = args[0]
        subtle = "subtle" in args
        
        # Find "to <zone>"
        if "to" not in args:
            self.caller.msg("|rYou must specify a target zone with 'to <zone>'.|n")
            return
        
        to_index = args.index("to")
        if to_index >= len(args) - 1:
            self.caller.msg("|rYou must specify a target zone.|n")
            return
        
        target_zone = args[to_index + 1]
        
        # Find asset
        asset = self.caller.has_asset(asset_name)
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
            return
        
        # Check if asset is in the duel
        if asset.id not in duel.db.assets:
            self.caller.msg(f"|r{asset.name} is not in this duel. Use |w+duel/add {asset_name}|r first.|n")
            return
        
        # Move asset
        success, message = duel.move_asset(self.caller, asset, target_zone, subtle)
        if success:
            self.caller.msg(f"|g{message}|n")
            
            # Notify opponent (unless subtle)
            if not subtle:
                opponent = duel.get_opponent(self.caller)
                if opponent:
                    opponent.msg(f"|y{self.caller.name} moves {asset.name} to {target_zone.replace('_', ' ')}.|n")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _attack(self, duel):
        """Attack with an asset"""
        if not self.args:
            self.caller.msg("Usage: +duel/attack <asset>")
            return
        
        # Find asset
        asset = self.caller.has_asset(self.args.strip())
        if not asset:
            self.caller.msg(f"|rYou don't have an asset named '{self.args.strip()}'.|n")
            return
        
        # Check if asset is in opponent's zone
        asset_id = asset.id
        if asset_id not in duel.db.assets:
            self.caller.msg(f"|r{asset.name} is not in this duel.|n")
            return
        
        asset_data = duel.db.assets[asset_id]
        current_zone = asset_data["zone"]
        
        # Check if asset is in opponent's zone (for attack)
        if not current_zone.startswith("opponent_"):
            self.caller.msg(f"|r{asset.name} must be in your opponent's zone to attack. Move it there first with |w+duel/move {asset.name} to opponent_personal|r|n")
            return
        
        # Get opponent
        opponent = duel.get_opponent(self.caller)
        if not opponent:
            self.caller.msg("|rNo opponent found.|n")
            return
        
        # Get defensive assets in the zone
        zone_name = current_zone.replace("opponent_", "")
        defensive_assets = duel.get_defensive_assets_in_zone(opponent, zone_name)
        difficulty_modifier = len(defensive_assets)
        
        # Calculate base difficulty
        base_difficulty = 1
        final_difficulty = base_difficulty + difficulty_modifier
        
        self.caller.msg(f"|wAttacking with {asset.name}...|n")
        self.caller.msg(f"|yDifficulty: {final_difficulty} (base {base_difficulty} + {difficulty_modifier} from defensive assets)|n")
        
        if defensive_assets:
            self.caller.msg(f"|yDefensive assets in zone: {', '.join([a.name for a in defensive_assets])}|n")
        
        # Check if opponent is a minor character (immediate defeat) or requires extended task
        # For now, assume non-minor characters need extended task
        # In full implementation, would check character type
        opponent_battle = opponent.get_skill("battle") if hasattr(opponent, 'get_skill') else 0
        
        if opponent_battle > 0:
            # Non-minor character - set up extended task
            if not duel.db.extended_task:
                duel.set_extended_task(opponent_battle)
                self.caller.msg(f"|yOpponent requires {opponent_battle} successes to defeat (extended task).|n")
            
            task_status = duel.get_extended_task_status()
            if task_status:
                self.caller.msg(f"|yExtended task progress: {task_status['points']}/{task_status['requirement']} successes|n")
        
        # Prompt for roll
        self.caller.msg(f"|yUse |w+roll <drive> + battle vs {final_difficulty}|y to make the attack.|n")
        self.caller.msg("|yIf successful, it will contribute to defeating your opponent.|n")
    
    def _defend(self, duel):
        """Prepare defensive stance"""
        self.caller.msg("|yYou prepare a defensive stance.|n")
        self.caller.msg("|yMove weapons to guard zones to use them defensively.|n")
        
        # Show current defensive assets
        zones = duel.get_zones(self.caller)
        if zones:
            left_guard = duel.get_defensive_assets_in_zone(self.caller, "left_guard")
            right_guard = duel.get_defensive_assets_in_zone(self.caller, "right_guard")
            
            if left_guard or right_guard:
                self.caller.msg("|yCurrent defensive assets:|n")
                if left_guard:
                    self.caller.msg(f"  Left Guard: {', '.join([a.name for a in left_guard])}")
                if right_guard:
                    self.caller.msg(f"  Right Guard: {', '.join([a.name for a in right_guard])}")
    
    def _create_intangible(self, duel):
        """Create an intangible asset"""
        if "=" not in self.args:
            self.caller.msg("Usage: +duel/create <name>=<description> [asset [type]]")
            self.caller.msg("")
            self.caller.msg("|yTo create an actual Asset object (not just a trait):|n")
            self.caller.msg("  +duel/create <name>=<description> asset [type]")
            self.caller.msg("  Example: +duel/create 'Good Position'='Taking advantage' asset Personal")
            self.caller.msg("  Types: Personal, Warfare, Espionage, Intrigue")
            self.caller.msg("")
            self.caller.msg("|yTo make the asset permanent:|n")
            self.caller.msg("  Spend 2 Momentum after creating it.")
            return
        
        parts = self.args.split("=", 1)
        name = parts[0].strip().strip('"')
        rest = parts[1].strip()
        
        # Check if creating an actual Asset object
        create_asset_object = "asset" in rest.lower()
        asset_type = None
        if create_asset_object:
            valid_types = ["Personal", "Warfare", "Espionage", "Intrigue"]
            for atype in valid_types:
                if atype.lower() in rest.lower():
                    asset_type = atype
                    break
            if not asset_type:
                asset_type = "Personal"  # Default to Personal
        
        # Extract description
        description = rest.replace("asset", "").strip()
        if asset_type:
            description = description.replace(asset_type, "").strip()
        description = description.strip('"')
        
        # Create as intangible asset (trait) in the duel
        if duel.create_intangible_asset(self.caller, name, description):
            self.caller.msg(f"|gCreated intangible asset: {name} - {description}|n")
            
            # If creating an actual Asset object, create it too
            if create_asset_object:
                from typeclasses.assets import create_custom_asset
                asset = create_custom_asset(
                    name=name,
                    asset_type=asset_type or "Personal",
                    character=self.caller,
                    quality=0,
                    keywords=["Intangible", "Temporary"],
                    description=description,
                    special="Created during conflict. Spend 2 Momentum to make permanent."
                )
                if asset:
                    self.caller.msg(f"|gCreated Asset object: {name} (Quality 0, temporary)|n")
                    self.caller.msg("|ySpend 2 Momentum to make this asset permanent.|n")
        else:
            self.caller.msg("|rFailed to create intangible asset.|n")
    
    def _target_asset(self, duel):
        """Target an opponent's asset"""
        if not self.args:
            self.caller.msg("Usage: +duel/target <opponent's asset>")
            return
        
        self.caller.msg("|yTargeting opponent's asset (disarm, disrupt, etc.)|n")
        self.caller.msg("|yThis would require a roll to succeed.|n")
        # Full implementation would handle asset targeting
    
    def _gather_info(self, duel):
        """Gather information about opponent"""
        opponent = duel.get_opponent(self.caller)
        if not opponent:
            self.caller.msg("|rNo opponent found.|n")
            return
        
        self.caller.msg(f"|yGathering information about {opponent.name}...|n")
        self.caller.msg("|yDifficulty: 0 (base, can increase for secrets)|n")
        self.caller.msg("|yUse |w+roll <drive> + understand|y or |w+roll <drive> + battle|y to learn about your opponent.|n")
        self.caller.msg("|ySpend Momentum to ask questions (1 Momentum per question).|n")
        self.caller.msg("|yThis can help you identify weaknesses or anticipate attacks.|n")
    
    def _show_turn(self, duel):
        """Show whose turn it is"""
        current_turn = duel.get_current_turn()
        if current_turn:
            if current_turn == self.caller:
                self.caller.msg(f"|gIt is your turn (Round {duel.get_current_round()}).|n")
            else:
                self.caller.msg(f"|yCurrent turn: {current_turn.name} (Round {duel.get_current_round()}).|n")
        else:
            self.caller.msg("|yTurn not set.|n")
    
    def _next_turn(self, duel):
        """Pass to next turn"""
        current_turn = duel.get_current_turn()
        if current_turn != self.caller:
            self.caller.msg("|rIt is not your turn.|n")
            return
        
        next_char = duel.next_turn()
        if next_char:
            room = self.caller.location
            if room:
                room.msg_contents(f"|w{self.caller.name} passes to {next_char.name}.|n")
            self.caller.msg(f"|gPassed to {next_char.name}.|n")
        else:
            self.caller.msg("|gTurn passed.|n")
    
    def _keep_initiative(self, duel):
        """Keep the initiative"""
        current_turn = duel.get_current_turn()
        if current_turn != self.caller:
            self.caller.msg("|rIt is not your turn.|n")
            return
        
        # Check Momentum
        momentum = getattr(self.caller.db, 'momentum', 0)
        if momentum < 2:
            self.caller.msg(f"|rYou need 2 Momentum to keep the initiative. Current: {momentum}|n")
            return
        
        # Check if already kept
        if duel.db.initiative_kept:
            self.caller.msg("|rInitiative has already been kept this round.|n")
            return
        
        # Keep initiative
        success, message = duel.keep_initiative(self.caller, momentum_cost=2)
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

