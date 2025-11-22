"""
Complication Management Command for Dune 2d20 System

Manages temporary complications that affect characters.
Complications occur when a die rolls 20 on a skill test.
"""

from evennia.commands.default.muxcommand import MuxCommand


# Example complications by skill (for reference)
EXAMPLE_COMPLICATIONS = {
    "battle": [
        "Bruised", "Exhausted", "Flanked", "Injured", "Stunned", "Unarmed"
    ],
    "communicate": [
        "Disconnected", "Gauche", "Inferior", "Outsider", "Rude", "Tongue-tied"
    ],
    "discipline": [
        "Angry", "Conflicted", "Distracted", "Frightened", "Intoxicated", "Unfocused"
    ],
    "move": [
        "Awkward", "Constricted", "Hurt", "Slow", "Tired", "Uncoordinated"
    ],
    "understand": [
        "Complicated", "Confused", "Misinformed", "Overthinking", "Uninformed", "Vague"
    ]
}


class CmdComplication(MuxCommand):
    """
    Manage character complications.
    
    Complications are temporary negative effects that occur when a die rolls 20.
    They can increase difficulty, prevent actions, or cause other problems.
    
    Usage:
        +complication - View your complications
        +complication <character> - View another character's complications (staff)
        +complication/add <skill>=<name> - Add a complication
        +complication/remove <name> - Remove a complication
        +complication/buyoff <name> - Buy off a complication with 2 Threat
        +complication/clear - Clear all complications
        +complication/list [<skill>] - List example complications by skill
        
    Switches:
        /add - Add a complication
        /remove or /rem - Remove a specific complication
        /clear - Clear all complications
        /list - List example complications
        
    Examples:
        +complication - View your complications
        +complication/add battle=Bruised - Add "Bruised" complication from Battle
        +complication/remove Bruised - Remove "Bruised" complication
        +complication/clear - Clear all complications
        +complication/list battle - List example Battle complications
        +complication Paul - View Paul's complications (staff)
    """
    
    key = "+complication"
    aliases = ["complication", "comp", "complications"]
    help_category = "Character"
    
    def func(self):
        """Manage complications"""
        
        # Initialize complications if needed
        if not hasattr(self.caller.db, 'complications'):
            self.caller.db.complications = []
        
        # Determine target character
        target = self.caller
        
        # Check if viewing another character (staff only)
        if self.args and not any(switch in self.switches for switch in ["add", "remove", "rem", "clear", "list"]):
            # Check if it's a character name or a command
            potential_name = self.args.strip()
            # If it looks like a character name and caller is staff
            if self.caller.check_permstring("Builder"):
                found_char = self.caller.search(potential_name)
                if found_char:
                    target = found_char
                    if not hasattr(target.db, 'complications'):
                        target.db.complications = []
                else:
                    # Not a character, treat as regular command
                    target = self.caller
            else:
                target = self.caller
        
        # List example complications
        if "list" in self.switches:
            self._list_examples()
            return
        
        # No switches - show complications
        if not self.switches:
            self._show_complications(target)
            return
        
        # Add complication
        if "add" in self.switches:
            self._add_complication(target)
            return
        
        # Remove complication
        if "remove" in self.switches or "rem" in self.switches:
            self._remove_complication(target)
            return
        
        # Clear all complications
        if "clear" in self.switches:
            self._clear_complications(target)
            return
        
        # Buy off complication with Threat
        if "buyoff" in self.switches:
            self._buyoff_complication(target)
            return
    
    def _show_complications(self, target):
        """Show character's complications"""
        complications = target.db.complications if hasattr(target.db, 'complications') else []
        
        output = []
        output.append("|w" + "=" * 78 + "|n")
        output.append(f"|w{target.name.upper()}'S COMPLICATIONS".center(78) + "|n")
        output.append("|w" + "=" * 78 + "|n")
        
        if not complications:
            output.append("|gNo active complications.|n")
        else:
            for comp in complications:
                skill = comp.get("skill", "unknown").title()
                name = comp.get("name", "Unknown")
                output.append(f"  |r{name}|n ({skill})")
                if comp.get("description"):
                    output.append(f"    {comp['description']}")
        
        output.append("|w" + "=" * 78 + "|n")
        output.append("|cUse +complication/add <skill>=<name> to add a complication.|n")
        output.append("|cUse +complication/remove <name> to remove one.|n")
        output.append("|cUse +complication/buyoff <name> to buy off with 2 Threat.|n")
        
        if target == self.caller:
            self.caller.msg("\n".join(output))
        else:
            self.caller.msg("\n".join(output))
            target.msg(f"|y{self.caller.name} is viewing your complications.|n")
    
    def _add_complication(self, target):
        """Add a complication"""
        # Check permissions if adding to another character
        if target != self.caller and not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou can only add complications to yourself.|n")
            return
        
        if "=" not in self.args:
            self.caller.msg("Usage: +complication/add <skill>=<name>")
            self.caller.msg("Example: +complication/add battle=Bruised")
            return
        
        parts = self.args.split("=", 1)
        skill = parts[0].strip().lower()
        name = parts[1].strip()
        
        # Validate skill
        valid_skills = ["battle", "communicate", "discipline", "move", "understand"]
        if skill not in valid_skills:
            self.caller.msg(f"|rInvalid skill: {skill}|n")
            self.caller.msg(f"Valid skills: {', '.join(valid_skills)}")
            return
        
        # Initialize complications if needed
        if not hasattr(target.db, 'complications'):
            target.db.complications = []
        
        # Check for duplicates (case-insensitive)
        for existing in target.db.complications:
            if existing.get("name", "").lower() == name.lower():
                self.caller.msg(f"|r{target.name} already has the complication: {existing.get('name')}|n")
                return
        
        # Add complication
        complication = {
            "skill": skill,
            "name": name,
            "description": ""  # Can be expanded later
        }
        target.db.complications.append(complication)
        
        if target == self.caller:
            self.caller.msg(f"|rAdded complication: {name} ({skill.title()})|n")
        else:
            self.caller.msg(f"|rAdded complication '{name}' ({skill.title()}) to {target.name}.|n")
            target.msg(f"|rYou have been given the complication: {name} ({skill.title()})|n")
    
    def _remove_complication(self, target):
        """Remove a complication"""
        # Check permissions if removing from another character
        if target != self.caller and not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou can only remove complications from yourself.|n")
            return
        
        if not self.args:
            self.caller.msg("Usage: +complication/remove <name>")
            return
        
        name = self.args.strip()
        
        if not hasattr(target.db, 'complications'):
            target.db.complications = []
        
        complications = target.db.complications
        removed = False
        
        for comp in complications[:]:  # Copy list to avoid modification during iteration
            if comp.get("name", "").lower() == name.lower():
                complications.remove(comp)
                removed = True
                break
        
        if removed:
            if target == self.caller:
                self.caller.msg(f"|gRemoved complication: {name}|n")
            else:
                self.caller.msg(f"|gRemoved complication '{name}' from {target.name}.|n")
                target.msg(f"|gThe complication '{name}' has been removed.|n")
        else:
            self.caller.msg(f"|r{target.name} doesn't have a complication named '{name}'.|n")
    
    def _clear_complications(self, target):
        """Clear all complications"""
        # Check permissions if clearing another character's complications
        if target != self.caller and not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou can only clear your own complications.|n")
            return
        
        if not hasattr(target.db, 'complications'):
            target.db.complications = []
        
        count = len(target.db.complications)
        target.db.complications = []
        
        if target == self.caller:
            self.caller.msg(f"|gCleared {count} complication(s).|n")
        else:
            self.caller.msg(f"|gCleared {count} complication(s) from {target.name}.|n")
            target.msg(f"|gAll your complications have been cleared.|n")
    
    def _list_examples(self):
        """List example complications by skill"""
        skill = None
        if self.args:
            skill = self.args.strip().lower()
        
        output = []
        output.append("|w" + "=" * 78 + "|n")
        output.append("|w" + " EXAMPLE COMPLICATIONS".center(78) + "|n")
        output.append("|w" + "=" * 78 + "|n")
        
        if skill and skill in EXAMPLE_COMPLICATIONS:
            # Show specific skill
            output.append(f"\n|y{skill.upper()}:|n")
            for comp in EXAMPLE_COMPLICATIONS[skill]:
                output.append(f"  • {comp}")
        else:
            # Show all skills
            for skill_name, comps in EXAMPLE_COMPLICATIONS.items():
                output.append(f"\n|y{skill_name.upper()}:|n")
                for comp in comps:
                    output.append(f"  • {comp}")
        
        output.append("\n|w" + "=" * 78 + "|n")
        output.append("|cUse +complication/add <skill>=<name> to add a complication.|n")
        output.append("|cYou can use these examples or create your own.|n")
        
        self.caller.msg("\n".join(output))

