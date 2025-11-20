"""
Roster Management Commands

Commands for managing and viewing House, School, and Guild rosters.
"""

from evennia.commands.default.muxcommand import MuxCommand
from evennia import search_object
from evennia.utils import evtable
from evennia.utils.utils import time_format
from django.utils import timezone


class CmdRoster(MuxCommand):
    """
    View the roster of a House, School, or Guild.
    
    Usage:
        +roster <organization>
        +roster/members <organization>
        +roster/full <organization>
        
    Switches:
        /members - Show only the members list
        /full - Show full detailed information
        
    Examples:
        +roster Atreides - View House Atreides roster
        +roster/members Molay - View only members of House Molay
        +roster/full Bene Gesserit - View full details of Bene Gesserit
        
    This command displays the member roster of a House, School, or Guild,
    showing each member's name, title/rank, and their tie to the organization.
    """
    
    key = "+roster"
    aliases = ["roster"]
    locks = "cmd:all()"
    help_category = "Dune"
    
    def func(self):
        """View organization roster"""
        
        if not self.args:
            self.caller.msg("Usage: +roster <organization>")
            return
        
        org_name = self.args.strip()
        
        # Search for the organization (could be House, School, Guild, etc.)
        orgs = search_object(org_name, typeclass="typeclasses.houses.House")
        
        if not orgs:
            # Try Organization typeclass
            orgs = search_object(org_name, typeclass="typeclasses.organizations.Organization")
        
        if not orgs:
            self.caller.msg(f"No organization found with the name '{org_name}'.")
            return
        
        if len(orgs) > 1:
            self.caller.msg(f"Multiple organizations found: {', '.join([o.key for o in orgs])}")
            return
        
        org = orgs[0]
        
        # Check if we should show full details or just members
        if "members" in self.switches:
            self.display_members_only(org)
        elif "full" in self.switches:
            self.display_full_roster(org)
        else:
            self.display_roster(org)
    
    def display_members_only(self, org):
        """Display just the members list."""
        members = org.get_all_members()
        
        if not members:
            self.caller.msg(f"{org.key} has no members.")
            return
        
        output = []
        output.append(f"\n|y{'=' * 78}|n")
        output.append(f"|y{f' {org.key} - Members ':=^78}|n")
        output.append(f"|y{'=' * 78}|n\n")
        
        # Sort by name
        members.sort(key=lambda x: x[0].name)
        
        for character, info in members:
            char_line = f"|c{character.name}|n"
            
            if info.get('title'):
                char_line += f" - {info['title']}"
            
            output.append(char_line)
            
            if info.get('description'):
                output.append(f"  {info['description']}")
            
            output.append("")
        
        output.append(f"|y{'=' * 78}|n")
        self.caller.msg("\n".join(output))
    
    def display_roster(self, org):
        """Display standard roster view."""
        output = []
        
        # Header
        output.append(f"\n|y{'=' * 78}|n")
        output.append(f"|y{f' {org.key} - Roster ':=^78}|n")
        output.append(f"|y{'=' * 78}|n")
        
        # Basic info
        output.append(f"\n|wType:|n {org.db.house_type}")
        
        if org.db.banner_colors and org.db.crest:
            colors = ", ".join(org.db.banner_colors)
            output.append(f"|wBanner:|n {colors} - {org.db.crest}")
        
        if org.db.traits:
            output.append(f"|wTraits:|n {', '.join(org.db.traits)}")
        
        # Members
        members = org.get_all_members()
        output.append(f"\n|w{f' Members ({len(members)}) ':-^78}|n")
        
        if members:
            # Sort by name
            members.sort(key=lambda x: x[0].name)
            
            for character, info in members:
                char_line = f"  |c{character.name}|n"
                
                if info.get('title'):
                    char_line += f" - {info['title']}"
                
                output.append(char_line)
                
                if info.get('description'):
                    # Wrap description if long
                    desc = info['description']
                    if len(desc) > 70:
                        desc = desc[:67] + "..."
                    output.append(f"    |x{desc}|n")
        else:
            output.append("  No members")
        
        output.append(f"\n|y{'=' * 78}|n")
        self.caller.msg("\n".join(output))
    
    def display_full_roster(self, org):
        """Display full detailed roster."""
        output = []
        
        # Header
        output.append(f"\n|y{'=' * 78}|n")
        output.append(f"|y{f' {org.key} - Full Roster ':=^78}|n")
        output.append(f"|y{'=' * 78}|n")
        
        # Organization info
        output.append(f"\n|wType:|n {org.db.house_type}")
        output.append(f"|wThreat Level:|n {org.get_threat_level()} per player")
        
        if org.db.banner_colors and org.db.crest:
            colors = ", ".join(org.db.banner_colors)
            output.append(f"|wBanner:|n {colors}")
            output.append(f"|wCrest:|n {org.db.crest}")
        
        if org.db.traits:
            output.append(f"|wTraits:|n {', '.join(org.db.traits)}")
        
        # Domains
        if org.db.primary_domains:
            output.append(f"\n|wPrimary Domains:|n")
            for domain in org.db.primary_domains:
                output.append(f"  • {domain['area']} - {domain['description']}")
        
        # Key Roles
        if org.db.roles:
            output.append(f"\n|w{' Key Roles ':-^78}|n")
            for role, info in sorted(org.db.roles.items()):
                output.append(f"  |c{role}:|n {info['character']}")
                if info.get('description'):
                    output.append(f"    {info['description']}")
        
        # Members
        members = org.get_all_members()
        output.append(f"\n|w{f' Members ({len(members)}) ':-^78}|n")
        
        if members:
            # Sort by title/name
            members.sort(key=lambda x: (x[1].get('title', '~'), x[0].name))
            
            for character, info in members:
                output.append(f"\n  |c{character.name}|n")
                
                if info.get('title'):
                    output.append(f"    |wTitle:|n {info['title']}")
                
                if info.get('description'):
                    output.append(f"    |wTie:|n {info['description']}")
                
                if info.get('date_joined'):
                    date_str = time_format(info['date_joined'].timestamp(), 3)
                    output.append(f"    |wJoined:|n {date_str}")
        else:
            output.append("  No members")
        
        output.append(f"\n|y{'=' * 78}|n")
        self.caller.msg("\n".join(output))


