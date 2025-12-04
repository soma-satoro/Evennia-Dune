"""
Organization Management Commands

Consolidated command for creating and managing Schools, Guilds, Orders, and Factions.
All commands require builder+ permission except viewing.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia import create_object, search_object
from typeclasses.organizations import ORG_TYPES


class CmdOrg(MuxCommand):
    """
    View and manage Organizations (Schools, Guilds, Orders, Factions).

    Usage:
        +org <name> | +org/list [type]
        +org/create <name>=<type> | +org/destroy <name> (staff only)
        +org/set <org>/type=<type> | +org/set <org>/trait=<trait> | +org/set <org>/headquarters=<loc> (staff only)
        +org/set <org>/leadership=<text> | +org/set <org>/requirements=<text> | +org/set <org>/benefits=<text> (staff only)
        +org/set <org>/quote=<text> (staff only)
        +org/set <org>/curriculum=<skill> (schools) | +org/set <org>/industry=<text> (guilds) | +org/set <org>/philosophy=<text> (orders) | +org/set <org>/goals=<text> (factions) (staff only)
        +org/role <org>/list | +org/role <org>/set <role>=<name>[:<desc>][:<traits>] | +org/role <org>/remove <role> (staff only)

    Organization Types: school (educational/training), guild (professional trade), order (religious/ideological), faction (political/social movement)

    Examples:
        +org Bene Gesserit | +org/list school | +org/create Bene Gesserit=school
        +org/set Bene Gesserit/trait=Secretive | +org/set Bene Gesserit/headquarters=Wallach IX
        +org/role Bene Gesserit/set Reverend Mother=Gaius Helen Mohiam

    Staff Only: All management commands require Builder permission or higher.
    """
    
    key = "+org"
    aliases = ["org"]
    locks = "cmd:all()"
    help_category = "Dune"
    
    def func(self):
        """Main command dispatcher"""
        
        # Check for staff-only switches
        staff_switches = ['create', 'destroy', 'set', 'role']
        needs_staff = any(sw in self.switches for sw in staff_switches)
        
        if needs_staff:
            if not self.caller.check_permstring("Builder"):
                self.caller.msg("You need Builder permission or higher to manage Organizations.")
                return
        
        # Route to appropriate handler
        if "list" in self.switches:
            self.list_organizations()
        elif "create" in self.switches:
            self.create_organization()
        elif "destroy" in self.switches:
            self.destroy_organization()
        elif "set" in self.switches:
            self.set_property()
        elif "role" in self.switches:
            self.manage_roles()
        elif not self.switches:
            # No switches - view an Organization
            self.view_organization()
        else:
            self.caller.msg("Invalid switch. See 'help +org' for available options.")
    
    def list_organizations(self):
        """List all Organizations."""
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
    
    def view_organization(self):
        """View specific Organization information."""
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
    
    def create_organization(self):
        """Create a new Organization."""
        if not self.args or "=" not in self.args:
            self.caller.msg("Usage: +org/create <name>=<type>")
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
        self.caller.msg(f"Use +org/set to configure details and +rosterset to manage members.")
    
    def destroy_organization(self):
        """Destroy an Organization."""
        if not self.args:
            self.caller.msg("Usage: +org/destroy <organization name>")
            return
        
        orgs = search_object(self.args.strip(), typeclass="typeclasses.organizations.Organization")
        if not orgs:
            self.caller.msg(f"No Organization found with the name '{self.args.strip()}'.")
            return
        
        if len(orgs) > 1:
            self.caller.msg(f"Multiple Organizations found: {', '.join([o.key for o in orgs])}")
            return
        
        org = orgs[0]
        org_name = org.key
        
        # Remove Organization affiliation from all members
        if org.db.member_roster:
            from evennia import ObjectDB
            for char_id in org.db.member_roster.keys():
                try:
                    character = ObjectDB.objects.get(id=char_id)
                    if hasattr(character.db, 'organizations') and org in character.db.organizations:
                        character.db.organizations.remove(org)
                except ObjectDB.DoesNotExist:
                    pass
        
        org.delete()
        self.caller.msg(f"|rDestroyed Organization {org_name}.|n")
    
    def set_property(self):
        """Set Organization properties."""
        if not self.lhs or "=" not in self.args:
            self.caller.msg("Usage: +org/set <org>/<property>=<value>")
            self.caller.msg("See 'help +org' for available properties.")
            return
        
        # Parse org name from lhs (before the /)
        parts = self.lhs.split("/")
        if len(parts) < 2:
            self.caller.msg("Usage: +org/set <org>/<property>=<value>")
            return
        
        org_name = parts[0].strip()
        property_name = parts[1].strip().lower()
        value = self.rhs.strip()
        
        # Find the Organization
        orgs = search_object(org_name, typeclass="typeclasses.organizations.Organization")
        if not orgs:
            self.caller.msg(f"No Organization found with the name '{org_name}'.")
            return
        
        if len(orgs) > 1:
            self.caller.msg(f"Multiple Organizations found: {', '.join([o.key for o in orgs])}")
            return
        
        org = orgs[0]
        
        # Handle different properties
        if property_name == "type":
            value_lower = value.lower()
            if value_lower not in ORG_TYPES:
                self.caller.msg(f"Invalid type. Valid: {', '.join(ORG_TYPES.keys())}")
                return
            org.db.org_type = value_lower
            self.caller.msg(f"Set {org.key} type to {ORG_TYPES[value_lower]['display']}.")
            
        elif property_name == "trait":
            if value not in org.db.traits:
                org.db.traits.append(value)
                self.caller.msg(f"Added trait '{value}' to {org.key}.")
            else:
                self.caller.msg(f"{org.key} already has the trait '{value}'.")
                
        elif property_name == "headquarters":
            org.db.headquarters = value
            self.caller.msg(f"Set {org.key} headquarters to: {value}")
            
        elif property_name == "leadership":
            org.db.leadership_structure = value
            self.caller.msg(f"Set {org.key} leadership structure.")
            
        elif property_name == "requirements":
            org.db.requirements = value
            self.caller.msg(f"Set {org.key} membership requirements.")
            
        elif property_name == "benefits":
            org.db.benefits = value
            self.caller.msg(f"Set {org.key} membership benefits.")
            
        elif property_name == "quote":
            org.db.quote = value
            self.caller.msg(f"Set {org.key} quote to: \"{value}\"")
            
        elif property_name == "curriculum":
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
                
        elif property_name == "industry":
            if org.db.org_type != "guild":
                self.caller.msg("Industry is only for guilds.")
                return
            org.db.industry = value
            self.caller.msg(f"Set {org.key} industry to: {value}")
            
        elif property_name == "philosophy":
            if org.db.org_type != "order":
                self.caller.msg("Philosophy is only for orders.")
                return
            org.db.philosophy = value
            self.caller.msg(f"Set {org.key} philosophy.")
            
        elif property_name == "goals":
            if org.db.org_type != "faction":
                self.caller.msg("Goals are only for factions.")
                return
            org.db.goals = value
            self.caller.msg(f"Set {org.key} goals.")
            
        else:
            self.caller.msg(f"Unknown property '{property_name}'. See 'help +org' for available properties.")
    
    def manage_roles(self):
        """Manage Organization roles."""
        if not self.lhs:
            self.caller.msg("Usage: +org/role <org>/<action>[=<value>]")
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
        
        # Determine action
        if "/list" in self.lhs.lower():
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
            
        elif "/set" in self.lhs.lower():
            if "=" not in self.args:
                self.caller.msg("Usage: +org/role <org>/set <role>=<character>[:<description>][:<traits>]")
                return
            
            # Role name is between /set and =
            lhs_parts = self.lhs.split("/")
            if len(lhs_parts) < 3:
                self.caller.msg("Usage: +org/role <org>/set <role>=<character>[:<description>][:<traits>]")
                return
            
            role_name = lhs_parts[2].strip()
            
            # Parse value (character:description:traits)
            parts = self.rhs.split(":")
            character_name = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            traits = [t.strip() for t in parts[2].split(",")] if len(parts) > 2 else []
            
            success, message = org.set_role(role_name, character_name, description, traits)
            self.caller.msg(message)
            
        elif "/remove" in self.lhs.lower():
            # Role name is after /remove
            lhs_parts = self.lhs.split("/")
            if len(lhs_parts) < 3:
                self.caller.msg("Usage: +org/role <org>/remove <role>")
                return
            
            role_name = lhs_parts[2].strip()
            success, message = org.remove_role(role_name)
            self.caller.msg(message)
        else:
            self.caller.msg("Usage: +org/role <org>/list|set|remove")

