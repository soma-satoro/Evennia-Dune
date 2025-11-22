"""
Pool Management Command for Dune 2d20 System

Manages character resource pools like Determination, and can be extended
for other pools as the ruleset expands.
"""

from evennia.commands.default.muxcommand import MuxCommand


# Define available pools and their properties
POOLS = {
    "determination": {
        "name": "Determination",
        "default": 3,
        "max": None,  # No maximum (or set based on character advancement)
        "description": "Hero points for special actions. Can be spent to set a die to 1 before rolling, or re-roll after rolling."
    },
    "momentum": {
        "name": "Momentum",
        "default": 0,
        "max": 6,  # Up to 6 points can be saved in the group pool
        "description": "Group resource generated from extra successes. Can be spent to buy dice, create traits/assets, or obtain information."
    },
    # Future pools can be added here:
    # "threat": {
    #     "name": "Threat",
    #     "default": 0,
    #     "max": None,
    #     "description": "GM resource pool"
    # },
}


class CmdPool(MuxCommand):
    """
    Manage character resource pools (Determination, etc.)
    
    Usage:
        +pool - View all pools
        +pool <pool> - View specific pool
        +pool/<pool>/spend [<amount>] - Spend pool points
        +pool/<pool>/gain [<amount>] - Gain pool points
        +pool/<pool>/set <amount> - Set pool value (staff only)
        +pool/<pool>/add <character>=<amount> - Award pool points to character (staff)
        
    Switches:
        /spend - Spend pool points
        /gain - Gain pool points
        /set - Set pool value directly (staff only)
        /add - Award pool points to another character (staff)
        
    Available Pools:
        determination - Hero points for special actions
        momentum - Group resource from extra successes (max 6)
        
    Examples:
        +pool - View all pools
        +pool determination - View determination
        +pool momentum - View momentum pool
        +pool/determination/spend - Spend 1 determination
        +pool/momentum/spend 2 - Spend 2 momentum
        +pool/momentum/gain 1 - Gain 1 momentum
        +pool/determination/set 5 - Set determination to 5 (staff)
        +pool/momentum/add Paul=1 - Award Paul 1 momentum (staff)
    """
    
    key = "+pool"
    aliases = ["pool", "pools"]
    help_category = "Character"
    
    def func(self):
        """Manage pools"""
        
        # Parse pool name and action
        pool_name = None
        action = None
        
        # Check if pool name is in switches (e.g., /determination/spend)
        for switch in self.switches:
            if switch in POOLS:
                pool_name = switch
                # Check for action in remaining switches
                for other_switch in self.switches:
                    if other_switch in ["spend", "gain", "set", "add"]:
                        action = other_switch
                break
        
        # If no pool in switches, check args
        if not pool_name:
            if self.args:
                # Try to get pool name from args
                args_parts = self.args.split()
                potential_pool = args_parts[0].lower()
                if potential_pool in POOLS:
                    pool_name = potential_pool
                    # Check if there's an action in switches
                    for switch in self.switches:
                        if switch in ["spend", "gain", "set", "add"]:
                            action = switch
            else:
                # No args and no pool in switches
                # Check if action is in switches but no pool specified
                for switch in self.switches:
                    if switch in ["spend", "gain", "set", "add"]:
                        self.caller.msg("|rPlease specify a pool name.|n")
                        self.caller.msg("Available pools: " + ", ".join(POOLS.keys()))
                        return
        
        # If still no pool, show all pools
        if not pool_name:
            self._show_all_pools()
            return
        
        # Validate pool exists
        if pool_name not in POOLS:
            self.caller.msg(f"|rUnknown pool: {pool_name}|n")
            self.caller.msg("Available pools: " + ", ".join(POOLS.keys()))
            return
        
        pool_info = POOLS[pool_name]
        
        # Initialize pool if it doesn't exist
        pool_attr = f"db.{pool_name}"
        if not hasattr(self.caller.db, pool_name):
            setattr(self.caller.db, pool_name, pool_info["default"])
        
        # No action - show pool status
        if not action:
            self._show_pool(pool_name, pool_info)
            return
        
        # Handle actions
        if action == "spend":
            self._spend_pool(pool_name, pool_info)
        elif action == "gain":
            self._gain_pool(pool_name, pool_info)
        elif action == "set":
            self._set_pool(pool_name, pool_info)
        elif action == "add":
            self._add_pool(pool_name, pool_info)
        else:
            self.caller.msg(f"|rUnknown action: {action}|n")
    
    def _show_all_pools(self):
        """Show all pools"""
        output = []
        output.append("|w" + "=" * 78 + "|n")
        output.append("|w" + " CHARACTER POOLS".center(78) + "|n")
        output.append("|w" + "=" * 78 + "|n")
        
        for pool_name, pool_info in POOLS.items():
            current = getattr(self.caller.db, pool_name, pool_info["default"])
            max_val = pool_info.get("max")
            
            if max_val:
                display = f"{pool_info['name']}: |c{current}/{max_val}|n"
            else:
                display = f"{pool_info['name']}: |c{current}|n"
            
            output.append(f"  {display}")
            if pool_info.get("description"):
                output.append(f"    |y{pool_info['description']}|n")
        
        output.append("|w" + "=" * 78 + "|n")
        output.append("|cUse +pool <pool> to view details, or +pool/<pool>/spend to spend points.|n")
        
        self.caller.msg("\n".join(output))
    
    def _show_pool(self, pool_name, pool_info):
        """Show specific pool status"""
        current = getattr(self.caller.db, pool_name, pool_info["default"])
        max_val = pool_info.get("max")
        
        output = []
        output.append("|w" + "=" * 78 + "|n")
        output.append(f"|w{pool_info['name']}|n")
        output.append("|w" + "-" * 78 + "|n")
        
        if max_val:
            output.append(f"Current: |c{current}/{max_val}|n")
        else:
            output.append(f"Current: |c{current}|n")
        
        if pool_info.get("description"):
            output.append(f"\n{pool_info['description']}")
        
        output.append("|w" + "=" * 78 + "|n")
        output.append("|cUsage:|n +pool/{}/spend [amount] | +pool/{}/gain [amount]".format(pool_name, pool_name))
        
        self.caller.msg("\n".join(output))
    
    def _spend_pool(self, pool_name, pool_info):
        """Spend pool points"""
        amount = 1  # Default
        
        # Parse amount from args
        if self.args:
            args_parts = self.args.split()
            # If first arg is pool name, skip it
            if args_parts[0].lower() == pool_name:
                if len(args_parts) > 1:
                    try:
                        amount = int(args_parts[1])
                    except (ValueError, IndexError):
                        amount = 1
            else:
                # First arg might be the amount
                try:
                    amount = int(args_parts[0])
                except (ValueError, IndexError):
                    amount = 1
        
        current = getattr(self.caller.db, pool_name, pool_info["default"])
        
        if current < amount:
            self.caller.msg(f"|rYou don't have enough {pool_info['name']}. You have {current}, need {amount}.|n")
            return
        
        new_value = current - amount
        setattr(self.caller.db, pool_name, new_value)
        
        self.caller.msg(f"|gSpent {amount} {pool_info['name']}. Remaining: {new_value}|n")
        
        # Special handling for determination
        if pool_name == "determination":
            if self.caller.location:
                self.caller.location.msg_contents(
                    f"|c{self.caller.name} spends Determination for a heroic action!|n",
                    exclude=self.caller
                )
    
    def _gain_pool(self, pool_name, pool_info):
        """Gain pool points"""
        amount = 1  # Default
        
        # Parse amount from args
        if self.args:
            args_parts = self.args.split()
            # If first arg is pool name, skip it
            if args_parts[0].lower() == pool_name:
                if len(args_parts) > 1:
                    try:
                        amount = int(args_parts[1])
                    except (ValueError, IndexError):
                        amount = 1
            else:
                # First arg might be the amount
                try:
                    amount = int(args_parts[0])
                except (ValueError, IndexError):
                    amount = 1
        
        current = getattr(self.caller.db, pool_name, pool_info["default"])
        max_val = pool_info.get("max")
        
        new_value = current + amount
        if max_val and new_value > max_val:
            new_value = max_val
            self.caller.msg(f"|yGained {amount} {pool_info['name']}, but capped at maximum {max_val}.|n")
        else:
            self.caller.msg(f"|gGained {amount} {pool_info['name']}. New total: {new_value}|n")
        
        setattr(self.caller.db, pool_name, new_value)
    
    def _set_pool(self, pool_name, pool_info):
        """Set pool value (staff only)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou don't have permission to set pool values.|n")
            return
        
        if not self.args:
            self.caller.msg(f"Usage: +pool/{pool_name}/set <amount>")
            return
        
        args_parts = self.args.split()
        try:
            amount = int(args_parts[-1])  # Take last arg as amount
        except (ValueError, IndexError):
            self.caller.msg("Amount must be a number.")
            return
        
        max_val = pool_info.get("max")
        if max_val and amount > max_val:
            amount = max_val
            self.caller.msg(f"|yCapped at maximum {max_val}.|n")
        
        setattr(self.caller.db, pool_name, amount)
        self.caller.msg(f"Set {pool_info['name']} to {amount}.")
    
    def _add_pool(self, pool_name, pool_info):
        """Award pool points to another character (staff)"""
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou don't have permission to award pool points.|n")
            return
        
        if "=" not in self.args:
            self.caller.msg(f"Usage: +pool/{pool_name}/add <character>=<amount>")
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
        
        # Initialize pool if needed
        if not hasattr(target.db, pool_name):
            setattr(target.db, pool_name, pool_info["default"])
        
        current = getattr(target.db, pool_name, pool_info["default"])
        max_val = pool_info.get("max")
        
        new_value = current + amount
        if max_val and new_value > max_val:
            new_value = max_val
            self.caller.msg(f"|yAwarded {amount} {pool_info['name']} to {target.name}, but capped at maximum {max_val}.|n")
        else:
            self.caller.msg(f"|gAwarded {amount} {pool_info['name']} to {target.name}. Their total: {new_value}|n")
        
        setattr(target.db, pool_name, new_value)
        target.msg(f"|gYou have been awarded {amount} {pool_info['name']}!|n")

