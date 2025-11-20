"""
Character Sheet Command

Displays character statistics for the 2d20 Dune system.
"""

from evennia.commands.default.muxcommand import MuxCommand


class CmdSheet(MuxCommand):
    """
    Display your character sheet or another character's sheet.
    
    Usage:
        +sheet
        +sheet <character name>
        +sheet/full
        
    Switches:
        /full - Display extended information including background
        
    Examples:
        +sheet - View your own character sheet
        +sheet Paul - View Paul's character sheet
        +sheet/full - View your full character sheet with background
    """
    
    key = "+sheet"
    aliases = ["sheet"]
    help_category = "Character"
    
    def func(self):
        """Display character sheet"""
        
        # Determine which character to display
        target = self.caller
        
        if self.args:
            # Look for another character
            target = self.caller.search(self.args.strip())
            if not target:
                return
                
            # Check if target is a character
            if not target.has_account and not hasattr(target, 'db.stats'):
                self.caller.msg(f"{target.name} is not a character.")
                return
        
        # Check if the target has stats initialized
        if not hasattr(target.db, 'stats') or not target.db.stats:
            self.caller.msg(f"{target.name} does not have a character sheet yet.")
            return
        
        # Get and display the sheet
        sheet = target.get_sheet_display()
        self.caller.msg(sheet)
        
        # If /full switch is used, also display background
        if "full" in self.switches:
            if target.db.background:
                self.caller.msg(f"\n|y{'BACKGROUND':-^78}|n")
                self.caller.msg(target.db.background)
                self.caller.msg("|w" + "=" * 78 + "|n")


