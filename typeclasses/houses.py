"""
House Typeclass

Noble Houses for the Dune MUSH, implementing the Modiphius 2d20 system.
Houses are organizations that player characters serve.

This module requires builder+ permission to create and manage Houses.
"""

from evennia.objects.objects import DefaultObject
from evennia.utils.ansi import ANSIString


# Domain areas of expertise and their subtypes
DOMAIN_AREAS = {
    "Artistic": {
        "Machinery": ["Stage effects", "Scenery pieces", "Scenic art", "Lighting and sound systems"],
        "Produce": ["Plays", "Poems", "Novels", "Comedy sketches", "Musical pieces"],
        "Expertise": ["Playwrights", "Poets", "Composers", "Directors"],
        "Workers": ["Actors", "Stage crew", "Musicians", "Speakers", "Traveling companies"],
        "Understanding": ["Philosophy", "Literary criticism", "Theatrical performance styles"]
    },
    "Espionage": {
        "Machinery": ["Surveillance devices", "Sensors", "Jamming technology"],
        "Produce": ["Information and secrets from other Houses"],
        "Expertise": ["Spymasters", "Agent handlers"],
        "Workers": ["Agents", "Spies", "Infiltrators"],
        "Understanding": ["Espionage techniques", "Counterintelligence techniques"]
    },
    "Farming": {
        "Machinery": ["Tractors", "Harvesters", "Large-scale farming equipment"],
        "Produce": ["Crops", "Animal products", "Specialty foods"],
        "Expertise": ["Stewards", "Land managers"],
        "Workers": ["Farm laborers", "Shepherds", "Herders"],
        "Understanding": ["New farming techniques", "Rotation methods"]
    },
    "Industrial": {
        "Machinery": ["Factory machines", "Spacecraft", "Large vehicles"],
        "Produce": ["Mass-produced goods", "Refined alloys", "Consumer products"],
        "Expertise": ["Supervisors", "Business managers"],
        "Workers": ["Factory workers", "Craftsmen", "Mechanics"],
        "Understanding": ["Business management", "Factory operation techniques"]
    },
    "Kanly": {
        "Machinery": ["Hunter-seekers", "Mines", "Bombs", "Assassination weapons"],
        "Produce": ["Poisons", "Toxins", "Incapacitants"],
        "Expertise": ["Assassin masters", "Operation planners", "Trainers"],
        "Workers": ["Assassins", "Thugs", "Infiltration specialists"],
        "Understanding": ["Assassination methods", "Infiltration techniques", "Deadly combat strikes"]
    },
    "Military": {
        "Machinery": ["Battlefield weapons", "Artillery", "Large-scale shields", "Tanks"],
        "Produce": ["Ammunition", "Personal weapons", "Small arms"],
        "Expertise": ["Tacticians", "Officers", "Strategists"],
        "Workers": ["Soldiers", "Engineers", "Pilots", "Logistics personnel"],
        "Understanding": ["Military strategies", "New tactics"]
    },
    "Political": {
        "Machinery": ["Couture fashion", "Expensive trinkets", "Message services"],
        "Produce": ["Information", "Secrets", "Favors", "Political influence"],
        "Expertise": ["Political analysts", "Mediators", "Diplomats", "Fashionistas"],
        "Workers": ["Courtiers", "Spies", "Administrators", "Servants"],
        "Understanding": ["Diplomacy techniques", "Forms of etiquette"]
    },
    "Religion": {
        "Machinery": ["Churches", "Statues", "Prayer beads", "Religious symbols", "Religious books"],
        "Produce": ["Prayers", "Hymns", "Religious writings", "Inspirational texts"],
        "Expertise": ["Philosophers", "Clergy"],
        "Workers": ["Choristers", "Altar servants", "Community managers"],
        "Understanding": ["New religious philosophies", "New forms of faith"]
    },
    "Science": {
        "Machinery": ["Laboratory equipment", "Quarantine areas", "Scientific facilities"],
        "Produce": ["Chemical compounds", "Drugs", "Genetically-adapted organisms"],
        "Expertise": ["Scientists", "Researchers"],
        "Workers": ["Lab assistants", "Lab managers"],
        "Understanding": ["New scientific research", "Technological advances"]
    }
}

