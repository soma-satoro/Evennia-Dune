"""
Character Generation Command

Command to create characters following the Modiphius Dune character creation system.
"""

from evennia.commands.default.muxcommand import MuxCommand
from typeclasses.archetypes import ARCHETYPES, get_archetype, get_all_archetype_names, list_archetypes_by_category, get_archetypes_by_faction, can_character_take_archetype
from typeclasses.factions import CASTES, FACTIONS, get_faction, get_all_faction_names, validate_faction_talents, validate_faction_focuses
from typeclasses.talents import TALENTS, get_talent, get_talents_by_category, get_talents_by_faction, can_character_take_talent, get_all_talent_names
from typeclasses.titles import TITLES, get_title, get_title_by_name, get_all_titles, get_titles_by_category, get_title_display_name, get_architect_access_for_title
from commands.dune.CmdSheet import DUNE_FOCUSES


class CmdChargen(MuxCommand):
    """
    Character generation command for Dune.
    
    Usage:
        +chargen/list - List all available archetypes
        +chargen/info <archetype> - Show information about an archetype
        +chargen/archetype <archetype> - Choose your archetype (Step 2)
        +chargen/caste <caste> - Set your caste (Na-Familia, Bondsman, Pyon)
        +chargen/title <title> - Set your noble title (optional)
        +chargen/title/list - List all available titles
        +chargen/title/info <title> - Show title information
        +chargen/faction <faction> - Set your faction (validates requirements)
        +chargen/faction/list - List all available factions
        +chargen/faction/info <faction> - Show faction requirements
        +chargen/skills - Set up skills based on archetype (Step 3)
        +chargen/focuses - Add focuses (Step 4)
        +chargen/talents - Add talents (Step 5)
        +chargen/drives - Set drives and drive statements (Step 6)
        +chargen/assets - Create starting assets (Step 7)
        +chargen/status - Show character generation progress
    
    Steps:
        2. Choose an archetype
        2a. Set caste (Na-Familia, Bondsman, Pyon)
        2b. Set title (optional, for noble characters)
        2c. Set faction (optional, validates mandatory talents/focuses)
        3. Set skills (primary 6, secondary 5, others 4, then add 5 points max 8)
        4. Choose 4 focuses (at least one for primary skill)
        5. Choose 3 talents (faction characters must pick mandatory talents)
        6. Set drives (8, 7, 6, 5, 4) and statements for top 3
        7. Create 3 assets (one must be tangible)
        8. Finishing touches (+bio command)
    """
    
    key = "+chargen"
    aliases = ["chargen"]
    help_category = "Character"
    
    def func(self):
        """Handle character generation commands"""
        
        if "list" in self.switches:
            self._list_archetypes()
            return
        
        if "info" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +chargen/info <archetype>")
                return
            self._show_archetype_info(self.args.strip())
            return
        
        if "archetype" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +chargen/archetype <archetype>")
                self.caller.msg("Use |w+chargen/list|n to see available archetypes.")
                return
            self._set_archetype(self.args.strip())
            return
        
        if "caste" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +chargen/caste <caste>")
                self.caller.msg("Valid castes: Na-Familia, Bondsman, Pyon")
                return
            self._set_caste(self.args.strip())
            return
        
        if "title" in self.switches:
            if not self.args:
                if "list" in self.switches:
                    self._list_titles()
                    return
                self.caller.msg("Usage: +chargen/title <title> | +chargen/title/list | +chargen/title/info <title>")
                return
            if "info" in self.switches:
                self._show_title_info(self.args.strip())
                return
            if "list" in self.switches:
                self._list_titles()
                return
            self._set_title(self.args.strip())
            return
        
        if "faction" in self.switches:
            if not self.args:
                if "list" in self.switches:
                    self._list_factions()
                    return
                self.caller.msg("Usage: +chargen/faction <faction> | +chargen/faction/list | +chargen/faction/info <faction>")
                return
            if "info" in self.switches:
                self._show_faction_info(self.args.strip())
                return
            self._set_faction(self.args.strip())
            return
        
        if "skills" in self.switches:
            self._setup_skills()
            return
        
        if "focuses" in self.switches:
            self._setup_focuses()
            return
        
        if "talents" in self.switches:
            self._setup_talents()
            return
        
        if "drives" in self.switches:
            self._setup_drives()
            return
        
        if "assets" in self.switches:
            self._setup_assets()
            return
        
        if "status" in self.switches:
            self._show_status()
            return
        
        # Default: show status
        self._show_status()
    
    def _list_archetypes(self):
        """List all available archetypes organized by category."""
        categories = list_archetypes_by_category()
        faction = self.caller.db.faction
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg("|w" + " AVAILABLE ARCHETYPES".center(80) + "|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        for category, archetype_list in categories.items():
            if not archetype_list:
                continue
            
            self.caller.msg(f"\n|y{category.upper()} ARCHETYPES:|n")
            for name, archetype in sorted(archetype_list):
                trait = archetype.get("trait", name)
                primary = archetype.get("primary_skill", "Unknown")
                secondary = archetype.get("secondary_skill", "Unknown")
                required_faction = archetype.get("requires_faction", "")
                
                display = f"  |w{name:<15}|n |c{primary}/{secondary}|n - {trait}"
                if required_faction:
                    if faction and faction.lower() == required_faction.lower():
                        display += f" |g[{required_faction}]|n"
                    else:
                        display += f" |m[{required_faction} only]|n"
                self.caller.msg(display)
        
        # Show faction-specific archetypes if character has a faction
        if faction:
            faction_archetypes = get_archetypes_by_faction(faction)
            if faction_archetypes:
                self.caller.msg(f"\n|y{faction.upper()} ARCHETYPES:|n")
                for name, archetype in faction_archetypes:
                    trait = archetype.get("trait", name)
                    primary = archetype.get("primary_skill", "Unknown")
                    secondary = archetype.get("secondary_skill", "Unknown")
                    self.caller.msg(f"  |w{name:<15}|n |c{primary}/{secondary}|n - {trait} |g[{faction}]|n")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg("|cUse |w+chargen/info <archetype>|c to see detailed information.|n")
        self.caller.msg("|cUse |w+chargen/archetype <archetype>|c to select an archetype.|n")
        if not faction:
            self.caller.msg("|yNote:|n Some archetypes require a specific faction. Set your faction first with |w+chargen/faction <faction>|y|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _show_archetype_info(self, archetype_name):
        """Show detailed information about an archetype."""
        archetype = get_archetype(archetype_name)
        
        if not archetype:
            self.caller.msg(f"|rUnknown archetype: {archetype_name}|n")
            self.caller.msg("Use |w+chargen/list|n to see available archetypes.")
            return
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg(f"|w{archetype['trait']}|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg(f"|yCategory:|n {archetype['category']}")
        
        required_faction = archetype.get("requires_faction", "")
        if required_faction:
            self.caller.msg(f"|yRequires Faction:|n {required_faction}")
            # Check if character can take this archetype
            can_take, reason = can_character_take_archetype(self.caller, archetype_name)
            if can_take:
                self.caller.msg(f"|g✓ {reason}|n")
            else:
                self.caller.msg(f"|r✗ {reason}|n")
        
        self.caller.msg(f"|yPrimary Skill:|n {archetype['primary_skill']}")
        self.caller.msg(f"|ySecondary Skill:|n {archetype['secondary_skill']}")
        
        if archetype.get("suggested_focuses"):
            focuses = ", ".join(archetype['suggested_focuses'])
            self.caller.msg(f"|ySuggested Focuses:|n {focuses}")
        
        if archetype.get("suggested_talents"):
            talents = ", ".join(archetype['suggested_talents'])
            self.caller.msg(f"|ySuggested Talents:|n {talents}")
        
        if archetype.get("suggested_drives"):
            drives = ", ".join(archetype['suggested_drives'])
            self.caller.msg(f"|ySuggested Drives:|n {drives}")
        
        self.caller.msg(f"\n|yDescription:|n {archetype['description']}")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg(f"|cUse |w+chargen/archetype {archetype['trait']}|c to select this archetype.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _set_caste(self, caste_name):
        """Set the character's caste."""
        caste_lower = caste_name.lower()
        valid_caste = None
        
        for caste in CASTES:
            if caste.lower() == caste_lower:
                valid_caste = caste
                break
        
        if not valid_caste:
            self.caller.msg(f"|rInvalid caste: {caste_name}|n")
            self.caller.msg(f"|yValid castes:|n {', '.join(CASTES)}")
            return
        
        self.caller.db.caste = valid_caste
        self.caller.msg(f"|gCaste set to:|n {valid_caste}")
        
        # Show descriptions
        if valid_caste == "Na-Familia":
            self.caller.msg("|cNobility - Members of the ruling class.|n")
        elif valid_caste == "Bondsman":
            self.caller.msg("|cFree individuals who are allowed to own small amounts of land and property, the middle class.|n")
        elif valid_caste == "Pyon":
            self.caller.msg("|cLowest classes, often employed as hard laborers.|n")
    
    def _list_titles(self):
        """List all available titles organized by category."""
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg("|w" + " AVAILABLE TITLES".center(80) + "|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        # Get character's gender if set (default to masculine)
        gender = getattr(self.caller.db, 'gender', 'masculine')
        if gender not in ['masculine', 'feminine']:
            gender = 'masculine'
        
        categories = ["Singular", "Major", "Noble", "Minor", "Lesser"]
        for category in categories:
            title_keys = get_titles_by_category(category)
            if not title_keys:
                continue
            
            self.caller.msg(f"\n|y{category.upper()} TITLES:|n")
            for title_key in sorted(title_keys):
                title = TITLES[title_key]
                display_name = get_title_display_name(title_key, gender)
                hereditary = "|g[Hereditary]|n" if title["hereditary"] else "|m[Non-Hereditary]|n"
                architect = title["architect_access"]
                if architect == "full":
                    architect_display = "|g[Full Architect]|n"
                elif architect == "limited":
                    architect_display = "|y[Limited Architect]|n"
                else:
                    architect_display = "|m[Roleplay Only]|n"
                
                self.caller.msg(f"  |w{display_name:<20}|n {hereditary} {architect_display}")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg("|cUse |w+chargen/title/info <title>|c to see detailed information.|n")
        self.caller.msg("|cUse |w+chargen/title <title>|c to set your title.|n")
        self.caller.msg("|yNote:|n Titles are generally for Na-Familia caste, but exceptions exist.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _show_title_info(self, title_name):
        """Show detailed information about a title."""
        # Try to find the title
        title_key, title = get_title_by_name(title_name)
        
        if not title:
            self.caller.msg(f"|rUnknown title: {title_name}|n")
            self.caller.msg("Use |w+chargen/title/list|n to see available titles.")
            return
        
        # Get character's gender if set
        gender = getattr(self.caller.db, 'gender', 'masculine')
        if gender not in ['masculine', 'feminine']:
            gender = 'masculine'
        
        display_name = get_title_display_name(title_key, gender)
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg(f"|w{display_name}|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        self.caller.msg(f"|yCategory:|n {title['category']}")
        self.caller.msg(f"|yHereditary:|n {'Yes' if title['hereditary'] else 'No'}")
        self.caller.msg(f"|yHierarchy Level:|n {title['hierarchy_level']}")
        
        architect = title['architect_access']
        if architect == "full":
            architect_display = "|gFull Architect Access|n - Can use all architect capabilities"
        elif architect == "limited":
            architect_display = "|yLimited Architect Access|n - Can use lower-level architect options"
        else:
            architect_display = "|mRoleplay Only|n - Primarily for background and roleplay"
        
        self.caller.msg(f"|yArchitect Access:|n {architect_display}")
        
        if title.get("description"):
            self.caller.msg(f"\n|yDescription:|n {title['description']}")
        
        # Show both forms
        if title['masculine'] != title['feminine']:
            self.caller.msg(f"\n|yForms:|n {title['masculine']} / {title['feminine']}")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg(f"|cUse |w+chargen/title {display_name}|c to select this title.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _set_title(self, title_name):
        """Set the character's title."""
        # Try to find the title
        title_key, title = get_title_by_name(title_name)
        
        if not title:
            self.caller.msg(f"|rUnknown title: {title_name}|n")
            self.caller.msg("Use |w+chargen/title/list|n to see available titles.")
            return
        
        # Get character's gender if set
        gender = getattr(self.caller.db, 'gender', 'masculine')
        if gender not in ['masculine', 'feminine']:
            gender = 'masculine'
        
        display_name = get_title_display_name(title_key, gender)
        
        # Store both the key and display name
        self.caller.db.title = title_key
        self.caller.db.title_display = display_name
        
        self.caller.msg(f"|gTitle set to:|n {display_name}")
        
        # Show information about the title
        architect = title['architect_access']
        if architect == "full":
            self.caller.msg("|gFull Architect Access|n - You can use all architect capabilities.")
        elif architect == "limited":
            self.caller.msg("|yLimited Architect Access|n - You can use lower-level architect options.")
        else:
            self.caller.msg("|cRoleplay Only|n - This title is primarily for background and roleplay.")
        
        if title['hereditary']:
            self.caller.msg("|cThis is a hereditary title.|n")
        else:
            self.caller.msg("|cThis is a non-hereditary title, typically awarded for service.|n")
        
        # Note about caste
        caste = self.caller.db.caste
        if caste != "Na-Familia":
            self.caller.msg("|yNote:|n Titles are generally for Na-Familia caste, but exceptions exist.|n")
    
    def _list_factions(self):
        """List all available factions."""
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg("|w" + " AVAILABLE FACTIONS".center(80) + "|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        for faction_name in sorted(FACTIONS.keys()):
            faction = FACTIONS[faction_name]
            mandatory = faction.get("mandatory_talents", [])
            mandatory_focuses = faction.get("mandatory_focuses", [])
            
            req_text = ""
            if mandatory:
                if len(mandatory) == 1:
                    req_text = f"Requires: {mandatory[0]}"
                else:
                    note = faction.get("note", "")
                    if "at least one" in note.lower() or "one of" in note.lower():
                        req_text = f"Requires one of: {', '.join(mandatory[:3])}..."
                    elif "both" in note.lower() or "all" in note.lower():
                        req_text = f"Requires all: {', '.join(mandatory)}"
                    else:
                        req_text = f"Requires: {', '.join(mandatory[:2])}..."
            
            if mandatory_focuses:
                if req_text:
                    req_text += f" + focus from: {', '.join(mandatory_focuses[:3])}..."
                else:
                    req_text = f"Requires focus from: {', '.join(mandatory_focuses[:3])}..."
            
            if not req_text:
                req_text = "No mandatory requirements"
            
            self.caller.msg(f"  |w{faction_name:<30}|n |c{req_text}|n")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg("|cUse |w+chargen/faction/info <faction>|c to see detailed requirements.|n")
        self.caller.msg("|cUse |w+chargen/faction <faction>|c to set your faction.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _show_faction_info(self, faction_name):
        """Show detailed information about a faction."""
        faction = get_faction(faction_name)
        
        if not faction:
            self.caller.msg(f"|rUnknown faction: {faction_name}|n")
            self.caller.msg("Use |w+chargen/faction/list|n to see available factions.")
            return
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg(f"|w{faction_name}|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        if faction.get("description"):
            self.caller.msg(f"\n|yDescription:|n {faction['description']}")
        
        mandatory_talents = faction.get("mandatory_talents", [])
        if mandatory_talents:
            self.caller.msg(f"\n|yMandatory Talents:|n")
            note = faction.get("note", "")
            if note:
                self.caller.msg(f"|c{note}|n")
            for talent in mandatory_talents:
                self.caller.msg(f"  • {talent}")
        else:
            self.caller.msg(f"\n|yMandatory Talents:|n None")
        
        mandatory_focuses = faction.get("mandatory_focuses", [])
        if mandatory_focuses:
            self.caller.msg(f"\n|yMandatory Focuses:|n (Must have at least one)")
            for focus in mandatory_focuses:
                self.caller.msg(f"  • {focus}")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg(f"|cUse |w+chargen/faction {faction_name}|c to select this faction.|n")
        self.caller.msg("|cNote: The system will validate you have the required talents/focuses.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _set_faction(self, faction_name):
        """Set the character's faction and validate requirements."""
        faction = get_faction(faction_name)
        
        if not faction:
            self.caller.msg(f"|rUnknown faction: {faction_name}|n")
            self.caller.msg("Use |w+chargen/faction/list|n to see available factions.")
            return
        
        # Validate talents
        talent_valid, talent_msg, missing_talents = validate_faction_talents(self.caller, faction_name)
        
        # Validate focuses
        focus_valid, focus_msg, missing_focuses = validate_faction_focuses(self.caller, faction_name)
        
        # Check if requirements are met
        if not talent_valid:
            self.caller.msg(f"|rCannot set faction: {talent_msg}|n")
            if missing_talents:
                self.caller.msg(f"|yMissing talents:|n {', '.join(missing_talents)}")
                self.caller.msg("|cUse |w+chargen/talents add <talent>|c or |w+stats/talent add=<talent>|c to add talents.|n")
            return
        
        if not focus_valid:
            self.caller.msg(f"|rCannot set faction: {focus_msg}|n")
            if missing_focuses:
                self.caller.msg(f"|yMissing focuses:|n {', '.join(missing_focuses)}")
                self.caller.msg("|cUse |w+chargen/focuses add <skill>:<focus>|c or |w+stats/focus add=<focus>|c to add focuses.|n")
            return
        
        # Set the faction
        self.caller.db.faction = faction_name
        self.caller.msg(f"|gFaction set to:|n {faction_name}")
        self.caller.msg(f"|g{talent_msg}|n")
        if focus_valid and missing_focuses == []:
            self.caller.msg(f"|g{focus_msg}|n")
    
    def _set_archetype(self, archetype_name):
        """Set the character's archetype and initialize skills."""
        archetype = get_archetype(archetype_name)
        
        if not archetype:
            self.caller.msg(f"|rUnknown archetype: {archetype_name}|n")
            self.caller.msg("Use |w+chargen/list|n to see available archetypes.")
            return
        
        # Check if character can take this archetype
        can_take, reason = can_character_take_archetype(self.caller, archetype_name)
        if not can_take:
            self.caller.msg(f"|rCannot select archetype: {reason}|n")
            required_faction = archetype.get("requires_faction", "")
            if required_faction:
                self.caller.msg(f"|cSet your faction first with: |w+chargen/faction {required_faction}|c|n")
            return
        
        # Store archetype information
        self.caller.db.chargen_archetype = archetype
        self.caller.db.role = archetype['trait']
        
        # Initialize skills based on archetype
        primary_skill = archetype['primary_skill'].lower()
        secondary_skill = archetype['secondary_skill'].lower()
        
        # Set base skill values: primary 6, secondary 5, others 4
        self.caller.set_skill(primary_skill, 6)
        self.caller.set_skill(secondary_skill, 5)
        
        for skill in ["battle", "communicate", "discipline", "move", "understand"]:
            if skill not in [primary_skill, secondary_skill]:
                self.caller.set_skill(skill, 4)
        
        # Initialize remaining skill points (5 to distribute)
        self.caller.db.chargen_skill_points = 5
        
        self.caller.msg(f"|gArchetype set to: {archetype['trait']}|n")
        self.caller.msg(f"|yPrimary Skill:|n {archetype['primary_skill']} at 6")
        self.caller.msg(f"|ySecondary Skill:|n {archetype['secondary_skill']} at 5")
        self.caller.msg(f"|yOther Skills:|n All at 4")
        self.caller.msg(f"|ySkill Points Remaining:|n 5 (max skill 8)")
        self.caller.msg("\n|cNext: Use |w+chargen/skills <skill>=<points>|c to add skill points (e.g., +chargen/skills battle=2)|n")
        self.caller.msg("|cOr use |w+chargen/status|c to see your progress.|n")
    
    def _setup_skills(self):
        """Handle skill point assignment."""
        if not self.caller.db.chargen_archetype:
            self.caller.msg("|rYou must select an archetype first. Use |w+chargen/archetype <name>|r|n")
            return
        
        # If no args, show current skills and remaining points
        if not self.args:
            archetype = self.caller.db.chargen_archetype
            skill_points = self.caller.db.chargen_skill_points or 5
            
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|wCURRENT SKILLS|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            
            skills = self.caller.db.stats.get("skills", {})
            for skill in ["battle", "communicate", "discipline", "move", "understand"]:
                value = skills.get(skill, 0)
                skill_name = skill.capitalize()
                
                # Mark primary/secondary
                if skill.lower() == archetype['primary_skill'].lower():
                    skill_name += " (Primary)"
                elif skill.lower() == archetype['secondary_skill'].lower():
                    skill_name += " (Secondary)"
                
                self.caller.msg(f"  {skill_name:<20} {value}")
            
            self.caller.msg(f"\n|ySkill Points Remaining:|n {skill_points}")
            self.caller.msg("\n|cUsage: |w+chargen/skills <skill>=<points>|c")
            self.caller.msg("|cExample: |w+chargen/skills battle=2|c")
            self.caller.msg("|cSkills: Battle, Communicate, Discipline, Move, Understand|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            return
        
        # Parse skill assignment
        if "=" not in self.args:
            self.caller.msg("|rUsage: +chargen/skills <skill>=<points>|n")
            self.caller.msg("|rExample: +chargen/skills battle=2|n")
            return
        
        parts = self.args.split("=", 1)
        skill_name = parts[0].strip().lower()
        try:
            points = int(parts[1].strip())
        except ValueError:
            self.caller.msg("|rPoints must be a number.|n")
            return
        
        valid_skills = ["battle", "communicate", "discipline", "move", "understand"]
        if skill_name not in valid_skills:
            self.caller.msg(f"|rInvalid skill. Must be one of: {', '.join([s.capitalize() for s in valid_skills])}|n")
            return
        
        skill_points = self.caller.db.chargen_skill_points or 5
        
        if points < 0:
            self.caller.msg("|rCannot assign negative points.|n")
            return
        
        if points > skill_points:
            self.caller.msg(f"|rYou only have {skill_points} skill points remaining.|n")
            return
        
        current_value = self.caller.get_skill(skill_name)
        new_value = current_value + points
        
        if new_value > 8:
            self.caller.msg(f"|rSkill cannot exceed 8. Current: {current_value}, adding {points} would make {new_value}.|n")
            return
        
        # Apply the change
        self.caller.set_skill(skill_name, new_value)
        self.caller.db.chargen_skill_points = skill_points - points
        
        self.caller.msg(f"|gSet {skill_name.capitalize()} to {new_value} (added {points} points).|n")
        remaining = self.caller.db.chargen_skill_points
        if remaining > 0:
            self.caller.msg(f"|ySkill points remaining:|n {remaining}")
        else:
            self.caller.msg("|yAll skill points assigned!|n")
            self.caller.msg("\n|cNext: Use |w+chargen/focuses|c to add focuses.|n")
    
    def _setup_focuses(self):
        """Handle focus assignment."""
        if not self.caller.db.chargen_archetype:
            self.caller.msg("|rYou must select an archetype first. Use |w+chargen/archetype <name>|r|n")
            return
        
        archetype = self.caller.db.chargen_archetype
        current_focuses = self.caller.db.stats.get("focuses", [])
        
        # Initialize if needed
        if "chargen_focuses" not in self.caller.db:
            self.caller.db.chargen_focuses = []
        
        # Show current status
        if not self.args:
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|wFOCUSES|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|yYou need 4 focuses total.|n")
            self.caller.msg(f"|yAt least one must be for your primary skill: {archetype['primary_skill']}|n")
            
            if archetype.get("suggested_focuses"):
                self.caller.msg(f"|ySuggested Focuses:|n {', '.join(archetype['suggested_focuses'])}")
            
            self.caller.msg(f"\n|yCurrent Focuses ({len(current_focuses)}/4):|n")
            if current_focuses:
                for focus in current_focuses:
                    self.caller.msg(f"  • {focus}")
            else:
                self.caller.msg("  None yet")
            
            self.caller.msg("\n|cUsage: |w+chargen/focuses add <skill>:<focus>|c")
            self.caller.msg("|cExample: |w+chargen/focuses add Battle:Short Blades|c")
            self.caller.msg("|cYou can also use: |w+chargen/focuses remove <focus>|c")
            self.caller.msg("|w" + "=" * 80 + "|n")
            return
        
        # Parse arguments
        parts = self.args.split(None, 1)
        if len(parts) < 2:
            self.caller.msg("|rUsage: +chargen/focuses add <skill>:<focus> OR +chargen/focuses remove <focus>|n")
            return
        
        action = parts[0].lower()
        
        if action == "add":
            if ":" not in parts[1]:
                self.caller.msg("|rUsage: +chargen/focuses add <skill>:<focus>|n")
                self.caller.msg("|rExample: +chargen/focuses add Battle:Short Blades|n")
                return
            
            focus_parts = parts[1].split(":", 1)
            skill_name = focus_parts[0].strip().lower()
            focus_name = focus_parts[1].strip()
            
            valid_skills = ["battle", "communicate", "discipline", "move", "understand"]
            if skill_name not in valid_skills:
                self.caller.msg(f"|rInvalid skill. Must be one of: {', '.join([s.capitalize() for s in valid_skills])}|n")
                return
            
            # Validate focus exists for this skill
            valid_focuses = DUNE_FOCUSES.get(skill_name, [])
            focus_found = False
            for valid_focus in valid_focuses:
                if focus_name.lower() == valid_focus.lower():
                    focus_name = valid_focus  # Use the canonical name
                    focus_found = True
                    break
            
            if not focus_found:
                self.caller.msg(f"|yWarning: '{focus_name}' is not in the standard focus list for {skill_name.capitalize()}.|n")
                self.caller.msg("|yYou can still add it, but make sure it makes sense.|n")
            
            # Check if already have 4 focuses
            if len(current_focuses) >= 4:
                self.caller.msg("|rYou already have 4 focuses. Remove one first if you want to change.|n")
                return
            
            # Format: "Skill: Focus" or just the focus name (to match existing +stats format)
            # Check if this is a specialized focus (has / in it)
            if "/" in focus_name:
                # Specialized focus like "music/baliset" - use as-is
                focus_entry = focus_name
            else:
                # Regular focus - use the format that matches +stats/focus
                focus_entry = focus_name
            
            # Check if already exists (case-insensitive)
            focus_lower = focus_entry.lower()
            for existing_focus in current_focuses:
                if existing_focus.lower() == focus_lower:
                    self.caller.msg(f"|rYou already have the focus '{existing_focus}'.|n")
                    return
            
            self.caller.add_focus(focus_entry)
            self.caller.msg(f"|gAdded focus: {focus_entry}|n")
            
            # Check if faction requirements are now met
            faction = self.caller.db.faction
            if faction:
                focus_valid, focus_msg, _ = validate_faction_focuses(self.caller, faction)
                if focus_valid:
                    self.caller.msg(f"|g✓ Faction requirements now met: {focus_msg}|n")
                else:
                    self.caller.msg(f"|yNote:|n {focus_msg}|n")
            
            remaining = 4 - len(self.caller.db.stats.get("focuses", []))
            if remaining > 0:
                self.caller.msg(f"|yFocuses remaining:|n {remaining}")
            else:
                self.caller.msg("|yAll focuses assigned!|n")
                self.caller.msg("\n|cNext: Use |w+chargen/talents|c to add talents.|n")
                
        elif action == "remove":
            focus_to_remove = parts[1].strip()
            
            # Try to find matching focus
            found = None
            for focus in current_focuses:
                if focus.lower() == focus_to_remove.lower() or focus.lower().endswith(focus_to_remove.lower()):
                    found = focus
                    break
            
            if not found:
                self.caller.msg(f"|rFocus '{focus_to_remove}' not found.|n")
                return
            
            self.caller.remove_focus(found)
            self.caller.msg(f"|gRemoved focus: {found}|n")
        else:
            self.caller.msg("|rAction must be 'add' or 'remove'.|n")
    
    def _setup_talents(self):
        """Handle talent assignment."""
        if not self.caller.db.chargen_archetype:
            self.caller.msg("|rYou must select an archetype first. Use |w+chargen/archetype <name>|r|n")
            return
        
        archetype = self.caller.db.chargen_archetype
        current_talents = self.caller.db.stats.get("talents", [])
        faction = self.caller.db.faction
        
        # Show current status
        if not self.args:
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|wTALENTS|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|yYou need 3 talents total.|n")
            
            if archetype.get("suggested_talents"):
                self.caller.msg(f"|ySuggested Talent:|n {', '.join(archetype['suggested_talents'])}")
            
            if faction:
                faction_talents = get_talents_by_faction(faction)
                if faction_talents:
                    self.caller.msg(f"\n|yFaction Talents ({faction}):|n {', '.join(faction_talents[:10])}")
                    if len(faction_talents) > 10:
                        self.caller.msg(f"  ... and {len(faction_talents) - 10} more")
            
            self.caller.msg(f"\n|yCurrent Talents ({len(current_talents)}/3):|n")
            if current_talents:
                for talent in current_talents:
                    talent_data = get_talent(talent)
                    if talent_data:
                        category = talent_data.get("category", "General")
                        param = talent_data.get("requires_parameter", "")
                        display = talent
                        if param:
                            display += f" |c({param})|n"
                        if category != "General":
                            display += f" |m[{category}]|n"
                        self.caller.msg(f"  • {display}")
                    else:
                        self.caller.msg(f"  • {talent}")
            else:
                self.caller.msg("  None yet")
            
            self.caller.msg("\n|cUsage: |w+chargen/talents add <talent name>|c")
            self.caller.msg("|cExample: |w+chargen/talents add The Slow Blade|c")
            self.caller.msg("|cFor talents requiring parameters: |w+chargen/talents add Bold (Battle)|c")
            self.caller.msg("|cYou can also use: |w+chargen/talents remove <talent>|c")
            self.caller.msg("|cUse: |w+chargen/talents/list|c to see available talents|n")
            self.caller.msg("|cUse: |w+chargen/talents/info <talent>|c to see talent details|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            return
        
        # Handle list command
        if self.args.strip().lower() == "list":
            self._list_talents()
            return
        
        # Handle info command
        if self.args.strip().lower().startswith("info "):
            talent_name = self.args.strip()[5:].strip()
            self._show_talent_info(talent_name)
            return
        
        # Parse arguments
        parts = self.args.split(None, 1)
        if len(parts) < 2:
            self.caller.msg("|rUsage: +chargen/talents add <talent> OR +chargen/talents remove <talent>|n")
            return
        
        action = parts[0].lower()
        talent_input = parts[1].strip()
        
        if action == "add":
            # Parse talent name and parameter if present
            talent_name = talent_input
            parameter = None
            
            # Check if parameter is in parentheses
            if "(" in talent_input and ")" in talent_input:
                import re
                match = re.match(r"(.+?)\s*\((.+?)\)", talent_input)
                if match:
                    talent_name = match.group(1).strip()
                    parameter = match.group(2).strip()
            
            # Validate talent exists
            talent_data = get_talent(talent_name)
            if not talent_data:
                self.caller.msg(f"|rUnknown talent: {talent_name}|n")
                self.caller.msg("|cUse |w+chargen/talents/list|c to see available talents.|n")
                return
            
            # Check if character can take this talent
            can_take, reason = can_character_take_talent(self.caller, talent_name)
            if not can_take:
                self.caller.msg(f"|rCannot take talent: {reason}|n")
                return
            
            # Check if parameter is required
            requires_param = talent_data.get("requires_parameter")
            if requires_param and not parameter:
                self.caller.msg(f"|rThis talent requires a {requires_param} parameter.|n")
                if requires_param == "skill":
                    self.caller.msg("|cUsage: |w+chargen/talents add {talent_name} (Battle)|c|n")
                    self.caller.msg("|cSkills: Battle, Communicate, Discipline, Move, Understand|n")
                elif requires_param == "drive":
                    self.caller.msg("|cUsage: |w+chargen/talents add {talent_name} (Duty)|c|n")
                    self.caller.msg("|cDrives: Duty, Faith, Justice, Power, Truth|n")
                return
            
            # Format talent name with parameter if provided
            if parameter:
                talent_entry = f"{talent_name} ({parameter})"
            else:
                talent_entry = talent_name
            
            # Check if already have 3 talents
            if len(current_talents) >= 3:
                self.caller.msg("|rYou already have 3 talents. Remove one first if you want to change.|n")
                return
            
            # Check for duplicates
            if talent_entry in current_talents:
                self.caller.msg(f"|rYou already have the talent '{talent_entry}'.|n")
                return
            
            # Check for duplicate base talent (can't have same talent twice with different parameters)
            for existing in current_talents:
                if existing.startswith(talent_name + " (") or existing == talent_name:
                    if not requires_param:
                        self.caller.msg(f"|rYou already have the talent '{talent_name}'.|n")
                        return
            
            self.caller.add_talent(talent_entry)
            self.caller.msg(f"|gAdded talent: {talent_entry}|n")
            
            # Check if faction requirements are now met
            if faction:
                talent_valid, talent_msg, _ = validate_faction_talents(self.caller, faction)
                if talent_valid:
                    self.caller.msg(f"|g✓ Faction requirements now met: {talent_msg}|n")
                else:
                    self.caller.msg(f"|yNote:|n {talent_msg}|n")
            
            remaining = 3 - len(self.caller.db.stats.get("talents", []))
            if remaining > 0:
                self.caller.msg(f"|yTalents remaining:|n {remaining}")
            else:
                self.caller.msg("|yAll talents assigned!|n")
                self.caller.msg("\n|cNext: Use |w+chargen/drives|c to set drives.|n")
                
        elif action == "remove":
            if talent_input not in current_talents:
                self.caller.msg(f"|rTalent '{talent_input}' not found.|n")
                return
            
            self.caller.remove_talent(talent_input)
            self.caller.msg(f"|gRemoved talent: {talent_input}|n")
            
            # Check if faction requirements are still met
            if faction:
                talent_valid, talent_msg, _ = validate_faction_talents(self.caller, faction)
                if not talent_valid:
                    self.caller.msg(f"|yWarning:|n {talent_msg}|n")
        else:
            self.caller.msg("|rAction must be 'add' or 'remove'.|n")
    
    def _list_talents(self):
        """List available talents, organized by category."""
        faction = self.caller.db.faction
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg("|w" + " AVAILABLE TALENTS".center(80) + "|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        # Show general talents
        general_talents = get_talents_by_category("General")
        if general_talents:
            self.caller.msg("\n|yGENERAL TALENTS:|n")
            for talent_name in sorted(general_talents):
                talent_data = TALENTS[talent_name]
                param = talent_data.get("requires_parameter", "")
                if param:
                    self.caller.msg(f"  • |w{talent_name}|n |c({param})|n")
                else:
                    self.caller.msg(f"  • |w{talent_name}|n")
        
        # Show faction-specific talents if character has a faction
        if faction:
            faction_talents = get_talents_by_faction(faction)
            if faction_talents:
                self.caller.msg(f"\n|y{faction.upper()} TALENTS:|n")
                for talent_name in sorted(faction_talents):
                    talent_data = TALENTS[talent_name]
                    param = talent_data.get("requires_parameter", "")
                    if param:
                        self.caller.msg(f"  • |w{talent_name}|n |c({param})|n")
                    else:
                        self.caller.msg(f"  • |w{talent_name}|n")
        
        # Show spice talents
        spice_physical = get_talents_by_category("Spice (Physical)")
        spice_mental = get_talents_by_category("Spice (Mental)")
        if spice_physical or spice_mental:
            self.caller.msg("\n|ySPICE TALENTS:|n")
            self.caller.msg("|c(Requires spice consumption)|n")
            for talent_name in sorted(spice_physical + spice_mental):
                self.caller.msg(f"  • |w{talent_name}|n")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg("|cUse |w+chargen/talents/info <talent>|c to see detailed information.|n")
        self.caller.msg("|cUse |w+chargen/talents add <talent>|c to add a talent.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _show_talent_info(self, talent_name):
        """Show detailed information about a talent."""
        talent_data = get_talent(talent_name)
        
        if not talent_data:
            self.caller.msg(f"|rUnknown talent: {talent_name}|n")
            self.caller.msg("Use |w+chargen/talents/list|n to see available talents.")
            return
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg(f"|w{talent_name}|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        category = talent_data.get("category", "General")
        self.caller.msg(f"|yCategory:|n {category}")
        
        param = talent_data.get("requires_parameter", "")
        if param:
            self.caller.msg(f"|yRequires Parameter:|n {param}")
            if param == "skill":
                self.caller.msg(f"|cExample: |w+chargen/talents add {talent_name} (Battle)|c|n")
            elif param == "drive":
                self.caller.msg(f"|cExample: |w+chargen/talents add {talent_name} (Duty)|c|n")
        
        description = talent_data.get("description", "")
        if description:
            self.caller.msg(f"\n|yDescription:|n {description}")
        
        # Check if character can take this talent
        can_take, reason = can_character_take_talent(self.caller, talent_name)
        if can_take:
            self.caller.msg(f"\n|g✓ {reason}|n")
        else:
            self.caller.msg(f"\n|r✗ {reason}|n")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg(f"|cUse |w+chargen/talents add {talent_name}|c to select this talent.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _setup_drives(self):
        """Handle drive assignment."""
        if not self.caller.db.chargen_archetype:
            self.caller.msg("|rYou must select an archetype first. Use |w+chargen/archetype <name>|r|n")
            return
        
        drives = self.caller.db.stats.get("drives", {})
        valid_drives = ["duty", "faith", "justice", "power", "truth"]
        required_ratings = [8, 7, 6, 5, 4]
        
        # If no args, show current drives
        if not self.args:
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|wDRIVES|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|yYou must assign the ratings 8, 7, 6, 5, and 4 (one to each drive).|n")
            self.caller.msg("|yDrives with rating 6+ need statements.|n")
            
            self.caller.msg("\n|yCurrent Drive Ratings:|n")
            assigned = []
            for drive_name in valid_drives:
                drive = drives.get(drive_name, {})
                if isinstance(drive, dict):
                    rating = drive.get("rating", 0)
                    statement = drive.get("statement", "")
                else:
                    rating = 0
                    statement = ""
                
                if rating > 0:
                    assigned.append(rating)
                    status = f"Rating: {rating}"
                    if statement:
                        status += f" - {statement[:50]}..."
                    self.caller.msg(f"  {drive_name.capitalize():<12} {status}")
                else:
                    self.caller.msg(f"  {drive_name.capitalize():<12} Not set")
            
            remaining_ratings = [r for r in required_ratings if r not in assigned]
            if remaining_ratings:
                self.caller.msg(f"\n|yRemaining Ratings:|n {', '.join(map(str, sorted(remaining_ratings, reverse=True)))}")
            
            self.caller.msg("\n|cUsage: |w+chargen/drives set <drive>=<rating>|c")
            self.caller.msg("|cExample: |w+chargen/drives set duty=8|c")
            self.caller.msg("|cDrives: Duty, Faith, Justice, Power, Truth|n")
            self.caller.msg("|cRatings: 8 (highest), 7, 6, 5, 4 (lowest)|n")
            self.caller.msg("\n|cTo set drive statements: |w+chargen/drives statement <drive>=<statement>|c")
            self.caller.msg("|w" + "=" * 80 + "|n")
            return
        
        # Parse command
        parts = self.args.split(None, 1)
        if len(parts) < 2:
            self.caller.msg("|rUsage: +chargen/drives set <drive>=<rating> OR +chargen/drives statement <drive>=<statement>|n")
            return
        
        action = parts[0].lower()
        
        if action == "set":
            if "=" not in parts[1]:
                self.caller.msg("|rUsage: +chargen/drives set <drive>=<rating>|n")
                return
            
            drive_parts = parts[1].split("=", 1)
            drive_name = drive_parts[0].strip().lower()
            try:
                rating = int(drive_parts[1].strip())
            except ValueError:
                self.caller.msg("|rRating must be a number (4, 5, 6, 7, or 8).|n")
                return
            
            if drive_name not in valid_drives:
                self.caller.msg(f"|rInvalid drive. Must be one of: {', '.join([d.capitalize() for d in valid_drives])}|n")
                return
            
            if rating not in required_ratings:
                self.caller.msg(f"|rRating must be one of: {', '.join(map(str, required_ratings))}|n")
                return
            
            success, message = self.caller.set_drive_rating(drive_name, rating)
            if success:
                self.caller.msg(f"|g{message}|n")
                
                # Check if all drives are set
                all_set = True
                for d in valid_drives:
                    d_obj = self.caller.db.stats["drives"].get(d, {})
                    if isinstance(d_obj, dict):
                        if d_obj.get("rating", 0) not in required_ratings:
                            all_set = False
                            break
                    else:
                        all_set = False
                        break
                
                if all_set:
                    self.caller.msg("|yAll drives assigned!|n")
                    self.caller.msg("|yRemember to add statements for drives with rating 6 or higher.|n")
                    self.caller.msg("\n|cNext: Use |w+chargen/drives statement <drive>=<statement>|c to add statements.|n")
                    self.caller.msg("|cThen use |w+chargen/assets|c for assets.|n")
            else:
                self.caller.msg(f"|r{message}|n")
                
        elif action == "statement":
            if "=" not in parts[1]:
                self.caller.msg("|rUsage: +chargen/drives statement <drive>=<statement>|n")
                return
            
            drive_parts = parts[1].split("=", 1)
            drive_name = drive_parts[0].strip().lower()
            statement = drive_parts[1].strip()
            
            if drive_name not in valid_drives:
                self.caller.msg(f"|rInvalid drive. Must be one of: {', '.join([d.capitalize() for d in valid_drives])}|n")
                return
            
            if not statement:
                self.caller.msg("|rStatement cannot be empty.|n")
                return
            
            success, message = self.caller.set_drive_statement(drive_name, statement)
            if success:
                self.caller.msg(f"|g{message}|n")
            else:
                self.caller.msg(f"|r{message}|n")
        else:
            self.caller.msg("|rAction must be 'set' or 'statement'.|n")
    
    def _setup_assets(self):
        """Handle starting assets."""
        if not self.caller.db.chargen_archetype:
            self.caller.msg("|rYou must select an archetype first. Use |w+chargen/archetype <name>|r|n")
            return
        
        assets = self.caller.get_assets()
        
        # Count tangible assets
        tangible_count = 0
        for asset in assets:
            if hasattr(asset, 'get_asset_type'):
                if asset.get_asset_type() == "Personal" or asset.get_asset_type() == "Warfare":
                    tangible_count += 1
        
        # Show current status
        if not self.args:
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|wSTARTING ASSETS|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|yYou need 3 assets total.|n")
            self.caller.msg("|yAt least one must be tangible (Personal or Warfare asset).|n")
            
            self.caller.msg(f"\n|yCurrent Assets ({len(assets)}/3):|n")
            if assets:
                for asset in assets:
                    asset_type = asset.get_asset_type() if hasattr(asset, 'get_asset_type') else "Unknown"
                    tangible = "|g[Tangible]|n" if asset_type in ["Personal", "Warfare"] else "|m[Intangible]|n"
                    self.caller.msg(f"  • {asset.name} {tangible}")
            else:
                self.caller.msg("  None yet")
            
            if len(assets) < 3:
                needed_tangible = 1 if tangible_count == 0 else 0
                if needed_tangible > 0:
                    self.caller.msg(f"\n|yYou still need at least {needed_tangible} tangible asset(s).|n")
            
            self.caller.msg("\n|cUse |w+asset/create <asset name>|c to create assets.|n")
            self.caller.msg("|cUse |w+asset/list|c to see available assets.|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            return
        
        # For now, just remind them to use +asset/create
        self.caller.msg("|yUse |w+asset/create <asset name>|y to create assets.|n")
        self.caller.msg("|yUse |w+asset/list|y to see available assets.|n")
    
    def _show_status(self):
        """Show character generation progress."""
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg("|w" + " CHARACTER GENERATION STATUS".center(80) + "|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        # Step 2: Archetype
        archetype = self.caller.db.chargen_archetype
        if archetype:
            self.caller.msg(f"|g[✓]|n Step 2: Archetype - |w{archetype['trait']}|n")
        else:
            self.caller.msg(f"|r[ ]|n Step 2: Archetype - Not selected")
            self.caller.msg("     |cUse |w+chargen/archetype <name>|c|n")
        
        # Caste
        caste = self.caller.db.caste
        if caste:
            self.caller.msg(f"|g[✓]|n Caste - |w{caste}|n")
        else:
            self.caller.msg(f"|y[~]|n Caste - Not set (optional)")
            self.caller.msg("     |cUse |w+chargen/caste <caste>|c (Na-Familia, Bondsman, Pyon)|n")
        
        # Title
        title_key = self.caller.db.title
        if title_key:
            title = get_title(title_key)
            if title:
                gender = getattr(self.caller.db, 'gender', 'masculine')
                if gender not in ['masculine', 'feminine']:
                    gender = 'masculine'
                display_name = get_title_display_name(title_key, gender)
                architect = title['architect_access']
                if architect == "full":
                    architect_display = " (Full Architect)"
                elif architect == "limited":
                    architect_display = " (Limited Architect)"
                else:
                    architect_display = " (Roleplay)"
                self.caller.msg(f"|g[✓]|n Title - |w{display_name}|n{architect_display}")
            else:
                self.caller.msg(f"|g[✓]|n Title - |w{title_key}|n")
        else:
            self.caller.msg(f"|y[~]|n Title - Not set (optional)")
            self.caller.msg("     |cUse |w+chargen/title/list|c to see available titles|n")
        
        # Faction
        faction = self.caller.db.faction
        if faction:
            # Validate faction requirements
            talent_valid, talent_msg, _ = validate_faction_talents(self.caller, faction)
            focus_valid, focus_msg, _ = validate_faction_focuses(self.caller, faction)
            
            if talent_valid and focus_valid:
                self.caller.msg(f"|g[✓]|n Faction - |w{faction}|n (requirements met)")
            else:
                self.caller.msg(f"|y[~]|n Faction - |w{faction}|n (requirements not met)")
                if not talent_valid:
                    self.caller.msg(f"     |r{talent_msg}|n")
                if not focus_valid:
                    self.caller.msg(f"     |r{focus_msg}|n")
        else:
            self.caller.msg(f"|y[~]|n Faction - Not set (optional)")
            self.caller.msg("     |cUse |w+chargen/faction/list|c to see factions|n")
        
        # Step 3: Skills
        skill_points = self.caller.db.chargen_skill_points
        if skill_points is not None:
            if skill_points == 0:
                self.caller.msg(f"|g[✓]|n Step 3: Skills - Complete")
            else:
                self.caller.msg(f"|y[~]|n Step 3: Skills - {skill_points} points remaining")
                self.caller.msg("     |cUse |w+chargen/skills <skill>=<points>|c|n")
        else:
            if archetype:
                self.caller.msg(f"|y[~]|n Step 3: Skills - Not started (have {archetype.get('primary_skill', 'Unknown')}/{archetype.get('secondary_skill', 'Unknown')} base)")
                self.caller.msg("     |cUse |w+chargen/skills|c to assign skill points|n")
            else:
                self.caller.msg(f"|r[ ]|n Step 3: Skills - Requires archetype")
        
        # Step 4: Focuses
        focuses = self.caller.db.stats.get("focuses", [])
        if len(focuses) >= 4:
            self.caller.msg(f"|g[✓]|n Step 4: Focuses - Complete ({len(focuses)}/4)")
        else:
            self.caller.msg(f"|y[~]|n Step 4: Focuses - {len(focuses)}/4")
            self.caller.msg("     |cUse |w+chargen/focuses|c to add focuses|n")
        
        # Step 5: Talents
        talents = self.caller.db.stats.get("talents", [])
        if len(talents) >= 3:
            self.caller.msg(f"|g[✓]|n Step 5: Talents - Complete ({len(talents)}/3)")
        else:
            self.caller.msg(f"|y[~]|n Step 5: Talents - {len(talents)}/3")
            self.caller.msg("     |cUse |w+chargen/talents|c to add talents|n")
        
        # Step 6: Drives
        drives = self.caller.db.stats.get("drives", {})
        valid_drives = ["duty", "faith", "justice", "power", "truth"]
        required_ratings = [8, 7, 6, 5, 4]
        drives_set = 0
        for drive_name in valid_drives:
            drive = drives.get(drive_name, {})
            if isinstance(drive, dict):
                rating = drive.get("rating", 0)
                if rating in required_ratings:
                    drives_set += 1
        
        if drives_set == 5:
            # Check statements for top 3
            top_3_count = 0
            for drive_name in valid_drives:
                drive = drives.get(drive_name, {})
                if isinstance(drive, dict):
                    rating = drive.get("rating", 0)
                    statement = drive.get("statement", "")
                    if rating >= 6 and statement:
                        top_3_count += 1
            
            if top_3_count >= 3:
                self.caller.msg(f"|g[✓]|n Step 6: Drives - Complete")
            else:
                self.caller.msg(f"|y[~]|n Step 6: Drives - Ratings set, {top_3_count}/3 statements needed")
                self.caller.msg("     |cUse |w+chargen/drives statement <drive>=<statement>|c|n")
        else:
            self.caller.msg(f"|y[~]|n Step 6: Drives - {drives_set}/5 ratings set")
            self.caller.msg("     |cUse |w+chargen/drives set <drive>=<rating>|c|n")
        
        # Step 7: Assets
        assets = self.caller.get_assets()
        if len(assets) >= 3:
            # Check if at least one is tangible
            tangible_count = 0
            for asset in assets:
                if hasattr(asset, 'get_asset_type'):
                    if asset.get_asset_type() in ["Personal", "Warfare"]:
                        tangible_count += 1
            
            if tangible_count >= 1:
                self.caller.msg(f"|g[✓]|n Step 7: Assets - Complete ({len(assets)}/3, {tangible_count} tangible)")
            else:
                self.caller.msg(f"|y[~]|n Step 7: Assets - {len(assets)}/3, need at least 1 tangible")
                self.caller.msg("     |cUse |w+asset/create|c to create tangible assets|n")
        else:
            self.caller.msg(f"|y[~]|n Step 7: Assets - {len(assets)}/3")
            self.caller.msg("     |cUse |w+asset/create <name>|c to create assets|n")
        
        # Step 8: Finishing Touches
        bio_complete = (
            self.caller.db.personality_traits and
            self.caller.db.ambition and
            (hasattr(self.caller, 'db') and self.caller.db.shortdesc)
        )
        if bio_complete:
            self.caller.msg(f"|g[✓]|n Step 8: Finishing Touches - Complete")
        else:
            self.caller.msg(f"|y[~]|n Step 8: Finishing Touches - Use |w+bio|c command|n")
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        # Show help
        self.caller.msg("\n|cQuick Commands:|n")
        self.caller.msg("  |w+chargen/list|c - List archetypes")
        self.caller.msg("  |w+chargen/info <archetype>|c - Archetype details")
        self.caller.msg("  |w+chargen/caste <caste>|c - Set caste")
        self.caller.msg("  |w+chargen/title/list|c - List titles")
        self.caller.msg("  |w+chargen/faction/list|c - List factions")
        self.caller.msg("  |w+chargen/status|c - Show this status")
        self.caller.msg("  |w+bio|c - Finishing touches (Step 8)")

