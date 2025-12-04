"""
GM Command for Rewarding Assets

Allows GMs to create and award custom assets to players as rewards.
"""

from evennia.commands.default.muxcommand import MuxCommand
from typeclasses.assets import create_custom_asset
from evennia.utils.search import search_object


class CmdReward(MuxCommand):
    """
    Award assets to characters (GM command).
    
    Usage:
        +reward/asset <character>=<name>/<type>/<quality>/<keywords>/<description>
        +reward/asset <character>=<name>/<type>/<quality>  (minimal format)
    
    Switches:
        /asset - Award a custom asset to a character
    
    Format:
        <name> - Name of the asset (use quotes if it contains spaces)
        <type> - Personal, Warfare, Espionage, or Intrigue
        <quality> - Quality rating (0-5, default 0)
        <keywords> - Comma-separated keywords (optional)
        <description> - Description of the asset (optional)
    
    Examples:
        +reward/asset Paul="Elite Guard Unit"/Warfare/2/"Infantry, Shield"/"Trained elite soldiers"
        +reward/asset Kara="Stolen Documents"/Espionage/0/"Intelligence, Blackmail"/"Documents stolen from enemy House"
        +reward/asset Nasir="Favor Owed"/Intrigue/0/"Favor"/"A favor owed by a contact"
        +reward/asset Paul="Custom Knife"/Personal/1/"Melee Weapon"/"A finely crafted blade"
    
    This command is for staff/GM use to reward players with custom assets
    created during play or as rewards for achievements.
    """
    
    key = "+reward"
    aliases = ["reward"]
    help_category = "Staff"
    
    def func(self):
        """Handle reward commands"""
        
        # Check permissions
        if not self.caller.check_permstring("Builder"):
            self.caller.msg("|rYou don't have permission to use this command.|n")
            return
        
        if "asset" not in self.switches:
            self.caller.msg("Usage: +reward/asset <character>=<name>/<type>/<quality>/<keywords>/<description>")
            self.caller.msg("")
            self.caller.msg("|yFormat:|n")
            self.caller.msg("  <character> - Character to reward")
            self.caller.msg("  <name> - Name of the asset (use quotes if it contains spaces)")
            self.caller.msg("  <type> - Personal, Warfare, Espionage, or Intrigue")
            self.caller.msg("  <quality> - Quality rating (0-5, default 0)")
            self.caller.msg("  <keywords> - Comma-separated keywords (optional)")
            self.caller.msg("  <description> - Description of the asset (optional)")
            self.caller.msg("")
            self.caller.msg("|yExamples:|n")
            self.caller.msg('  +reward/asset Paul="Elite Guard Unit"/Warfare/2/"Infantry, Shield"/"Trained elite soldiers"')
            self.caller.msg('  +reward/asset Kara="Stolen Documents"/Espionage/0/"Intelligence, Blackmail"/"Documents stolen from enemy House"')
            return
        
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +reward/asset <character>=<name>/<type>/<quality>/<keywords>/<description>")
            return
        
        # Parse: character=name/type/quality/keywords/description
        parts = self.args.split("=", 1)
        if len(parts) != 2:
            self.caller.msg("|rInvalid format. Use: <character>=<name>/<type>/<quality>/<keywords>/<description>|n")
            return
        
        char_name = parts[0].strip()
        rest = parts[1].strip()
        
        # Find character
        character = self.caller.search(char_name)
        if not character:
            return
        
        if not hasattr(character, 'has_asset'):
            self.caller.msg(f"|r{character.name} is not a character.|n")
            return
        
        # Split by / to get name, type, quality, keywords, description
        rest_parts = rest.split("/")
        if len(rest_parts) < 2:
            self.caller.msg("|rInvalid format. Must include at least asset name and type.|n")
            return
        
        name = rest_parts[0].strip().strip('"')
        asset_type = rest_parts[1].strip()
        quality = 0
        keywords = []
        description = ""
        special = ""
        
        if len(rest_parts) > 2:
            try:
                quality = int(rest_parts[2].strip())
                if not (0 <= quality <= 5):
                    self.caller.msg("|rQuality must be 0-5.|n")
                    return
            except ValueError:
                self.caller.msg("|rQuality must be a number (0-5).|n")
                return
        
        if len(rest_parts) > 3:
            keywords_str = rest_parts[3].strip().strip('"')
            if keywords_str:
                keywords = [k.strip() for k in keywords_str.split(",")]
        
        if len(rest_parts) > 4:
            description = rest_parts[4].strip().strip('"')
        
        # Validate asset type
        valid_types = ["Personal", "Warfare", "Espionage", "Intrigue"]
        if asset_type not in valid_types:
            self.caller.msg(f"|rInvalid asset type: {asset_type}|n")
            self.caller.msg(f"|yValid types:|n {', '.join(valid_types)}")
            return
        
        # Check if character already has an asset with this name
        existing = character.has_asset(name)
        if existing:
            self.caller.msg(f"|y{character.name} already has an asset named '{name}'.|n")
            return
        
        # Create the custom asset
        asset = create_custom_asset(
            name=name,
            asset_type=asset_type,
            character=character,
            quality=quality,
            keywords=keywords,
            description=description,
            special=special
        )
        
        if asset:
            self.caller.msg(f"|gAwarded custom asset to {character.name}: {name} ({asset_type}, Quality {quality})|n")
            character.msg(f"|gYou have been awarded: {name} ({asset_type}, Quality {quality})|n")
            if description:
                character.msg(f"|yDescription:|n {description}")
        else:
            self.caller.msg(f"|rFailed to create custom asset: {name}|n")




