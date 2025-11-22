"""
Threat Management Command for Dune 2d20 System

Manages the GM's Threat pool, which is scene-based (stored per room).
Threat is the GM's resource pool, similar to Momentum for players.
"""

from evennia.commands.default.muxcommand import MuxCommand


class CmdThreat(MuxCommand):
    """
    Manage the GM's Threat pool for the current scene.
    
    Threat is a scene-based resource pool for staff/GM use.
    It represents perils, dangers, and dramatic tension.
    
    Usage:
        +threat - View current scene's Threat
        +threat/add <amount> - Add Threat to the scene (staff)
        +threat/spend <amount> - Spend Threat (staff)
        +threat/set <amount> - Set Threat to specific value (staff)
        +threat/reset - Reset Threat to 0 (staff)
        
    Switches:
        /add - Add Threat points (staff)
        /spend - Spend Threat points (staff)
        /set - Set Threat to specific value (staff)
        /reset - Reset Threat to 0 (staff)
        
    Threat can be added by:
        - Players buying dice (1, 2, 3 Threat per die)
        - Complications (2 Threat to ignore a complication)
        - Escalation (1 Threat for risky actions)
        - GM: Threatening circumstances (1-2 Threat)
        - GM: NPC Momentum (1 Threat per unspent Momentum)
        
    Threat can be spent by GM for:
        - Buying d20s for NPCs (1, 2, 3 Threat per die)
        - Increase Difficulty (2 Threat per +1 Difficulty)
        - NPC Complications (2 Threat to buy off)
        - Traits (2 Threat to change/create/remove)
        - Environmental effects
        - Rival House Action (1 Threat)
        
    Examples:
        +threat - View current Threat
        +threat/add 2 - Add 2 Threat (staff)
        +threat/spend 3 - Spend 3 Threat (staff)
        +threat/set 5 - Set Threat to 5 (staff)
        +threat/modifier <amount> - Adjust contest Difficulty modifier (staff)
    """
    
    key = "+threat"
    aliases = ["threat"]
    help_category = "Staff"
    
    def func(self):
        """Manage Threat"""
        
        # Get current room (scene)
        if not self.caller.location:
            self.caller.msg("|rYou must be in a room to manage Threat.|n")
            return
        
        room = self.caller.location
        
        # Initialize Threat if needed
        if not hasattr(room.db, 'threat'):
            room.db.threat = 0
        
        # No switches - display current Threat
        if not self.switches:
            self.caller.msg(f"|wScene Threat:|n {room.db.threat}")
            if self.caller.check_permstring("Builder"):
                self.caller.msg("|cUse +threat/add, +threat/spend, or +threat/set to manage Threat.|n")
            return
        
        # Check permissions for all actions
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou don't have permission to manage Threat.|n")
            return
        
        # Add Threat
        if "add" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +threat/add <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            room.db.threat = max(0, room.db.threat + amount)
            self.caller.msg(f"|gAdded {amount} Threat. Current: {room.db.threat}|n")
            
            # Notify others in the room
            if room:
                room.msg_contents(
                    f"|y{self.caller.name} adds {amount} Threat to the scene. (Current: {room.db.threat})|n",
                    exclude=self.caller
                )
        
        # Spend Threat
        elif "spend" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +threat/spend <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            if amount < 1:
                self.caller.msg("You must spend at least 1 Threat.")
                return
            
            if room.db.threat < amount:
                self.caller.msg(f"|rNot enough Threat. Current: {room.db.threat}, Need: {amount}|n")
                return
            
            room.db.threat -= amount
            self.caller.msg(f"|gSpent {amount} Threat. Remaining: {room.db.threat}|n")
            
            # Notify others in the room
            if room:
                room.msg_contents(
                    f"|y{self.caller.name} spends {amount} Threat. (Remaining: {room.db.threat})|n",
                    exclude=self.caller
                )
        
        # Set Threat
        elif "set" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +threat/set <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            room.db.threat = max(0, amount)
            self.caller.msg(f"|gSet Threat to {room.db.threat}|n")
        
        # Reset Threat
        elif "reset" in self.switches:
            room.db.threat = 0
            self.caller.msg("|gReset Threat to 0|n")
        
        # Adjust contest modifier (staff) - use /modifier switch
        elif "modifier" in self.switches:
            if not hasattr(room.db, 'pending_contest') or not room.db.pending_contest:
                self.caller.msg("|rNo pending contest found.|n")
                return
            
            if not self.args:
                self.caller.msg("Usage: +threat/modifier <amount>")
                self.caller.msg("|yThis adjusts the Difficulty modifier for external factors in a contest.|n")
                self.caller.msg("|yEach point reduces the Difficulty by 1 (minimum 0).|n")
                return
            
            try:
                modifier = int(self.args.strip())
            except ValueError:
                self.caller.msg("Modifier must be a number.")
                return
            
            contest_data = room.db.pending_contest
            contest_data["modifiers"] = max(0, modifier)  # Can't be negative
            opponent_successes = contest_data.get("successes", 0)
            new_difficulty = max(0, opponent_successes - contest_data["modifiers"])
            
            self.caller.msg(f"|gSet contest modifier to {contest_data['modifiers']}.|n")
            self.caller.msg(f"|yOpponent's {opponent_successes} successes - {contest_data['modifiers']} modifier = Difficulty {new_difficulty}|n")

