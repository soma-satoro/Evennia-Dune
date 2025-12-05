"""
Quick Advancement Point Award Commands

Provides simplified commands for GMs to award advancement points
based on the specific triggers defined in Modiphius 2d20.
"""

from evennia.commands.default.muxcommand import MuxCommand


class CmdAdvanceAward(MuxCommand):
    """
    Award advancement points for specific triggers.
    
    Usage:
        +xp/pain <character>        - Award 1 point (defeated in conflict)
        +xp/failure <character>     - Award 1 point (failed Difficulty 3+ test)
        +xp/peril <character>       - Award 1 point (GM spent 4+ Threat)
        +xp/ambition <character>    - Award 1 point (minor ambition progress)
        +xp/ambition/major <character> - Award 3 points (major ambition progress)
        +xp/impress <character>     - Award 1 point (impressed the group)
        +xp/custom <character>=<amount> - Award custom amount
    
    Switches:
        /pain       - Defeated in conflict (1 point)
        /failure    - Failed Difficulty 3+ test (1 point)
        /peril      - GM spent 4+ Threat (1 point)
        /ambition   - Minor ambition progress (1 point)
        /major      - Major ambition progress (3 points, use with /ambition)
        /impress    - Impressed the group (1 point, max once per session)
        /custom     - Award custom amount
    
    Examples:
        +xp/pain Paul
        +xp/failure Alia
        +xp/peril Jessica
        +xp/ambition Leto
        +xp/ambition/major Ghanima
        +xp/impress Duncan
        +xp/custom Stilgar=5
    
    Note: This command requires Builder permissions.
    """
    
    key = "+xp"
    aliases = []
    locks = "cmd:perm(Builder)"
    help_category = "Character"
    
    def func(self):
        """Main command handler"""
        
        # Determine the award type and amount
        award_type = None
        amount = 0
        reason = ""
        
        if "pain" in self.switches:
            award_type = "Pain"
            amount = 1
            reason = "Defeated in conflict"
        elif "failure" in self.switches:
            award_type = "Failure"
            amount = 1
            reason = "Failed Difficulty 3+ test"
        elif "peril" in self.switches:
            award_type = "Peril"
            amount = 1
            reason = "GM spent 4+ Threat at once"
        elif "ambition" in self.switches:
            if "major" in self.switches:
                award_type = "Ambition (Major)"
                amount = 3
                reason = "Major contribution to ambition"
            else:
                award_type = "Ambition (Minor)"
                amount = 1
                reason = "Minor contribution to ambition"
        elif "impress" in self.switches:
            award_type = "Impressing the Group"
            amount = 1
            reason = "Impressed the group (max once per session)"
        elif "custom" in self.switches:
            award_type = "Custom"
            # Amount will be parsed from args
        else:
            self.caller.msg("|rPlease specify an award type.|n")
            self.caller.msg("Use: +xp/pain, +xp/failure, +xp/peril, +xp/ambition, +xp/impress, or +xp/custom")
            return
        
        # Parse character name (and amount for custom)
        if "custom" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +xp/custom <character>=<amount>")
                return
            
            char_name, amount_str = self.args.split("=", 1)
            char_name = char_name.strip()
            amount_str = amount_str.strip()
            
            try:
                amount = int(amount_str)
            except ValueError:
                self.caller.msg("Amount must be a number.")
                return
            
            if amount < 1:
                self.caller.msg("Amount must be positive.")
                return
            
            reason = "Custom award"
        else:
            if not self.args:
                self.caller.msg("Usage: +xp/<type> <character>")
                return
            
            char_name = self.args.strip()
        
        # Find target character
        target = self.caller.search(char_name)
        if not target:
            return
        
        if not hasattr(target.db, 'stats'):
            self.caller.msg(f"{target.name} does not have stats initialized.")
            return
        
        # Initialize advancement tracking if needed
        if not hasattr(target.db, 'advancement_points'):
            target.db.advancement_points = 0
        if not hasattr(target.db, 'advancement_history'):
            target.db.advancement_history = []
        
        # Award points
        target.db.advancement_points += amount
        
        # Record in history
        import datetime
        target.db.advancement_history.append({
            "type": "award",
            "award_type": award_type,
            "reason": reason,
            "points": amount,
            "awarded_by": self.caller.name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Notify staff
        self.caller.msg(f"|g[XP] {award_type}:|n Awarded {amount} advancement point{'s' if amount > 1 else ''} to {target.name}")
        self.caller.msg(f"|cReason:|n {reason}")
        self.caller.msg(f"|wNew total:|n {target.db.advancement_points} points")
        
        # Notify target
        target.msg("|w" + "=" * 78 + "|n")
        target.msg("|g*** ADVANCEMENT POINTS AWARDED ***|n".center(78))
        target.msg("|w" + "=" * 78 + "|n")
        target.msg(f"|yType:|n {award_type}")
        target.msg(f"|yReason:|n {reason}")
        target.msg(f"|yAmount:|n {amount} point{'s' if amount > 1 else ''}")
        target.msg(f"|yAwarded by:|n {self.caller.name}")
        target.msg(f"|yYour Total:|n {target.db.advancement_points} points")
        target.msg("|w" + "=" * 78 + "|n")
        target.msg("Use |w+advance|n to see what you can purchase with your points.")
        target.msg("|w" + "=" * 78 + "|n")


class CmdAdvanceSession(MuxCommand):
    """
    Track advancement point awards per session.
    
    Usage:
        +xp/session              - View current session awards
        +xp/session/clear        - Clear session tracking (end of session)
        +xp/session/list         - List all characters and their session awards
    
    This command helps GMs track who has received "Impressing the Group"
    awards (max 1 per session) and other session-based awards.
    
    Note: This command requires Builder permissions.
    """
    
    key = "+xp"
    aliases = []
    locks = "cmd:perm(Builder)"
    help_category = "Character"
    
    def func(self):
        """Main command handler"""
        
        # Initialize global session tracking if needed
        from evennia import DefaultScript
        
        # Get or create the session tracker
        tracker = DefaultScript.objects.filter(db_key="advancement_session_tracker").first()
        
        if not tracker:
            # Create the tracker
            tracker = DefaultScript.objects.create(
                db_key="advancement_session_tracker",
                db_persistent=True
            )
            tracker.db.session_awards = {}
            tracker.db.session_start = None
        
        if "clear" in self.switches:
            # Clear session tracking
            tracker.db.session_awards = {}
            import datetime
            tracker.db.session_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.caller.msg("|g[XP] Session tracking cleared.|n")
            self.caller.msg("New session started.")
            return
        
        if "list" in self.switches:
            # List all session awards
            session_awards = tracker.db.session_awards or {}
            
            if not session_awards:
                self.caller.msg("|yNo advancement points awarded this session yet.|n")
                return
            
            lines = []
            lines.append("|w" + "=" * 78 + "|n")
            lines.append("|w" + " SESSION ADVANCEMENT AWARDS".center(78) + "|n")
            lines.append("|w" + "=" * 78 + "|n")
            
            if tracker.db.session_start:
                lines.append(f"|wSession Start:|n {tracker.db.session_start}")
                lines.append("")
            
            for char_name, awards in sorted(session_awards.items()):
                total = sum(award.get('amount', 0) for award in awards)
                lines.append(f"|y{char_name}:|n {total} points")
                
                for award in awards:
                    award_type = award.get('type', 'Unknown')
                    amount = award.get('amount', 0)
                    reason = award.get('reason', '')
                    lines.append(f"  • {award_type}: {amount} point{'s' if amount > 1 else ''} ({reason})")
                
                lines.append("")
            
            lines.append("|w" + "=" * 78 + "|n")
            self.caller.msg("\n".join(lines))
            return
        
        # Default: show session summary
        session_awards = tracker.db.session_awards or {}
        
        if not session_awards:
            self.caller.msg("|yNo advancement points awarded this session yet.|n")
            self.caller.msg("Use |w+xp/<type> <character>|n to award points.")
            return
        
        lines = []
        lines.append("|w" + "=" * 78 + "|n")
        lines.append("|w" + " SESSION SUMMARY".center(78) + "|n")
        lines.append("|w" + "=" * 78 + "|n")
        
        if tracker.db.session_start:
            lines.append(f"|wSession Start:|n {tracker.db.session_start}")
            lines.append("")
        
        total_points = 0
        for char_name, awards in sorted(session_awards.items()):
            char_total = sum(award.get('amount', 0) for award in awards)
            total_points += char_total
            lines.append(f"|y{char_name}:|n {char_total} points")
        
        lines.append("")
        lines.append(f"|wTotal Points Awarded:|n {total_points}")
        lines.append("")
        lines.append("Use |w+xp/session/list|n for details")
        lines.append("Use |w+xp/session/clear|n to start a new session")
        lines.append("|w" + "=" * 78 + "|n")
        
        self.caller.msg("\n".join(lines))

