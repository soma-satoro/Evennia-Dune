"""
Inventory Command

Displays a character's assets (inventory) organized by asset type.
"""

from evennia.commands.default.muxcommand import MuxCommand


class CmdInventory(MuxCommand):
    """
    View your inventory of assets.
    
    Usage:
        +inventory | +inv
        +inventory <asset type> | +inv <asset type>
        +inventory/detail <asset name> | +inv/detail <asset name>
    
    Switches:
        /detail - Show detailed information about a specific asset
    
    Asset Types:
        Personal - Items carried by individual characters
        Warfare - Large items (heavy ordnance, soldiers, vehicles)
        Espionage - Items for assassination, stealth, information gathering
        Intrigue - Social assets (favors, debts, reputation)
    
    Examples:
        +inv - Show all assets organized by type
        +inv Personal - Show only Personal assets
        +inv/detail Lasgun - Show detailed information about a Lasgun
    """
    
    key = "+inventory"
    aliases = ["+inv", "inventory", "inv"]
    help_category = "Character"
    
    def func(self):
        """Display inventory"""
        
        target = self.caller
        
        # Check if viewing another character's inventory (staff only)
        if self.args and "detail" not in self.switches:
            # Check if args is an asset type first
            valid_types = ["Personal", "Warfare", "Espionage", "Intrigue"]
            if self.args.strip() not in valid_types:
                # Might be a character name - check permissions
                if self.caller.check_permstring("Builder"):
                    target = self.caller.search(self.args.strip())
                    if not target:
                        return
                else:
                    self.caller.msg("|rYou don't have permission to view other characters' inventories.|n")
                    return
        
        # Handle /detail switch
        if "detail" in self.switches:
            if not self.args:
                self.caller.msg("Usage: +inventory/detail <asset name>")
                return
            
            asset_name = self.args.strip()
            asset = self._find_asset_in_inventory(target, asset_name)
            
            if not asset:
                self.caller.msg(f"|rYou don't have an asset named '{asset_name}'.|n")
                return
            
            # Show detailed information
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg(asset.get_detailed_display())
            self.caller.msg("|w" + "=" * 80 + "|n")
            return
        
        # Get all assets from inventory
        assets = self._get_assets_from_inventory(target)
        
        if not assets:
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|w" + f" {target.name.upper()}'S INVENTORY".center(80) + "|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            self.caller.msg("|yYou have no assets in your inventory.|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            return
        
        # Filter by asset type if specified
        filter_type = None
        if self.args and self.args.strip() in ["Personal", "Warfare", "Espionage", "Intrigue"]:
            filter_type = self.args.strip()
        
        # Organize assets by type
        assets_by_type = {
            "Personal": [],
            "Warfare": [],
            "Espionage": [],
            "Intrigue": []
        }
        
        for asset in assets:
            asset_type = asset.get_asset_type()
            if asset_type in assets_by_type:
                assets_by_type[asset_type].append(asset)
        
        # Display inventory
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg("|w" + f" {target.name.upper()}'S INVENTORY".center(80) + "|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        displayed_any = False
        
        for asset_type in ["Personal", "Warfare", "Espionage", "Intrigue"]:
            type_assets = assets_by_type[asset_type]
            
            # Skip if filtering and this isn't the requested type
            if filter_type and asset_type != filter_type:
                continue
            
            # Skip if no assets of this type
            if not type_assets:
                continue
            
            displayed_any = True
            self.caller.msg(f"\n|y{asset_type} Assets:|n")
            
            for asset in sorted(type_assets, key=lambda x: x.name):
                quality = asset.get_quality()
                keywords = asset.get_keywords()
                
                # Build display line
                line = f"  • |w{asset.name}|n"
                
                if quality and quality != 0:
                    if quality == "Special":
                        line += " |c[Special]|n"
                    else:
                        line += f" |c[Q{quality}]|n"
                
                if keywords:
                    line += f" |m({', '.join(keywords)})|n"
                
                self.caller.msg(line)
        
        if not displayed_any:
            if filter_type:
                self.caller.msg(f"|yYou have no {filter_type} assets.|n")
            else:
                self.caller.msg("|yYou have no assets.|n")
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg("|cUse |w+inv/detail <asset name>|c to see detailed information about an asset.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _get_assets_from_inventory(self, character):
        """
        Get all Asset objects from a character's inventory.
        
        Args:
            character: The character to get assets from
            
        Returns:
            list: List of Asset objects
        """
        assets = []
        
        # Get all objects in the character's inventory (contents)
        for obj in character.contents:
            # Check if it's an Asset typeclass
            if obj.is_typeclass("typeclasses.assets.Asset", exact=False):
                assets.append(obj)
        
        return assets
    
    def _find_asset_in_inventory(self, character, asset_name):
        """
        Find a specific asset in a character's inventory by name.
        
        Args:
            character: The character to search
            asset_name: Name of the asset to find
            
        Returns:
            Asset or None: The asset if found, None otherwise
        """
        assets = self._get_assets_from_inventory(character)
        
        # Search by name (case-insensitive, partial match)
        asset_name_lower = asset_name.lower()
        for asset in assets:
            if asset_name_lower in asset.name.lower():
                return asset
        
        return None

