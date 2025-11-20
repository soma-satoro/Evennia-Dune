"""
Dice Rolling Commands for Modiphus 2d20 System

Implements the 2d20 dice rolling mechanics:
- Roll 2d20 (base) + additional dice from assists/momentum
- Compare each die to target number (Attribute + Skill)
- Dice that roll equal or under the target are successes
- Rolling a 1 is a critical success (2 successes)
- Rolling a 20 is a complication
- Extra successes beyond the difficulty generate Momentum
"""

import random
from evennia.commands.default.muxcommand import MuxCommand


class CmdRoll(MuxCommand):
    """
    Roll dice using the 2d20 system.
    
    Usage:
        +roll <attribute> + <skill>
        +roll <attribute> + <skill> vs <difficulty>
        +roll <attribute> + <skill> vs <difficulty> focus
        +roll <attribute> + <skill> vs <difficulty> bonus <dice>
        +roll/private <attribute> + <skill> vs <difficulty>
        
    Switches:
        /private or /p - Only you see the result
        
    Arguments:
        attribute - One of: control, dexterity, fitness, insight, presence, reason
        skill - One of: battle, communicate, discipline, move, understand
        difficulty - Target number of successes needed (default: 1)
        focus - Include this keyword if you have a relevant focus
        bonus <dice> - Add bonus dice from assists/momentum (e.g., "bonus 2")
        
    The 2d20 System:
        - Roll 2d20 (or more with assists)
        - Each die that rolls equal or under (Attribute + Skill) is a success
        - Rolling a 1 generates 2 successes (critical!)
        - Rolling a 20 is a complication
        - Having a relevant focus lets you roll an extra d20
        - You need to meet or exceed the difficulty to succeed
        - Extra successes generate Momentum for the group
        
    Examples:
        +roll fitness + battle - Simple roll
        +roll fitness + battle vs 2 - Roll against difficulty 2
        +roll fitness + battle vs 2 focus - Roll with a relevant focus
        +roll control + communicate vs 3 bonus 1 - Roll with 1 bonus die
        +roll/private insight + understand vs 2 - Private roll only you see
    """
    
    key = "+roll"
    aliases = ["roll", "r"]
    help_category = "Dice"
    
    def func(self):
        """Execute the roll"""
        
        if not self.args:
            self.caller.msg("Usage: +roll <attribute> + <skill> vs <difficulty> [focus] [bonus <dice>]")
            return
        
        # Check if character has stats
        if not hasattr(self.caller.db, 'stats'):
            self.caller.msg("Your character does not have stats initialized.")
            return
        
        # Parse the roll command
        args = self.args.lower().strip()
        
        # Extract difficulty
        difficulty = 1
        if " vs " in args:
            parts = args.split(" vs ")
            args = parts[0].strip()
            
            # Parse difficulty and any additional modifiers
            diff_part = parts[1].strip().split()
            try:
                difficulty = int(diff_part[0])
            except (ValueError, IndexError):
                difficulty = 1
        
        # Check for focus
        has_focus = "focus" in self.args.lower()
        
        # Check for bonus dice
        bonus_dice = 0
        if "bonus" in args:
            bonus_idx = args.split().index("bonus")
            try:
                bonus_dice = int(args.split()[bonus_idx + 1])
            except (ValueError, IndexError):
                bonus_dice = 0
            # Remove bonus part from args
            args = " ".join([w for w in args.split() if w not in ["bonus", str(bonus_dice)]])
        
        # Parse attribute and skill
        if "+" not in args:
            self.caller.msg("Usage: +roll <attribute> + <skill>")
            return
        
        parts = args.split("+")
        if len(parts) < 2:
            self.caller.msg("Usage: +roll <attribute> + <skill>")
            return
        
        attr_name = parts[0].strip()
        skill_name = parts[1].strip().split()[0]  # Take first word in case of other modifiers
        
        # Validate attribute
        valid_attrs = ["control", "dexterity", "fitness", "insight", "presence", "reason"]
        if attr_name not in valid_attrs:
            self.caller.msg(f"Invalid attribute. Choose from: {', '.join(valid_attrs)}")
            return
        
        # Validate skill
        valid_skills = ["battle", "communicate", "discipline", "move", "understand"]
        if skill_name not in valid_skills:
            self.caller.msg(f"Invalid skill. Choose from: {', '.join(valid_skills)}")
            return
        
        # Get attribute and skill values
        attribute = self.caller.get_attribute(attr_name)
        skill = self.caller.get_skill(skill_name)
        target_number = attribute + skill
        
        # Determine number of dice
        num_dice = 2  # Base
        if has_focus:
            num_dice += 1
        num_dice += bonus_dice
        
        # Roll the dice!
        rolls = [random.randint(1, 20) for _ in range(num_dice)]
        
        # Calculate results
        successes = 0
        complications = 0
        critical_rolls = []
        complication_rolls = []
        success_rolls = []
        fail_rolls = []
        
        for roll in rolls:
            if roll == 1:
                successes += 2  # Critical success!
                critical_rolls.append(roll)
            elif roll == 20:
                complications += 1
                complication_rolls.append(roll)
            elif roll <= target_number:
                successes += 1
                success_rolls.append(roll)
            else:
                fail_rolls.append(roll)
        
        # Determine outcome
        success = successes >= difficulty
        momentum_generated = max(0, successes - difficulty) if success else 0
        
        # Format the output
        output = []
        output.append("|w" + "=" * 78 + "|n")
        output.append(f"|w{self.caller.name} rolls {attr_name.title()} + {skill_name.title()}|n")
        output.append("|w" + "-" * 78 + "|n")
        output.append(f"Target Number: |c{target_number}|n  Difficulty: |c{difficulty}|n  Dice: |c{num_dice}d20|n")
        
        if has_focus:
            output.append("|g(Using relevant Focus)|n")
        if bonus_dice > 0:
            output.append(f"|y(+{bonus_dice} bonus dice)|n")
        
        output.append("")
        
        # Display rolls
        roll_display = []
        if critical_rolls:
            roll_display.append("|g" + ", ".join(str(r) for r in critical_rolls) + " (CRITICAL!)|n")
        if success_rolls:
            roll_display.append("|c" + ", ".join(str(r) for r in success_rolls) + " (success)|n")
        if fail_rolls:
            roll_display.append("|r" + ", ".join(str(r) for r in fail_rolls) + " (fail)|n")
        if complication_rolls:
            roll_display.append("|m" + ", ".join(str(r) for r in complication_rolls) + " (COMPLICATION!)|n")
        
        output.append("Rolls: " + " ".join(roll_display))
        output.append("")
        
        # Results
        output.append(f"Successes: |w{successes}|n")
        
        if success:
            output.append("|gSUCCESS!|n")
            if momentum_generated > 0:
                output.append(f"|yGenerate {momentum_generated} Momentum!|n")
        else:
            output.append("|rFAILURE!|n")
        
        if complications > 0:
            output.append(f"|m{complications} Complication{'s' if complications > 1 else ''}!|n")
        
        output.append("|w" + "=" * 78 + "|n")
        
        # Send the output
        result_text = "\n".join(output)
        
        if "private" in self.switches or "p" in self.switches:
            # Private roll - only caller sees it
            self.caller.msg(result_text)
            if self.caller.location:
                self.caller.location.msg_contents(
                    f"|w{self.caller.name} makes a private roll.|n",
                    exclude=self.caller
                )
        else:
            # Public roll - everyone in the room sees it
            if self.caller.location:
                self.caller.location.msg_contents(result_text)
            else:
                self.caller.msg(result_text)


