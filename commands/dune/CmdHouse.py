"""
House Management Commands

Commands for creating and managing Noble Houses in the Dune MUSH.
All commands require builder+ permission.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia import create_object, search_object
from typeclasses.houses import (
    House, DOMAIN_AREAS, HOUSE_ROLES, HATRED_LEVELS, ENEMY_REASONS
)


class CmdHouse(MuxCommand):
    """
    View information about a Noble House.
    
    Usage:
        +house <house name>
        +house/list
        
    Switches:
        /list - List all Houses
        
    Examples:
        +house Atreides - View House Atreides information
        +house/list - List all Noble Houses
        
    This command displays comprehensive information about a Noble House including
    its type, domains, homeworld, roles, and enemies.
    """
    
    key = "+house"
    aliases = ["house"]
    locks = "cmd:all()"
    help_category = "Dune"
    
    def func(self):
        """View House information"""
        
        # List all Houses
        if "list" in self.switches:
            houses = search_object(typeclass="typeclasses.houses.House")
            if not houses:
                self.caller.msg("No Noble Houses have been created yet.")
                return
            
            self.caller.msg("|y" + "=" * 78 + "|n")
            self.caller.msg("|y" + " Noble Houses ".center(78, "=") + "|n")
            self.caller.msg("|y" + "=" * 78 + "|n")
            
            for house in houses:
                house_type = house.db.house_type
                member_count = len(house.db.members) if house.db.members else 0
                self.caller.msg(f"  |c{house.key}|n - {house_type} ({member_count} members)")
            
            self.caller.msg("|y" + "=" * 78 + "|n")
            return
        
        # View specific House
        if not self.args:
            self.caller.msg("Usage: +house <house name> or +house/list")
            return
        
        # Search for the House
        houses = search_object(self.args.strip(), typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{self.args.strip()}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        self.caller.msg(house.get_display())


class CmdHouseCreate(MuxCommand):
    """
    Create a new Noble House (staff only).
    
    Usage:
        +housecreate <house name>=<house type>
        
    House Types:
        Nascent House - Just acquired Minor House status (0 starting Threat)
        House Minor - Established vassal House (1 Threat per player)
        House Major - Ruling power of a planet (2 Threat per player)
        Great House - Controls multiple planets (3 Threat per player)
        
    Examples:
        +housecreate Molay=House Minor
        +housecreate Arcuri=House Minor
        
    This creates a new Noble House with the specified type. Further configuration
    is done with +houseset and related commands.
    
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+housecreate"
    aliases = ["housecreate"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Create a new House"""
        
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +housecreate <house name>=<house type>")
            self.caller.msg("House Types: Nascent House, House Minor, House Major, Great House")
            return
        
        house_name, house_type = self.args.split("=", 1)
        house_name = house_name.strip()
        house_type = house_type.strip()
        
        # Validate house type
        valid_types = ["Nascent House", "House Minor", "House Major", "Great House"]
        if house_type not in valid_types:
            self.caller.msg(f"Invalid house type. Valid types: {', '.join(valid_types)}")
            return
        
        # Check if House already exists
        existing = search_object(house_name, typeclass="typeclasses.houses.House")
        if existing:
            self.caller.msg(f"A House named '{house_name}' already exists.")
            return
        
        # Create the House
        house = create_object(
            typeclass="typeclasses.houses.House",
            key=house_name,
            location=None
        )
        
        house.db.house_type = house_type
        
        self.caller.msg(f"|gCreated {house_name} as a {house_type}.|n")
        self.caller.msg(f"Use +houseset to configure domains, banner, homeworld, and other details.")


class CmdHouseSet(MuxCommand):
    """
    Set properties of a Noble House (staff only).
    
    Usage:
        +houseset <house>/type=<house type>
        +houseset <house>/banner=<color>,<color>
        +houseset <house>/crest=<crest description>
        +houseset <house>/trait=<trait name>
        +houseset <house>/homeworld=<name>
        +houseset <house>/desc=<description>
        +houseset <house>/weather=<weather description>
        +houseset <house>/habitation=<habitation type>
        +houseset <house>/crime=<crime rate>
        +houseset <house>/populace=<populace mood>
        +houseset <house>/wealth=<wealth distribution>
        
    Switches:
        /type - Set House type
        /banner - Set banner colors (comma-separated)
        /crest - Set House crest/symbol
        /trait - Add a House trait
        /homeworld - Set homeworld name
        /desc - Set homeworld description
        /weather - Set weather description
        /habitation - Set habitation type
        /crime - Set crime rate description
        /populace - Set populace mood
        /wealth - Set wealth distribution
        
    Examples:
        +houseset Molay/type=House Minor
        +houseset Molay/banner=White,Red
        +houseset Molay/crest=Scroll
        +houseset Molay/trait=Secretive
        +houseset Molay/homeworld=Molay Prime
        +houseset Molay/desc=A string of large islands with varied terrain
        
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+houseset"
    aliases = ["houseset"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Set House properties"""
        
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +houseset <house>/<switch>=<value>")
            self.caller.msg("See 'help +houseset' for available switches.")
            return
        
        house_name, value = self.args.split("=", 1)
        house_name = house_name.strip()
        value = value.strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Handle switches
        if "type" in self.switches:
            valid_types = ["Nascent House", "House Minor", "House Major", "Great House"]
            if value not in valid_types:
                self.caller.msg(f"Invalid house type. Valid: {', '.join(valid_types)}")
                return
            house.db.house_type = value
            self.caller.msg(f"Set {house.key} type to {value}.")
            
        elif "banner" in self.switches:
            colors = [c.strip() for c in value.split(",")]
            house.db.banner_colors = colors
            self.caller.msg(f"Set {house.key} banner colors to: {', '.join(colors)}")
            
        elif "crest" in self.switches:
            house.db.crest = value
            self.caller.msg(f"Set {house.key} crest to: {value}")
            
        elif "trait" in self.switches:
            if value not in house.db.traits:
                house.db.traits.append(value)
                self.caller.msg(f"Added trait '{value}' to {house.key}.")
            else:
                self.caller.msg(f"{house.key} already has the trait '{value}'.")
                
        elif "homeworld" in self.switches:
            house.db.homeworld_name = value
            self.caller.msg(f"Set {house.key} homeworld to: {value}")
            
        elif "desc" in self.switches:
            house.db.homeworld_desc = value
            self.caller.msg(f"Set {house.key} homeworld description.")
            
        elif "weather" in self.switches:
            house.db.weather = value
            self.caller.msg(f"Set {house.key} weather to: {value}")
            
        elif "habitation" in self.switches:
            house.db.habitation = value
            self.caller.msg(f"Set {house.key} habitation to: {value}")
            
        elif "crime" in self.switches:
            house.db.crime_rate = value
            self.caller.msg(f"Set {house.key} crime rate to: {value}")
            
        elif "populace" in self.switches:
            house.db.populace_mood = value
            self.caller.msg(f"Set {house.key} populace mood to: {value}")
            
        elif "wealth" in self.switches:
            house.db.wealth_distribution = value
            self.caller.msg(f"Set {house.key} wealth distribution to: {value}")
            
        else:
            self.caller.msg("Invalid switch. See 'help +houseset' for available switches.")


class CmdHouseDomain(MuxCommand):
    """
    Manage House domains (areas of expertise) (staff only).
    
    Usage:
        +housedomain <house>/list
        +housedomain <house>/areas
        +housedomain <house>/add primary=<area>:<subtype>:<description>
        +housedomain <house>/add secondary=<area>:<subtype>:<description>
        +housedomain <house>/remove primary=<number>
        +housedomain <house>/remove secondary=<number>
        
    Switches:
        /list - List current domains
        /areas - List available domain areas and subtypes
        /add - Add a new domain (primary or secondary)
        /remove - Remove a domain by number
        
    Domain Areas:
        Artistic, Espionage, Farming, Industrial, Kanly, Military,
        Political, Religion, Science
        
    Subtypes:
        Machinery, Produce, Expertise, Workers, Understanding
        
    Examples:
        +housedomain Molay/list
        +housedomain Molay/areas
        +housedomain Molay/add primary=Artistic:Produce:Poetry
        +housedomain Molay/add secondary=Kanly:Workers:Assassins
        +housedomain Molay/remove secondary=1
        
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+housedomain"
    aliases = ["housedomain"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Manage House domains"""
        
        if not self.args:
            self.caller.msg("Usage: +housedomain <house>/<switch>[=<value>]")
            self.caller.msg("See 'help +housedomain' for details.")
            return
        
        # Parse house name
        if "/" in self.args:
            house_name = self.args.split("/")[0].strip()
        else:
            house_name = self.args.strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Handle switches
        if "list" in self.switches:
            output = [f"\n|y{'Domains for ' + house.key:=^78}|n"]
            
            primary_limit, secondary_limit = house.get_domain_limits()
            output.append(f"\n|wPrimary Domains ({len(house.db.primary_domains)}/{primary_limit}):|n")
            if house.db.primary_domains:
                for i, domain in enumerate(house.db.primary_domains):
                    output.append(f"  {i+1}. |c{domain['area']}|n ({domain['subtype']}): {domain['description']}")
            else:
                output.append("  None")
            
            output.append(f"\n|wSecondary Domains ({len(house.db.secondary_domains)}/{secondary_limit}):|n")
            if house.db.secondary_domains:
                for i, domain in enumerate(house.db.secondary_domains):
                    output.append(f"  {i+1}. |c{domain['area']}|n ({domain['subtype']}): {domain['description']}")
            else:
                output.append("  None")
            
            self.caller.msg("\n".join(output))
            
        elif "areas" in self.switches:
            output = ["\n|y{'Domain Areas':=^78}|n"]
            
            for area, subtypes in DOMAIN_AREAS.items():
                output.append(f"\n|c{area}|n")
                for subtype, examples in subtypes.items():
                    output.append(f"  {subtype}: {', '.join(examples[:3])}...")
            
            output.append("\n|wUsage:|n +housedomain <house>/add primary=<area>:<subtype>:<description>")
            self.caller.msg("\n".join(output))
            
        elif "add" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +housedomain <house>/add primary|secondary=<area>:<subtype>:<description>")
                return
            
            _, value = self.args.split("=", 1)
            parts = value.strip().split(":")
            
            if len(parts) != 3:
                self.caller.msg("Format: <area>:<subtype>:<description>")
                self.caller.msg("Example: Artistic:Produce:Poetry")
                return
            
            area, subtype, description = [p.strip() for p in parts]
            
            # Validate area
            if area not in DOMAIN_AREAS:
                self.caller.msg(f"Invalid area. Use +housedomain <house>/areas to see valid areas.")
                return
            
            # Validate subtype
            if subtype not in DOMAIN_AREAS[area]:
                self.caller.msg(f"Invalid subtype for {area}. Valid: {', '.join(DOMAIN_AREAS[area].keys())}")
                return
            
            # Determine if primary or secondary
            if "primary" in self.lhs.lower():
                is_primary = True
            elif "secondary" in self.lhs.lower():
                is_primary = False
            else:
                self.caller.msg("Specify 'primary' or 'secondary' in the house name.")
                self.caller.msg("Example: +housedomain Molay/add primary=...")
                return
            
            success, message = house.add_domain(is_primary, area, subtype, description)
            self.caller.msg(message)
            
        elif "remove" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +housedomain <house>/remove primary|secondary=<number>")
                return
            
            _, value = self.args.split("=", 1)
            
            try:
                index = int(value.strip()) - 1  # Convert to 0-based index
            except ValueError:
                self.caller.msg("Invalid number.")
                return
            
            # Determine if primary or secondary
            if "primary" in self.lhs.lower():
                is_primary = True
            elif "secondary" in self.lhs.lower():
                is_primary = False
            else:
                self.caller.msg("Specify 'primary' or 'secondary' in the house name.")
                return
            
            success, message = house.remove_domain(is_primary, index)
            self.caller.msg(message)
            
        else:
            self.caller.msg("Invalid switch. See 'help +housedomain' for available switches.")


class CmdHouseRole(MuxCommand):
    """
    Manage House roles and positions (staff only).
    
    Usage:
        +houserole <house>/list
        +houserole <house>/set <role>=<character name>[:<description>][:<traits>]
        +houserole <house>/remove <role>
        
    Switches:
        /list - List all roles and current holders
        /set - Assign a character to a role
        /remove - Clear a role
        
    Available Roles:
        Ruler, Consort, Advisor, Chief Physician, Councilor, Envoy, Heir,
        Marshal, Scholar, Spymaster, Swordmaster, Treasurer, Warmaster
        
    Examples:
        +houserole Molay/list
        +houserole Molay/set Ruler=Lady Elara Molay:Wise and just:Honorable,Political
        +houserole Molay/set Heir=Lord Marcus Molay
        +houserole Molay/remove Advisor
        
    Format: character name:description:trait1,trait2
    (description and traits are optional)
    
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+houserole"
    aliases = ["houserole"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Manage House roles"""
        
        if not self.args:
            self.caller.msg("Usage: +houserole <house>/<switch>[=<value>]")
            self.caller.msg("See 'help +houserole' for details.")
            return
        
        # Parse house name
        if "/" in self.args:
            house_name = self.args.split("/")[0].strip()
        else:
            house_name = self.args.strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Handle switches
        if "list" in self.switches:
            output = [f"\n|y{'Roles for ' + house.key:=^78}|n"]
            output.append(f"\n|wAvailable Roles:|n {', '.join(HOUSE_ROLES)}")
            
            if house.db.roles:
                output.append(f"\n|wFilled Roles:|n")
                for role, info in sorted(house.db.roles.items()):
                    traits_str = f" ({', '.join(info['traits'])})" if info.get('traits') else ""
                    desc_str = f" - {info['description']}" if info.get('description') else ""
                    output.append(f"  |c{role}:|n {info['character']}{traits_str}{desc_str}")
            else:
                output.append(f"\n|wFilled Roles:|n None")
            
            self.caller.msg("\n".join(output))
            
        elif "set" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +houserole <house>/set <role>=<character>[:<description>][:<traits>]")
                return
            
            role_part, value = self.args.split("=", 1)
            role_name = role_part.split("/")[-1].strip()
            
            # Parse value (character:description:traits)
            parts = value.split(":")
            character_name = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            traits = [t.strip() for t in parts[2].split(",")] if len(parts) > 2 else []
            
            success, message = house.set_role(role_name, character_name, description, traits)
            self.caller.msg(message)
            
        elif "remove" in self.switches:
            role_name = self.args.split("/")[-1].strip()
            success, message = house.remove_role(role_name)
            self.caller.msg(message)
            
        else:
            self.caller.msg("Invalid switch. See 'help +houserole' for available switches.")


class CmdHouseEnemy(MuxCommand):
    """
    Manage House enemies and rivalries (staff only).
    
    Usage:
        +houseenemy <house>/list
        +houseenemy <house>/add=<enemy house>:<hatred>:<reason>
        +houseenemy <house>/remove=<number>
        
    Switches:
        /list - List all enemy Houses
        /add - Add an enemy House
        /remove - Remove an enemy by number
        
    Hatred Levels:
        Dislike - Distrustful interactions (+1 Difficulty)
        Rival - Actively working against each other
        Loathing - Plans to destroy, but cautious
        Kanly - All-out vendetta to the death
        
    Reasons:
        Competition, Slight, Debt, Ancient Feud, Morality, Servitude,
        Family Ties, Theft, Jealousy, No Reason
        
    Examples:
        +houseenemy Molay/list
        +houseenemy Molay/add=House Arcuri:Loathing:Morality
        +houseenemy Molay/remove=1
        
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+houseenemy"
    aliases = ["houseenemy"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Manage House enemies"""
        
        if not self.args:
            self.caller.msg("Usage: +houseenemy <house>/<switch>[=<value>]")
            self.caller.msg("See 'help +houseenemy' for details.")
            return
        
        # Parse house name
        if "/" in self.args:
            house_name = self.args.split("/")[0].strip()
        else:
            house_name = self.args.strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Handle switches
        if "list" in self.switches:
            output = [f"\n|y{'Enemies of ' + house.key:=^78}|n"]
            
            if house.db.enemies:
                for i, enemy in enumerate(house.db.enemies):
                    output.append(f"\n{i+1}. |r{enemy['house']}|n")
                    output.append(f"   Hatred: {enemy['hatred']}")
                    output.append(f"   Reason: {enemy['reason']}")
                    output.append(f"   Effect: {HATRED_LEVELS[enemy['hatred']]}")
            else:
                output.append("\nNo enemies defined.")
            
            self.caller.msg("\n".join(output))
            
        elif "add" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +houseenemy <house>/add=<enemy>:<hatred>:<reason>")
                self.caller.msg(f"Hatred: {', '.join(HATRED_LEVELS.keys())}")
                self.caller.msg(f"Reasons: {', '.join(ENEMY_REASONS)}")
                return
            
            _, value = self.args.split("=", 1)
            parts = value.split(":")
            
            if len(parts) != 3:
                self.caller.msg("Format: <enemy house>:<hatred level>:<reason>")
                self.caller.msg("Example: House Arcuri:Loathing:Morality")
                return
            
            enemy_house, hatred, reason = [p.strip() for p in parts]
            
            success, message = house.add_enemy(enemy_house, hatred, reason)
            self.caller.msg(message)
            
        elif "remove" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +houseenemy <house>/remove=<number>")
                return
            
            _, value = self.args.split("=", 1)
            
            try:
                index = int(value.strip()) - 1  # Convert to 0-based index
            except ValueError:
                self.caller.msg("Invalid number.")
                return
            
            success, message = house.remove_enemy(index)
            self.caller.msg(message)
            
        else:
            self.caller.msg("Invalid switch. See 'help +houseenemy' for available switches.")


class CmdHouseMember(MuxCommand):
    """
    Manage House membership (staff only).
    
    Usage:
        +housemember <house>/add=<character>
        +housemember <house>/remove=<character>
        +housemember <house>/list
        +housemember <character>
        
    Switches:
        /add - Add a character to the House
        /remove - Remove a character from the House
        /list - List all members of the House
        
    Examples:
        +housemember Molay/add=Paul
        +housemember Molay/remove=Paul
        +housemember Molay/list
        +housemember Paul - Check which House Paul serves
        
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+housemember"
    aliases = ["housemember"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Manage House membership"""
        
        if not self.args:
            self.caller.msg("Usage: +housemember <house>/<switch>=<character>")
            self.caller.msg("       +housemember <character> - Check membership")
            return
        
        # Check membership (no switches, just character name)
        if not self.switches and "=" not in self.args:
            character = self.caller.search(self.args.strip())
            if not character:
                return
            
            if hasattr(character.db, 'house') and character.db.house:
                self.caller.msg(f"{character.name} serves {character.db.house.key}.")
            else:
                self.caller.msg(f"{character.name} does not serve any House.")
            return
        
        # Parse house name
        if "/" in self.args:
            house_name = self.args.split("/")[0].strip()
        else:
            house_name = self.args.split("=")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Handle switches
        if "add" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +housemember <house>/add=<character>")
                return
            
            _, char_name = self.args.split("=", 1)
            character = self.caller.search(char_name.strip())
            if not character:
                return
            
            success, message = house.add_member(character)
            self.caller.msg(message)
            
        elif "remove" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +housemember <house>/remove=<character>")
                return
            
            _, char_name = self.args.split("=", 1)
            character = self.caller.search(char_name.strip())
            if not character:
                return
            
            success, message = house.remove_member(character)
            self.caller.msg(message)
            
        elif "list" in self.switches:
            if not house.db.members:
                self.caller.msg(f"{house.key} has no members.")
                return
            
            output = [f"\n|y{'Members of ' + house.key:=^78}|n"]
            
            # Search for member objects
            from evennia import ObjectDB
            members = ObjectDB.objects.filter(id__in=house.db.members)
            
            for member in members:
                output.append(f"  {member.name}")
            
            output.append(f"\nTotal: {len(members)} member(s)")
            self.caller.msg("\n".join(output))
            
        else:
            self.caller.msg("Invalid switch. See 'help +housemember' for available switches.")