class CmdRosterSet(MuxCommand):
    """
    Manage member information in organization rosters (staff only).
    
    Usage:
        +rosterset <organization>/add <character>=<title>:<description>
        +rosterset <organization>/remove <character>
        +rosterset <organization>/title <character>=<title>
        +rosterset <organization>/desc <character>=<description>
        +rosterset <organization>/sync - Sync all members to new roster system
        
    Switches:
        /add - Add a member with title and description
        /remove - Remove a member
        /title - Set a member's title/rank
        /desc - Set a member's description/tie
        /sync - Migrate legacy members to new roster system
        
    Examples:
        +rosterset Molay/add Paul=Poet:Aspiring member of the poetry school
        +rosterset Molay/remove Paul
        +rosterset Molay/title Paul=Master Poet
        +rosterset Molay/desc Paul=Lead instructor at the northern academy
        +rosterset Molay/sync
        
    The title field represents the character's rank or position in the organization.
    The description field explains their tie or relationship to the organization.
    
    Staff Only: Requires Builder permission or higher.
    """
    
    key = "+rosterset"
    aliases = ["rosterset"]
    locks = "cmd:perm(Builder)"
    help_category = "Building"
    
    def func(self):
        """Manage roster membership"""
        
        if not self.args:
            self.caller.msg("Usage: +rosterset <organization>/<switch> <character>[=<value>]")
            self.caller.msg("See 'help +rosterset' for details.")
            return
        
        # Parse organization name
        if "/" in self.args:
            org_name = self.args.split("/")[0].strip()
        else:
            org_name = self.args.split()[0].strip() if self.args else ""
        
        # Find the organization (House or Organization)
        orgs = search_object(org_name, typeclass="typeclasses.houses.House")
        if not orgs:
            orgs = search_object(org_name, typeclass="typeclasses.organizations.Organization")
        
        if not orgs:
            self.caller.msg(f"No organization found with the name '{org_name}'.")
            return
        
        if len(orgs) > 1:
            self.caller.msg(f"Multiple organizations found: {', '.join([o.key for o in orgs])}")
            return
        
        org = orgs[0]
        
        # Handle switches
        if "add" in self.switches:
            self.add_member(org)
        elif "remove" in self.switches:
            self.remove_member(org)
        elif "title" in self.switches:
            self.set_title(org)
        elif "desc" in self.switches:
            self.set_description(org)
        elif "sync" in self.switches:
            self.sync_members(org)
        else:
            self.caller.msg("Invalid switch. Use: /add, /remove, /title, /desc, or /sync")
    
    def add_member(self, org):
        """Add a member to the organization."""
        # Parse: <org>/add <character>=<title>:<description>
        if "=" not in self.args:
            self.caller.msg("Usage: +rosterset <org>/add <character>=<title>:<description>")
            self.caller.msg("Example: +rosterset Molay/add Paul=Poet:Member of the poetry school")
            return
        
        char_part, value_part = self.args.split("=", 1)
        char_name = char_part.split("/")[-1].strip()
        
        # Parse title and description
        if ":" in value_part:
            title, description = value_part.split(":", 1)
            title = title.strip()
            description = description.strip()
        else:
            title = value_part.strip()
            description = ""
        
        # Find the character
        character = self.caller.search(char_name)
        if not character:
            return
        
        # Add to organization
        success, message = org.add_member(character, title, description)
        self.caller.msg(message)
        
        if success:
            self.caller.msg(f"Title: {title if title else '(none)'}")
            self.caller.msg(f"Description: {description if description else '(none)'}")
    
    def remove_member(self, org):
        """Remove a member from the organization."""
        # Parse: <org>/remove <character>
        char_name = self.args.split("/")[-1].strip()
        
        if not char_name or char_name == org.key:
            self.caller.msg("Usage: +rosterset <org>/remove <character>")
            return
        
        # Find the character
        character = self.caller.search(char_name)
        if not character:
            return
        
        # Remove from organization
        success, message = org.remove_member(character)
        self.caller.msg(message)
    
    def set_title(self, org):
        """Set a member's title."""
        # Parse: <org>/title <character>=<title>
        if "=" not in self.args:
            self.caller.msg("Usage: +rosterset <org>/title <character>=<title>")
            return
        
        char_part, title = self.args.split("=", 1)
        char_name = char_part.split("/")[-1].strip()
        title = title.strip()
        
        # Find the character
        character = self.caller.search(char_name)
        if not character:
            return
        
        # Set title
        success, message = org.set_member_title(character, title)
        self.caller.msg(message)
    
    def set_description(self, org):
        """Set a member's description."""
        # Parse: <org>/desc <character>=<description>
        if "=" not in self.args:
            self.caller.msg("Usage: +rosterset <org>/desc <character>=<description>")
            return
        
        char_part, description = self.args.split("=", 1)
        char_name = char_part.split("/")[-1].strip()
        description = description.strip()
        
        # Find the character
        character = self.caller.search(char_name)
        if not character:
            return
        
        # Set description
        success, message = org.set_member_description(character, description)
        self.caller.msg(message)
    
    def sync_members(self, org):
        """Sync legacy members to new roster system."""
        from evennia import ObjectDB
        from django.utils import timezone
        
        if not hasattr(org.db, 'members') or not org.db.members:
            self.caller.msg(f"{org.key} has no legacy members to sync.")
            return
        
        synced = 0
        skipped = 0
        
        for char_id in org.db.members:
            # Skip if already in roster
            if char_id in org.db.member_roster:
                skipped += 1
                continue
            
            try:
                character = ObjectDB.objects.get(id=char_id)
                org.db.member_roster[char_id] = {
                    'title': '',
                    'description': '',
                    'date_joined': timezone.now()
                }
                synced += 1
            except ObjectDB.DoesNotExist:
                continue
        
        self.caller.msg(f"Synced {synced} members to new roster system ({skipped} already synced).")


