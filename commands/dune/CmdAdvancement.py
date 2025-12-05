"""
Character Advancement Commands

Implements the Modiphius 2d20 character advancement system for Dune,
allowing characters to gain and spend advancement points to improve
their skills, focuses, talents, and assets.
"""

from evennia.commands.default.muxcommand import MuxCommand


class CmdAdvancement(MuxCommand):
    """
    Manage character advancement points and purchases.
    
    Usage:
        +advance                    - View your advancement points and purchase history
        +advance/award <char>=<points> - Award advancement points (staff only)
        +advance/spend <type>=<value>  - Spend points on an advancement
        +advance/retrain <type>=<old>/<new> - Retrain (half cost)
        +advance/history            - View detailed advancement history
        +advance/reset <character>  - Reset advancement tracking (staff only)
    
    Advancement Types:
        skill/<name>        - Increase a skill by +1 (max 8, once per skill)
                              Cost: 10 + (previous skill advances)
        focus/<name>        - Purchase a new focus (requires skill 6+)
                              Cost: Current number of focuses
        talent/<name>       - Purchase a new talent
                              Cost: 3 × current number of talents
        asset/<name>        - Make an asset permanent
                              Cost: 3 points
        asset/<name>/quality - Improve asset quality by +1
                              Cost: 2 × new Quality
    
    Retraining (Half Cost):
        Retrain reduces cost by half (rounded up), but requires removing
        an existing ability:
        - Skill retrain: Another skill reduced by 1 (min 4)
        - Focus retrain: Remove an existing focus
        - Talent retrain: Remove an existing talent
    
    Gaining Advancement Points:
        - Pain: 1 point when defeated in conflict
        - Failure: 1 point when failing Difficulty 3+ test
        - Peril: 1 point when GM spends 4+ Threat at once
        - Ambition (minor): 1 point for minor contribution
        - Ambition (major): 3 points for major contribution
        - Impressing the Group: 1 point (max once per session)
    
    Examples:
        +advance
        +advance/award Paul=5
        +advance/spend skill/battle
        +advance/spend focus/Tactics
        +advance/spend talent/Mentat Training
        +advance/spend asset/Personal Shield
        +advance/retrain skill/move/battle
        +advance/retrain focus/Charm/Tactics
    """
    
    key = "+advance"
    aliases = ["advance", "+xp", "xp"]
    help_category = "Character"
    
    def func(self):
        """Main command handler"""
        
        # Check if character has stats initialized
        if not hasattr(self.caller.db, 'stats'):
            self.caller.msg("Your character does not have stats initialized.")
            return
        
        # Initialize advancement tracking if needed
        self._init_advancement_tracking()
        
        # Handle different switches
        if "award" in self.switches:
            self._handle_award()
        elif "spend" in self.switches:
            self._handle_spend()
        elif "retrain" in self.switches:
            self._handle_retrain()
        elif "history" in self.switches:
            self._handle_history()
        elif "reset" in self.switches:
            self._handle_reset()
        else:
            # Default: Show current advancement status
            self._show_advancement_status()
    
    def _init_advancement_tracking(self):
        """Initialize advancement tracking attributes if they don't exist"""
        if not hasattr(self.caller.db, 'advancement_points'):
            self.caller.db.advancement_points = 0
        
        if not hasattr(self.caller.db, 'advancement_history'):
            self.caller.db.advancement_history = []
        
        if not hasattr(self.caller.db, 'skill_advances'):
            # Track how many times each skill has been advanced
            self.caller.db.skill_advances = {
                "battle": 0,
                "communicate": 0,
                "discipline": 0,
                "move": 0,
                "understand": 0
            }
        
        if not hasattr(self.caller.db, 'total_skill_advances'):
            # Track total number of skill advances for cost calculation
            self.caller.db.total_skill_advances = 0
    
    def _show_advancement_status(self):
        """Show current advancement points and purchase options"""
        lines = []
        lines.append("|w" + "=" * 78 + "|n")
        lines.append("|w" + f" CHARACTER ADVANCEMENT - {self.caller.name}".center(78) + "|n")
        lines.append("|w" + "=" * 78 + "|n")
        
        # Show current points
        points = self.caller.db.advancement_points
        lines.append(f"|yAvailable Advancement Points:|n {points}")
        lines.append("")
        
        # Show what can be purchased
        lines.append("|cWhat You Can Purchase:|n")
        lines.append("")
        
        # Skill advances
        lines.append("|wSkills:|n (Max 8, can only advance each skill once)")
        skills = self.caller.db.stats.get("skills", {})
        skill_advances = self.caller.db.skill_advances
        total_advances = self.caller.db.total_skill_advances
        
        for skill_name in ["battle", "communicate", "discipline", "move", "understand"]:
            current_val = skills.get(skill_name, 0)
            times_advanced = skill_advances.get(skill_name, 0)
            
            if times_advanced > 0:
                status = "|r(Already advanced)|n"
                cost = "N/A"
            elif current_val >= 8:
                status = "|r(At maximum)|n"
                cost = "N/A"
            else:
                cost = 10 + total_advances
                status = f"|g{cost} points|n"
            
            lines.append(f"  {skill_name.capitalize():<12} (Current: {current_val}) - {status}")
        
        lines.append("")
        
        # Focus
        focuses = self.caller.db.stats.get("focuses", [])
        focus_count = len(focuses)
        focus_cost = focus_count
        
        # Check if any skill is 6+
        can_buy_focus = any(v >= 6 for v in skills.values())
        if can_buy_focus:
            lines.append(f"|wFocus:|n {focus_cost} points |g(Requires skill 6+)|n")
        else:
            lines.append(f"|wFocus:|n {focus_cost} points |r(Need skill 6+ first)|n")
        
        lines.append(f"  Current focuses: {focus_count}")
        lines.append("")
        
        # Talent
        talents = self.caller.db.stats.get("talents", [])
        talent_count = len(talents)
        talent_cost = 3 * talent_count
        lines.append(f"|wTalent:|n {talent_cost} points")
        lines.append(f"  Current talents: {talent_count}")
        lines.append("")
        
        # Asset
        lines.append(f"|wAsset:|n 3 points (make permanent) or 2×Quality (improve)")
        lines.append("")
        
        # Retraining
        lines.append("|yRetraining:|n Half cost (rounded up), but must remove existing ability")
        lines.append("  Use: +advance/retrain skill/old/new")
        lines.append("")
        
        lines.append("|w" + "-" * 78 + "|n")
        lines.append("|cHow to Gain Points:|n")
        lines.append("  • Pain: 1 point (defeated in conflict)")
        lines.append("  • Failure: 1 point (failed Difficulty 3+ test)")
        lines.append("  • Peril: 1 point (GM spends 4+ Threat)")
        lines.append("  • Ambition: 1 point (minor) or 3 points (major)")
        lines.append("  • Impressing Group: 1 point (max once per session)")
        lines.append("|w" + "=" * 78 + "|n")
        
        self.caller.msg("\n".join(lines))
    
    def _handle_award(self):
        """Award advancement points (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou don't have permission to award advancement points.|n")
            return
        
        if "=" not in self.args:
            self.caller.msg("Usage: +advance/award <character>=<points>")
            return
        
        char_name, points_str = self.args.split("=", 1)
        char_name = char_name.strip()
        points_str = points_str.strip()
        
        # Find target character
        target = self.caller.search(char_name)
        if not target:
            return
        
        if not hasattr(target.db, 'stats'):
            self.caller.msg(f"{target.name} does not have stats initialized.")
            return
        
        # Parse points
        try:
            points = int(points_str)
        except ValueError:
            self.caller.msg("Points must be a number.")
            return
        
        if points < 1:
            self.caller.msg("Points must be positive.")
            return
        
        # Initialize tracking
        if not hasattr(target.db, 'advancement_points'):
            target.db.advancement_points = 0
        if not hasattr(target.db, 'advancement_history'):
            target.db.advancement_history = []
        
        # Award points
        target.db.advancement_points += points
        
        # Record in history
        import datetime
        target.db.advancement_history.append({
            "type": "award",
            "points": points,
            "awarded_by": self.caller.name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.caller.msg(f"|gAwarded {points} advancement points to {target.name}.|n")
        self.caller.msg(f"New total: {target.db.advancement_points} points")
        
        # Notify target
        target.msg(f"|gYou have been awarded {points} advancement points by {self.caller.name}!|n")
        target.msg(f"Total: {target.db.advancement_points} points")
    
    def _handle_spend(self):
        """Spend advancement points"""
        if "=" not in self.args:
            self.caller.msg("Usage: +advance/spend <type>=<value>")
            self.caller.msg("Examples:")
            self.caller.msg("  +advance/spend skill/battle")
            self.caller.msg("  +advance/spend focus/Tactics")
            self.caller.msg("  +advance/spend talent/Mentat Training")
            self.caller.msg("  +advance/spend asset/Personal Shield")
            return
        
        type_path, value = self.args.split("=", 1)
        type_path = type_path.strip().lower()
        value = value.strip()
        
        # Parse type (e.g., "skill/battle" or "asset/shield/quality")
        parts = type_path.split("/")
        if len(parts) < 1:
            self.caller.msg("Invalid type format.")
            return
        
        category = parts[0]
        
        if category == "skill":
            self._spend_skill(value)
        elif category == "focus":
            self._spend_focus(value)
        elif category == "talent":
            self._spend_talent(value)
        elif category == "asset":
            self._spend_asset(value, improve=("quality" in parts))
        else:
            self.caller.msg(f"Unknown category: {category}")
            self.caller.msg("Valid categories: skill, focus, talent, asset")
    
    def _spend_skill(self, skill_name):
        """Spend points to increase a skill"""
        skill_name = skill_name.lower()
        
        skills = self.caller.db.stats.get("skills", {})
        if skill_name not in skills:
            self.caller.msg(f"|rUnknown skill: {skill_name}|n")
            self.caller.msg("Valid skills: battle, communicate, discipline, move, understand")
            return
        
        current_val = skills[skill_name]
        skill_advances = self.caller.db.skill_advances
        
        # Check if already advanced
        if skill_advances.get(skill_name, 0) > 0:
            self.caller.msg(f"|rYou have already advanced {skill_name} once.|n")
            self.caller.msg("Each skill can only be advanced once through advancement.")
            return
        
        # Check if at maximum
        if current_val >= 8:
            self.caller.msg(f"|r{skill_name.capitalize()} is already at maximum (8).|n")
            return
        
        # Calculate cost
        total_advances = self.caller.db.total_skill_advances
        cost = 10 + total_advances
        
        # Check if enough points
        if self.caller.db.advancement_points < cost:
            self.caller.msg(f"|rNot enough advancement points.|n")
            self.caller.msg(f"Cost: {cost} points, You have: {self.caller.db.advancement_points} points")
            return
        
        # Spend points
        self.caller.db.advancement_points -= cost
        
        # Increase skill
        self.caller.set_skill(skill_name, current_val + 1)
        
        # Track advance
        skill_advances[skill_name] = skill_advances.get(skill_name, 0) + 1
        self.caller.db.skill_advances = skill_advances
        self.caller.db.total_skill_advances += 1
        
        # Record in history
        import datetime
        self.caller.db.advancement_history.append({
            "type": "skill",
            "skill": skill_name,
            "old_value": current_val,
            "new_value": current_val + 1,
            "cost": cost,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.caller.msg(f"|gAdvanced {skill_name.capitalize()} from {current_val} to {current_val + 1}!|n")
        self.caller.msg(f"Cost: {cost} points, Remaining: {self.caller.db.advancement_points} points")
    
    def _spend_focus(self, focus_name):
        """Spend points to purchase a new focus"""
        # Check if any skill is 6+
        skills = self.caller.db.stats.get("skills", {})
        if not any(v >= 6 for v in skills.values()):
            self.caller.msg("|rYou need at least one skill at 6 or higher to purchase a focus.|n")
            return
        
        # Validate focus
        from commands.dune.CmdSheet import CmdStats
        validator = CmdStats()
        validator.caller = self.caller
        if not validator._validate_focus(focus_name):
            self.caller.msg(f"|rInvalid focus: {focus_name}|n")
            self.caller.msg("Use |w+stats/focus list|n to see valid focuses.")
            return
        
        # Check for duplicates
        current_focuses = self.caller.db.stats.get("focuses", [])
        focus_lower = focus_name.lower()
        for existing_focus in current_focuses:
            if existing_focus.lower() == focus_lower:
                self.caller.msg(f"|rYou already have the focus: {existing_focus}|n")
                return
        
        # Calculate cost
        focus_count = len(current_focuses)
        cost = focus_count
        
        # Check if enough points
        if self.caller.db.advancement_points < cost:
            self.caller.msg(f"|rNot enough advancement points.|n")
            self.caller.msg(f"Cost: {cost} points, You have: {self.caller.db.advancement_points} points")
            return
        
        # Spend points
        self.caller.db.advancement_points -= cost
        
        # Add focus
        self.caller.add_focus(focus_name)
        
        # Record in history
        import datetime
        self.caller.db.advancement_history.append({
            "type": "focus",
            "focus": focus_name,
            "cost": cost,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.caller.msg(f"|gPurchased focus: {focus_name}!|n")
        self.caller.msg(f"Cost: {cost} points, Remaining: {self.caller.db.advancement_points} points")
    
    def _spend_talent(self, talent_name):
        """Spend points to purchase a new talent"""
        # Check for duplicates
        current_talents = self.caller.db.stats.get("talents", [])
        talent_lower = talent_name.lower()
        for existing_talent in current_talents:
            if existing_talent.lower() == talent_lower:
                self.caller.msg(f"|rYou already have the talent: {existing_talent}|n")
                return
        
        # Calculate cost
        talent_count = len(current_talents)
        cost = 3 * talent_count
        
        # Check if enough points
        if self.caller.db.advancement_points < cost:
            self.caller.msg(f"|rNot enough advancement points.|n")
            self.caller.msg(f"Cost: {cost} points, You have: {self.caller.db.advancement_points} points")
            return
        
        # Spend points
        self.caller.db.advancement_points -= cost
        
        # Add talent
        self.caller.add_talent(talent_name)
        
        # Record in history
        import datetime
        self.caller.db.advancement_history.append({
            "type": "talent",
            "talent": talent_name,
            "cost": cost,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.caller.msg(f"|gPurchased talent: {talent_name}!|n")
        self.caller.msg(f"Cost: {cost} points, Remaining: {self.caller.db.advancement_points} points")
    
    def _spend_asset(self, asset_name, improve=False):
        """Spend points on an asset"""
        if improve:
            # Improve quality - would need asset object system
            self.caller.msg("|yAsset quality improvement not yet implemented.|n")
            self.caller.msg("This requires the full Asset object system.")
        else:
            # Make permanent
            cost = 3
            
            # Check if enough points
            if self.caller.db.advancement_points < cost:
                self.caller.msg(f"|rNot enough advancement points.|n")
                self.caller.msg(f"Cost: {cost} points, You have: {self.caller.db.advancement_points} points")
                return
            
            # Spend points
            self.caller.db.advancement_points -= cost
            
            # Add to assets list (simple version)
            self.caller.add_asset(asset_name)
            
            # Record in history
            import datetime
            self.caller.db.advancement_history.append({
                "type": "asset",
                "asset": asset_name,
                "cost": cost,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.caller.msg(f"|gMade asset permanent: {asset_name}!|n")
            self.caller.msg(f"Cost: {cost} points, Remaining: {self.caller.db.advancement_points} points")
    
    def _handle_retrain(self):
        """Handle retraining (half cost, rounded up)"""
        if "=" not in self.args:
            self.caller.msg("Usage: +advance/retrain <type>=<old>/<new>")
            self.caller.msg("Examples:")
            self.caller.msg("  +advance/retrain skill=move/battle")
            self.caller.msg("  +advance/retrain focus=Charm/Tactics")
            self.caller.msg("  +advance/retrain talent=Old Talent/New Talent")
            return
        
        type_spec, swap = self.args.split("=", 1)
        type_spec = type_spec.strip().lower()
        
        if "/" not in swap:
            self.caller.msg("Format: <old>/<new>")
            return
        
        old_val, new_val = swap.split("/", 1)
        old_val = old_val.strip()
        new_val = new_val.strip()
        
        if type_spec == "skill":
            self._retrain_skill(old_val, new_val)
        elif type_spec == "focus":
            self._retrain_focus(old_val, new_val)
        elif type_spec == "talent":
            self._retrain_talent(old_val, new_val)
        else:
            self.caller.msg(f"Unknown type: {type_spec}")
            self.caller.msg("Valid types: skill, focus, talent")
    
    def _retrain_skill(self, old_skill, new_skill):
        """Retrain a skill (reduce one, increase another)"""
        old_skill = old_skill.lower()
        new_skill = new_skill.lower()
        
        skills = self.caller.db.stats.get("skills", {})
        
        # Validate skills
        if old_skill not in skills or new_skill not in skills:
            self.caller.msg("|rInvalid skill name.|n")
            self.caller.msg("Valid skills: battle, communicate, discipline, move, understand")
            return
        
        if old_skill == new_skill:
            self.caller.msg("|rCannot retrain a skill into itself.|n")
            return
        
        # Check old skill minimum
        if skills[old_skill] <= 4:
            self.caller.msg(f"|r{old_skill.capitalize()} is already at minimum (4).|n")
            return
        
        # Check new skill maximum and already advanced
        skill_advances = self.caller.db.skill_advances
        if skill_advances.get(new_skill, 0) > 0:
            self.caller.msg(f"|rYou have already advanced {new_skill} once.|n")
            return
        
        if skills[new_skill] >= 8:
            self.caller.msg(f"|r{new_skill.capitalize()} is already at maximum (8).|n")
            return
        
        # Calculate cost (half of normal, rounded up)
        total_advances = self.caller.db.total_skill_advances
        full_cost = 10 + total_advances
        cost = (full_cost + 1) // 2  # Round up
        
        # Check if enough points
        if self.caller.db.advancement_points < cost:
            self.caller.msg(f"|rNot enough advancement points.|n")
            self.caller.msg(f"Cost: {cost} points (half of {full_cost}), You have: {self.caller.db.advancement_points} points")
            return
        
        # Execute retrain
        self.caller.db.advancement_points -= cost
        
        old_val = skills[old_skill]
        new_val = skills[new_skill]
        
        self.caller.set_skill(old_skill, old_val - 1)
        self.caller.set_skill(new_skill, new_val + 1)
        
        # Track advance
        skill_advances[new_skill] = skill_advances.get(new_skill, 0) + 1
        self.caller.db.skill_advances = skill_advances
        self.caller.db.total_skill_advances += 1
        
        # Record in history
        import datetime
        self.caller.db.advancement_history.append({
            "type": "retrain_skill",
            "old_skill": old_skill,
            "new_skill": new_skill,
            "old_skill_change": f"{old_val} → {old_val - 1}",
            "new_skill_change": f"{new_val} → {new_val + 1}",
            "cost": cost,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.caller.msg(f"|gRetrained skills!|n")
        self.caller.msg(f"  {old_skill.capitalize()}: {old_val} → {old_val - 1}")
        self.caller.msg(f"  {new_skill.capitalize()}: {new_val} → {new_val + 1}")
        self.caller.msg(f"Cost: {cost} points (half of {full_cost}), Remaining: {self.caller.db.advancement_points} points")
    
    def _retrain_focus(self, old_focus, new_focus):
        """Retrain a focus (remove one, add another)"""
        current_focuses = self.caller.db.stats.get("focuses", [])
        
        # Check if old focus exists
        if old_focus not in current_focuses:
            self.caller.msg(f"|rYou don't have the focus: {old_focus}|n")
            return
        
        # Validate new focus
        from commands.dune.CmdSheet import CmdStats
        validator = CmdStats()
        validator.caller = self.caller
        if not validator._validate_focus(new_focus):
            self.caller.msg(f"|rInvalid focus: {new_focus}|n")
            self.caller.msg("Use |w+stats/focus list|n to see valid focuses.")
            return
        
        # Check for duplicates
        focus_lower = new_focus.lower()
        for existing_focus in current_focuses:
            if existing_focus.lower() == focus_lower:
                self.caller.msg(f"|rYou already have the focus: {existing_focus}|n")
                return
        
        # Calculate cost (half of normal, rounded up)
        focus_count = len(current_focuses)
        full_cost = focus_count
        cost = (full_cost + 1) // 2  # Round up
        
        # Check if enough points
        if self.caller.db.advancement_points < cost:
            self.caller.msg(f"|rNot enough advancement points.|n")
            self.caller.msg(f"Cost: {cost} points (half of {full_cost}), You have: {self.caller.db.advancement_points} points")
            return
        
        # Execute retrain
        self.caller.db.advancement_points -= cost
        self.caller.remove_focus(old_focus)
        self.caller.add_focus(new_focus)
        
        # Record in history
        import datetime
        self.caller.db.advancement_history.append({
            "type": "retrain_focus",
            "old_focus": old_focus,
            "new_focus": new_focus,
            "cost": cost,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.caller.msg(f"|gRetrained focus!|n")
        self.caller.msg(f"  Removed: {old_focus}")
        self.caller.msg(f"  Added: {new_focus}")
        self.caller.msg(f"Cost: {cost} points (half of {full_cost}), Remaining: {self.caller.db.advancement_points} points")
    
    def _retrain_talent(self, old_talent, new_talent):
        """Retrain a talent (remove one, add another)"""
        current_talents = self.caller.db.stats.get("talents", [])
        
        # Check if old talent exists
        if old_talent not in current_talents:
            self.caller.msg(f"|rYou don't have the talent: {old_talent}|n")
            return
        
        # Check for duplicates
        talent_lower = new_talent.lower()
        for existing_talent in current_talents:
            if existing_talent.lower() == talent_lower:
                self.caller.msg(f"|rYou already have the talent: {existing_talent}|n")
                return
        
        # Calculate cost (half of normal, rounded up)
        talent_count = len(current_talents)
        full_cost = 3 * talent_count
        cost = (full_cost + 1) // 2  # Round up
        
        # Check if enough points
        if self.caller.db.advancement_points < cost:
            self.caller.msg(f"|rNot enough advancement points.|n")
            self.caller.msg(f"Cost: {cost} points (half of {full_cost}), You have: {self.caller.db.advancement_points} points")
            return
        
        # Execute retrain
        self.caller.db.advancement_points -= cost
        self.caller.remove_talent(old_talent)
        self.caller.add_talent(new_talent)
        
        # Record in history
        import datetime
        self.caller.db.advancement_history.append({
            "type": "retrain_talent",
            "old_talent": old_talent,
            "new_talent": new_talent,
            "cost": cost,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self.caller.msg(f"|gRetrained talent!|n")
        self.caller.msg(f"  Removed: {old_talent}")
        self.caller.msg(f"  Added: {new_talent}")
        self.caller.msg(f"Cost: {cost} points (half of {full_cost}), Remaining: {self.caller.db.advancement_points} points")
    
    def _handle_history(self):
        """Show detailed advancement history"""
        history = self.caller.db.advancement_history
        
        if not history:
            self.caller.msg("You have no advancement history yet.")
            return
        
        lines = []
        lines.append("|w" + "=" * 78 + "|n")
        lines.append("|w" + f" ADVANCEMENT HISTORY - {self.caller.name}".center(78) + "|n")
        lines.append("|w" + "=" * 78 + "|n")
        
        for entry in history:
            entry_type = entry.get("type", "unknown")
            timestamp = entry.get("timestamp", "Unknown")
            cost = entry.get("cost", 0)
            
            if entry_type == "award":
                points = entry.get("points", 0)
                awarded_by = entry.get("awarded_by", "Unknown")
                lines.append(f"|y[{timestamp}]|n Awarded |g{points}|n points by {awarded_by}")
            
            elif entry_type == "skill":
                skill = entry.get("skill", "unknown")
                old_val = entry.get("old_value", 0)
                new_val = entry.get("new_value", 0)
                lines.append(f"|y[{timestamp}]|n Skill: {skill.capitalize()} {old_val} → {new_val} (|r-{cost}|n points)")
            
            elif entry_type == "focus":
                focus = entry.get("focus", "unknown")
                lines.append(f"|y[{timestamp}]|n Focus: {focus} (|r-{cost}|n points)")
            
            elif entry_type == "talent":
                talent = entry.get("talent", "unknown")
                lines.append(f"|y[{timestamp}]|n Talent: {talent} (|r-{cost}|n points)")
            
            elif entry_type == "asset":
                asset = entry.get("asset", "unknown")
                lines.append(f"|y[{timestamp}]|n Asset: {asset} (|r-{cost}|n points)")
            
            elif entry_type == "retrain_skill":
                old_skill = entry.get("old_skill", "unknown")
                new_skill = entry.get("new_skill", "unknown")
                old_change = entry.get("old_skill_change", "")
                new_change = entry.get("new_skill_change", "")
                lines.append(f"|y[{timestamp}]|n Retrain: {old_skill.capitalize()} {old_change}, "
                           f"{new_skill.capitalize()} {new_change} (|r-{cost}|n points)")
            
            elif entry_type == "retrain_focus":
                old_focus = entry.get("old_focus", "unknown")
                new_focus = entry.get("new_focus", "unknown")
                lines.append(f"|y[{timestamp}]|n Retrain Focus: {old_focus} → {new_focus} (|r-{cost}|n points)")
            
            elif entry_type == "retrain_talent":
                old_talent = entry.get("old_talent", "unknown")
                new_talent = entry.get("new_talent", "unknown")
                lines.append(f"|y[{timestamp}]|n Retrain Talent: {old_talent} → {new_talent} (|r-{cost}|n points)")
        
        lines.append("|w" + "=" * 78 + "|n")
        lines.append(f"|wCurrent Points:|n {self.caller.db.advancement_points}")
        lines.append("|w" + "=" * 78 + "|n")
        
        self.caller.msg("\n".join(lines))
    
    def _handle_reset(self):
        """Reset advancement tracking (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou don't have permission to reset advancement tracking.|n")
            return
        
        if not self.args:
            self.caller.msg("Usage: +advance/reset <character>")
            return
        
        target = self.caller.search(self.args.strip())
        if not target:
            return
        
        if not hasattr(target.db, 'stats'):
            self.caller.msg(f"{target.name} does not have stats initialized.")
            return
        
        # Reset tracking
        target.db.advancement_points = 0
        target.db.advancement_history = []
        target.db.skill_advances = {
            "battle": 0,
            "communicate": 0,
            "discipline": 0,
            "move": 0,
            "understand": 0
        }
        target.db.total_skill_advances = 0
        
        self.caller.msg(f"|gReset advancement tracking for {target.name}.|n")
        target.msg("|yYour advancement tracking has been reset by staff.|n")

