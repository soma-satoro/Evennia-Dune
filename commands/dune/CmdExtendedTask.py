"""
Extended Task Management Command for Dune 2d20 System

Manages extended tasks that require multiple skill tests to complete.
Extended tasks can be scene-based (stored on room) or character-based.
"""

from evennia.commands.default.muxcommand import MuxCommand


class CmdExtendedTask(MuxCommand):
    """
    Manage extended tasks that require multiple skill tests.
    
    Extended tasks represent activities that take ongoing effort over time.
    Each successful skill test scores points toward a requirement.
    
    Usage:
        +extend - View active extended tasks
        +extend/create <name>=<requirement> - Create an extended task (staff)
        +extend/create <name>=<requirement>/<max_attempts> - Create with max attempts (staff)
        +extend/contribute <name> - Mark next roll to contribute to this task
        +extend/complete <name> - Complete an extended task (staff)
        +extend/remove <name> - Remove an extended task (staff)
        +extend/clear - Clear all extended tasks (staff)
        
    Switches:
        /create - Create a new extended task (staff)
        /contribute - Mark next roll to contribute to a task
        /complete - Manually complete a task (staff)
        /remove - Remove a task (staff)
        /clear - Clear all tasks (staff)
        
    Extended Task Mechanics:
        - Each successful skill test scores 2 points (default)
        - Each complication reduces points by 1
        - Spending Momentum can increase points
        - Traits and assets (Quality 1+) can add points
        - Task completes when points >= requirement
        
    Examples:
        +extend - View all active tasks
        +extend/create "Repair Reputation"=5 - Create task requiring 5 points
        +extend/create "Fix Engine"=8/3 - Create task with 8 requirement, 3 max attempts
        +extend/contribute "Repair Reputation" - Next roll contributes to this task
        +extend/complete "Repair Reputation" - Complete task (staff)
    """
    
    key = "+extend"
    aliases = ["extendedtask", "extask", "etask"]
    help_category = "Dice"
    
    def func(self):
        """Manage extended tasks"""
        
        # Get room for scene-based tasks
        room = self.caller.location if self.caller.location else None
        
        # Initialize extended tasks storage
        if room:
            if not hasattr(room.db, 'extended_tasks'):
                room.db.extended_tasks = {}
        
        # No switches - show active tasks
        if not self.switches:
            self._show_tasks(room)
            return
        
        # Create extended task (staff)
        if "create" in self.switches:
            self._create_task(room)
            return
        
        # Contribute to task
        if "contribute" in self.switches:
            self._set_contribution(room)
            return
        
        # Complete task (staff)
        if "complete" in self.switches:
            self._complete_task(room)
            return
        
        # Remove task (staff)
        if "remove" in self.switches or "rem" in self.switches:
            self._remove_task(room)
            return
        
        # Clear all tasks (staff)
        if "clear" in self.switches:
            self._clear_tasks(room)
            return
    
    def _show_tasks(self, room):
        """Show all active extended tasks"""
        if not room or not hasattr(room.db, 'extended_tasks') or not room.db.extended_tasks:
            self.caller.msg("|yNo active extended tasks.|n")
            return
        
        tasks = room.db.extended_tasks
        output = []
        output.append("|w" + "=" * 78 + "|n")
        output.append("|w" + " ACTIVE EXTENDED TASKS".center(78) + "|n")
        output.append("|w" + "=" * 78 + "|n")
        
        for task_name, task_data in tasks.items():
            points = task_data.get("points", 0)
            requirement = task_data.get("requirement", 0)
            max_attempts = task_data.get("max_attempts", None)
            attempts = task_data.get("attempts", 0)
            contributing = task_data.get("contributing", [])
            
            progress = f"{points}/{requirement}"
            if max_attempts:
                progress += f" (Attempts: {attempts}/{max_attempts})"
            
            output.append(f"|y{task_name}:|n {progress}")
            
            if contributing:
                contrib_list = ", ".join([c.name for c in contributing if hasattr(c, 'name')])
                output.append(f"  |cContributing:|n {contrib_list}")
        
        output.append("|w" + "=" * 78 + "|n")
        output.append("|cUse +extendedtask/contribute <name> to mark your next roll for a task.|n")
        
        self.caller.msg("\n".join(output))
    
    def _create_task(self, room):
        """Create a new extended task (staff)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can create extended tasks.|n")
            return
        
        if not room:
            self.caller.msg("|rYou must be in a room to create an extended task.|n")
            return
        
        if "=" not in self.args:
            self.caller.msg("Usage: +extendedtask/create <name>=<requirement>[/<max_attempts>]")
            self.caller.msg("Example: +extendedtask/create 'Repair Reputation'=5")
            self.caller.msg("Example: +extendedtask/create 'Fix Engine'=8/3")
            return
        
        parts = self.args.split("=", 1)
        task_name = parts[0].strip()
        requirement_part = parts[1].strip()
        
        # Parse requirement and optional max_attempts
        if "/" in requirement_part:
            req_parts = requirement_part.split("/")
            try:
                requirement = int(req_parts[0])
                max_attempts = int(req_parts[1])
            except (ValueError, IndexError):
                self.caller.msg("|rInvalid format. Use: <requirement>[/<max_attempts>]|n")
                return
        else:
            try:
                requirement = int(requirement_part)
                max_attempts = None
            except ValueError:
                self.caller.msg("|rRequirement must be a number.|n")
                return
        
        if not hasattr(room.db, 'extended_tasks'):
            room.db.extended_tasks = {}
        
        # Create task
        room.db.extended_tasks[task_name] = {
            "requirement": requirement,
            "points": 0,
            "max_attempts": max_attempts,
            "attempts": 0,
            "contributing": []  # Characters who will contribute on next roll
        }
        
        max_attempts_str = f" (Max {max_attempts} attempts)" if max_attempts else ""
        self.caller.msg(f"|gCreated extended task '{task_name}' with requirement {requirement}{max_attempts_str}.|n")
        
        if room:
            room.msg_contents(
                f"|y{self.caller.name} creates an extended task: {task_name} (Requirement: {requirement}{max_attempts_str})|n",
                exclude=self.caller
            )
    
    def _set_contribution(self, room):
        """Mark next roll to contribute to a task"""
        if not self.args:
            self.caller.msg("Usage: +extendedtask/contribute <task name>")
            return
        
        if not room or not hasattr(room.db, 'extended_tasks') or not room.db.extended_tasks:
            self.caller.msg("|rNo active extended tasks.|n")
            return
        
        task_name = self.args.strip()
        tasks = room.db.extended_tasks
        
        if task_name not in tasks:
            self.caller.msg(f"|rExtended task '{task_name}' not found.|n")
            self.caller.msg(f"|yActive tasks: {', '.join(tasks.keys())}|n")
            return
        
        task_data = tasks[task_name]
        contributing = task_data.get("contributing", [])
        
        # Add caller to contributing list if not already there
        if self.caller not in contributing:
            contributing.append(self.caller)
            task_data["contributing"] = contributing
        
        self.caller.msg(f"|gYour next roll will contribute to '{task_name}'.|n")
        self.caller.msg(f"|yCurrent progress: {task_data.get('points', 0)}/{task_data.get('requirement', 0)}|n")
    
    def _complete_task(self, room):
        """Manually complete a task (staff)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can complete extended tasks.|n")
            return
        
        if not self.args:
            self.caller.msg("Usage: +extendedtask/complete <task name>")
            return
        
        if not room or not hasattr(room.db, 'extended_tasks') or not room.db.extended_tasks:
            self.caller.msg("|rNo active extended tasks.|n")
            return
        
        task_name = self.args.strip()
        tasks = room.db.extended_tasks
        
        if task_name not in tasks:
            self.caller.msg(f"|rExtended task '{task_name}' not found.|n")
            return
        
        del tasks[task_name]
        self.caller.msg(f"|gCompleted and removed extended task '{task_name}'.|n")
        
        if room:
            room.msg_contents(
                f"|yExtended task '{task_name}' has been completed.|n",
                exclude=self.caller
            )
    
    def _remove_task(self, room):
        """Remove a task (staff)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can remove extended tasks.|n")
            return
        
        if not self.args:
            self.caller.msg("Usage: +extendedtask/remove <task name>")
            return
        
        if not room or not hasattr(room.db, 'extended_tasks') or not room.db.extended_tasks:
            self.caller.msg("|rNo active extended tasks.|n")
            return
        
        task_name = self.args.strip()
        tasks = room.db.extended_tasks
        
        if task_name not in tasks:
            self.caller.msg(f"|rExtended task '{task_name}' not found.|n")
            return
        
        del tasks[task_name]
        self.caller.msg(f"|gRemoved extended task '{task_name}'.|n")
    
    def _clear_tasks(self, room):
        """Clear all extended tasks (staff)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rOnly staff can clear extended tasks.|n")
            return
        
        if not room:
            self.caller.msg("|rYou must be in a room to clear extended tasks.|n")
            return
        
        if hasattr(room.db, 'extended_tasks'):
            count = len(room.db.extended_tasks)
            room.db.extended_tasks = {}
            self.caller.msg(f"|gCleared {count} extended task(s).|n")
        else:
            self.caller.msg("|yNo extended tasks to clear.|n")