class CmdWho(MuxCommand):
    """
    Enhanced who command showing House affiliations.
    
    Usage:
        who
        who/house
        
    Switches:
        /house - Group players by House
        
    Shows all connected players, optionally grouped by their House affiliation.
    """
    
    key = "who"
    aliases = ["+who"]
    locks = "cmd:all()"
    help_category = "General"
    
    def func(self):
        """Show who is online"""
        from evennia import SESSION_HANDLER
        
        # Get all connected sessions
        sessions = SESSION_HANDLER.get_sessions()
        
        if not sessions:
            self.caller.msg("No players are currently connected.")
            return
        
        # Group by House if requested
        if "house" in self.switches:
            self.display_by_house(sessions)
        else:
            self.display_standard(sessions)
    
    def display_standard(self, sessions):
        """Standard who display with House affiliation."""
        output = []
        output.append(f"\n|y{'=' * 78}|n")
        output.append(f"|y{' Connected Players ':=^78}|n")
        output.append(f"|y{'=' * 78}|n\n")
        
        for session in sessions:
            character = session.get_puppet()
            if not character:
                continue
            
            char_line = f"|c{character.name}|n"
            
            # Add House affiliation if present
            if hasattr(character.db, 'house') and character.db.house:
                house = character.db.house
                char_line += f" |x(House {house.key})|n"
            
            # Add idle time
            idle = session.cmd_last_visible
            if idle:
                from evennia.utils.utils import time_format
                idle_str = time_format(idle, 0)
                char_line += f" - Idle: {idle_str}"
            
            output.append(char_line)
        
        output.append(f"\n|y{'=' * 78}|n")
        output.append(f"Total: {len(sessions)} connected")
        output.append(f"|y{'=' * 78}|n")
        
        self.caller.msg("\n".join(output))
    
    def display_by_house(self, sessions):
        """Display grouped by House."""
        from collections import defaultdict
        
        houses = defaultdict(list)
        
        for session in sessions:
            character = session.get_puppet()
            if not character:
                continue
            
            house_name = "No House"
            if hasattr(character.db, 'house') and character.db.house:
                house_name = character.db.house.key
            
            houses[house_name].append((character, session))
        
        output = []
        output.append(f"\n|y{'=' * 78}|n")
        output.append(f"|y{' Connected Players by House ':=^78}|n")
        output.append(f"|y{'=' * 78}|n\n")
        
        # Sort houses alphabetically, but put "No House" last
        sorted_houses = sorted([h for h in houses.keys() if h != "No House"])
        if "No House" in houses:
            sorted_houses.append("No House")
        
        for house_name in sorted_houses:
            members = houses[house_name]
            output.append(f"|w{house_name}|n ({len(members)})")
            
            for character, session in sorted(members, key=lambda x: x[0].name):
                char_line = f"  |c{character.name}|n"
                
                # Add idle time
                idle = session.cmd_last_visible
                if idle:
                    from evennia.utils.utils import time_format
                    idle_str = time_format(idle, 0)
                    char_line += f" - Idle: {idle_str}"
                
                output.append(char_line)
            
            output.append("")
        
        output.append(f"|y{'=' * 78}|n")
        output.append(f"Total: {len(sessions)} connected")
        output.append(f"|y{'=' * 78}|n")
        
        self.caller.msg("\n".join(output))

