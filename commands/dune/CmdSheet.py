"""
Character Sheet Command

Displays character statistics for the 2d20 Dune system.
"""

from evennia.commands.default.muxcommand import MuxCommand


# Dune-specific focuses organized by skill
DUNE_FOCUSES = {
    "battle": [
        "Assassination",
        "Atomics",
        "Dirty Fighting",
        "Dueling",
        "Evasive Action",
        "Lasgun",
        "Long Blades",
        "Pistols",
        "Rifle",
        "Shield Fighting",
        "Short Blades",
        "Sneak Attacks",
        "Strategy",
        "Tactics",
        "Unarmed Combat",
    ],
    "communicate": [
        "Acting",
        "Bartering",
        "Charm",
        "Deceit",
        "Diplomacy",
        "Disguise",
        "Empathy",
        "Gossip",
        "Innuendo",
        "Inspiration",
        "Interrogation",
        "Intimidation",
        "Linguistics",
        "Listening",
        "Music",  # Requires specification
        "Neurolinguistics",
        "Persuasion",
        "Secret Language",  # Requires specification
        "Teaching",
    ],
    "discipline": [
        "Command",
        "Composure",
        "Espionage",
        "Infiltration",
        "Observe",
        "Precision",
        "Resolve",
        "Self-Control",
        "Survival",  # Requires specification
    ],
    "move": [
        "Acrobatics",
        "Body Control",
        "Climb",
        "Dance",
        "Distance Running",
        "Drive",
        "Escaping",
        "Grace",
        "Pilot",  # Requires specification
        "Stealth",
        "Swift",
        "Swim",
        "Unobtrusive",
        "Worm Rider",
    ],
    "understand": [
        "Advanced Technology",
        "Botany",
        "CHOAM Bureaucracy",
        "Cultural Studies",
        "Danger Sense",
        "Data Analysis",
        "Deductive Reasoning",
        "Ecology",
        "Emergency Medicine",
        "Etiquette",
        "Faction Lore",  # Requires specification
        "Genetics",
        "Geology",
        "House Politics",
        "Imperial Politics",
        "Infectious Diseases",
        "Kanly",
        "Philosophy",
        "Physical Empathy",
        "Physics",
        "Poison",
        "Psychiatry",
        "Religion",
        "Smuggling",
        "Surgery",
        "Traps",
        "Virology",
    ],
}


