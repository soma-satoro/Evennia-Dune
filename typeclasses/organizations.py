"""
Organizations Typeclass

Schools, Guilds, and other organizations in the Dune universe.
These use the same roster system as Houses.
"""

from typeclasses.houses import House


# Organization types
ORG_TYPES = {
    'school': {
        'display': 'School',
        'description': 'Educational or training institution',
        'examples': ['Bene Gesserit', 'Suk School', 'Mentat School', 'Swordmaster School']
    },
    'guild': {
        'display': 'Guild',
        'description': 'Professional trade organization',
        'examples': ['Spacing Guild', 'CHOAM', 'Ixian Guild', 'Water Sellers Guild']
    },
    'order': {
        'display': 'Order',
        'description': 'Religious or ideological organization',
        'examples': ['Orange Catholic Bible Scholars', 'Zensunni Wanderers']
    },
    'faction': {
        'display': 'Faction',
        'description': 'Political or social movement',
        'examples': ['Fremen', 'Sardaukar', 'Fedaykin']
    }
}


class Organization(House):
    """
    A School, Guild, or other organization in the Dune universe.
    
    Similar to Houses but represents educational institutions, trade guilds,
    religious orders, and other organizations that characters can belong to.
    
    Organizations use the same roster system as Houses, allowing for:
    - Member tracking with titles and descriptions
    - Organizational hierarchy
    - Multiple character affiliations
    
    Only staff (builder+) can create and modify Organizations.
    """
    
    def at_object_creation(self):
        """Called when the Organization is first created."""
        super().at_object_creation()
        
        # Override some House-specific attributes
        self.db.org_type = "school"  # school, guild, order, faction
        
        # Organizations don't have all House attributes
        self.db.house_type = "Organization"  # Keep for compatibility
        
        # Organization-specific attributes
        self.db.headquarters = ""  # Main location
        self.db.leadership_structure = ""  # How the org is structured
        self.db.requirements = ""  # Requirements for membership
        self.db.benefits = ""  # Benefits of membership
        
        # Multiple characters can belong to multiple organizations
        self.db.allow_multiple = True  # Can belong to org AND a House
        
        # Set default locks
        self.locks.add("view:all();edit:perm(Builder);delete:perm(Admin)")
    
    def get_org_type_display(self):
        """Get display name for organization type."""
        return ORG_TYPES.get(self.db.org_type, {}).get('display', 'Organization')
    
    def add_member(self, character, title="", description=""):
        """
        Add a character as a member of this Organization.
        
        Organizations allow multiple affiliations, so characters
        can belong to an Organization and a House simultaneously.
        
        Args:
            character: Character object to add
            title (str): Optional title/rank in the Organization
            description (str): Optional description of their tie
            
        Returns:
            tuple: (success, message)
        """
        from django.utils import timezone
        
        if character.id in self.db.member_roster:
            return False, f"{character.name} is already a member of {self.key}."
        
        # Add to detailed roster
        self.db.member_roster[character.id] = {
            'title': title,
            'description': description,
            'date_joined': timezone.now()
        }
        
        # Legacy support
        if character.id not in self.db.members:
            self.db.members.append(character.id)
        
        # Organizations use a different attribute name
        if not hasattr(character.db, 'organizations'):
            character.db.organizations = []
        
        if self not in character.db.organizations:
            character.db.organizations.append(self)
        
        return True, f"{character.name} is now a member of {self.key}."
    
    def remove_member(self, character):
        """
        Remove a character from this Organization.
        
        Args:
            character: Character object to remove
            
        Returns:
            tuple: (success, message)
        """
        if character.id not in self.db.member_roster and character.id not in self.db.members:
            return False, f"{character.name} is not a member of {self.key}."
        
        # Remove from roster
        if character.id in self.db.member_roster:
            del self.db.member_roster[character.id]
        
        # Legacy support
        if character.id in self.db.members:
            self.db.members.remove(character.id)
        
        # Remove from character's organizations list
        if hasattr(character.db, 'organizations') and self in character.db.organizations:
            character.db.organizations.remove(self)
        
        return True, f"{character.name} has been removed from {self.key}."
    
    def get_display(self):
        """
        Get a formatted display of the Organization information.
        
        Returns:
            str: Formatted Organization information
        """
        output = []
        
        # Header
        output.append("|y" + "=" * 78 + "|n")
        output.append("|y" + f" {self.key} ".center(78, "=") + "|n")
        output.append("|y" + "=" * 78 + "|n")
        
        # Organization Type
        output.append(f"\n|wType:|n {self.get_org_type_display()}")
        
        # Headquarters
        if self.db.headquarters:
            output.append(f"|wHeadquarters:|n {self.db.headquarters}")
        
        # Leadership Structure
        if self.db.leadership_structure:
            output.append(f"\n|wLeadership:|n {self.db.leadership_structure}")
        
        # Requirements
        if self.db.requirements:
            output.append(f"\n|wMembership Requirements:|n")
            output.append(f"  {self.db.requirements}")
        
        # Benefits
        if self.db.benefits:
            output.append(f"\n|wMembership Benefits:|n")
            output.append(f"  {self.db.benefits}")
        
        # Traits
        if self.db.traits:
            output.append(f"\n|wOrganization Traits:|n {', '.join(self.db.traits)}")
        
        # Domains (for schools - areas of expertise)
        if self.db.primary_domains:
            output.append("\n|w" + "Primary Specializations".center(78, "-") + "|n")
            for i, domain in enumerate(self.db.primary_domains):
                output.append(f"  {i+1}. |c{domain['area']}|n: {domain['description']}")
        
        if self.db.secondary_domains:
            output.append("\n|w" + "Secondary Specializations".center(78, "-") + "|n")
            for i, domain in enumerate(self.db.secondary_domains):
                output.append(f"  {i+1}. |c{domain['area']}|n: {domain['description']}")
        
        # Key Roles
        if self.db.roles:
            output.append("\n|w" + "Key Positions".center(78, "-") + "|n")
            for role, info in sorted(self.db.roles.items()):
                traits_str = f" ({', '.join(info['traits'])})" if info.get('traits') else ""
                desc_str = f" - {info['description']}" if info.get('description') else ""
                output.append(f"  |c{role}:|n {info['character']}{traits_str}{desc_str}")
        
        # Members Roster
        if self.db.member_roster:
            output.append("\n|w" + f"Members ({len(self.db.member_roster)})".center(78, "-") + "|n")
            members = self.get_all_members()
            
            if members:
                # Sort by name
                members.sort(key=lambda x: x[0].name)
                
                for character, info in members:
                    char_line = f"  |c{character.name}|n"
                    
                    # Add title if present
                    if info.get('title'):
                        char_line += f" - {info['title']}"
                    
                    output.append(char_line)
                    
                    # Add description if present
                    if info.get('description'):
                        output.append(f"    {info['description']}")
            else:
                output.append(f"  {len(self.db.member_roster)} member(s)")
        elif self.db.members:  # Legacy support
            output.append("\n|w" + f"Members ({len(self.db.members)})".center(78, "-") + "|n")
            output.append(f"  {len(self.db.members)} member(s)")
        
        output.append("\n|y" + "=" * 78 + "|n")
        
        return "\n".join(output)


