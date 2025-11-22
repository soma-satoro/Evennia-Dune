"""
Bio Command

Command for Step 8 of character creation - Finishing Touches:
- Trait (reputation/personality)
- Ambition
- Personal Details (name, personality, appearance, relationships)
"""

from evennia.commands.default.muxcommand import MuxCommand


class CmdBio(MuxCommand):
    """
    Set finishing touches for your character (Step 8 of character generation).
    
    Usage:
        +bio - Show current bio information
        +bio/trait <trait name> - Set reputation trait
        +bio/ambition <ambition> - Set character ambition
        +bio/name <name> - Set character name (staff only, use IC naming)
        +bio/personality <description> - Set personality description
        +bio/appearance <description> - Set appearance description
        +bio/relationships <description> - Set relationships description
        
    Switches:
        /trait - Set reputation/personality trait
        /ambition - Set character ambition (related to highest drive)
        /personality - Set personality description
        /appearance - Set appearance description
        /relationships - Set relationships description
        /name - Set character name (staff only)
    
    Step 8 Questions:
        Trait - Choose a trait based on reputation or personality
        Ambition - Decide on a goal related to highest drive
        Personal Details - Name, personality, appearance, relationships
    
    Examples:
        +bio - View current bio
        +bio/trait Honorable - Set reputation trait
        +bio/ambition Become the premier assassin in the Imperium - Set ambition
        +bio/personality Stoic and disciplined, with a dry wit - Set personality
        +bio/appearance Tall and lean, with piercing blue eyes - Set appearance
        +bio/relationships Close to my House retainers, distant from family - Set relationships
    """
    
    key = "+bio"
    aliases = ["bio"]
    help_category = "Character"
    
    def func(self):
        """Handle bio commands"""
        
        # No arguments - show current bio
        if not self.args and not self.switches:
            self._show_bio()
            return
        
        # No args with switch - show help for that section
        if not self.args:
            if "trait" in self.switches:
                self.caller.msg("Usage: +bio/trait <trait name>")
                self.caller.msg("Example: +bio/trait Honorable")
                self.caller.msg("\n|cA trait is based on your character's reputation or personality.|n")
                return
            elif "ambition" in self.switches:
                self.caller.msg("Usage: +bio/ambition <ambition statement>")
                self.caller.msg("Example: +bio/ambition Become the premier assassin in the Imperium")
                self.caller.msg("\n|cAmbition should be related to your highest drive.|n")
                return
            elif "personality" in self.switches:
                self.caller.msg("Usage: +bio/personality <personality description>")
                self.caller.msg("Example: +bio/personality Stoic and disciplined, with a dry wit")
                return
            elif "appearance" in self.switches:
                self.caller.msg("Usage: +bio/appearance <appearance description>")
                self.caller.msg("Example: +bio/appearance Tall and lean, with piercing blue eyes")
                return
            elif "relationships" in self.switches:
                self.caller.msg("Usage: +bio/relationships <relationships description>")
                self.caller.msg("Example: +bio/relationships Close to my House retainers, distant from family")
                return
            elif "name" in self.switches:
                self.caller.msg("Usage: +bio/name <new name>")
                self.caller.msg("\n|cNote: This is staff-only. Characters should set their name through RP.|n")
                return
        
        # Handle trait
        if "trait" in self.switches:
            self._set_trait(self.args.strip())
            return
        
        # Handle ambition
        if "ambition" in self.switches:
            self._set_ambition(self.args.strip())
            return
        
        # Handle personality
        if "personality" in self.switches:
            self._set_personality(self.args.strip())
            return
        
        # Handle appearance
        if "appearance" in self.switches:
            self._set_appearance(self.args.strip())
            return
        
        # Handle relationships
        if "relationships" in self.switches:
            self._set_relationships(self.args.strip())
            return
        
        # Handle name (staff only)
        if "name" in self.switches:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("|rYou don't have permission to change names.|n")
                return
            self._set_name(self.args.strip())
            return
        
        # Default: show bio
        self._show_bio()
    
    def _show_bio(self):
        """Display current bio information"""
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg("|w" + " CHARACTER BIO".center(80) + "|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        # Archetype (if set)
        archetype = self.caller.db.chargen_archetype
        if archetype:
            self.caller.msg(f"|yArchetype:|n {archetype.get('trait', 'Unknown')}")
            if archetype.get('category'):
                self.caller.msg(f"|yCategory:|n {archetype['category']}")
        
        # Reputation Trait (from Step 8)
        reputation_trait = self.caller.db.reputation_trait
        if reputation_trait:
            self.caller.msg(f"\n|yReputation Trait:|n {reputation_trait}")
        else:
            self.caller.msg("\n|yReputation Trait:|n |rNot set|n (use |w+bio/trait <trait>|r|n)")
        
        # Ambition
        ambition = self.caller.db.ambition
        if ambition:
            self.caller.msg(f"\n|yAmbition:|n {ambition}")
        else:
            self.caller.msg("\n|yAmbition:|n |rNot set|n (use |w+bio/ambition <ambition>|r|n)")
        
        # Personality
        personality = self.caller.db.personality_traits
        if personality:
            self.caller.msg(f"\n|yPersonality:|n {personality}")
        else:
            self.caller.msg("\n|yPersonality:|n |rNot set|n (use |w+bio/personality <description>|r|n)")
        
        # Appearance
        appearance = self.caller.db.appearance
        if appearance:
            self.caller.msg(f"\n|yAppearance:|n {appearance}")
        else:
            self.caller.msg("\n|yAppearance:|n |rNot set|n (use |w+bio/appearance <description>|r|n)")
        
        # Relationships
        relationships = self.caller.db.relationships
        if relationships:
            self.caller.msg(f"\n|yRelationships:|n {relationships}")
        else:
            self.caller.msg("\n|yRelationships:|n |rNot set|n (use |w+bio/relationships <description>|r|n)")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg("|cUse |w+bio/<section> <text>|c to set or update each section.|n")
        self.caller.msg("|cSections: trait, ambition, personality, appearance, relationships|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _set_trait(self, trait):
        """Set reputation trait"""
        if not trait:
            self.caller.msg("Usage: +bio/trait <trait name>")
            return
        
        self.caller.db.reputation_trait = trait
        self.caller.msg(f"|gSet reputation trait:|n {trait}")
        self.caller.msg("|cThis trait reflects how others perceive your character.|n")
    
    def _set_ambition(self, ambition):
        """Set character ambition"""
        if not ambition:
            self.caller.msg("Usage: +bio/ambition <ambition statement>")
            return
        
        # Check highest drive to suggest relevance
        drives = self.caller.db.stats.get("drives", {})
        highest_drive = None
        highest_rating = 0
        
        for drive_name in ["duty", "faith", "justice", "power", "truth"]:
            drive = drives.get(drive_name, {})
            if isinstance(drive, dict):
                rating = drive.get("rating", 0)
                if rating > highest_rating:
                    highest_rating = rating
                    highest_drive = drive_name.capitalize()
        
        self.caller.db.ambition = ambition
        self.caller.msg(f"|gSet ambition:|n {ambition}")
        if highest_drive:
            self.caller.msg(f"|cNote: Your highest drive is {highest_drive} ({highest_rating}). Make sure your ambition relates to it.|n")
        self.caller.msg("|cAmbition guides your character's long-term actions.|n")
    
    def _set_personality(self, personality):
        """Set personality description"""
        if not personality:
            self.caller.msg("Usage: +bio/personality <personality description>")
            return
        
        self.caller.db.personality_traits = personality
        self.caller.msg(f"|gSet personality:|n {personality}")
        self.caller.msg("|cPersonality describes how your character behaves in normal circumstances.|n")
    
    def _set_appearance(self, appearance):
        """Set appearance description"""
        if not appearance:
            self.caller.msg("Usage: +bio/appearance <appearance description>")
            return
        
        self.caller.db.appearance = appearance
        self.caller.msg(f"|gSet appearance:|n {appearance}")
        self.caller.msg("|cAppearance describes what your character looks like.|n")
    
    def _set_relationships(self, relationships):
        """Set relationships description"""
        if not relationships:
            self.caller.msg("Usage: +bio/relationships <relationships description>")
            return
        
        self.caller.db.relationships = relationships
        self.caller.msg(f"|gSet relationships:|n {relationships}")
        self.caller.msg("|cRelationships describe your character's connections to others.|n")
    
    def _set_name(self, name):
        """Set character name (staff only)"""
        if not name:
            self.caller.msg("Usage: +bio/name <new name>")
            return
        
        target = self.caller
        old_name = target.key
        
        # Set the name
        target.key = name
        target.save()
        
        self.caller.msg(f"|gChanged {old_name}'s name to {name}|n")
        target.msg(f"|yYour name has been changed to: {name}|n")