# House roles
HOUSE_ROLES = [
    "Ruler", "Consort", "Advisor", "Chief Physician", "Councilor", "Envoy",
    "Heir", "Marshal", "Scholar", "Spymaster", "Swordmaster", "Treasurer", "Warmaster"
]

# Enemy hatred levels
HATRED_LEVELS = {
    "Dislike": "Any interaction with this House is at +1 Difficulty, due to distrust",
    "Rival": "Actively seeks to bring the House down through gossip and politics",
    "Loathing": "Always has plans to destroy the House, but won't risk resources lightly",
    "Kanly": "Dedicated all resources to wiping out the House to the last person"
}

# Enemy reasons
ENEMY_REASONS = [
    "Competition", "Slight", "Debt", "Ancient Feud", "Morality", "Servitude",
    "Family Ties", "Theft", "Jealousy", "No Reason"
]


class House(DefaultObject):
    """
    A Noble House in the Dune universe.
    
    Houses are organizations that characters serve. They have various attributes:
    - House Type (Nascent, Minor, Major, Great)
    - Domains (primary and secondary areas of expertise)
    - Homeworld description
    - Banner (colors and crest)
    - House Traits
    - Key Roles (Ruler, Heir, etc.)
    - Enemy Houses
    
    Only staff (builder+) can create and modify Houses.
    """
    
    def at_object_creation(self):
        """Called when the House is first created."""
        super().at_object_creation()
        
        # House Type
        self.db.house_type = "Nascent House"  # Nascent, House Minor, House Major, Great House
        
        # Domains
        self.db.primary_domains = []  # List of {area, subtype, description}
        self.db.secondary_domains = []
        
        # Homeworld
        self.db.homeworld_name = ""
        self.db.homeworld_desc = ""
        self.db.weather = ""
        self.db.habitation = ""
        self.db.crime_rate = ""
        self.db.populace_mood = ""
        self.db.wealth_distribution = ""
        
        # Banner and Arms
        self.db.banner_colors = []  # e.g., ["White", "Red"]
        self.db.crest = ""  # e.g., "Scroll"
        
        # House Traits
        self.db.traits = []  # List of trait names
        
        # Roles - dict of role_name: {name, description, traits}
        self.db.roles = {}
        
        # Enemies - list of {house_name, hatred_level, reason}
        self.db.enemies = []
        
        # Members - now stores detailed member information
        # Format: {character_id: {'title': '', 'description': '', 'date_joined': datetime}}
        self.db.member_roster = {}
        self.db.members = []  # Legacy list for backward compatibility
        
        # Set default locks
        self.locks.add("view:all();edit:perm(Builder);delete:perm(Admin)")
    
    def get_threat_level(self):
        """
        Get the starting Threat per player based on House type.
        
        Returns:
            int: Threat level (0-3)
        """
        threat_map = {
            "Nascent House": 0,
            "House Minor": 1,
            "House Major": 2,
            "Great House": 3
        }
        return threat_map.get(self.db.house_type, 0)
    
    def get_domain_limits(self):
        """
        Get the number of primary and secondary domains allowed.
        
        Returns:
            tuple: (primary_count, secondary_count)
        """
        limits = {
            "Nascent House": (0, 1),
            "House Minor": (1, 1),
            "House Major": (1, 2),
            "Great House": (2, 3)
        }
        return limits.get(self.db.house_type, (0, 1))
    
    def add_domain(self, is_primary, area, subtype, description):
        """
        Add a domain to the House.
        
        Args:
            is_primary (bool): Whether this is a primary domain
            area (str): Domain area (e.g., "Artistic", "Military")
            subtype (str): Domain subtype (e.g., "Produce", "Workers")
            description (str): Specific description of this domain
            
        Returns:
            tuple: (success, message)
        """
        primary_limit, secondary_limit = self.get_domain_limits()
        
        if is_primary:
            if len(self.db.primary_domains) >= primary_limit:
                return False, f"House can only have {primary_limit} primary domain(s)."
            self.db.primary_domains.append({
                "area": area,
                "subtype": subtype,
                "description": description
            })
            # Add area as a trait if it's a primary domain
            if area not in self.db.traits:
                self.db.traits.append(area)
        else:
            if len(self.db.secondary_domains) >= secondary_limit:
                return False, f"House can only have {secondary_limit} secondary domain(s)."
            self.db.secondary_domains.append({
                "area": area,
                "subtype": subtype,
                "description": description
            })
        
        return True, "Domain added successfully."
    
    def remove_domain(self, is_primary, index):
        """
        Remove a domain by index.
        
        Args:
            is_primary (bool): Whether to remove from primary domains
            index (int): Index of the domain to remove
            
        Returns:
            tuple: (success, message)
        """
        domains = self.db.primary_domains if is_primary else self.db.secondary_domains
        
        if index < 0 or index >= len(domains):
            return False, "Invalid domain index."
        
        removed = domains.pop(index)
        
        # Remove trait if it was a primary domain
        if is_primary and removed["area"] in self.db.traits:
            self.db.traits.remove(removed["area"])
        
        return True, f"Removed domain: {removed['area']} - {removed['description']}"
    
    def set_role(self, role_name, character_name, description="", traits=None):
        """
        Assign a character to a House role.
        
        Args:
            role_name (str): Name of the role (e.g., "Ruler", "Heir")
            character_name (str): Name of the character filling this role
            description (str): Description of the character
            traits (list): List of trait strings for this character
            
        Returns:
            tuple: (success, message)
        """
        if role_name not in HOUSE_ROLES:
            return False, f"Invalid role. Valid roles: {', '.join(HOUSE_ROLES)}"
        
        self.db.roles[role_name] = {
            "character": character_name,
            "description": description,
            "traits": traits or []
        }
        
        return True, f"Set {role_name} to {character_name}."
    
    def remove_role(self, role_name):
        """
        Remove a character from a House role.
        
        Args:
            role_name (str): Name of the role to clear
            
        Returns:
            tuple: (success, message)
        """
        if role_name not in self.db.roles:
            return False, f"{role_name} is not currently filled."
        
        del self.db.roles[role_name]
        return True, f"Cleared {role_name} role."
    
    def add_enemy(self, house_name, hatred_level, reason):
        """
        Add an enemy House.
        
        Args:
            house_name (str): Name of the enemy House
            hatred_level (str): Level of hatred (Dislike, Rival, Loathing, Kanly)
            reason (str): Reason for the enmity
            
        Returns:
            tuple: (success, message)
        """
        if hatred_level not in HATRED_LEVELS:
            return False, f"Invalid hatred level. Valid: {', '.join(HATRED_LEVELS.keys())}"
        
        if reason not in ENEMY_REASONS:
            return False, f"Invalid reason. Valid: {', '.join(ENEMY_REASONS)}"
        
        self.db.enemies.append({
            "house": house_name,
            "hatred": hatred_level,
            "reason": reason
        })
        
        return True, f"Added enemy: {house_name} ({hatred_level})"
    
    def remove_enemy(self, index):
        """
        Remove an enemy House by index.
        
        Args:
            index (int): Index of the enemy to remove
            
        Returns:
            tuple: (success, message)
        """
        if index < 0 or index >= len(self.db.enemies):
            return False, "Invalid enemy index."
        
        removed = self.db.enemies.pop(index)
        return True, f"Removed enemy: {removed['house']}"
    
    def add_member(self, character, title="", description=""):
        """
        Add a character as a member of this House.
        
        Args:
            character: Character object to add
            title (str): Optional title/rank in the House
            description (str): Optional description of their tie to the House
            
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
        
        character.db.house = self
        
        return True, f"{character.name} is now a member of {self.key}."
    
    def remove_member(self, character):
        """
        Remove a character from this House.
        
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
        
        character.db.house = None
        
        return True, f"{character.name} has been removed from {self.key}."
    
    def set_member_title(self, character, title):
        """
        Set a member's title in the House.
        
        Args:
            character: Character object
            title (str): Title/rank in the House
            
        Returns:
            tuple: (success, message)
        """
        if character.id not in self.db.member_roster:
            return False, f"{character.name} is not a member of {self.key}."
        
        self.db.member_roster[character.id]['title'] = title
        return True, f"Set {character.name}'s title to: {title}"
    
    def set_member_description(self, character, description):
        """
        Set a member's description of their tie to the House.
        
        Args:
            character: Character object
            description (str): Description of tie to House
            
        Returns:
            tuple: (success, message)
        """
        if character.id not in self.db.member_roster:
            return False, f"{character.name} is not a member of {self.key}."
        
        self.db.member_roster[character.id]['description'] = description
        return True, f"Set {character.name}'s description."
    
    def get_member_info(self, character):
        """
        Get a member's roster information.
        
        Args:
            character: Character object
            
        Returns:
            dict: Member information or None
        """
        return self.db.member_roster.get(character.id)
    
    def get_all_members(self):
        """
        Get all members with their full information.
        
        Returns:
            list: List of (character, info_dict) tuples
        """
        from evennia import ObjectDB
        
        members = []
        for char_id, info in self.db.member_roster.items():
            try:
                character = ObjectDB.objects.get(id=char_id)
                members.append((character, info))
            except ObjectDB.DoesNotExist:
                continue
        
        return members
    
    def get_display(self):
        """
        Get a formatted display of the House information.
        
        Returns:
            str: Formatted House information
        """
        output = []
        
        # Header
        output.append("|y" + "=" * 78 + "|n")
        output.append("|y" + f" {self.key} ".center(78, "=") + "|n")
        output.append("|y" + "=" * 78 + "|n")
        
        # House Type and Threat
        output.append(f"\n|wHouse Type:|n {self.db.house_type}")
        output.append(f"|wThreat Level:|n {self.get_threat_level()} per player")
        
        # Banner
        if self.db.banner_colors or self.db.crest:
            colors = ", ".join(self.db.banner_colors) if self.db.banner_colors else "Not set"
            crest = self.db.crest if self.db.crest else "Not set"
            output.append(f"\n|wBanner Colors:|n {colors}")
            output.append(f"|wCrest:|n {crest}")
        
        # Traits
        if self.db.traits:
            output.append(f"\n|wHouse Traits:|n {', '.join(self.db.traits)}")
        
        # Primary Domains
        if self.db.primary_domains:
            output.append("\n|w" + "Primary Domains".center(78, "-") + "|n")
            for i, domain in enumerate(self.db.primary_domains):
                output.append(f"  {i+1}. |c{domain['area']}|n ({domain['subtype']}): {domain['description']}")
        
        # Secondary Domains
        if self.db.secondary_domains:
            output.append("\n|w" + "Secondary Domains".center(78, "-") + "|n")
            for i, domain in enumerate(self.db.secondary_domains):
                output.append(f"  {i+1}. |c{domain['area']}|n ({domain['subtype']}): {domain['description']}")
        
        # Homeworld
        if self.db.homeworld_name:
            output.append("\n|w" + "Homeworld".center(78, "-") + "|n")
            output.append(f"|wName:|n {self.db.homeworld_name}")
            if self.db.homeworld_desc:
                output.append(f"|wDescription:|n {self.db.homeworld_desc}")
            if self.db.weather:
                output.append(f"|wWeather:|n {self.db.weather}")
            if self.db.habitation:
                output.append(f"|wHabitation:|n {self.db.habitation}")
            if self.db.crime_rate:
                output.append(f"|wCrime Rate:|n {self.db.crime_rate}")
            if self.db.populace_mood:
                output.append(f"|wPopulace:|n {self.db.populace_mood}")
            if self.db.wealth_distribution:
                output.append(f"|wWealth Distribution:|n {self.db.wealth_distribution}")
        
        # Roles
        if self.db.roles:
            output.append("\n|w" + "Key Roles".center(78, "-") + "|n")
            for role, info in sorted(self.db.roles.items()):
                traits_str = f" ({', '.join(info['traits'])})" if info.get('traits') else ""
                desc_str = f" - {info['description']}" if info.get('description') else ""
                output.append(f"  |c{role}:|n {info['character']}{traits_str}{desc_str}")
        
        # Enemies
        if self.db.enemies:
            output.append("\n|w" + "Enemy Houses".center(78, "-") + "|n")
            for i, enemy in enumerate(self.db.enemies):
                output.append(f"  {i+1}. |r{enemy['house']}|n - {enemy['hatred']} ({enemy['reason']})")
                output.append(f"      {HATRED_LEVELS[enemy['hatred']]}")
        
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
                output.append(f"  {len(self.db.member_roster)} character(s) serve this House")
        elif self.db.members:  # Legacy support
            output.append("\n|w" + f"Members ({len(self.db.members)})".center(78, "-") + "|n")
            output.append(f"  {len(self.db.members)} character(s) serve this House")
        
        output.append("\n|y" + "=" * 78 + "|n")
        
        return "\n".join(output)