class School(Organization):
    """
    An educational or training institution in the Dune universe.
    
    Examples: Bene Gesserit, Suk School, Mentat School, Swordmaster Schools
    
    Schools train characters in specific disciplines and grant them
    special abilities or certifications.
    """
    
    def at_object_creation(self):
        """Called when the School is first created."""
        super().at_object_creation()
        self.db.org_type = "school"
        
        # School-specific attributes
        self.db.curriculum = []  # List of skills/subjects taught
        self.db.graduation_requirements = ""
        self.db.tuition = ""  # Cost or requirements for training


class Guild(Organization):
    """
    A professional trade organization in the Dune universe.
    
    Examples: Spacing Guild, CHOAM, Ixian Guild, Water Sellers Guild
    
    Guilds represent professional organizations that control
    specific industries or services in the Imperium.
    """
    
    def at_object_creation(self):
        """Called when the Guild is first created."""
        super().at_object_creation()
        self.db.org_type = "guild"
        
        # Guild-specific attributes
        self.db.industry = ""  # What industry/service the guild controls
        self.db.monopoly = False  # Does the guild have a monopoly?
        self.db.membership_dues = ""  # Cost of membership


class Order(Organization):
    """
    A religious or ideological organization in the Dune universe.
    
    Examples: Orange Catholic Bible Scholars, Zensunni Wanderers
    
    Orders represent religious, philosophical, or ideological groups.
    """
    
    def at_object_creation(self):
        """Called when the Order is first created."""
        super().at_object_creation()
        self.db.org_type = "order"
        
        # Order-specific attributes
        self.db.philosophy = ""  # Core beliefs/philosophy
        self.db.practices = ""  # Religious practices or rituals
        self.db.hierarchy = ""  # Religious hierarchy structure


class Faction(Organization):
    """
    A political or social movement in the Dune universe.
    
    Examples: Fremen, Sardaukar, Fedaykin
    
    Factions represent political movements, military units, or
    social groups with specific goals or identities.
    """
    
    def at_object_creation(self):
        """Called when the Faction is first created."""
        super().at_object_creation()
        self.db.org_type = "faction"
        
        # Faction-specific attributes
        self.db.goals = ""  # Political or social goals
        self.db.methods = ""  # How the faction operates
        self.db.reputation = ""  # How others view the faction