class CmdStats(MuxCommand):
    """
    Set or view character statistics (staff only).
    
    Usage:
        +stats <character>
        +stats <character>/<type>/<stat>=<value>
        
    Types:
        attr - Attributes (control, dexterity, fitness, insight, presence, reason)
        skill - Skills (battle, communicate, discipline, move, understand)
        
    Examples:
        +stats Paul - View Paul's stats
        +stats Paul/attr/fitness=9 - Set Paul's fitness to 9
        +stats Paul/skill/battle=3 - Set Paul's battle skill to 3
    """
    
    key = "+stats"
    aliases = ["stats"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Set or view character stats"""
        
        if not self.args:
            self.caller.msg("Usage: +stats <character> or +stats <character>/<type>/<stat>=<value>")
            return
        
        # Parse arguments
        if "=" in self.args:
            # Setting a stat
            if len(self.switches) < 2:
                self.caller.msg("Usage: +stats <character>/<type>/<stat>=<value>")
                self.caller.msg("Types: attr, skill")
                return
            
            char_name = self.args.split("=")[0].strip()
            value_str = self.args.split("=")[1].strip()
            
            try:
                value = int(value_str)
            except ValueError:
                self.caller.msg("Value must be a number.")
                return
            
            # Find the character
            target = self.caller.search(char_name.split("/")[0].strip())
            if not target:
                return
            
            if not hasattr(target.db, 'stats'):
                self.caller.msg(f"{target.name} does not have stats initialized.")
                return
            
            # Determine stat type and name
            stat_type = self.switches[0].lower()
            stat_name = self.switches[1].lower()
            
            if stat_type == "attr":
                target.set_attribute(stat_name, value)
                self.caller.msg(f"Set {target.name}'s {stat_name} attribute to {value}.")
            elif stat_type == "skill":
                target.set_skill(stat_name, value)
                self.caller.msg(f"Set {target.name}'s {stat_name} skill to {value}.")
            else:
                self.caller.msg("Invalid type. Use 'attr' or 'skill'.")
        else:
            # Viewing stats
            target = self.caller.search(self.args.strip())
            if not target:
                return
            
            if not hasattr(target.db, 'stats'):
                self.caller.msg(f"{target.name} does not have stats initialized.")
                return
            
            # Display the sheet
            sheet = target.get_sheet_display()
            self.caller.msg(sheet)


class CmdFocus(MuxCommand):
    """
    Manage character focuses (skill specializations).
    
    Usage:
        +focus - List your focuses
        +focus/add <skill>: <specialization> - Add a focus
        +focus/remove <focus> - Remove a focus
        
    Switches:
        /add - Add a new focus
        /remove - Remove a focus
        
    Examples:
        +focus - List your focuses
        +focus/add Battle: Knife Fighting
        +focus/remove Battle: Knife Fighting
    """
    
    key = "+focus"
    aliases = ["focus", "focuses"]
    help_category = "Character"
    
    def func(self):
        """Manage focuses"""
        
        target = self.caller
        
        if not hasattr(target.db, 'stats'):
            self.caller.msg("Your character does not have stats initialized.")
            return
        
        # No switches - list focuses
        if not self.switches:
            focuses = target.db.stats.get("focuses", [])
            if not focuses:
                self.caller.msg("You have no focuses.")
                return
            
            self.caller.msg("|wYour Focuses:|n")
            for focus in focuses:
                self.caller.msg(f"  • {focus}")
            return
        
        # Add focus
        if "add" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +focus/add <skill>: <specialization>")
                return
            
            target.add_focus(self.args.strip())
            self.caller.msg(f"Added focus: {self.args.strip()}")
        
        # Remove focus
        elif "remove" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +focus/remove <focus>")
                return
            
            if target.remove_focus(self.args.strip()):
                self.caller.msg(f"Removed focus: {self.args.strip()}")
            else:
                self.caller.msg(f"You don't have that focus.")


class CmdStress(MuxCommand):
    """
    Manage character stress (damage).
    
    Usage:
        +stress - View your current stress
        +stress <character> - View another character's stress
        +stress/take <amount> - Take stress damage
        +stress/heal <amount> - Heal stress
        +stress/set <character>=<amount> - Set stress (staff only)
        
    Switches:
        /take - Take stress damage
        /heal - Heal stress
        /set - Set stress directly (staff only)
        
    Examples:
        +stress - Check your stress
        +stress Paul - Check Paul's stress
        +stress/take 3 - Take 3 stress
        +stress/heal 2 - Heal 2 stress
        +stress/set Paul=5 - Set Paul's stress to 5 (staff)
    """
    
    key = "+stress"
    aliases = ["stress"]
    help_category = "Character"
    
    def func(self):
        """Manage stress"""
        
        target = self.caller
        
        # Check for target in args
        if self.args and "=" not in self.args and not self.switches:
            target = self.caller.search(self.args.strip())
            if not target:
                return
        
        if not hasattr(target.db, 'stress'):
            self.caller.msg(f"{target.name} does not have stress tracking.")
            return
        
        # No switches - display current stress
        if not self.switches:
            self.caller.msg(f"{target.name}'s Stress: {target.db.stress}/{target.db.max_stress}")
            if target.db.stress >= target.db.max_stress:
                self.caller.msg("|rINCAPACITATED|n")
            return
        
        # Take stress
        if "take" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +stress/take <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            new_stress, incapacitated = target.take_stress(amount)
            self.caller.msg(f"You take {amount} stress. Current: {new_stress}/{target.db.max_stress}")
            
            if incapacitated:
                self.caller.msg("|rYou are INCAPACITATED!|n")
                target.location.msg_contents(
                    f"{target.name} collapses from their injuries!",
                    exclude=target
                )
        
        # Heal stress
        elif "heal" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +stress/heal <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            new_stress = target.heal_stress(amount)
            self.caller.msg(f"You heal {amount} stress. Current: {new_stress}/{target.db.max_stress}")
        
        # Set stress (staff only)
        elif "set" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You don't have permission to set stress.")
                return
            
            if "=" not in self.args:
                self.caller.msg("Usage: +stress/set <character>=<amount>")
                return
            
            char_name, value_str = self.args.split("=", 1)
            target = self.caller.search(char_name.strip())
            if not target:
                return
            
            try:
                value = int(value_str.strip())
            except ValueError:
                self.caller.msg("Value must be a number.")
                return
            
            target.db.stress = max(0, min(value, target.db.max_stress))
            self.caller.msg(f"Set {target.name}'s stress to {target.db.stress}/{target.db.max_stress}")