class CmdMomentum(MuxCommand):
    """
    Manage the group Momentum pool.
    
    Usage:
        +momentum - View current momentum
        +momentum/spend <amount> - Spend momentum
        +momentum/add <amount> - Add momentum (staff/GM)
        +momentum/set <amount> - Set momentum (staff/GM)
        +momentum/reset - Reset momentum to 0 (staff/GM)
        
    Switches:
        /spend - Spend momentum points
        /add - Add momentum points (staff/GM)
        /set - Set momentum to specific value (staff/GM)
        /reset - Reset momentum to 0 (staff/GM)
        
    Momentum is a group resource that can be spent to:
        - Add extra dice to rolls
        - Activate special abilities
        - Create advantages in scenes
        - Obtain information
        
    Examples:
        +momentum - Check current momentum
        +momentum/spend 2 - Spend 2 momentum
        +momentum/add 3 - Add 3 momentum (GM)
    """
    
    key = "+momentum"
    aliases = ["momentum", "mom"]
    help_category = "Dice"
    
    def func(self):
        """Manage momentum"""
        
        # Initialize momentum if it doesn't exist
        if not hasattr(self.caller.db, 'momentum'):
            self.caller.db.momentum = 0
        
        # No switches - display current momentum
        if not self.switches:
            self.caller.msg(f"|wGroup Momentum:|n {self.caller.db.momentum}")
            return
        
        # Spend momentum
        if "spend" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +momentum/spend <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            if amount < 1:
                self.caller.msg("You must spend at least 1 momentum.")
                return
            
            if self.caller.db.momentum < amount:
                self.caller.msg(f"Not enough momentum. Current: {self.caller.db.momentum}")
                return
            
            self.caller.db.momentum -= amount
            self.caller.msg(f"Spent {amount} momentum. Current: {self.caller.db.momentum}")
            
            if self.caller.location:
                self.caller.location.msg_contents(
                    f"|y{self.caller.name} spends {amount} Momentum.|n",
                    exclude=self.caller
                )
        
        # Add momentum (staff/GM)
        elif "add" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You don't have permission to add momentum.")
                return
            
            if not self.args:
                self.caller.msg("Usage: +momentum/add <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            self.caller.db.momentum = max(0, self.caller.db.momentum + amount)
            self.caller.msg(f"Added {amount} momentum. Current: {self.caller.db.momentum}")
        
        # Set momentum (staff/GM)
        elif "set" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You don't have permission to set momentum.")
                return
            
            if not self.args:
                self.caller.msg("Usage: +momentum/set <amount>")
                return
            
            try:
                amount = int(self.args.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            self.caller.db.momentum = max(0, amount)
            self.caller.msg(f"Set momentum to {self.caller.db.momentum}")
        
        # Reset momentum (staff/GM)
        elif "reset" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You don't have permission to reset momentum.")
                return
            
            self.caller.db.momentum = 0
            self.caller.msg("Reset momentum to 0")


class CmdDetermination(MuxCommand):
    """
    Manage your character's Determination points.
    
    Usage:
        +determination - View your determination
        +determination/spend - Spend 1 determination for a special action
        +determination/add <character>=<amount> - Award determination (staff)
        
    Switches:
        /spend - Spend 1 determination point
        /add - Award determination to a character (staff)
        
    Determination can be spent to:
        - Re-roll a failed test
        - Perform a heroic action
        - Resist a serious consequence
        - Activate powerful abilities
        
    Examples:
        +determination - Check your determination
        +determination/spend - Spend 1 determination
        +determination/add Paul=1 - Award Paul 1 determination (staff)
    """
    
    key = "+determination"
    aliases = ["determination", "det"]
    help_category = "Character"
    
    def func(self):
        """Manage determination"""
        
        if not hasattr(self.caller.db, 'determination'):
            self.caller.db.determination = 3
        
        # No switches - display current determination
        if not self.switches:
            self.caller.msg(f"|wDetermination:|n {self.caller.db.determination}")
            return
        
        # Spend determination
        if "spend" in self.switches:
            if self.caller.spend_determination(1):
                self.caller.msg(f"Spent 1 determination. Remaining: {self.caller.db.determination}")
                
                if self.caller.location:
                    self.caller.location.msg_contents(
                        f"|c{self.caller.name} spends Determination for a heroic action!|n",
                        exclude=self.caller
                    )
            else:
                self.caller.msg("You don't have any determination left.")
        
        # Add determination (staff)
        elif "add" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You don't have permission to award determination.")
                return
            
            if "=" not in self.args:
                self.caller.msg("Usage: +determination/add <character>=<amount>")
                return
            
            char_name, value_str = self.args.split("=", 1)
            target = self.caller.search(char_name.strip())
            if not target:
                return
            
            try:
                amount = int(value_str.strip())
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            target.gain_determination(amount)
            self.caller.msg(f"Awarded {amount} determination to {target.name}. Their total: {target.db.determination}")
            target.msg(f"|gYou have been awarded {amount} determination!|n")

