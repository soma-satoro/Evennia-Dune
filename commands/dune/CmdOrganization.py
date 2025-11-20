"""
Organization Management Commands

Commands for creating and managing Schools, Guilds, Orders, and Factions.
Similar to House commands but for other organizations.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia import create_object, search_object
from typeclasses.organizations import ORG_TYPES


class CmdOrg(MuxCommand):
    """
    View information about an Organization.
    
    Usage:
        +org <name>
        +org/list [type]
        
    Switches:
        /list - List all Organizations (or filter by type)
        
    Types: school, guild, order, faction
        
    Examples:
        +org Bene Gesserit
        +org/list
        +org/list school
        
    This command displays comprehensive information about a School, Guild,
    Order, or Faction including its type, membership, and specializations.
    """
    
    key = "+org"
    aliases = ["org"]
    locks = "cmd:all()"
    help_category = "Dune"
    
    def func(self):
        """View Organization information"""
        
        # List all Organizations
        if "list" in self.switches:
            # Optional type filter
            org_type_filter = self.args.strip().lower() if self.args else None
            
            if org_type_filter and org_type_filter not in ORG_TYPES:
                self.caller.msg(f"Invalid type. Valid types: {', '.join(ORG_TYPES.keys())}")
                return
            
            orgs = search_object(typeclass="typeclasses.organizations.Organization")
            
            if not orgs:
                self.caller.msg("No Organizations have been created yet.")
                return
            
            # Filter by type if specified
            if org_type_filter:
                orgs = [o for o in orgs if o.db.org_type == org_type_filter]
                if not orgs:
                    self.caller.msg(f"No Organizations of type '{org_type_filter}' found.")
                    return
            
            self.caller.msg("|y" + "=" * 78 + "|n")
            self.caller.msg("|y" + " Organizations ".center(78, "=") + "|n")
            self.caller.msg("|y" + "=" * 78 + "|n")
            
            for org in sorted(orgs, key=lambda x: x.key):
                org_type = org.get_org_type_display()
                member_count = len(org.db.member_roster) if org.db.member_roster else 0
                self.caller.msg(f"  |c{org.key}|n - {org_type} ({member_count} members)")
            
            self.caller.msg("|y" + "=" * 78 + "|n")
            return
        
        # View specific Organization
        if not self.args:
            self.caller.msg("Usage: +org <name> or +org/list")
            return
        
        # Search for the Organization
        orgs = search_object(self.args.strip(), typeclass="typeclasses.organizations.Organization")
        if not orgs:
            self.caller.msg(f"No Organization found with the name '{self.args.strip()}'.")
            return
        
        if len(orgs) > 1:
            self.caller.msg(f"Multiple Organizations found: {', '.join([o.key for o in orgs])}")
            return
        
        org = orgs[0]
        self.caller.msg(org.get_display())


class CmdOrgCreate(MuxCommand):
    """
    Create a new Organization (staff only).
    
    Usage:
        +orgcreate <name>=<type>
        
    Organization Types:
        school - Educational or training institution
        guild - Professional trade organization
        order - Religious or ideological organization
        faction - Political or social movement
        
    Examples:
        +orgcreate Bene Gesserit=school
        +orgcreate Spacing Guild=guild
        +orgcreate Zensunni Wanderers=order
        +orgcreate Fremen=faction
        
    This creates a new Organization with the specified type. Further configuration
    is done with +orgset and +rosterset commands.
    
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+orgcreate"
    aliases = ["orgcreate"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Create a new Organization"""
        
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +orgcreate <name>=<type>")
            self.caller.msg(f"Types: {', '.join(ORG_TYPES.keys())}")
            return
        
        org_name, org_type = self.args.split("=", 1)
        org_name = org_name.strip()
        org_type = org_type.strip().lower()
        
        # Validate org type
        if org_type not in ORG_TYPES:
            self.caller.msg(f"Invalid organization type. Valid types: {', '.join(ORG_TYPES.keys())}")
            return
        
        # Check if Organization already exists
        existing = search_object(org_name, typeclass="typeclasses.organizations.Organization")
        if existing:
            self.caller.msg(f"An Organization named '{org_name}' already exists.")
            return
        
        # Choose the appropriate typeclass
        typeclass_map = {
            'school': "typeclasses.organizations.School",
            'guild': "typeclasses.organizations.Guild",
            'order': "typeclasses.organizations.Order",
            'faction': "typeclasses.organizations.Faction"
        }
        
        typeclass = typeclass_map.get(org_type, "typeclasses.organizations.Organization")
        
        # Create the Organization
        org = create_object(
            typeclass=typeclass,
            key=org_name,
            location=None
        )
        
        self.caller.msg(f"|gCreated {org_name} as a {ORG_TYPES[org_type]['display']}.|n")
        self.caller.msg(f"Use +orgset to configure details and +rosterset to manage members.")


class CmdOrgSet(MuxCommand):
    """
    Set properties of an Organization (staff only).
    
    Usage:
        +orgset <org>/type=<type>
        +orgset <org>/trait=<trait name>
        +orgset <org>/headquarters=<location>
        +orgset <org>/leadership=<structure>
        +orgset <org>/requirements=<text>
        +orgset <org>/benefits=<text>
        +orgset <org>/curriculum=<skill> (schools)
        +orgset <org>/industry=<industry> (guilds)
        +orgset <org>/philosophy=<text> (orders)
        +orgset <org>/goals=<text> (factions)
        
    Switches:
        /type - Set organization type
        /trait - Add an organization trait
        /headquarters - Set main location
        /leadership - Set leadership structure
        /requirements - Set membership requirements
        /benefits - Set membership benefits
        /curriculum - Add to curriculum (schools only)
        /industry - Set industry (guilds only)
        /philosophy - Set philosophy (orders only)
        /goals - Set goals (factions only)
        
    Examples:
        +orgset Bene Gesserit/type=school
        +orgset Bene Gesserit/trait=Secretive
        +orgset Bene Gesserit/headquarters=Wallach IX
        +orgset Bene Gesserit/requirements=Female only, rigorous testing
        +orgset Bene Gesserit/benefits=Enhanced abilities, Voice training
        +orgset Spacing Guild/industry=Interstellar travel and navigation
        
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+orgset"
    aliases = ["orgset"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Set Organization properties"""
        
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +orgset <org>/<switch>=<value>")
            self.caller.msg("See 'help +orgset' for available switches.")
            return
        
        org_name, value = self.args.split("=", 1)
        org_name = org_name.strip()
        value = value.strip()
        
        # Find the Organization
        orgs = search_object(org_name, typeclass="typeclasses.organizations.Organization")
        if not orgs:
            self.caller.msg(f"No Organization found with the name '{org_name}'.")
            return
        
        if len(orgs) > 1:
            self.caller.msg(f"Multiple Organizations found: {', '.join([o.key for o in orgs])}")
            return
        
        org = orgs[0]
        
        # Handle switches
        if "type" in self.switches:
            value_lower = value.lower()
            if value_lower not in ORG_TYPES:
                self.caller.msg(f"Invalid type. Valid: {', '.join(ORG_TYPES.keys())}")
                return
            org.db.org_type = value_lower
            self.caller.msg(f"Set {org.key} type to {ORG_TYPES[value_lower]['display']}.")
            
        elif "trait" in self.switches:
            if value not in org.db.traits:
                org.db.traits.append(value)
                self.caller.msg(f"Added trait '{value}' to {org.key}.")
            else:
                self.caller.msg(f"{org.key} already has the trait '{value}'.")
                
        elif "headquarters" in self.switches:
            org.db.headquarters = value
            self.caller.msg(f"Set {org.key} headquarters to: {value}")
            
        elif "leadership" in self.switches:
            org.db.leadership_structure = value
            self.caller.msg(f"Set {org.key} leadership structure.")
            
        elif "requirements" in self.switches:
            org.db.requirements = value
            self.caller.msg(f"Set {org.key} membership requirements.")
            
        elif "benefits" in self.switches:
            org.db.benefits = value
            self.caller.msg(f"Set {org.key} membership benefits.")
            
        elif "curriculum" in self.switches:
            if org.db.org_type != "school":
                self.caller.msg("Curriculum is only for schools.")
                return
            if not hasattr(org.db, 'curriculum'):
                org.db.curriculum = []
            if value not in org.db.curriculum:
                org.db.curriculum.append(value)
                self.caller.msg(f"Added '{value}' to {org.key} curriculum.")
            else:
                self.caller.msg(f"'{value}' is already in the curriculum.")
                
        elif "industry" in self.switches:
            if org.db.org_type != "guild":
                self.caller.msg("Industry is only for guilds.")
                return
            org.db.industry = value
            self.caller.msg(f"Set {org.key} industry to: {value}")
            
        elif "philosophy" in self.switches:
            if org.db.org_type != "order":
                self.caller.msg("Philosophy is only for orders.")
                return
            org.db.philosophy = value
            self.caller.msg(f"Set {org.key} philosophy.")
            
        elif "goals" in self.switches:
            if org.db.org_type != "faction":
                self.caller.msg("Goals are only for factions.")
                return
            org.db.goals = value
            self.caller.msg(f"Set {org.key} goals.")
            
        else:
            self.caller.msg("Invalid switch. See 'help +orgset' for available switches.")


class CmdOrgRole(MuxCommand):
    """
    Manage Organization positions and roles (staff only).
    
    Usage:
        +orgrole <org>/list
        +orgrole <org>/set <role>=<character name>[:<description>][:<traits>]
        +orgrole <org>/remove <role>
        
    Switches:
        /list - List all roles and current holders
        /set - Assign a character to a role
        /remove - Clear a role
        
    Common Roles for Organizations:
        Schools: Headmaster, Proctor, Instructor, Dean
        Guilds: Guildmaster, Treasurer, Representative
        Orders: High Priest/Priestess, Elder, Keeper
        Factions: Leader, Commander, Spokesman
        
    Examples:
        +orgrole Bene Gesserit/list
        +orgrole Bene Gesserit/set Reverend Mother=Gaius Helen Mohiam
        +orgrole Bene Gesserit/set Proctor=Lady Margot:Proctor of Arrakis
        +orgrole Spacing Guild/set Navigator=Edric:Steersman
        
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+orgrole"
    aliases = ["orgrole"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Manage Organization roles"""
        
        if not self.args:
            self.caller.msg("Usage: +orgrole <org>/<switch>[=<value>]")
            self.caller.msg("See 'help +orgrole' for details.")
            return
        
        # Parse org name
        if "/" in self.args:
            org_name = self.args.split("/")[0].strip()
        else:
            org_name = self.args.strip()
        
        # Find the Organization
        orgs = search_object(org_name, typeclass="typeclasses.organizations.Organization")
        if not orgs:
            self.caller.msg(f"No Organization found with the name '{org_name}'.")
            return
        
        if len(orgs) > 1:
            self.caller.msg(f"Multiple Organizations found: {', '.join([o.key for o in orgs])}")
            return
        
        org = orgs[0]
        
        # Handle switches (reuse House logic)
        if "list" in self.switches:
            output = [f"\n|y{'Roles for ' + org.key:=^78}|n"]
            
            if org.db.roles:
                output.append(f"\n|wFilled Roles:|n")
                for role, info in sorted(org.db.roles.items()):
                    traits_str = f" ({', '.join(info['traits'])})" if info.get('traits') else ""
                    desc_str = f" - {info['description']}" if info.get('description') else ""
                    output.append(f"  |c{role}:|n {info['character']}{traits_str}{desc_str}")
            else:
                output.append(f"\n|wFilled Roles:|n None")
            
            self.caller.msg("\n".join(output))
            
        elif "set" in self.switches:
            if "=" not in self.args:
                self.caller.msg("Usage: +orgrole <org>/set <role>=<character>[:<description>][:<traits>]")
                return
            
            role_part, value = self.args.split("=", 1)
            role_name = role_part.split("/")[-1].strip()
            
            # Parse value (character:description:traits)
            parts = value.split(":")
            character_name = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            traits = [t.strip() for t in parts[2].split(",")] if len(parts) > 2 else []
            
            success, message = org.set_role(role_name, character_name, description, traits)
            self.caller.msg(message)
            
        elif "remove" in self.switches:
            role_name = self.args.split("/")[-1].strip()
            success, message = org.remove_role(role_name)
            self.caller.msg(message)
            
        else:
            self.caller.msg("Invalid switch. See 'help +orgrole' for available switches.")

