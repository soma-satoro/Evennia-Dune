"""
Asset Creation Command

Command to create and manage assets for characters.
"""

from evennia.commands.default.muxcommand import MuxCommand
from typeclasses.personal_assets import PERSONAL_ASSETS, create_personal_asset, get_all_personal_asset_names
from typeclasses.warfare_assets import WARFARE_ASSETS, create_warfare_asset, get_all_warfare_asset_names
from typeclasses.espionage_assets import ESPIONAGE_ASSETS, create_espionage_asset, get_all_espionage_asset_names
from typeclasses.intrigue_assets import INTRIGUE_ASSETS, create_intrigue_asset, get_all_intrigue_asset_names


# Combined asset dictionaries for lookup
ALL_ASSETS = {**PERSONAL_ASSETS, **WARFARE_ASSETS, **ESPIONAGE_ASSETS, **INTRIGUE_ASSETS}


class CmdAsset(MuxCommand):
    """
    Create and manage assets.
    
    Usage:
        +asset/create <asset name> - Create an Asset
        +asset/list [Personal|Warfare|Espionage|Intrigue] - List all available Assets (optionally filtered by type)
        +asset/info <asset name> - Show information about an asset
        +asset/quality <asset name>=<quality> - Set quality of an asset in your inventory
        +asset/quality <character>/<asset name>=<quality> - Set quality of another's asset (staff only)
    
    Switches:
        /create - Create an asset and add it to your inventory
        /list - List all available Assets (optionally filter by type)
        /info - Show detailed information about an asset
        /quality - Set quality of an asset (0-5, or "Special")
    
    Examples:
        +asset/create Lasgun - Create a Lasgun and add it to inventory
        +asset/list - See all available Assets
        +asset/list Personal - See only Personal Assets
        +asset/list Warfare - See only Warfare Assets
        +asset/info Crysknife - See details about Crysknife
        +asset/info Strategic/House Shield - See details about Strategic/House Shield
        +asset/quality Lasgun=3 - Set Lasgun quality to 3
        +asset/quality Ridulian Crystal=Special - Set Ridulian Crystal quality to Special
        +asset/quality Paul/Lasgun=4 - Set Paul's Lasgun quality to 4 (staff only)
    """
    
    key = "+asset"
    aliases = ["asset"]
    help_category = "Character"
    
    def func(self):
        """Handle asset commands"""
        
        if not self.args and "list" not in self.switches:
            self.caller.msg("Usage: +asset/create <asset name> | +asset/list [Personal|Warfare|Espionage|Intrigue] | +asset/info <asset name> | +asset/quality <asset name>=<quality>")
            return
        
        # List available assets
        if "list" in self.switches or (not self.switches and not self.args):
            filter_type = None
            if self.args:
                if self.args.strip() in ["Personal", "Warfare", "Espionage", "Intrigue"]:
                    filter_type = self.args.strip()
            self._list_assets(filter_type)
            return
        
        # Set asset quality
        if "quality" in self.switches:
            self._set_asset_quality()
            return
        
        # Show asset info
        if "info" in self.switches:
            self._show_asset_info()
            return
        
        # Create asset
        if "create" in self.switches:
            self._create_asset()
            return
        
        # Default: try to create if no switch
        if not self.switches:
            self._create_asset()
    
    def _list_assets(self, filter_type=None):
        """List all available Assets, optionally filtered by type"""
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        
        # If showing both types, organize by type
        if not filter_type:
            self.caller.msg("|w" + " AVAILABLE ASSETS".center(80) + "|n")
            self.caller.msg("|w" + "=" * 80 + "|n")
            # Personal Assets
            self.caller.msg("\n|y" + "PERSONAL ASSETS".center(80) + "|n")
            self._list_asset_category(PERSONAL_ASSETS, get_all_personal_asset_names(), use_categories=True)
            
            # Warfare Assets
            self.caller.msg("\n|y" + "WARFARE ASSETS".center(80) + "|n")
            self._list_asset_category(WARFARE_ASSETS, get_all_warfare_asset_names(), use_categories=True)
            
            # Espionage Assets
            self.caller.msg("\n|y" + "ESPIONAGE ASSETS".center(80) + "|n")
            self._list_asset_category(ESPIONAGE_ASSETS, get_all_espionage_asset_names(), use_categories=True)
            
            # Intrigue Assets
            self.caller.msg("\n|y" + "INTRIGUE ASSETS".center(80) + "|n")
            self._list_asset_category(INTRIGUE_ASSETS, get_all_intrigue_asset_names(), use_categories=True)
        else:
            # Single type, use category grouping
            if filter_type == "Personal":
                self.caller.msg("|w" + " PERSONAL ASSETS".center(80) + "|n")
                self.caller.msg("|w" + "=" * 80 + "|n")
                self._list_asset_category(PERSONAL_ASSETS, get_all_personal_asset_names(), use_categories=True)
            elif filter_type == "Warfare":
                self.caller.msg("|w" + " WARFARE ASSETS".center(80) + "|n")
                self.caller.msg("|w" + "=" * 80 + "|n")
                self._list_asset_category(WARFARE_ASSETS, get_all_warfare_asset_names(), use_categories=True)
            elif filter_type == "Espionage":
                self.caller.msg("|w" + " ESPIONAGE ASSETS".center(80) + "|n")
                self.caller.msg("|w" + "=" * 80 + "|n")
                self._list_asset_category(ESPIONAGE_ASSETS, get_all_espionage_asset_names(), use_categories=True)
            elif filter_type == "Intrigue":
                self.caller.msg("|w" + " INTRIGUE ASSETS".center(80) + "|n")
                self.caller.msg("|w" + "=" * 80 + "|n")
                self._list_asset_category(INTRIGUE_ASSETS, get_all_intrigue_asset_names(), use_categories=True)
        
        self.caller.msg("\n|w" + "=" * 80 + "|n")
        self.caller.msg("|cUse |w+asset/create <name>|c to create an asset and add it to your inventory.|n")
        self.caller.msg("|cUse |w+asset/info <name>|c to see detailed information about an asset.|n")
        if not filter_type:
            self.caller.msg("|cUse |w+asset/list Personal|n, |w+asset/list Warfare|n, |w+asset/list Espionage|n, or |w+asset/list Intrigue|n to filter by type.|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _list_asset_category(self, asset_dict, asset_names, use_categories=False):
        """List assets in a category, optionally grouped by subcategory"""
        
        if use_categories and asset_dict == PERSONAL_ASSETS:
            # Personal Assets grouped by category
            categories = {
                "Ranged Weapons": ["Lasgun", "Maula Pistol"],
                "Melee Weapons": ["Blade", "Bodkin", "Crysknife", "Kindjal", "Pulse-Sword"],
                "Armor and Dress": ["Jubba Cloak", "Shield", "Personal Shield", "Semi Shield", "Stillsuit"],
                "Communication": ["Communinet", "Ixian Damper", "Emergency Transmitter", "Filmbook", "Memocorder", "Ridulian Crystal"],
                "Tools and Equipment": ["Baradye Pistol", "Cibus Hood", "Dew Collector", "Fremkit", "Glowglobe", "Krimskel Fiber Rope", "Maker Hooks", "Palm Lock", "Paracompass", "Poison Snooper", "Ixian Probe", "Sapho", "Stilltent", "Personal Suspensor", "Thumper"]
            }
            
            for category, items in categories.items():
                matching = [name for name in asset_names if name in items]
                if matching:
                    self.caller.msg(f"\n|y{category}:|n")
                    for name in sorted(matching):
                        asset_data = asset_dict[name]
                        keywords = ", ".join(asset_data["keywords"])
                        quality = asset_data["quality"]
                        quality_str = f" [Q{quality}]" if quality and quality != 0 else ""
                        if quality == "Special":
                            quality_str = " [Special]"
                        self.caller.msg(f"  • |w{name}|n{quality_str} |m({keywords})|n")
        elif use_categories and asset_dict == WARFARE_ASSETS:
            # Warfare Assets grouped by category
            categories = {
                "Shields & Emplacements": ["Strategic/House Shield", "Fortress", "Bunker"],
                "Soldiers": ["Conscript", "Shield Infantry"],
                "Transports": ["Personnel Carrier", "Anti-Grav Platform", "Naval Transport", "Ornithopter - Scout", "Ornithopter - Troop Transport", "Ornithopter - Supply Carrier", "Ornithopter - Attack/Arrakis", "Carryall"],
                "Artillery & Anti-Aircraft": ["Artillery", "RPG", "MPAD", "Mortar", "Rocket Launcher", "Missile Launcher"],
                "Other Vehicles": ["Spice Harvester", "Orbital Transport", "Heighliner"]
            }
            
            for category, items in categories.items():
                matching = [name for name in asset_names if name in items]
                if matching:
                    self.caller.msg(f"\n|y{category}:|n")
                    for name in sorted(matching):
                        asset_data = asset_dict[name]
                        keywords = ", ".join(asset_data["keywords"])
                        quality = asset_data["quality"]
                        quality_str = f" [Q{quality}]" if quality and quality != 0 else ""
                        if quality == "Special":
                            quality_str = " [Special]"
                        self.caller.msg(f"  • |w{name}|n{quality_str} |m({keywords})|n")
        elif use_categories and asset_dict == ESPIONAGE_ASSETS:
            # Espionage Assets grouped by category
            categories = {
                "Weapons": ["Shigawire Garrote", "Slip-Tip"],
                "Drugs": ["Chaumas and Chaumurky", "Elacca", "Residual Poison", "Semuta", "Shere", "Truthsayer Drug", "Verite"],
                "Communication & Information": ["Distrans", "Intelligence", "Interrogation", "Map", "Shigawire"],
                "Contacts and Agents": ["Assassin", "Corporate Spy", "Face Dancer", "Mentat Master of Assassins", "Political Spy"]
            }
            
            for category, items in categories.items():
                matching = [name for name in asset_names if name in items]
                if matching:
                    self.caller.msg(f"\n|y{category}:|n")
                    for name in sorted(matching):
                        asset_data = asset_dict[name]
                        keywords = ", ".join(asset_data["keywords"])
                        quality = asset_data["quality"]
                        quality_str = f" [Q{quality}]" if quality and quality != 0 else ""
                        if quality == "Special":
                            quality_str = " [Special]"
                        self.caller.msg(f"  • |w{name}|n{quality_str} |m({keywords})|n")
        elif use_categories and asset_dict == INTRIGUE_ASSETS:
            # Intrigue Assets grouped by category
            categories = {
                "Favors": ["Debtor", "Old Friendship", "Service"],
                "Valuables": ["Land Rights", "Manufactured Goods", "Raw Materials", "Supply Contract", "Valuable Item"],
                "Blackmail": ["Hostage", "Illicit Recording", "Stolen File"],
                "Contacts": ["Black Market Trader", "Courtesan", "Ex-Agent"],
                "Courtiers": ["Ambitious Newcomer", "Confidant of the Emperor", "House Retainer", "Indebted Landowner", "Politician"]
            }
            
            for category, items in categories.items():
                matching = [name for name in asset_names if name in items]
                if matching:
                    self.caller.msg(f"\n|y{category}:|n")
                    for name in sorted(matching):
                        asset_data = asset_dict[name]
                        keywords = ", ".join(asset_data["keywords"])
                        quality = asset_data["quality"]
                        quality_str = f" [Q{quality}]" if quality and quality != 0 else ""
                        if quality == "Special":
                            quality_str = " [Special]"
                        self.caller.msg(f"  • |w{name}|n{quality_str} |m({keywords})|n")
        else:
            # Simple list
            for name in sorted(asset_names):
                asset_data = asset_dict[name]
                keywords = ", ".join(asset_data["keywords"])
                quality = asset_data["quality"]
                quality_str = f" [Q{quality}]" if quality and quality != 0 else ""
                if quality == "Special":
                    quality_str = " [Special]"
                self.caller.msg(f"  • |w{name}|n{quality_str} |m({keywords})|n")
    
    def _show_asset_info(self):
        """Show detailed information about an asset"""
        if not self.args:
            self.caller.msg("Usage: +asset/info <asset name>")
            return
        
        asset_name = self.args.strip()
        
        # Try to find exact match first
        if asset_name not in ALL_ASSETS:
            # Try case-insensitive search
            found = None
            for name in ALL_ASSETS.keys():
                if name.lower() == asset_name.lower():
                    found = name
                    break
            
            if not found:
                self.caller.msg(f"|rUnknown asset: {asset_name}|n")
                self.caller.msg("Use |w+asset/list|n to see available assets.")
                return
            
            asset_name = found
        
        asset_data = ALL_ASSETS[asset_name]
        
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg(f"|w{asset_name}|n")
        self.caller.msg("|w" + "=" * 80 + "|n")
        self.caller.msg(f"|yType:|n {asset_data['asset_type']}")
        
        quality = asset_data["quality"]
        if quality:
            if quality == "Special":
                self.caller.msg(f"|yQuality:|n Special")
            else:
                self.caller.msg(f"|yQuality:|n {quality}")
        
        if asset_data["keywords"]:
            self.caller.msg(f"|yKeywords:|n {', '.join(asset_data['keywords'])}")
        
        self.caller.msg(f"\n|yDescription:|n {asset_data['description']}")
        
        if asset_data["special"]:
            self.caller.msg(f"\n|ySpecial:|n {asset_data['special']}")
        
        self.caller.msg("|w" + "=" * 80 + "|n")
    
    def _create_asset(self):
        """Create an asset and add it to inventory"""
        if not self.args:
            self.caller.msg("Usage: +asset/create <asset name>")
            self.caller.msg("Use |w+asset/list|n to see available assets.")
            return
        
        asset_name = self.args.strip()
        
        # Try to find exact match first
        if asset_name not in ALL_ASSETS:
            # Try case-insensitive search
            found = None
            for name in ALL_ASSETS.keys():
                if name.lower() == asset_name.lower():
                    found = name
                    break
            
            if not found:
                self.caller.msg(f"|rUnknown asset: {asset_name}|n")
                self.caller.msg("Use |w+asset/list|n to see available assets.")
                return
            
            asset_name = found
        
        # Check if character already has this asset
        existing = self.caller.has_asset(asset_name)
        if existing:
            self.caller.msg(f"|yYou already have a {asset_name} in your inventory.|n")
            return
        
        # Create the asset based on type
        asset = None
        if asset_name in PERSONAL_ASSETS:
            asset = create_personal_asset(asset_name, character=self.caller)
        elif asset_name in WARFARE_ASSETS:
            asset = create_warfare_asset(asset_name, character=self.caller)
        elif asset_name in ESPIONAGE_ASSETS:
            asset = create_espionage_asset(asset_name, character=self.caller)
        elif asset_name in INTRIGUE_ASSETS:
            asset = create_intrigue_asset(asset_name, character=self.caller)
        
        if asset:
            self.caller.msg(f"|gCreated {asset_name} and added it to your inventory.|n")
            self.caller.msg(f"Use |w+inv|n to view your inventory, or |w+inv/detail {asset_name}|n for details.")
        else:
            self.caller.msg(f"|rFailed to create {asset_name}.|n")
    
    def _set_asset_quality(self):
        """Set the quality of an asset in inventory"""
        if not self.args:
            self.caller.msg("Usage: +asset/quality <asset name>=<quality>")
            self.caller.msg("Quality can be 0-5, or 'Special'")
            return
        
        if "=" not in self.args:
            self.caller.msg("Usage: +asset/quality <asset name>=<quality>")
            self.caller.msg("Quality can be 0-5, or 'Special'")
            return
        
        parts = self.args.split("=", 1)
        asset_path = parts[0].strip()
        quality_str = parts[1].strip()
        
        # Check if setting for another character (staff only)
        target_character = self.caller
        asset_name = asset_path
        
        if "/" in asset_path:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("|rYou don't have permission to set other characters' asset quality.|n")
                return
            
            # Parse character/asset=quality
            path_parts = asset_path.split("/", 1)
            char_name = path_parts[0].strip()
            asset_name = path_parts[1].strip()
            
            target_character = self.caller.search(char_name)
            if not target_character:
                return
            
            if not target_character.has_account and not hasattr(target_character, 'has_asset'):
                self.caller.msg(f"{target_character.name} is not a character.")
                return
        
        # Find the asset in the character's inventory
        asset = target_character.has_asset(asset_name)
        if not asset:
            if target_character == self.caller:
                self.caller.msg(f"|rYou don't have an asset named '{asset_name}' in your inventory.|n")
            else:
                self.caller.msg(f"|r{target_character.name} doesn't have an asset named '{asset_name}' in their inventory.|n")
            return
        
        # Parse quality value
        quality = None
        if quality_str.lower() == "special":
            quality = "Special"
        else:
            try:
                quality_int = int(quality_str)
                if 0 <= quality_int <= 5:
                    quality = quality_int
                else:
                    self.caller.msg("|rQuality must be between 0 and 5, or 'Special'.|n")
                    return
            except ValueError:
                self.caller.msg("|rQuality must be a number (0-5) or 'Special'.|n")
                return
        
        # Set the quality
        if asset.set_quality(quality):
            quality_display = "Special" if quality == "Special" else str(quality)
            if target_character == self.caller:
                self.caller.msg(f"|gSet {asset_name} quality to {quality_display}.|n")
            else:
                self.caller.msg(f"|gSet {target_character.name}'s {asset_name} quality to {quality_display}.|n")
                target_character.msg(f"|y{self.caller.name} set your {asset_name} quality to {quality_display}.|n")
        else:
            self.caller.msg(f"|rFailed to set quality. Quality must be 0-5 or 'Special'.|n")
