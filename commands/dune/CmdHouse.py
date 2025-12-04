"""
House Management Commands

Consolidated command for creating and managing Noble Houses in the Dune MUSH.
All commands require builder+ permission except viewing.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia import create_object, search_object
from typeclasses.houses import (
    House, DOMAIN_AREAS, HOUSE_ROLES, HATRED_LEVELS, ENEMY_REASONS
)


class CmdHouse(MuxCommand):
    """
    View and manage Noble Houses.

    Usage:
        +house <house name>               - View House information
        +house/list                       - List all Houses
        +house/create <name>=<type>       - Create a new House (staff only)
        +house/destroy <name>             - Destroy a House (staff only)
        +house/set <house>/type=<type>    - Set House type (staff only)
        +house/set <house>/banner=<colors> - Set banner colors (staff only)
        +house/set <house>/crest=<symbol> - Set House crest (staff only)
        +house/set <house>/trait=<trait>  - Add a House trait (staff only)
        +house/set <house>/homeworld=<name> - Set homeworld name (staff only)
        +house/set <house>/desc=<text>    - Set homeworld description (staff only)
        +house/set <house>/weather=<text> - Set weather (staff only)
        +house/set <house>/habitation=<text> - Set habitation type (staff only)
        +house/set <house>/crime=<text>   - Set crime rate (staff only)
        +house/set <house>/populace=<text> - Set populace mood (staff only)
        +house/set <house>/wealth=<text>  - Set wealth distribution (staff only)
        +house/set <house>/quote=<text>  - Set House quote/motto (staff only)
        +house/skill <house>/values       - Show default skill values (staff only)
        +house/skill <house>/set <skill>=<value> - Set individual skill (staff only)
        +house/skill <house>/init=<b>,<c>,<d>,<m>,<u> - Initialize all skills (staff only)
        +house/status <house>             - View status and reputation (staff only)
        +house/status <house>/set=<value> - Set status (0-100) (staff only)
        +house/status <house>/adjust=<+/-amount> - Adjust status (staff only)
        +house/status <house>/reputation  - View reputation details (staff only)
        +house/spaces <house>             - View space allocations (staff only)
        +house/spaces <house>/allocate=<planet>:<#> - Allocate spaces (staff only)
        +house/spaces <house>/deallocate=<planet> - Remove allocation (staff only)
        +house/treasury <house>           - View treasury and income (staff only)
        +house/treasury <house>/income    - View detailed income breakdown (staff only)
        +house/treasury <house>/add wealth=<#> - Add wealth (staff only)
        +house/treasury <house>/add resources=<#> - Add resources (staff only)
        +house/treasury <house>/remove wealth=<#> - Remove wealth (staff only)
        +house/treasury <house>/remove resources=<#> - Remove resources (staff only)
        +house/treasury <house>/trade wealth=<#> - Trade wealth for resources (staff only)
        +house/treasury <house>/trade resources=<#> - Trade resources for wealth (staff only)
        +house/domain <house>/list        - List domains (staff only)
        +house/domain <house>/areas       - Show available areas (staff only)
        +house/domain <house>/add primary=<area>:<subtype>:<desc> (staff only)
        +house/domain <house>/add secondary=<area>:<subtype>:<desc> (staff only)
        +house/domain <house>/remove primary=<#> - Remove domain (staff only)
        +house/domain <house>/remove secondary=<#> - Remove domain (staff only)
        +house/role <house>/list          - List roles (staff only)
        +house/role <house>/set <role>=<name>[:<desc>][:<traits>] (staff only)
        +house/role/npc <house>/set <role>=<name>[:<desc>][:<traits>] - Set NPC role (staff only)
        +house/role <house>/remove <role> - Remove role (staff only)
        +house/enemy <house>/list         - List enemies (staff only)
        +house/enemy <house>/add=<enemy>:<hatred>:<reason> (staff only)
        +house/enemy <house>/remove=<#>   - Remove enemy (staff only)
        +house/member <house>/list        - List members (staff only)
        +house/member <house>/add=<character> - Add member (staff only)
        +house/member <house>/remove=<character> - Remove member (staff only)
        +house/member <character>         - Check character's House

    House Types: Nascent House (0 Threat), House Minor (1 Threat/player), House Major (2 Threat/player), Great House (3 Threat/player)

    Examples:
        +house Atreides | +house/list | +house/create Molay=House Minor
        +house/set Molay/banner=White,Red | +house/skill Molay/init=7,6,6,5,4
        +house/status Molay/set=25 | +house/treasury Molay/add wealth=100
        +house/domain Molay/add primary=Artistic:Produce:Poetry | +house/role Molay/set Ruler=Lady Elara Molay

    Staff Only: All management commands require Builder permission or higher.
    """
    
    key = "+house"
    aliases = ["house"]
    locks = "cmd:all()"
    help_category = "Dune"
    
    def func(self):
        """Main command dispatcher"""
        
        # Check for staff-only switches first
        staff_switches = ['create', 'destroy', 'set', 'skill', 'status', 'spaces', 'treasury', 'domain', 'role', 'enemy', 'member']
        
        # Allow 'member' switch with just character name (non-staff can check their own)
        if 'member' in self.switches and not self.lhs and self.args:
            # This is +house/member <character> format - check character's House
            self.check_character_house()
            return
        
        # Check if any staff switch is used
        needs_staff = any(sw in self.switches for sw in staff_switches)
        
        if needs_staff:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You need Builder permission or higher to manage Houses.")
                return
        
        # Route to appropriate handler
        if "list" in self.switches:
            self.list_houses()
        elif "create" in self.switches:
            self.create_house()
        elif "destroy" in self.switches:
            self.destroy_house()
        elif "set" in self.switches:
            self.set_property()
        elif "skill" in self.switches:
            self.manage_skills()
        elif "status" in self.switches:
            self.manage_status()
        elif "spaces" in self.switches:
            self.manage_spaces_house()
        elif "treasury" in self.switches:
            self.manage_treasury()
        elif "domain" in self.switches:
            self.manage_domains()
        elif "role" in self.switches:
            self.manage_roles()
        elif "enemy" in self.switches:
            self.manage_enemies()
        elif "member" in self.switches:
            self.manage_members()
        elif not self.switches:
            # No switches - view a House
            self.view_house()
        else:
            self.caller.msg("Invalid switch. See 'help +house' for available options.")
    
    def list_houses(self):
        """List all Houses."""
        from typeclasses.houses import House
        houses = House.objects.all()
        if not houses:
            self.caller.msg("No Noble Houses have been created yet.")
            return
        
        self.caller.msg("|y" + "=" * 78 + "|n")
        self.caller.msg("|y" + " Noble Houses ".center(78, "=") + "|n")
        self.caller.msg("|y" + "=" * 78 + "|n")
        
        for house in sorted(houses, key=lambda x: x.key):
            house_type = house.db.house_type
            member_count = len(house.db.member_roster) if house.db.member_roster else len(house.db.members) if house.db.members else 0
            self.caller.msg(f"  |c{house.key}|n - {house_type} ({member_count} members)")
        
        self.caller.msg("|y" + "=" * 78 + "|n")
    
    def view_house(self):
        """View specific House information."""
        if not self.args:
            self.caller.msg("Usage: +house <house name> or +house/list")
            return
        
        houses = search_object(self.args.strip(), typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{self.args.strip()}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        self.caller.msg(house.get_display())
    
    def create_house(self):
        """Create a new House."""
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +house/create <house name>=<house type>")
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
        
        # Set default status for House type
        default_status = house.get_default_status()
        house.db.status = default_status
        
        self.caller.msg(f"|gCreated {house_name} as a {house_type}.|n")
        self.caller.msg(f"Default status set to {default_status} (Reputation: {house.get_reputation()}).")
        self.caller.msg(f"Use +house/skill, +house/set, and +house/domain to configure the House.")
    
    def destroy_house(self):
        """Destroy a House."""
        if not self.args:
            self.caller.msg("Usage: +house/destroy <house name>")
            return
        
        houses = search_object(self.args.strip(), typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{self.args.strip()}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        house_name = house.key
        
        # Remove House affiliation from all members
        if house.db.member_roster:
            from evennia import ObjectDB
            for char_id in house.db.member_roster.keys():
                try:
                    character = ObjectDB.objects.get(id=char_id)
                    character.db.house = None
                except ObjectDB.DoesNotExist:
                    pass
        
        house.delete()
        self.caller.msg(f"|rDestroyed House {house_name}.|n")
    
    def set_property(self):
        """Set House properties."""
        if not self.lhs or "=" not in self.args:
            self.caller.msg("Usage: +house/set <house>/<property>=<value>")
            self.caller.msg("See 'help +house' for available properties.")
            return
        
        # Parse house name from lhs (before the /)
        parts = self.lhs.split("/")
        if len(parts) < 2:
            self.caller.msg("Usage: +house/set <house>/<property>=<value>")
            return
        
        house_name = parts[0].strip()
        property_name = parts[1].strip().lower()
        value = self.rhs.strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Handle different properties
        if property_name == "type":
            valid_types = ["Nascent House", "House Minor", "House Major", "Great House"]
            if value not in valid_types:
                self.caller.msg(f"Invalid house type. Valid: {', '.join(valid_types)}")
                return
            house.db.house_type = value
            self.caller.msg(f"Set {house.key} type to {value}.")
            
        elif property_name == "banner":
            colors = [c.strip() for c in value.split(",")]
            house.db.banner_colors = colors
            self.caller.msg(f"Set {house.key} banner colors to: {', '.join(colors)}")
            
        elif property_name == "crest":
            house.db.crest = value
            self.caller.msg(f"Set {house.key} crest to: {value}")
            
        elif property_name == "trait":
            if value not in house.db.traits:
                house.db.traits.append(value)
                self.caller.msg(f"Added trait '{value}' to {house.key}.")
            else:
                self.caller.msg(f"{house.key} already has the trait '{value}'.")
                
        elif property_name == "homeworld":
            house.db.homeworld_name = value
            self.caller.msg(f"Set {house.key} homeworld to: {value}")
            
        elif property_name == "desc":
            house.db.homeworld_desc = value
            self.caller.msg(f"Set {house.key} homeworld description.")
            
        elif property_name == "weather":
            house.db.weather = value
            self.caller.msg(f"Set {house.key} weather to: {value}")
            
        elif property_name == "habitation":
            house.db.habitation = value
            self.caller.msg(f"Set {house.key} habitation to: {value}")
            
        elif property_name == "crime":
            house.db.crime_rate = value
            self.caller.msg(f"Set {house.key} crime rate to: {value}")
            
        elif property_name == "populace":
            house.db.populace_mood = value
            self.caller.msg(f"Set {house.key} populace mood to: {value}")
            
        elif property_name == "wealth":
            house.db.wealth_distribution = value
            self.caller.msg(f"Set {house.key} wealth distribution to: {value}")
            
        elif property_name == "quote":
            house.db.quote = value
            self.caller.msg(f"Set {house.key} quote to: \"{value}\"")
            
        else:
            self.caller.msg(f"Unknown property '{property_name}'. See 'help +house' for available properties.")
    
    def manage_skills(self):
        """Manage House skills."""
        if not self.lhs:
            self.caller.msg("Usage: +house/skill <house>/<action>[=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action
        if "/values" in self.lhs.lower():
            # Show default skill values for this house type
            default_values = house.get_default_skill_values()
            output = [f"\n|y{'Skill Values for ' + house.key:=^78}|n"]
            output.append(f"\n|wHouse Type:|n {house.db.house_type}")
            output.append(f"|wRecommended Starting Values:|n {', '.join(map(str, default_values))}")
            output.append(f"\n|wCurrent Skills:|n")
            output.append(f"  Battle: {house.db.skills.get('Battle', 0)}")
            output.append(f"  Communicate: {house.db.skills.get('Communicate', 0)}")
            output.append(f"  Discipline: {house.db.skills.get('Discipline', 0)}")
            output.append(f"  Move: {house.db.skills.get('Move', 0)}")
            output.append(f"  Understand: {house.db.skills.get('Understand', 0)}")
            output.append(f"\n|wSkill Descriptions:|n")
            output.append(f"  |cBattle:|n Military power, tactical skill, and armed forces quality")
            output.append(f"  |cCommunicate:|n Diplomatic reputation, influence, and espionage")
            output.append(f"  |cDiscipline:|n Loyalty of people and forces, internal stability")
            output.append(f"  |cMove:|n Response time, crisis management, and agent placement")
            output.append(f"  |cUnderstand:|n Academic excellence, research, and technology")
            output.append(f"\n|wUsage:|n")
            output.append(f"  +house/skill {house.key}/init=<battle>,<communicate>,<discipline>,<move>,<understand>")
            output.append(f"  +house/skill {house.key}/set <skill>=<value>")
            self.caller.msg("\n".join(output))
            
        elif "/set" in self.lhs.lower():
            # Set individual skill
            if "=" not in self.args:
                self.caller.msg("Usage: +house/skill <house>/set <skill>=<value>")
                self.caller.msg("Skills: Battle, Communicate, Discipline, Move, Understand")
                return
            
            # Parse: Alexin/set Battle=8
            # Split on /set to get skill name from the part after
            set_split = self.lhs.lower().split("/set")
            if len(set_split) < 2:
                self.caller.msg("Usage: +house/skill <house>/set <skill>=<value>")
                return
            
            # Get everything after /set, which should be the skill name (possibly with whitespace)
            skill_part = set_split[1].strip()
            if not skill_part:
                self.caller.msg("Usage: +house/skill <house>/set <skill>=<value>")
                self.caller.msg("Skills: Battle, Communicate, Discipline, Move, Understand")
                return
            
            # The skill name is what's left after /set and before the =
            # Since self.lhs is "Alexin/set Battle", and we want "Battle"
            # We need to extract from the original self.lhs
            lhs_parts = self.lhs.split("/set", 1)
            if len(lhs_parts) > 1:
                skill_name = lhs_parts[1].strip()
            else:
                self.caller.msg("Usage: +house/skill <house>/set <skill>=<value>")
                return
            
            value = self.rhs.strip()
            
            success, message = house.set_skill(skill_name, value)
            self.caller.msg(message)
            
        elif "/init" in self.lhs.lower():
            # Initialize all skills at once
            if "=" not in self.args:
                default_values = house.get_default_skill_values()
                self.caller.msg("Usage: +house/skill <house>/init=<battle>,<communicate>,<discipline>,<move>,<understand>")
                self.caller.msg(f"Recommended values for {house.db.house_type}: {', '.join(map(str, default_values))}")
                return
            
            # Parse comma-separated values
            values = [v.strip() for v in self.rhs.split(",")]
            
            if len(values) != 5:
                self.caller.msg("You must provide exactly 5 values: Battle, Communicate, Discipline, Move, Understand")
                return
            
            try:
                battle, communicate, discipline, move, understand = [int(v) for v in values]
            except ValueError:
                self.caller.msg("All values must be numbers.")
                return
            
            success, message = house.initialize_skills(battle, communicate, discipline, move, understand)
            self.caller.msg(message)
            
            # Show the result
            output = [f"\n|gSkills initialized for {house.key}:|n"]
            output.append(f"  Battle: {battle}")
            output.append(f"  Communicate: {communicate}")
            output.append(f"  Discipline: {discipline}")
            output.append(f"  Move: {move}")
            output.append(f"  Understand: {understand}")
            self.caller.msg("\n".join(output))
        else:
            self.caller.msg("Usage: +house/skill <house>/values|set|init")
    
    def manage_status(self):
        """Manage House status and reputation."""
        if not self.lhs:
            self.caller.msg("Usage: +house/status <house>[/<action>][=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action
        if "/set" in self.lhs.lower():
            # Set status to specific value
            if "=" not in self.args:
                self.caller.msg("Usage: +house/status <house>/set=<value>")
                self.caller.msg("Value must be between 0 and 100.")
                return
            
            success, message = house.set_status(self.rhs.strip())
            self.caller.msg(message)
            
        elif "/adjust" in self.lhs.lower():
            # Adjust status by amount
            if "=" not in self.args:
                self.caller.msg("Usage: +house/status <house>/adjust=<+/-amount>")
                self.caller.msg("Example: +house/status Molay/adjust=+5")
                return
            
            success, message = house.adjust_status(self.rhs.strip())
            self.caller.msg(message)
            
        elif "/reputation" in self.lhs.lower():
            # Show detailed reputation information
            reputation = house.get_reputation()
            output = [f"\n|y{'Reputation Details for ' + house.key:=^78}|n"]
            output.append(f"\n|wCurrent Status:|n {house.db.status}/100")
            output.append(f"|wReputation Level:|n {reputation}")
            output.append(f"\n|wDescription:|n")
            
            # Wrap description text
            desc = house.get_reputation_description()
            import textwrap
            wrapped = textwrap.fill(desc, width=76)
            for line in wrapped.split('\n'):
                output.append(f"  {line}")
            
            output.append(f"\n|wMechanical Effects:|n")
            effects = house.get_reputation_effects()
            for effect in effects.split('|'):
                if effect.strip():
                    output.append(f"  • {effect.strip()}")
            
            # Show reputation thresholds for this House type
            output.append(f"\n|wReputation Thresholds for {house.db.house_type}:|n")
            
            house_type = house.db.house_type
            if house_type == "Nascent House":
                house_type = "House Minor"
            
            if house_type == "House Minor":
                output.append("  Feeble: 0-10 | Weak: 11-20 | Respected: 21-40")
                output.append("  Strong: 41-50 | Problematic: 51-70 | Dangerous: 71+")
            elif house_type == "House Major":
                output.append("  Feeble: 0-20 | Weak: 21-40 | Respected: 41-60")
                output.append("  Strong: 61-70 | Problematic: 71-80 | Dangerous: 81+")
            elif house_type == "Great House":
                output.append("  Feeble: 0-40 | Weak: 41-60 | Respected: 61-70")
                output.append("  Strong: 71-80 | Problematic: 81-90 | Dangerous: 91+")
            
            self.caller.msg("\n".join(output))
            
        else:
            # Just show current status
            reputation = house.get_reputation()
            reputation_color = {
                "Feeble": "|r",
                "Weak": "|y",
                "Respected": "|g",
                "Strong": "|c",
                "Problematic": "|m",
                "Dangerous": "|R"
            }.get(reputation, "|w")
            
            output = [f"\n|y{'Status for ' + house.key:=^78}|n"]
            output.append(f"\n|wHouse Type:|n {house.db.house_type}")
            output.append(f"|wCurrent Status:|n {house.db.status}/100")
            output.append(f"|wReputation:|n {reputation_color}{reputation}|n")
            output.append(f"\n|wEffects:|n {house.get_reputation_effects()}")
            output.append(f"\n|wCommands:|n")
            output.append(f"  +house/status {house.key}/set=<value>")
            output.append(f"  +house/status {house.key}/adjust=<+/-amount>")
            output.append(f"  +house/status {house.key}/reputation")
            self.caller.msg("\n".join(output))
    
    def manage_spaces_house(self):
        """Manage House space allocations."""
        if not self.lhs:
            self.caller.msg("Usage: +house/spaces <house>[/<action>][=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action
        if "/allocate" in self.lhs.lower():
            # Allocate spaces on a planet
            if "=" not in self.args:
                self.caller.msg("Usage: +house/spaces <house>/allocate=<planet name>:<spaces>")
                self.caller.msg("Example: +house/spaces Molay/allocate=Molay Prime:35")
                return
            
            # Parse planet:spaces format
            parts = self.rhs.strip().split(":")
            if len(parts) != 2:
                self.caller.msg("Format: <planet name>:<spaces>")
                self.caller.msg("Example: Molay Prime:35")
                return
            
            planet_name, spaces_str = parts
            planet_name = planet_name.strip()
            
            # Find the Planet
            planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
            if not planets:
                self.caller.msg(f"No Planet found with the name '{planet_name}'.")
                return
            if len(planets) > 1:
                self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
                return
            
            planet = planets[0]
            
            # Allocate spaces
            success, message = house.allocate_spaces_on_planet(planet, spaces_str.strip())
            self.caller.msg(message)
            
            if success:
                # Show updated information
                total_house = house.get_total_spaces()
                required = house.get_domain_space_requirements()
                surplus_deficit = house.get_space_surplus_deficit()
                
                self.caller.msg(f"{house.key} now controls {total_house} total spaces.")
                self.caller.msg(f"Domain requirements: {required} spaces")
                if surplus_deficit >= 0:
                    self.caller.msg(f"Surplus: |g{surplus_deficit} spaces|n")
                else:
                    self.caller.msg(f"Deficit: |r{abs(surplus_deficit)} spaces needed!|n")
            
        elif "/deallocate" in self.lhs.lower():
            # Remove allocation on a planet
            if "=" not in self.args:
                self.caller.msg("Usage: +house/spaces <house>/deallocate=<planet name>")
                return
            
            planet_name = self.rhs.strip()
            
            # Find the Planet
            planets = search_object(planet_name, typeclass="typeclasses.planets.Planet")
            if not planets:
                self.caller.msg(f"No Planet found with the name '{planet_name}'.")
                return
            if len(planets) > 1:
                self.caller.msg(f"Multiple Planets found: {', '.join([p.key for p in planets])}")
                return
            
            planet = planets[0]
            
            # Deallocate spaces
            success, message = house.deallocate_spaces_on_planet(planet)
            self.caller.msg(message)
            
        else:
            # Show space information
            output = [f"\n|y{'Space Allocations for ' + house.key:=^78}|n"]
            
            total_spaces = house.get_total_spaces()
            typical_spaces = house.get_typical_spaces()
            required_spaces = house.get_domain_space_requirements()
            surplus_deficit = house.get_space_surplus_deficit()
            
            output.append(f"\n|wHouse Type:|n {house.db.house_type} (Typical: {typical_spaces} spaces)")
            output.append(f"|wTotal Spaces Controlled:|n {total_spaces}")
            output.append(f"|wDomain Requirements:|n {required_spaces} spaces")
            
            if surplus_deficit >= 0:
                output.append(f"|wSurplus:|n |g{surplus_deficit} spaces available|n")
            else:
                output.append(f"|wDeficit:|n |r{abs(surplus_deficit)} spaces needed!|n")
            
            # Show domain breakdown
            if house.db.primary_domains or house.db.secondary_domains:
                output.append(f"\n|wDomain Space Requirements:|n")
                if house.db.primary_domains:
                    for domain in house.db.primary_domains:
                        output.append(f"  Primary ({domain['area']}): 25 spaces")
                if house.db.secondary_domains:
                    for domain in house.db.secondary_domains:
                        output.append(f"  Secondary ({domain['area']}): 10 spaces")
            
            # Show planet allocations
            allocations = house.get_planet_allocations()
            if allocations:
                output.append(f"\n|wPlanet Allocations:|n")
                for planet, spaces in allocations:
                    percentage = (spaces / total_spaces * 100) if total_spaces > 0 else 0
                    output.append(f"  |c{planet.key}|n: {spaces} spaces ({percentage:.1f}%)")
            else:
                output.append(f"\n|yNo space allocations yet.|n")
            
            output.append(f"\n|wCommands:|n")
            output.append(f"  +house/spaces {house.key}/allocate=<planet>:<spaces>")
            output.append(f"  +house/spaces {house.key}/deallocate=<planet>")
            
            self.caller.msg("\n".join(output))
    
    def manage_treasury(self):
        """Manage House treasury (Wealth and Resources)."""
        if not self.lhs:
            self.caller.msg("Usage: +house/treasury <house>[/<action>][=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action
        if "/income" in self.lhs.lower():
            # Show detailed income breakdown
            output = [f"\n|y{'Income Breakdown for ' + house.key:=^78}|n"]
            
            domain_resources, domain_wealth = house.calculate_domain_income()
            role_resources, role_wealth = house.calculate_role_bonuses()
            total_resources, total_wealth = house.get_total_income()
            
            output.append(f"\n|w{'Domain Income':^78}|n")
            
            # Show primary domains
            if house.db.primary_domains:
                output.append(f"\n|wPrimary Domains:|n")
                for domain in house.db.primary_domains:
                    output.append(f"  {domain['area']} ({domain['subtype']})")
            
            # Show secondary domains
            if house.db.secondary_domains:
                output.append(f"\n|wSecondary Domains:|n")
                for domain in house.db.secondary_domains:
                    output.append(f"  {domain['area']} ({domain['subtype']})")
            
            output.append(f"\n|wDomain Total:|n")
            output.append(f"  Resources: {domain_resources}")
            output.append(f"  Wealth: {domain_wealth}")
            
            # Show role bonuses
            if role_resources > 0 or role_wealth > 0:
                output.append(f"\n|wRole Bonuses:|n")
                if "Treasurer" in house.db.roles:
                    output.append(f"  Treasurer: +10 Wealth")
                output.append(f"\n|wRole Total:|n")
                output.append(f"  Resources: +{role_resources}")
                output.append(f"  Wealth: +{role_wealth}")
            
            output.append(f"\n|w{'=' * 78}|n")
            output.append(f"|wTotal Income per Cycle:|n")
            output.append(f"  |gResources: {total_resources}|n")
            output.append(f"  |gWealth: {total_wealth}|n")
            
            self.caller.msg("\n".join(output))
            
        elif "/add" in self.lhs.lower():
            # Add wealth or resources
            if "=" not in self.args:
                self.caller.msg("Usage: +house/treasury <house>/add wealth|resources=<amount>")
                self.caller.msg("Example: +house/treasury Molay/add wealth=100")
                return
            
            # Parse: Alexin/add wealth=100
            # Split on /add to extract resource type
            add_split = self.lhs.split("/add", 1)
            if len(add_split) < 2:
                self.caller.msg("Usage: +house/treasury <house>/add wealth|resources=<amount>")
                return
            
            resource_type = add_split[1].strip().lower()
            amount = self.rhs.strip()
            
            if not resource_type:
                self.caller.msg("Usage: +house/treasury <house>/add wealth|resources=<amount>")
                return
            
            if resource_type == "wealth":
                success, message = house.add_wealth(amount)
                self.caller.msg(message)
            elif resource_type == "resources":
                success, message = house.add_resources(amount)
                self.caller.msg(message)
            else:
                self.caller.msg("Specify 'wealth' or 'resources'.")
                self.caller.msg("Example: +house/treasury Molay/add wealth=100")
            
        elif "/remove" in self.lhs.lower():
            # Remove wealth or resources
            if "=" not in self.args:
                self.caller.msg("Usage: +house/treasury <house>/remove wealth|resources=<amount>")
                self.caller.msg("Example: +house/treasury Molay/remove wealth=50")
                return
            
            # Parse: Alexin/remove wealth=50
            # Split on /remove to extract resource type
            remove_split = self.lhs.split("/remove", 1)
            if len(remove_split) < 2:
                self.caller.msg("Usage: +house/treasury <house>/remove wealth|resources=<amount>")
                return
            
            resource_type = remove_split[1].strip().lower()
            amount = self.rhs.strip()
            
            if not resource_type:
                self.caller.msg("Usage: +house/treasury <house>/remove wealth|resources=<amount>")
                return
            
            if resource_type == "wealth":
                success, message = house.remove_wealth(amount)
                self.caller.msg(message)
            elif resource_type == "resources":
                success, message = house.remove_resources(amount)
                self.caller.msg(message)
            else:
                self.caller.msg("Specify 'wealth' or 'resources'.")
                self.caller.msg("Example: +house/treasury Molay/remove resources=10")
            
        elif "/trade" in self.lhs.lower():
            # Trade wealth for resources or vice versa
            if "=" not in self.args:
                self.caller.msg("Usage: +house/treasury <house>/trade wealth|resources=<amount>")
                self.caller.msg("Exchange rate: 3 Wealth = 1 Resource or 1 Resource = 3 Wealth")
                self.caller.msg("Can trade up to 1/3 of current holdings")
                return
            
            # Parse: Alexin/trade wealth=9
            # Split on /trade to extract resource type
            trade_split = self.lhs.split("/trade", 1)
            if len(trade_split) < 2:
                self.caller.msg("Usage: +house/treasury <house>/trade wealth|resources=<amount>")
                return
            
            resource_type = trade_split[1].strip().lower()
            amount = self.rhs.strip()
            
            if not resource_type:
                self.caller.msg("Usage: +house/treasury <house>/trade wealth|resources=<amount>")
                return
            
            if resource_type == "wealth":
                success, message = house.trade_wealth_for_resources(amount)
                self.caller.msg(message)
                if success:
                    self.caller.msg("|yNote: Trading uses one venture slot.|n")
            elif resource_type == "resources":
                success, message = house.trade_resources_for_wealth(amount)
                self.caller.msg(message)
                if success:
                    self.caller.msg("|yNote: Trading uses one venture slot.|n")
            else:
                self.caller.msg("Specify 'wealth' or 'resources'.")
                self.caller.msg("Example: +house/treasury Molay/trade wealth=9")
            
        else:
            # Show treasury information
            output = [f"\n|y{'Treasury for ' + house.key:=^78}|n"]
            
            current_wealth = house.db.wealth if hasattr(house.db, 'wealth') else 0
            current_resources = house.db.resources if hasattr(house.db, 'resources') else 0
            
            output.append(f"\n|wCurrent Holdings:|n")
            output.append(f"  Wealth: |g{current_wealth}|n")
            output.append(f"  Resources: |g{current_resources}|n")
            
            # Show income
            total_resources, total_wealth = house.get_total_income()
            
            output.append(f"\n|wIncome per Cycle:|n")
            output.append(f"  Resources: {total_resources}")
            output.append(f"  Wealth: {total_wealth}")
            
            # Show trading capacity
            if current_wealth >= 3:
                max_wealth_trade = current_wealth // 3
                output.append(f"\n|wTrading Capacity (1/3 limit):|n")
                output.append(f"  Can trade up to {max_wealth_trade} Wealth for {max_wealth_trade // 3} Resources")
            if current_resources >= 1:
                max_resource_trade = current_resources // 3
                if current_wealth < 3:
                    output.append(f"\n|wTrading Capacity (1/3 limit):|n")
                output.append(f"  Can trade up to {max_resource_trade} Resources for {max_resource_trade * 3} Wealth")
            
            output.append(f"\n|wExchange Rate:|n 3 Wealth = 1 Resource | 1 Resource = 3 Wealth")
            
            output.append(f"\n|wCommands:|n")
            output.append(f"  +house/treasury {house.key}/income")
            output.append(f"  +house/treasury {house.key}/add wealth|resources=<amount>")
            output.append(f"  +house/treasury {house.key}/remove wealth|resources=<amount>")
            output.append(f"  +house/treasury {house.key}/trade wealth|resources=<amount>")
            
            self.caller.msg("\n".join(output))
    
    def manage_domains(self):
        """Manage House domains."""
        if not self.lhs:
            self.caller.msg("Usage: +house/domain <house>/<action>[=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action from lhs
        action = None
        if "/list" in self.lhs.lower():
            action = "list"
        elif "/areas" in self.lhs.lower():
            action = "areas"
        elif "/add" in self.lhs.lower():
            action = "add"
        elif "/remove" in self.lhs.lower():
            action = "remove"
        
        if action == "list":
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
            
        elif action == "areas":
            output = ["\n|y{'Domain Areas':=^78}|n"]
            
            for area, subtypes in DOMAIN_AREAS.items():
                output.append(f"\n|c{area}|n")
                for subtype, examples in subtypes.items():
                    output.append(f"  {subtype}: {', '.join(examples[:3])}...")
            
            output.append("\n|wUsage:|n +house/domain <house>/add primary=<area>:<subtype>:<description>")
            self.caller.msg("\n".join(output))
            
        elif action == "add":
            if "=" not in self.args:
                self.caller.msg("Usage: +house/domain <house>/add primary|secondary=<area>:<subtype>:<description>")
                return
            
            parts = self.rhs.strip().split(":")
            
            if len(parts) != 3:
                self.caller.msg("Format: <area>:<subtype>:<description>")
                self.caller.msg("Example: Artistic:Produce:Poetry")
                return
            
            area, subtype, description = [p.strip() for p in parts]
            
            # Validate area
            if area not in DOMAIN_AREAS:
                self.caller.msg(f"Invalid area. Use +house/domain <house>/areas to see valid areas.")
                return
            
            # Validate subtype
            if subtype not in DOMAIN_AREAS[area]:
                self.caller.msg(f"Invalid subtype for {area}. Valid: {', '.join(DOMAIN_AREAS[area].keys())}")
                return
            
            # Determine if primary or secondary from lhs
            if "primary" in self.lhs.lower():
                is_primary = True
            elif "secondary" in self.lhs.lower():
                is_primary = False
            else:
                self.caller.msg("Specify 'primary' or 'secondary' in the command.")
                self.caller.msg("Example: +house/domain Molay/add primary=...")
                return
            
            success, message = house.add_domain(is_primary, area, subtype, description)
            self.caller.msg(message)
            
        elif action == "remove":
            if "=" not in self.args:
                self.caller.msg("Usage: +house/domain <house>/remove primary|secondary=<number>")
                return
            
            try:
                index = int(self.rhs.strip()) - 1  # Convert to 0-based index
            except ValueError:
                self.caller.msg("Invalid number.")
                return
            
            # Determine if primary or secondary
            if "primary" in self.lhs.lower():
                is_primary = True
            elif "secondary" in self.lhs.lower():
                is_primary = False
            else:
                self.caller.msg("Specify 'primary' or 'secondary' in the command.")
                return
            
            success, message = house.remove_domain(is_primary, index)
            self.caller.msg(message)
        else:
            self.caller.msg("Usage: +house/domain <house>/list|areas|add|remove")
    
    def manage_roles(self):
        """Manage House roles."""
        if not self.lhs:
            self.caller.msg("Usage: +house/role <house>/<action>[=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action
        if "/list" in self.lhs.lower():
            output = [f"\n|y{'Roles for ' + house.key:=^78}|n"]
            output.append(f"\n|wAvailable Roles:|n {', '.join(HOUSE_ROLES)}")
            
            if house.db.roles:
                output.append(f"\n|wFilled Roles:|n")
                for role, info in sorted(house.db.roles.items()):
                    traits_str = f" ({', '.join(info['traits'])})" if info.get('traits') else ""
                    desc_str = f" - {info['description']}" if info.get('description') else ""
                    npc_str = " |r(NPC)|n" if info.get('is_npc', False) else ""
                    output.append(f"  |c{role}:|n {info['character']}{npc_str}{traits_str}{desc_str}")
            else:
                output.append(f"\n|wFilled Roles:|n None")
            
            self.caller.msg("\n".join(output))
            
        elif "/set" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +house/role <house>/set <role>=<character>[:<description>][:<traits>]")
                self.caller.msg("Add /npc flag to set an NPC role without character validation.")
                return
            
            # Check for /npc flag
            is_npc = "npc" in self.switches
            
            # Parse: Alexin/set Ruler=Character Name
            # Split on /set to extract role name
            set_split = self.lhs.split("/set", 1)
            if len(set_split) < 2:
                self.caller.msg("Usage: +house/role <house>/set <role>=<character>[:<description>][:<traits>]")
                self.caller.msg("Add /npc flag to set an NPC role without character validation.")
                return
            
            # Get role name from everything after /set
            role_name = set_split[1].strip()
            
            if not role_name:
                self.caller.msg("Usage: +house/role <house>/set <role>=<character>[:<description>][:<traits>]")
                self.caller.msg("Add /npc flag to set an NPC role without character validation.")
                return
            
            # Parse value (character:description:traits)
            parts = self.rhs.split(":")
            character_name = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            traits = [t.strip() for t in parts[2].split(",")] if len(parts) > 2 else []
            
            success, message = house.set_role(role_name, character_name, description, traits, caller=self.caller, is_npc=is_npc)
            if success:
                self.caller.msg(f"|g{message}|n")
            else:
                self.caller.msg(f"|r{message}|n")
            
        elif "/remove" in self.lhs.lower():
            # Parse: Alexin/remove Ruler
            # Split on /remove to extract role name
            remove_split = self.lhs.split("/remove", 1)
            if len(remove_split) < 2:
                self.caller.msg("Usage: +house/role <house>/remove <role>")
                return
            
            role_name = remove_split[1].strip()
            
            if not role_name:
                self.caller.msg("Usage: +house/role <house>/remove <role>")
                return
            
            success, message = house.remove_role(role_name)
            self.caller.msg(message)
        else:
            self.caller.msg("Usage: +house/role <house>/list|set|remove")
    
    def manage_enemies(self):
        """Manage House enemies."""
        if not self.lhs:
            self.caller.msg("Usage: +house/enemy <house>/<action>[=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action
        if "/list" in self.lhs.lower():
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
            
        elif "/add" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +house/enemy <house>/add=<enemy>:<hatred>:<reason>")
                self.caller.msg(f"Hatred: {', '.join(HATRED_LEVELS.keys())}")
                self.caller.msg(f"Reasons: {', '.join(ENEMY_REASONS)}")
                return
            
            parts = self.rhs.split(":")
            
            if len(parts) != 3:
                self.caller.msg("Format: <enemy house>:<hatred level>:<reason>")
                self.caller.msg("Example: House Arcuri:Loathing:Morality")
                return
            
            enemy_house, hatred, reason = [p.strip() for p in parts]
            
            success, message = house.add_enemy(enemy_house, hatred, reason)
            self.caller.msg(message)
            
        elif "/remove" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +house/enemy <house>/remove=<number>")
                return
            
            try:
                index = int(self.rhs.strip()) - 1  # Convert to 0-based index
            except ValueError:
                self.caller.msg("Invalid number.")
                return
            
            success, message = house.remove_enemy(index)
            self.caller.msg(message)
        else:
            self.caller.msg("Usage: +house/enemy <house>/list|add|remove")
    
    def manage_members(self):
        """Manage House membership."""
        # Check if this is a character check (non-staff)
        if not self.lhs and self.args and "=" not in self.args:
            self.check_character_house()
            return
        
        if not self.lhs:
            self.caller.msg("Usage: +house/member <house>/<action>[=<value>]")
            return
        
        # Parse house name
        house_name = self.lhs.split("/")[0].strip()
        
        # Find the House
        houses = search_object(house_name, typeclass="typeclasses.houses.House")
        if not houses:
            self.caller.msg(f"No House found with the name '{house_name}'.")
            return
        
        if len(houses) > 1:
            self.caller.msg(f"Multiple Houses found: {', '.join([h.key for h in houses])}")
            return
        
        house = houses[0]
        
        # Determine action
        if "/list" in self.lhs.lower():
            if not house.db.member_roster and not house.db.members:
                self.caller.msg(f"{house.key} has no members.")
                return
            
            output = [f"\n|y{'Members of ' + house.key:=^78}|n"]
            
            # Use roster if available
            if house.db.member_roster:
                members = house.get_all_members()
                for member in sorted(members, key=lambda x: x[0].name):
                    character, info = member
                    char_line = f"  {character.name}"
                    if info.get('title'):
                        char_line += f" - {info['title']}"
                    output.append(char_line)
            else:
                # Legacy member list
                from evennia import ObjectDB
                members = ObjectDB.objects.filter(id__in=house.db.members)
                for member in sorted(members, key=lambda x: x.name):
                    output.append(f"  {member.name}")
            
            output.append(f"\nTotal: {len(house.db.member_roster) if house.db.member_roster else len(house.db.members)} member(s)")
            self.caller.msg("\n".join(output))
            
        elif "/add" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +house/member <house>/add=<character>")
                return
            
            character = self.caller.search(self.rhs.strip())
            if not character:
                return
            
            success, message = house.add_member(character)
            self.caller.msg(message)
            
        elif "/remove" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +house/member <house>/remove=<character>")
                return
            
            character = self.caller.search(self.rhs.strip())
            if not character:
                return
            
            success, message = house.remove_member(character)
            self.caller.msg(message)
        else:
            self.caller.msg("Usage: +house/member <house>/list|add|remove")
    
    def check_character_house(self):
        """Check which House a character serves."""
        char_name = self.args.strip() if self.args else self.lhs.strip()
        
        character = self.caller.search(char_name)
        if not character:
            return
        
        if hasattr(character.db, 'house') and character.db.house:
            self.caller.msg(f"{character.name} serves {character.db.house.key}.")
        else:
            self.caller.msg(f"{character.name} does not serve any House.")
