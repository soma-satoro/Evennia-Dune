"""
Dice Rolling Commands for Modiphus 2d20 Dune System

Implements the Dune 2d20 dice rolling mechanics:
- Target Number = Drive + Skill (what you need to roll under)
- Difficulty = How many successes you need (set by GM, 0-5)
- Roll 2d20 (base) + additional dice from focus/assists/momentum
- Each die ≤ target number = 1 success
- Die = 1 = Critical success (2 successes)
- With focus: Die ≤ skill = Critical success (2 successes)
- Die = 20 = Complication
- Meet or exceed difficulty to succeed
- Extra successes beyond difficulty generate Momentum
"""

import random
from evennia.commands.default.muxcommand import MuxCommand


class CmdRoll(MuxCommand):
    """
    Roll dice using the 2d20 system.

    Usage:
        +roll <drive> + <skill>
        +roll <drive> + <skill> vs <difficulty>
        +roll <drive> + <skill> vs <difficulty> focus
        +roll <drive> + <skill> vs <difficulty> bonus <dice>
        +roll <drive> + <skill> vs <difficulty> threat <dice>
        +roll/determination <drive> + <skill> vs <difficulty>
        +roll/reroll <drive> + <skill> vs <difficulty>
        +roll/assist <assistant> <drive> + <skill> vs <difficulty>
        +roll/opponent <drive> + <skill> [vs <difficulty>] - Opponent rolls first in contest
        +roll/contest <drive> + <skill> - Roll against opponent's successes in contest
        +roll/cost <drive> + <skill> vs <difficulty> (staff - succeed at cost)
        +roll/increase <amount> <drive> + <skill> vs <difficulty> (staff - increase difficulty)
        +roll/private <drive> + <skill> vs <difficulty>

    Switches: 
        /private or /p - Only you see the result
        /determination or /det - Spend 1 determination to set one die to 1 (before rolling)
        /reroll - Spend 1 determination to re-roll all dice (after rolling)
        /assist <character> - Have another character assist with the roll
        /opponent - Opponent rolls first in a contest (sets Difficulty)
        /contest - Active character rolls in a contest (against opponent's successes)
    
    Arguments: drive (duty, faith, justice, power, truth), skill (battle, communicate, discipline, move, understand), difficulty (default: 1, can be 0-5), focus (keyword if you have a relevant focus), bonus <dice> (add bonus dice from assists/momentum)

    The Dune 2d20 System: 
    - Target Number = Drive + Skill (what you need to roll under)
    - Difficulty = How many successes you need (set by GM, default 1)
    - Roll 2d20 (or more with focus/assists)
    - Each die ≤ target number = 1 success
    - Die = 1 = Critical success (2 successes)
    - With focus: Die ≤ skill = Critical success (2 successes)
    - Die = 20 = Complication
    - Meet or exceed difficulty to succeed
    - Extra successes beyond difficulty generate Momentum

    Examples:
        +roll duty + battle | +roll faith + battle vs 2 | +roll power + communicate vs 2 focus
        +roll truth + understand vs 3 bonus 1 | +roll/private justice + discipline vs 0
        +roll battle | +roll battle vs 2 | +roll communicate focus
        +roll/determination duty + battle vs 2 | +roll/assist Anna duty + communicate vs 3
    """
    
    key = "+roll"
    aliases = ["roll", "r"]
    help_category = "Dice"
    
    def func(self):
        """Execute the roll"""
        
        if not self.args:
            self.caller.msg("Usage: +roll <drive> + <skill> [vs <difficulty>] [focus] [bonus <dice>]")
            self.caller.msg("       +roll <skill> [vs <difficulty>] [focus] [bonus <dice>]")
            self.caller.msg("       +roll/determination <drive> + <skill> [vs <difficulty>]")
            self.caller.msg("       +roll/assist <assistant> <drive> + <skill> [vs <difficulty>]")
            self.caller.msg("       +roll/opponent <drive> + <skill> - Opponent rolls first in contest")
            self.caller.msg("       +roll/contest <drive> + <skill> - Roll against opponent in contest")
            self.caller.msg("Drives: duty, faith, justice, power, truth")
            self.caller.msg("Skills: battle, communicate, discipline, move, understand")
            self.caller.msg("Note: Skill-only rolls use skill rating as default difficulty (harder!)")
            self.caller.msg("      Determination: Spend 1 point to set one die to 1 (before rolling)")
            self.caller.msg("      Assistance: Another character rolls 1d20 to help (successes only count if main roll succeeds)")
            self.caller.msg("      Contests: Opponent rolls first with /opponent, then active character rolls with /contest")
            return
        
        # Check if character has stats
        if not hasattr(self.caller.db, 'stats'):
            self.caller.msg("Your character does not have stats initialized.")
            return
        
        # Parse the roll command
        # Save original args for assistance parsing
        original_args = self.args.strip()
        args = original_args.lower().strip()
        
        # Extract difficulty (default: 1, but can be 0-5)
        # Track if difficulty was explicitly set
        difficulty_explicit = False
        difficulty = 1
        if " vs " in args:
            difficulty_explicit = True
            parts = args.split(" vs ")
            args = parts[0].strip()
            
            # Parse difficulty and any additional modifiers
            diff_part = parts[1].strip().split()
            try:
                difficulty = int(diff_part[0])
                # Clamp difficulty to valid range (0-5)
                difficulty = max(0, min(5, difficulty))
            except (ValueError, IndexError):
                difficulty = 1
        
        # Check for focus - also check if character actually has a relevant focus
        has_focus = "focus" in self.args.lower()
        # We'll check for actual focus later after we know the skill
        
        # Check for bonus dice (from Momentum or Threat)
        bonus_dice = 0
        use_threat_for_dice = False
        
        if "bonus" in args:
            bonus_idx = args.split().index("bonus")
            try:
                bonus_dice = int(args.split()[bonus_idx + 1])
            except (ValueError, IndexError):
                bonus_dice = 0
            # Remove bonus part from args
            args = " ".join([w for w in args.split() if w not in ["bonus", str(bonus_dice)]])
        
        # Check for threat dice (buying dice with Threat instead of Momentum)
        if "threat" in args:
            threat_idx = args.split().index("threat")
            try:
                threat_dice = int(args.split()[threat_idx + 1])
                bonus_dice = threat_dice
                use_threat_for_dice = True
            except (ValueError, IndexError):
                pass
            # Remove threat part from args
            args = " ".join([w for w in args.split() if w not in ["threat", str(bonus_dice)]])
        
        # Check for succeed at cost (staff only)
        succeed_at_cost = "cost" in self.switches
        if succeed_at_cost and not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can declare a roll to succeed at cost.|n")
            return
        
        # Check for difficulty increase (staff only, before rolling)
        difficulty_increase = 0
        if "increase" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("|rOnly staff can increase difficulty.|n")
                return
            # Parse increase amount from args
            if self.args:
                args_parts = self.args.split()
                try:
                    difficulty_increase = int(args_parts[0])
                except (ValueError, IndexError):
                    pass
        
        # Check for determination usage (before rolling - set one die to 1)
        use_determination = "determination" in self.switches or "det" in self.switches
        if use_determination:
            if not hasattr(self.caller.db, 'determination'):
                self.caller.db.determination = 1  # Start with 1 per adventure
            if self.caller.db.determination < 1:
                self.caller.msg("|rYou don't have any Determination points to spend.|n")
                return
        
        # Check for assistance (parse assistant name from original args before processing)
        assistant = None
        assistant_name = None
        if "assist" in self.switches:
            # Parse assistant name from original args (first word)
            assist_parts = original_args.split(None, 1)  # Split on first space only
            if assist_parts:
                assistant_name = assist_parts[0]
                # Find the assistant
                assistant = self.caller.search(assistant_name)
                if not assistant:
                    return
                if not hasattr(assistant.db, 'stats'):
                    self.caller.msg(f"{assistant.name} does not have stats initialized.")
                    return
                # Update args to remove assistant name for further parsing
                if len(assist_parts) > 1:
                    args = assist_parts[1].lower().strip()
                else:
                    self.caller.msg("Usage: +roll/assist <assistant> <drive> + <skill> [vs <difficulty>]")
                    return
        
        # Parse drive and skill - support both skill-only and drive+skill
        using_drive = "+" in args
        drive_name = None
        drive_rating = 0
        
        if using_drive:
            # Drive + Skill format: +roll duty + battle
            parts = args.split("+")
            if len(parts) < 2:
                self.caller.msg("Usage: +roll <drive> + <skill> or +roll <skill>")
                return
            
            drive_name = parts[0].strip()
            skill_name = parts[1].strip().split()[0]  # Take first word in case of other modifiers
            
            # Validate drive
            valid_drives = ["duty", "faith", "justice", "power", "truth"]
            if drive_name not in valid_drives:
                self.caller.msg(f"Invalid drive. Choose from: {', '.join(valid_drives)}")
                return
            
            # Get drive value
            drives = self.caller.db.stats.get("drives", {})
            drive_data = drives.get(drive_name) if drives else None
            
            # Handle _SaverDict or regular dict
            if drive_data and hasattr(drive_data, 'get'):
                # Convert _SaverDict to regular dict to get rating
                try:
                    drive_dict = dict(drive_data) if drive_data else {}
                    drive_rating = drive_dict.get("rating", 0) if isinstance(drive_dict, dict) else 0
                except (TypeError, ValueError):
                    # Fallback to direct access
                    drive_rating = drive_data.get("rating", 0) if hasattr(drive_data, 'get') else 0
            elif isinstance(drive_data, dict):
                drive_rating = drive_data.get("rating", 0)
            else:
                # Legacy format or not found - treat as 0
                drive_rating = 0
            
            if drive_rating == 0:
                self.caller.msg(f"|rError:|n Your {drive_name} drive has no rating set. Use +stats/drive to set drive ratings.")
                return
            
            # Check if drive is crossed out
            if self.caller.is_drive_crossed_out(drive_name):
                self.caller.msg(f"|rError:|n Your {drive_name} drive is crossed out and cannot be used.|n")
                self.caller.msg(f"|yUse +determination/recover {drive_name} (staff) or choose a different drive.|n")
                return
        else:
            # Skill-only format: +roll battle
            skill_name = args.strip().split()[0]  # Take first word in case of other modifiers
        
        # Validate skill
        valid_skills = ["battle", "communicate", "discipline", "move", "understand"]
        if skill_name not in valid_skills:
            self.caller.msg(f"Invalid skill. Choose from: {', '.join(valid_skills)}")
            return
        
        # Get skill value (skills are stored as direct values, not dicts)
        skills = self.caller.db.stats.get("skills", {})
        skill_rating = skills.get(skill_name, 0)
        
        if skill_rating == 0:
            self.caller.msg(f"|rError:|n Your {skill_name} skill has no rating set. Use +stats to set skill ratings.")
            return
        
        # Calculate target number and default difficulty
        if using_drive:
            # Drive + Skill: target = drive + skill, default difficulty = 1
            target_number = drive_rating + skill_rating
            if not difficulty_explicit:
                difficulty = 1
        else:
            # Skill-only: target = skill, default difficulty = skill rating
            target_number = skill_rating
            if not difficulty_explicit:
                difficulty = skill_rating
                difficulty_explicit = True  # Treat skill rating as explicit difficulty
        
        # Check if character actually has a relevant focus for this skill
        actual_focus = False
        if has_focus:
            focuses = self.caller.db.stats.get("focuses", [])
            # Check if any focus matches this skill (simplified check)
            from commands.dune.CmdSheet import DUNE_FOCUSES
            valid_focuses = DUNE_FOCUSES.get(skill_name, [])
            for focus in focuses:
                focus_lower = focus.lower()
                # Check if focus matches (handles "music/baliset" format)
                if "/" in focus_lower:
                    base_focus = focus_lower.split("/")[0].strip()
                else:
                    base_focus = focus_lower
                
                for valid_focus in valid_focuses:
                    if base_focus == valid_focus.lower():
                        actual_focus = True
                        break
                if actual_focus:
                    break
        
        # Calculate number of dice (base 2, +1 for focus, +bonus dice)
        num_dice = 2
        if actual_focus:
            num_dice += 1
        num_dice += bonus_dice
        
        # Handle buying dice with Threat or Momentum
        threat_spent_for_dice = 0
        momentum_spent_for_dice = 0
        if bonus_dice > 0:
            if use_threat_for_dice:
                # Buying dice with Threat ADDS to Threat pool (cost: 1, 2, 3 for 1st, 2nd, 3rd die)
                threat_cost = sum(range(1, bonus_dice + 1))  # 1 + 2 + 3 = 6 for 3 dice
                if self.caller.location:
                    if not hasattr(self.caller.location.db, 'threat'):
                        self.caller.location.db.threat = 0
                    self.caller.location.db.threat += threat_cost
                    threat_spent_for_dice = threat_cost
                    self.caller.msg(f"|yBought {bonus_dice} die/dice, adding {threat_cost} Threat to the scene.|n")
                else:
                    self.caller.msg("|rNo location available.|n")
                    return
            else:
                # Buying dice with Momentum (cost: 1, 2, 3 for 1st, 2nd, 3rd die)
                momentum_cost = sum(range(1, bonus_dice + 1))
                if hasattr(self.caller.db, 'momentum') and self.caller.db.momentum >= momentum_cost:
                    self.caller.db.momentum -= momentum_cost
                    momentum_spent_for_dice = momentum_cost
                    self.caller.msg(f"|yBought {bonus_dice} die/dice with {momentum_cost} Momentum.|n")
                else:
                    current_momentum = getattr(self.caller.db, 'momentum', 0)
                    self.caller.msg(f"|rNot enough Momentum. Need {momentum_cost}, have {current_momentum}.|n")
                    self.caller.msg("|yYou can buy dice with Threat instead: +roll ... threat <dice>|n")
                    return
        
        # Roll the dice
        rolls = [random.randint(1, 20) for _ in range(num_dice)]
        
        # Apply determination (set one die to 1 before rolling)
        if use_determination:
            if self.caller.spend_determination(1):
                # Set the first die to 1 (critical success)
                if rolls:
                    rolls[0] = 1
                self.caller.msg("|ySpent 1 Determination - one die set to 1 (critical success)!|n")
            else:
                self.caller.msg("|rFailed to spend Determination.|n")
                return
        
        # Calculate results
        # In Dune: 
        # - Die = 1: Critical success (2 successes)
        # - Die ≤ skill (if focus): Critical success (2 successes) 
        # - Die ≤ target (Drive + Skill): Success (1 success)
        # - Die = 20: Complication
        successes = 0
        complications = 0
        critical_rolls = []
        complication_rolls = []
        success_rolls = []
        fail_rolls = []
        
        for roll in rolls:
            if roll == 1:
                successes += 2  # Critical success (always 2 successes on 1)
                critical_rolls.append(roll)
            elif roll == 20:
                complications += 1
                complication_rolls.append(roll)
            elif actual_focus and roll <= skill_rating:
                # With focus: die ≤ skill = critical success (2 successes)
                successes += 2
                critical_rolls.append(roll)
            elif roll <= target_number:
                # Regular success: die ≤ target number
                successes += 1
                success_rolls.append(roll)
            else:
                fail_rolls.append(roll)
        
        # Handle assistance (assistants roll 1d20 each)
        assistant_successes = 0
        assistant_complications = 0
        assistant_output = []
        
        if assistant:
            # Assistant needs to specify their drive + skill
            # For now, we'll prompt them or use the same drive/skill as the main roller
            # Actually, the assistant should specify their own drive + skill in the command
            # But for simplicity, let's assume they use the same skill and need to specify drive
            # Or we can make it so the assistant uses the same drive+skill as specified
            
            # For assistance, the assistant rolls 1d20 with their own drive + skill
            # We'll use the same drive and skill as the main roller (assistant must have them)
            if using_drive:
                # Get assistant's drive and skill
                assist_drives = assistant.db.stats.get("drives", {})
                assist_drive_data = assist_drives.get(drive_name) if assist_drives else None
                
                if assist_drive_data and hasattr(assist_drive_data, 'get'):
                    try:
                        assist_drive_dict = dict(assist_drive_data) if assist_drive_data else {}
                        assist_drive_rating = assist_drive_dict.get("rating", 0) if isinstance(assist_drive_dict, dict) else 0
                    except (TypeError, ValueError):
                        assist_drive_rating = assist_drive_data.get("rating", 0) if hasattr(assist_drive_data, 'get') else 0
                elif isinstance(assist_drive_data, dict):
                    assist_drive_rating = assist_drive_data.get("rating", 0)
                else:
                    assist_drive_rating = 0
                
                assist_skills = assistant.db.stats.get("skills", {})
                assist_skill_rating = assist_skills.get(skill_name, 0)
                
                if assist_drive_rating == 0 or assist_skill_rating == 0:
                    self.caller.msg(f"|r{assistant.name} doesn't have {drive_name} drive or {skill_name} skill set.|n")
                    return
                
                assist_target = assist_drive_rating + assist_skill_rating
                
                # Assistant rolls 1d20
                assist_roll = random.randint(1, 20)
                
                # Calculate assistant's result
                if assist_roll == 1:
                    assistant_successes = 2  # Critical
                    assistant_output.append(f"{assistant.name} assists: |g{assist_roll} (CRITICAL - 2 successes!)|n")
                elif assist_roll == 20:
                    assistant_complications = 1
                    assistant_output.append(f"{assistant.name} assists: |m{assist_roll} (COMPLICATION!)|n")
                elif assist_roll <= assist_target:
                    assistant_successes = 1
                    assistant_output.append(f"{assistant.name} assists: |c{assist_roll} (success)|n")
                else:
                    assistant_output.append(f"{assistant.name} assists: |r{assist_roll} (fail)|n")
                
                # Add assistant successes only if main roller has at least 1 success
                if successes > 0:
                    successes += assistant_successes
                    assistant_output.append(f"|g{assistant.name} adds {assistant_successes} success(es) to the roll!|n")
                else:
                    assistant_output.append(f"|y{assistant.name} rolled {assistant_successes} success(es), but main roll had no successes, so they don't count.|n")
                
                # Add assistant complications to total
                complications += assistant_complications
            else:
                self.caller.msg("|rAssistance requires a drive + skill roll. Use: +roll/assist <name> <drive> + <skill>|n")
                return
        
        # Determine outcome
        success = successes >= difficulty
        
        # Handle contest resolution
        contest_resolved = False
        is_contest = "contest" in self.switches
        room = self.caller.location if self.caller.location else None
        
        if is_contest and room and hasattr(room.db, 'pending_contest') and room.db.pending_contest:
            contest_data = room.db.pending_contest
            opponent = contest_data.get("opponent")
            
            if success:
                # Active character wins - they get Momentum as normal
                momentum_generated = max(0, successes - difficulty)
                contest_resolved = True
                if room:
                    room.msg_contents(
                        f"|g{self.caller.name} wins the contest against {opponent.name}!|n",
                        exclude=[self.caller, opponent] if opponent != self.caller else self.caller
                    )
            else:
                # Active character loses - opponent gets Momentum
                momentum_generated = 0
                opponent_momentum = difficulty - successes  # Momentum for opponent
                contest_resolved = True
                
                # Give Momentum to opponent (if they're a character with momentum tracking)
                if opponent and hasattr(opponent.db, 'momentum'):
                    current_opponent_momentum = opponent.db.momentum
                    new_opponent_momentum = min(6, current_opponent_momentum + opponent_momentum)
                    opponent.db.momentum = new_opponent_momentum
                    if room:
                        room.msg_contents(
                            f"|r{self.caller.name} fails the contest! {opponent.name} gains {opponent_momentum} Momentum (Pool: {new_opponent_momentum}/6).|n"
                        )
                else:
                    # NPC opponent - could add to Threat or just note it
                    if room:
                        room.msg_contents(
                            f"|r{self.caller.name} fails the contest! {opponent.name} gains {opponent_momentum} Momentum.|n"
                        )
                
                # Clear pending contest
                room.db.pending_contest = None
        else:
            # Normal roll - calculate Momentum as usual
            momentum_generated = max(0, successes - difficulty) if success else 0
        
        # Add generated Momentum to pool (capped at 6 for group pool)
        momentum_added = 0
        if momentum_generated > 0:
            if not hasattr(self.caller.db, 'momentum'):
                self.caller.db.momentum = 0
            # Add momentum, but cap at 6 for the group pool
            current_momentum = self.caller.db.momentum
            new_momentum = min(6, current_momentum + momentum_generated)
            momentum_added = new_momentum - current_momentum
            self.caller.db.momentum = new_momentum
        
        # Clear contest state if resolved
        if contest_resolved and room and hasattr(room.db, 'pending_contest'):
            room.db.pending_contest = None
        
        # Handle extended task contribution
        extended_task_points = 0
        extended_task_name = None
        if room and hasattr(room.db, 'extended_tasks') and room.db.extended_tasks and success:
            # Check if caller is contributing to any extended task
            for task_name, task_data in room.db.extended_tasks.items():
                contributing = task_data.get("contributing", [])
                if self.caller in contributing:
                    extended_task_name = task_name
                    
                    # Check max attempts
                    max_attempts = task_data.get("max_attempts")
                    attempts = task_data.get("attempts", 0)
                    if max_attempts and attempts >= max_attempts:
                        self.caller.msg(f"|rExtended task '{task_name}' has reached maximum attempts ({max_attempts}).|n")
                        contributing.remove(self.caller)
                        break
                    
                    # Calculate points: base 2, reduced by complications, can be increased
                    points = 2
                    points -= complications  # Each complication reduces by 1
                    
                    # Check for traits that might add points (GM discretion, but we'll note it)
                    # Assets with Quality 1+ would add points (not implemented yet)
                    # Momentum can be spent to increase points (handled separately)
                    
                    # Ensure points is at least 0
                    points = max(0, points)
                    
                    # Add points to task
                    task_data["points"] = task_data.get("points", 0) + points
                    task_data["attempts"] = attempts + 1
                    extended_task_points = points
                    
                    # Remove from contributing list
                    contributing.remove(self.caller)
                    
                    # Check if task is complete
                    current_points = task_data["points"]
                    requirement = task_data.get("requirement", 0)
                    
                    if current_points >= requirement:
                        # Task complete!
                        if room:
                            room.msg_contents(
                                f"|gExtended task '{task_name}' is COMPLETE! ({current_points}/{requirement} points)|n"
                            )
                        # Task will be removed by staff or can auto-complete
                    break
        
        # Format the output
        output = []
        output.append("|w" + "=" * 78 + "|n")
        if is_contest:
            contest_info = room.db.pending_contest if room and hasattr(room.db, 'pending_contest') and room.db.pending_contest else None
            if contest_info:
                opponent = contest_info.get("opponent")
                output.append(f"|wCONTEST: {self.caller.name} vs {opponent.name}|n")
        if using_drive:
            output.append(f"|w{self.caller.name} rolls {drive_name.title()} + {skill_name.title()}|n")
            output.append("|w" + "-" * 78 + "|n")
            output.append(f"Target Number (Drive + Skill): |c{target_number}|n  Difficulty: |c{difficulty}|n  Dice: |c{num_dice}d20|n")
        else:
            output.append(f"|w{self.caller.name} rolls {skill_name.title()}|n")
            output.append("|w" + "-" * 78 + "|n")
            output.append(f"Target Number (Skill): |c{target_number}|n  Difficulty: |c{difficulty}|n  Dice: |c{num_dice}d20|n")
            output.append("|y(Skill-only roll - harder without a Drive)|n")
        
        if is_contest:
            output.append("|y(CONTEST - Difficulty set by opponent's successes)|n")
        
        if actual_focus:
            output.append(f"|g(Using relevant Focus - dice ≤ {skill_rating} are criticals)|n")
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
        
        # Add assistant output
        if assistant_output:
            output.append("")
            output.extend(assistant_output)
        
        output.append("")
        
        # Results
        output.append(f"Successes: |w{successes}|n")
        
        # Only show success/failure if difficulty was explicitly set
        if difficulty_explicit:
            if success:
                if succeed_at_cost:
                    output.append("|ySUCCESS AT COST!|n")
                    output.append("|yGM will determine extra complications. No Momentum generated.|n")
                else:
                    output.append("|gSUCCESS!|n")
                    if momentum_generated > 0:
                        current_momentum = self.caller.db.momentum
                        if momentum_added < momentum_generated:
                            output.append(f"|yGenerated {momentum_generated} Momentum, but only {momentum_added} added (pool at maximum 6)!|n")
                        else:
                            output.append(f"|yGenerated {momentum_generated} Momentum! (Pool: {current_momentum}/6)|n")
            else:
                output.append("|rFAILURE!|n")
        else:
            # No explicit difficulty - just show successes and momentum
            if momentum_generated > 0:
                current_momentum = self.caller.db.momentum
                if momentum_added < momentum_generated:
                    output.append(f"|yGenerated {momentum_generated} Momentum, but only {momentum_added} added (pool at maximum 6)!|n")
                else:
                    output.append(f"|yGenerated {momentum_generated} Momentum! (Pool: {current_momentum}/6)|n")
        
        if complications > 0:
            output.append(f"|m{complications} Complication{'s' if complications > 1 else ''}!|n")
            output.append(f"|yUse +complication/add <skill>=<name> to set a complication.|n")
            output.append(f"|yExample: +complication/add {skill_name}=Bruised|n")
        
        # Show extended task contribution
        if extended_task_name and extended_task_points > 0:
            if room and hasattr(room.db, 'extended_tasks') and room.db.extended_tasks:
                task_data = room.db.extended_tasks.get(extended_task_name)
                if task_data:
                    current_points = task_data.get("points", 0)
                    requirement = task_data.get("requirement", 0)
                    output.append(f"|yExtended Task '{extended_task_name}': +{extended_task_points} points ({current_points}/{requirement})|n")
                    if current_points >= requirement:
                        output.append(f"|gExtended task '{extended_task_name}' is COMPLETE!|n")
        
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
    
    Determination is tied to drive statements. When your drive statement supports
    an action, you can spend Determination for benefits. When it conflicts, the GM
    may offer Determination for you to choose: comply (suffer complication) or
    challenge (cross out drive, act freely).
    
    Usage:
        +determination - View your determination
        +determination/reroll - Re-roll dice after a roll (spend 1 Determination)
        +determination/declaration <trait> - Create/change/remove a trait (spend 1 Determination)
        +determination/extra - Take an extra action in conflict (spend 1 Determination)
        +determination/comply <drive> - Comply with conflicting drive (suffer complication, gain 1 Determination)
        +determination/challenge <drive> - Challenge conflicting drive (cross it out, act freely, gain 1 Determination)
        +determination/refuse <drive> - Refuse offered Determination, choose different drive
        +determination/recover <drive> - Recover a crossed out drive (staff)
        +determination/add <character>=<amount> - Award determination (staff)
        
    Switches:
        /reroll - Re-roll any number of d20s after rolling
        /declaration - Create/change/remove a trait
        /extra - Take an extra action in conflict
        /comply - Comply with conflicting drive (suffer complication)
        /challenge - Challenge conflicting drive (cross it out)
        /refuse - Refuse offered Determination
        /recover - Recover a crossed out drive (staff)
        /add - Award determination to a character (staff)
        
    Determination Benefits (when drive supports action):
        - Automatic 1: Set one die to 1 before rolling (use +roll/determination)
        - Re-roll: Re-roll any number of d20s after rolling
        - Declaration: Create/change/remove a trait
        - Extra Action: Take an additional action in conflict
        
    Drive Conflicts:
        - If drive statement conflicts with action, GM may offer Determination
        - Comply: Suffer a complication, gain 1 Determination
        - Challenge: Cross out drive, act freely, gain 1 Determination
        - Refuse: Choose a different drive for the test
        
    Examples:
        +determination - Check your determination
        +determination/reroll - Re-roll dice after a failed roll
        +determination/declaration "Always Prepared" - Create a trait
        +determination/comply duty - Comply with duty drive conflict
        +determination/challenge faith - Challenge faith drive conflict
    """
    
    key = "+determination"
    aliases = ["determination", "det"]
    help_category = "Character"
    
    def func(self):
        """Manage determination"""
        
        if not hasattr(self.caller.db, 'determination'):
            self.caller.db.determination = 1  # Start with 1 per adventure
        
        # No switches - display current determination and crossed out drives
        if not self.switches:
            crossed_out = getattr(self.caller.db, 'crossed_out_drives', [])
            self.caller.msg(f"|wDetermination:|n {self.caller.db.determination}/3")
            if crossed_out:
                self.caller.msg(f"|rCrossed out drives:|n {', '.join([d.title() for d in crossed_out])}")
            return
        
        # Re-roll dice (after a roll)
        if "reroll" in self.switches:
            self.caller.msg("|yRe-roll functionality: Use this after a roll to re-roll any number of d20s.|n")
            self.caller.msg("|yThis requires spending 1 Determination and should be done immediately after rolling.|n")
            # Note: Actual re-roll would need to be integrated with roll command
            if self.caller.spend_determination(1):
                self.caller.msg("|gSpent 1 Determination for re-roll. Work with GM to re-roll dice.|n")
            else:
                self.caller.msg("|rYou don't have enough Determination.|n")
        
        # Declaration - create/change/remove trait
        elif "declaration" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +determination/declaration <trait name>")
                self.caller.msg("Example: +determination/declaration 'Always Prepared'")
                return
            
            if self.caller.db.determination < 1:
                self.caller.msg("|rYou don't have enough Determination.|n")
                return
            
            trait_name = self.args.strip()
            # Check if trait exists
            traits = self.caller.db.stats.get("talents", [])
            if not traits:
                traits = self.caller.db.stats.get("traits", [])
            
            if trait_name in traits:
                # Remove existing trait
                if "talents" in self.caller.db.stats:
                    self.caller.db.stats["talents"].remove(trait_name)
                elif "traits" in self.caller.db.stats:
                    self.caller.db.stats["traits"].remove(trait_name)
                self.caller.spend_determination(1)
                self.caller.msg(f"|gRemoved trait '{trait_name}' (spent 1 Determination).|n")
            else:
                # Add new trait
                if "talents" not in self.caller.db.stats:
                    self.caller.db.stats["talents"] = []
                self.caller.db.stats["talents"].append(trait_name)
                self.caller.spend_determination(1)
                self.caller.msg(f"|gCreated trait '{trait_name}' (spent 1 Determination).|n")
                self.caller.msg("|yYou may retroactively describe how this trait came to be.|n")
        
        # Extra action in conflict
        elif "extra" in self.switches:
            if self.caller.spend_determination(1):
                self.caller.msg("|gSpent 1 Determination for an extra action in conflict.|n")
                if self.caller.location:
                    self.caller.location.msg_contents(
                        f"|c{self.caller.name} takes an extra action!|n",
                        exclude=self.caller
                    )
            else:
                self.caller.msg("|rYou don't have enough Determination.|n")
        
        # Comply with conflicting drive
        elif "comply" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +determination/comply <drive>")
                return
            
            drive_name = self.args.strip().lower()
            valid_drives = ["duty", "faith", "justice", "power", "truth"]
            if drive_name not in valid_drives:
                self.caller.msg(f"|rInvalid drive. Valid drives: {', '.join(valid_drives)}|n")
                return
            
            # Gain Determination and suffer a complication
            self.caller.gain_determination(1)
            self.caller.msg(f"|yYou comply with your {drive_name} drive.|n")
            self.caller.msg(f"|gGained 1 Determination (now {self.caller.db.determination}/3).|n")
            self.caller.msg(f"|rYou immediately suffer a complication from the conflict.|n")
            self.caller.msg(f"|yUse +complication/add to set the complication.|n")
        
        # Challenge conflicting drive
        elif "challenge" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +determination/challenge <drive>")
                return
            
            drive_name = self.args.strip().lower()
            valid_drives = ["duty", "faith", "justice", "power", "truth"]
            if drive_name not in valid_drives:
                self.caller.msg(f"|rInvalid drive. Valid drives: {', '.join(valid_drives)}|n")
                return
            
            # Cross out drive and gain Determination
            self.caller.cross_out_drive(drive_name)
            self.caller.gain_determination(1)
            self.caller.msg(f"|yYou challenge your {drive_name} drive.|n")
            self.caller.msg(f"|r{drive_name.title()} drive is now crossed out and cannot be used until recovered.|n")
            self.caller.msg(f"|gGained 1 Determination (now {self.caller.db.determination}/3).|n")
            self.caller.msg(f"|yYou may act freely now.|n")
        
        # Refuse offered Determination
        elif "refuse" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +determination/refuse <drive>")
                return
            
            drive_name = self.args.strip().lower()
            self.caller.msg(f"|yYou refuse the offered Determination for {drive_name} drive.|n")
            self.caller.msg(f"|yChoose a different drive for your skill test.|n")
        
        # Recover crossed out drive (staff)
        elif "recover" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("|rOnly staff can recover crossed out drives.|n")
                return
            
            if not self.args:
                self.caller.msg("Usage: +determination/recover <drive>")
                return
            
            drive_name = self.args.strip().lower()
            valid_drives = ["duty", "faith", "justice", "power", "truth"]
            if drive_name not in valid_drives:
                self.caller.msg(f"|rInvalid drive. Valid drives: {', '.join(valid_drives)}|n")
                return
            
            if self.caller.is_drive_crossed_out(drive_name):
                self.caller.recover_drive(drive_name)
                self.caller.msg(f"|gRecovered {drive_name} drive. It can now be used again.|n")
            else:
                self.caller.msg(f"|r{drive_name.title()} drive is not crossed out.|n")
        
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
            self.caller.msg(f"Awarded {amount} determination to {target.name}. Their total: {target.db.determination}/3")
            target.msg(f"|gYou have been awarded {amount} determination!|n")