class CmdSheet(MuxCommand):
    """
    Display your character sheet or another character's sheet (staff only for others).

    Usage:
        +sheet | +sheet <character name> (staff only) | +sheet/full

    Switches: /full - Display extended information including background

    Examples:
        +sheet | +sheet Paul (staff only) | +sheet/full
    """
    
    key = "+sheet"
    aliases = ["sheet"]
    help_category = "Character"
    
    def func(self):
        """Display character sheet"""
        
        # Determine which character to display
        target = self.caller
        
        if self.args:
            # Check if caller has permission to view other sheets
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("|rYou don't have permission to view other people's sheets.|n")
                return
            
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
        
        # If /full switch is used, also display background and bio info
        if "full" in self.switches:
            # Show caste and faction
            caste = target.db.caste
            faction = target.db.faction
            if caste or faction:
                self.caller.msg(f"\n|y{'CASTE & FACTION':-^78}|n")
                if caste:
                    self.caller.msg(f"|wCaste:|n {caste}")
                if faction:
                    self.caller.msg(f"|wFaction:|n {faction}")
                    # Show faction requirements
                    from typeclasses.factions import get_faction, validate_faction_talents, validate_faction_focuses
                    faction_data = get_faction(faction)
                    if faction_data:
                        mandatory_talents = faction_data.get("mandatory_talents", [])
                        mandatory_focuses = faction_data.get("mandatory_focuses", [])
                        if mandatory_talents:
                            talent_valid, _, _ = validate_faction_talents(target, faction)
                            status = "|g✓|n" if talent_valid else "|r✗|n"
                            self.caller.msg(f"|wRequired Talents:|n {status} {', '.join(mandatory_talents)}")
                        if mandatory_focuses:
                            focus_valid, _, _ = validate_faction_focuses(target, faction)
                            status = "|g✓|n" if focus_valid else "|r✗|n"
                            self.caller.msg(f"|wRequired Focuses:|n {status} {', '.join(mandatory_focuses)}")
                self.caller.msg("|w" + "=" * 78 + "|n")
            
            # Show archetype info
            archetype = target.db.chargen_archetype
            if archetype:
                self.caller.msg(f"\n|y{'ARCHETYPE':-^78}|n")
                self.caller.msg(f"|wTrait:|n {archetype.get('trait', 'Unknown')}")
                if archetype.get('category'):
                    self.caller.msg(f"|wCategory:|n {archetype['category']}")
                if archetype.get('description'):
                    self.caller.msg(f"|wDescription:|n {archetype['description']}")
                if archetype.get('suggested_focuses'):
                    self.caller.msg(f"|wSuggested Focuses:|n {', '.join(archetype['suggested_focuses'])}")
                if archetype.get('suggested_talents'):
                    self.caller.msg(f"|wSuggested Talents:|n {', '.join(archetype['suggested_talents'])}")
                self.caller.msg("|w" + "=" * 78 + "|n")
            
            # Show finishing touches (Step 8)
            bio_sections = []
            if target.db.reputation_trait:
                bio_sections.append(("Reputation Trait", target.db.reputation_trait))
            if target.db.ambition:
                bio_sections.append(("Ambition", target.db.ambition))
            if target.db.personality_traits:
                bio_sections.append(("Personality", target.db.personality_traits))
            if target.db.appearance:
                bio_sections.append(("Appearance", target.db.appearance))
            if target.db.relationships:
                bio_sections.append(("Relationships", target.db.relationships))
            
            if bio_sections:
                self.caller.msg(f"\n|y{'FINISHING TOUCHES':-^78}|n")
                for title, content in bio_sections:
                    self.caller.msg(f"|w{title}:|n {content}")
                self.caller.msg("|w" + "=" * 78 + "|n")
            
            # Show background
            if target.db.background:
                self.caller.msg(f"\n|y{'BACKGROUND':-^78}|n")
                self.caller.msg(target.db.background)
                self.caller.msg("|w" + "=" * 78 + "|n")


class CmdStats(MuxCommand):
    """
    Set character statistics, focuses, talents, assets, and drives.

    Usage:
        +stats <stat>=<value> | +stats <character>/<stat>=<value> (staff)
        +stats/focus | +stats/focus add=<focus> | +stats/focus rem=<focus> | +stats/focus list [<skill>]
        +stats/talent add=<talent> | +stats/talent rem=<talent>
        +stats/asset add=<asset> | +stats/asset rem=<asset>
        +stats/drive | +stats/drive <drive>=<rating> | +stats/drive <drive>/statement=<text>
        +stats/set <name>/<stat>=<value> | +stats/set <name>/focus/add=<focus> | +stats/set <name>/talent/add=<talent> | +stats/set <name>/asset/add=<asset> | +stats/set <name>/drive/<drive>=<rating> | +stats/set <name>/drive/<drive>/statement=<text> (staff)

    Switches: /focus (manage focuses), /talent (manage talents), /asset (manage assets), /drive (manage drives), /set (set stats for others, staff only)
    Skills: battle, communicate, discipline, move, understand (range 0-5)
    Drives: duty, faith, justice, power, truth (ratings: 4, 5, 6, 7, 8 - one of each)
    Drive statements: Required for drives with rating 6 or higher

    Examples:
        +stats battle=3 | +stats paul/battle=3 (staff) | +stats communicate=2
        +stats/focus | +stats/focus list | +stats/focus list battle | +stats/focus add=Short Blades | +stats/focus add=music/baliset
        +stats/talent add=Mentat Training | +stats/asset add=Personal Shield
        +stats/drive | +stats/drive duty=8 | +stats/drive duty/statement=I serve at the pleasure of the House
        +stats/set Paul/focus/add=Charm | +stats/set Paul/drive/duty=8 | +stats/set Paul/drive/duty/statement=My duty statement
    """
    
    key = "+stats"
    aliases = ["stats"]
    help_category = "Character"
    
    def func(self):
        """Set character stats, focuses, talents, assets, and drives"""
        
        if not self.args:
            self.caller.msg("Usage: +stats <stat>=<value> or see 'help +stats' for more options.")
            return
        
        # Check if target has stats
        if not hasattr(self.caller.db, 'stats'):
            self.caller.msg("Your character does not have stats initialized.")
            return
        
        # Handle /set switch (staff only)
        if "set" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("|rYou don't have permission to set other characters' stats.|n")
                return
            self._handle_staff_set()
            return
        
        # Handle /focus switch
        if "focus" in self.switches:
            self._handle_focus()
            return
        
        # Handle /talent switch
        if "talent" in self.switches:
            self._handle_talent()
            return
        
        # Handle /asset switch
        if "asset" in self.switches:
            self._handle_asset()
            return
        
        # Handle /drive switch
        if "drive" in self.switches:
            self._handle_drive()
            return
        
        # Default: Setting a stat
        if "=" not in self.args:
            self.caller.msg("Usage: +stats <stat>=<value>")
            return
        
        self._handle_stat_set()
    
    def _handle_stat_set(self):
        """Handle setting a stat (attribute or skill)"""
        # Check if setting for another character (staff only)
        if "/" in self.args.split("=")[0]:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("|rYou don't have permission to set other characters' stats.|n")
                return
            
            # Parse character/stat=value
            parts = self.args.split("=")
            if len(parts) != 2:
                self.caller.msg("Usage: +stats <character>/<stat>=<value>")
                return
            
            char_and_stat = parts[0].strip()
            value_str = parts[1].strip()
            
            char_parts = char_and_stat.split("/")
            if len(char_parts) != 2:
                self.caller.msg("Usage: +stats <character>/<stat>=<value>")
                return
            
            char_name = char_parts[0].strip()
            stat_name = char_parts[1].strip().lower()
            
            target = self.caller.search(char_name)
            if not target:
                return
            
            if not hasattr(target.db, 'stats'):
                self.caller.msg(f"{target.name} does not have stats initialized.")
                return
        else:
            # Setting own stat
            target = self.caller
            parts = self.args.split("=")
            if len(parts) != 2:
                self.caller.msg("Usage: +stats <stat>=<value>")
                return
            
            stat_name = parts[0].strip().lower()
            value_str = parts[1].strip()
        
        # Convert value to int
        try:
            value = int(value_str)
        except ValueError:
            self.caller.msg("Value must be a number.")
            return
        
        # Set skill (Dune doesn't use attributes)
        skills = target.db.stats.get("skills", {})
        
        if stat_name in skills:
            target.set_skill(stat_name, value)
            self.caller.msg(f"Set {target.name}'s {stat_name} skill to {value}.")
        else:
            self.caller.msg(f"Unknown skill: {stat_name}")
            self.caller.msg("Valid skills: battle, communicate, discipline, move, understand")
    
    def _handle_focus(self):
        """Handle listing, adding, and removing focuses"""
        target = self.caller
        
        # No arguments - list current focuses
        if not self.args:
            focuses = target.db.stats.get("focuses", [])
            if not focuses:
                self.caller.msg("|wYou have no focuses.|n")
                self.caller.msg("Use |w+stats/focus list|n to see available focuses.")
                return
            
            self.caller.msg("|w" + "=" * 78 + "|n")
            self.caller.msg("|w" + " YOUR FOCUSES".center(78) + "|n")
            self.caller.msg("|w" + "=" * 78 + "|n")
            for focus in sorted(focuses):
                self.caller.msg(f"  • {focus}")
            self.caller.msg("|w" + "=" * 78 + "|n")
            return
        
        # List available focuses
        if self.args.strip().lower().startswith("list"):
            args_parts = self.args.strip().split(None, 1)
            
            if len(args_parts) == 1:
                # List all focuses
                self.caller.msg("|w" + "=" * 78 + "|n")
                self.caller.msg("|w" + " AVAILABLE FOCUSES".center(78) + "|n")
                self.caller.msg("|w" + "=" * 78 + "|n")
                
                for skill in sorted(DUNE_FOCUSES.keys()):
                    self.caller.msg(f"\n|y{skill.upper()}:|n")
                    for focus in DUNE_FOCUSES[skill]:
                        # Mark focuses that require specification
                        if focus in ["Music", "Secret Language", "Survival", "Pilot", "Faction Lore"]:
                            self.caller.msg(f"  • {focus} |c(use: {focus.lower()}/type)|n")
                        else:
                            self.caller.msg(f"  • {focus}")
                
                self.caller.msg("\n|w" + "=" * 78 + "|n")
                self.caller.msg("|cNote:|n Focuses marked with |c(specify type)|n require you to specify")
                self.caller.msg("a particular type using the / separator.")
                self.caller.msg("Examples: |wmusic/baliset|n, |wsurvival/desert|n, |wpilot/ornithopter|n")
                self.caller.msg("You can add the same base focus multiple times with different specializations.")
                self.caller.msg("|w" + "=" * 78 + "|n")
            else:
                # List focuses for a specific skill
                skill = args_parts[1].strip().lower()
                
                if skill not in DUNE_FOCUSES:
                    self.caller.msg(f"|rUnknown skill: {skill}|n")
                    self.caller.msg("Valid skills: battle, communicate, discipline, move, understand")
                    return
                
                self.caller.msg("|w" + "=" * 78 + "|n")
                self.caller.msg("|w" + f" {skill.upper()} FOCUSES".center(78) + "|n")
                self.caller.msg("|w" + "=" * 78 + "|n")
                
                for focus in DUNE_FOCUSES[skill]:
                    if focus in ["Music", "Secret Language", "Survival", "Pilot", "Faction Lore"]:
                        self.caller.msg(f"  • {focus} |c(use: {focus.lower()}/type)|n")
                    else:
                        self.caller.msg(f"  • {focus}")
                
                self.caller.msg("|w" + "=" * 78 + "|n")
                if any(f in ["Music", "Secret Language", "Survival", "Pilot", "Faction Lore"] 
                       for f in DUNE_FOCUSES[skill]):
                    self.caller.msg("|cNote:|n For specialized focuses, use |w+stats/focus add=music/baliset|n")
                    self.caller.msg("|w" + "=" * 78 + "|n")
            return
        
        # Add or remove focus
        if "=" not in self.args:
            self.caller.msg("Usage: +stats/focus add=<focus> or +stats/focus rem=<focus>")
            self.caller.msg("       +stats/focus list [skill]")
            return
        
        parts = self.args.split("=", 1)
        action = parts[0].strip().lower()
        focus_name = parts[1].strip()
        
        if action == "add":
            # Validate the focus
            if not self._validate_focus(focus_name):
                self.caller.msg(f"|rInvalid focus: {focus_name}|n")
                self.caller.msg("Use |w+stats/focus list|n to see valid focuses.")
                self.caller.msg("Remember: Some focuses require specification using /")
                self.caller.msg("Example: |wmusic/baliset|n or |wsurvival/desert|n")
                return
            
            # Check for duplicates (case-insensitive)
            current_focuses = target.db.stats.get("focuses", [])
            focus_lower = focus_name.lower()
            
            # Check if this exact focus already exists
            for existing_focus in current_focuses:
                if existing_focus.lower() == focus_lower:
                    self.caller.msg(f"|rYou already have the focus: {existing_focus}|n")
                    return
            
            target.add_focus(focus_name)
            self.caller.msg(f"|gAdded focus:|n {focus_name}")
            
            # Check if faction requirements are now met
            faction = target.db.faction
            if faction:
                from typeclasses.factions import validate_faction_focuses
                focus_valid, focus_msg, _ = validate_faction_focuses(target, faction)
                if focus_valid:
                    self.caller.msg(f"|g✓ Faction requirements now met: {focus_msg}|n")
                else:
                    self.caller.msg(f"|yNote:|n {focus_msg}|n")
        elif action == "rem" or action == "remove":
            if target.remove_focus(focus_name):
                self.caller.msg(f"|gRemoved focus:|n {focus_name}")
                
                # Check if faction requirements are still met
                faction = target.db.faction
                if faction:
                    from typeclasses.factions import validate_faction_focuses
                    focus_valid, focus_msg, _ = validate_faction_focuses(target, faction)
                    if not focus_valid:
                        self.caller.msg(f"|yWarning:|n {focus_msg}|n")
            else:
                self.caller.msg(f"|rYou don't have that focus.|n")
        else:
            self.caller.msg("Usage: +stats/focus add=<focus> or +stats/focus rem=<focus>")
    
    def _validate_focus(self, focus_name):
        """
        Validate a focus against the approved list.
        Supports exact matches and focuses that require specification.
        
        Args:
            focus_name (str): The focus to validate (e.g., "Short Blades" or "music/baliset")
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Normalize the focus name for comparison
        focus_lower = focus_name.lower()
        
        # Check if this is a specialized focus (contains a /)
        if "/" in focus_lower:
            # Split on the first slash
            base_focus, specialization = focus_lower.split("/", 1)
            base_focus = base_focus.strip()
            specialization = specialization.strip()
            
            # Must have both parts
            if not base_focus or not specialization:
                return False
            
            # Check if the base focus is one that requires specification
            for skill, focuses in DUNE_FOCUSES.items():
                for valid_focus in focuses:
                    valid_lower = valid_focus.lower()
                    if base_focus == valid_lower and valid_focus in ["Music", "Secret Language", "Survival", "Pilot", "Faction Lore"]:
                        return True
            
            return False
        
        # Check all skills for an exact match
        for skill, focuses in DUNE_FOCUSES.items():
            for valid_focus in focuses:
                valid_lower = valid_focus.lower()
                
                # Exact match (case-insensitive) for non-specialized focuses
                if focus_lower == valid_lower:
                    # If this focus requires specification, it should use the / format
                    if valid_focus in ["Music", "Secret Language", "Survival", "Pilot", "Faction Lore"]:
                        return False  # Should be using format like "music/baliset"
                    return True
        
        return False
    
    def _handle_talent(self):
        """Handle adding/removing talents (traits)"""
        target = self.caller
        
        if "=" not in self.args:
            self.caller.msg("Usage: +stats/talent add=<talent> or +stats/talent rem=<talent>")
            return
        
        parts = self.args.split("=", 1)
        action = parts[0].strip().lower()
        talent_name = parts[1].strip()
        
        if action == "add":
            # Validate faction restrictions
            from typeclasses.talents import can_character_take_talent
            can_take, reason = can_character_take_talent(target, talent_name)
            if not can_take:
                self.caller.msg(f"|rCannot add talent: {reason}|n")
                return
            
            target.add_trait(talent_name)
            self.caller.msg(f"Added talent: {talent_name}")
            
            # Check if faction requirements are now met
            faction = target.db.faction
            if faction:
                from typeclasses.factions import validate_faction_talents
                talent_valid, talent_msg, _ = validate_faction_talents(target, faction)
                if talent_valid:
                    self.caller.msg(f"|g✓ Faction requirements now met: {talent_msg}|n")
                else:
                    self.caller.msg(f"|yNote:|n {talent_msg}|n")
        elif action == "rem" or action == "remove":
            if target.remove_trait(talent_name):
                self.caller.msg(f"Removed talent: {talent_name}")
                
                # Check if faction requirements are still met
                faction = target.db.faction
                if faction:
                    from typeclasses.factions import validate_faction_talents
                    talent_valid, talent_msg, _ = validate_faction_talents(target, faction)
                    if not talent_valid:
                        self.caller.msg(f"|yWarning:|n {talent_msg}|n")
            else:
                self.caller.msg(f"You don't have that talent.")
        else:
            self.caller.msg("Usage: +stats/talent add=<talent> or +stats/talent rem=<talent>")
    
    def _handle_asset(self):
        """Handle adding/removing assets"""
        target = self.caller
        
        if "=" not in self.args:
            self.caller.msg("Usage: +stats/asset add=<asset> or +stats/asset rem=<asset>")
            return
        
        parts = self.args.split("=", 1)
        action = parts[0].strip().lower()
        asset_name = parts[1].strip()
        
        if action == "add":
            target.add_asset(asset_name)
            self.caller.msg(f"Added asset: {asset_name}")
        elif action == "rem" or action == "remove":
            if target.remove_asset(asset_name):
                self.caller.msg(f"Removed asset: {asset_name}")
            else:
                self.caller.msg(f"You don't have that asset.")
        else:
            self.caller.msg("Usage: +stats/asset add=<asset> or +stats/asset rem=<asset>")
    
    def _handle_drive(self):
        """Handle setting drive ratings and statements"""
        target = self.caller
        
        if not self.args:
            # Show current drives
            drives = target.db.stats.get("drives", {})
            self.caller.msg("|wCurrent Drives:|n")
            for drive_name in ["duty", "faith", "justice", "power", "truth"]:
                drive = drives.get(drive_name, {})
                
                # Handle legacy format
                if isinstance(drive, str):
                    if drive:
                        self.caller.msg(f"  |y{drive_name.capitalize()}:|n {drive}")
                    else:
                        self.caller.msg(f"  |y{drive_name.capitalize()}:|n (not set)")
                    continue
                
                rating = drive.get("rating", 0) if isinstance(drive, dict) else 0
                statement = drive.get("statement", "") if isinstance(drive, dict) else ""
                
                if rating > 0:
                    display = f"  |y{drive_name.capitalize()}|n [{rating}]"
                    if statement:
                        display += f": {statement}"
                    self.caller.msg(display)
                else:
                    self.caller.msg(f"  |y{drive_name.capitalize()}:|n (not set)")
            self.caller.msg("\n|wUsage:|n")
            self.caller.msg("  +stats/drive <drive>=<rating> - Set drive rating (4, 5, 6, 7, or 8)")
            self.caller.msg("  +stats/drive <drive>/statement=<text> - Set drive statement (rating 6+ only)")
            self.caller.msg("  Valid drives: duty, faith, justice, power, truth")
            self.caller.msg("  Each rating (4, 5, 6, 7, 8) must be assigned to exactly one drive")
            return
        
        if "=" not in self.args:
            self.caller.msg("Usage: +stats/drive <drive name>=<rating> or +stats/drive <drive>/statement=<text>")
            self.caller.msg("Valid drives: duty, faith, justice, power, truth")
            return
        
        parts = self.args.split("=", 1)
        drive_part = parts[0].strip().lower()
        value = parts[1].strip()
        
        # Check if setting statement
        if "/statement" in drive_part:
            drive_name = drive_part.replace("/statement", "").strip()
            valid_drives = ["duty", "faith", "justice", "power", "truth"]
            if drive_name not in valid_drives:
                self.caller.msg(f"Unknown drive: {drive_name}")
                self.caller.msg(f"Valid drives: {', '.join(valid_drives)}")
                return
            
            success, message = target.set_drive_statement(drive_name, value)
            if success:
                self.caller.msg(f"|g{message}|n")
            else:
                self.caller.msg(f"|r{message}|n")
            return
        
        # Setting rating
        drive_name = drive_part
        valid_drives = ["duty", "faith", "justice", "power", "truth"]
        if drive_name not in valid_drives:
            self.caller.msg(f"Unknown drive: {drive_name}")
            self.caller.msg(f"Valid drives: {', '.join(valid_drives)}")
            return
        
        try:
            rating = int(value)
        except ValueError:
            self.caller.msg("Rating must be a number (4, 5, 6, 7, or 8)")
            return
        
        success, message = target.set_drive_rating(drive_name, rating)
        if success:
            self.caller.msg(f"|g{message}|n")
            # Remind about statements for rating 6+
            if rating >= 6:
                self.caller.msg(f"|yNote:|n You can set a statement for {drive_name} with: +stats/drive {drive_name}/statement=<text>")
        else:
            self.caller.msg(f"|r{message}|n")
    
    def _handle_staff_set(self):
        """Handle staff setting stats for other characters"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou don't have permission to set other characters' stats.|n")
            return
        
        if "=" not in self.args:
            self.caller.msg("Usage: +stats/set <name>/<stat>=<value>")
            return
        
        # Parse the arguments
        parts = self.args.split("=", 1)
        path = parts[0].strip()
        value = parts[1].strip()
        
        path_parts = path.split("/")
        if len(path_parts) < 2:
            self.caller.msg("Usage: +stats/set <name>/<stat>=<value>")
            return
        
        char_name = path_parts[0].strip()
        
        # Find the target character
        target = self.caller.search(char_name)
        if not target:
            return
        
        if not hasattr(target.db, 'stats'):
            self.caller.msg(f"{target.name} does not have stats initialized.")
            return
        
        # Handle different paths
        if len(path_parts) == 2:
            # Simple stat set: +stats/set Paul/fitness=10
            stat_name = path_parts[1].strip().lower()
            
            try:
                int_value = int(value)
            except ValueError:
                self.caller.msg("Value must be a number.")
                return
            
            skills = target.db.stats.get("skills", {})
            
            if stat_name in skills:
                target.set_skill(stat_name, int_value)
                self.caller.msg(f"Set {target.name}'s {stat_name} skill to {int_value}.")
            else:
                self.caller.msg(f"Unknown skill: {stat_name}")
                self.caller.msg("Valid skills: battle, communicate, discipline, move, understand")
        
        elif len(path_parts) == 3:
            # Focus/talent/asset/drive: +stats/set Paul/focus/add=Charm
            category = path_parts[1].strip().lower()
            action = path_parts[2].strip().lower()
            
            if category == "focus":
                if action == "add":
                    # Validate the focus
                    if not self._validate_focus(value):
                        self.caller.msg(f"|rInvalid focus: {value}|n")
                        self.caller.msg("Use |w+stats/focus list|n to see valid focuses.")
                        self.caller.msg("Remember: Some focuses require specification using /")
                        self.caller.msg("Example: |wmusic/baliset|n or |wsurvival/desert|n")
                        return
                    
                    # Check for duplicates (case-insensitive)
                    current_focuses = target.db.stats.get("focuses", [])
                    focus_lower = value.lower()
                    
                    for existing_focus in current_focuses:
                        if existing_focus.lower() == focus_lower:
                            self.caller.msg(f"|r{target.name} already has the focus: {existing_focus}|n")
                            return
                    
                    target.add_focus(value)
                    self.caller.msg(f"|gAdded focus '{value}' to {target.name}.|n")
                elif action == "rem" or action == "remove":
                    if target.remove_focus(value):
                        self.caller.msg(f"|gRemoved focus '{value}' from {target.name}.|n")
                    else:
                        self.caller.msg(f"|r{target.name} doesn't have that focus.|n")
                else:
                    self.caller.msg("Use 'add' or 'rem' for focuses.")
            
            elif category == "talent":
                if action == "add":
                    target.add_trait(value)
                    self.caller.msg(f"Added talent '{value}' to {target.name}.")
                elif action == "rem" or action == "remove":
                    if target.remove_trait(value):
                        self.caller.msg(f"Removed talent '{value}' from {target.name}.")
                    else:
                        self.caller.msg(f"{target.name} doesn't have that talent.")
                else:
                    self.caller.msg("Use 'add' or 'rem' for talents.")
            
            elif category == "asset":
                if action == "add":
                    target.add_asset(value)
                    self.caller.msg(f"Added asset '{value}' to {target.name}.")
                elif action == "rem" or action == "remove":
                    if target.remove_asset(value):
                        self.caller.msg(f"Removed asset '{value}' from {target.name}.")
                    else:
                        self.caller.msg(f"{target.name} doesn't have that asset.")
                else:
                    self.caller.msg("Use 'add' or 'rem' for assets.")
            
            elif category == "drive":
                # +stats/set Paul/drive/duty=<rating> or +stats/set Paul/drive/duty/statement=<text>
                drive_name = action
                valid_drives = ["duty", "faith", "justice", "power", "truth"]
                
                # Check if setting statement
                if "/statement" in drive_name:
                    drive_name = drive_name.replace("/statement", "").strip()
                    if drive_name not in valid_drives:
                        self.caller.msg(f"Unknown drive: {drive_name}")
                        self.caller.msg(f"Valid drives: {', '.join(valid_drives)}")
                        return
                    
                    success, message = target.set_drive_statement(drive_name, value)
                    if success:
                        self.caller.msg(f"|gSet {target.name}'s {drive_name} drive statement: {value}|n")
                    else:
                        self.caller.msg(f"|r{message}|n")
                    return
                
                # Setting rating
                if drive_name not in valid_drives:
                    self.caller.msg(f"Unknown drive: {drive_name}")
                    self.caller.msg(f"Valid drives: {', '.join(valid_drives)}")
                    return
                
                try:
                    rating = int(value)
                except ValueError:
                    self.caller.msg("Rating must be a number (4, 5, 6, 7, or 8)")
                    return
                
                success, message = target.set_drive_rating(drive_name, rating)
                if success:
                    self.caller.msg(f"|gSet {target.name}'s {drive_name} drive rating to {rating}|n")
                else:
                    self.caller.msg(f"|r{message}|n")
            
            else:
                self.caller.msg(f"Unknown category: {category}")
                self.caller.msg("Valid categories: focus, talent, asset, drive")
        
        else:
            self.caller.msg("Invalid command format. See 'help +stats' for usage.")
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

